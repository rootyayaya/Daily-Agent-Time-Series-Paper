---
title: "ConceptCF: Concept-based Counterfactuals for the Explainability of Time Series"
authors:
  - "Annemarie Jutte"
  - "Faizan Ahmed"
  - "Jeroen Linssen"
  - "Maurice van Keulen"
date: "2026-07-21"
arxiv_id: "2607.18748"
arxiv_url: "https://arxiv.org/abs/2607.18748"
pdf_url: "https://arxiv.org/pdf/2607.18748v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "可解释时间序列"
  - "反事实解释"
  - "概念基础解释"
  - "时间序列分解"
  - "遗传算法"
  - "预测性维护"
  - "高 stakes 领域"
relevance_score: 7.5
---

# ConceptCF: Concept-based Counterfactuals for the Explainability of Time Series

## 原始摘要

This paper proposes ConceptCF, a method for counterfactual generation that operates on human-interpretable concepts. In high-stakes domains such as healthcare and predictive maintenance, artificial intelligence models can increase efficiency and safety. Explainability is key to ensure these models rely on causal relationships rather than spurious correlations. Counterfactual explanations identify minimal modifications that would change a model's predictions. Existing methods for time series operate on individual points or subsequences without ensuring interpretability of the mutations. ConceptCF instead modifies meaningful concepts. As a result we can provide explanations in terms of these concepts, for example ``the model's prediction would be `Sit' instead of `Walk' if you increase the scale of the movement''. In this paper, the concepts are constructed through time series decomposition, resulting in concepts such as scale, and frequency bands. Counterfactuals are generated using a genetic algorithm that optimizes the concept mutations. Evaluation against five state-of-the-art approaches demonstrates that ConceptCF consistently achieves top-tier performance across validity, confidence, proximity, sparsity and plausibility metrics.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在高风险领域（如医疗和预测性维护）中，AI模型虽能提升效率与安全性，但其黑箱特性可能导致依赖虚假相关性而非因果关系，因此可解释性至关重要。反事实解释通过识别能改变模型预测的最小修改来提供解释，但现有时间序列反事实方法存在不足：它们通常修改单个点或子序列，无法保证修改的语义可解释性。例如，修改一个点可能破坏序列的整体语义，而修改子序列虽能保留局部上下文，却难以捕捉尺度、周期性等全局特征，且修改后的属性往往不明确，导致解释难以被人类理解。

本文旨在解决上述问题，提出ConceptCF方法，核心创新在于将反事实生成从原始信号层面提升至人类可理解的概念层面。通过时间序列分解（如傅里叶、小波或基于人类认知的分解）提取尺度、频带等高层次概念，并利用遗传算法优化这些概念的突变，从而生成具有内在可解释性的反事实。例如，解释可表述为“若增加运动尺度，模型预测将从‘走路’变为‘坐着’”。该方法旨在确保反事实的有效性、置信度、接近性、稀疏性和合理性，同时提供比现有方法更直观的因果解释。

### Q2: 有哪些相关研究？

在时间序列反事实解释领域，相关研究主要分为三类。**方法类**中，梯度法（如Wachter等）和模型无关法（如遗传算法）是基础，但直接应用于时间序列会破坏时序依赖。现有改进包括：Native Guide通过贪婪替换子序列，Sub-SpaCE用遗传算法优化子序列替换；LatentCF++和Glacier在自编码器隐空间扰动以保持分布；TSEvo支持位置和频率突变。本文与TSEvo最接近，但将其频率操作重新定义为概念，并扩展了尺度等其他概念，且专注于概念级解释。**概念类XAI**中，TCAV、CaCE、ConceptSHAP提供概念归因，原型网络和概念瓶颈模型（CBM）是内在可解释的，但归因不解释决策原因，本文用反事实填补此空白。**应用类**中，X-CHAR基于CBM将概念视为有意义的子序列，而本文考虑更广泛的高层特征（如尺度、频带）。本文通过时间序列分解构建概念，用遗传算法优化概念突变，在有效性、置信度、邻近性、稀疏性和合理性指标上优于五种SOTA方法。

### Q3: 论文如何解决这个问题？

ConceptCF通过三个核心设计解决时间序列反事实解释的可解释性问题：**概念构建模块**、**多目标优化框架**和**遗传算法求解器**。

首先，**概念构建模块**利用三种可逆分解算法将原始时间序列转化为人类可理解的概念集。离散傅里叶变换将信号分解为频率带（如低频、高频），离散小波变换生成近似分量和细节分量，而**人本分解**则提取趋势、偏置、尺度等标量概念以及低频、方差、高频等序列概念。这些分解均满足可逆性，确保修改概念后能重构有效信号。

