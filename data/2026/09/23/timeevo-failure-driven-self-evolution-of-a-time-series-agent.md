---
title: "TimeEvo: Failure-Driven Self-Evolution of a Time Series Agent"
authors:
  - "Jie Yang"
  - "Yan Zheng"
  - "Jiarui Sun"
  - "Xiran Fan"
  - "Junpeng Wang"
  - "Liang Wang"
  - "Zelin Xu"
  - "Qinghua Liu"
  - "Zhengyu Fang"
  - "Yiwei Cai"
  - "Philip S. Yu"
date: "2026-09-23"
arxiv_id: "2609.27277"
arxiv_url: "https://arxiv.org/abs/2609.27277"
pdf_url: "https://arxiv.org/pdf/2609.27277v1"
github_url: "https://github.com/Muyiiiii/TimeEvo"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "自进化Skill"
  - "工具调用"
  - "失败驱动学习"
  - "时序问答"
  - "工具对齐"
  - "能力缺口聚类"
  - "证据路由"
  - "可解释诊断链"
  - "LLM Agent"
relevance_score: 9.5
---

# TimeEvo: Failure-Driven Self-Evolution of a Time Series Agent

## 原始摘要

Time series agents answer analytical questions by calling external tools, and which tools they carry is decided by people before the agent runs. However, we identify two failures in this setup. Human-Agent Tool Misalignment: a library of 21 expert-curated tools helps on some tasks and hurts on others, dropping anomaly accuracy under every backbone we test. Silent Harm: one round of generic self-revision changes 147 answers and breaks 56 of them, while the final score moves by less than a point. Both follow from the same gap: whether a tool helps is decided question by question at runtime, while tools are supplied in advance and judged by a single average. To address this, we propose TimeEvo, which clusters an agent's diagnosed failures into capability gaps, plans a measurement for each, synthesizes evidence-only tools that fill them, and admits the candidate library only through a paired admission gate. Experiments on ten time series QA tasks and three backbones show that TimeEvo, starting from an empty library, improves accuracy on every task and every backbone, and that a library grown on a cheap model still gains when it is installed into stronger ones. Code is available at https://github.com/Muyiiiii/TimeEvo.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是基于大语言模型的时间序列智能体（TSAgent）在调用外部工具回答分析性问题时的可靠性问题。研究背景是：现有智能体通常由人类在部署前预先配置好一组专家工具库，智能体运行时只能在这些固定工具中选择调用。然而，作者通过实验发现这种“预先供给、事后平均评估”的模式存在两个结构性缺陷。其一是“人—智能体工具错配”：由专家精心挑选的21个工具在某些任务上带来提升，却在另一些任务上造成明显下降，例如在三个不同骨干模型下，异常检测任务反而下降5.8至8.8个百分点，说明工具是否有用实际上取决于具体问题，而非任务层面的平均判断。其二是“静默伤害”：一轮通用的自我修正会改动147个答案，修复49个却破坏56个原本正确的答案，但由于最终平均分几乎不变，这种伤害被掩盖而无法察觉。这两个现象共同指向一个核心问题：时间序列智能体能否从自身诊断出的失败中自主发现并合成真正需要的工具，同时通过严格的配对准入机制，确保每一次自我更新可测量地有益，且不会静默损害已经答对的问题。

### Q2: 有哪些相关研究？

时间序列分析长期以预测、分类、异常检测等专用模型为主，Chronos、TimesFM、Moirai 等预训练基础模型进一步提升了跨域迁移能力。随着 LLM 的发展，ChatTS、TimeLLM 等多模态语言模型将时间序列作为额外输入模态，实现端到端问答，但面对新任务仍需收集数据并训练或微调。与之相对，TS-Reasoner、TS-Agent、TimeCopilot 等智能体系统提供了免训练方案，将分析能力外移到外部工具，由智能体规划并综合输出。然而免训练不等于免投入，人力从模型训练转移到提示、工作流和工具设计上。为降低这种依赖，本文提出 TimeEvo，将诊断出的失败作为演化能力库的监督信号。在通用 LLM 智能体领域，自演化已有广泛探索：Reflexion、EvolveR 从历史轨迹中提炼经验或原则；Voyager 维护不断增长的技能库，SkillOpt、CoEvoSkills 则在部署前用留出分数或逐任务检查验证技能。时间序列领域的 TimeClaw 在固定工具库上蒸馏使用经验。但这些框架最多通过最终分数或逐任务检查来接纳更新，部分甚至完全跳过验证，从未考虑更新破坏了多少原本正确的答案。单一最终分数会掩盖破坏与修复的相互抵消，导致 Silent Harm。TimeEvo 因此从诊断失败出发演化工具库，并通过两层配对验证门控，权衡修复与破坏后再接纳每次更新。

