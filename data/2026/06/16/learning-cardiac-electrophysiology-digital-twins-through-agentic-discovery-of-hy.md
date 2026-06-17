---
title: "Learning Cardiac Electrophysiology Digital Twins Through Agentic Discovery of Hybrid Structure"
authors:
  - "Ziqi Zhou"
  - "Yubo Ye"
  - "Sumeet Atul Vadhavka"
  - "Linwei Wang"
  - "Zhiqiang Tao"
date: "2026-06-16"
arxiv_id: "2606.18154"
arxiv_url: "https://arxiv.org/abs/2606.18154"
pdf_url: "https://arxiv.org/pdf/2606.18154v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "LLM/Agent"
  - "可解释时序诊断"
  - "数字孪生"
  - "混合模型发现"
  - "领域知识结构化"
  - "迭代推理-行动循环"
  - "心脏电生理"
relevance_score: 7.5
---

# Learning Cardiac Electrophysiology Digital Twins Through Agentic Discovery of Hybrid Structure

## 原始摘要

Building personalized cardiac electrophysiology (EP) digital twins requires identifying the appropriate model structure for each patient, not merely fitting parameters. Traditional methods rely on experts to manually prescribe hybrid physics-neural architectures, which requires deep domain expertise and does not transfer across patients. Recent works have applied large language models (LLMs) to generate or act as hybrid models. However, despite their promising generalization capacity, these LLM-based methods lack the structural priors needed for stable cardiac simulations. Hence, we propose LEADS, a framework that formulates cardiac EP domain knowledge as a structured action space and utilizes an LLM agent to discover hybrid models. The agent follows an iterative reasoning-and-action loop to select, combine, and refine hybrid models, whilst gradient descent handles parameter fitting. The proposed LEADS designs every candidate model towards physically grounded, interpretable, and numerically stable, while allowing open-ended architectural discovery. We validate LEADS on synthetic data with three ground-truth reaction models and on real cardiac EP data, demonstrating that it outperforms both human-designed hybrid models and other LLM-based hybrid modeling.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

构建个性化心脏电生理数字双胞胎需要为每位患者识别合适的模型结构，而不仅仅是拟合参数。传统方法依赖专家手动设计混合物理-神经网络架构，这需要深厚的领域知识且无法跨患者迁移。近期工作尝试用大语言模型生成或充当混合模型，但缺乏心脏模拟所需的稳定结构先验，导致生成的模型无法产生有效的心脏激活。本文提出LEADS框架，将心脏电生理领域知识形式化为结构化动作空间，利用LLM智能体通过迭代推理-行动循环来发现混合模型。核心问题是：如何自动发现患者特异的、兼具物理可解释性和数值稳定性的混合模型架构，同时避免人工设计的高成本和纯LLM生成的不稳定性。LEADS通过结构化动作空间提供领域先验，智能体在此空间内搜索、组合和优化混合模型，梯度下降负责参数拟合，从而桥接了人工设计范式与LLM自动化范式之间的鸿沟。

### Q2: 有哪些相关研究？

相关研究可分为两类：

1. **混合数字孪生方法**：包括APHYNITY（通过将动力学分解为已知物理项与学习残差）、HyPer-EP（在心脏电生理中应用元学习实现跨组织适应）等。这些方法均需领域专家手动设计混合结构（物理与神经网络的组合方式），无法跨患者迁移。本文LEADS通过LLM智能体自动搜索结构，克服了这一局限。

2. **基于LLM的自动发现方法**：HDTwinGen使用LLM通过进化循环生成和迭代优化模型架构，在简单动力系统上表现良好，但应用于心脏电生理时，无约束的代码生成常导致数值不稳定或生理不合理。CALM-DT则将数字孪生视为上下文学习，但牺牲了数学结构。本文LEADS通过将心脏电生理领域知识形式化为结构化动作空间，约束LLM的搜索过程，确保生成的混合模型具有物理基础、可解释性和数值稳定性。

与上述工作的核心区别在于：LEADS既保留了LLM的泛化能力，又通过领域约束保证了心脏模拟所需的稳定性，实现了开放架构发现与物理有效性的平衡。

### Q3: 论文如何解决这个问题？

LEADS通过将心脏电生理领域知识构建为结构化动作空间，并利用LLM代理进行迭代式混合模型发现来解决该问题。其核心方法是将物理先验与神经架构搜索相结合，而非让LLM自由生成代码。

