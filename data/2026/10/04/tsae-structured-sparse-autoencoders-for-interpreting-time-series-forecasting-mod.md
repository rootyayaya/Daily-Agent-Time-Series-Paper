---
title: "TSAE: Structured Sparse Autoencoders for Interpreting Time-Series Forecasting Models"
authors:
  - "Baoxi Liu"
  - "Yi Xie"
date: "2026-10-04"
arxiv_id: "2610.04925"
arxiv_url: "https://arxiv.org/abs/2610.04925"
pdf_url: "https://arxiv.org/pdf/2610.04925v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "可解释时序预测"
  - "稀疏自编码器"
  - "时序表示解耦"
  - "特征归因"
  - "预测一致性微调"
  - "时序语义评估协议"
  - "PatchTST"
  - "工业传感器解释"
relevance_score: 7.5
---

# TSAE: Structured Sparse Autoencoders for Interpreting Time-Series Forecasting Models

## 原始摘要

Time-series forecasting informs critical decisions in energy dispatch, industrial operations, and environmental monitoring; understanding the patterns models rely on is essential for assessing reliability and identifying failures. Input attribution identifies important variables and time segments but offers limited insight into internal features, while standard sparse autoencoder (SAE) objectives do not directly constrain cross-variable structure or temporal continuity. We introduce TSAE, a structured sparse autoencoder for forecasting representations that decomposes hidden states into individually inspectable features. TSAE organizes cross-variable structure through shared and variable-routed private dictionaries, separates feature detection from magnitude estimation with gated encoding, and constrains neighboring sparse-code changes according to raw-segment similarity. These mechanisms support analysis of variable context, activation strength, and temporal evolution. Forecast-consistency fine-tuning further improves preservation of the frozen forecaster's outputs. The accompanying TSEVAL protocol separately audits fidelity, feature coherence, and physical calibration to ground feature interpretation. In three-seed experiments with frozen PatchTST on ETTh1, ETTh2, and ETTm1, TSAE achieves the lowest hidden-state reconstruction error, normalized forecast-reconstruction error (NFRE), and feature transition rate among five SAEs at comparable per-token activity. NFRE decreases by 4.3-26.4% relative to the next-best mean. Dataset-dependent tradeoffs in selectivity, physical correlation, and calibration show that fidelity and temporal-stability gains require independent semantic validation to support feature interpretation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决时间序列预测模型内部表征难以解释的问题。在能源调度、工业运营和环境监测等高风险场景中，预测模型的可靠性至关重要，但现有可解释性方法大多停留在输入层面，如显著性图、遮挡分析、Shapley值和反事实解释，只能将预测归因到变量、时间步或扰动子序列，无法探测预测骨干网络学到的潜在特征，因而难以判断模型是否编码了语义连贯、物理合理且与预测相关的时序模式。近年来，稀疏自编码器（SAE）被用于解释大模型隐藏表征，可将隐藏状态分解为稀疏特征方向的线性组合，但标准SAE目标并未针对时间序列结构设计：它不直接约束跨变量结构或时间连续性，稀疏惩罚还可能压缩激活幅度，且平坦的重建-稀疏目标无法保证特征在变量间一致、与信号 motif 校准或对预测敏感。因此，本文提出TSAE，一种面向时间序列预测表征的结构化稀疏自编码器，通过共享与变量路由的私有字典组织跨变量结构，用门控编码分离特征检测与幅度估计，并依据原始片段相似性约束相邻稀疏码变化，同时提出TSEval协议从重建保真、特征纯度、物理校准和预测敏感性等维度审计稀疏特征。

### Q2: 有哪些相关研究？

相关研究主要分为三类。方法类方面，输入级归因方法（如显著性图、遮挡分析、Shapley值、动态掩码和反事实解释）将预测归因于变量、时间步或扰动子序列，但无法探测预测骨干学到的潜在特征；稀疏自编码器（SAE）通过将隐藏状态分解为稀疏线性组合来识别内部概念，但标准SAE目标未直接约束跨变量结构或时间连续性。应用类方面，SAE已在语言模型可解释性中广泛使用，其重建保真度、稀疏度和top激活示例等实践较为成熟，但在时间序列领域应用不足。评测类方面，现有SAE评估多依赖重建损失和top激活示例，缺乏对特征跨变量一致性、物理校准和预测相关性的系统审计。本文与上述工作的区别在于：提出TSAE，通过共享/变量路由私有字典、门控编码和时间连续性约束，显式建模多变量时间序列结构；并提出TSEval协议，从保真度、特征纯度、物理校准和预测干预敏感性等多轴评估稀疏特征，弥补了标准SAE在时间序列可解释性中的不足。

