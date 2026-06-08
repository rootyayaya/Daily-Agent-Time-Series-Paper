#!/usr/bin/env python3
"""
对指定日期的论文重新打分 + 打标（taxonomy），保留原有 QA 不动。

每篇论文 2 次 LLM query：
  1. 重新打分 + 旧式 tags（score_only prompt）
  2. 新标签体系分类（taxonomy prompt）

需要临时下载论文全文（LaTeX/PDF）以获取更详细信息。

用法:
    python scripts/reprocess_day.py --date 2026-03-04
    python scripts/reprocess_day.py --date 2026-03-04 --limit 3
    python scripts/reprocess_day.py --date 2026-03-04 --paper-id 2603.04257
    python scripts/reprocess_day.py --date 2026-03-04 --dry-run
"""

import argparse
import json
import logging
import os
import re
import shutil
import sys
import time

import yaml
from dotenv import load_dotenv

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)

from llm_client import call_llm, _load_prompt, _parse_llm_json, _score_paper
from paper_content import fetch_paper_content

logger = logging.getLogger("reprocess")

# ── 分类体系 ──

TAXONOMY = {
    "capability": [
        "Reasoning & Planning",
        "Tool Use & API Interaction",
        "Multi-Agent Systems",
        "Memory & Context Management",
        "Learning & Optimization",
        "Human-Agent Interaction",
        "Safety & Alignment",
        "Architecture & Frameworks",
        "World Modeling & Simulation",
        "Perception & Multimodal",
        "Web & Browser Automation",
        "Code & Software Engineering",
    ],
    "domain": [
        "General Purpose",
        "Scientific Research",
        "Enterprise & Workflow",
        "Cybersecurity",
        "Robotics & Embodied",
        "Data Science & Analytics",
        "Games & Entertainment",
        "Social & Behavioral Science",
        "Legal & Financial",
        "Healthcare & Bio",
        "Finance & Trading",
    ],
    "research_type": [
        "New Method/Model",
        "New Algorithm",
        "Benchmark/Evaluation",
        "Empirical Study/Analysis",
        "System/Tooling/Library",
        "Survey/Position Paper",
    ],
}

TAXONOMY_SYSTEM_PROMPT = """你是一位 AI Agent 研究领域的论文分类专家。
你的任务是根据论文的标题、摘要和内容，从预定义的分类体系中选择标签，并提取结构化元数据。

重要约束：
- 三个维度（capability / domain / research_type）的标签列表互不相通，你只能从各维度给定的选项中选择。
- 不要自创标签，不要将一个维度的标签填到另一个维度。
- 只输出 JSON，不要用 markdown code block 包裹，不要添加任何解释。"""

