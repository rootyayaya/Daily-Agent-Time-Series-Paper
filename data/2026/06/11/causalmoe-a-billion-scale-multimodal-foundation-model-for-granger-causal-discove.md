---
title: "CausalMoE: A Billion-Scale Multimodal Foundation Model for Granger Causal Discovery with Pattern-Routed Heterogeneous Experts"
authors:
  - "Bo Liu"
  - "Di Dai"
  - "Jingwei Liu"
  - "Jiarui Jin"
  - "Xiaocheng Fang"
  - "Guangkun Nie"
  - "Hongyan Li"
  - "Shenda Hong"
date: "2026-06-11"
arxiv_id: "2606.13024"
arxiv_url: "https://arxiv.org/abs/2606.13024"
pdf_url: "https://arxiv.org/pdf/2606.13024v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Granger因果发现"
  - "时间序列分析"
  - "多模态基础模型"
  - "混合专家系统"
  - "LLM集成"
  - "VLM集成"
  - "因果图学习"
  - "分布偏移建模"
  - "少样本泛化"
relevance_score: 7.5
---

# CausalMoE: A Billion-Scale Multimodal Foundation Model for Granger Causal Discovery with Pattern-Routed Heterogeneous Experts

## 原始摘要

Granger Causal Discovery (GCD) is fundamental for analyzing temporal dependencies in complex systems. However, existing neural GCD methods predominantly rely on a "one-size-fits-all" paradigm, struggling to capture distribution shifts and dynamic regime changes inherent in real-world time series. This often leads to entangled representations and spurious causal graphs. In this paper, we propose CausalMoE, a billion-scale multimodal Granger causal foundation model that explicitly models patch-level heterogeneity. CausalMoE introduces a Pattern-Routed Mixture of Heterogeneous Experts, which dynamically identifies latent temporal patterns and routes patches to specialized domain experts, effectively decoupling regime-specific mechanisms from shared dynamics. To ensure interpretable graph recovery, we design a Causality-Aware Self-Attention mechanism operating across variables, yielding sparse Granger causal graphs via proximal optimization. Furthermore, CausalMoE is the first to integrate LLMs and VLMs to align numerical signals with textual and visual priors, regularizing causal estimation in complex scenarios. Extensive experiments demonstrate that CausalMoE establishes a new state-of-the-art on fully supervised benchmarks, while effectively generalizing to few-shot settings where traditional methods fail.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决现有格兰杰因果发现（GCD）方法在处理真实世界时间序列时面临的“一刀切”范式局限性。研究背景方面，尽管深度神经网络已成功将GCD扩展到非线性和高维场景，但现有方法普遍隐含“均匀分布建模”（UDM）假设，即认为所有时间片段服从单一数据生成分布。然而，现实系统常存在分布偏移和动态机制变化，甚至短时间片内因果关系都可能发生改变。现有方法的不足体现在两方面：一是UDM策略将异质机制混为一谈，导致因果表征纠缠，产生虚假因果图；二是现有GCD方法严格局限于单模态数值数据，忽略了文本描述、事件标注或视觉状态等语义上下文，而这些信息对于区分仅凭数值无法识别的因果联系至关重要。本文要解决的核心问题是：能否构建一个十亿参数级别的多模态格兰杰因果基础模型，既能显式建模时间序列中补丁级别的异质性，通过模式路由的异构专家混合架构解耦机制特定因果与共享动态，又能首次将大语言模型和视觉语言模型集成到因果发现流程中，利用多模态语义先验正则化因果估计，从而在少样本和复杂时序场景下实现可靠、可解释的因果图恢复。

### Q2: 有哪些相关研究？

**相关研究**

本文的相关工作主要分为三类：

1. **神经格兰杰因果发现方法**：现有方法包括稀疏分量网络、基于预测的图学习、动态变分自编码器以及针对不规则时间序列的方法。这些方法大多依赖纯数值输入，假设数据生成过程同质，难以处理分布偏移和机制变化。CausalMoE 通过引入多模态信息和异质时序模式建模，突破了这一“一刀切”范式。

2. **大规模预训练时间序列模型**：如 GPT4TS 等 LLM 用于时间序列学习，通过组件分解、统计提示、文本重编程和对齐嵌入提升泛化能力。近期基础模型采用 MoE 架构和检索增强改进少样本预测。然而，它们主要优化预测目标，使用同质专家池，不适合异质时序机制下的因果发现。CausalMoE 直接面向格兰杰因果，采用模式路由的异质专家。

3. **非平稳时序分布偏移处理**：相关工作通过域适应、自适应架构和归一化策略应对分布偏移，但主要优化预测误差，可能平滑掉对因果发现有用的机制变化。CausalMoE 则保留时序异质性，将其作为路由信号，使专门专家捕获机制特定的因果机制。

