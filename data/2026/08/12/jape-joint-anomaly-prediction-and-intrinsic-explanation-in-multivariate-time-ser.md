---
title: "JAPE: Joint Anomaly Prediction and Intrinsic Explanation in Multivariate Time Series"
authors:
  - "Yian Wei"
  - "Yuanyuan Yao"
  - "Lu Chen"
  - "Xiangmin Zhou"
  - "Tianyi Li"
date: "2026-08-12"
arxiv_id: "2608.11801"
arxiv_url: "https://arxiv.org/abs/2608.11801"
pdf_url: "https://arxiv.org/pdf/2608.11801v1"
categories:
  - "cs.LG"
tags:
  - "Multivariate Time Series"
  - "Anomaly Prediction"
  - "Explainability"
  - "Dependency Structure Modeling"
  - "Spatio-Temporal Representation"
  - "Variable-level Explanation"
  - "Graph-based Anomaly Detection"
relevance_score: 7.5
---

# JAPE: Joint Anomaly Prediction and Intrinsic Explanation in Multivariate Time Series

## 原始摘要

Multivariate time-series anomaly prediction aims to identify whether and when anomalies will occur over a future horizon from historical observations. Existing methods primarily characterize anomalies as deviations in future numerical values, which may overlook subtle dependency changes induced by weak anomaly precursors and provide no native variable-level explanation together with the alert. To bridge these gaps, we propose JAPE, a Joint Anomaly Prediction and Explanation framework that lifts anomaly prediction from numerical-deviation modeling to dependency-structure modeling. JAPE is the first anomaly prediction framework to explicitly model evolving dependency structures for both point-wise alerting and native variable-level explanation. Specifically, JAPE (i) proposes a Decoupled Spatio-Temporal Representation (DSTR) backbone that decouples temporal and spatial modeling and captures lag-aware dependencies via learnable lag aggregation, thereby perceiving structural precursors before numerical deviations emerge; (ii) designs a dual-view alerting mechanism that fuses numerical forecasts with evolving dependency graphs for point-wise anomaly prediction, capturing structural evidence even under subtle numerical deviations; and (iii) presents Native Predictive Explanation (NPE), which directly reuses the predicted dependency graphs to rank variables by structural deviations without additional models or training. Extensive experiments on five real-world benchmarks across three prediction horizons demonstrate that JAPE improves average F1 and AUC-PR by 19.7% and 41.3%, respectively, while improving explainability with 26.6% gain in MRR.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

多变量时间序列异常预测旨在从历史观测中提前判断未来是否发生异常及发生时间。然而，现有方法主要存在三大局限：其一，主流方法将异常建模为未来数值的偏差，但弱异常前兆往往被主导的正常模式掩盖，导致检测延迟；其二，异常传播过程中源变量与响应变量常呈现相似数值偏差，数值中心方法难以区分异常源头，判别力受限；其三，现有方法缺乏内在的可解释性，无法在告警时直接给出变量级解释，需依赖事后分析。

为突破上述瓶颈，本文提出JAPE框架，首次将异常预测从数值偏差建模提升至依赖结构建模层面。其核心创新包括：解耦时空表示骨干网络，通过可学习的滞后聚合捕获演化中的依赖关系，从而在数值偏差显现前感知结构前兆；双视角告警机制融合数值预测与动态依赖图，在数值变化微弱时仍能捕捉结构证据；原生预测解释机制直接复用预测阶段生成的依赖图，无需额外训练即可对变量进行结构偏差排序。实验表明，JAPE在五个真实基准上平均F1提升19.7%，AUC-PR提升41.3%，解释MRR提升26.6%。

### Q2: 有哪些相关研究？

相关研究主要围绕多变量时间序列异常预测展开，可分为三类。**方法类**中，早期工作如PoA检测异常前兆，TranAP结合预测与重建误差进行无监督异常预测，FCM利用预测未来上下文增强弱前兆，A2P通过注入合成伪异常进行自监督学习，F2A则采用监督方式联合预测与异常损失并引入检索增强。这些方法均将异常视为未来数值偏差，与JAPE将异常建模为依赖结构演变的思路不同。**应用类**研究聚焦分布式系统监控与故障诊断，传统异常检测仅在故障发生后提供被动告警，而JAPE强调主动预测与原生变量级解释。**评测类**方面，现有工作多采用点级F1和AUC-PR评估，JAPE在五个基准数据集上验证了性能提升。与上述工作的核心区别在于：JAPE首次显式建模演化依赖图，通过解耦时空表示捕捉数值偏差出现前的结构前兆，并利用双视图告警机制融合数值与结构证据，同时以零额外成本提供原生预测解释，克服了现有方法延迟检测、判别力不足和缺乏内在可解释性的局限。

