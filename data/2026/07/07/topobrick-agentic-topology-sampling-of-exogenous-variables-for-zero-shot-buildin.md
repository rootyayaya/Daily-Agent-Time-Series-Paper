---
title: "TopoBrick: Agentic Topology Sampling of Exogenous Variables for Zero-Shot Building IoT Forecasting"
authors:
  - "Xiachong Lin"
  - "Du Yin"
  - "Arian Prabowo"
  - "Hao Xue"
  - "Wen Hu"
  - "Imran Razzak"
  - "Matthew Amos"
  - "Sam Behrens"
  - "Flora D. Salim"
date: "2026-07-07"
arxiv_id: "2607.06349"
arxiv_url: "https://arxiv.org/abs/2607.06349"
pdf_url: "https://arxiv.org/pdf/2607.06349v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Zero-Shot Forecasting"
  - "Building IoT"
  - "Knowledge Graph"
  - "Topology Sampling"
  - "Exogenous Variables"
  - "Training-Free Framework"
  - "HVAC"
  - "Sensor Forecasting"
relevance_score: 8.5
---

# TopoBrick: Agentic Topology Sampling of Exogenous Variables for Zero-Shot Building IoT Forecasting

## 原始摘要

Building sensors are embedded in physical topology, spatial hierarchy, and operational context, yet existing forecasters often treat them as isolated time series or rely on fixed covariate sets. We present TopoBrick, a training-free framework for zero-shot building IoT (Internet-of-Things) forecasting. TopoBrick uses building knowledge graphs to construct a compact structural skeleton and employs an agentic topology sampler to select target-specific exogenous variables. The selected variables are organized by deployment-time availability, separating past-known sensor states from future-known calendar, schedule, and meteorological exogenous variables. Across three real-world buildings, TopoBrick outperforms strong zero-shot foundation-model baselines and remains competitive with fully trained building-specific models. Ablations show that topology-aware sampling is more reliable than random, ontology-only, or fixed-hop selection, especially for physically coupled HVAC and weather-driven sensing variables.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

现代建筑是密集的信息物理系统，包含成百上千个传感与控制点。准确预测这些传感器时间序列对于需求响应、故障检测和预测性控制至关重要。然而，现有方法存在显著不足：通道独立模型将每个传感器孤立处理，多变量模型依赖固定的预定义变量集，时间序列基础模型虽支持零样本预测，但仍将外生变量视为平坦集合，缺乏从异构建筑知识图谱中为目标传感器选择物理相关外生变量的机制。此外，训练建筑专用模型需要大量历史数据和调参，难以跨建筑组合规模化部署。本文要解决的核心问题是：如何在无需建筑特定训练的条件下，利用建筑知识图谱（如Brick模式）提供的物理拓扑、空间层级和运行上下文，为零样本建筑物联网预测自动选择目标特定的外生变量。TopoBrick通过将原始知识图谱蒸馏为紧凑骨架，并采用智能体拓扑采样器结合图谱验证，实现了无需训练的外生变量选择，从而让冻结的时间序列基础模型能利用建筑特定上下文进行准确预测。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及三大类工作。**方法类**包括基于深度学习的时序预测模型，如Transformer变体（Informer）、线性模型（DLinear）、通道独立模型（PatchTST）、跨变量注意力（iTransformer）、多尺度混合（TimeMixer）及显式外生变量建模（TimeXer）。此外，LLM适配方法（GPT4TS、TimeLLM、GPT4MTS）和时序基础模型（Chronos、TimesFM、Moirai）也属此类。这些方法通常需要任务特定训练或假设固定变量集，而TopoBrick无需训练，且能利用建筑拓扑动态选择外生变量，避免了噪声注入和成本问题。**应用类**聚焦建筑领域，如基于Brick本体的语义元数据研究，用于点分类、实体标注及端到端管道构建；建筑知识图谱还被用于自然语言问答和负荷预测（包括隐私保护场景）。这些工作虽利用语义元数据，但通常针对单栋建筑或依赖手工规则，未实现跨建筑零样本泛化。**评测类**工作较少，现有基础模型多在固定变量集的基准上评估，忽略了建筑IoT中变量选择的空间物理关系。TopoBrick填补了这一空白，通过无训练、建筑无关的拓扑采样机制，将零样本基础模型与建筑知识图谱的异构结构连接起来，实现了物理相关外生变量的自动选择与分离。

