---
title: "UACR: Uncertainty-Aware Collaborative Routing for Explainable Industrial Anomaly Inspection"
authors:
  - "Yiwei Li"
  - "Qiyang Chen"
  - "Zheming Yang"
date: "2026-11-21"
arxiv_id: "2611.28655"
arxiv_url: "https://arxiv.org/abs/2611.28655"
pdf_url: "https://arxiv.org/pdf/2611.28655v1"
categories:
  - "cs.CV"
  - "cs.LG"
tags:
  - "工业异常检测"
  - "可解释性"
  - "不确定性感知路由"
  - "自适应计算"
  - "在线检测"
  - "协作路由"
  - "面向操作员的解释"
relevance_score: 6.5
---

# UACR: Uncertainty-Aware Collaborative Routing for Explainable Industrial Anomaly Inspection

## 原始摘要

Industrial anomaly inspection requires not only accurate anomaly discrimination but also trustworthy explanations for operators, while satisfying the strict latency constraints of online inspection. Existing methods, however, typically apply a fixed computational path to all samples, making it difficult to strike a good balance among detection accuracy, inference efficiency, and interpretability. To address this issue, we propose UACR, an uncertainty-aware collaborative routing framework for explainable industrial anomaly inspection. UACR aims to deliver reliable anomaly decisions together with operator-facing explanations under the online inspection budget, while adaptively allocating computation so that ambiguous cases receive deeper scrutiny. The framework consists of two stages. Stage I, Offline Training and Routing Hyperparameter Search, learns the anomaly inspection modules and calibrates the uncertainty estimator that drives routing. Stage II, Uncertainty-Aware Adaptive Routing, collaboratively dispatches each input across inspection paths according to its estimated uncertainty. Experimental results on multiple public datasets show that UACR achieves over 5.16% improvement in accuracy compared to the baseline method, while reducing latency by over 31.5%. It also enhances the interpretability of industrial detection by over 15%.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决工业异常检测中检测精度、推理效率与可解释性难以兼顾的问题。研究背景是：制造质检场景中缺陷样本稀少、视觉差异细微且标注成本高，产线又要求在线及时决策，因此需要既准确又高效、还能为操作员提供可行动解释的检测系统。现有方法存在明显不足：轻量视觉异常检测模型虽能毫秒级筛查，但依赖类别相关的分数尺度，决策边界附近的模糊样本容易误判，且仅输出异常分数或证据图，无法说明缺陷类型及支撑决策的可见线索；多模态大语言模型虽能提供语义推理与解释，但逐样本调用开销和延迟过高，不适合处理全部产线图像；已有的选择性预测、延迟决策及基于场景复杂度的边云路由方法，其路由信号并不反映部署检测器自身的不确定性——视觉简单的图像可能靠近决策边界，而杂乱但正常的图像反而容易判断，因而无法协调本地可靠性、MLLM调用开销与为每次本地报警附加缺陷语义的需求。本文要解决的核心问题是：在严格在线延迟预算下，如何根据检测器自身的不确定性自适应分配计算资源，让高置信正常样本走快速本地路径，而模糊或报警样本交由参考条件化的语义验证器深入核查，从而同时输出可靠的异常判定与面向操作员的解释。

### Q2: 有哪些相关研究？

相关研究可分为三类。方法类方面，PaDiM通过建模预训练特征空间中的patch分布实现异常检测，PatchCore用记忆库保留代表性正常patch特征，反向蒸馏（Reverse Distillation）放大教师-学生网络在异常处的表示差异，SimpleNet学习目标域适配器与特征判别器，统一多类模型则致力于跨产品类别共享表示。这些方法在基于分数的识别与定位上表现优异，但本身不产生面向操作员的解释。应用类方面，AnomalyGPT利用合成异常-文本对适配视觉语言模型以生成解释，MMAD揭示了通用多模态大模型在细粒度工业异常推理上的持续弱点。评测与决策类方面，拒绝选项分类器在覆盖率约束下优化预测质量，learning-to-defer方法平衡模型与下游专家，SAEC依据图像复杂度选择本地或云端检测。与上述工作相比，本文的区别在于：现有方法要么缺乏原生解释能力，要么虽能生成解释却无显式机制量化解释质量，且难以满足在线检测的严格延迟与可验证性要求；UACR则通过不确定性感知的协同路由，在检测精度、推理效率与可解释性之间取得平衡，并按样本不确定性自适应分配计算，使模糊样本获得更深入审查。

### Q3: 论文如何解决这个问题？

UACR的核心思路是用不确定性驱动的协作路由，在在线检测预算内自适应分配计算资源，让模糊样本获得更深入审查，同时输出面向操作员的可解释结果。整体框架分为两个阶段。

