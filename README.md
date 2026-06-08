# Daily Agentic Time Series Papers

每日 arXiv 时序智能体论文自动检索、评分、中文解读与网页归档。

本仓库聚焦以下方向：

- Agentic Time Series / 时间序列智能体
- TimeSeries2Report、时序语义描述、报告生成
- 可解释故障诊断、工业时序、预测性维护
- RAG、工具调用、多智能体推理、Skill-MoE、自进化工作流

## 最新论文

暂无自动收录结果。配置好 GitHub Actions Secrets 后，可手动触发 `Daily Arxiv Agentic Time Series Papers` 工作流生成第一批论文。

## 本地运行

```bash
pip install -r requirements.txt
python scripts/fetch_papers.py --dry-run
python scripts/fetch_papers.py --date 2026-06-08
```

## GitHub Actions Secrets

在仓库 `Settings -> Secrets and variables -> Actions` 中添加：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`

工作流会在北京时间工作日 14:30 自动运行，也可在 Actions 页面手动触发。

## 输出结构

```text
data/
  index.json
  YYYY/MM/DD/
    papers.json
    paper-title.md
web/
  Next.js static site for GitHub Pages
```

## Attribution

This project is adapted from [CMander02/DailyAgentPapers](https://github.com/CMander02/DailyAgentPapers), licensed under the MIT License.