整体框架采用“观察-思考-行动”循环。首先，代理观察一个维护的档案库，其中包含所有先前候选模型的验证损失和训练曲线。然后，代理生成显式推理轨迹，例如诊断过拟合或识别模型容量限制。最后，代理通过选择反应模型并对扩散模块执行四种操作之一来生成新的混合结构。

主要模块包括两个基础目录：扩散目录（从无参数均值聚合到图注意力网络）和反应目录（如Aliev-Panfilov等已建立的离子模型）。代理的决策是解耦的：为反应模型选择架构，为扩散模块选择操作（选择、精炼、修改或简化）。反应模型具有固定函数形式，仅需选择，其可学习参数通过梯度下降优化。

关键技术在于：1）结构化动作空间确保所有候选模型物理可解释、数值稳定；2）代理通过迭代推理从先前评估中学习，避免穷举搜索；3）解耦设计允许独立探索每个组件。创新点包括：将领域知识编码为受限动作空间而非自由代码生成，以及将LLM的结构决策与梯度下降的参数拟合分离，从而在保持物理合理性的同时实现开放式架构发现。

### Q4: 论文做了哪些实验？

论文在合成数据和真实数据上评估了LEADS框架。合成数据使用三个真实反应模型（AP、RM、MS）生成的32个TMP样本（20/6/6划分），真实数据采用犹他数据集20个EGM记录（12/3/5划分）。对比方法包括：有真实反应模型先验的Physics-Based（拉普拉斯扩散）和人工设计Hybrid-Model（图注意力网络），以及LLM驱动的无约束代码生成器HDTwinGen。所有方法共享相同网格（1119节点）和优化设置，LLM均使用Gemini-2.5-Flash。

主要结果：合成数据上，LEADS平均MSE为26.7（×10⁻³），优于Hybrid-Model的37.6和HDTwinGen的416.3，接近Physics-Based上界0.041。真实数据上，LEADS激活时间误差5.52，优于Hybrid-Model的5.64，略逊于最优Physics-Based的3.42。消融实验显示：仅优化扩散（Diff-Only）在RM/MS上表现相当但AP下降；仅优化反应（React-Only）使RM误差从10.1升至20.4；全神经网络（All-Neural）在所有数据集上性能最差（AP 66.1 vs 49.2）。LEADS能自动识别真实反应模型并生成准确的激活时间图，而HDTwinGen完全失败。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是当前仅使用单一心脏网格几何结构和固定组件目录，限制了模型对患者间解剖差异的泛化能力；二是LLM Agent的推理过程依赖预定义动作空间，可能遗漏某些病理状态下需要的特殊反应项；三是未考虑临床数据中常见的噪声、缺失通道等实际挑战。未来可探索的方向包括：1）引入多几何网格自适应机制，使Agent能根据患者心脏形状动态调整模型结构；2）扩展组件目录至更多离子通道模型和病理反应项，并设计增量式发现策略；3）结合贝叶斯优化或强化学习来平衡Agent探索与参数拟合效率；4）将框架推广至其他生理系统（如呼吸力学、神经电生理），验证其通用性；5）在真实临床场景中集成数据预处理模块，提升对噪声和缺失数据的鲁棒性。此外，可尝试让Agent生成可解释的发现报告，辅助临床医生理解模型选择依据。

### Q6: 总结一下论文的主要内容

这篇论文提出LEADS框架，用于自动化发现个性化心脏电生理数字孪生的混合模型结构。核心问题在于传统方法依赖专家手动设计混合物理-神经网络架构，耗时且无法跨患者迁移，而现有基于大语言模型的方法缺乏心脏模拟所需的结构先验。LEADS通过将心脏电生理领域知识形式化为结构化动作空间，利用LLM代理进行迭代推理-行动循环，选择、组合和优化混合模型，同时用梯度下降处理参数拟合。该方法确保每个候选模型物理可解释、数值稳定，并允许开放式架构发现。在合成数据和真实心脏电生理数据上的实验表明，LEADS优于人工设计的混合模型和其他基于LLM的方法。其核心贡献在于将混合模型设计转化为由代理推理引导的迭代搜索，既避免了人工设计劳动，又克服了无约束LLM方法的失败模式，为个性化心脏数字孪生构建提供了自动化、可解释且稳定的新范式。
