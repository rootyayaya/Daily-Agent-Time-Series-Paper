---
title: "TelcoAgent: A Scalable 5G Multi-KPM Forecasting With 3GPP-Grounded Explainability"
authors:
  - "Geon Kim"
  - "Dara Ron"
  - "Sukhdeep Singh"
  - "Suyog Moogi"
  - "Pranshav Gajjar"
  - "V V N K Someswara Rao Koduri"
  - "Een Kee Hong"
  - "Vijay K. Shah"
date: "2026-06-18"
arxiv_id: "2606.19821"
arxiv_url: "https://arxiv.org/abs/2606.19821"
pdf_url: "https://arxiv.org/pdf/2606.19821v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "时间序列预测"
  - "可解释故障诊断"
  - "LLM/Agent工作流"
  - "知识图谱"
  - "基础模型"
  - "零样本预测"
  - "电信网络"
  - "KPM预测"
  - "3GPP"
relevance_score: 8.5
---

# TelcoAgent: A Scalable 5G Multi-KPM Forecasting With 3GPP-Grounded Explainability

## 原始摘要

Key Performance Measurement (KPM) forecasting is essential for proactive network management of 5G and next-generation telecom networks. However, existing machine learning (ML) approaches face significant limitations in scalability and explainability, restricting their effectiveness in real-world deployments. We propose TelcoAgent, a foundation model-based framework that enables accurate, scalable, and explainable forecasting of multiple KPMs across diverse network cells without the need for site-specific training. Specifically, the framework comprises three key components: (i) an automated three-agent pipeline that constructs a 3rd Generation Partnership Project (3GPP) knowledge graph directly from specification documents, (ii) a scalable, time-series foundation model (TSFM)-based prediction pipeline to deliver accurate, zero-shot forecasting, and finally (iii) a reasoning and explanation pipeline that provides actionable, domain-grounded diagnostics. Evaluated using a 3-month, real-world, city-scale 5G KPM dataset from a U.S.-based network operator, TelcoAgent demonstrates high forecasting accuracy for all 7 considered KPMs per cell across 200 cells, while delivering explainable insights and actionable instructions to address network degradations.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

5G及下一代电信网络的主动式管理依赖于关键性能指标（KPM）的准确预测。然而，现有机器学习方法在可扩展性和可解释性方面存在显著局限。传统方法如回归神经网络、时空图神经网络和LSTM等，虽能捕捉部分时序或空间依赖，但难以建模KPM间的非线性交叉依赖关系，且需要为每个小区单独训练模型，导致计算开销巨大，无法实现网络级的大规模部署。更关键的是，这些模型仅输出预测数值，缺乏基于领域知识的根因诊断能力，无法为运营商提供可操作的洞察，从而限制了其在真实网络管理中的有效性。

针对上述问题，本文提出TelcoAgent框架，旨在实现大规模、多KPM的零样本预测，并提供基于3GPP标准的可解释性分析。核心挑战在于：如何在不进行小区特定训练的前提下，同时保证跨小区、跨KPM的预测精度，并利用领域规范（3GPP）自动生成可解释的根因分析与行动建议，以替代传统“黑盒”预测模式。

### Q2: 有哪些相关研究？

在相关研究中，本文首先回顾了5G网络KPM预测工作，指出LSTM和GNN等监督方法依赖大量标注数据、需频繁重训练且忽略跨KPM相关性，而本文的TelcoAgent通过时间序列基础模型（TSFM）实现了零样本预测，克服了这些局限。其次，在时间序列基础模型方面，Chronos-2、Moirai和MOMENT等模型虽具备零样本能力，但缺乏领域特定的因果知识（如3GPP标准）且无法提供结构化解释；TelcoAgent通过构建3GPP知识图谱弥补了这一不足。最后，在LLM智能体与知识推理方面，ReAct、ORAN-Bench-13K和OG-RAG等工作聚焦于文本检索与标准问答，但未能桥接领域知识与时间序列动态；TelcoAgent创新地将TSFM与3GPP知识图谱耦合，实现了知识驱动的预测、因果诊断与可操作建议。整体上，本文属于方法类研究，在可扩展性、可解释性和领域适配性上显著优于现有工作。

### Q3: 论文如何解决这个问题？

