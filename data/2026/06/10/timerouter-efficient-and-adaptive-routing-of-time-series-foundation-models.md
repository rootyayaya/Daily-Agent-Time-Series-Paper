---
title: "TimeRouter: Efficient and Adaptive Routing of Time-Series Foundation Models"
authors:
  - "Kanghui Ning"
  - "Yushan Jiang"
  - "Kashif Rasul"
  - "Anderson Schneider"
  - "Yuriy Nevmyvaka"
  - "Dongjin Song"
date: "2026-06-10"
arxiv_id: "2606.11625"
arxiv_url: "https://arxiv.org/abs/2606.11625"
pdf_url: "https://arxiv.org/pdf/2606.11625v1"
github_url: "https://github.com/UConn-DSIS/TimeRouter"
categories:
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "时间序列基础模型"
  - "模型路由"
  - "自适应专家选择"
  - "轻量级路由"
  - "时序预测"
  - "GIFT-EVAL"
  - "集成回退"
  - "选择性门控"
  - "可解释性"
relevance_score: 8.5
---

# TimeRouter: Efficient and Adaptive Routing of Time-Series Foundation Models

## 原始摘要

Time-series foundation models (TSFMs) are increasingly explored as predictive experts within emerging agentic time-series systems. However, TSFMs exhibit heterogeneous inductive biases, and no single model consistently dominates across forecasting regimes, making expert selection a critical challenge. Existing systems often delegate this decision to LLM-based controllers, incurring substantial inference overhead. We present TimeRouter, an efficient routing framework that leverages empirical complementarity across a pool of pretrained TSFMs through lightweight discriminative routing, selective gating, and ensemble fallback. Concretely, TimeRouter combines a learned routing head, a selective gate, and an ensemble fallback, enabling adaptive expert selection without invoking an LLM at inference time. TimeRouter achieves state-of-the-art performance on the GIFT-EVAL leaderboard, with an LB MASE of 0.6765. Beyond benchmark performance, our ablation studies provide empirical insights into TSFM routing design, highlighting the importance of pool composition and selective gating. Taken together, these results position TimeRouter as a modular and lightweight routing layer for future agentic time-series systems built upon foundation-model pools. Our code is available at https://github.com/UConn-DSIS/TimeRouter.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列基础模型（TSFM）近年来发展迅速，但不同模型在架构、预训练数据上存在异质性归纳偏差，导致没有任何单一模型能在所有预测场景（如不同采样频率、预测长度、领域和噪声结构）中持续最优。现有方法主要依赖LLM作为控制器进行专家选择（如TimeCopilot、MoiraiAgent），虽然有效但推理开销巨大；而其他非LLM方法（如Synapse的逐时间步自适应加权、ZooCast的嵌入相似度匹配）则缺乏轻量级的判别式路由机制。因此，核心挑战在于如何在不引入LLM推理负担的前提下，实现高效、自适应的TSFM专家选择。本文提出TimeRouter，通过轻量级判别式路由、选择性门控和集成回退机制，利用预训练TSFM池的经验互补性，在GIFT-EVAL榜单上达到0.6765的LB MASE，创下新纪录。该方法无需LLM参与推理，为未来基于基础模型池的智能时间序列系统提供了模块化、高效的路由层。

### Q2: 有哪些相关研究？

相关研究可分为三类：

**1. LLM驱动的时序模型路由方法**：TimeCopilot通过通用LLM代理进行特征分析和模型选择；MoiraiAgent使用微调的Qwen-2.5-3B进行逐序列专家选择；TSOrchestra采用R1风格微调LLM进行多模型池的集成编排。这些方法依赖LLM进行决策，推理开销大。TimeRouter通过轻量级判别路由头替代LLM，显著降低计算成本。

**2. 非LLM的模型协调方法**：Synapse通过动态重加权实现时间戳级别的自适应仲裁；ZooCast利用嵌入和相似性进行Top-K模型匹配。这些方法虽不依赖LLM，但缺乏可学习的判别式路由机制。TimeRouter结合了可学习的路由头、选择性门控和集成回退，实现更精细的专家选择。

**3. 理论基础相关工作**：堆叠泛化（Stacked Generalisation）启发TimeRouter使用交叉验证分数和下采样预测作为路由特征；选择性预测（Selective Prediction）指导TimeRouter通过置信度阈值实现风险-覆盖率的可控权衡，将低置信度输入导向集成回退。

TimeRouter的核心创新在于将判别式路由、选择性门控和集成回退三者有机结合，在不调用LLM的情况下实现自适应专家选择，并在GIFT-EVAL基准上达到SOTA性能（LB MASE 0.6765）。

### Q3: 论文如何解决这个问题？

