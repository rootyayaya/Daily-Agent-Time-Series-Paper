---
title: "Self-Adaptive Anomaly Detection with Reinforcement Learning and Human Feedback in Connected Vehicles"
authors:
  - "Matthias Weiß"
  - "Athreya Hosahalli Prakash"
  - "Maurice Artelt"
  - "Falk Dettinger"
  - "Nasser Jazdi"
  - "Michael Weyrich"
date: "2026-07-09"
arxiv_id: "2607.08373"
arxiv_url: "https://arxiv.org/abs/2607.08373"
pdf_url: "https://arxiv.org/pdf/2607.08373v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "在线异常检测"
  - "强化学习"
  - "人类反馈"
  - "自适应框架"
  - "概念漂移"
  - "连接车辆"
  - "微服务拓扑"
  - "深度Q网络"
  - "统计漂移检测"
  - "人机协同重训练"
relevance_score: 6.5
---

# Self-Adaptive Anomaly Detection with Reinforcement Learning and Human Feedback in Connected Vehicles

## 原始摘要

Connected vehicles are autonomous cyber-physical systems whose behavior must be continuously monitored during operation to detect deviations from normal operation before they propagate into failures. Such evaluation is challenging because the systems themselves evolve: over-the-air updates, configuration changes, and shifting workloads alter the definition of normal behavior, causing static diagnostic methods to degrade silently over time. Existing approaches typically address either automated model adaptation or operator integration in isolation, rather than as a single coordinated supervisory loop.
  This paper presents an online anomaly detection framework for autonomous CPS that integrates three coordinated mechanisms. A factorized deep Q-network with self-attention selects the most suitable detector from a candidate pool for each monitored service, exploiting inter-service dependencies in the microservice topology. An ensemble of three statistical drift detectors monitors the input distribution and raises an alarm only when all three concur, prioritizing precision over recall. A human-in-the-loop retraining mechanism, built around a pending transition buffer and a 60/40 prioritized replay strategy, allows the operator to incorporate expert knowledge while preserving the system's learned response to prior data distributions.
  The framework is evaluated on a connected-vehicle testbed running an automated valet parking application across seven backend microservices. The attention-augmented agent achieves an F1 score of 0.69, compared to at most 0.11 for any single detector applied uniformly. Following a real software update that induces measurable concept drift, F1 drops to 0.52; after operator-triggered retraining, performance recovers to 0.65 on the new distribution while remaining at 0.69 on the prior one, demonstrating sustained adaptation without catastrophic forgetting.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

联网车辆是自主信息物理系统，其行为需持续监控以在故障传播前检测异常。然而，系统本身会不断演变：空中升级、配置变更和动态负载会改变正常行为的统计特性，导致静态诊断方法随时间悄然失效。现有方法存在两大不足：一是自动化适应方法（如模型选择策略）能应对数据分布变化，但作为黑箱运行，操作员无法注入领域知识或纠正错误推断；二是操作员参与方法保留了人类决策权，但缺乏检测何时需要适应的机制，且在重训练时无法保留先前知识。对于需要持续适应和操作员监督的自主信息物理系统，这两类方法均不充分。本文旨在解决这一核心问题：如何构建一个集成的自监督循环，既能自动适应概念漂移，又能让操作员有效介入并防止灾难性遗忘。为此，论文提出了一个在线异常检测框架，通过因子化深度Q网络选择检测器、统计漂移检测器集成触发重训练、以及基于待定回放缓冲区和优先重放策略的人机协同重训练机制，实现持续适应与知识保留的统一。

### Q2: 有哪些相关研究？

在相关研究中，本文主要涉及三类工作。**方法类**包括非强化学习的自适应异常检测方法，如ADWIN（自适应窗口算法）、SALAD（分裂主动学习异常检测）和基于LSTM的流式方法，这些方法需要精细的阈值调优、依赖周期性人工标注或缺乏显式漂移处理机制，且未提供操作员知识的结构化通道。**应用类**中，强化学习已被用于异常检测，Zhang等人提出的基于RL的模型选择方法最接近本文工作，但缺少在线概念漂移操作、显式漂移检测机制和操作员集成。Zhou等人的因子化DQN架构为微服务拓扑中每服务检测器选择提供了结构基础。**评测类**中，统计漂移检测领域已成熟，如Page-Hinkley检验、Kolmogorov-Smirnov检验和基于马氏距离的方法，ADA-ADF框架集成了KS漂移检测与重建误差监控，但未涉及RL检测器选择或专家反馈。此外，人类反馈强化学习（RLHF）已用于时间序列异常检测的人机协同框架，但仍与漂移检测和自主CPS监督上下文脱节。本文首次将RL检测器选择、统计漂移检测和操作员驱动的重训练（含遗忘预防）集成到单一监督循环中，用于网联车辆异常检测。

