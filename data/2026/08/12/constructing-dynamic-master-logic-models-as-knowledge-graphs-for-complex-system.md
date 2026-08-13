---
title: "Constructing Dynamic Master Logic Models as Knowledge Graphs for Complex System Diagnostics Using Retrieval-Augmented Large Language Models"
authors:
  - "Saman Marandi"
  - "Yu-Shu Hu"
  - "Mohammad Modarres"
date: "2026-08-12"
arxiv_id: "2608.12304"
arxiv_url: "https://arxiv.org/abs/2608.12304"
pdf_url: "https://arxiv.org/pdf/2608.12304v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Knowledge Graph"
  - "Retrieval-Augmented Generation"
  - "Functional Modeling"
  - "Fault Diagnosis"
  - "LLM Agent"
  - "Diagnostic Reasoning"
  - "Reliability Analysis"
relevance_score: 9.5
---

# Constructing Dynamic Master Logic Models as Knowledge Graphs for Complex System Diagnostics Using Retrieval-Augmented Large Language Models

## 原始摘要

Dynamic Master Logic (DML) provides a hierarchical framework for representing system behavior by linking functional objectives to underlying structural elements. However, DML construction typically relies on expert interpretation of technical documentation, limiting scalability for complex systems. This study presents a framework for automated construction of DML models from system descriptions and their representation as Knowledge Graphs (KG-DML), using Retrieval-Augmented Generation and Large Language Models as enabling tools. Building on prior work with small-scale systems, the framework extends automated KG-DML construction and evaluation to substantially larger and more complex systems. Model construction proceeds across the DML hierarchy using targeted retrieval while preserving functional dependencies and explicit logical relationships. The resulting KG-DML supports diagnostic reasoning, safety assessment, upward failure propagation, and downward dependency tracing. A multi-level validation methodology evaluates layer-specific precision and recall, logical gate consistency, and overall structural integrity. Application to the Low-Pressure Coolant Injection system of a decommissioned Boiling Water Reactor demonstrates consistent reconstruction across repeated runs. The results show that automated KG-DML construction can transform technical documentation into executable functional models for diagnostic and reliability analysis.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文旨在解决复杂工程系统诊断中动态主逻辑（DML）模型构建的瓶颈问题。传统DML模型依赖专家对技术文档的人工解读，过程耗时且难以扩展至大型复杂系统。同时，现有事件驱动方法（如故障树分析）需要穷举故障事件，无法处理未预见的故障序列。论文提出利用检索增强生成（RAG）和大型语言模型（LLM）自动从系统文档构建DML模型，并将其表示为知识图谱（KG-DML），以支持可扩展的、基于功能依赖的诊断推理。核心挑战包括：从非结构化文本中提取功能元素和依赖关系、保持层级逻辑一致性、以及确保模型结构完整性以支撑可靠的图遍历推理。论文还强调，由于诊断推理通过确定性图遍历和布尔传播进行，KG-DML的结构质量直接影响诊断结论的准确性，因此需要系统的评估框架来量化模型质量。

### Q2: 有哪些相关研究？

相关研究分为三类。第一类是传统诊断方法，如事件树分析（ETA）和故障树分析（FTA），它们基于事件驱动表示，需要预定义故障序列，难以处理复杂系统的未预见故障。第二类是LLM在故障诊断中的应用，包括微调LLM用于HVAC诊断、振动信号故障分类、多任务框架联合诊断与剩余寿命预测，以及基于Agent的传感器数据诊断。这些研究多聚焦于故障识别和分类，而非从文档构建可执行功能模型。第三类是知识图谱与LLM结合，如KG-RAG增强诊断推理、LLM驱动KG构建用于网络安全、以及图结构用于风险传播分析。然而，这些工作通常将KG用于组织领域知识或增强检索，而非构建保留层级功能依赖和逻辑关系的可执行模型。本文的独特之处在于将RAG、LLM、schema约束提取和图数据库整合为自动化DML构建框架，强调功能层级和逻辑门结构，区别于通用KG方法。