TimeRouter通过一个轻量级路由框架解决时间序列基础模型（TSFM）的异构归纳偏差与专家选择问题，无需在推理时调用LLM。其核心方法包含三个组件：**路由头**、**选择性门控**和**集成回退**。

**整体框架**：给定一个固定池中的K个冻结TSFM，TimeRouter将输入上下文x映射为路由策略π(x)，输出为选定的最佳模型或集成组合的预测。路由头基于一个固定特征映射φ(x)，该特征映射拼接了上下文统计量（趋势、季节性、自相关等）、每个模型在上下文上的交叉验证分数以及下采样后的模型预测。对每个模型Fk，训练一个二分类器gθk预测其是否为该输入的最优模型（通过最小化二元交叉熵损失）。推理时，K个分类器分数经L1归一化得到得分向量p(x)。

**选择性门控**：门控机制基于两个标量信号——**边际m(x)**（最高分与次高分之差）和**多样性d(x)**（各模型预测在时间步上的标准差，经上下文尺度归一化）。当m(x)低于阈值τm或d(x)低于阈值τd时（表示置信度低或模型预测高度一致），门控将决策回退至集成组合；否则选择得分最高的模型。

**集成回退**：采用**CV逆加权平均**作为组合器，权重与每个模型在上下文上的交叉验证MASE（CV_score）成反比，即表现越好的模型权重越大。该组合器可替换为其他组合方式（如均值、中位数等），不影响门控机制。

**创新点**：1）通过轻量级路由头替代LLM控制器，大幅降低推理开销；2）引入基于边际和多样性的选择性门控，实现自适应专家选择；3）在GIFT-EVAL榜单上达到SOTA（LB MASE 0.6765），并通过消融实验揭示了池组成和选择性门控的重要性。

### Q4: 论文做了哪些实验？

论文在GIFT-EVAL基准上进行了实验，该基准包含97个预测任务，使用公共排行榜评估。实验设置中，基础模型池包含四个冻结的预训练模型：Chronos-2、FlowState、PatchTST-FM和Sundial。路由头使用305维特征图，通过XGBoost进行一对多分类，并采用选择性门控和集成回退机制。主要结果方面，TimeRouter在GIFT-EVAL排行榜上取得了0.6765的LB MASE，优于最强单模型Chronos-2（0.6978）约200个基点，并略胜于最强LLM路由系统TSOrchestra（0.6768）约3个基点，且无需LLM推理开销。效率方面，TimeRouter训练仅需约110秒，推理延迟仅9.9毫秒/序列，远低于TSOrchestra（≥472.6毫秒）。消融实验显示：选择性门控带来13个基点的整体提升，尤其在长周期任务上提升90个基点；XGBoost作为路由头表现最佳（0.6765），而逻辑回归最差（0.6836）；模型池消融表明Chronos-2是关键锚点，移除它导致性能下降111个基点，而完整四模型池优于任何子集。

### Q5: 有什么可以进一步探索的点？

TimeRouter虽然取得了优异性能，但存在几个值得深入探索的局限。首先，其路由决策完全依赖时间序列的统计特征，忽略了任务语义和领域知识，未来可引入轻量级元学习器，将任务描述、数据来源等上下文信息编码为路由先验。其次，当前池中模型均为预训练TSFM，未考虑针对特定工业场景微调的专用模型，可探索混合池策略，将通用基础模型与领域特化模型结合，并通过在线学习动态调整路由权重。第三，选择性门控在长时域任务中有效，但短时域下可能因模型分歧不足而退化，可设计自适应门控阈值，根据预测不确定性动态启用或禁用集成回退。此外，当前框架仅支持单步路由，未来可扩展为多步时序路由，允许在不同预测阶段切换专家模型。最后，可研究路由头的可解释性，将模型选择依据可视化，提升工业故障诊断场景下的信任度。

### Q6: 总结一下论文的主要内容

TimeRouter提出了一种高效、自适应的时序基础模型路由框架，解决了现有基于LLM的控制器在选择专家模型时推理开销大的问题。其核心贡献在于通过轻量级判别路由、选择性门控和集成回退机制，在不调用LLM的情况下实现自适应专家选择。方法上，TimeRouter结合了可学习路由头、选择性门控和集成回退，能够从预训练的时序基础模型池中动态选择最优模型。在GIFT-EVAL排行榜上，TimeRouter取得了0.6765的LB MASE，达到最先进性能。消融实验揭示了池组成和选择性门控的重要性，特别是门控在长时域任务中效果显著。该框架作为模块化路由层，可轻松集成新模型而无需重新训练，为未来基于基础模型池的智能时序系统提供了高效、可扩展的解决方案。
