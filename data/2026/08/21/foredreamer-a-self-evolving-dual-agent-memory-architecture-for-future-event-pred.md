---
title: "ForeDreamer: A Self-Evolving Dual-Agent Memory Architecture for Future Event Prediction"
authors:
  - "Linhao Zhong"
  - "Zongze Du"
  - "Linyu Wu"
  - "Yu Bo"
  - "Hourong Li"
  - "Chenchen Jing"
  - "Hao Chen"
  - "Yuling Xi"
  - "Chunhua Shen"
date: "2026-08-21"
arxiv_id: "2608.20920"
arxiv_url: "https://arxiv.org/abs/2608.20920"
pdf_url: "https://arxiv.org/pdf/2608.20920v1"
categories:
  - "cs.CL"
tags:
  - "Agentic Time Series"
  - "未来事件预测"
  - "双智能体架构"
  - "记忆管理"
  - "自进化"
  - "证据蒸馏"
  - "开放网络预测"
relevance_score: 7.5
---

# ForeDreamer: A Self-Evolving Dual-Agent Memory Architecture for Future Event Prediction

## 原始摘要

Open-web future event prediction requires agents to distill reliable signals from noisy, redundant, and incomplete evidence. Existing retrieval/memory mechanisms directly feed retrieved information to agents or rely on simple memory functions such as storing and reusing prior information for prediction, leaving them insufficient for open-web forecasting. We propose to transform raw web evidence into structured memory before prediction, enabling agents to reason over distilled, question-specific evidence rather than noisy retrieval results. This paper presents ForeDreamer, a self-evolving dual-agent framework for managing memory over open-web evidence. ForeDreamer separates factual memory, a question-specific evidence state for the current forecast, from experiential memory, persistent agent experience accumulated across forecasting episodes. It uses a main agent for search and prediction, and a memory-processing subagent to convert search results into factual memory with dedicated tools. ForeDreamer further evolves experiential memory through two tracks, improving both forecasting decisions and factual-memory construction. Experiments on Prophet Arena and FutureX demonstrate the effectiveness of ForeDreamer. Project page: https://zhongzero.github.io/ForeDreamer

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

开放网络未来事件预测要求智能体从嘈杂、冗余且不完整的网络证据中提炼可靠信号。现有方法存在明显不足：检索增强生成通常仅对检索结果进行轻量筛选或聚合，简单长上下文策略则直接输入原始信息，当相关信号稀疏、时效性强且混杂冲突报道时，这些方法都不可靠；而长期记忆系统多面向对话个性化或静态知识复用，侧重存储、检索和重用先前信息，难以处理开放网络证据的异构性与冲突性。本文核心问题是：如何让智能体从嘈杂开放网络证据中做出可靠未来事件预测，并利用预测反馈持续进化经验记忆，以同时改进事实记忆构建和预测决策。为此，论文提出ForeDreamer框架，将事实记忆（当前问题特定的证据状态）与经验记忆（跨预测任务积累的持久经验）分离，采用双智能体架构——主智能体负责搜索与预测，记忆处理子智能体通过专用工具将搜索结果转化为结构化事实记忆，并通过双轨进化机制更新文本预测经验与程序化证据处理经验，从而解决现有记忆机制与开放预测任务不匹配的问题。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及三类工作。**方法类**上，早期记忆增强系统依赖检索增强生成（RAG）和稠密/非参数记忆，而近期如HippoRAG、Mem0、MemoryOS、A-MEM、LightMem等探索了图结构关联检索、持久化用户画像、层次化记忆管理和动态记忆图，LangMem则整合语义、情景和程序性记忆。本文与这些工作的区别在于，ForeDreamer并非简单存储或检索原始信息，而是通过双智能体架构将网络证据转化为结构化的“事实记忆”，并引入跨预测任务累积的“经验记忆”进行自我演化，实现记忆的主动蒸馏与动态更新。**自演化智能体类**工作关注部署后的反思、经验复用和技能发现，如失败轨迹反思、工具使用学习等，本文的独特之处在于演化不仅针对预测决策，还同时优化事实记忆的构建过程，形成双轨演化。**评测与应用类**上，MIRAI、ForecastBench等基准评估智能体预测能力，Prophet Arena和FutureX侧重实时市场预测与动态未来事件推理，本文在这两个基准上验证了所提架构在处理噪声、冗余和不完整证据时的有效性，相比直接使用检索结果的基线方法，显著提升了预测准确性与鲁棒性。

### Q3: 论文如何解决这个问题？

