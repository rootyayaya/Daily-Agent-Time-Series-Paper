---
title: "Benchmarking Forecasting Agents on Yesterday's Tomorrows"
authors:
  - "Yuxuan Wang"
  - "Yishu Wang"
  - "Jiaqi Deng"
date: "2026-10-29"
arxiv_id: "2610.40940"
arxiv_url: "https://arxiv.org/abs/2610.40940"
pdf_url: "https://arxiv.org/pdf/2610.40940v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "Forecasting Agents"
  - "Benchmark"
  - "Retrieval-Augmented Generation"
  - "Evidence Weighting"
  - "Probabilistic Forecasting"
  - "LLM Agent Evaluation"
relevance_score: 6.5
---

# Benchmarking Forecasting Agents on Yesterday's Tomorrows

## 原始摘要

Digital agents can now gather and organize information, reason over it, and use tools to complete complex tasks. Forecasting puts all of these abilities to the test: it requires integrating incomplete evidence, inferring causal drivers, and committing to calibrated probabilistic judgments. Existing benchmarks are poorly suited to measuring and improving this ability. Live benchmarks provide feedback only after events resolve, so every evaluation cycle waits on the calendar; fixed-corpus evaluations return results immediately but confine research to pre-collected documents. We introduce FABench, a scalable backtesting environment for Forecasting Agents. An automated pipeline discovers events, generates questions, and resolves outcomes for any past forecast date, so the benchmark can be renewed to stay ahead of model training cutoffs; its first release poses 287 questions across nine domains. Agents research each question freely in an archive environment that combines an offline archive with live web search screened to prevent temporal leakage. Evaluating agents built on eight recent models, we find that retrieval improves the Brier score of all eight in every retrieval setting and lifts the leading agents to the market consensus on the 54 questions linked to Polymarket, with the best three scoring slightly above it. Research traces reveal recurring failures in how agents weigh and apply evidence, leaving ample room for improvement. We release our code, data, and archive environment as a foundation for community research on forecasting agents.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是如何衡量和提升 LLM 智能体的预测（forecasting）能力。预测任务要求智能体整合不完整甚至相互冲突的证据、推断因果驱动因素，并给出经过校准的概率判断，是检验不确定性下决策能力的严苛场景，现有 LLM 预测者已开始接近人类专家水平。但现有预测基准存在两类互补缺陷：一是“实时基准”，只能等事件真正发生后才能获得反馈，评估周期受日历制约，题目由待决事件决定，不同时期的分数无法比较；二是“固定语料基准”，虽能即时、可复现地反馈，但智能体只能研究基准创建者预先收集的文档，语料外证据无法获取，且题目集固定、会饱和，结果最终进入模型训练数据。本文提出 FABench，一个可扩展的预测智能体回测环境，试图消除这一权衡：它在结果已知的历史时点出题，使反馈即时且可验证，同时让智能体在限定于该时点之前发布内容的档案环境与实时网页中自由检索，保持研究的开放性；并通过自动化流水线发现事件、生成问题、解析结果，使基准可按需更新、领先于模型训练截止时间，从而系统性地测量并改进智能体的预测能力。

### Q2: 有哪些相关研究？

本文的相关工作可分为两类。

**实时评测类（Live benchmarks）**：ForecastBench、Prophet Arena 和 FutureX 等基准在事件尚未揭晓时提出问题，因而不会泄漏结果，答案对模型不可见。但它们必须等待事件真正发生才能评分，评测周期受日历约束，且不同时间评测的系统回答的是不同问题，可比性差。其中 FutureX 缺少校准度量，ForecastBench 仅部分支持开放检索与校准。

**回测类（Backtest benchmarks）**：Autocast、Daily Oracle、BTF-2 和 ATM 可即时评分。Daily Oracle 从报道结果的新闻中生成问题，属于事后选题，存在结果泄漏；Autocast 将预测限制在预先收集的语料内，不支持开放检索；BTF-2 在选题与评分上最接近本文，但其语料需在问题开放期间提前爬取，新时段须预先规划采集，模型训练更新后需重新构建数据集；ATM 虽允许智能体检索实时网页，但其过滤机制会读取问题及已知答案，可能使证据偏向结果，且它复用已有问题并只评分点预测，无法揭示校准性。

**本文区别**：FABench 针对任意历史预测日期事后构建问题集，新闻档案独立于问题采集，网页仅按发布时间过滤，从而同时实现即时评分、结果盲、开放检索、答案盲与校准评估，并支持随模型训练截止时间滚动更新。

### Q3: 论文如何解决这个问题？

