---
title: "Temporal Island Sparse Autoencoders for Interpreting Clinical Time-Series Models"
authors:
  - "Muhan Yeo"
  - "Bong Gyun Kang"
  - "HyunGi Kim"
  - "Sungroh Yoon"
date: "2026-11-02"
arxiv_id: "2611.03420"
arxiv_url: "https://arxiv.org/abs/2611.03420"
pdf_url: "https://arxiv.org/pdf/2611.03420v1"
categories:
  - "cs.LG"
tags:
  - "可解释时序诊断"
  - "临床时间序列"
  - "稀疏自编码器"
  - "概念字典"
  - "时序归因"
  - "表示学习"
  - "MIMIC-III"
  - "MIMIC-IV"
relevance_score: 6.5
---

# Temporal Island Sparse Autoencoders for Interpreting Clinical Time-Series Models

## 原始摘要

Deep learning models for electronic health records achieve strong predictive performance but provide little insight into what clinical concepts they represent internally. Post-hoc attribution methods produce per-cell importance scores that lack temporal coherence, cross-variable structure, and reusability across patients. We introduce the Temporal Island Sparse Autoencoder (TI-SAE), which learns a backbone-specific, patient-shared clinical concept dictionary from a frozen predictive model's representations. Each dictionary entry (latent) is defined by learned temporal Gaussian islands (specifying when the concept is active) and a sparse variable-composition vector (specifying which variables are involved). A decoupled selector then identifies which dictionary entries drive each patient's prediction, separating representation learning from attribution. We evaluate TI-SAE across five backbone architectures spanning different representation strategies on MIMIC-III and MIMIC-IV (three prediction tasks each). TI-SAE produces structured clinical concepts that go beyond transient attribution heatmaps while achieving strong performance on standard faithfulness benchmarks.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

电子健康记录（EHR）深度学习模型在死亡率、病情恶化和再入院等临床预测任务上性能优异，但内部表示缺乏可解释性，临床医生难以用熟悉的临床概念理解模型行为。现有的事后归因方法（如Integrated Gradients、SHAP、Dynamask、TimeX）在“时间×变量”输入网格上产生逐单元重要性分数，只能回答“哪些输入重要”，却无法回答“模型使用了哪些临床概念”。这类点归因存在两方面不足：一是缺乏时间延展性和多变量结构，而这两者是临床解释的前提；二是无法组合成可跨患者泛化的概念，且难以复用。此外，多数时间序列解释方法假设输入稠密且规则采样，而临床事件序列稀疏且不规则，只能做临时性适配。稀疏自编码器（SAE）虽可通过字典学习将模型内部表示分解为稀疏可解释特征，但标准SAE往往学到与单个token绑定或高度局部的特征，与时间上延展的临床概念不对齐；同时临床片段跨越数百个变量和较长时间窗，若不知道关注哪些变量和时间窗口，从原始轨迹中提取连贯概念不可行。因此，本文的核心问题是：如何设计一种结构上编码时空组合的SAE架构，从冻结预测模型的表示中学习患者共享、骨干特定的临床概念字典，使每个概念同时具备明确的时间活跃区间（时间高斯岛）和稀疏的变量组成，从而在保持忠实性的同时提供可分解、可复用、临床可理解的解释。

### Q2: 有哪些相关研究？

本文的相关研究可分为四类。事件表示类：BEHRT、CLMBR、MOTOR等编码级模型仅处理离散医疗编码；STraTS、HyMaTE采用连续值嵌入，ETHOS、EHRMamba采用离散量化，DuETT、BAT则直接在时间×变量网格上建模。这些工作为TI-SAE提供了骨干架构基础，但均不涉及概念级解释。梯度类方法：Integrated Gradients、DeepLIFT、GradSHAP及TSR产生逐单元格归因图，缺乏时间结构与可分解性。扰动类方法：KernelSHAP、TimeSHAP、Dynamask、FIT、WinIT、ContraLSP通过掩码或采样估计重要性，虽引入时间平滑，但仍输出扁平归因，无法分解为结构化概念。学习选择类：TimeX、TimeX++、L2X在单元格层面做实例级特征选择，同样缺少概念分解。概念与字典学习类：TCAV、ACE及概念瓶颈模型（CBM）依赖预定义概念或需修改训练过程；SAE在语言模型中被证明可分解出单义特征，Gated SAE、TopK SAE改进重构-稀疏权衡，并已扩展至视觉-语言模型和时间序列基础模型。本文区别在于：首次将SAE用于临床时间序列模型，以时间高斯岛和稀疏变量组合显式刻画概念时空结构，且完全事后、无需概念标签监督，优于CBM的静态属性与训练耦合。

### Q3: 论文如何解决这个问题？

