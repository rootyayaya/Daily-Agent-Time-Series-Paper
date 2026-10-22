---
title: "Charts as Epistemic Actions for Experience-Driven Agentic Data Analysis"
authors:
  - "Xinzhe Wang"
  - "Xudong Weng"
  - "Zang Li"
  - "Shaolei Zhang"
date: "2026-10-21"
arxiv_id: "2610.30072"
arxiv_url: "https://arxiv.org/abs/2610.30072"
pdf_url: "https://arxiv.org/pdf/2610.30072v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Data Analysis"
  - "Chart as Epistemic Action"
  - "Experience Distillation"
  - "Trajectory Rollout"
  - "Tool Use"
  - "Visual Reasoning"
  - "Time Series Anomaly Detection"
  - "LLM Agent"
  - "Self-Evolving Skill"
  - "Feedback Optimization"
relevance_score: 7.5
---

# Charts as Epistemic Actions for Experience-Driven Agentic Data Analysis

## 原始摘要

Data agents built on ReAct-style loops now execute complex analytical workflows over structured data, yet their intermediate reasoning still runs almost entirely through text. Human analysts instead move between numbers, tables, and charts, reading visual evidence to expose trends and anomalies that text summaries drop. We ask whether charts can serve as internal epistemic actions inside a data agent's reasoning loop, and how to teach an agent to use them. We first build \probe{}, a suite of 200 controlled tasks under four matched interface conditions, and find a persistent gap between what agents can read and what they choose to use. Agents score as well from self-generated charts as from numeric output, yet plotting access alone does not translate into consistent use. Task slices show that charts lead on temporal, pattern, and anomaly reasoning, while text leads on precise reading and conditional verification. We then propose \method{}, which distils two families of experience from conditioned trajectory rollouts. One family records how to select and verify analytical operations, and the other records when to invoke text, charts, or both. A trajectory judge scores outcomes and labels intermediate steps, and a validation gate admits only experience that improves held-out performance. On three held-out benchmarks with four LLM backbones, \method{} raises analytical accuracy and visual evidence quality over matched baselines, and backbones that never drew charts begin using them, all without touching model parameters.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

当前的数据分析智能体主要基于ReAct式推理-行动循环，能够规划、执行并修正结构化数据上的复杂分析流程，但其中间推理几乎完全依赖文本。然而，人类分析师并非只用文本思考，而是在数值摘要、表格与图表之间不断切换，借助视觉证据揭示文本摘要容易遗漏的趋势、分布与异常。图表在人类分析循环中充当认识论行动，而非事后报告产物。现有方法只覆盖了这一决策的一部分：图表生成方法优化用户或智能体请求的可视化，图表理解方法假定图表已存在并专注于信息抽取，近期工作也比较了不同输入表示或按需构建视觉证据，但都没有研究数据智能体在中间分析状态下如何选择文本证据与图表证据。本文的核心问题正是：图表能否作为数据智能体推理循环内部的认识论行动，以及如何教会智能体在恰当的时机调用图表。为此，作者构建了包含200个受控任务、四种匹配接口条件的探针套件，发现智能体虽能读懂自生成图表，却不会稳定地使用它们，且图表与文本在不同任务切片上互为补充证据。基于此，本文提出经验驱动方法，将表示选择转化为智能体可学习的行为，在不改动模型参数的前提下，让智能体学会何时调用文本、图表或二者结合。

### Q2: 有哪些相关研究？

本文的相关研究主要涉及三类。方法类上，ReAct 式数据智能体通过文本轨迹完成结构化数据分析，但中间推理几乎全为文本；已有工作多关注工具调用与代码执行，鲜有把图表作为推理循环内部认知动作。本文区别在于将图表视为“认知动作”，并提出从条件化轨迹中蒸馏操作选择与表示选择两类经验的方法。评测类上，InsightBench 等基准提供企业表格、开放问题与可执行分析，用于端到端分析评测；本文在其基础上构建 200 个受控任务的探针套件，设置无工具、纯文本、纯图表、自由式四种匹配接口，隔离中间表示的影响。应用与实证类上，已有研究表明多模态模型能读取图表，但本文发现“能读不等于会用”：图表单独即可支撑端到端分析，表示选择却依赖模型而非能力，且图表在时序、模式与异常推理上占优、文本在精确读取与条件验证上占优。这些工作为本文的“能力—使用差距”与互补性发现提供了对照，而本文进一步用经验蒸馏与验证门控来弥合该差距。

### Q3: 论文如何解决这个问题？

论文提出的核心方法是让“图表”成为数据智能体推理循环中的内部认知动作，而非仅作为最终展示产物。整体框架分为经验存储、经验蒸馏和推理时调用三部分。