论文提出TelcoAgent框架，通过三个核心流水线解决5G多KPM预测的可扩展性和可解释性问题。整体框架包括：(1) **知识图谱构建流水线**，采用三个专用LLM智能体（提取器、对齐器、评估器）自动从3GPP规范文档中提取结构化知识。提取器将规范解析为章节级块并抽取{主体、谓词、客体}三元组；对齐器将这些实体映射到规范3GPP本体并标准化不一致术语；评估器为每条知识分配置信度分数q∈[0,1]，若低于阈值q_TH则触发反馈循环重新对齐，确保结构语义一致性。最终构建的3GPP知识图谱编码了KPM定义、因果链和物理层约束。(2) **预测流水线**，基于时间序列基础模型（TSFM）实现零样本多步预测。通过滑动窗口聚合历史观测形成输入矩阵X∈R^(L×C)（C为KPM通道数），TSFM零样本推理生成预测Ŷ∈R^(H×C)，自然捕捉跨KPM依赖关系，无需领域微调即可适应不同小区。(3) **推理与解释流水线**，采用ReAct范式结合知识图谱提供可操作诊断。首先从预测轨迹提取均值、趋势斜率等关键指标建立定量基线；然后使用模型无关的PAX-TS方法计算跨通道敏感度矩阵S∈R^(C×C)，并通过3GPP知识图谱中的有向因果路径解决方向性问题；最后融合敏感度分数、3GPP因果链和OpenStreetMap空间上下文，多模态推理识别异常根因，生成针对特定RAN参数的可追溯建议，并通过自动自验证模块交叉检查数值准确性，消除LLM幻觉。创新点在于将TSFM零样本预测与3GPP知识图谱驱动的因果推理相结合，实现跨200个小区的7种KPM高精度预测与可解释诊断。

### Q4: 论文做了哪些实验？

论文在真实5G网络数据集上进行了全面实验。数据集来自美国运营商，覆盖200个小区，采集3个月（2025年9月至11月）的7种KPM指标（RRC、CQI、iBLER、rBLER、MAC Th、PRB、IP Th），粒度1小时。实验设置包括：零样本预测使用3个时间序列基础模型（Chronos-2、Moirai-1.1-R-base、MOMENT-1-large），监督基线使用3个模型（N-BEATS、GRU、MLP）在81天历史数据上逐站训练。预测窗口为7天，通过输入长度扫描确定最优配置（Chronos-2和Moirai用81天，MOMENT用22天）。主要结果：Chronos-2在所有7个KPM上均取得最佳nRMSE和MASE（如PRB的nRMSE=0.13, MASE=0.72），Moirai次之，MOMENT在RRC和PRB上表现较差（nRMSE=0.24和0.21），表明跨通道依赖的重要性。解释质量评估使用Faithfulness（0.615）和Answer Relevancy（0.807），消融实验显示去除3GPP知识图谱后Answer Relevancy下降7.4%。数值验证显示99.8%的指标匹配精度。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是知识图谱仅基于3GPP规范构建，未涵盖运营商自定义参数或跨厂商差异，可能导致解释粒度不足；二是当前仅依赖单站点时序特征，忽略了相邻小区间的空间依赖和干扰耦合，限制了故障根因定位的准确性；三是零样本预测虽避免了重训练，但面对极端网络事件或新型异常模式时，基础模型的泛化能力可能下降。未来可探索的方向包括：引入多源异构数据（如告警日志、配置变更）扩展知识图谱，增强因果推理的覆盖范围；设计图神经网络或时空Transformer捕获小区间交互，提升多KPM联合预测的鲁棒性；结合在线学习或提示微调机制，使基础模型能快速适应网络动态变化；同时可参照O-RAN架构，将推理结果转化为闭环控制策略，实现从预测到自动优化的端到端Agent工作流。

### Q6: 总结一下论文的主要内容

TelcoAgent是一个面向5G网络的多KPM（关键性能指标）预测与可解释性框架。现有方法在可扩展性和可解释性方面存在局限，难以大规模部署。该框架包含三个核心组件：一是基于三个自动化Agent从3GPP规范文档构建知识图谱；二是利用时间序列基础模型（TSFM）实现零样本预测；三是提供基于领域知识的可解释诊断。基于美国运营商3个月的城市级5G KPM数据集评估，TelcoAgent在200个小区上对全部7种KPM实现了高精度预测，数值保真度达99.8%，且优于有监督基线。其核心贡献在于将零样本可扩展性与规范驱动的可解释性相结合，无需站点级训练或人工验证，为大规模5G网络智能运维提供了可行方案。
