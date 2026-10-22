---
title: "GRAIL: From Saliency to Semantics in Time-Series Explanation"
authors:
  - "Enver Menadjiev"
  - "Yiqiu Shen"
  - "Jaesik Choi"
  - "Julia Stoyanovich"
date: "2026-10-21"
arxiv_id: "2610.29036"
arxiv_url: "https://arxiv.org/abs/2610.29036"
pdf_url: "https://arxiv.org/pdf/2610.29036v1"
categories:
  - "cs.AI"
tags:
  - "时间序列解释"
  - "区域归因"
  - "反事实基线"
  - "Owen值"
  - "语义特征"
  - "ECG"
  - "可解释性"
  - "领域知识"
relevance_score: 6.5
---

# GRAIL: From Saliency to Semantics in Time-Series Explanation

## 原始摘要

Explaining a time-series model requires both locating the evidence and extracting meaningful knowledge from it. Yet a single timestep is not a semantic unit: the meaningful patterns live across many samples, not in any one of them. Per-timestep saliency is therefore noisy, high-dimensional, and unstable. Existing methods address this by introducing fixed-size windows and treating them as independent players in a cooperative game. Evaluating a coalition of such players requires defining a ``baseline'' region, which prior work tackles with fixed counterfactuals (e.g., a flat line, noise, or a spectral surrogate). This choice frequently dominates the resulting explanation, obscuring the model's true decisions.
  To address these issues, we propose GRAIL, a region-based time-series explanation framework that uses domain-specific intervals, such as the P-wave and the QRS complex of an electrocardiogram (ECG) beat, as players. We describe each region with human-readable features and generate counterfactual baselines with an on-manifold conditional generator. Such a choice of players also admits non-temporal features: static covariates enter as singleton players attributed with the temporal regions on one scale, so a patient's tabular evidence (e.g., age, sex) is weighed directly against the signal. We attribute the predictions to the features via Owen values with common-random-number variance reduction. Experimental results on both synthetic and real data show that the proposed framework produces faithful and robust explanations, evaluated under matched on- and off-manifold operators, offering meaningful knowledge to domain experts.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决时间序列模型解释中“定位证据”与“提取语义知识”之间的鸿沟问题。研究背景是：深度学习模型 increasingly 被部署于临床、工业传感器和金融等高风险时间序列场景，部署的关键在于回答“信号的哪一部分驱动了决策”，且答案需以领域专家可操作的形式呈现。现有方法的不足体现在两个层面：其一，逐时间步的显著性图虽能定位证据，但单个时间步并非语义单元，有意义的模式往往跨越多个样本，导致显著性图噪声大、维度高、不稳定，且无法直接表达区域模式及其临床含义；其二，已有工作引入固定大小窗口并将其视为合作博弈中的独立参与者，但评估这类参与者的联盟需要定义“基线”区域，先前工作采用固定反事实（如平线、噪声或频谱替代），这一任意选择常常主导最终解释，掩盖模型的真实决策。此外，模型通常同时接收时间信号与非时间协变量（如患者年龄、性别），而现有解释器难以将二者放在同一尺度上权衡。因此，本文的核心问题是：如何以领域对齐的语义区域（如心电图的P波、QRS波群、T波）为解释单元，构建在数据流形上的反事实基线，并将时间区域与静态协变量统一归因，从而生成忠实、稳健且对领域专家有意义的时间序列解释。

### Q2: 有哪些相关研究？

本文的相关工作主要分为两类。

方法类：一是基于Shapley值的归因方法，其核心在于如何建模“缺失”特征。多数时间序列解释器给出逐时间步显著性，较粗粒度的则把时间步分组为窗口或片段（WindowSHAP、TimeSHAP、TS-MULE、LIMESegment、Dynamask），但均用固定的、偏离流形的填充值表示缺失状态。本文的区别在于将移除算子改为保持流形的条件生成器，并把平坦的Shapley博弈提升为特征嵌套于区域的两级Owen值。二是最接近的“时间序列玩家”方法：C-SHAP使用信号概念，GroupSegment-SHAP重新定义玩家，但都保留偏离流形的均值替换算子，且不支持非时间协变量。本文保持玩家结构不变而改变算子。CausalConceptTS同样基于生成式前提，但在整段记录上插补；ManifoldShap将干预背景限制在流形区域内而非生成它。本文的逐区域生成使精确Owen扫描可行。

评测类：由于扰动忠实性受移除算子混淆，本文在匹配的流形内算子和中性的流形外算子下对所有方法评分，并对精确博弈进行摊销以支持部署。

### Q3: 论文如何解决这个问题？

GRAIL 的核心思路是把时间序列归因从“逐时间步显著性”提升为“语义区域合作博弈”。整体框架分三步：定义博弈、精确求解、摊销加速。