ForeDreamer提出了一种自进化的双智能体记忆架构，核心思路是将原始网页证据转化为结构化记忆后再进行预测，避免智能体直接处理噪声检索结果。整体框架包含两个智能体：主智能体负责搜索规划、证据整合和最终预测，记忆处理子智能体则负责将搜索结果转化为问题特定的事实记忆。

在架构设计上，系统将记忆分为两类：事实记忆是当前预测问题的局部证据接口，经验记忆则是跨预测任务积累的持久指导。主智能体在预测时查询经验库，通过搜索-处理工具获取时间有效的证据，子智能体则依据MemGuide工作流和MemTools可执行工具，将原始搜索结果转化为结构化的事实记忆，使证据处理过程显式化、可检查。

关键技术在于双轨自进化机制。文本轨道通过验证后的增删改操作更新经验库，改进搜索规划、证据整合和校准策略。程序轨道则进化MemGuide树和MemTools：采用组合式工具复用避免重复生成功能重叠的工具，通过多样性引导探索防止进化过度集中于局部成功的指南家族。系统在进化验证池上评估候选方案，只有验证性能提升才被采纳。

创新点包括：将证据处理与预测解耦、引入可进化的程序化记忆、组合式工具复用和多样性引导探索机制，显著提升了开放网页未来事件预测的准确性和鲁棒性。

### Q4: 论文做了哪些实验？

论文在Prophet Arena和FutureX两个基准上评估了ForeDreamer，使用Qwen3.5-Flash和GPT-5.4-Nano作为骨干模型，采用时间受限的网页搜索收集证据。Prophet Arena用Brier分数评估（越低越好），FutureX用准确率评估（越高越好）。对比方法包括Full Text、RAG以及HippoRAG 2、Mem0、MemoryOS、A-MEM、LightMem、LangMem等记忆系统。

主要结果：在Prophet Arena上，ForeDreamer在两种骨干模型下均取得最佳平均Brier分数（Qwen3.5-Flash为0.1471，GPT-5.4-Nano为0.1839），显著优于Full Text（0.2059/0.2084）和所有基线。在FutureX上，ForeDreamer准确率最高（0.4108/0.3883），优于Full Text（0.3298/0.2766）。

消融实验验证了双轨经验演化的贡献：移除任一演化轨道均导致性能下降；程序性演化优化（组合工具复用和多样性引导探索）均有效。鲁棒性测试表明在不同搜索设置下ForeDreamer持续优于基线。无信息提示检查排除了数据泄漏可能。工具相似性分析显示组合工具复用减少了工具冗余，多样性引导探索使MemGuide覆盖更多流水线原型。

### Q5: 有什么可以进一步探索的点？

ForeDreamer在开放网络未来事件预测中展现了潜力，但其局限性也指明了几个可探索的方向。首先，当前框架依赖小规模反馈池进行记忆演化，存在验证集过拟合风险。未来可引入在线学习或主动学习机制，从用户反馈或事后结果中持续获取标注，扩大反馈池规模，并设计更严格的交叉验证策略来评估演化记忆的泛化性。其次，框架未在传统agent记忆基准上测试，未来可探索如何将事实记忆与经验记忆的分离机制适配到标准记忆任务中，例如在对话或决策场景中验证其通用性。此外，当前记忆演化依赖手工设计的MemGuides和MemTools，可考虑引入元学习或神经架构搜索来自动生成和优化这些工具，减少人工干预。最后，双智能体协作的通信效率与延迟问题值得优化，例如通过分层记忆压缩或异步更新机制降低交互成本，同时保持证据处理的准确性。这些方向有望提升框架的鲁棒性、通用性和实际部署价值。

### Q6: 总结一下论文的主要内容

ForeDreamer提出了一种面向开放网络未来事件预测的自进化双智能体记忆框架。现有检索与记忆机制直接将噪声、冗余的网络证据输入智能体，或仅依赖简单的信息存储复用，难以应对开放场景下的预测任务。该框架将事实记忆与经验记忆分离：事实记忆是针对当前问题的结构化证据状态，由记忆处理子智能体通过MemGuide工作流和MemTools工具将搜索结果转化为可推理的证据接口；经验记忆则跨预测周期积累，通过双轨进化机制同时优化预测决策与证据处理流程。针对初始进化中的工具冗余和探索过度集中问题，论文引入组合式工具复用与多样性引导的探索调度。在Prophet Arena和FutureX基准上的实验验证了该方法的有效性，表明开放网络预测应将记忆视为持续演化的证据处理经验，而非静态信息存储。
