"""
Markdown 文件生成器
- 生成单篇论文的 markdown 文件 (YAML frontmatter)
- 更新 README.md
- 生成 papers.json 供前端使用（支持逐篇追加）
"""

import logging
import os
import re
import json
import shutil

logger = logging.getLogger(__name__)


def slugify(title: str, max_length: int = 80) -> str:
    """将标题转为文件名友好的 slug"""
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s]+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug[:max_length].rstrip("-")


def generate_paper_markdown(paper: dict, llm_result: dict, config: dict) -> str:
    """生成单篇论文的 markdown 内容"""
    output_config = config.get("output", {})
    max_authors = output_config.get("max_authors_frontmatter", 20)

    authors_list = []
    for a in paper["authors"][:max_authors]:
        author_str = a["name"]
        if a.get("affiliation"):
            author_str += f" ({a['affiliation']})"
        author_str = author_str.replace('"', '\\"')
        authors_list.append(f'  - "{author_str}"')

    tags_list = [f'  - "{t}"' for t in llm_result.get("tags", [])]
    cats_list = [f'  - "{c}"' for c in paper.get("categories", [])]

    escaped_title = paper['title'].replace('"', '\\"')

    github_line = ""
    if paper.get("github_url"):
        github_line = f'\ngithub_url: "{paper["github_url"]}"'

    md = f"""---
title: "{escaped_title}"
authors:
{chr(10).join(authors_list)}
date: "{paper['published'][:10]}"
arxiv_id: "{paper['arxiv_id']}"
arxiv_url: "{paper['arxiv_url']}"
pdf_url: "{paper['pdf_url']}"{github_line}
categories:
{chr(10).join(cats_list)}
tags:
{chr(10).join(tags_list)}
relevance_score: {llm_result.get('relevance_score', 0)}
---

# {paper['title']}

## 原始摘要

{paper['summary']}
"""

    qa_pairs = llm_result.get("qa_pairs")
    if qa_pairs:
        md += "\n## Q&A 论文解读\n"
        for i, pair in enumerate(qa_pairs):
            md += f"\n### Q{i+1}: {pair['question']}\n\n{pair['answer']}\n"
    else:
        contributions = llm_result.get("core_contributions", [])
        contributions_md = "\n".join(f"- {c}" for c in contributions)
        md += f"""
## 中文摘要

{llm_result.get('chinese_summary', 'N/A')}

## 核心贡献

{contributions_md}

## 文章解读

{llm_result.get('analysis', 'N/A')}
"""

    return md


def write_paper_file(paper: dict, llm_result: dict, base_dir: str, date_str: str, config: dict) -> str:
    """写入单篇论文的 markdown 文件，返回文件路径。"""
    output_config = config.get("output", {})
    slug_max = output_config.get("slug_max_length", 80)

    year, month, day = date_str.split("-")
    dir_path = os.path.join(base_dir, "data", year, month, day)
    os.makedirs(dir_path, exist_ok=True)

    slug = slugify(paper["title"], max_length=slug_max)
    filepath = os.path.join(dir_path, f"{slug}.md")

    content = generate_paper_markdown(paper, llm_result, config)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def _build_paper_json(paper: dict, result: dict, date_str: str, config: dict) -> dict:
    """构建单篇论文的 JSON 数据。"""
    output_config = config.get("output", {})
    max_authors = output_config.get("max_authors_json", 5)
    slug_max = output_config.get("slug_max_length", 80)

    year, month, day = date_str.split("-")
    slug = slugify(paper["title"], max_length=slug_max)

    paper_data = {
        "arxiv_id": paper["arxiv_id"],
        "version": paper.get("version", 1),
        "title": paper["title"],
        "authors": [a["name"] for a in paper["authors"][:max_authors]],
        "author_count": len(paper["authors"]),
        "categories": paper["categories"],
        "arxiv_url": paper["arxiv_url"],
        "pdf_url": paper["pdf_url"],
        "github_url": paper.get("github_url", ""),
        "published": paper["published"][:10],
        "tags": result.get("tags", []),
        "relevance_score": result.get("relevance_score", 0),
        "md_path": f"data/{year}/{month}/{day}/{slug}.md",
    }
    return paper_data


