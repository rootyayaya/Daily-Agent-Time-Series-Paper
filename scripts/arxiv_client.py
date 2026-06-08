"""
arxiv API 查询客户端（基于 arxiv 库）
- 宽泛搜索 agent 相关论文
- 关键词精筛
"""

import logging
import re

import arxiv

logger = logging.getLogger(__name__)


def extract_github_url(*texts: str) -> str:
    """
    从多个文本（comment, summary 等）中提取第一个 GitHub 仓库链接。
    返回仓库级 URL（去掉尾部的 tree/blob/wiki 等路径），无则返回空字符串。
    """
    for text in texts:
        if not text:
            continue
        # 匹配 github.com/owner/repo，可能带后续路径
        matches = re.findall(r'https?://github\.com/[\w.-]+/[\w.-]+', text)
        for url in matches:
            # 规范化：去掉尾部标点（句号、逗号等）、.git 后缀、尾部斜杠
            url = url.rstrip('/').rstrip('.,;:!?')
            url = re.sub(r'\.git$', '', url)
            return url
    return ""


def build_query(
    keywords: list[str],
    categories: list[str],
    date_str: str | None = None,
    date_end: str | None = None,
) -> str:
    """
    构建 arxiv API 搜索查询字符串。
    date_str: 起始日期 YYYY-MM-DD（含），若提供则通过 submittedDate 在服务端过滤。
    date_end: 结束日期 YYYY-MM-DD（含），未提供则与 date_str 相同（单日查询）。
    """
    kw_parts = [f'all:"{kw}"' for kw in keywords]
    kw_query = " OR ".join(kw_parts)

    cat_parts = [f"cat:{cat}" for cat in categories]
    cat_query = " OR ".join(cat_parts)

    query = f"({kw_query}) AND ({cat_query})"

    if date_str:
        start = date_str.replace("-", "")
        end = (date_end or date_str).replace("-", "")
        query += f" AND submittedDate:[{start} TO {end}]"

    return query


def fetch_arxiv_papers(
    query: str,
    config: dict,
    max_results: int = 200,
) -> list[dict]:
    """使用 arxiv 库查询论文，自动处理限流和重试。"""
    network_config = config.get("network", {})
    delay = network_config.get("arxiv_request_delay", 5.0)
    retries = network_config.get("arxiv_retries", 4)

    client = arxiv.Client(
        page_size=100,
        delay_seconds=delay,
        num_retries=retries,
    )

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    papers = []
    for result in client.results(search):
        raw_id = result.entry_id.split("/abs/")[-1]
        version_match = re.search(r"v(\d+)$", raw_id)
        version = int(version_match.group(1)) if version_match else 1
        arxiv_id = re.sub(r"v\d+$", "", raw_id)

        authors = []
        for a in result.authors:
            authors.append({"name": a.name, "affiliation": ""})

        pdf_url = result.pdf_url or f"https://arxiv.org/pdf/{arxiv_id}"
        comment = (result.comment or "").strip()
        summary = result.summary.strip()
        github_url = extract_github_url(comment, summary)

        papers.append({
            "arxiv_id": arxiv_id,
            "version": version,
            "title": re.sub(r"\s+", " ", result.title.replace("\n", " ")).strip(),
            "authors": authors,
            "summary": summary,
            "categories": result.categories,
            "primary_category": result.primary_category,
            "published": result.published.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated": result.updated.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "arxiv_url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": pdf_url,
            "github_url": github_url,
            "comment": comment,
        })

    return papers


def fetch_updated_papers(
    query: str,
    config: dict,
    target_date: str,
    max_results: int = 500,
) -> list[dict]:
    """
    查询 arxiv 按 LastUpdatedDate 排序，客户端过滤出在 target_date 更新且版本 >= 2 的论文。
    用于捕获在 target_date 修订的旧论文（submittedDate 查询无法覆盖的情况）。
    """
    network_config = config.get("network", {})
    delay = network_config.get("arxiv_request_delay", 5.0)
    retries = network_config.get("arxiv_retries", 4)

    client = arxiv.Client(
        page_size=100,
        delay_seconds=delay,
        num_retries=retries,
    )

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.LastUpdatedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    papers = []
    for result in client.results(search):
        updated_date = result.updated.strftime("%Y-%m-%d")

        # 结果按 LastUpdatedDate 降序，早于目标日期即可停止
        if updated_date < target_date:
            break

        # 只要目标日期更新的论文
        if updated_date != target_date:
            continue

        raw_id = result.entry_id.split("/abs/")[-1]
        version_match = re.search(r"v(\d+)$", raw_id)
        version = int(version_match.group(1)) if version_match else 1
        arxiv_id = re.sub(r"v\d+$", "", raw_id)

        # 只保留 v2+ 的修订论文
        if version < 2:
            continue

        # 过滤掉发布日期过早的论文（早于 LLM 时代）
        min_published = config.get("updates", {}).get("min_published_date", "2023-01-01")
        if result.published.strftime("%Y-%m-%d") < min_published:
            continue

        authors = []
        for a in result.authors:
            authors.append({"name": a.name, "affiliation": ""})

        pdf_url = result.pdf_url or f"https://arxiv.org/pdf/{arxiv_id}"
        comment = (result.comment or "").strip()
        summary = result.summary.strip()
        github_url = extract_github_url(comment, summary)

        papers.append({
            "arxiv_id": arxiv_id,
            "version": version,
            "title": re.sub(r"\s+", " ", result.title.replace("\n", " ")).strip(),
            "authors": authors,
            "summary": summary,
            "categories": result.categories,
            "primary_category": result.primary_category,
            "published": result.published.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated": result.updated.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "arxiv_url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": pdf_url,
            "github_url": github_url,
            "comment": comment,
        })

    return papers


def filter_by_date(papers: list[dict], target_date: str) -> list[dict]:
    """
    按日期过滤论文。target_date 格式: YYYY-MM-DD
    arxiv published 的时间是 UTC，我们取 published 日期匹配的论文。
    """
    return [p for p in papers if p["published"][:10] == target_date]


def keyword_filter(papers: list[dict], must_have: list[str], boost_keywords: list[str]) -> list[dict]:
    """
    关键词精筛：
    - must_have 中至少命中一个关键词才保留
    - boost_keywords 用于后续评分加权
    """
    filtered = []
    for p in papers:
        text = (p["title"] + " " + p["summary"]).lower()
        hit = any(kw.lower() in text for kw in must_have)
        if hit:
            boost_count = sum(1 for kw in boost_keywords if kw.lower() in text)
            p["keyword_boost"] = boost_count
            filtered.append(p)
    return filtered
