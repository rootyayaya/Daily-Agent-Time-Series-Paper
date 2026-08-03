---
title: "CENDRe: Concept Extraction with Natural Domain Representations"
authors:
  - "Antonia Holzapfel"
  - "Andres Felipe Posada Moreno"
  - "Sebastian Trimpe"
date: "2026-07-31"
arxiv_id: "2607.29621"
arxiv_url: "https://arxiv.org/abs/2607.29621"
pdf_url: "https://arxiv.org/pdf/2607.29621v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "可解释时间序列分析"
  - "概念提取"
  - "CNN时间序列分类"
  - "频域分析"
  - "故障诊断"
  - "轴承故障"
  - "潜在表示聚类"
  - "显著性定位"
relevance_score: 7.5
---

# CENDRe: Concept Extraction with Natural Domain Representations

## 原始摘要

Convolutional neural networks (CNNs) are widely used for time-series classification, but their deployment in critical domains requires understanding the temporal and spectral patterns that drive their predictions. Concept extraction (CE) methods identify such patterns by analyzing representations within the models' latent space. However, existing time-series CE methods have three limitations: they operate only in the time domain and overlook frequency features, predefine the number of concepts, and produce localizations misaligned with the regions the model uses. We address these limitations by proposing CENDRe, a concept extraction method for CNNs. It first discovers concepts by clustering per-timestep latent representations in two stages, where silhouette-guided aggregation selects the number of concepts automatically. Then, it localizes each concept through gradients of a presence score that contrasts the latent representations with their prototypes, producing masks that concentrate on the regions driving the concept. These gradients, propagated through a differentiable invertible mapping of the input such as a Fourier transform, yield localizations for the same concepts in the frequency domain. Finally, each concept receives a relevance score that quantifies its contribution to each class. On synthetic benchmarks, CENDRe achieves representation correctness comparable to state-of-the-art CE methods and significantly higher importance correctness. On real bearing-fault data, CENDRe extracts the frequency bands driving the model's predictions, located in regions commonly inspected for fault diagnosis, producing evidence to assess the model that time-domain CE methods cannot.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

本文聚焦于时间序列分类中卷积神经网络（CNN）的可解释性问题。研究背景在于，CNN在工业监测、医疗诊断等关键领域广泛应用，但其决策依赖的时域和频域模式难以被用户直接理解。现有概念提取（CE）方法虽能通过分析模型潜在空间揭示其学习到的模式，但存在三大不足：其一，仅能在时域生成解释，完全忽略模型可能依赖的频域特征；其二，概念数量需人为预先设定，导致解释结果受主观先验影响，无法反映模型真实的决策结构；其三，定位方法生成的掩码与模型实际关注的区域不匹配，可能遗漏关键区域或覆盖无关区域。

为此，本文提出CENDRe方法，旨在解决上述三个核心问题。该方法通过两阶段聚类自动确定概念数量，利用对比性存在分数的梯度生成精确的时域定位掩码，并借助可逆变换（如傅里叶变换）将同一概念的定位迁移至频域，从而首次实现时域与频域的双域概念提取。在合成基准和真实轴承故障数据上的实验表明，CENDRe不仅能恢复时域概念，还能提取专家用于故障诊断的特征频带，显著提升了概念解释的完整性与可信度。

### Q2: 有哪些相关研究？

在时间序列可解释性领域，相关研究主要分为三类。**概念提取方法**：现有工作如ECLAD-ts通过聚类探针层的逐时间步描述符提取概念，MultiVISION则基于有效感受野（ERF）对高激活神经元分段聚类。与它们相比，CENDRe首次将概念提取扩展至频域，并利用轮廓系数自动确定概念数量，避免了手动预设K的偏差。**频谱归因方法**：现有频谱归因（如扰动法、虚拟检测层）虽能提供频域局部解释，但仅针对单个预测，而CENDRe通过虚拟检测层机制将全局概念解释引入频域，这是此前未实现的。**原型可解释性方法**：传统原型法需预先固定每类原型数，轮廓分数仅用于事后评估，而CENDRe将其作为聚类聚合的主动选择准则。此外，图像领域的ACE、ConceptSHAP等方法虽启发了概念提取框架，但无法直接处理时间序列的时序与频谱特性。CENDRe的创新在于：通过两阶段聚类自动发现概念，利用对比原型梯度的显著性掩码实现跨域定位，并在轴承故障数据上验证了其提取频带与专家诊断区域的一致性，弥补了时域方法无法提供频域证据的不足。