阶段一为离线训练与路由超参数搜索。首先训练各检测模块：局部检测器以原生异常检测目标训练，其中仅正常样本检测器只用正常图像；语义验证器在可用检测记录上适配，采用字段加权自回归目标，将损失分解为标签、缺陷类型和解释三项token交叉熵之和，并设置正权重控制决策与语义监督的相对比例。训练完成后冻结两个组件。由于分数尺度随纹理、几何和正常波动而变化，校准在每个类别内独立进行：在验证子集上选取使正常与异常召回平衡准确率最大的阈值t_c，再由验证样本到阈值的边界距离分位数定义不确定性半径r_c(q)。随后在完整级联上搜索分位数q，目标函数综合准确率、缺陷类型召回和验证器调用率，并在调用预算约束下取最优q*，最终冻结阈值、分位数、参考分配和检测规则。

阶段二为不确定性感知自适应路由。廉价局部检测器先筛查每个查询，路由门控定义为：局部报警（s_i≥t_c）或落入边界区间（|s_i−t_c|≤r_c）的样本被升级到验证器；只有s_i<t_c−r_c的样本走本地正常出口。被升级样本由验证器结合正常参考和冻结的检测规则联合判定，可确认报警或纠正误报、漏报，最终输出统一的三元组（决策、缺陷类型、解释），保证下游看到一致的输出模式。创新点在于将路由阈值建模为不确定性分位数而非原始分数偏移，报警区始终纳入升级，且在线推理阶段无需任何训练或参数搜索。

### Q4: 论文做了哪些实验？

实验在Ubuntu 22.04.4系统、两块NVIDIA H100 GPU上进行，本地检测器采用EfficientAD，语义骨干为Qwen 9B与Qwen 7B，LoRA适配器rank为8、α=16、dropout 0.05、学习率2×10⁻⁴，字段损失权重为(10,3,1)。评测使用MVTec AD、MVTec LOCO、VisA和KSDD2四个公开数据集，验证/测试规模分别为732/1090、594/895、1299/2016、402/602。对比方法包括EfficientAD（仅本地检测器）、未适配MLLM骨干（每张图均调用）、受控SAEC（沿用SAEC路由但使用与UACR相同的三字段LoRA验证器）以及UACR。评价指标包括准确率、平衡准确率、TypeHit-A/P、TypeF1、ExplainHit、MLLM调用率和端到端时延。结果显示：UACR相对SAEC在9B和7B骨干上准确率分别提升5.16%和5.42%，相对EfficientAD提升9.69和8.11个百分点；MVTec AD上9B骨干达97.8%（SAEC为87.9%）。可解释性方面，MVTec AD上TypeF1由69.8%升至85.1%（9B），ExplainHit达94.9%；VisA上TypeF1提升11.2个百分点、ExplainHit提升17.5个百分点。调用率降至45.1%/43.9%（SAEC为78.2%），时延相对SAEC降低至少31.5%。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点。其一，不确定性估计器的校准质量直接决定路由效果，但论文仅在公开数据集上验证，真实产线中分布漂移、类别极度不均衡与标注噪声可能使校准失效，未来可研究在线校准或持续学习机制，使路由阈值随工况自适应调整。其二，路由策略目前以单样本不确定性为驱动，未显式建模多路径间的协同与成本约束，可引入预算约束下的强化学习或约束优化，实现全局时延-精度权衡。其三，可解释性提升以数值指标衡量，缺乏对操作员实际信任与决策效率的人因评估，未来可开展用户实验，并探索解释与不确定性的一致性约束。其四，路由决策本身的可解释性尚未讨论，可输出路由理由以增强系统透明度。此外，可扩展到多模态（图像+时序传感）工业场景，并研究冷启动与少样本新类别的路由泛化能力。

### Q6: 总结一下论文的主要内容

论文针对工业异常检测中检测精度、推理效率与可解释性难以兼顾的问题，指出现有方法对所有样本采用固定计算路径，无法在在线检测的严格延迟约束下平衡三者。为此提出UACR——一种不确定性感知的协同路由框架，其核心思想是估计每个样本的不确定性，并据此自适应分配计算资源，使模糊样本获得更深入的分析。框架分为两个阶段：阶段一为离线训练与路由超参数搜索，学习异常检测模块并校准驱动路由的不确定性估计器；阶段二为不确定性感知自适应路由，依据估计的不确定性将每个输入协同分派到不同检测路径。在多个公开数据集上的实验表明，UACR相较基线方法精度提升超过5.16%，延迟降低超过31.5%，可解释性提升超过15%。该工作表明，UACR能够在严格延迟预算下同时提供可靠的异常决策与面向操作人员的解释，为可解释工业异常检测提供了兼顾精度、效率与可解释性的有效方案。