### Q3: 论文如何解决这个问题？

该论文提出一个集成了强化学习与人类反馈的自适应异常检测框架，核心方法围绕一个因子化深度Q网络（F-DQN）展开。整体架构包含四个主要组件：**指标收集与特征提取层**、**强化学习智能体**、**概念漂移检测集成模块**以及**专家反馈接口**。

**核心方法**是将异常检测器选择问题建模为多离散马尔可夫决策过程。智能体基于每个服务的9维统计特征（均值、标准差、偏度等）状态，为每个服务从候选池（MAD、SRD、OC-SVM等7种）中选择最优检测器。

**架构设计**的关键创新在于因子化网络结构：一个共享编码器处理所有服务的特征，再通过N个独立的线性头为每个服务输出Q值。这种设计支持服务拓扑的动态变化（增删服务只需调整对应头）。进一步地，**多头自注意力机制**被引入以建模微服务间的依赖关系，使每个服务能关注其他服务的嵌入表示，从而捕捉级联故障模式。

**关键技术**包括：1）**集成漂移检测**：Page-Hinkley、Kolmogorov-Smirnov和Mahalanobis距离三种统计检测器共同判定，仅当三者一致时才触发告警，优先保证精度。2）**人类反馈循环**：通过待定过渡缓冲区异步处理专家反馈，采用选择性更新策略（为未标注服务分配伪奖励）保持梯度完整。3）**60/40优先重放策略**：重放缓冲区中60%来自新分布、40%来自旧分布，在适应新分布的同时防止灾难性遗忘。

### Q4: 论文做了哪些实验？

论文在连接车辆测试平台上进行实验，运行自动代客泊车应用，包含7个后端微服务。实验设置包括：使用OpenTelemetry以1秒分辨率收集每个服务的CPU利用率和RAM使用率，滑动窗口大小为64，共14个时间序列。RL代理通过注入三种异常（突然尖峰、逐渐漂移、服务退化）进行初始化，生成超过80万数据点，其中30万用于监督训练，10万用于验证，40万用于评估。

对比方法包括MAD、SRD、SPOT、OC-SVM、RRCF、LODA、xStream等单一检测器，以及MLP变体F-DQN。主要结果：提出的F-DQN-Attn（注意力增强）在评估集上F1得分为0.69（精确率0.71，召回率0.68），显著优于最佳单一检测器MAD（F1=0.11）和MLP变体（F1=0.47）。在真实软件更新导致概念漂移后，F1降至0.52；通过操作员触发的重训练（使用60/40优先回放缓冲区），在新分布上恢复至0.65，同时旧分布保持0.69，证明无灾难性遗忘的稳定适应。漂移检测集成在更新后约600秒达成一致，优先保证精度。

### Q5: 有什么可以进一步探索的点？

该论文在实验设计上存在明显局限：仅基于单一测试平台、单一应用场景和一次概念漂移事件，且专家反馈通过模拟标签实现，忽略了真实标注噪声与专家分歧。未来可沿三个方向深入：首先，扩展至更多车辆拓扑、应用类型及信号模态（如CAN总线、网络流量），验证框架的跨域泛化能力；其次，引入真实操作员进行人机交互实验，研究标注噪声对重训练策略鲁棒性的影响，并设计能减轻操作员认知负荷的反馈界面；最后，强化统计严谨性，通过多随机种子实验、漂移检测器集成消融及注意力层计算开销分析，明确各组件贡献。此外，当前仅使用CPU/RAM指标且仅覆盖三种异常模式，可探索更丰富的故障类型（如传感器偏差、通信延迟）与高维时序特征，并考虑将强化学习动作空间扩展为连续型检测器参数调整，而非离散选择，以提升自适应粒度。

### Q6: 总结一下论文的主要内容

该论文提出了一种面向网联车辆的自适应异常检测框架，将强化学习、统计漂移检测与人工反馈整合为统一在线监控回路。问题定义在于网联车辆系统因OTA更新、配置变化等导致行为分布漂移，静态检测方法性能会随时间退化。方法上，采用带自注意力的分解深度Q网络从候选池中为每个微服务选择最优检测器，利用三个统计漂移检测器组成集成模块（三者一致才触发告警），并引入基于待定过渡缓冲区和60/40优先级回放策略的人工参与重训练机制。在自动代客泊车应用七个后端微服务上的实验表明，注意力增强智能体F1达0.69，远超单一检测器（最高0.11）；软件更新引发概念漂移后F1降至0.52，经人工触发重训练恢复至0.65，且旧分布上保持0.69，验证了无灾难性遗忘的在线自适应能力。该工作首次将自动化模型适应与操作员监督结合为协调回路，为复杂CPS的持续监控提供了新范式。
