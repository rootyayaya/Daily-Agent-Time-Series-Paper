---
title: "BALMS: Benchmarking Agentic LLMs for Longitudinal Mental Health Sensing"
authors:
  - "Yu Yvonne Wu"
  - "Arvind Pillai"
  - "Yuliang Chen"
  - "Yuwei Zhang"
  - "Sudarshan Regmi"
  - "Tess Z. Griffin"
  - "Michael V. Heinz"
  - "Lisa A. Marsch"
  - "Nicholas C. Jacobson"
  - "Andrew Campbell"
date: "2026-08-27"
arxiv_id: "2608.27219"
arxiv_url: "https://arxiv.org/abs/2608.27219"
pdf_url: "https://arxiv.org/pdf/2608.27219v1"
categories:
  - "cs.CL"
tags:
  - "Agentic Time Series"
  - "LLM Agent"
  - "时间序列报告"
  - "可解释诊断"
  - "自然语言生成"
  - "时序推理"
  - "传感器数据"
  - "LLM-as-Judge"
  - "证据路由"
  - "长期时序建模"
  - "健康监测"
relevance_score: 7.5
---

# BALMS: Benchmarking Agentic LLMs for Longitudinal Mental Health Sensing

## 原始摘要

Mental health assessment relies on episodic self-report scales, which convert subjective states such as stress into numerical scores but provide only sparse snapshots of wellbeing. Wearable devices offer longitudinal behavioral and physiological signals for continuous, low-burden monitoring. Recent LLM-driven personal-health agents enable natural language queries over wearable signals, but mainly handle short-term, retrieval-based lookups (e.g., highest step count over a week). They do not evaluate whether agents can reason over long-term signals to predict wellbeing scores paired with evidence-grounded rationales. To address this gap, we introduce BALMS, the first systematic benchmark of LLM-based agentic systems for longitudinal mental health sensing. BALMS spans 3 real-world longitudinal datasets, 2 task families (closed-form wellbeing-score prediction and rationale generation auto-graded by an LLM-as-Judge), 3 agentic paradigms evaluated across 5 open- and closed-source LLM backbones. We find that zero-shot agents rarely outperform a simple mean baseline, except with stronger backbones or compact, semantically meaningful features. Chain-of-thought prompting improves reasoning-oriented backbones, but does not guarantee temporal grounding or numerical correctness. Together with more analysis on efficiency and temporal scaling, BALMS highlights the need for longitudinal mental health agents that selectively retrieve history, ground temporal evidence, and reason over interpretable behavioral features.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

心理健康评估长期依赖 episodic 临床访谈和自我报告量表，这类方法将压力等主观状态转化为数值评分，但只能提供稀疏的“快照”，难以捕捉数周至数月内的动态变化。可穿戴设备虽能持续采集多通道行为与生理信号，为连续、低负担监测提供了可能，但现有基于大语言模型（LLM）的个人健康智能体主要处理短期、检索式查询（如一周内最高步数），缺乏对长期信号进行推理以预测心理健康评分并给出证据支撑 rationale 的能力。

现有方法的不足体现在三方面：一是多通道传感历史转化为文本后极易超出 LLM 上下文窗口；二是 LLM 直接对长数值序列进行数值推理不可靠；三是不同数据集在传感器类型、特征格式和观测时长上差异大，导致精心设计的智能体难以跨数据集迁移。因此，目前尚不清楚哪种智能体范式最适合长期心理健康感知。

本文核心问题是系统性地评估 LLM 智能体在纵向心理健康感知上的表现，为此提出 BALMS——首个针对该任务的系统化基准，涵盖三个真实世界数据集、两类任务（封闭式健康评分预测与 LLM-as-Judge 自动评分的 rationale 生成）及三种智能体范式，旨在揭示现有智能体在长期时序推理、证据 grounding 和数值准确性上的关键瓶颈。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要与三类工作形成对比。**方法类**：现有工作如MedAgentBench评估医疗智能体在电子健康记录环境中的交互能力，Mobile-agent基准测试智能体控制手机应用的能力，这些方法侧重工具使用与规划，但未涉及长期可穿戴信号的时间推理。**应用类**：已有LLM驱动的个人健康智能体支持自然语言查询，但仅处理短期检索任务（如查询一周最高步数），缺乏对多周至多年纵向数据的预测与解释能力。**评测类**：现有基准多关注单轮问答或短期行为，未系统评估智能体在纵向心理健康感知中的表现，包括数值预测的准确性、时间证据的锚定以及解释的合理性。本文提出的BALMS填补了这一空白，首次构建覆盖3个真实纵向数据集、2类任务（封闭式幸福感评分预测与LLM-as-Judge自动评分的理由生成）和5种开源/闭源LLM骨干的基准。与现有工作相比，BALMS强调智能体需具备选择性检索历史、锚定时间证据并基于可解释行为特征推理的能力，而不仅仅是简单的检索或交互。

