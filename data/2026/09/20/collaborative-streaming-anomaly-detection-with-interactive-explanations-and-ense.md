---
title: "Collaborative Streaming Anomaly Detection with Interactive Explanations and Ensemble Consensus"
authors:
  - "Diogo Risca"
  - "Afonso Lourenço"
  - "Ricardo Martins"
  - "Goreti Marreiros"
date: "2026-09-20"
arxiv_id: "2609.23883"
arxiv_url: "https://arxiv.org/abs/2609.23883"
pdf_url: "https://arxiv.org/pdf/2609.23883v1"
categories:
  - "cs.LG"
tags:
  - "流式异常检测"
  - "集成共识"
  - "可解释性"
  - "代理模型"
  - "人机交互"
  - "工业传感器"
  - "异常解释"
  - "交互式诊断"
relevance_score: 7.5
---

# Collaborative Streaming Anomaly Detection with Interactive Explanations and Ensemble Consensus

## 原始摘要

We present a collaborative streaming anomaly detection system for high-speed data streams that explicitly integrates human analysts into the decision loop. The system combines heterogeneous detectors and aggregates their outputs through a normalization-based weighted consensus, complemented by artifact-aware rules to stabilize anomaly scoring under deployment. To improve interpretability, it derives surrogate models that approximate the ensemble consensus and expose human-readable sensor conditions associated with anomalous behavior. Analysts can actively intervene by reviewing anomaly episodes, adjusting consensus behavior, and refining surrogate rules used for anomaly prediction, producing a human-adjusted ensemble. We evaluate the approach on an industrial stream with 260\,000 events and 3 anomalous episodes, showing robust detection and actionable human-AI interaction.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决高速数据流场景下异常检测系统难以在实际部署中落地的问题。研究背景是：工业等实时流数据具有未知且动态演化的特性，而现有流式机器学习方法大多依赖即时获得真实标签进行全监督自适应，这在现实中不可行。尽管已有大量异常检测技术和成熟开源工具，但它们仍难以被广泛采用。作者认为，核心障碍在于缺乏一套能在部署条件下有效运行、并系统性地增强流中监督信息的技术栈。现有方法的主要不足包括：过度依赖监督标签、异构检测器输出难以稳定融合、异常评分缺乏可解释性，以及人类分析师无法有效介入决策循环。因此，本文要解决的核心问题是：如何构建一个协作式流式异常检测系统，将异构检测器通过归一化加权共识进行集成，利用代理模型将共识结果转化为人类可读的传感器条件解释，并支持分析师审查异常片段、调整共识行为、优化代理规则，从而形成“人在回路”与“AI在回路”相结合的人机协同异常检测与解释机制，并在真实工业提花织机数据流上验证其有效性。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，流式机器学习方法多依赖全监督自适应，但真实场景难以即时获得标签；为此出现了大量无监督/半监督流式异常检测与集成技术，以及成熟开源项目，但它们在部署条件下的稳定性与可解释性仍不足。本文与这些工作的区别在于，不追求单一检测器精度，而是通过异构检测器、增量归一化与真值发现式加权共识，并加入伪影感知规则来稳定在线评分。人机交互类方面，已有机器教学（human-in-the-loop）与交互学习（AI-in-the-loop）两条脉络：前者由人提供标签、约束与特征设计，后者由模型向人提供解释与不确定性以支持决策。本文明确落在AI-in-the-loop协作范式，但进一步将解释、阈值调整、检测器选择与规则精炼整合为统一流式系统。可解释性类方面，代理模型与规则提取被广泛用于事后解释，但多用于离线批处理。本文的规则代理模型不仅解释共识评分、暴露可读传感器条件，还用于过滤不一致评分向量并监测概念漂移，进而支持分析师干预形成“人调集成”。评测类方面，现有流式异常检测评测多关注检测指标，缺乏对协作交互有效性的工业验证；本文以提花织机26万事件、3个异常片段的工业流案例，验证了鲁棒检测与可操作的人机交互。

### Q3: 论文如何解决这个问题？

