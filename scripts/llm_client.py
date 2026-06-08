"""
LLM 客户端 - 兼容 OpenAI API 格式
支持两种模式：
  1. 分步模式（有 LaTeX section 结构时）：评分 → 章节规划 → 6次单问
  2. 一次性模式（abstract-only 回退）：评分+Q&A 一次完成
"""

import json
import logging
import os
import time
import urllib.request
from typing import Optional

from paper_content import get_section_list, get_section_previews, extract_sections

logger = logging.getLogger(__name__)

# prompt 文件目录
_PROMPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")

# 固定 6 个问题：(问题文本, prompt 文件名)
QA_QUESTIONS = [
    ("这篇论文试图解决什么问题？", "qa_1_problem.txt"),
    ("有哪些相关研究？", "qa_2_related_work.txt"),
    ("论文如何解决这个问题？", "qa_3_method.txt"),
    ("论文做了哪些实验？", "qa_4_experiment.txt"),
    ("有什么可以进一步探索的点？", "qa_5_further.txt"),
    ("总结一下论文的主要内容", "qa_6_summary.txt"),
]


def _load_prompt(name: str) -> str:
    """从 prompts/ 目录加载 prompt 模板文件。"""
    path = os.path.join(_PROMPTS_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def call_llm(
    messages: list[dict],
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 2000,
    timeout: int = 60,
) -> str:
    """调用 OpenAI 兼容 API"""
    model = model or os.environ.get("LLM_MODEL", "gpt-4o-mini")
    base_url = base_url or os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    api_key = api_key or os.environ.get("LLM_API_KEY", "")

    base_url = base_url.rstrip("/")
    url = f"{base_url}/chat/completions"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                logger.warning("LLM API 请求失败 (attempt %d): %s, 等待 %ds...", attempt + 1, e, wait)
                time.sleep(wait)
            else:
                raise RuntimeError(f"LLM API 请求失败 (已重试 3 次): {e}")


def _parse_llm_json(response: str) -> dict:
    """从 LLM 响应中解析 JSON，处理 markdown code block 包裹。"""
    response = response.strip()
    if response.startswith("```"):
        response = response.split("\n", 1)[1]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
    return json.loads(response)


def quick_relevance_check(paper: dict, config: dict) -> float | None:
    """
    基于摘要快速预评分，仅返回相关度分数。
    用于在获取全文前过滤掉低相关度论文，节省全文获取和完整评分的开销。
    返回分数 (1-10)，失败返回 None。
    """
    llm_config = config.get("llm", {})
    network_config = config.get("network", {})

    system_prompt = _load_prompt("system.txt")
    user_prompt = _load_prompt("quick_check.txt").format_map({
        "title": paper["title"],
        "categories": ", ".join(paper["categories"]),
        "summary": paper["summary"],
    })

    temperature = llm_config.get("temperature", 0.3)
    timeout = network_config.get("request_timeout", 60)

    try:
        response = call_llm(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=100,
            timeout=timeout,
        )

        result = _parse_llm_json(response)
        return float(result.get("relevance_score", 0))

    except Exception as e:
        logger.warning("预评分失败: %s", e)
        return None


def _build_authors_str(paper: dict) -> str:
    """构建作者字符串。"""
    authors_str = ", ".join(
        f"{a['name']}" + (f" ({a['affiliation']})" if a["affiliation"] else "")
        for a in paper["authors"][:10]
    )
    if len(paper["authors"]) > 10:
        authors_str += f" 等共 {len(paper['authors'])} 位作者"
    return authors_str


def _score_paper(paper: dict, config: dict) -> Optional[dict]:
    """
    第一步：评分 + 标签（轻量调用）。
    返回 {"relevance_score": float, "tags": list} 或 None。
    """
    llm_config = config.get("llm", {})
    network_config = config.get("network", {})

    system_prompt = _load_prompt("system.txt")
    user_prompt = _load_prompt("score_only.txt").format_map({
        "title": paper["title"],
        "authors": _build_authors_str(paper),
        "categories": ", ".join(paper["categories"]),
        "summary": paper["summary"],
    })

    try:
        response = call_llm(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=llm_config.get("temperature", 0.3),
            max_tokens=200,
            timeout=network_config.get("request_timeout", 90),
        )
        result = _parse_llm_json(response)
        if "relevance_score" not in result or "tags" not in result:
            logger.warning("评分返回缺少字段")
            return None
        return result
    except Exception as e:
        logger.warning("评分失败: %s", e)
        return None


def _plan_sections(
    paper: dict,
    sections: list[str],
    config: dict,
    latex_content: str = "",
    preview_sections: list[str] | None = None,
) -> Optional[dict]:
    """
    第二步：章节规划。给 LLM 目录（含 subsection 预览），返回每个 Q 对应的 section 列表。
    preview_sections: 包含 subsection 的完整目录（用于生成预览），LLM 只需返回 section 级别的名称。
    返回 {"Q1": [...], "Q2": [...], ...} 或 None。
    """
    network_config = config.get("network", {})
    llm_config = config.get("llm", {})

    preview_chars = config.get("paper_content", {}).get("section_preview_chars", 256)
    # 用包含 subsection 的目录生成预览，让 LLM 看到更多结构信息
    toc_sections = preview_sections if preview_sections else sections
    if latex_content and preview_chars > 0:
        sections_list = get_section_previews(latex_content, toc_sections, preview_chars)
    else:
        sections_list = "\n".join(f"- {s}" for s in toc_sections)

    system_prompt = _load_prompt("system.txt")
    user_prompt = _load_prompt("section_planning.txt").format_map({
        "title": paper["title"],
        "summary": paper["summary"],
        "sections_list": sections_list,
    })

    try:
        response = call_llm(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=llm_config.get("temperature", 0.3),
            max_tokens=300,
            timeout=network_config.get("request_timeout", 90),
        )
        plan = _parse_llm_json(response)
        # 验证格式
        for key in ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]:
            if key not in plan or not isinstance(plan[key], list):
                plan[key] = []
        return plan
    except Exception as e:
        logger.warning("章节规划失败: %s", e)
        return None


