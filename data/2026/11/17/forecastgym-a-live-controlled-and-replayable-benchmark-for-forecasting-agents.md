---
title: "ForecastGym: A Live, Controlled, and Replayable Benchmark for Forecasting Agents"
authors:
  - "Yicheng Tao"
  - "Yuante Li"
  - "Zipei Fan"
date: "2026-11-17"
arxiv_id: "2611.23045"
arxiv_url: "https://arxiv.org/abs/2611.23045"
pdf_url: "https://arxiv.org/pdf/2611.23045v1"
categories:
  - "cs.AI"
  - "cs.CL"
tags:
  - "LLM Agent"
  - "Forecasting Agent"
  - "Benchmark"
  - "Evidence Routing"
  - "Memory Strategy"
  - "Web Search"
  - "Prediction Market"
  - "Time Series Forecasting"
  - "Retrieval-Augmented Generation"
  - "Evaluation"
relevance_score: 7.5
---

# ForecastGym: A Live, Controlled, and Replayable Benchmark for Forecasting Agents

## 原始摘要

Agents built on large language models (LLMs) increasingly forecast real-world events by searching the Web and reasoning over what they find. How well such an agent forecasts depends on both the retrieved evidence and the model, making control over that evidence essential for evaluation. Live evaluations can mix retrieval with reasoning when each system searches on its own, while retrospective search can leak later information through date filters or today's ranking of historical pages. Comparing models, search sources, and memory strategies requires both fixed evidence and a record of how it evolved before resolution. We introduce ForecastGym, which records what four commercial web search APIs return for open prediction-market questions every two days and replays this frozen evidence offline once outcomes are known, comparing models, memory, and captured search sources under a fixed evidence-acquisition policy. Its first release covers 150 questions, 614 evidence states, one per question and collection time, and 131k search results. Rerunning the same queries after settlement returns results that all but state the outcome for up to 92% of the questions, despite the tested date filters. On the frozen evidence, all tested LLMs trail the market in forecasting accuracy. Our diagnostic analysis suggests that missed public information contributes more to the gap in high-gap states than misreading does. Switching the search API changes a model's Brier score by up to 0.043, more than the spread across models, while persistent notes score similarly to rereading all evidence at half the input tokens. The evidence a forecaster sees can matter as much as the model that reads it.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决LLM智能体在预测真实世界事件时缺乏可控、可复现评测基准的问题。研究背景是：预测市场与LLM智能体已能通过搜索网页并推理来预测事件，其准确率接近人类预测群体，因此需要在可比条件下评估它们。然而，预测结果同时取决于检索到的证据和阅读证据的模型，现有基准分为“实时”和“回溯”两类，均存在明显不足：回溯评测难以还原某一时刻真实可得的证据，日期过滤会混入事后更新内容，历史快照也可能按今天的索引排序，造成信息泄漏；实时评测中每个系统自行检索，使检索与推理纠缠，分数无法归因；证据随事件临近不断演化，缺乏可复用的证据轨迹来固定输入、单独变化记忆策略；搜索服务商不同会改变智能体所见内容，其影响难以与模型差异分离。本文的核心问题是：如何把“证据”作为受控实验变量，在问题尚未揭晓时前瞻性记录各搜索API返回的结果，并在结果已知后离线回放这些冻结证据，从而在固定证据获取策略下，分别比较模型、记忆策略与搜索来源，并诊断模型落后于市场的原因。

### Q2: 有哪些相关研究？

本文的相关工作主要分为三类。第一类是预测评测基准。早期数据集如ForecastQA将事件预测建模为问答，Autocast将预测竞赛问题与按日期索引的新闻语料配对；后续系统通过检索新闻、工具推理或多模型聚合生成概率预测。实时基准（ForecastBench、FutureX、Prophet Arena、Daily Oracle、MIRAI）在结果揭晓前评估提交的预测并刷新问题以避免污染；回顾式基准（Bench to the Future、Hindcast）提供可复用的历史环境，但前者冻结页面内容却仍用实时Google搜索，可能改变排序，后者回放Reddit存档。ForecastGym的区别在于同时做到前瞻性采集与离线精确回放，保留各搜索提供商在结果揭晓前返回的原始结果。第二类是智能体的搜索证据。RealTime QA、FreshLLMs表明检索证据本身应被评估；BrowseComp-Plus用精选语料分离检索与推理，Deep Research Bench冻结抓取页面；Dr-CiK测试时间序列预测的支撑上下文检索，WorldReasoner评估事件预测所引证据；OpenHands-Versa与Selvam和Ghosh发现不同搜索提供商带来性能与证据差异。Prophet Arena审计时间门控搜索但承认排序泄漏且导出不含页面文本，无法精确回放。第三类是信念修正与记忆。EvolveCast比较新闻更新后的预测修正，但问题—新闻关联是回溯重建的；FutureSim回放新闻流研究长期适应与记忆；ForecastCompass跨任务迁移记忆；LongMemEval考察长对话中的记忆保持。这些工作要么事后重建证据，要么跨任务迁移记忆，均未在结果揭晓前捕获的固定证据上隔离记忆效应，而ForecastGym通过固定同一问题的证据轨迹、仅改变智能体保留内容来填补这一空白。