TAXONOMY_USER_TEMPLATE = """请对以下论文进行分类和元数据提取。

## 分类体系

三个维度的标签列表互不相通。每个维度只能从该维度的选项中选择，禁止跨维度使用。

### 核心能力（capability）— 从以下 12 个选项中选 1-2 个
{capability_list}

### 应用领域（domain）— 从以下 11 个选项中选 1 个
{domain_list}

### 研究类型（research_type）— 从以下 6 个选项中选 1 个
{research_type_list}

## 分类指引

- capability 描述的是论文在智能体技术层面的核心关注点（如推理、工具调用、多智能体协调等）。
- domain 描述的是论文的应用场景或目标领域（如通用、科研、医疗等）。如果论文不针对特定领域，选 "General Purpose"。
- research_type 描述的是论文的贡献形式（如提出新方法、构建评测基准、实证分析等）。
- "Benchmark/Evaluation" 只存在于 research_type，不要将其作为 capability。如果论文的主要贡献是评测框架/数据集，research_type 选 "Benchmark/Evaluation"，capability 选论文实际评测的技术方向。
- "Code & Software Engineering" 只存在于 capability，不要将其作为 domain。如果论文研究代码生成/调试类智能体，capability 选 "Code & Software Engineering"，domain 根据应用场景选择（通常是 "General Purpose"）。

## 输出格式

只输出如下 JSON（不要用 markdown code block 包裹）：
{{
  "capability": ["选项1", "选项2"],
  "domain": "选项",
  "research_type": "选项",
  "base_model": "论文使用/测试的主要基座模型，如 GPT-4o、Llama-3-70B、Qwen-2.5 等，多个用逗号分隔，未提及则填 N/A",
  "key_technique": "论文提出的核心方法或算法的名称，如 ReAct、GRPO、DPO 等，未明确命名则简要概括",
  "primary_benchmark": "论文使用的主要评测基准，如 SWE-bench、WebArena 等，自建基准填其名称，无则填 N/A"
}}

## 论文信息

标题: {title}
摘要: {summary}

{content_block}"""


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("arxiv").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def load_config() -> dict:
    with open(os.path.join(BASE_DIR, "config.yaml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_papers(date_str: str) -> list[dict]:
    year, month, day = date_str.split("-")
    path = os.path.join(BASE_DIR, "data", year, month, day, "papers.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_summary_from_md(md_path: str) -> str:
    """从 .md 文件读取原始摘要。"""
    full_path = os.path.join(BASE_DIR, md_path)
    if not os.path.exists(full_path):
        return ""
    with open(full_path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"## 原始摘要\s*\r?\n\r?\n([\s\S]*?)(?=\r?\n## |$)", text)
    return m.group(1).strip() if m else ""


def read_qa_from_md(md_path: str) -> str:
    """从 .md 文件读取 Q&A 部分（原样保留）。"""
    full_path = os.path.join(BASE_DIR, md_path)
    if not os.path.exists(full_path):
        return ""
    with open(full_path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"(## Q&A 论文解读\s*\r?\n[\s\S]*)", text)
    return m.group(1).strip() if m else ""


def extract_taxonomy(title: str, summary: str, content: str, config: dict) -> dict | None:
    """1 次 LLM 调用：提取 taxonomy + 元数据。"""
    network_config = config.get("network", {})

    cap_list = "\n".join(f"- {c}" for c in TAXONOMY["capability"])
    dom_list = "\n".join(f"- {d}" for d in TAXONOMY["domain"])
    rt_list = "\n".join(f"- {r}" for r in TAXONOMY["research_type"])

    content_block = ""
    if content:
        content_block = f"论文内容（前 8000 字符）:\n{content[:8000]}"

    user_prompt = TAXONOMY_USER_TEMPLATE.format(
        capability_list=cap_list,
        domain_list=dom_list,
        research_type_list=rt_list,
        title=title,
        summary=summary,
        content_block=content_block,
    )

    try:
        response = call_llm(
            messages=[
                {"role": "system", "content": TAXONOMY_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=500,
            timeout=network_config.get("request_timeout", 90),
        )
        return _parse_llm_json(response)
    except Exception as e:
        logger.warning("  taxonomy 失败: %s", e)
        return None


def update_md_file(md_path: str, paper: dict, new_score: float, new_tags: list[str],
                   taxonomy: dict, attributes: dict, summary: str, qa_block: str,
                   config: dict):
    """用新的 frontmatter 重写 .md 文件，保留原有摘要和 QA。"""
    output_config = config.get("output", {})
    max_authors = output_config.get("max_authors_frontmatter", 20)

    authors = paper.get("authors", [])
    authors_list = []
    for a in authors[:max_authors]:
        name = a if isinstance(a, str) else a.get("name", "")
        name = name.replace('"', '\\"')
        authors_list.append(f'  - "{name}"')

    tags_list = [f'  - "{t}"' for t in new_tags]
    cats_list = [f'  - "{c}"' for c in paper.get("categories", [])]
    escaped_title = paper["title"].replace('"', '\\"')

    github_line = ""
    if paper.get("github_url"):
        github_line = f'\ngithub_url: "{paper["github_url"]}"'

    cap_lines = "\n".join(f'    - "{c}"' for c in taxonomy.get("capability", []))

    md = f'''---
title: "{escaped_title}"
authors:
{chr(10).join(authors_list)}
date: "{paper["published"][:10]}"
arxiv_id: "{paper["arxiv_id"]}"
arxiv_url: "{paper["arxiv_url"]}"
pdf_url: "{paper["pdf_url"]}"{github_line}
categories:
{chr(10).join(cats_list)}
tags:
{chr(10).join(tags_list)}
relevance_score: {new_score}
taxonomy:
  capability:
{cap_lines}
  domain: "{taxonomy.get("domain", "General Purpose")}"
  research_type: "{taxonomy.get("research_type", "New Method/Model")}"
attributes:
  base_model: "{attributes.get("base_model", "N/A")}"
  key_technique: "{attributes.get("key_technique", "N/A")}"
  primary_benchmark: "{attributes.get("primary_benchmark", "N/A")}"
---

# {paper["title"]}

## 原始摘要

{summary}

{qa_block}
'''

    full_path = os.path.join(BASE_DIR, md_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(md)


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Reprocess: re-score + taxonomy tagging")
    parser.add_argument("--date", type=str, required=True)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--paper-id", type=str, default="")
    parser.add_argument("--min-score", type=float, default=7.5)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(os.path.join(BASE_DIR, ".env"))
    config = load_config()

    all_papers = load_papers(args.date)
    papers = [p for p in all_papers if p.get("relevance_score", 0) >= args.min_score]

    if args.paper_id:
        papers = [p for p in papers if p["arxiv_id"] == args.paper_id]
    if args.limit > 0:
        papers = papers[:args.limit]

    logger.info("=== 重新处理 %s ===", args.date)
    logger.info("总: %d, >=%.1f: %d, 本次: %d", len(all_papers), args.min_score,
                sum(1 for p in all_papers if p.get("relevance_score", 0) >= args.min_score), len(papers))

    if args.dry_run:
        for p in papers:
            logger.info("  [%s] %.1f  %s", p["arxiv_id"], p["relevance_score"], p["title"][:60])
        logger.info("Dry run: %d papers * 2 queries = %d LLM calls", len(papers), len(papers) * 2)
        return

    year, month, day = args.date.split("-")
    day_dir = os.path.join(BASE_DIR, "data", year, month, day)

    # 进度文件（断点续跑）
    progress_path = os.path.join(day_dir, ".reprocess_progress.json")
    if os.path.exists(progress_path):
        with open(progress_path, encoding="utf-8") as f:
            progress = json.load(f)
    else:
        progress = {}

    updated_papers = []
    completed = 0
    failed = 0

    for i, paper in enumerate(papers):
        aid = paper["arxiv_id"]

        # 断点续跑：跳过已处理
        if aid in progress:
            logger.info("[%d/%d] 跳过已处理: %s", i + 1, len(papers), aid)
            updated_papers.append(progress[aid])
            continue

        logger.info("[%d/%d] %s — %s", i + 1, len(papers), aid, paper["title"][:50])

        # 读取原有摘要和 QA
        md_path = paper.get("md_path", "")
        summary = read_summary_from_md(md_path)
        qa_block = read_qa_from_md(md_path)

        if not summary:
            logger.warning("  无法读取摘要，跳过")
            failed += 1
            continue

        # 构建 paper dict（兼容 _score_paper 需要的格式）
        paper_for_llm = {
            "title": paper["title"],
            "authors": [{"name": a, "affiliation": ""} if isinstance(a, str) else a
                        for a in paper.get("authors", [])],
            "categories": paper.get("categories", []),
            "summary": summary,
        }

        # Step 1: 获取论文全文
        content, source_type = fetch_paper_content(aid, config)
        logger.info("  内容: %s (%d chars)", source_type, len(content) if content else 0)

        # Step 2: 重新评分 (query 1)
        score_result = _score_paper(paper_for_llm, config)
        if not score_result:
            logger.warning("  评分失败，保留原分 %.1f", paper["relevance_score"])
            new_score = paper["relevance_score"]
            score_tags = paper.get("tags", [])
        else:
            new_score = score_result["relevance_score"]
            score_tags = score_result.get("tags", [])
            logger.info("  评分: %.1f → %.1f", paper["relevance_score"], new_score)

        # Step 3: taxonomy 打标 (query 2)
        tax_result = extract_taxonomy(paper["title"], summary, content or "", config)
        if not tax_result:
            logger.warning("  taxonomy 失败，使用空值")
            tax_result = {
                "capability": [], "domain": "General Purpose",
                "research_type": "New Method/Model",
                "base_model": "N/A", "key_technique": "N/A", "primary_benchmark": "N/A",
            }
        else:
            logger.info("  cap=%s, dom=%s, type=%s",
                        tax_result.get("capability"), tax_result.get("domain"),
                        tax_result.get("research_type"))

        taxonomy = {
            "capability": tax_result.get("capability", []),
            "domain": tax_result.get("domain", "General Purpose"),
            "research_type": tax_result.get("research_type", "New Method/Model"),
        }
        attributes = {
            "base_model": tax_result.get("base_model", "N/A"),
            "key_technique": tax_result.get("key_technique", "N/A"),
            "primary_benchmark": tax_result.get("primary_benchmark", "N/A"),
        }

        # tags 使用 capability 作为新标签
        new_tags = taxonomy["capability"]

        # 更新 .md 文件
        update_md_file(md_path, paper, new_score, new_tags, taxonomy, attributes,
                       summary, qa_block, config)

        # 构建新的 papers.json 条目
        output_config = config.get("output", {})
        max_authors_json = output_config.get("max_authors_json", 5)
        slug_max = output_config.get("slug_max_length", 80)
        from markdown_writer import slugify
        slug = slugify(paper["title"], max_length=slug_max)

        paper_json = {
            "arxiv_id": aid,
            "version": paper.get("version", 1),
            "title": paper["title"],
            "authors": [(a if isinstance(a, str) else a["name"]) for a in paper.get("authors", [])][:max_authors_json],
            "author_count": paper.get("author_count", len(paper.get("authors", []))),
            "categories": paper.get("categories", []),
            "arxiv_url": paper["arxiv_url"],
            "pdf_url": paper["pdf_url"],
            "github_url": paper.get("github_url", ""),
            "published": paper["published"][:10],
            "tags": new_tags,
            "relevance_score": new_score,
            "taxonomy": taxonomy,
            "attributes": attributes,
            "md_path": f"data/{year}/{month}/{day}/{slug}.md",
        }
        updated_papers.append(paper_json)

        # 保存进度
        progress[aid] = paper_json
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)

        completed += 1
        logger.info("  完成 (%d/%d)", completed, len(papers))

    # 写入 papers.json（合并模式：更新已处理的，保留未处理的）
    if updated_papers:
        day_json_path = os.path.join(day_dir, "papers.json")

        # 读取现有 papers.json，用处理结果覆盖对应条目
        if os.path.exists(day_json_path):
            with open(day_json_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        else:
            existing = []

        updated_ids = {p["arxiv_id"] for p in updated_papers}
        # 保留未被本次处理覆盖的条目
        merged = [p for p in existing if p["arxiv_id"] not in updated_ids]
        merged.extend(updated_papers)
        merged.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        with open(day_json_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        logger.info("papers.json 已更新: %d 篇 (本次处理 %d)", len(merged), len(updated_papers))

        # 同步到 web
        index_path = os.path.join(BASE_DIR, "data", "index.json")
        if os.path.exists(index_path) and os.path.isdir(os.path.join(BASE_DIR, "web", "public")):
            from markdown_writer import _sync_to_web
            _sync_to_web(BASE_DIR, day_json_path, index_path, year, month, day)
            logger.info("已同步到 web/public/data/")

    # 清理进度文件
    if failed == 0 and os.path.exists(progress_path):
        os.remove(progress_path)

    logger.info("")
    logger.info("=== 完成 ===")
    logger.info("成功: %d, 失败: %d, 新论文数: %d (旧: %d)", completed, failed, len(updated_papers), len(all_papers))


if __name__ == "__main__":
    main()
