---
title: "EEG-PRISM: Physiologically-Grounded Interpretability of Predictions by EEG Foundation Models"
authors:
  - "Deeksha M Shama"
  - "Punnisa Amornsirikul"
  - "Archana Venkataraman"
date: "2026-08-13"
arxiv_id: "2608.13676"
arxiv_url: "https://arxiv.org/abs/2608.13676"
pdf_url: "https://arxiv.org/pdf/2608.13676v1"
categories:
  - "cs.LG"
tags:
  - "EEG foundation models"
  - "interpretability"
  - "post-hoc attribution"
  - "frequency domain mapping"
  - "source domain mapping"
  - "biomarker identification"
  - "clinical EEG analysis"
relevance_score: 6.5
---

# EEG-PRISM: Physiologically-Grounded Interpretability of Predictions by EEG Foundation Models

## 原始摘要

Objective: Foundation models represent the next advancement in AI for EEG analysis; however current explainable AI techniques provide attribution scores in the time-channel input space, which is mismatched to clinical intuition about EEG. Thus, there is a critical need for a universal method that can extend the interpretability of any foundation model to alternative and physiologically relevant domains without modifying or retraining the underlying model. Methods: EEG-PRISM leverages linear transformations and established backpropagation rules to map time-channel attribution scores into alternative domains. We derive mappings to the frequency domain via an invertible DFT and to the source domain via an approximately invertible EEG generative model. We evaluate EEG-PRISM in simulated and real data, assessing recovery of ground-truth phenomena across domains with five foundation models and four AI explainers. Results: In simulation, EEG-PRISM achieves near-perfect spectral recovery and 69.2% spatial accuracy. In epilepsy, EEG-PRISM correctly determines that delta-theta activity is most salient and correctly localizes the seizure onset region with 50% accuracy. In autism, EEG-PRISM localizes the predictive delta-alpha biomarkers to frontal and temporal regions, consistent with prior work. Conclusion: EEG-PRISM is a theoretically-grounded post-hoc attribution method with accurate mapping into the spectral and spatial domains. It supports window-level analysis of transient events (e.g., seizures) and group-level identification of clinically relevant biomarkers (e.g., autism), thus advancing interpretable EEG foundation models. Significance: This work enables physiologically-grounded interpretation of EEG foundation models and supports clinically relevant insights such as event localization and biomarker identification.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

脑电图（EEG）基础模型虽在预测性能上表现优异，但其黑箱特性严重限制了临床转化。现有可解释AI方法（如GradCAM、SHAP）生成的归因分数局限于时间-通道输入空间，这与临床医生基于频谱（如delta/theta频带）和空间（如癫痫灶定位）的判读习惯严重脱节。同时，将领域知识直接融入基础模型需修改架构并重新训练，计算成本高昂。因此，本文旨在开发一种通用的、与模型无关的后处理方法，无需改动或重训基础模型，即可将任意EEG基础模型的时间-通道归因分数，通过线性变换（如可逆DFT）和近似可逆的EEG生成模型，数学严谨地映射到生理相关的频谱域和源空间域，从而弥合AI预测与临床直觉之间的鸿沟，提供可解释的频谱与空间归因，支持事件定位和生物标志物发现。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，现有工作聚焦于为EEG基础模型设计可解释性工具，如BENDR、BIOT、Labram、FoME、Cbramod和LUNA等模型，它们通过自监督学习从时间-通道输入中提取表征，但决策机制不透明；后验解释器如LRP、Integrated Gradients、DeepLIFT和SHAP虽能提供归因分数，但仅限于时间-通道域，与临床常用的频谱和源空间表征脱节。**应用类**研究涉及癫痫的频谱动态分析和源定位、自闭症的频带生物标志物识别，以及传统特征工程方法（如傅里叶变换、小波分解）在神经科学中的应用，但这些方法依赖手工特征且泛化性有限。**评测类**工作多通过模拟数据或真实临床数据验证解释器的准确性，但缺乏跨模型、跨解释器的系统评估。本文与上述工作的核心区别在于：EEG-PRISM不修改或重训练基础模型，而是通过可逆DFT和近似可逆的EEG生成模型，将时间-通道归因分数线性映射到频谱和源域，实现生理学可解释性。相比现有方法，它首次统一了跨五个基础模型和四种解释器的归因映射框架，并在模拟和真实数据上验证了频谱恢复和源定位性能，同时支持窗口级事件分析和群体级生物标志物识别，弥补了现有工作在临床可操作解释上的空白。

### Q3: 论文如何解决这个问题？