### Q3: 论文如何解决这个问题？

JAPE通过将异常预测从数值偏差建模提升到依赖结构建模来解决现有方法的不足。其核心架构包含三个关键组件：

**DSTR骨干网络**采用解耦的时空建模方式。空间轴通过可学习的滞后感知非对称图构建机制，利用指数衰减权重聚合前K个patch的投影，并设计方向对比分数来区分变量间的有向依赖关系，从而捕捉数值偏差出现前的结构前兆。时间轴则独立建模每个变量的时序演化，避免主导时序模式掩盖弱结构变化。未来导向分支将依赖建模扩展到预测区间，生成未来依赖图。

**双视图告警机制**融合数值预测和结构依赖两个视角。它将动态依赖图压缩为13维结构描述符（包括切片级统计如熵、Top-k共享度、方向不平衡，以及段级统计如入/出度变化、图能量），通过交叉注意力融合数值token和结构token，最终用Transformer编码器输出逐点异常概率。

**原生预测解释（NPE）**直接复用预测阶段生成的依赖图，计算图偏差分数（GDS）来衡量异常段与正常参考图的依赖结构偏差，无需额外模型即可实现变量级解释，并通过多跳传播捕捉依赖变化的级联效应。

创新点在于：首次显式建模演化依赖结构用于异常预测和原生解释；滞后感知有向图构建能感知弱前兆；双视图融合机制在数值偏差微弱时仍能捕捉结构证据；NPE实现了零额外成本的变量级解释。

### Q4: 论文做了哪些实验？

论文在五个公开多元时间序列基准数据集（SMD、WADI、MSL、PSM、EXATHLON）上进行了异常预测实验，设置历史窗口长度L=200，预测长度L_out∈{50,100,200}三种预测跨度。对比方法涵盖三类基线：无监督方法（FCM、RED-F）、自监督方法（A2P）以及基于PatchTST和iTransformer的预测-检测流水线（分别搭配AT和CAD检测器），还包括A2P的监督变体A2P-Sup。评估指标为F1和AUC-PR，采用严格逐点匹配。

主要结果显示，JAPE在所有设置下均取得最佳平均性能，平均F1达62.9、AUC-PR达70.9，较最强基线分别提升19.7%（10.4个F1点）和41.3%（20.7个AUC-PR点）。在MSL数据集上优势尤为显著，JAPE的AUC-PR达68.1，而预测类方法最高仅31.8。AUC-PR的提升幅度普遍大于F1，表明JAPE学习到更具判别性的异常评分空间。

此外，论文在SMD和WADI数据集上评估了变量级解释性能，对比Random、Pred-Dev、GRAD和CF四种基线。JAPE在SMD上将HR@1从0.235提升至0.333、HR@3从0.407提升至0.505、MRR从0.364提升至0.461，相对提升26.6%；在WADI上HR@3和HR@5也均有提升。

### Q5: 有什么可以进一步探索的点？

JAPE在异常预测和解释方面取得了显著进展，但仍存在若干可探索的方向。首先，其依赖结构建模主要基于静态图或固定时序窗口，未来可引入动态图神经网络或自适应结构学习，以捕捉更复杂、非平稳的依赖演化模式。其次，NPE解释仅依赖预测的依赖图进行变量排序，缺乏因果层面的验证，可结合因果推断或干预方法，区分相关性与因果性，提升解释的可靠性。此外，当前方法在极长预测视界（如L_out>200）下的性能衰减明显，可探索多尺度预测或层次化结构建模以增强长期依赖捕获能力。最后，JAPE的监督训练依赖异常标签，在标签稀缺或存在噪声的工业场景中可能受限，未来可研究半监督或自监督预训练策略，利用大量未标注数据增强模型泛化性，并进一步验证其在跨域迁移中的鲁棒性。

### Q6: 总结一下论文的主要内容

JAPE框架针对多元时间序列异常预测中依赖结构建模缺失的问题，提出将异常预测从数值偏差建模提升至依赖结构建模。其核心包含三部分：解耦时空表示骨干网络，通过可学习滞后聚合捕获变量间演化中的领先-滞后依赖，在数值偏差显现前感知结构前兆；双视角告警机制，融合数值预测与动态依赖图，在数值变化微弱时仍能捕捉结构证据；原生预测解释模块，直接复用预测得到的依赖图，基于图偏差分数对变量排序，无需额外训练即可提供变量级解释。在五个真实基准数据集、三个预测时域上的实验表明，JAPE在F1和AUC-PR上分别平均提升19.7%和41.3%，解释MRR提升26.6%，验证了依赖结构建模对早期告警和内在可解释性的双重价值。