首先，在博弈定义上，GRAIL 用分割器把信号划分为具有领域含义的区域（如 ECG 的 P 波、QRS 波群），每个区域经可解释编码器（codec）编码为人类可读特征（如水平、趋势、峰值、R 波幅值、QRS 宽度等），这些区域特征作为博弈参与者；静态协变量（年龄、性别等）作为单例参与者附加其后，使信号证据与表格证据在同一尺度上比较。codec 由可解释编码器与条件生成器配对，支持 shape、stat、spectral-mix、clinical 等多种配置，且可插拔。

其次，在求解上，GRAIL 用数据流形上的条件生成器（默认高斯过程后验）为缺失区域生成反事实基线，避免平坦线、噪声等固定反事实主导解释；联盟值定义为对生成随机性的期望 logit。归因采用 Owen 值，保持“区域→特征”的嵌套一致性（如 QRS 内各特征值之和等于 QRS 的区域 Shapley 值），并用公共随机数（CRN）望远镜式扫描，仅需 |N|+1 次模型调用即可精确满足效率公理；同时引入形态残差参与者，把重建残差 ρ 变为可归因通道，保证账目无损完整。无区域先验时，用 PELT 变点或模型感知分割器自动发现区域。

最后，为部署加速，GRAIL 用 FastSHAP 目标训练单次前向代理网络 Amort，并通过投影强制加性效率约束，推理时精确完整，速度约提升 10³ 倍。创新点在于：以领域区域为参与者、流形上条件反事实、Owen 值精确完整归因、残差可归因化，以及精确博弈与摊销代理的双轨设计。

### Q4: 论文做了哪些实验？

论文在六个数据集上评估GRAIL，覆盖三个领域：两个带真值区域掩码的合成数据集族（Synth及加入静态协变量的Mixed）、两个带心脏病专家P/QRS/T标注的临床ECG数据集族（来自MIT-BIH与QT的ECG，以及携带患者年龄和性别的多变量LUDB）、两个无区域标注的工业传感器数据集族（FordA、Wafer）。所有目标模型均为InceptionTime分类器。GRAIL以三种配置运行：提供区域、用Auto发现区域、用Amort摊销部署，并与六种时间序列窗口化与扰动基线（WindowSHAP、TimeSHAP、TS-MULE、LIMESegment、Dynamask）、最接近的概念级与组级Shapley方法（C-SHAP、GS-SHAP）以及非时间序列的梯度与采样归因方法（Integrated Gradients、gradient×input、KernelSHAP）对比。评估在两种匹配算子下进行：中性off-manifold算子与on-manifold再生算子，并报告定位、鲁棒性、成本与完备性，所有结论均通过配对Wilcoxon检验并以BH q<0.05把关。主要结果：on-manifold下精确博弈在每个数据集族上都是最忠实的方法，GRAIL在Synth达0.872、Mixed 0.921、ECG 0.828、LuDB 0.657、FordA 0.864，Auto在Wafer达0.774，均显著优于全部十二个基线（144项检验BH q<0.05）；完备性精确，平均绝对残差为0.000。多变量LUDB上三导联较单导联在各项质量指标上更优（on-manifold忠实度0.659升至0.735），代价约为39倍运行时间（2.4秒至94.4秒）。静态协变量作为单例玩家与信号区域同尺度归因，年龄平均|φ|=1.663高于最高ECG区域1.542，性别仅0.238，静态量合计占24.8%。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于：尚未通过用户研究验证解释对领域专家的实际可用性；摊销代理模型针对单一模型训练，模型随机化检验需重新训练，成本较高；精确生成器会使 logit 饱和，虽可由残差检测并用 cVAE/DDPM 缓解，但未根治；自动区域发现虽有改进但仍未解决；方法在 GP 无法表征的非平稳信号上仍需验证。未来可探索的方向包括：开展专家用户研究以评估解释的实用价值；设计模型无关或可快速适配的摊销代理，降低随机化检验开销；引入更稳健的生成器或约束机制避免 logit 饱和；结合学习型分割与领域先验实现更可靠的自动区域发现；将框架扩展到更多模态与非平稳信号，并系统分析多变量与多导联场景下解释的稳定性与忠实性。此外，可研究区域粒度自适应选择，以及将静态协变量与时间区域联合归因的因果解释框架。

### Q6: 总结一下论文的主要内容

论文针对时间序列模型解释中"单时间步并非语义单元"这一核心问题，指出逐点显著性图噪声大、维度高且不稳定，而现有方法引入固定窗口并依赖平坦线、噪声或频谱替代等固定反事实基线，该选择常主导解释结果、掩盖模型真实决策。为此提出GRAIL框架：以领域语义区间（如心电图的P波、QRS波群）及静态协变量作为合作博弈的参与者，用可解释编码器将每个区域编码为人类可读特征，并以流形上的条件生成器重建缺失区域，使每个联盟都对应可信的真实信号；再通过Owen值与公共随机数方差缩减精确估计归因，并始终报告残差以保证账目完备。实验在合成数据、真实心电图与工业传感器数据上表明，该方法在流形上归因最忠实、完备性精确，且能将信号与年龄、性别等元数据置于同一尺度比较，揭示模型对非时序信息的依赖；作者还提供摊销代理网络以加速部署，并支持无先验的区域发现与多导联信号。
