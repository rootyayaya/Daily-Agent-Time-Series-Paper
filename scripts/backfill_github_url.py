#!/usr/bin/env python3
"""
回填脚本：为所有已有论文的 .md frontmatter 和 papers.json 添加 github_url 字段。

两步策略：
  1. 从本地 .md 的原始摘要提取 GitHub URL（零 API 调用）
  2. 用 arxiv API 批量查询 comment 字段，补充摘要中没有的

用法:
    python scripts/backfill_github_url.py              # 完整回填（含 API 查询）
    python scripts/backfill_github_url.py --local-only  # 仅从本地摘要提取，不查 API
    python scripts/backfill_github_url.py --dry-run      # 预览，不写文件
"""

import argparse
import glob
import json
import logging
import os
import re
import sys
import time

import arxiv

# 复用项目已有的提取函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arxiv_client import extract_github_url

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_frontmatter(text: str) -> tuple[dict, str, str]:
    """
    解析 markdown 文件，返回 (frontmatter_dict, frontmatter_raw, body)。
    frontmatter_raw 包含 --- 分隔符之间的原始文本。
    """
    match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$', text)
    if not match:
        return {}, "", text
    raw = match.group(1)
    body = match.group(2)

    fm = {}
    for m in re.finditer(r'^(\w+):\s*"?([^"\n]*)"?\s*$', raw, re.MULTILINE):
        fm[m.group(1)] = m.group(2)
    return fm, raw, body


def extract_summary_from_md(body: str) -> str:
    """从 markdown body 中提取原始摘要 section。"""
    match = re.search(r'## 原始摘要\s*\r?\n\r?\n([\s\S]*?)(?=\r?\n## |$)', body)
    return match.group(1).strip() if match else ""


def inject_github_url_in_frontmatter(raw_fm: str, github_url: str) -> str:
    """在 frontmatter 的 pdf_url 行后插入 github_url 行。"""
    # 如果已有 github_url 行，替换它
    if re.search(r'^github_url:', raw_fm, re.MULTILINE):
        return re.sub(
            r'^github_url:.*$',
            f'github_url: "{github_url}"',
            raw_fm,
            flags=re.MULTILINE,
        )
    # 在 pdf_url 行后插入
    return re.sub(
        r'^(pdf_url:\s*"[^"]*")\s*$',
        rf'\1\ngithub_url: "{github_url}"',
        raw_fm,
        flags=re.MULTILINE,
    )


def batch_fetch_comments(arxiv_ids: list[str], batch_size: int = 50, delay: float = 5.0) -> dict[str, str]:
    """
    批量查询 arxiv API 获取 comment 字段。
    返回 {arxiv_id: comment}。
    """
    comments = {}
    client = arxiv.Client(page_size=100, delay_seconds=delay, num_retries=3)

    for i in range(0, len(arxiv_ids), batch_size):
        batch = arxiv_ids[i:i + batch_size]
        logger.info("  查询 arxiv API: %d-%d / %d", i + 1, min(i + batch_size, len(arxiv_ids)), len(arxiv_ids))

        search = arxiv.Search(id_list=batch)
        for result in client.results(search):
            raw_id = result.entry_id.split("/abs/")[-1]
            aid = re.sub(r"v\d+$", "", raw_id)
            comment = (result.comment or "").strip()
            if comment:
                comments[aid] = comment

        if i + batch_size < len(arxiv_ids):
            time.sleep(delay)

    return comments


