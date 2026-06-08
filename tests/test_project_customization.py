from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


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

    def test_empty_data_index_is_available_for_first_deploy(self):
        index = (ROOT / "data" / "index.json").read_text(encoding="utf-8")

        self.assertIn('"available_dates": []', index)


if __name__ == "__main__":
    unittest.main()
