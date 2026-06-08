---
title: "DAST: A VLM-LLM Framework for Cross-Interface Anomaly Detection in O-RAN"
authors:
  - "Francesco Spinelli"
  - "Esteban Municio"
  - "Pau Baguer"
  - "Gines Garcia-Aviles"
  - "Xavier Costa-Perez"
date: "2026-06-04"
arxiv_id: "2606.06261"
arxiv_url: "https://arxiv.org/abs/2606.06261"
pdf_url: "https://arxiv.org/pdf/2606.06261v1"
categories:
  - "cs.NI"
  - "cs.AI"
  - "cs.ET"
  - "cs.MA"
tags:
  - "Agentic Time Series"
  - "多模态时间序列异常检测"
  - "VLM-LLM 管道"
  - "零样本故障诊断"
  - "O-RAN 安全"
  - "跨接口异常检测"
  - "自然语言报告生成"
  - "多智能体框架"
  - "可解释诊断链"
  - "领域知识注入"
relevance_score: 9.5
---

# DAST: A VLM-LLM Framework for Cross-Interface Anomaly Detection in O-RAN

## 原始摘要

O-RAN enables a disaggregated baseband stack with programmable functions that communicate over standardized open interfaces. The same openness that enables multi-vendor composition also expands the attack surface across logically decoupled tiers that make up the compute continuum. Among these threats, Denial-of-Service and performance-degradation attacks, which account for the majority of catalogued O-RAN threats, are particularly difficult to detect. Traditional Time-Series Anomaly Detection (TSAD) methods fail in this new regime where labelled baselines are scarce, threats evolve faster than detectors can be retrained, and the high-dimensional multivariate telemetry overwhelms monolithic inference models. To address these challenges, we present DAST, a zero-shot multi-agent framework for cross-interface anomaly detection in O-RAN that chains a three-stage VLM $\rightarrow$ LLM $\rightarrow$ VLM pipeline. DAST converts multivariate KPI streams into visual representations, scores textual per-interface descriptions against O-RAN domain knowledge, and verifies suspects on high-resolution heatmaps to output the problematic interfaces, the anomalous time intervals, an indicative O-RAN WG11-aligned operational impact rating and the decision rationale. We evaluate DAST on real network traces collected from an O-RAN testbed under representative performance degradation scenarios, achieving 0.910 F1-Score and 0.843 Accuracy, outperforming state-of-the-art TSAD baselines.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

O-RAN通过开放接口实现多厂商设备互操作，但也引入了新的安全挑战，其中拒绝服务（DoS）和性能退化攻击占已识别威胁的60%，且影响会跨接口级联。现有时间序列异常检测（TSAD）方法存在三大不足：一是依赖大量标注数据，而在多厂商动态部署场景下获取成本极高；二是孤立评估每个接口，无法捕捉O-RAN闭环控制导致的跨接口级联异常；三是单一的大语言模型（LLM）或视觉语言模型（VLM）在处理高维多变量KPI数据时存在维度瓶颈和数值推理能力弱的问题。本文旨在解决O-RAN中跨接口异常检测的零样本泛化难题，核心目标是设计一种无需标注数据或微调、能利用领域知识进行多模态推理的框架，以准确识别异常接口、时间区间、影响等级并给出决策依据。

### Q2: 有哪些相关研究？

### 相关研究

本文的相关工作主要分为三类：

**1. 传统时间序列异常检测（TSAD）方法**  
典型工作如MSCRED（利用卷积编码器与循环解码器检测多变量流异常并定位根因）和SpotLight（在运营商级O-RAN测试平台上实现可解释检测）。本文指出，这些方法在O-RAN场景下面临三大结构性限制：标注数据稀缺、分布漂移导致重训练失效、以及孤立检测接口无法捕捉跨接口级联效应。DAST通过零样本多智能体框架和视觉-语言模型（VLM+LLM）的协同，直接规避了这些限制。

**2. 基于基础模型（LLM/VLM）的异常检测**  
已有研究尝试将LLM预训练用于异常检测（需大量计算资源），或直接向LLM输入数值序列、将时序数据渲染为图像后送入VLM，以及构建多智能体系统。本文创新性地提出三阶段VLM→LLM→VLM流水线：第一阶段将多接口KPI渲染为堆叠折线图；第二阶段利用O-RAN领域知识对文本描述评分；第三阶段通过高分辨率热图验证可疑接口并输出WG11对齐的影响评级。这种设计解决了单一模型处理高维遥测时上下文窗口溢出和性能退化的问题。

**3. O-RAN领域的异常检测**  
现有O-RAN相关工作仅将基础模型用作训练后分类器的后验解释工具，而非直接作为检测器。DAST首次将VLM/LLM作为零样本异常检测核心，直接处理跨接口遥测数据，并输出可解释的决策依据（含问题接口、时间区间、影响评级）。

### Q3: 论文如何解决这个问题？