其次，**多目标优化框架**将反事实生成定义为约束优化问题。目标函数包含四个指标：置信度（最大化目标类概率）、邻近性（L1范数衡量点级差异）、稀疏性（修改概念的比例）和合理性（自编码器重建误差增量）。有效性作为硬约束，要求反事实必须改变原始预测类别。通过加权求和将多目标转化为单目标，并支持定向生成指定类别的反事实。

最后，**遗传算法求解器**通过进化策略优化概念集。初始种群基于最近异类邻居构建，保证至少一个有效解。变异操作针对标量概念（高斯噪声扰动）和序列概念（从训练数据中采样替换）分别设计，并引入重置概率促进稀疏性。通过锦标赛选择、单点交叉和精英保留机制迭代优化，最终输出满足所有约束且可解释的反事实样本。

创新点在于：1）将反事实解释从点/子序列层面提升到概念层面，使解释更符合人类认知；2）提出人本分解方法，生成具有语义含义的概念（如“运动幅度”）；3）通过可逆分解保证概念修改后信号的可重构性，确保反事实的物理可行性。

### Q4: 论文做了哪些实验？

论文围绕ConceptCF方法进行了全面的实验评估。实验设置上，使用PyTorch 2.8在配备NVIDIA TITAN V GPU的Ubuntu系统上运行。数据集包括MotionSenseHAR（MS-HAR，来自UEA档案）以及CBF、Coffee、ECG200、GunPoint四个UCR档案数据集，所有数据均归一化处理。黑盒模型采用全卷积神经网络（FCN）。对比方法包括Wachter、Native Guide、TSEvo、Glacier和Sub-SpaCE五种基线。评估指标涵盖有效性（Validity）、置信度（Confidence）、邻近性（Proximity）、稀疏性（Sparsity）和合理性（Plausibility）。主要结果显示：ConceptCF在所有数据集上均达到100%有效性；在稀疏性上排名第一（例如MS-HAR上稀疏度0.288，远优于Wachter的1.000）；在邻近性上也获得最高排名（MS-HAR上RMSE 0.189，优于多数基线）；置信度排名第二（MS-HAR上0.933），仅次于Glacier；合理性排名第二（MS-HAR上0.721），同样仅次于Glacier。此外，还进行了敏感性分析，通过独立调整目标权重（α_conf、α_prox、α_s、α_pl）验证了各指标的可调性，表明方法可根据用户需求灵活配置。

### Q5: 有什么可以进一步探索的点？

ConceptCF在概念构建上依赖时间序列分解（如DFT），这限制了其捕捉局部动态模式的能力。未来可探索**混合概念表示**，将全局分解特征与局部子序列模式（如shapelets）结合，通过注意力机制动态融合，提升对异常片段的解释力。其次，当前遗传算法的优化目标未显式考虑因果约束，可能导致反事实修改违反物理规律。可引入**结构因果模型**，在概念空间中学习因果图，确保反事实扰动仅作用于可干预变量。此外，**无监督概念发现**是重要方向，例如利用变分自编码器从原始信号中解耦出独立可解释因子，避免人工定义概念的偏差。最后，现有评估指标（如稀疏性）无法衡量用户实际理解度，需设计**人机交互实验**，通过任务完成时间、错误率等量化概念级解释的认知负荷，并开发可视化界面支持用户迭代修改概念阈值。

### Q6: 总结一下论文的主要内容

ConceptCF提出了一种基于人类可解释概念的时间序列反事实生成方法。现有方法在时间序列反事实解释中通常修改单个点或子序列，导致突变缺乏可解释性。ConceptCF通过时间序列分解（如傅里叶、小波或人为定义）提取高层概念（如尺度、频带），并利用遗传算法优化这些概念的突变，生成反事实样本。该方法的核心贡献在于将反事实解释从原始特征空间提升到概念层面，例如“若增加运动幅度，模型预测将从‘行走’变为‘坐下’”。实验表明，ConceptCF在有效性、置信度、接近性、稀疏性和合理性五个指标上均达到顶尖水平，与五种基线方法相比具有竞争力。该工作为高风险领域（如医疗、工业）中时间序列模型的可解释性提供了新工具，确保模型依赖因果关系而非虚假相关，同时通过概念级解释增强了人类理解能力。未来可探索局部模式或自相关等概念类型，并开展用户评估研究。