def _ask_single_question(
    paper: dict,
    question: str,
    prompt_file: str,
    section_content: str,
    config: dict,
) -> Optional[str]:
    """
    第三步（单次）：用对应 section 内容回答一个问题。
    prompt_file: 该问题对应的 prompt 模板文件名。
    返回 answer 字符串或 None。
    """
    llm_config = config.get("llm", {})
    network_config = config.get("network", {})

    if section_content:
        section_block = f"\n以下是论文相关章节内容:\n{section_content}"
    else:
        section_block = ""

    system_prompt = _load_prompt("system.txt")
    user_prompt = _load_prompt(prompt_file).format_map({
        "title": paper["title"],
        "summary": paper["summary"],
        "section_block": section_block,
    })

    max_tokens = llm_config.get("max_tokens_single_qa", 800)

    try:
        response = call_llm(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=llm_config.get("temperature", 0.3),
            max_tokens=max_tokens,
            timeout=network_config.get("request_timeout", 90),
        )
        answer = response.strip()
        if not answer:
            return None
        return answer
    except Exception as e:
        logger.warning("单问失败 (%s): %s", question[:20], e)
        return None


def score_and_summarize(
    paper: dict,
    config: dict,
    full_content: Optional[str] = None,
    content_source: Optional[str] = None,
) -> Optional[dict]:
    """
    对单篇论文进行评分和 Q&A 解读。

    有 LaTeX 源码时使用分步模式（评分 → 规划 → 6次单问），更省 token。
    仅有 PDF 或仅摘要时回退为一次性模式。

    返回: {relevance_score, tags, qa_pairs: [{question, answer}, ...]}
    如果论文不相关(评分低于阈值)则返回 None。
    """
    llm_config = config.get("llm", {})
    min_score = llm_config.get("min_relevance_score", 4)

    # ── 分步模式：有 LaTeX 源码，可以用 section 结构 ──
    if full_content and content_source == "latex":
        sections = get_section_list(full_content, include_subsections=False)
        sections_with_subs = get_section_list(full_content, include_subsections=True)

        if sections:
            # Step 1: 评分 + 标签
            score_result = _score_paper(paper, config)
            if not score_result:
                return None
            if score_result["relevance_score"] < min_score:
                return None

            # Step 2: 章节规划（给 LLM 看 section+subsection 预览，只返回 section 名）
            plan = _plan_sections(paper, sections, config, latex_content=full_content, preview_sections=sections_with_subs)
            if not plan:
                # 规划失败，回退到无规划逐问（每问不带 section）
                logger.warning("章节规划失败，回退为无 section 逐问")
                plan = {f"Q{i+1}": [] for i in range(6)}

            # Step 3: 6 次单问
            max_chars = config.get("paper_content", {}).get("max_section_chars", 15000)
            qa_pairs = []
            for i, (question, prompt_file) in enumerate(QA_QUESTIONS):
                key = f"Q{i+1}"
                needed_sections = plan.get(key, [])
                section_text = extract_sections(full_content, needed_sections, max_chars_per_section=max_chars, all_sections=sections) if needed_sections else ""
                logger.info("    Q%d: %d 个 section, %d 字符", i + 1, len(needed_sections), len(section_text))

                answer = _ask_single_question(paper, question, prompt_file, section_text, config)
                if answer:
                    qa_pairs.append({"question": question, "answer": answer})
                else:
                    qa_pairs.append({"question": question, "answer": "（回答生成失败）"})

            if len(qa_pairs) < 6:
                return None

            return {
                "relevance_score": score_result["relevance_score"],
                "tags": score_result["tags"],
                "qa_pairs": qa_pairs,
            }

    # ── 一次性模式：PDF 全文 / 仅摘要 ──
    return _score_and_summarize_oneshot(paper, config, full_content, content_source)