DAST提出了一种零样本、多智能体的VLM-LLM-VLM三阶段流水线架构，用于解决O-RAN跨接口异常检测问题。其核心设计模仿人类网络专家的推理过程，将任务分解为三个专业化步骤：

1. **第一阶段（VLM视觉感知）**：将来自O-RAN各接口（如E2、A1、F1-c等）的多维KPI时间序列数据转换为可视化图表（如折线图）。首个VLM模型对这些图表进行视觉分析，生成每个接口的文本描述性“画像”，包括趋势、波动和异常模式。

2. **第二阶段（LLM领域推理）**：一个经过O-RAN领域知识（如WG11标准）增强的LLM接收第一阶段输出的文本描述，将其与接口的预期行为进行对比，并给出异常评分。该阶段利用语言模型的语义理解能力，结合领域知识库进行跨接口因果推理（例如，F1-c的延迟异常可能引发F1-u的吞吐量崩溃）。

3. **第三阶段（VLM高分辨率验证）**：针对LLM标记的可疑接口和时间区间，第二个VLM在更高分辨率的热力图上进行精细验证，确认异常的具体位置、持续时间和严重程度。

**关键技术**包括：完全零样本（无需标注数据或微调）、多模态融合（视觉+语言）、以及模块化解耦（避免单一模型处理高维数值的瓶颈）。**创新点**在于首次将VLM-LLM链式架构应用于O-RAN安全领域，输出包含异常接口、时间区间、操作影响评级（符合O-RAN WG11标准）和决策理由的结构化报告，实现了跨接口级联异常的检测与可解释性。

### Q4: 论文做了哪些实验？

论文在自建的O-RAN测试床上进行实验，该测试床使用srsRAN、O-RAN SC和Open5GS等开源软件栈，以及USRP B210和Quectel RM520N-GL设备，模拟真实网络流量。实验通过在F1-u、F1-c、A1和E2接口上注入不同严重程度的性能退化攻击（增加时延和丢包）来生成异常数据。对比方法包括MSCRED、TAMA、VLM4TS和TSAD Agents，其中MSCRED和TAMA需要训练，VLM4TS和TSAD Agents为零样本方法。DAST框架运行在配备Intel Xeon Silver、72GB RAM和双RTX A5000 GPU的服务器上，使用qwen3.6:35b模型。主要结果采用标准指标（要求预测区间与真实异常区间重叠≥70%且不超过30%）和范围级指标（按比例分配分数）评估。DAST在聚合指标上表现最优，标准F1分数为0.910，准确率为0.843，远超最强基线（TSAD Agents的0.500 F1和0.338准确率）。在接口级评估中，DAST在所有接口上均领先，其中F1-c最难检测（标准F1为0.808），而E2（0.932）和A1（0.941）表现最佳。范围级指标进一步验证了DAST的鲁棒性，其误报率低（非异常基线中48个样本仅9个假阳性），且能通过领域知识正确识别根因（如F1-u时延而非丢包）。

### Q5: 有什么可以进一步探索的点？

DAST的局限性首先体现在验证范围狭窄，仅基于单一开源O-RAN栈，未在异构多厂商部署中测试，且性能退化模式有限，其零样本泛化能力尚需在更真实的零日攻击场景中验证。其次，当前框架仅输出报告和分级标签，未形成闭环自动化——即无法基于检测结果自动定位根因并生成缓解策略（如动态调整资源分配或隔离受损接口）。未来可探索的方向包括：1）引入联邦学习或跨域知识图谱，使DAST能适应不同厂商的接口特征差异，同时保持隐私合规；2）将VLM/LLM的推理结果与因果图模型结合，实现从“检测异常”到“解释根因”的端到端推理；3）设计轻量化微调策略（如LoRA），使领域知识能低成本适配新攻击模式，避免完全重新训练。此外，可考虑将多模态时间序列表示从固定热力图扩展为动态图结构（如时序知识图谱），以捕捉接口间的高阶依赖关系，提升对复杂级联故障的检测能力。

### Q6: 总结一下论文的主要内容

DAST提出了一种面向O-RAN跨接口异常检测的零样本多智能体框架，解决了传统时序异常检测方法在标签稀缺、威胁演化快、高维多变量遥测数据中失效的问题。该框架采用三阶段VLM→LLM→VLM流水线：首先将多变量KPI流转换为视觉表示，然后利用LLM基于O-RAN领域知识对每个接口的文本描述进行评分，最后通过VLM在高分辨率热图上验证可疑区域，输出问题接口、异常时间区间、符合O-RAN WG11标准的操作影响评级及决策依据。在真实O-RAN测试台数据上的评估表明，DAST在代表性性能退化场景下取得了0.910的F1分数和0.843的准确率，优于现有最先进的时序异常检测基线。其核心贡献在于将异常检测从单模型数值拟合问题转化为基于领域知识的多智能体推理问题，为6G计算连续体提供了可维护的观测原语。
