---
title: "ConTex: Reformulating Counterfactual Generation For Time Series Forecasting"
authors:
  - "Jan Voets"
  - "Hasan Tercan"
  - "Tobias Meisen"
  - "Sebastian Baum"
date: "2026-06-16"
arxiv_id: "2606.18049"
arxiv_url: "https://arxiv.org/abs/2606.18049"
pdf_url: "https://arxiv.org/pdf/2606.18049v1"
categories:
  - "cs.LG"
tags:
  - "counterfactual explanation"
  - "time series forecasting"
  - "interpretability"
  - "model-agnostic"
  - "real-time inference"
relevance_score: 6.5
---

# ConTex: Reformulating Counterfactual Generation For Time Series Forecasting

## 原始摘要

Decision-making with deep learning-based time series forecasting requires not only accurate predictions but also actionable insights. However, current architectures do not inherently provide such information. Specifically, guidance is needed on how current conditions must be modified to shift from a predicted outcome to a desired future scenario. Counterfactual explanations provide a natural framework for this task, as they represent minimal input changes that alter the model's prediction, indicating when and how intervention is required. Existing approaches rely on instance-wise optimization, leading to inconsistency across instances, high computational costs, and limited applicability in real-time settings.
  To address these limitations, we reformulate counterfactual generation for time series forecasting as the problem of learning a globally consistent intervention strategy, allowing counterfactuals to be generated through a single shared function. We propose Counterfactual Time Series Explanations (ConTex), a model-agnostic, decomposed architecture comprising a temporal context encoder and a conditional encoder, followed by two heads that capture interventions in terms of temporal relevance and modification strength. This structure overcomes the instability and inconsistency of instance-based approaches by producing targeted, interpretable interventions across time and feature dimensions in a single forward pass, making it suitable for real-time applications.
  Across multiple forecasting architectures and benchmark datasets, ConTex achieves state-of-the-art validity while generating sparse counterfactuals that minimize the number of necessary interventions. Additionally, our approach reduces computational cost by at least 12-36x compared to instance-wise generation and supports real-time inference at approximately 0.007 seconds.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列预测在能源、医疗等高风险决策场景中至关重要，但现有深度学习模型虽预测准确，却缺乏可操作的洞察。例如，电网运营商需要知道如何调整当前负荷以避免未来峰值，医生需要了解如何改变患者当前状态以防止病情恶化。然而，现有解释方法大多是回顾性的（如特征归因），只能解释“为什么预测到某结果”，无法回答“如何改变当前条件以达到期望的未来结果”。现有反事实生成方法存在三个主要不足：一是基于实例的逐样本优化，导致不同样本间干预不一致，且计算成本高，难以实时应用；二是生成的干预在时间和特征维度上缺乏稀疏性和可解释性；三是许多方法使用依赖于输入的动态目标，模糊了实现期望结果的真实难度。本文核心问题是：如何高效、一致地生成时间序列预测的反事实解释，以提供最小、可操作的干预建议，使预测结果转向期望的未来情景。

### Q2: 有哪些相关研究？

在时间序列反事实生成领域，现有研究主要分为三类：基于优化的方法、基于生成式潜空间的方法以及基于因果推理的方法。本文与这些工作的核心区别在于，首次将反事实生成从实例级优化重构为全局一致的干预策略学习问题。

**基于优化的方法**是最主流的方向，如ForecastCF通过迭代扰动输入实现趋势变化，后续工作将其扩展到加密货币预测和多变量场景。这些方法虽能生成反事实，但存在计算成本高（本文实验显示至少慢12-36倍）、实例间不一致等缺陷。本文提出的ConTex通过单次前向传播替代实例级优化，从根本上解决了这些问题。

**生成式潜空间方法**（如基于分位数回归的轨迹生成）侧重于生成符合分布约束的合理未来轨迹，而非最小干预。本文不显式约束分布，而是通过时序上下文编码和最小干预目标隐式正则化，在保持有效性的同时实现更稀疏的干预。

**因果推理方法**将因果机制嵌入预测模型实现“what-if”分析，但这类方法依赖模型内部结构，不适用于固定预测器的后验解释。ConTex采用模型无关架构，可适配任意预训练预测模型。

此外，现有工作主要聚焦分类任务，而本文专门面向时间序列预测场景。与Temporal Fusion Transformer等场景分析方法不同，ConTex明确优化最小输入干预而非探索多情景。

### Q3: 论文如何解决这个问题？