论文提出一个模块化四阶段协同流式异常检测框架。首先，在检测层采用四种异构流式检测器——xStream、RSHash、HST 和 RRCF，分别基于多尺度密度、随机子空间直方图、随机二叉树节点质量和鲁棒随机割森林，以互补假设覆盖统计、距离、密度与隔离等不同异常机制。其次，在集成层将异常检测建模为“归一化 + 真值发现”两阶段过程：用增量 Z-Score 校准器把各检测器分数转为可比概率，再通过 Full、DivE 或 ULARA 三种策略加权融合，并可选实例级与检测器级过滤，共形成 12 种集成策略，从而在部署中稳定异常评分。第三，在解释层构建基于 AMRules 的规则代理模型，包括原始数据代理和共识分数代理，增量学习可读规则，并引入 ChebyOS 过采样缓解极端不平衡，同时利用规则统计量计算 Ascore 识别不一致分数向量。最后，在人机交互层，分析人员可审查异常片段、过滤伪异常、调整聚合权重、选择检测器子集并精炼代理规则，形成“人类调整后的共识集成”。创新点在于将异构检测器集成、规则代理解释与人类干预统一为信息流闭环，使系统既能解释“为何判定异常”，又能表达不确定性，并在 26 万事件工业流上验证了稳健检测与可操作的人机协同。

### Q4: 论文做了哪些实验？

论文在工业织机数据流上进行了实验，共包含260,000个事件和3个异常片段。实验首先独立评估了四种流式异常检测器（HS-Trees、RRCF、RSHash、xStream），其ROC-AUC分别为97.71、45.77、11.64和7.64，说明单一检测器不可靠。随后引入基于归一化加权共识的集成框架：仅用增量Z-score归一化和检测器级过滤时ROC-AUC达99.08；再加入实例级过滤与规则覆盖验证后提升至99.46。系统还训练代理模型在原始传感器空间复现集成决策，并提取可读规则R1（过流且相电压塌陷）和R2（过流且电压正常但电流谐波畸变增大），经专家交互修正后形成人类调整集成。特征重要性显示PhaseVoltage、PowerFactor和ReactivePower最关键。三个异常片段分别以约89%、60%/40%、54%/46%的R1/R2比例被规则覆盖。计算开销方面，RRCF约1080s、HST约480s、xStream约150s、RSHash约95s；代理规则约1600s，检测器共识约45s，实例过滤约420s，专家规则应用约12s。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于仅在单一工业场景（提花机、26万事件、3个异常片段）上验证，样本量小且异常类型有限，泛化性存疑；同时人类反馈目前依赖人工审查与规则调整，缺乏自动化的偏好学习机制，交互成本较高。未来可从三方面探索：一是引入自动化偏好学习，将分析师的接受、拒绝与阈值调整转化为可训练的反馈信号，实现人在回路中的持续自适应；二是扩展到多设备、多工况与概念漂移场景，检验共识集成与代理规则在分布变化下的稳定性；三是将代理规则与因果推断或反事实解释结合，使异常解释不仅可读，还能回答“若调整某传感器会怎样”。此外，可探索多分析师协作与反馈冲突消解机制，并研究代理规则漂移的自动检测与再校准策略。

### Q6: 总结一下论文的主要内容

论文针对高速数据流中的异常检测问题，提出了一种将人类分析师显式纳入决策回路的协作式流式异常检测系统。方法上，系统集成多种异构检测器，通过基于归一化的加权共识进行集成，并引入伪影感知规则以稳定部署时的异常评分；同时构建代理模型近似集成共识，输出与异常行为相关的可读传感器条件。分析师可审查异常片段、调整共识行为并优化代理规则，形成人工校正后的集成。在包含26万事件、3个异常片段的工业提花机数据流上，该方法将ROC-AUC从最佳单检测器的97.71提升至99.46，且原始数据代理提炼出两条可解释规则，能区分电压崩溃与波形畸变故障。结论表明，该架构为流式环境中可操作的人机协作提供了可推广的管道，未来将探索从分析师反馈中自动学习偏好。