### Q3: 论文如何解决这个问题？

TimeEvo 的核心思路是把“工具是否有用”从预先人工决定，转变为由智能体自身失败驱动的运行时进化。整体框架以轮次迭代方式运行：每轮先让当前库在训练集上重放，收集答错的题目，并将错误聚类为若干互不重叠的失败桶。聚类分两步——先从小样本定义少量失败类别，再把每个错误归入唯一类别；工具触发过的错误与无工具触及的错误分开聚类，以区分“工具缺陷”与“覆盖缺口”，且定义阶段不看任务元数据，保证按缺失能力而非题型分组。

每个失败桶由局部规划器诊断，产出测量契约：根因、所需测量、输入、成功判据、适用范围与反范围，并声明一种库动作（create/refine/rescope/retire）。全局规划器随后合并重复测量、收窄重叠范围。契约被合成为“仅证据”工具：只输出数值证据，不输出结论或选项，输入缺失时弃权而非编造；工具可调用 Chronos-2 作为预测原语，也可在训练行上拟合浅决策树并编译进源码，阈值由数据测得而非智能体臆造。

验证分两级：先做单工具预筛，要求至少带来一次可归因修复；再对整轮候选库做配对准入检验，用 helped/harmed 计数构造下界统计量 δ_lb，仅当 h>0 且 δ_lb>0 才严格通过，单轮场景辅以净修复与危害率规则。被拒时按每项更新的 h_u、m_u 剪除明显有害工具并重测一次。推理时冻结智能体先作答，仅范围内问题由工具复核，默认保留原答案，从而避免范围外退化。创新点在于失败驱动的能力缺口聚类、证据-only 工具合成、以及整库配对准入门控。

### Q4: 论文做了哪些实验？

论文在10个时间序列问答任务（T1–T4、TSExam、Match、Merrill、Anomaly、Cls、TSAQA-DT）和3个骨干模型（GPT-5.6-luna、GPT-5.6-terra、GPT-5.4-mini）上进行了主实验，对比方法包括无工具基线、Chronos-2固定工具、TimeART的21个专家工具、Self-Refine、vote@5和few-shot ICL（k=4）。TimeEvo从空工具库出发，在每个任务和每个骨干上均取得提升：luna上平均准确率从56.0%升至64.8%（+8.79pp），terra从56.6%升至63.9%（+7.21pp），mini从54.6%升至63.3%（+8.73pp），且Anomaly、Cls、TSAQA-DT等任务提升显著（如luna的Anomaly +14.69pp、Cls +12.08pp）。此外，论文还验证了跨模型迁移：将luna进化出的工具库安装到Claude-opus-5、Claude-sonnet-5和GPT-5.6-sol上，平均准确率分别提升10.50pp、10.65pp和约8pp以上，说明廉价模型进化的库对更强模型仍有效。

### Q5: 有什么可以进一步探索的点？

论文的局限主要在于其失败驱动机制高度依赖诊断质量：若失败聚类不准确，能力缺口识别就会偏差，进而合成无效工具；同时“证据-only”工具虽降低幻觉，却可能限制复杂推理任务的表现。此外，实验集中在十个时间序列 QA 任务，跨领域泛化性仍待验证。未来可探索：一是将配对准入门扩展到多轮动态淘汰机制，使工具库能随任务分布漂移而持续更新；二是引入工具组合与编排的自动搜索，而非仅合成单点工具；三是让失败诊断本身可学习，用强化学习或元学习优化聚类粒度；四是研究工具库在异构骨干间的迁移规律，解释为何廉价模型生长的库能增益强模型，从而指导低成本持续进化。

### Q6: 总结一下论文的主要内容

论文关注LLM时间序列智能体的工具配置与自我修正问题。作者首先揭示两种失败现象：一是人机工具错配，即专家预先配置的21个工具在某些任务上反而降低性能，异常检测准确率在各骨干模型下均下降5.8至8.8分；二是静默伤害，即一轮通用自我修正改动了147个答案，修复49个却破坏56个，而最终平均分几乎不变，掩盖了实际损害。针对此，论文提出TimeEvo：将智能体诊断出的失败聚类为能力缺口，为每个缺口规划度量契约，合成仅基于证据的工具，并通过配对准入闸门决定候选工具库是否被接纳，失败则剪枝重测。在十个时间序列QA任务和三个骨干模型上，TimeEvo从空工具库出发，在所有任务和骨干上均提升准确率，且廉价模型上成长出的工具库迁移到更强模型仍有效。其意义在于让智能体从自身失败中自演化工具，并以可验证方式防止静默伤害。
