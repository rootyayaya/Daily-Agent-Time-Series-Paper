---
title: "Agentic Anomaly Detection with ORCA-Style Dynamic Inductive Bias Adaptation in Multimodal Wearable Time Series Data"
authors:
  - "Anushka Roy"
  - "Jyotirmoy Singh"
  - "Shreea Bose"
  - "Chittaranjan Hota"
date: "2026-08-09"
arxiv_id: "2608.08859"
arxiv_url: "https://arxiv.org/abs/2608.08859"
pdf_url: "https://arxiv.org/pdf/2608.08859v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Anomaly Detection"
  - "Multivariate Time Series"
  - "Adaptive Inductive Bias"
  - "Temporal Receptive Field"
  - "Wearable Sensors"
  - "Physiological Signals"
  - "Inference-time Adaptation"
  - "Resource-constrained"
  - "MIMIC-IV"
relevance_score: 7.5
---

# Agentic Anomaly Detection with ORCA-Style Dynamic Inductive Bias Adaptation in Multimodal Wearable Time Series Data

## 原始摘要

Wireless Body Area Networks (WBANs) generate multivariate physiological time series that are highly nonstationary and must often be processed under strict computational and memory constraints. A critical yet underexplored challenge in this setting is selecting an appropriate temporal receptive field, which serves as a strong inductive bias for anomaly detection models. Existing approaches typically rely on fixed temporal contexts, which can perform inconsistently across heterogeneous signal regimes and require dataset-specific tuning. We propose ORCA, an agentically controlled anomaly detection framework that dynamically adapts the temporal receptive field at inference time based on lightweight signal statistics. Rather than introducing additional trainable parameters or learned policies, ORCA employs a supervisory controller that autonomously selects among discrete temporal contexts, enabling state-dependent inductive bias adaptation without retraining. Across a custom WBAN dataset, ORCA achieves performance comparable to the strongest fixed-context baselines (AUROC = 0.99) while eliminating the need to tune temporal horizons in advance. We further evaluate ORCA on MIMIC-IV as a challenging out-of-distribution benchmark, observing conservative generalization behavior without performance collapse under heterogeneous clinical conditions. These results highlight adaptive temporal inductive bias control as a practical and robust design principle for anomaly detection in resource-constrained, nonstationary physiological time series.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

无线体域网（WBAN）中的多模态生理时间序列具有高度非平稳性和强上下文依赖性，异常通常表现为依赖于周围时空上下文的“情境异常”。然而，现有异常检测方法大多依赖固定时间感受野，即预设的滑动窗口或注意力跨度。这种静态归纳偏置在异构生理状态（如静息、活动、睡眠）下表现不一致：短窗口能捕捉突发尖峰但漏检缓慢演变的异常，长窗口虽能覆盖慢变模式却稀释了瞬态临床事件。尽管注意力架构可学习时间权重，但仍受限于固定注意力跨度，且二次复杂度、高内存占用使其难以部署于资源受限的可穿戴设备。轻量级替代方案同样预设时间范围，隐含假设时间依赖的平稳性，缺乏对动态信号状态的适应性。

本文核心问题是：如何在严格计算与内存约束下，动态选择每个输入窗口的时间感受野，以匹配非平稳生理信号的时变特性？为此提出ORCA框架，通过一个不引入额外可训练参数的监督智能体，基于轻量级信号统计量在推理时自主切换离散时间上下文，实现状态依赖的归纳偏置自适应，无需重训练即可达到与最强固定上下文基线相当的性能（AUROC=0.99），并在MIMIC-IV上展现保守泛化能力，验证了自适应时间控制作为资源受限场景下鲁棒设计原则的有效性。

### Q2: 有哪些相关研究？

相关研究主要围绕四个方向展开。**方法类**上，传统WBAN异常检测依赖监督学习与信号处理，如ADSBAN框架比较逻辑回归与集成分类器；深度学习方面，ConvLSTM捕捉时空依赖，卷积Transformer混合模型兼顾局部与长程模式，Temporal Fusion Transformer强调可解释性，但均采用固定感受野。**架构类**中，Transformer虽擅长长程建模但二次复杂度受限，TCN提供并行与有界感受野却依赖静态时间偏置，近期递归网络与ConSmax等硬件感知优化关注效率，但未涉及动态上下文调整。**应用类**研究聚焦边缘-云协同部署，如边缘轻量CNN配合云端预测，以及基于CSI的异常检测，但假设架构固定。**智能体类**工作将agentic AI用于边缘编排与资源感知控制，或通过跨层框架实现分布式检测，但agency多作为外部规划层。本文与上述工作的核心区别在于，ORCA将智能体决策内化于时序建模过程，通过轻量统计量在推理时动态选择离散时间上下文，无需额外参数或重训练，首次实现非平稳多模态信号下感受野的自适应调节，在保持高AUROC的同时消除人工调参需求，并展现出跨域保守泛化能力。