def append_paper_json(paper: dict, result: dict, base_dir: str, date_str: str, config: dict):
    """
    追加一篇论文到当日 papers.json（逐篇落盘）。
    同时更新 index.json 和 web/public 同步。
    """
    year, month, day = date_str.split("-")
    day_dir = os.path.join(base_dir, "data", year, month, day)
    os.makedirs(day_dir, exist_ok=True)
    day_json_path = os.path.join(day_dir, "papers.json")

    # 读取已有数据
    if os.path.exists(day_json_path):
        with open(day_json_path, "r", encoding="utf-8") as f:
            day_papers = json.load(f)
    else:
        day_papers = []

    # 追加新论文（去重）
    paper_data = _build_paper_json(paper, result, date_str, config)
    existing_ids = {p["arxiv_id"] for p in day_papers}
    if paper_data["arxiv_id"] not in existing_ids:
        day_papers.append(paper_data)

    # 按评分排序后写入
    day_papers.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
    with open(day_json_path, "w", encoding="utf-8") as f:
        json.dump(day_papers, f, ensure_ascii=False, indent=2)

    # 更新日期索引
    index_path = os.path.join(base_dir, "data", "index.json")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index_data = json.load(f)
    else:
        index_data = {"available_dates": []}

    if date_str not in index_data["available_dates"]:
        index_data["available_dates"].append(date_str)
    index_data["available_dates"] = sorted(index_data["available_dates"], reverse=True)

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    # 同步到 web/public/data/
    _sync_to_web(base_dir, day_json_path, index_path, year, month, day)


def _sync_to_web(base_dir: str, day_json_path: str, index_path: str, year: str, month: str, day: str):
    """同步数据到 web/public/data/（本地开发用）。"""
    web_data_dir = os.path.join(base_dir, "web", "public", "data")
    if os.path.isdir(os.path.join(base_dir, "web", "public")):
        web_day_dir = os.path.join(web_data_dir, year, month, day)
        os.makedirs(web_day_dir, exist_ok=True)
        shutil.copy2(day_json_path, os.path.join(web_day_dir, "papers.json"))
        shutil.copy2(index_path, os.path.join(web_data_dir, "index.json"))
        # 同步 .md 文件（前端需要 fetch .md 获取论文详情）
        src_day_dir = os.path.join(base_dir, "data", year, month, day)
        for fname in os.listdir(src_day_dir):
            if fname.endswith(".md"):
                shutil.copy2(
                    os.path.join(src_day_dir, fname),
                    os.path.join(web_day_dir, fname),
                )


def update_readme(base_dir: str, date_str: str, config: dict):
    """
    更新 README.md — 从当日 papers.json 读取数据，生成简表。
    每篇论文落盘后调用，始终反映最新状态。
    """
    year, month, day = date_str.split("-")
    day_json_path = os.path.join(base_dir, "data", year, month, day, "papers.json")

    if not os.path.exists(day_json_path):
        return

    with open(day_json_path, "r", encoding="utf-8") as f:
        day_papers = json.load(f)

    readme_path = os.path.join(base_dir, "README.md")
    output_config = config.get("output", {})
    core_threshold = output_config.get("core_recommendation_score", 8.0)
    related_threshold = output_config.get("related_recommendation_score", 6.5)

    core_papers = [
        p for p in day_papers
        if p.get("relevance_score", 0) >= core_threshold
    ]
    related_papers = [
        p for p in day_papers
        if related_threshold <= p.get("relevance_score", 0) < core_threshold
    ]

    lines = [
        "# Daily Agentic Time Series Papers",
        "",
        "每日 arXiv 时序智能体论文自动摘要 | Daily Agentic Time Series Paper Summaries",
        "",
        f"## {date_str} ({len(day_papers)} 篇)",
        "",
    ]

    def append_table(title: str, papers: list[dict]):
        lines.extend([
            f"### {title} ({len(papers)} 篇)",
            "",
        ])
        if not papers:
            lines.extend(["暂无。", ""])
            return

        lines.extend([
            "| 分数 | 论文 | 标签 |",
            "|:----:|------|------|",
        ])
        for p in papers:
            score = p.get("relevance_score", 0)
            paper_title = p.get("title", "")
            url = p.get("arxiv_url", "")
            github_url = p.get("github_url", "")
            tags = p.get("tags", [])
            tags_str = ", ".join(tags[:3])
            title_cell = f"[{paper_title}]({url})"
            if github_url:
                title_cell += f" [[Code]({github_url})]"
            lines.append(f"| {score} | {title_cell} | {tags_str} |")
        lines.append("")

    append_table("核心推荐", core_papers)
    append_table("可借鉴论文", related_papers)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