该论文通过将反事实生成重新定义为学习全局一致干预策略的问题，提出了ConTex（Counterfactual Time Series Explanations）架构。其核心方法包括一个模型无关的分解架构，由时间上下文编码器和条件编码器组成，后接两个预测头分别捕获时间相关性和修改强度。

整体框架上，ConTex采用模块化设计：时间编码器（如TCN或BiLSTM）提取输入序列的时序上下文h_x，条件编码器（MLP）将目标条件c（期望轨迹中心、宽度、当前预测和斜率）映射为嵌入。两者通过特征线性调制（FiLM）结合，生成调整后的表示h̃_x，再分别输入掩码头（预测时间掩码m∈[0,1]^T）和强度头（预测修改强度s∈R^{T×D}）。最终干预z=m⊙s加到原始输入x上得到反事实序列x_cf。

关键技术包括：1）复合损失函数，由中心损失（L_center）、有效性损失（L_valid）、邻近损失（L_prox）和稀疏损失（L_sparse）组成，平衡目标满足度和最小干预；2）稀疏性正则化，通过L1邻近损失和掩码二值化正则项促进稀疏、可解释的干预；3）早期停止策略，优先保证有效性和紧凑性。

创新点在于：1）将反事实生成从实例级优化转为全局一致函数学习，单次前向传播即可生成反事实，计算成本降低12-36倍；2）分解架构分离时序上下文提取和目标条件编码，通过FiLM实现条件自适应；3）生成稀疏且时间定位精准的干预，支持实时推理（约0.007秒）。

### Q4: 论文做了哪些实验？

实验在4个公开时间序列数据集（M4、NN5、Tourism、Electricity）上进行，涵盖日度、月度、小时级分辨率，输入长度从42到288不等，预测视界从14到96。对比了4种预测骨干网络（PatchTST、N-HiTS、DLinear、TiDE）和3种反事实生成基线方法：实例级优化的ForecastCF、启发式平移的BaseShift、以及基于最近邻检索的BaseNN。实验采用受控目标族（线性轨迹）并校准难度，使用Validity Ratio和S-AUC评估有效性，Compactness和Proximity评估稀疏性。

主要结果：ConTex在16个数据集-骨干组合中全部优于ForecastCF（Validity Ratio平均提升显著），并在8/16组合中超越检索式BaseNN。平均Validity Ratio从BaseNN的0.891提升至0.910（+2.1%），S-AUC从0.677提升至0.830（+22.6%）。在稀疏性方面，ConTex在14/16组合中取得最佳Compactness。计算效率方面，ConTex推理时间仅约0.007秒，相比实例级方法加速12-36倍。

### Q5: 有什么可以进一步探索的点？

论文的核心局限在于未显式约束反事实的“合理性”，仅通过隐式正则化（如训练数据分布、时间编码）来维持时序连贯性，这可能导致生成的干预在现实中不可行或违反物理规律。未来可引入基于物理模型或领域知识的显式约束（如工业场景中的操作边界），或利用扩散模型等生成式方法直接采样合理反事实。其次，超参数（稀疏度0.05-0.4、邻近度0.4-0.5）仍需数据集级调优，可探索元学习或自适应机制（如基于预测置信度动态调整权重）来提升跨域泛化性。此外，当前架构仅关注单步干预策略，可扩展为多步序贯反事实生成（如逐步调整特征以模拟动态干预过程），并引入因果结构学习来区分可干预变量与不可变变量，避免对因果无关特征的无意义修改。最后，在工业故障诊断中，可结合LLM将反事实干预转化为自然语言操作建议，形成“检测-解释-行动”闭环。

### Q6: 总结一下论文的主要内容

该论文针对时间序列预测中的反事实生成问题，提出了一种名为ConTex的新方法。现有方法依赖逐实例优化，导致不一致性、高计算成本且难以实时应用。核心贡献在于将反事实生成重新定义为学习全局一致的干预策略问题，通过单一共享函数生成反事实。方法上，ConTex采用模型无关的解耦架构，包含时序上下文编码器和条件编码器，以及两个分别捕捉时间相关性和修改强度的输出头，实现单次前向传播即可生成稀疏、可解释的干预。主要结论表明，ConTex在多个预测架构和基准数据集上实现了最先进的有效性，生成的反事实更稀疏、干预更少，且计算成本降低至少12-36倍，支持约0.007秒的实时推理。该工作为时间序列预测提供了高效、可解释的因果洞察，对工业故障诊断等实时决策场景具有重要意义。