def main():
    parser = argparse.ArgumentParser(description="Backfill github_url for existing papers")
    parser.add_argument("--local-only", action="store_true", help="Only extract from local abstracts, skip API")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--base-dir", type=str, default=None)
    args = parser.parse_args()

    base_dir = args.base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")

    # ── Step 1: 扫描所有 .md 文件，从本地摘要提取 GitHub URL ──
    md_files = sorted(glob.glob(os.path.join(data_dir, "**", "*.md"), recursive=True))
    logger.info("扫描到 %d 个 .md 文件", len(md_files))

    # {arxiv_id: {md_path, github_url, summary}}
    papers_info = {}
    for md_path in md_files:
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read()
        fm, raw_fm, body = parse_frontmatter(text)
        aid = fm.get("arxiv_id", "")
        if not aid:
            continue

        summary = extract_summary_from_md(body)
        github_url = extract_github_url(summary)

        papers_info[aid] = {
            "md_path": md_path,
            "raw_fm": raw_fm,
            "body": body,
            "full_text": text,
            "summary": summary,
            "github_url": github_url,
        }

    local_found = sum(1 for v in papers_info.values() if v["github_url"])
    logger.info("本地摘要提取: %d / %d 篇有 GitHub URL", local_found, len(papers_info))

    # ── Step 2: 用 arxiv API 查询 comment 字段补充 ──
    if not args.local_only:
        missing_ids = [aid for aid, info in papers_info.items() if not info["github_url"]]
        logger.info("需要查询 API 补充 comment: %d 篇", len(missing_ids))

        if missing_ids:
            comments = batch_fetch_comments(missing_ids)
            logger.info("API 返回 %d 个 comment", len(comments))

            api_found = 0
            for aid, comment in comments.items():
                if aid in papers_info and not papers_info[aid]["github_url"]:
                    url = extract_github_url(comment)
                    if url:
                        papers_info[aid]["github_url"] = url
                        api_found += 1
            logger.info("API comment 补充: %d 篇新增 GitHub URL", api_found)

    total_found = sum(1 for v in papers_info.values() if v["github_url"])
    logger.info("总计: %d / %d 篇有 GitHub URL", total_found, len(papers_info))

    if args.dry_run:
        for aid, info in sorted(papers_info.items()):
            if info["github_url"]:
                logger.info("  [%s] %s", aid, info["github_url"])
        logger.info("Dry run 完成，未写入文件。")
        return

    # ── Step 3: 写入 .md frontmatter ──
    md_updated = 0
    for aid, info in papers_info.items():
        github_url = info["github_url"]
        raw_fm = info["raw_fm"]
        body = info["body"]
        md_path = info["md_path"]

        # 检查是否已有 github_url 且值相同
        existing = re.search(r'^github_url:\s*"([^"]*)"', raw_fm, re.MULTILINE)
        if existing and existing.group(1) == github_url:
            continue
        if not github_url and not existing:
            continue

        if github_url:
            new_fm = inject_github_url_in_frontmatter(raw_fm, github_url)
        else:
            # 没有 github_url 也不需要添加空行
            continue

        new_text = f"---\n{new_fm}\n---\n{body}"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(new_text)
        md_updated += 1

    logger.info("更新 %d 个 .md 文件", md_updated)

    # ── Step 4: 更新 papers.json ──
    json_files = sorted(glob.glob(os.path.join(data_dir, "**", "papers.json"), recursive=True))
    json_updated = 0
    for json_path in json_files:
        with open(json_path, "r", encoding="utf-8") as f:
            papers = json.load(f)

        changed = False
        for p in papers:
            aid = p.get("arxiv_id", "")
            if aid in papers_info:
                new_url = papers_info[aid]["github_url"]
                old_url = p.get("github_url", "")
                if new_url != old_url:
                    p["github_url"] = new_url
                    changed = True
            elif "github_url" not in p:
                p["github_url"] = ""
                changed = True

        if changed:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(papers, f, ensure_ascii=False, indent=2)
            json_updated += 1

    logger.info("更新 %d 个 papers.json 文件", json_updated)

    # ── Step 5: 同步到 web/public/data/ ──
    import shutil
    web_data = os.path.join(base_dir, "web", "public", "data")
    if os.path.isdir(web_data):
        synced = 0
        for json_path in json_files:
            rel = os.path.relpath(json_path, data_dir)
            dst = os.path.join(web_data, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(json_path, dst)
            synced += 1
            # 同步同目录下的 .md
            src_dir = os.path.dirname(json_path)
            dst_dir = os.path.dirname(dst)
            for fname in os.listdir(src_dir):
                if fname.endswith(".md"):
                    shutil.copy2(os.path.join(src_dir, fname), os.path.join(dst_dir, fname))
        logger.info("同步到 web/public/data/: %d 个目录", synced)

    logger.info("完成!")


if __name__ == "__main__":
    main()