### Q3: 论文如何解决这个问题？

论文提出一个三阶段框架。第一阶段是文档预处理与嵌入：标准化术语、扩展缩写、解析代词，将文档分段（1500字符，重叠150）并嵌入向量库。第二阶段是逐层模型构建：沿DML层级（目标→功能→子功能→组件→成功条件）顺序进行，每层使用语义定义和父节点构建检索查询，从向量库检索top-K（K=10）相关段落，提供给LLM（GPT-4o，温度0）生成候选元素和逻辑关系，输出受JSON schema约束。验证后追加到主JSON，作为下一层的父节点来源。第三阶段是知识图谱合成：将主JSON转换为Cypher查询，在Neo4j中创建节点和关系，支持嵌套布尔门（AND/OR）的递归构建。评估框架包括层级别精度/召回/F2分数、链接和门一致性检查，以及综合完整性分数（Integrity Score），该分数结合加权F2均值和指数结构惩罚，惩罚项考虑缺失节点、缺失链接、门不匹配和孤立节点。交互阶段通过LLM Agent调用图遍历工具（向上传播、向下追踪）进行诊断推理，并支持Graph-RAG回答结构性问题。

### Q4: 论文做了哪些实验？

论文以退役沸水反应堆的低压冷却剂注入（LPCI）系统为案例，该系统规模较大且文档密集。实验设置包括：使用GPT-4o（温度0）进行多次运行以评估一致性，参考模型由专家构建。评估指标包括各层（目标、功能、子功能、组件、成功条件）的精度、召回和F2分数，以及链接和门准确性。主要结果：框架能一致地重建KG-DML，重复运行间结构稳定。完整性分数对惩罚缩放参数S的敏感性分析显示，S值在合理范围内变化时分数稳定，表明指标鲁棒性。实验还考察了批大小对模型质量的影响，发现较小的批大小（如1）通常提高精度但可能增加计算成本，而较大批大小可能降低提取质量。诊断推理示例展示了向上传播（从组件故障推断系统级影响）和向下追踪（从目标分解到具体组件）的能力。总体而言，自动构建的模型与专家参考模型高度一致，验证了方法的可行性。

### Q5: 有什么可以进一步探索的点？

局限性包括：依赖GPT-4o单一模型，未测试其他LLM的泛化性；评估基于单一案例（LPCI系统），需在更多复杂系统上验证；文档预处理依赖人工规则，自动化程度有限；完整性分数中的权重和惩罚参数需专家设定，可能影响通用性。未来方向包括：引入自反思机制让LLM验证和修正提取结果，减少幻觉；利用多Agent协作（如一个Agent提取、一个Agent验证）提高一致性；结合时序数据（如传感器流）实现动态DML更新，支持实时诊断；探索将KG-DML与强化学习结合，优化诊断路径选择；以及开发更自动化的评估方法，减少对专家参考模型的依赖。此外，可研究如何将构建的KG-DML用于生成自然语言诊断报告，增强可解释性。

### Q6: 总结一下论文的主要内容

论文提出一个自动化框架，利用检索增强生成和大型语言模型从工程文档构建动态主逻辑（DML）模型，并表示为知识图谱（KG-DML）。该框架通过分层检索和结构化提取，将非结构化文本转换为保留功能层级和逻辑关系的可执行模型，支持故障诊断、安全评估和可靠性分析。主要贡献包括：自动化DML构建方法、扩展到大型复杂系统的能力、以及多级评估框架（层级别指标+完整性分数）。案例研究（LPCI系统）验证了方法的有效性和一致性。论文强调，KG-DML的结构质量直接决定诊断推理的可靠性，因此提出了综合评估方法。该工作为将LLM应用于工程功能建模提供了新范式，有望推动可扩展的、文档驱动的诊断模型构建。