首先，方法将经验外置为可编辑的文档存储，采用两层结构：存储层是文件系统树，入口文档索引独立经验文档，每篇文档含名称、描述、类别等元数据与正文；工具层提供Read、Create、Edit、Bash供构建器管理，数据智能体则通过只读接口kb_read按需检索，先取元数据再读相关内容，以控制上下文开销。经验分为两族：分析经验记录如何选择、组织与验证分析操作；表示经验记录何时用文本、图表或二者混合，以及如何消费所得证据。两族共享存储与工具接口，并作为整体更新与验证。

其次，为打破多数骨干模型“文本偏好”的惯性，方法对每个任务在固定智能体、工具与交互预算下生成条件化轨迹束：一条无约束、一条文本偏好、三条图表偏好轨迹，且图表偏好轨迹之间强制排除重复图表类型，以多样化视觉分析。每条轨迹由轨迹评判器给出结果分数和步骤级归因标签（Helpful/Ineffective/Harmful），区分分析操作与表示选择的贡献。构建器据此进行洞察归纳与包修订，将可迁移模式合并进现有文档或新建条目。

关键创新是验证门控更新：只有使验证集性能提升的提案才被接受，保证性能单调不降并过滤只适配单批次的模式。最终冻结的经验包作为只读外部记忆挂载到ReAct循环中，无需额外训练、检索模型或改动核心循环，即可在分析状态需要视觉模式识别时触发图表使用。

### Q4: 论文做了哪些实验？

论文在三个留出基准上评估方法，覆盖分析报告生成、长程探索和精确答案分析三类任务，均采用官方评测协议。DAComp-DA评估完整性、准确性、洞察力、可读性、分析深度、可视化和总体分数；DDR-Bench（10-K）评估消息级、轨迹级和总体准确率；DSBench数据分析子集评估任务级、竞赛级和总体准确率。对比方法包括OpenHands、DA-Agent、ReAct、Code Interpreter、AutoGen，以及共享相同模型版本、解码配置、工具接口和交互预算的匹配基线，骨干模型为Claude Sonnet 5、GPT-5.6 Luna、GPT-5.6 Sol和DeepSeek V4.1 Flash。主要结果：DAComp-DA总体分数提升1.71–5.46分，平均3.07分，可视化平均提升7.48分，GPT-5.6 Luna提升达19.95分；DDR-Bench总体提升1.17–5.47分，平均2.99分，消息级和轨迹级分别平均提升2.39和3.60分；DSBench总体提升0.10–2.02分，平均1.00分。消融显示迭代蒸馏优于单步蒸馏（总体59.78对56.94），去掉条件化轨迹或验证门分别降至57.11和56.73；两类经验互补，分析经验提升准确性3.70分，表示经验提升可视化13.09分。验证门在30次候选更新中接受8次，将验证分数从72.50单调提升至85.42。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索点主要有三方面。其一，经验以外部文档形式冻结，依赖只读检索接口，agent 在分析中是否真正“查阅”经验缺乏强制约束，可探索将经验检索与表示决策更紧耦合，例如让表示选择本身触发经验查询。其二，条件化 rollout 仅覆盖文本与三类图表偏好，图表类型排除策略较粗，未来可引入更细粒度的视觉编码维度（如聚合粒度、坐标变换）并研究其与任务切片的匹配规律。其三，验证门仅以整体验证性能单调提升为准，可能过滤掉局部有益但短期波动的经验，可探索多目标或分层验证机制。此外，当前经验蒸馏依赖轨迹判官的打分与步骤归因，其可靠性未被系统评估；可研究归因噪声对经验质量的影响，并引入反事实 rollout 来区分表示选择与分析操作的因果贡献。最后，论文未涉及多轮交互中经验随任务演化的在线更新，未来可探索带遗忘与冲突消解的持续经验维护机制。

### Q6: 总结一下论文的主要内容

论文针对数据智能体在分析循环中几乎只用文本推理、而人类分析师会在数字、表格与图表之间切换的问题，提出“图表能否作为智能体推理过程中的内部认知动作”这一核心问题。作者首先构建包含200个受控任务的探针套件，在四种匹配接口下评测多个骨干模型，发现三个现象：仅用图表即可支撑端到端分析；拥有绘图工具并不等于会一致使用图表，存在能力—使用差距；图表与文本在不同任务切片上互补，图表擅长时序、模式与异常推理，文本擅长精确读取与条件验证。基于此，作者提出一种经验驱动方法：在多种表示条件下生成轨迹，用结果评分与步骤归因标注轨迹，由构建智能体蒸馏出“分析经验”和“表示经验”两类文档，并通过验证门控只接纳能提升留出性能的更新，最终以只读外部记忆形式供数据智能体在推理循环中调用，且不改变模型参数。在三个留出基准和四个骨干模型上，该方法一致提升分析准确率与视觉证据质量，并使原本不绘图的骨干开始使用图表，消融实验验证了条件化轨迹、验证门控和两类经验的贡献。