此外，CausalMoE 是首个集成 LLM 和 VLM 的方法，通过文本和视觉先验正则化因果估计，在少样本场景中显著优于传统方法。

### Q3: 论文如何解决这个问题？

CausalMoE通过一个多模态基础框架系统性地解决了Granger因果发现中的分布偏移和动态机制变化问题。其核心设计包含三个关键组件：

首先，**模式路由混合异构专家（MoHE）** 是核心创新。它包含一个**补丁特定模式路由（PSPR）**模块，该模块利用子空间聚类动态识别每个时间序列补丁的潜在模式（如季节性、趋势），并通过正交约束确保子空间区分性。路由模块将补丁分配给四个功能各异的专家：**语义专家**利用冻结LLM从文本提示中提取统计语义；**多模态专家**通过VLM从数值信号和归一化图像中捕捉形状级视觉结构；**时频专家**结合时域和傅里叶域特征建模周期模式；**多尺度时间专家**通过下采样聚合捕捉全局趋势。这种异构设计避免了传统“一刀切”模型的表征纠缠。

其次，**因果感知自注意力（CASA）** 机制替代了传统的时间维度注意力，在变量维度上计算注意力。通过将输入转置为变量列，并使用变量级投影矩阵计算查询、键、值，CASA直接编码变量间的影响关系，并通过近端优化对投影矩阵施加L2正则化，生成稀疏的Granger因果图。

最后，论文首次将**大语言模型（LLM）和视觉语言模型（VLM）** 集成到因果发现中。通过将时间序列补丁转化为包含数据集上下文、历史数据、统计特征和任务指令的文本提示，以及通过双线性插值生成的归一化图像，多模态先验为因果估计提供了正则化约束，尤其在少样本场景下弥补了纯数值方法的不足。整体损失函数结合了预测误差、因果矩阵稀疏性惩罚和模式路由正则化，实现了端到端的优化。

### Q4: 论文做了哪些实验？

论文在五个基准数据集上进行了实验：VAR（线性）、Lorenz-96（非线性）、fMRI、DREAM-3和DREAM-4。实验设置包括全监督和少样本因果发现两种场景。对比方法包括GC、PCMCI、NGC、CR-VAE、CUTS、KANGCI和JRNGC七种基线。评估指标采用AUROC、AUPRC、F1分数和SHD。

主要结果如下：
- 在VAR数据集上，CausalMoE在所有设置下均取得最优，例如在VAR(20,1000,5)上AUROC达0.989，SHD仅4，显著优于次优的JRNGC（AUROC 0.972，SHD 13）。
- 在Lorenz-96数据集上，CausalMoE在混沌条件下（F=20）仍保持强健，如Lorenz(20,1000,10)上AUROC为0.986，SHD为6，远超基线。
- 在fMRI的28个模拟中，CausalMoE在22个场景下取得最佳AUROC，且方差更低。
- 在DREAM-3和DREAM-4基因表达数据集上，CausalMoE全面领先，例如在DREAM-3的Ecoli-1上AUROC达0.845，而JRNGC仅为0.713。这些结果证明了CausalMoE在复杂场景下的优越性和鲁棒性。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：1) 模型依赖大规模预训练数据，在极端小样本场景下泛化能力仍有限；2) 因果图稀疏性通过近端优化实现，但未考虑时滞效应和反馈环路；3) 多模态对齐仅依赖LLM/VLM的静态先验，未能动态适应领域知识迁移。未来可探索：1) 引入因果结构先验（如时序逻辑约束）提升稀疏图的可解释性；2) 设计在线适应机制，使专家路由能捕捉非平稳环境中的概念漂移；3) 结合因果强化学习，让模型主动干预生成反事实样本以验证因果方向；4) 针对工业故障诊断场景，开发跨模态的因果迁移学习框架，利用源域知识辅助目标域少样本因果发现。

### Q6: 总结一下论文的主要内容

CausalMoE提出了一种十亿参数规模的多模态格兰杰因果发现基础模型，旨在解决传统“一刀切”方法无法处理时间序列中分布偏移和动态机制变化的问题。其核心贡献在于：1）设计了模式路由混合异构专家架构，通过动态识别潜在时间模式并将补丁路由至特定领域专家，解耦了机制特异性因果与共享动态；2）首次将大语言模型和视觉语言模型融入因果发现流程，利用文本和视觉先验对齐数值信号，并通过因果感知自注意力机制和近端优化恢复稀疏可解释的因果图。实验表明，CausalMoE在全监督基准上达到新最优性能，并在传统方法失效的小样本场景中展现出强泛化能力，为复杂系统中的可靠因果推断提供了新范式。