### Q3: 论文如何解决这个问题？

TopoBrick通过一个无需训练的三阶段框架解决建筑IoT零样本预测问题。其核心创新在于利用建筑知识图谱进行智能外生变量选择。

**整体框架**包含三个模块：
1. **建筑骨架构建**：从原始知识图谱中提取结构节点（设备、位置）和结构关系（设备流、空间包含），将传感器点作为附件挂载，形成紧凑的拓扑骨架，避免全图遍历的不稳定性。
2. **智能拓扑采样器**：针对目标传感器点，构建包含目标锚点、局部拓扑和全局上下文的拓扑上下文。基于物理相关性、拓扑定位和受控扩展三大原则，由LLM推理生成结构化的采样动作（锚点、扩展范围、物理角色）。随后通过KG验证器检查动作的合法性（锚点存在性、角色匹配性、范围一致性），确保选择可靠。
3. **零样本预测器**：将验证后的动作执行并物化为时间序列变量。关键创新是按部署时可用性将变量分为两类：**过去已知变量**（其他传感器历史观测）和**未来已知变量**（日历、运行计划、气象预报）。其中气象预报由独立的轻量级预测器生成。最终将目标历史、两类外生变量拼接后输入冻结的预训练基础模型，实现零样本预测。

**关键技术**包括：基于知识图谱的拓扑推理、LLM驱动的结构化动作生成、KG验证的可靠性保障，以及部署时可用性感知的变量组织。该方法在三个真实建筑中优于强零样本基线，与全监督模型竞争力相当，尤其对物理耦合的HVAC和气象变量采样更可靠。

### Q4: 论文做了哪些实验？

论文在三个真实建筑（LBNL59、BTS-B、BTS-C）上评估TopoBrick，数据粒度为15分钟，历史长度96步，预测步长H={24,48,72,96}（对应6h-24h）。对比方法包括：Naive方法（Persistence、Seasonal Naive）、全监督方法（FITS、DLinear、PatchTST、iTransformer）和零样本方法（Chronos-2、Moirai、TimesFM）。主要指标为归一化MAE和MSE。结果显示：TopoBrick在LBNL59上所有H下nMSE最优（0.976/1.691/2.064/2.228），较最强基线PatchTST在H=48提升7.4%；在BTS-B上所有H下两项指标均最优，如H=24时nMAE从Chronos-2的0.316降至0.295；在BTS-C上nMAE与最佳监督模型持平（H=24时均为0.319）。消融实验表明拓扑感知采样优于随机、本体或固定跳数选择，尤其在HVAC和气象相关传感器上提升显著。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：1) 拓扑采样依赖预定义的知识图谱，构建成本高且难以迁移至无图谱场景；2) 对高方差传感器（如BTS-C中的部分流）提升有限，表明当前拓扑感知的外生变量集可能遗漏了某些关键驱动因素；3) 仅使用单一LLM（gpt-oss-20b）进行agentic推理，未探索不同规模或专业领域模型的影响。

未来可探索的方向包括：1) 引入动态拓扑学习机制，使系统能自动发现并更新传感器间的隐式关联，降低对人工知识图谱的依赖；2) 结合因果发现方法，识别对特定目标变量真正有因果影响的外生变量，而非仅基于拓扑邻近性采样；3) 设计多Agent协作框架，让不同Agent分别负责拓扑推理、变量筛选和预测优化，提升复杂场景下的鲁棒性；4) 探索将TopoBrick与轻量级在线微调结合，在零样本基础上快速适应建筑运行模式的变化。

### Q6: 总结一下论文的主要内容

TopoBrick提出了一种零样本建筑物联网预测框架，解决了现有方法将传感器视为孤立时间序列或依赖固定协变量集的问题。其核心贡献在于利用建筑知识图谱构建紧凑结构骨架，并通过智能体拓扑采样器自动选择目标特定的外生变量。方法上，根据部署时的可用性将变量分为过去已知的传感器状态和未来已知的日历、气象等外生变量。在三个真实建筑上的实验表明，TopoBrick超越了强零样本基础模型基线，并与完全训练的建筑专用模型性能相当。消融实验证实，拓扑感知采样比随机、仅本体或固定跳数选择更可靠，尤其对物理耦合的暖通空调和气象传感变量效果显著。该工作为无需训练的零样本预测提供了新范式，展示了利用结构化知识提升时间序列预测泛化能力的潜力。