### Q3: 论文如何解决这个问题？

TSAE 的核心思路是在预测模型隐藏表示层插入一个结构化稀疏自编码器，将隐藏 token 分解为可单独检查的稀疏特征，而非直接重建原始输入。整体框架为：原始多元序列先经冻结的预测骨干（如 PatchTST）编码为隐藏 token，TSAE 再学习过完备稀疏码并重建该隐藏 token。

方法包含三个关键机制。第一，共享/私有变量路由：每个 token 同时用跨变量共享字典和按变量索引选择的私有字典重建，即 ĥ = D^sh z^sh + D^priv_c z^priv + b，从而让跨变量重复出现的时序模式进入共享特征，变量条件残差进入紧凑私有特征。第二，门控检测与幅度分离：编码器对每个特征分别计算门控 g(h) 和幅度 m(h)，激活为 z = 1[g(h)>0] ⊙ m(h)，稀疏惩罚施加于门控而非幅度，避免幅度收缩破坏特征强度与物理量（如斜率、波动率）的对应。第三，条件时序连续性：对同一变量相邻有序 token 的稀疏码施加加权图全变差正则，权重由原始片段相似度的 RBF 核决定，原始片段相似时强惩罚特征切换以抑制闪烁，出现尖峰或状态切换时允许变化。

训练分两阶段：第一阶段联合优化重建、稀疏、门控辅助、时序连续及平衡/正交辅助损失；第二阶段进行预测一致性微调，仅更新 TSAE 参数，加入 f(ĥ) 与 f(h) 的归一化 MSE，使重建表示保留冻结骨干的预测输出。配套 TSEVAL 协议分别审计保真度、特征一致性与物理校准。创新点在于将变量结构、幅度保持和时序结构作为归纳偏置显式注入 SAE，而非依赖平坦共享字典。

### Q4: 论文做了哪些实验？

论文在冻结的PatchTST patch-token表示上进行实验，核心基准在ETTh1、ETTh2、ETTm1上对比TSAE与L1、Gated、TopK、JumpReLU四种SAE，编码宽度2048，采用验证集选点、三种子测试协议，Weather作为外部有效性扩展，iTransformer和DLinear作为跨骨干迁移检查。评估指标包括重构MSE、NFRE、平均活跃特征数、死特征率、转移率、选择性AUROC、物理相关性和校准误差。主要结果：TSAE在四个数据集上均取得最低重构误差和NFRE，ETT三集NFRE相对次优均值分别降低4.3%、26.4%、9.1%，Weather降低11.3%；重构MSE降低1.0%–24.4%，转移率也最低。活动-保真度扫描显示优势不限于单一活跃水平。跨骨干中，iTransformer上TSAE同样最优，但DLinear上Gated SAE更优。消融显示移除路由使转移率上升39%–69%，移除门控使活跃特征降至46–108并恶化重构，时间连续性项影响较小。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于验证范围较窄：仅在PatchTST和三个ETT数据集上评估，未验证跨架构（如iTransformer、TimesNet）与高维真实工业数据的迁移性；同时TSAE并非在所有可解释性指标上占优，JumpReLU或TopK在选择性、物理相关性上可能更强，说明保真度与语义可解释性之间存在权衡。物理motif为手工设计，难以覆盖领域语义；FIS干预也只是敏感性分析而非完整因果归因。未来可探索：一是将结构化字典与门控机制扩展到非patch、无序token表示，并设计自适应时间图；二是引入领域知识或LLM先验自动发现语义特征，替代手工motif；三是建立端到端的因果干预与反事实评估协议，把特征解释与预测失败诊断闭环；四是研究多变量路由字典在跨变量因果结构发现中的潜力，并探索在异常检测、根因定位等下游任务中的实际增益。

### Q6: 总结一下论文的主要内容

论文针对时间序列预测模型内部表示难以解释的问题，提出结构化稀疏自编码器TSAE。其核心思路是将隐藏状态分解为可单独检查的特征：通过共享字典与变量路由私有字典组织跨变量结构，利用门控编码分离特征检测与幅度估计，并依据原始片段相似性约束相邻稀疏编码的变化，从而支持对变量上下文、激活强度和时间演化的分析。配套的TSEVAL协议分别审计保真度、特征一致性与物理校准。在ETTh1、ETTh2和ETTm1上以冻结PatchTST进行三随机种子实验，TSAE在五种SAE中取得最低的隐藏状态重构误差、归一化预测重构误差（NFRE）和特征转移率，NFRE较次优方法降低4.3%–26.4%。结论表明，TSAE在提升预测相关隐藏信息保真度的同时，也在选择性、物理相关性和校准方面存在权衡，需独立语义验证支撑特征解释。