EEG-PRISM的核心创新在于提出了一种通用的后验归因映射框架，无需修改或重训练底层基础模型，即可将时间-通道空间的归因分数转换到生理学相关的频域和源空间域。其理论基础是一个关键命题：对于任意线性变换 \( \mathbf{x} = W\mathbf{z} \)，目标空间中的归因分数可表示为 \( \mathcal{A}^z_i = \mathbf{z}_i \sum_{j=1}^{N} W_{ji} \frac{\mathcal{A}^x_j}{\mathbf{x}_j} \)。该命题对三类主流解释器（LRP、梯度类方法如G×I和IG、DeepLIFT/DeepSHAP）均成立，通过链式法则和线性变换的复合性质严格推导，保证了映射后归因的忠实性和守恒性。

在架构上，EEG-PRISM包含两个主要映射模块。**频域映射**利用可逆的离散傅里叶变换（DFT），将每个通道的时间序列分解为实部和虚部，通过余弦和正弦基函数构建线性权重矩阵，将时间域归因投影到频谱域，最终跨通道平均得到整体频谱归因。**空间映射**则利用生物物理启发的EEG正演模型（leadfield矩阵）建立头皮通道与皮层源活动之间的线性关系，通过正则化逆求解器估计源活动，再将归因分数线性传播到源空间。该方法对逆问题误差具有线性保真度，不会引入额外失真。

创新点在于：一是理论完备性，统一了多类解释器的映射规则；二是即插即用性，适用于任意基础模型；三是支持窗口级瞬态事件分析和群体级生物标志物识别，在癫痫发作源定位和自闭症频谱特征提取中验证了临床价值。

### Q4: 论文做了哪些实验？

论文围绕EEG-PRISM方法展开了系统性实验评估，涵盖模拟数据、癫痫和自闭症三个场景。实验设置上，使用五个EEG基础模型（如LaBraM、Cbramod、EEGNet、ABNet等）和四种可解释性方法（IG、DeepLift、DeepSHAP、LRP），先获取时间-通道归因分数，再通过EEG-PRISM映射到频谱和源空间域。

在模拟数据实验中，频谱恢复任务中所有方法均接近完美准确率，DeepSHAP表现最佳；空间定位任务中，平均定位误差约3±2厘米，IG取得最优象限级准确率（高于20%的随机水平），LaBraM模型空间精度最高。在癫痫数据集（TUSZ）上，模型分类准确率约88%，EEG-PRISM正确识别delta和theta频段为最显著特征（与43%和35%的临床报告一致），源空间定位癫痫发作起始区的平均准确率约50%，混淆主要出现在中央区和左右半球。在自闭症数据集（ACE）上，采用LaBraM模型，正确分类的ASD个体主要归因于delta频段活动，TDC个体则主要归因于alpha频段，空间归因显示额叶驱动分类，组间差异定位于颞叶和右中央区，与既有文献一致。整体结果表明EEG-PRISM能在多种模型和解释器组合下稳定实现频谱和空间域的可解释映射。

### Q5: 有什么可以进一步探索的点？

EEG-PRISM虽在频谱与空间映射上表现优异，但仍存在若干可探索方向。首先，其源域映射依赖近似可逆的生成模型，空间定位精度（69.2%）与癫痫灶识别率（50%）仍有提升空间，未来可引入更精细的神经生理约束（如皮层电流密度模型）或基于扩散模型的非线性可逆映射，以增强源域重建的生理真实性。其次，当前方法仅支持静态频谱与空间域，未充分利用时频联合表征（如小波或Hilbert-Huang变换），可扩展至动态时频域以捕捉瞬态振荡的演化模式。第三，EEG-PRISM依赖基础模型内部梯度的可访问性，对黑盒API模型不适用，可探索基于扰动或蒸馏的梯度近似策略。此外，跨被试、跨数据集的泛化性及多模态（如结合fMRI或行为数据）的联合归因尚未验证，未来可构建多尺度生理图谱以提升临床可解释性。最后，将归因结果与临床决策支持系统（如癫痫手术规划）结合，开展前瞻性验证，是推动实际落地的关键。

### Q6: 总结一下论文的主要内容

EEG-PRISM提出了一种基于生理学可解释性的框架，用于将EEG基础模型的预测归因从时间-通道空间映射到临床相关的频谱和源空间域。该方法利用离散傅里叶变换和EEG生成模型实现线性可逆映射，无需修改或重训练底层模型，且兼容LRP、Integrated Gradients、DeepLIFT等多种解释器。在模拟数据中，EEG-PRISM实现了近乎完美的频谱恢复和69.2%的空间定位精度；在癫痫数据中，正确识别delta-theta频带显著性并以50%准确率定位发作起始区；在自闭症数据中，将预测性delta-alpha生物标志物定位至额叶和颞叶区域。该工作为EEG基础模型提供了理论严谨的事后归因方法，支持瞬态事件窗口级分析和群体级临床生物标志物识别，推动了可解释EEG基础模型在临床转化中的应用。
