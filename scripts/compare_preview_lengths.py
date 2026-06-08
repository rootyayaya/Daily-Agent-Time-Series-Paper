"""
比较不同 preview 长度对 section planning 的影响。
测试: 100 / 256 / 512 / 1024 字符预览。

用法: python scripts/compare_preview_lengths.py [arxiv_id]
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

from paper_content import _fetch_latex, get_section_list, get_section_previews
from llm_client import call_llm, _load_prompt, _parse_llm_json

QUESTIONS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
Q_LABELS = ["解决什么问题", "相关研究", "如何解决", "做了什么实验", "进一步探索", "总结"]


def plan_with_config(paper, sections, latex, preview_len, label=""):
    """用指定配置调用 section planning。"""
    sections_list = get_section_previews(latex, sections, preview_len)

    system_prompt = _load_prompt("system.txt")
    user_prompt = _load_prompt("section_planning.txt").format_map({
        "title": paper["title"],
        "summary": paper["summary"],
        "sections_list": sections_list,
    })

    print(f"\n{'='*60}")
    print(f"{label}")
    print(f"Sections: {len(sections)}, Preview: {preview_len} chars")
    print(f"Prompt sections_list length: {len(sections_list)} chars")
    print(f"{'='*60}")

    try:
        response = call_llm(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=600,
            timeout=90,
        )
        result = _parse_llm_json(response)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except Exception as e:
        print(f"  Error: {e}")
        return None


def load_config():
    import yaml
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    if len(sys.argv) > 1:
        arxiv_id = sys.argv[1]
    else:
        print("Usage: python compare_preview_lengths.py <arxiv_id>")
        sys.exit(1)

    latex = _fetch_latex(arxiv_id, config)
    if not latex:
        print(f"No LaTeX available for {arxiv_id}.")
        sys.exit(1)

    paper = {"title": arxiv_id, "summary": ""}
    try:
        import arxiv
        result = next(arxiv.Client().results(arxiv.Search(id_list=[arxiv_id])))
        paper["summary"] = result.summary
        paper["title"] = result.title
    except Exception as e:
        print(f"Warning: {e}")
        paper["summary"] = "(unavailable)"

    print(f"\nPaper: {paper['title']}")
    print(f"arXiv: {arxiv_id}")

    sections_all = get_section_list(latex, include_subsections=True)
    sections_only = get_section_list(latex, include_subsections=False)
    print(f"Sections: {len(sections_only)}, With subsections: {len(sections_all)}")

    # 测试不同预览长度
    preview_lengths = [100, 256, 512, 1024]
    results = {}
    for plen in preview_lengths:
        label = f"section+subsection, {plen} chars"
        results[plen] = plan_with_config(paper, sections_all, latex, plen, label)

    # 汇总比较
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)

    for qi, ql in zip(QUESTIONS, Q_LABELS):
        print(f"\n{qi} ({ql}):")
        for plen in preview_lengths:
            plan = results.get(plen)
            if plan:
                secs = plan.get(qi, [])
                print(f"  [{plen:>4}] {secs if secs else '(abstract)'}")

    # 统计各长度的 sections_list 长度
    print(f"\n{'='*70}")
    print("PROMPT SIZE (sections_list only):")
    for plen in preview_lengths:
        sl = get_section_previews(latex, sections_all, plen)
        print(f"  {plen:>4} chars -> {len(sl):>5} chars total")


if __name__ == "__main__":
    main()