### Q3: 论文如何解决这个问题？

BALMS通过构建一个系统化的基准测试框架来解决LLM智能体在纵向心理健康感知中的评估缺失问题。其核心方法围绕两个任务家族和三种智能体范式展开，在三个真实世界纵向数据集上对五个开源/闭源LLM骨干进行评测。

整体框架包含两大任务：T1是封闭式心理健康分数预测，要求智能体基于目标日前瞻窗口的多模态传感信号（如步数、心率、卡路里）输出整数自评分数；T2是开放式传感推理，要求智能体生成自由形式的思维链理由，引用具体传感器通道和数值，并推理多日趋势、周周期或恢复模式，由LLM-as-Judge按规则自动评分。

三种智能体范式构成主要模块：基于提示的范式（如Health-LLM）将传感器数据格式化为每日数值数组，结合人口统计特征和任务指令组装成单一提示；基于工具的方法（如PHIA）通过ReAct循环驱动LLM调用Python代码执行日期过滤、分组聚合等操作，将执行结果回填到上下文中；基于记忆的方法则采用两种RAG变体——分块RAG按天粒度编码历史数据并通过余弦相似度检索top-k相似日，树状RAG（改编自RAPTOR）构建两层记忆树，叶节点捕获日内子时段变化，内部节点为LLM生成的每日抽象摘要，检索时混合细粒度证据与每日摘要。

创新点在于：首次系统评估LLM智能体在纵向心理健康感知中的表现，发现零样本智能体难以超越简单均值基线，思维链提示虽改善推理骨干但无法保证时间接地和数值正确性，从而揭示了对选择性历史检索、时间证据接地和可解释行为特征推理的迫切需求。

### Q4: 论文做了哪些实验？

论文构建了BALMS基准，系统评估了基于LLM的智能体在纵向心理健康感知中的表现。实验设置包含3个真实数据集（DiversityOne情绪、PMData压力、GLOBEM焦虑），2类任务（闭式健康评分预测和开放理由生成），以及3种智能体范式（Health-LLM、RAG、Raptor、PHIA），覆盖5种LLM骨干（Qwen2.5-7B/14B、Mistral-7B、DeepSeek-R1-Distill-Qwen-14B、Claude-Haiku-4.5）。

主要结果：零样本智能体在多数情况下难以超越简单均值基线（如DiversityOne均值MAE 0.58），仅Claude-Haiku-4.5配合Health-LLM达到0.42，PHIA在PMData上达0.54。CoT提示主要提升推理型骨干（DeepSeek、Claude），最高改善41.4%，但对指导型模型效果有限。LLM-as-Judge评估显示，仅Claude-Haiku-4.5能同时满足时间推理和证据 grounding，开源模型虽生成流畅理由但缺乏时间对齐（C1）和结构识别（C5）能力。窗口长度实验表明RAG随历史增长获益最大（PMData MAE降29%），Health-LLM反而退化。传感器敏感性分析显示，仅用Fitbit语义特征常优于全模态设置，且PHIA延迟显著高于其他范式。

### Q5: 有什么可以进一步探索的点？

BALMS的局限为后续研究提供了清晰方向。首先，当前仅评估了单智能体的提示、工具和记忆范式，未来可探索多智能体协作、规划器-执行器架构，以及动态组合工具、记忆与反思的混合系统，以提升复杂时序推理能力。其次，回顾性预测无法验证真实干预效果，需推进前瞻性部署研究，在交互式场景中评估智能体对用户状态的实际影响，并纳入临床专家与用户主观评估以补充LLM-as-Judge的客观性。此外，可改进时间感知机制，如设计显式的时序记忆检索策略或事件抽取模块，增强对长期依赖的数值校准与证据锚定。最后，安全性与个性化值得深入，包括不确定性校准、隐私保护下的个性化特征选择，以及针对不同人群（如青少年、老年）的适应性调整，从而推动智能体从基准测试走向可靠的实际心理健康支持工具。

### Q6: 总结一下论文的主要内容

BALMS首次系统评估了基于LLM的智能体在纵向心理健康感知中的表现，填补了现有研究仅关注短期检索查询的空白。论文定义了从可穿戴设备长期行为与生理信号中预测幸福感评分并生成证据支撑解释的任务，涵盖3个真实纵向数据集、2类任务（封闭式评分预测与LLM评判的推理生成）及5种开源/闭源LLM骨干下的3种智能体范式。核心发现是：零样本智能体通常难以超越简单均值基线，仅在更强骨干或紧凑语义特征下才具竞争力；思维链提示能提升推理型模型，但无法保证时间锚定与数值准确性。研究强调，纵向心理健康智能体需具备选择性历史检索、时间证据锚定及可解释行为特征推理能力，为设计高效、可扩展的长期健康监测系统提供了重要基准与方向指引。
