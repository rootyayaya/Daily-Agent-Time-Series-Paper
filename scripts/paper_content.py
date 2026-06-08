"""
论文全文获取模块 - 通过 arxiv-to-prompt 获取 LaTeX 源码，PDF 作为 fallback。
支持按 section 提取内容，实现精准送达 LLM。
"""

import logging
import os
import re
import tempfile
import urllib.request

logger = logging.getLogger(__name__)


def _fetch_latex(arxiv_id: str, config: dict) -> str | None:
    """尝试通过 arxiv-to-prompt 获取 LaTeX 源码。"""
    try:
        from arxiv_to_prompt import process_latex_source

        latex_config = config.get("paper_content", {}).get("latex", {})
        result = process_latex_source(
            arxiv_id,
            keep_comments=latex_config.get("keep_comments", False),
            remove_appendix_section=latex_config.get("remove_appendix_section", True),
            use_cache=latex_config.get("use_cache", True),
        )
        if result:
            return result
    except ImportError:
        logger.warning("arxiv-to-prompt 未安装，跳过 LaTeX 获取")
    except Exception as e:
        logger.warning("LaTeX 获取失败 (%s): %s", arxiv_id, e)
    return None


def _fetch_pdf_text(arxiv_id: str, config: dict) -> str | None:
    """下载 PDF 并提取文本（fallback 方案）。"""
    try:
        import fitz  # pymupdf
    except ImportError:
        logger.warning("pymupdf 未安装，跳过 PDF 获取")
        return None

    network_config = config.get("network", {})
    user_agent = network_config.get("user_agent", "Daily-Agent-Time-Series-Paper/1.0")
    timeout = network_config.get("request_timeout", 60)

    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
    tmp_path = None
    try:
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
        os.close(tmp_fd)

        req = urllib.request.Request(pdf_url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            with open(tmp_path, "wb") as f:
                f.write(resp.read())

        doc = fitz.open(tmp_path)
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()

        text = "\n".join(text_parts)
        if text.strip():
            return text
        return None

    except Exception as e:
        logger.warning("PDF 获取失败 (%s): %s", arxiv_id, e)
        return None
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


def get_section_list(latex_content: str, include_subsections: bool = False) -> list[str]:
    """
    从 LaTeX 内容中提取目录。
    include_subsections=True 时包含 subsection 和 subsubsection（带缩进前缀标识层级）。
    """
    try:
        from arxiv_to_prompt import list_sections
        sections = list_sections(latex_content)
        if not include_subsections:
            return sections

        # 构建包含 subsection 的完整目录
        all_items = []
        # 提取所有级别，按在文档中出现的顺序排列
        pattern = re.compile(
            r'\\(section|subsection|subsubsection)\*?\{([^}]+)\}'
        )
        seen = set()
        for match in pattern.finditer(latex_content):
            level, name = match.group(1), match.group(2)
            # 去重（同名 section 可能在 appendix 中重复出现）
            key = (level, name)
            if key in seen:
                continue
            seen.add(key)

            if level == "section":
                all_items.append(name)
            elif level == "subsection":
                all_items.append(f"  {name}")
            else:  # subsubsection
                all_items.append(f"    {name}")
        return all_items if all_items else sections
    except Exception as e:
        logger.warning("提取目录失败: %s", e)
        return []


def _strip_latex(text: str) -> str:
    """移除常见 LaTeX 命令，保留可读文本用于预览。"""
    # 移除 section/subsection 标题命令（整行删除，heading 已在外部生成）
    text = re.sub(r'\\(?:sub)*section\*?\{[^}]*\}', '', text)
    text = re.sub(r'\\label\{[^}]*\}', '', text)
    text = re.sub(r'~?\\cite\w*\{[^}]*\}', '', text)
    text = re.sub(r'\\(?:eq)?ref\{[^}]*\}', '', text)
    text = re.sub(r'\\(?:emph|textbf|textit|text|mathrm|texttt)\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\(?:noindent|thinspace|hspace\{[^}]*\}|vspace\{[^}]*\})', ' ', text)
    text = re.sub(r'\\(?:begin|end)\{[^}]*\}', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_section_previews(latex_content: str, sections: list[str], preview_chars: int = 256) -> str:
    """
    为每个 section/subsection 生成 markdown 格式的目录预览，辅助 AI 判断与问题的相关性。
    格式: # Section Name\ncontent... / ## Subsection Name\ncontent...
    preview_chars: 每个条目截断的字符数（0 表示仅标题）。
    """
    try:
        from arxiv_to_prompt import extract_section
    except ImportError:
        return "\n".join(f"- {s}" for s in sections)

    lines = []
    for s in sections:
        name = s.lstrip()
        indent_level = len(s) - len(name)  # 0=section, 2=subsection, 4=subsubsection

        hashes = "#" * (min(indent_level // 2, 2) + 1)
        heading = f"{hashes} {name}"

        if preview_chars <= 0:
            lines.append(heading)
            continue

        content = extract_section(latex_content, name)
        if content:
            cleaned = _strip_latex(content)
            preview = cleaned[:preview_chars]
            if len(cleaned) > preview_chars:
                preview += "..."
            lines.append(f"{heading}\n{preview}")
        else:
            lines.append(heading)
    return "\n\n".join(lines)


def _fuzzy_match_section(name: str, all_sections: list[str]) -> str | None:
    """
    当 LLM 返回的 section 名与目录不完全匹配时，尝试模糊匹配。
    策略: 精确匹配（忽略大小写）→ 子串包含。
    """
    name_lower = name.lower()
    for s in all_sections:
        if s.lstrip().lower() == name_lower:
            return s.lstrip()
    for s in all_sections:
        s_clean = s.lstrip().lower()
        if s_clean in name_lower or name_lower in s_clean:
            return s.lstrip()
    return None



def extract_sections(
    latex_content: str,
    section_names: list[str],
    max_chars_per_section: int = 15000,
    all_sections: list[str] | None = None,
) -> str:
    """
    从 LaTeX 内容中提取指定 section 的内容，以 markdown 格式拼接返回。
    输出格式: # Section Name\ncleaned content\n\n# Section Name\ncleaned content
    all_sections: 完整目录列表，用于模糊匹配回退。
    """
    try:
        from arxiv_to_prompt import extract_section
    except ImportError:
        return ""

    parts = []
    seen = set()
    for name in section_names:
        clean_name = name.lstrip()
        content = extract_section(latex_content, clean_name)
        # 模糊匹配回退
        if not content and all_sections:
            matched = _fuzzy_match_section(clean_name, all_sections)
            if matched and matched != clean_name:
                logger.info("章节名模糊匹配: %r -> %r", clean_name, matched)
                clean_name = matched
                content = extract_section(latex_content, clean_name)
        if content and clean_name not in seen:
            seen.add(clean_name)
            cleaned = _strip_latex(content)
            if len(cleaned) > max_chars_per_section:
                cleaned = cleaned[:max_chars_per_section] + "..."
            parts.append(f"# {clean_name}\n{cleaned}")

    return "\n\n".join(parts)


def fetch_paper_content(arxiv_id: str, config: dict) -> tuple[str, str]:
    """
    获取论文全文内容。

    返回: (content_text, source_type)
      - source_type: "latex" | "pdf" | "abstract_only"
      - 当全文不可用时，content_text 为空字符串，source_type 为 "abstract_only"
    """
    max_length = config.get("paper_content", {}).get("max_content_length", 50000)

    # 主路径：LaTeX 源码
    content = _fetch_latex(arxiv_id, config)
    if content:
        if len(content) > max_length:
            content = content[:max_length]
        return content, "latex"

    # Fallback：PDF 文本
    content = _fetch_pdf_text(arxiv_id, config)
    if content:
        if len(content) > max_length:
            content = content[:max_length]
        return content, "pdf"

    return "", "abstract_only"