def _score_and_summarize_oneshot(
    paper: dict,
    config: dict,
    full_content: Optional[str] = None,
    content_source: Optional[str] = None,
) -> Optional[dict]:
    """一次性评分 + Q&A（回退模式）。"""
    llm_config = config.get("llm", {})
    network_config = config.get("network", {})
    min_score = llm_config.get("min_relevance_score", 4)

    system_prompt = _load_prompt("system.txt")
    user_prompt = _load_prompt("score_and_summarize.txt").format_map({
        "title": paper["title"],
        "authors": _build_authors_str(paper),
        "categories": ", ".join(paper["categories"]),
        "summary": paper["summary"],
    })

    if full_content:
        source_label = "PDF 提取文本" if content_source == "pdf" else "论文内容"
        content_block = _load_prompt("full_content_block.txt").format_map({
            "source_label": source_label,
            "full_content": full_content,
        })
        user_prompt += "\n\n" + content_block

    temperature = llm_config.get("temperature", 0.3)
    if full_content:
        llm_max_tokens = llm_config.get("max_tokens_with_content", 5000)
    else:
        llm_max_tokens = llm_config.get("max_tokens_abstract_only", 3000)
    timeout = network_config.get("request_timeout", 90)

    try:
        response = call_llm(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=llm_max_tokens,
            timeout=timeout,
        )

        result = _parse_llm_json(response)

        required = ["relevance_score", "tags", "qa_pairs"]
        for field in required:
            if field not in result:
                logger.warning("LLM 返回缺少字段 %s", field)
                return None

        qa_pairs = result["qa_pairs"]
        if not isinstance(qa_pairs, list) or len(qa_pairs) < 6:
            logger.warning("qa_pairs 格式不正确: 需要至少 6 个问答对，实际 %s",
                           len(qa_pairs) if isinstance(qa_pairs, list) else type(qa_pairs))
            return None
        for i, pair in enumerate(qa_pairs):
            if not isinstance(pair, dict) or "question" not in pair or "answer" not in pair:
                logger.warning("qa_pairs[%d] 缺少 question 或 answer 字段", i)
                return None

        if result["relevance_score"] < min_score:
            return None

        return result

    except json.JSONDecodeError as e:
        logger.warning("LLM 返回非法 JSON: %s", e)
        return None
    except Exception as e:
        logger.warning("论文评分失败: %s", e)
        return None
