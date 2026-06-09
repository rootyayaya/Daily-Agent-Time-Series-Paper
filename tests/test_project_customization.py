from pathlib import Path
import json
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from markdown_writer import update_readme


class ProjectCustomizationTest(unittest.TestCase):
    def test_config_is_time_series_agent_focused(self):
        config = (ROOT / "config.yaml").read_text(encoding="utf-8")

        required_terms = [
            "time series",
            "TimeSeries2Report",
            "fault diagnosis",
            "industrial",
            "agentic",
        ]
        for term in required_terms:
            self.assertIn(term, config)

    def test_daily_workflow_is_renamed_for_target_project(self):
        workflow = (ROOT / ".github" / "workflows" / "daily_arxiv.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("Daily Arxiv Agentic Time Series Papers", workflow)
        self.assertIn("Daily-Agent-Time-Series-Paper", workflow)
        self.assertIn("scripts/fetch_papers.py", workflow)

    def test_frontend_links_to_target_repository(self):
        page = (ROOT / "web" / "src" / "app" / "page.tsx").read_text(encoding="utf-8")
        taxonomy = (ROOT / "web" / "src" / "app" / "taxonomy" / "page.tsx").read_text(
            encoding="utf-8"
        )

        expected_url = "https://github.com/rootyayaya/Daily-Agent-Time-Series-Paper"
        self.assertIn(expected_url, page)
        self.assertIn(expected_url, taxonomy)
        self.assertNotIn("CMander02/DailyAgentPapers", page)
        self.assertNotIn("CMander02/DailyAgentPapers", taxonomy)

    def test_data_index_is_available(self):
        index = json.loads((ROOT / "data" / "index.json").read_text(encoding="utf-8"))

        self.assertIn("available_dates", index)
        self.assertIsInstance(index["available_dates"], list)

    def test_config_defines_two_recommendation_layers(self):
        config = (ROOT / "config.yaml").read_text(encoding="utf-8")

        self.assertIn("min_relevance_score: 6.5", config)
        self.assertIn("core_recommendation_score: 8.0", config)
        self.assertIn("related_recommendation_score: 6.5", config)

    def test_frontend_fetches_all_saved_papers_for_two_layers(self):
        data_ts = (ROOT / "web" / "src" / "lib" / "data.ts").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("all.filter((p) => p.relevance_score >= 8)", data_ts)
        self.assertIn("cachedDayPapers[dateStr] = all", data_ts)

    def test_readme_groups_core_and_related_papers(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            day_dir = base / "data" / "2026" / "06" / "04"
            day_dir.mkdir(parents=True)
            papers = [
                {
                    "title": "Core Paper",
                    "arxiv_url": "https://arxiv.org/abs/1",
                    "tags": ["核心", "时序"],
                    "relevance_score": 8.2,
                },
                {
                    "title": "Related Paper",
                    "arxiv_url": "https://arxiv.org/abs/2",
                    "tags": ["可借鉴"],
                    "relevance_score": 7.1,
                },
            ]
            (day_dir / "papers.json").write_text(
                json.dumps(papers, ensure_ascii=False), encoding="utf-8"
            )

            update_readme(
                str(base),
                "2026-06-04",
                {
                    "output": {
                        "core_recommendation_score": 8.0,
                        "related_recommendation_score": 6.5,
                    }
                },
            )

            readme = (base / "README.md").read_text(encoding="utf-8")
            self.assertIn("### 核心推荐 (1 篇)", readme)
            self.assertIn("### 可借鉴论文 (1 篇)", readme)
            self.assertIn("Core Paper", readme)
            self.assertIn("Related Paper", readme)
            self.assertNotIn("## 输出口径", readme)
            self.assertNotIn("## 配置提醒", readme)
            self.assertNotIn("LLM_API_KEY", readme)


if __name__ == "__main__":
    unittest.main()