论文提出 Temporal Island Sparse Autoencoder（TI-SAE），核心是在冻结的预测骨干模型之上学习一个患者共享、骨干特定的临床概念字典，从而把“模型表征了什么”与“哪些概念驱动了预测”解耦。整体框架包含四个组件：编码器、岛参数网络、岛选择器与解码器。编码器将骨干输出的稠密“时间×变量×维度”网格映射为 K 个潜在概念的激活轨迹，每个潜在概念通过 top-κ 稀疏、行归一化的变量路由向量只关注少数变量，再投影为标量激活。岛参数网络用一维卷积提取时间特征，为每个潜在概念生成 M 个高斯“时间岛”，其中心 μ 由 softmax 加权时间位置得到，宽度 σ 通过 EM 估计并裁剪，从而显式刻画概念“何时活跃”。岛选择器以能量门控得分对 K×M 个候选岛做可微 top-k（STE）选择，得到时间掩码并作用于激活。解码器复用同一路由参数、以更稀疏的 top-κ 和概念原子重建骨干表征，训练损失为观测单元上的归一化 MSE，并辅以死潜变量复活、μ 排斥、解码器多样性、掩码覆盖和通道纯度等正则项。第二阶段冻结整个 TI-SAE，训练预测感知选择器：将岛特征（μ、σ、激活统计、路由权重、观测覆盖）与患者查询向量投影交互后打分，选出驱动该患者预测的岛，并以 logit 保真损失和互补 hinge 损失优化。创新点在于用高斯时间岛赋予概念时间连贯性、用稀疏变量路由提供跨变量结构、用两阶段解耦实现可复用的患者共享字典，并支持后续 LLM 生成临床概念标签。

### Q4: 论文做了哪些实验？

论文在MIMIC-III（28,626个ICU episode，死亡率14.1%）和MIMIC-IV（46,140个episode，死亡率14.4%）上开展实验，提取48小时ICU片段，分别含135和132个临床变量，按患者划分64/16/20%训练/验证/测试。任务为院内死亡、30天再入院、住院时长>7天三项二分类预测。TI-SAE（K=1280, M=4）在五种冻结骨干上训练：离散Transformer（含/不含预训练）、STraTS、HyMaTE、BAT。对比基线包括骨干注意力、Integrated Gradients、TimeSHAP、Dynamask、TSR、Cluster-TCAV、FIT、WinIT及随机检查，采用移除、边际替换、邻域替换三种扰动策略，以AOPC衡量忠实性，并以SOFA严重度作为临床合理性软标签计算AUROC/AUPRC。结果显示TI-SAE在五个骨干中的四个取得最高AOPC（如HyMaTE上.097对基线最高.062），离散骨干上AUROC/AUPRC达.593/.286。此外还进行了跨数据集迁移（MIMIC-III→IV，AOPC .130）、概念可复现性、消融实验（稀疏变量路由贡献58–75% AOPC）、LLM与四名临床医生对解释质量的成对评估（概念层面胜出30–17等）。

### Q5: 有什么可以进一步探索的点？

论文的局限为后续探索留下了多个切入点。首先是输入形式与时间尺度：TI-SAE依赖固定长度的“时间×变量”网格，未来可扩展到变长序列、不同观测窗口，并检验跨时间尺度概念字典的稳定性与迁移性。其次是骨干适配性：变量路由编码器要求隐表示兼顾逐变量局部性与上下文概念形成，并非所有层都满足，可研究层选择准则或对不匹配层做轻量适配。第三是概念验证：当前latent的临床意义依赖事后验证，未来可引入临床专家闭环评估或与结构化知识库对齐，减少对SOFA等粗粒度代理的依赖。第四是多token事件表示需要架构改造，可探索事件级与token级概念的层级建模。最后，LLM verbalizer的强临床先验可能“美化”解释，未来应设计对照实验，直接度量概念输入对verbalizer的约束程度，区分“解释流畅”与“忠实反映模型推理”，并引入扰动一致性等忠实性指标。

### Q6: 总结一下论文的主要内容

论文针对电子健康记录深度学习模型预测性能强但内部临床概念难以解释的问题，指出现有事后归因方法只给出逐单元重要性分数，缺乏时间连贯性、跨变量结构和跨患者可复用性。为此提出时间岛稀疏自编码器（TI-SAE），从冻结预测模型的表示中学习患者共享、骨干特定的临床概念字典：每个字典条目由学习到的时间高斯岛（刻画概念何时激活）和稀疏变量组成向量（刻画涉及哪些变量）定义，并用解耦选择器识别驱动单个患者预测的字典条目，从而将表示学习与归因分离。作者在MIMIC-III和MIMIC-IV的三个预测任务、五种骨干架构上评估，发现TI-SAE能产生超越瞬时归因热图的结构化临床概念，并在标准忠实性基准上表现强劲，在五个骨干中的四个取得最高忠实性，同时提供基线方法无法生成的可分解、可临床标注的概念字典。