### Q3: 论文如何解决这个问题？

ORCA通过引入一个轻量级的“监督智能体”来动态调整时间感受野，从而解决固定时间上下文在非平稳生理信号中表现不一致的问题。其核心架构由三部分组成：最小化门控循环单元（MinGRU）骨干网络、常数归一化注意力机制、以及一个基于信号统计量的智能体控制器。

在整体框架上，ORCA采用滑动窗口处理多元传感器流。每个时间步，系统先计算窗口内的轻量统计特征（如方差、自相关），智能体根据这些统计量从离散的候选集合中选择一个感受野k。这一设计基于生理信号的局部平稳性假设：稳定期适合长依赖，突变期需要短上下文。随后，MinGRU以极简方式更新隐状态（省略重置门和递归仿射变换），堆叠的隐状态通过注意力机制建模时序关系。

关键技术在于常数归一化注意力（ConSmax），它用可学习的标量β和γ替代softmax的序列级归一化，使计算可完全并行化。智能体选择的感受野k通过截断相对位置偏置矩阵B^(k)注入注意力分数，从而限制注意力只关注动态选定的时间邻域，无需重算全窗口权重。最终，上下文感知表示经线性层映射为异常分数。

创新点包括：无需额外训练参数或学习策略即可实现推理时自适应；通过离散感受野选择实现状态依赖的归纳偏置调整；以及将可解释性模块（TFT）与实时检测管线解耦。实验表明，ORCA在自定义WBAN数据集上达到AUROC=0.99，与最优固定上下文基线持平，同时免除了预先调参，并在MIMIC-IV上展现出保守泛化能力。

### Q4: 论文做了哪些实验？

论文在自建WBAN数据集和MIMIC-IV临床基准上评估了ORCA框架。实验设置采用窗口长度L=15、步长为1的滑动窗口，输入特征仅用训练集统计量标准化，标签分配给窗口末时间步。对比方法包括固定感受野k∈{1,3,5}的相同架构基线、轻量循环模型及固定时间视野的注意力模型，ORCA的监督智能体仅在推理时运行且不引入额外可训练参数。

主要结果：在WBAN数据集上，ORCA自适应k达到AUROC=0.9993、AUPRC=0.9928，与最优固定k=3基线（0.9994/0.9932）几乎持平；在MIMIC-IV上，ORCA取得AUROC=0.9983、AUPRC=0.9845，略优于固定k=3基线（0.9982/0.9843）。消融实验显示，随机策略、仅波动性或仅相关性线索的智能体均无法产生系统性增益，而完整ORCA能动态切换短、中、长感受野——异常窗口中选择k=5的比例达73.06%，正常窗口则以k=1为主（48.21%）。此外，ORCA通过常数归一化注意力将参数量较全Transformer降低6倍以上，在CPU环境下保持低推理延迟，验证了边缘部署可行性。

### Q5: 有什么可以进一步探索的点？

ORCA在动态感受野控制上展现了高效性，但其局限也指明了几个值得深挖的方向。首先，其监督代理依赖确定性启发式规则，难以捕捉复杂的隐性状态转换，未来可引入轻量级在线学习策略（如元学习或上下文Bandit）来学习决策边界，同时保持低计算开销。其次，固定滑动窗口限制了跨窗口的长期依赖建模，可探索基于事件触发或状态感知的变长窗口机制，或结合层次化记忆模块来扩展时间范围。第三，当前二元分类框架过于粗糙，未来可扩展为多标签或回归式异常严重度评分，并细化到事件级定位（如子序列分割），以提升临床可操作性。此外，跨域泛化仍是痛点，可设计域自适应正则化或持续学习框架，使代理在部署中根据新数据分布动态调整策略。最后，将ORCA与可解释性模块更深度融合，例如让代理决策过程本身可被解释，将有助于建立用户信任并支持临床决策。

### Q6: 总结一下论文的主要内容

ORCA提出了一种面向非平稳多模态生理时间序列的智能体异常检测框架，核心创新在于动态调整时间感受野这一归纳偏置。现有方法依赖固定时间上下文，在不同信号状态下性能不稳定且需数据集级调参。ORCA通过轻量级统计探针，在推理时由监督控制器自主选择离散时间上下文，无需额外训练参数或学习策略。在自定义WBAN数据集上，ORCA达到与最优固定上下文基线相当的AUROC（0.99），同时免去预先调整时间窗口的需求；在MIMIC-IV跨域基准上表现出保守泛化，无性能崩溃。该方法结合最小循环骨干、常数归一化注意力和事后Temporal Fusion Transformer解释模块，在严格计算与内存约束下实现效率、适应性与可解释性的平衡，为资源受限的可穿戴监测系统提供了实用的设计原则。
