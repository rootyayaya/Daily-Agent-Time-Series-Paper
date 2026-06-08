#!/usr/bin/env python3
"""
主入口脚本：获取 arXiv Agentic Time Series 论文，LLM 评分/摘要，写入 markdown。

根据 arxiv 发布时间表自动计算需要抓取的日期：
  - arxiv 周日至周四（ET）发布论文，周五周六不发布
  - API 数据在论文发布次日可查
  - 因此本脚本 UTC 周一至周五 06:00 执行：
    周一: 抓取周四+周五（周日 ET 发布的）
    周二: 抓取周六+周日+周一（周一 ET 发布的，含周末积压）
    周三~周五: 抓取前一天

用法:
    python scripts/fetch_papers.py                    # 自动计算目标日期
    python scripts/fetch_papers.py --date 2026-02-22  # 指定单个日期
"""

import argparse
import glob
import json
import logging
import os
import sys
import threading
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from arxiv_client import build_query, fetch_arxiv_papers, fetch_updated_papers, keyword_filter
from llm_client import quick_relevance_check, score_and_summarize
from markdown_writer import write_paper_file, append_paper_json, update_readme
from paper_content import fetch_paper_content

logger = logging.getLogger("dailyagentpapers")


def setup_logging():
    """配置日志格式。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("arxiv").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def load_config(base_dir: str) -> dict:
    """加载 config.yaml"""
    config_path = os.path.join(base_dir, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_target_dates(today: datetime | None = None) -> list[str]:
    """
    根据当前 UTC 日期计算需要抓取的论文投稿日期列表。

    arxiv 发布时间表 (ET):
      周日 20:00 发布: 周四 14:00 – 周五 14:00 投稿的论文
      周一 20:00 发布: 周五 14:00 – 周一 14:00 投稿的论文（含周末积压）
      周二 20:00 发布: 周一 14:00 – 周二 14:00
      周三 20:00 发布: 周二 14:00 – 周三 14:00
      周四 20:00 发布: 周三 14:00 – 周四 14:00

    API 在发布次日可查，所以 UTC 执行日对应：
      周一 UTC → 查周四+周五（周日 ET 发布）
      周二 UTC → 查周六+周日+周一（周一 ET 发布）
      周三 UTC → 查周二
      周四 UTC → 查周三
      周五 UTC → 查周四
    """
    if today is None:
        today = datetime.now(timezone.utc)

    weekday = today.weekday()  # 0=Monday

    if weekday == 0:  # 周一 → 上周四 + 上周五
        dates = [today - timedelta(days=4), today - timedelta(days=3)]
    elif weekday == 1:  # 周二 → 上周六 + 上周日 + 周一
        dates = [today - timedelta(days=3), today - timedelta(days=2), today - timedelta(days=1)]
    else:  # 周三~周五 → 前一天
        dates = [today - timedelta(days=1)]

    return [d.strftime("%Y-%m-%d") for d in dates]


def load_history_index(base_dir: str) -> dict[str, int]:
    """
    扫描所有历史 papers.json，构建 {arxiv_id: max_version} 索引。
    用于去重：跳过已收录且版本相同的论文。
    """
    index = {}
    pattern = os.path.join(base_dir, "data", "*", "*", "*", "papers.json")
    for path in glob.glob(pattern):
        try:
            with open(path, "r", encoding="utf-8") as f:
                papers = json.load(f)
            for p in papers:
                aid = p.get("arxiv_id", "")
                ver = p.get("version", 1)
                if aid and ver > index.get(aid, 0):
                    index[aid] = ver
        except Exception:
            continue
    return index


def dedup_papers(papers: list[dict], history: dict[str, int]) -> list[dict]:
    """
    去重：
    - 历史中不存在 → 保留（新论文）
    - 历史中存在但版本更高 → 保留（论文有更新）
    - 历史中存在且版本相同或更低 → 跳过
    """
    kept = []
    for p in papers:
        aid = p["arxiv_id"]
        ver = p.get("version", 1)
        hist_ver = history.get(aid, 0)
        if ver > hist_ver:
            kept.append(p)
        else:
            logger.info("  跳过已收录: %s v%d (历史 v%d)", aid, ver, hist_ver)
    return kept


def process_date(target_date: str, base_dir: str, config: dict, history: dict[str, int], dry_run: bool) -> int:
    """
    处理单个日期的论文。返回收录篇数。
    """
    search_keywords = config.get("search_keywords", [])
    categories = config.get("categories", [])
    filter_keywords = config.get("filter_keywords", [])
    boost_keywords = config.get("boost_keywords", [])
    max_results = config.get("max_results", 200)
    min_score = config.get("llm", {}).get("min_relevance_score", 4)

    # Step 1: 查询 arxiv API（含日期过滤）
    logger.info("[1/4] 查询 arxiv API (日期: %s)...", target_date)
    query = build_query(search_keywords, categories, date_str=target_date)
    papers = fetch_arxiv_papers(query, config, max_results=max_results)
    logger.info("  获取到 %d 篇论文", len(papers))

    # Step 1b: 查询更新论文（v2+ 在目标日期修订的）
    updates_config = config.get("updates", {})
    if updates_config.get("fetch_updates", True):
        max_results_updates = updates_config.get("max_results_updates", 500)
        logger.info("[1b/4] 查询更新论文 (updated on %s, v2+)...", target_date)
        query_no_date = build_query(search_keywords, categories)
        updated_papers = fetch_updated_papers(query_no_date, config, target_date, max_results=max_results_updates)
        logger.info("  获取到 %d 篇更新论文", len(updated_papers))

        if updated_papers:
            # 合并去重：按 arxiv_id 保留版本更高的
            existing = {p["arxiv_id"]: p for p in papers}
            for up in updated_papers:
                aid = up["arxiv_id"]
                if aid not in existing or up["version"] > existing[aid].get("version", 1):
                    existing[aid] = up
            papers = list(existing.values())
            logger.info("  合并后共 %d 篇论文", len(papers))

    if not papers:
        logger.info("  该日期无论文，跳过。")
        return 0

    # Step 2: 关键词精筛
    logger.info("[2/4] 关键词精筛 (过滤词: %d)...", len(filter_keywords))
    filtered = keyword_filter(papers, filter_keywords, boost_keywords)
    logger.info("  关键词匹配: %d 篇", len(filtered))

    if not filtered:
        return 0

    # Step 2.5: 历史去重
    before_dedup = len(filtered)
    filtered = dedup_papers(filtered, history)
    logger.info("  去重后: %d 篇 (跳过 %d 篇已收录)", len(filtered), before_dedup - len(filtered))

    if not filtered:
        return 0

    if dry_run:
        for p in filtered:
            logger.info("  - [%s] %s", p["arxiv_id"], p["title"])
        return len(filtered)

    # Step 3: LLM 预评分（并发）
    concurrency = config.get("concurrency", 4)
    logger.info("[3/4] LLM 预评分 (%d 篇, 阈值: %s, 并发: %d)...", len(filtered), min_score, concurrency)

    def _pre_score(paper):
        score = quick_relevance_check(paper, config)
        return paper, score

    relevant_papers = []
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {executor.submit(_pre_score, p): p for p in filtered}
        for future in as_completed(futures):
            paper, score = future.result()
            if score is None:
                logger.info("  预评分失败，保留: %s", paper["title"][:60])
                relevant_papers.append(paper)
            elif score >= min_score:
                logger.info("  预评分: %.1f/10 -> 通过: %s", score, paper["title"][:60])
                relevant_papers.append(paper)
            else:
                logger.info("  预评分: %.1f/10 -> 跳过: %s", score, paper["title"][:60])
    logger.info("  预评分通过: %d/%d 篇", len(relevant_papers), len(filtered))

    if not relevant_papers:
        return 0

    # Step 4: 逐篇处理（获取全文 → LLM 评分/摘要 → 落盘，并发）
    logger.info("[4/4] 逐篇处理 (%d 篇, 并发: %d)...", len(relevant_papers), concurrency)
    total_saved = 0
    source_stats = {"latex": 0, "pdf": 0, "abstract_only": 0}
    write_lock = threading.Lock()

    def _process_paper(paper):
        content, source_type = fetch_paper_content(paper["arxiv_id"], config)
        if content:
            logger.info("  [%s] 全文来源: %s (%d 字符)", paper["arxiv_id"], source_type, len(content))
        else:
            logger.info("  [%s] 全文来源: %s", paper["arxiv_id"], source_type)

        result = score_and_summarize(paper, config, full_content=content or None, content_source=source_type)
        return paper, result, source_type

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {executor.submit(_process_paper, p): p for p in relevant_papers}
        for future in as_completed(futures):
            paper, result, source_type = future.result()
            with write_lock:
                source_stats[source_type] += 1
            if not result:
                logger.info("  [%s] 跳过 (评分过低或处理失败)", paper["arxiv_id"])
                continue

            logger.info("  [%s] 评分: %.1f/10, 标签: %s", paper["arxiv_id"], result["relevance_score"], result["tags"])

            with write_lock:
                filepath = write_paper_file(paper, result, base_dir, target_date, config)
                logger.info("  [%s] 写入: %s", paper["arxiv_id"], filepath)
                append_paper_json(paper, result, base_dir, target_date, config)
                total_saved += 1
                logger.info("  已落盘 (%d 篇累计)", total_saved)

        # 所有论文处理完后统一更新 README
        update_readme(base_dir, target_date, config)

    logger.info("  全文统计: LaTeX %d, PDF %d, 仅摘要 %d",
                source_stats["latex"], source_stats["pdf"], source_stats["abstract_only"])
    return total_saved


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Fetch daily arXiv agentic time-series papers")
    parser.add_argument("--date", type=str, help="Target date (YYYY-MM-DD), overrides auto-detection")
    parser.add_argument("--base-dir", type=str, default=None, help="Project root directory")
    parser.add_argument("--dry-run", action="store_true", help="Only fetch and filter, don't call LLM")
    args = parser.parse_args()

    base_dir = args.base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(base_dir, ".env"))

    # 确定目标日期
    if args.date:
        target_dates = [args.date]
    else:
        target_dates = get_target_dates()

    logger.info("=== Daily Agentic Time Series Papers ===")
    logger.info("目标日期: %s", ", ".join(target_dates))
    logger.info("项目目录: %s", base_dir)

    config = load_config(base_dir)

    # 加载历史去重索引（所有日期共享）
    logger.info("加载历史数据去重...")
    history = load_history_index(base_dir)
    logger.info("历史索引: %d 篇论文", len(history))

    grand_total = 0
    for target_date in target_dates:
        logger.info("")
        logger.info(">>> 处理日期: %s <<<", target_date)
        saved = process_date(target_date, base_dir, config, history, args.dry_run)
        grand_total += saved
        logger.info(">>> %s 完成: 收录 %d 篇 <<<", target_date, saved)

    if args.dry_run:
        logger.info("=== Dry Run 结果: 共 %d 篇待处理 ===", grand_total)
    else:
        logger.info("=== 完成! 共收录 %d 篇论文 ===", grand_total)


if __name__ == "__main__":
    main()