### Q3: 论文如何解决这个问题？

CENDRe通过三个核心技术创新解决了时间序列概念提取的三大局限。首先，在概念发现阶段，它采用两阶段聚类策略：第一阶段用mini-batch k-means将逐时间步的LAD（层激活描述符）压缩为大量微质心，第二阶段通过轮廓系数引导的层次聚类自动确定概念数量K，避免了人为预设。LAD通过跨层激活上采样拼接而成，利用CNN的平移等变性捕捉多抽象层次的局部模式。

其次，在概念定位阶段，CENDRe定义了存在分数ρ_k，通过对比LAD与所属微质心的相似度及与其他概念微质心的平均相似度，量化概念成员关系。关键创新在于将梯度通过可逆可微变换（如傅里叶变换）反向传播，从而在任意自然域（时间域、频率域）生成定位掩码，解决了传统方法仅限时域且定位失准的问题。

最后，通过计算概念掩码与类别敏感度的内积，得到概念对各类别的重要性分数I_{c,k,ch}，量化概念对预测的推动或抑制作用。整体框架包含LAD构建、两阶段聚类、梯度定位和重要性评分四个模块，创新点在于自动确定概念数、跨域定位能力以及对比式存在分数设计。

### Q4: 论文做了哪些实验？

实验围绕合成数据集与真实轴承故障数据展开。合成数据包括syntheticLocal（注入方形、圆形、三角形等局部时域形状）和syntheticFrequency（在特定频带放置判别性峰值）两类二分类任务，均提供真实原始掩码作为基准。真实数据采用CWRU轴承故障集（四类：健康及三种故障位置，双通道12kHz采样，2048样本窗口）及BearingPD和UCR归档数据集。模型涵盖InceptionTime10、ResNet1D-18和DenseNet1D-121三种CNN架构，以AdamW优化（学习率1e-4），80/20划分，11个随机种子重复训练。

对比方法包括ECLAD-ts、MultiVISION及CENDRe的三种变体（kMeans、silhouette、HDBSCAN）。评估指标采用软表示正确性（sRC）和软重要性正确性（sIC），基于Relevance Mass Accuracy计算对齐分数。主要结果：在syntheticLocal上，CENDRe的sRC与ECLAD-ts相当，但sIC显著更高；MultiVISION两项指标均弱。在syntheticFrequency上，CENDRe的频域掩码准确定位判别频带，sRC和sIC接近时域表现。在CWRU上，概念按类别清晰分离，频域掩码对齐约2000Hz的故障特征频率，验证了方法从合成到真实信号的迁移能力。

### Q5: 有什么可以进一步探索的点？

CENDRe虽在时频双域概念提取上取得突破，但仍存在若干可探索方向。首先，其依赖1D CNN的近似平移等变性，限制了向Transformer、状态空间模型等非等变架构的迁移，未来可设计不依赖该性质的潜在表示对齐策略。其次，当前仅支持傅里叶变换作为可逆映射，可扩展至小波变换、短时傅里叶变换等时频分布，以捕捉非平稳信号的局部瞬态特征。第三，概念发现仍基于静态聚类，未利用时序依赖关系，可引入时序约束或动态聚类以提升概念一致性。此外，概念与类别间的相关性仅通过简单评分衡量，可结合因果干预或反事实推理，更严谨地验证概念对预测的因果贡献。最后，缺乏真实场景下的专家评估，未来应开展领域用户研究，验证概念掩码在故障诊断、医疗监测等任务中的实用性与可解释性，并探索概念反馈驱动的模型调试与捷径学习检测机制。

### Q6: 总结一下论文的主要内容

CENDRe提出了一种面向时间序列CNN的概念提取方法，旨在解决现有方法的三项局限：仅关注时域而忽略频域特征、需预设概念数量、以及定位与模型实际使用区域不匹配。该方法通过两阶段聚类（基于轮廓系数自动选择概念数）发现逐时间步的潜在表示概念，并利用对比原型的存在分数梯度生成时域掩码；随后通过可微的可逆变换（如傅里叶变换）将梯度传播至频域，实现同一概念的频域定位。最后，每个概念获得对各类别贡献的相关性评分。在合成基准上，CENDRe达到了与先进方法相当的表示正确性和更高的重要性正确性；在真实轴承故障数据中，它成功提取了驱动模型预测的频带，这些频带位于故障诊断常用区域，提供了时域方法无法给出的可验证证据。该工作首次结合时域与频域概念提取，为可解释时间序列分析开辟了新方向。