论文提出 FABench，一个可扩展的“回测式”预测智能体基准，核心思路是把每个问题锚定在过去某个预测日 t₀，让智能体只能使用 t₀ 之前发布的信息，从而无需等待事件发生即可即时评分。整体框架分两部分：上半部分是自动出题流水线，以 t₀ 为输入，从两类来源生成问题——一是定期发布（如标普100公司财报、央行决议、官方统计数据），由 LLM 智能体从 t₀ 前公布的日历中挑选 t₀ 后到期的事件，再用模板和固定规则计算阈值，保证阈值与结果无关；二是新兴事件（选举、药物审批、产品发布等），通过检索 t₀ 前的新闻与事件日历，并从 Polymarket 取 t₀ 时仍开放的市场，保留其措辞与结算规则，市场在 t₀ 前的价格即人类基线。随后由第二个智能体校验问题是否可无歧义结算、在 t₀ 时是否仍开放、是否泄露 t₀ 后信息，结算后从指定来源记录结果。下半部分是档案环境：离线档案由 t₀ 前抓取的 CC-News 新闻（约2010万篇）和 t₀ 前最后一次修订的维基百科页面构成，天然不会泄露；检索用 BM25 加规则去重重排，词项统计全部来自 t₀ 前文档，保证同一查询结果可复现。为弥补档案覆盖不足，搜索还调用实时搜索引擎，但每个网页先抓取、清洗，再由一个看不到问题和答案的 LLM 审查者仅按发布时间判断是否在 t₀ 前公开，时间不明或含 t₀ 后信息则整页扣留，预测市场站点一律拒绝。创新点在于：按发布时间而非事件发生时间过滤、审查者答案盲以避免证据偏向结果、档案与网页按固定比例混合使结果不依赖单一来源，以及可针对任意过去 t₀ 事后重建题目集，从而跟上模型训练截止时间。

### Q4: 论文做了哪些实验？

论文在FABench回测环境中评估了8个模型（GPT-6 Astra、GPT-6 Sol、Claude Opus 5.5、DeepSeek V4.1 Flash、Kimi K3、GLM 5.3、Qwen3.8-27B、Qwen3.6-35B-A3B），并引入两个校准模型JEV 1.13.0和StartLux 27B作参照，基线为常数预测0.5和Polymarket市场共识。实验设置四种信息条件：none（无工具）、archive（仅离线档案）、online-filtered（仅过滤后的网络搜索）和full（两者结合），全部287道题（覆盖九个领域，截止日2026年7月1日）在每个设置下均作答，每题最多100次工具调用，以Brier指数（BI）衡量准确性、ECE衡量校准。主要结果：检索在每种设置下都提升了全部8个模型的BI；full设置下五个模型形成57–58 BI的领先组，最佳模型仅消除常数预测约31%的平方误差；无工具时最佳仅55.0 BI。在54道与Polymarket关联的题目上，领先智能体达到市场共识水平，最好的三个略高于市场；无检索时所有模型落后市场1.8–10.8 BI。检索使8个模型中7个的ECE下降。分领域看，full下平均BI从Culture的49.1到Health的63.2不等；检索在72个模型-领域对中分别有48个（archive）和60个（full）得到改善，但也会误导，如Kimi K3在地缘政治上损失4.8 BI。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三。其一，检索虽普遍提升Brier分数，但增益随模型与领域波动明显，说明"如何用证据"比"能否检索到"更关键；未来可研究证据加权、冲突信息消解与因果驱动的推理机制，而非仅扩大检索规模。其二，当前仅287题、九个领域，且以Polymarket关联题为市场对照，样本与领域覆盖有限，可扩展至更多事件类型并引入多市场、多时间尺度校准评估。其三，基准为静态回测，缺少对智能体研究轨迹的过程性奖励；可探索以结果反馈进行强化学习或自训练，将校准误差直接作为训练信号。此外，时间泄漏筛查依赖规则，可引入更严格的反事实泄漏检测；并研究检索失败与过度自信的联合诊断，提升智能体在信息稀缺下的谦逊校准能力。

### Q6: 总结一下论文的主要内容

论文提出 FABench，一个面向预测智能体的可扩展回测环境，旨在解决现有预测基准的两难：实时基准只能等待事件揭晓、反馈滞后且问题不可比；固定语料基准反馈即时但研究范围受限、易饱和并泄漏进训练数据。FABench 将预测视为回测：在结果已知的历史时点提问，使反馈即时可验证；同时让智能体在仅含该时点前信息的离线档案与经时间筛查的实时网页中自由研究。其自动化流水线可从数据发布、新闻与预测市场中发现事件、生成问题并解析结果，首版覆盖九大领域共 287 题，且可按新日期重跑以领先模型训练截止。作者用八个前沿模型构建智能体进行评估，发现检索平均提升 Brier 分数 3.4 分，使领先智能体在 54 个 Polymarket 相关问题上达到甚至略超市场共识；但约四分之一问题上仍劣于恒定 0.5 预测，并揭示三类证据权衡与应用失败模式。该工作为预测智能体的快速评估与基于结果的训练奠定基础。
