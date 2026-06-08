# Daily Agentic Time Series Papers 论文过滤规则

## 收录流程

```
arxiv API 查询 → 关键词精筛 → 历史去重 → LLM 预评分 → 全文处理 + LLM 评分/摘要 → 落盘
```

## Step 1: arxiv API 查询（服务端过滤）

- **主查询**: 按 `submittedDate` 过滤目标日期新提交的论文
- **更新查询 (Step 1b)**: 按 `LastUpdatedDate` 排序，客户端过滤出在目标日期修订的 v2+ 论文
- **搜索关键词** (`search_keywords`): agent, multi-agent, multi agent, MAS, tool use, tool-use, agent memory, agentic, agentic RL, reasoning, CoT, chain of thought, chains of thought
- **arxiv 类别** (`categories`): cs.AI, cs.CL, cs.MA, cs.LG, cs.SE

### 更新论文过滤条件

1. 版本 >= 2（仅修订论文）
2. 发布日期 (published) >= 2023-01-01（ChatGPT 发布后，即 LLM 时代的论文）
3. 更新日期 (updated) 匹配目标日期

## Step 2: 关键词精筛（客户端过滤）

标题或摘要中至少命中 `filter_keywords` 中的一个关键词才保留。详见 `config.yaml` 中的完整列表。

`boost_keywords` 中命中越多的论文，在后续评分中可获得加权。

## Step 2.5: 历史去重

- 已收录且版本相同或更低的论文会被跳过
- 版本更高的论文会被保留（视为内容更新）

## Step 3: LLM 预评分

- 使用 LLM 快速判断论文与 Agentic Time Series、可解释时序诊断和时序报告生成方向的相关性
- 评分低于 `min_relevance_score`（默认 4/10）的论文被过滤

## Step 4: 全文处理

- 获取论文全文（LaTeX > PDF > 仅摘要）
- LLM 生成结构化评分和 Q&A 解读
- 写入 markdown 文件和 papers.json