### Q3: 论文如何解决这个问题？

论文提出 ForecastGym，一个“实时采集 + 受控回放”的两阶段基准，核心是把“预测智能体看到的证据”从模型推理中剥离出来，使模型、搜索源、记忆策略可以单因子对比。

整体框架分两阶段。第一阶段 Live Capture：对每个预测市场问题，每两天用四个商业搜索 API（Serper、Tavily、Parallel、Exa）在采集时刻实时发起查询并记录返回结果，形成证据状态 E_t^(k)。由于查询在 t 时刻本身发出，证据天然满足时间有效性（R1），避免回溯搜索中“旧日期页面内容已被改写”的泄漏；同时用 LLM 统一生成初始查询计划（resolution、current-evidence、base-rate、counterevidence 四类）及最多两条追问，保证不同搜索源在相同查询策略下比较（R2）。第二阶段 Controlled Replay：结果揭晓后，将冻结的证据快照离线回放给智能体，每次运行读取完全相同的证据（R3），并加入三重防护——隐藏晚于状态的条目、隐藏问题自身市场价格、合并近重复内容。

关键设计是把记忆显式化为可替换对象 M_{t-1}=(p_{t-1}, R_{t-1}, N_{t-1})，即上一轮预测、理由与智能体每步重写的笔记，从而能像更换模型或搜索源一样单独干预记忆。基于此，论文定义了模型、搜索源、证据、记忆四类单因子干预（如 closed-book、final-only、previous-only、no-memory、全量证据、BM25 检索等），以 Brier 分数差值量化各组件贡献。

创新点在于：用检索时间而非发布日期界定“可知性”，用冻结回放保证跨运行证据不变，并用滚动采集协议持续补充新问题以防止记忆污染，从而把“证据”本身变成可度量、可控制的实验变量。

### Q4: 论文做了哪些实验？

论文围绕四个研究问题展开实验。RQ1检验事后搜索能否替代实时抓取：在60个已结算问题上重跑查询，原始结果泄漏率31%–42%，加日期过滤后仍为17%–27%，被"揭示"结局的问题比例高达43%–92%，且过滤后Brier分数（0.080–0.194）明显优于实时快照（0.224），说明泄漏会虚高成绩。RQ2比较模型与市场：在Tavily冻结证据上评估GPT-5.6 Terra、Claude Sonnet 5、Gemini 3.8 Flash、DeepSeek-V4.1-Flash四个模型，末状态Brier为0.217–0.244，准确率0.597–0.660，均落后市场（0.176/0.719）；闭卷均不如常数0.5预测；差距主要来自分辨力不足而非校准，且近三倍归因于漏检公开信息而非误读。RQ3消融记忆：持久笔记TBS 0.228最佳，无记忆0.237且更新幅度翻倍，笔记以9.5M token实现与重读全部证据（19.5M）相当的效果。RQ4比较搜索源：固定Gemini切换API使Brier变化达0.043，超过模型间差异，且Kendall's τ=0，模型排序随来源改变。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有以下几点。其一，证据捕获虽冻结了检索结果，但仍是“被动回放”，未来可探索主动式证据获取策略，例如让智能体自主决定何时、向哪个源发起查询，并在回放中模拟多源交叉验证，而非固定采集策略。其二，诊断显示差距主要来自“未检索到公开信息”而非“误读”，这提示可研究查询规划与证据补全机制，如基于市场分歧信号反向生成检索意图，或引入多源证据融合与冲突消解模块。其三，记忆实验表明笔记能稳定预测却可能固化错误解读，未来可探索带不确定性标注、可自我修正的结构化记忆，以及记忆与检索的联合优化。其四，当前基准仅覆盖预测市场且以Brier评分为主，可扩展到更细粒度的事件类型与多步推理任务，并结合交易模拟评估实际决策价值。此外，搜索API差异对分数影响超过模型差异，值得系统研究检索源质量评估与自适应源选择。

### Q6: 总结一下论文的主要内容

论文针对LLM预测智能体评测中证据不可控的问题，提出ForecastGym基准。问题定义：预测结果同时取决于检索到的证据与推理模型，现有live评测混淆检索与推理，回溯检索又因日期过滤和今日排序而泄漏未来信息，难以单独比较模型、搜索源与记忆策略。方法上分两阶段：第一阶段在预测市场问题尚未揭晓时，每两天调用四个商业搜索API记录证据状态，并共享初始查询计划；第二阶段在结果揭晓后离线回放冻结证据，每次只改变模型、搜索源或记忆中的一个因素。首个版本含150个问题、614个证据状态和13.1万条搜索结果。主要结论：事后重跑查询可泄漏高达92%问题的结果；在冻结证据上所有LLM均落后于市场，差距主要源于遗漏公开信息而非误读；更换搜索API可使Brier分数变动达0.043，超过模型间差异；记忆主要起稳定预测作用。其意义在于确立了"证据即受控变量"的评测范式。
