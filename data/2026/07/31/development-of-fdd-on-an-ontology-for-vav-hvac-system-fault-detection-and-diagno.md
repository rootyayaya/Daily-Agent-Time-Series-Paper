---
title: "Development of FDD-ON: an Ontology for VAV HVAC System Fault Detection and Diagnostics"
authors:
  - "Yimin Chen"
  - "Brian Fricke"
  - "Bo Shen"
  - "Jamie Lian"
  - "Mingkan Zhang"
  - "James Lo"
  - "Yun Zhang"
  - "Shi Ye"
  - "Jiajing Huang"
  - "Han Hu"
  - "Chujie Lu"
  - "Rui Tang"
  - "George Zhuang"
date: "2026-07-31"
arxiv_id: "2607.29657"
arxiv_url: "https://arxiv.org/abs/2607.29657"
pdf_url: "https://arxiv.org/pdf/2607.29657v1"
categories:
  - "cs.AI"
tags:
  - "Ontology"
  - "HVAC FDD"
  - "可解释故障诊断"
  - "语义互操作"
  - "知识图谱"
  - "故障-症状-影响链"
  - "VAV系统"
relevance_score: 7.5
---

# Development of FDD-ON: an Ontology for VAV HVAC System Fault Detection and Diagnostics

## 原始摘要

Fault detection and diagnosis (FDD) technology is essential for improving HVAC system reliability, energy efficiency, and maintenance effectiveness. However, effective deployment of FDD solutions in buildings requires structured domain knowledge that can bridge heterogeneous data sources, diverse equipment types, and varied diagnostic outputs. Limited data interpretability and interoperability within the FDD domain have led to fragmented information silos, hindering the implementation of FDD and related applications, such as the digital twin-enabled FDD frameworks and artificial intelligence (AI)-driven maintenance decision-making systems. This paper presents an FDD Ontology (FDD-ON), a modular and extensible ontology to formally represent variable air volume (VAV) HVAC system components, fault types, symptom statuses, fault impacts and associated attributes. FDD-ON integrates HVAC system FDD semantics to provide comprehensive representations of fault and symptom attributes, supported by the well-defined controlled vocabulary. Additionally, FDD-ON offers comprehensive fault, symptom, and impact libraries to capture a broad spectrum of operational abnormalities and their consequences in VAV HVAC systems. Through explicit contributing cause-fault-symptom-impact relations, FDD-ON serves as a machine-interpretable basis for querying diagnostic knowledge, mapping heterogeneous FDD outputs, and developing interoperable FDD-related applications. FDD-ON is evaluated using publicly available VAV HVAC system datasets and demonstrated through FDD development applications. Results indicate that FDD-ON provides a foundational semantic framework for advancing scalable, transparent, and interoperable FDD solutions across various applications.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文针对VAV HVAC系统故障检测与诊断（FDD）领域存在的三大核心问题：1）故障、症状和影响缺乏统一定义，导致诊断推理和评估混乱；2）故障和症状的属性描述不足，如症状模式（缓慢响应、振荡等）常被忽略；3）FDD工具输出格式异构，缺乏互操作性，阻碍自动化处理和决策支持。这些问题导致FDD领域信息孤岛化，限制了数字孪生和AI驱动的维护决策系统的发展。为此，论文开发了FDD-ON本体，旨在提供结构化、机器可解释的领域知识模型，统一表示故障类型、症状状态、影响及其属性，并通过明确的因果链（贡献原因-故障-症状-影响）支持查询、映射和互操作应用。

### Q2: 有哪些相关研究？

相关工作分为两类：建筑领域本体和HVAC FDD本体。建筑领域包括IFC（缺乏FDD知识）、Brick Schema（提供设备层级但未覆盖故障机制）、Project Haystack（通用标签框架，无故障语义）、以及EFOnt、CTRLont、BOT等专用本体。HVAC FDD本体方面：Chen等人开发了故障分类法，但将症状归为故障类型；Hwang等人扩展Brick为FSBrick，但未捕捉故障机制和症状特征；Blechmann等人开发AHU故障本体但结构不完整；Gourabpasi的AFDDOnto集成BIM和BAS但缺乏故障性质描述；Ploennigs用语义图识别因果关系但未标准化数据格式；Mallak等人构建系统本体但缺乏统一数据格式；Li等人开发领域本体但未详述故障性质和测量类型。本文通过提供开源故障库、症状库和影响库，以及完整的属性分类，弥补了这些不足。

### Q3: 论文如何解决这个问题？

论文采用Gruninger & Fox方法论，构建了五阶段迭代框架。核心是四层语义模型（症状检测→故障诊断→贡献原因识别→影响分析），基于因果链概念。FDD-ON使用RDFS和OWL实现，包含类、属性、个体三大组件：类体系分三层（系统类型、设备类型、组件/测量类型），属性包括对象属性（如hasSymptom、hasContributingCause）、数据属性（如hasDeviationMagnitudeValue）和注解属性。关键创新是20个故障类型和11个症状状态的受控词汇表，以及四元命名法（位置-测量类型-行为-状态）确保语义精确。本体包含469种故障类型、468种症状状态、447种影响类型，覆盖冷水机组、锅炉、AHU、VAV末端和屋顶机组五大子系统。通过显式因果链关系，支持SPARQL查询和推理，实现异构FDD输出的映射和互操作。

### Q4: 论文做了哪些实验？

论文使用公开可用的VAV HVAC系统数据集进行本体评估，并演示了FDD开发应用。评估包括：1）本体结构验证，检查类层次、属性定义和受控词汇的一致性；2）通过SPARQL查询验证因果链的推理能力，如查询特定故障的症状和影响；3）演示将异构FDD输出映射到本体实例，实现语义互操作。结果证明FDD-ON能有效表示故障-症状-影响关系，支持可追溯诊断决策。但论文未提供定量指标（如查询响应时间、映射准确率），主要展示定性评估和案例演示。

### Q5: 有什么可以进一步探索的点？

局限性包括：1）本体目前仅覆盖VAV系统，需扩展至其他HVAC配置（如定风量系统、辐射系统）；2）受控词汇表需持续更新以涵盖新兴故障类型；3）缺乏与LLM/Agent工作流的集成，未来可探索将本体作为RAG的知识源，支持自然语言诊断报告生成；4）本体评估主要依赖定性方法，可引入自动化一致性检查工具（如Pellet、HermiT）进行逻辑验证；5）可开发基于本体的数字孪生FDD框架，实现实时推理和预测性维护；6）研究本体驱动的多Agent协作诊断，利用因果链指导故障隔离和根因分析。

### Q6: 总结一下论文的主要内容

论文提出了FDD-ON，一个模块化、可扩展的VAV HVAC系统故障检测与诊断本体。它通过四层语义模型（症状检测、故障诊断、贡献原因识别、影响分析）和受控词汇表，统一了故障、症状和影响的定义，解决了FDD领域信息孤岛和互操作性问题。本体包含469种故障类型、468种症状状态和447种影响类型，覆盖五大子系统，并提供开源库支持持续演进。通过显式因果链关系，FDD-ON支持SPARQL查询、异构数据映射和可解释推理，为数字孪生FDD、AI维护决策等应用提供语义基础。该工作为可解释时间序列分析在工业故障诊断中的应用提供了知识建模范式。
