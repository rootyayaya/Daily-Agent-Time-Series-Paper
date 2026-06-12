---
title: "ProtoX-AD: Self-Explainable Time Series Anomaly Detection and Characterization"
authors:
  - "Aitor Sánchez-Ferrera"
  - "Elisabeth Wetzer"
  - "Kristoffer Wickstrøm"
  - "Michael Kampffmeyer"
  - "Robert Jenssen"
date: "2026-06-11"
arxiv_id: "2606.13277"
arxiv_url: "https://arxiv.org/abs/2606.13277"
pdf_url: "https://arxiv.org/pdf/2606.13277v1"
github_url: "https://github.com/Aitorzan3/ProtoX-AD"
categories:
  - "stat.ML"
  - "cs.LG"
tags:
  - "时间序列异常检测"
  - "可解释性"
  - "原型学习"
  - "自监督学习"
  - "特征变换"
  - "异常表征"
relevance_score: 6.5
---

# ProtoX-AD: Self-Explainable Time Series Anomaly Detection and Characterization

## 原始摘要

Recent advances in time series anomaly detection (TSAD) have highlighted the effectiveness of self-supervised classification-based approaches. These methods apply transformations to normal training samples, training a classifier to recognize transformation-specific patterns that help identify anomalies through increased classification errors. Despite their strong performance, a significant challenge is their lack of explainability, as they provide limited insight into the characteristics of flagged anomalies. To address this limitation, we propose ProtoX-AD, a prototype-based self-explainable framework for self-supervised TSAD. ProtoX-AD learns transformation-aware latent representations alongside interpretable prototypes, enabling both accurate anomaly detection and the identification of distinct anomalous profiles through prototype-based explanations. Additionally, it allows for systematic analysis of how transformation design impacts detection performance and explainability. Experimental results on synthetic and real-world datasets demonstrate that ProtoX-AD achieves detection performance comparable to its black-box counterparts while offering more consistent and semantically meaningful explanations than existing explainable baselines. Our code is publicly available at https://github.com/Aitorzan3/ProtoX-AD.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列异常检测（TSAD）在金融、物联网和医疗等关键领域至关重要，但由于异常标注成本高，通常采用无监督方法。近期，基于自监督分类的方法（SSC-TSAD）表现突出，通过对正常样本施加变换并训练分类器识别变换模式，利用异常样本的分类误差增大来检测异常。然而，现有方法存在显著不足：它们仅提供异常分数，缺乏可解释性，无法揭示异常行为的潜在结构，例如无法区分不同类型的异常模式（如点异常、模式异常或上下文异常），也难以分析变换设计如何影响检测性能。这限制了在实际应用中识别和解读不同异常特征的能力。为解决这一核心问题，本文提出ProtoX-AD，一个基于原型的自解释框架。它通过学习变换感知的潜在表示和可解释原型，在保持与黑盒方法相当检测性能的同时，能够通过原型重建在输入空间可视化异常特征，从而实现对不同异常模式的系统性表征，并支持分析变换设计对检测性能与可解释性的影响。

### Q2: 有哪些相关研究？

在时间序列异常检测（TSAD）领域，相关研究主要分为三类。**方法类**工作聚焦于自监督分类（SSC）框架，通过设计变换生成正常样本的增强视图，训练分类器识别异常模式。本文与这些工作的核心区别在于：现有方法（如基于手工变换的水泄漏检测、癫痫检测，或基于可学习神经变换的对比学习）仅关注检测性能，缺乏可解释性。ProtoX-AD 首次引入原型机制，在保持检测性能的同时提供语义级异常解释。**应用类**工作针对特定领域（如工业故障、医疗监测）设计变换，但通用性受限。本文通过原型分析系统评估变换设计对检测与可解释性的影响，弥补了领域适应性的研究空白。**评测类**工作主要比较不同变换策略的检测精度，而本文额外评估了异常表征的一致性，提出更全面的可解释性度量。总体而言，ProtoX-AD 将可解释性从事后分析提升为模型内建特性，填补了自监督 TSAD 在异常表征与解释之间的鸿沟。

### Q3: 论文如何解决这个问题？

ProtoX-AD通过一个五模块的自解释框架解决时间序列异常检测的可解释性问题。核心方法是在自监督分类框架中引入可解释的原型学习，使模型既能检测异常，又能通过原型提供语义解释。

整体架构包含五个关键组件：1）**变换模块**：应用K种变换（含恒等变换）生成增强视图，模拟不同异常模式；2）**特征提取模块**：基于VAE将增强视图编码为概率性潜在表示（均值与方差），促进平滑结构化的潜在空间；3）**双重建模块**：包含解释器（重建增强视图）和语义保持解码器（重建原始样本），前者支持原型可视化，后者防止表示坍塌；4）**原型模块**：为每个变换类学习M个原型，通过欧氏距离计算潜在表示与原型间的相似度矩阵；5）**分类模块**：基于相似度矩阵进行线性分类，直接利用原型概念完成自监督分类任务。

关键技术包括：**三重损失函数**：分类损失（交叉熵）、双重建损失（视图重建+语义保持+原型中心正则化）和原型学习损失（聚类损失+覆盖损失）。其中原型中心正则化通过KL散度将潜在表示对齐到类特定原型，覆盖损失防止原型退化。**异常评分**：测试时仅用恒等视图，其分类交叉熵值作为异常分数——若被误分为其他变换类，表明样本具有异常特征。**解释机制**：通过解码最近原型到输入空间，提供可视化的异常特征描述，且不同变换类原型可刻画多种异常模式。该方法满足自解释模型的透明性（原型直接用于分类）、多样性（多原型捕获不同模式）和可信赖性（性能与黑盒模型相当）。

### Q4: 论文做了哪些实验？

论文在三个数据集上进行了实验：UMD（合成时间序列，含钟形异常）、GTA（全球温度异常，基于GISTEMP和gcag两个来源）和Yorkshire Water Leak Detection（真实水流量数据，含4个百分位阈值设置）。对比方法包括浅层方法（Isolation Forest、One-Class SVM、Local Outlier Factor）、可解释自监督基线KMEx（基于原型）以及无解释机制的黑盒自监督方法。ProtoX-AD采用手动设计变换和可学习神经变换两种策略。主要结果：在UMD上，ProtoX-AD（手动变换）AUROC和AUPR均达100%，与黑盒方法持平，优于浅层方法（最高91.75% AUROC）；在GTA的GISTEMP源上，ProtoX-AD（手动变换）AUROC为99.61%，略优于KMEx（99.53%）和黑盒方法（99.51%），但在gcag源上低于KMEx（91.47% vs 96.46%）；在Yorkshire数据集上，ProtoX-AD（手动变换）在多数百分位下AUROC和AUPR最高（如p=0.8时AUROC 98.00%），优于所有对比方法。神经变换版本性能显著下降，且解释质量（MAE/MSE）更差。ProtoX-AD（手动变换）在解释误差上普遍低于KMEx，例如UMD上使用7个原型时MAE为10.99（KMEx为11.01）。

### Q5: 有什么可以进一步探索的点？

ProtoX-AD在可解释时间序列异常检测上迈出了重要一步，但仍存在若干可探索的方向。首先，其原型解释依赖于预定义的变换集合，这限制了发现未知异常模式的能力，未来可引入动态原型生成机制，结合在线学习或元学习，使原型能自适应地捕捉数据中的新异常形态。其次，当前框架对变换设计的分析是事后性的，缺乏对变换选择与解释质量之间因果关系的理论指导，可尝试利用因果推断或信息瓶颈理论来优化变换集，提升解释的鲁棒性。此外，原型解释的语义一致性在跨域场景下可能退化，建议引入领域自适应或对比学习，增强原型在不同工业场景下的迁移能力。最后，从实用角度看，可探索将原型解释与LLM结合，生成自然语言描述，辅助运维人员快速理解异常根因，并开发交互式Agent工作流，实现从检测到诊断的闭环自动化。

### Q6: 总结一下论文的主要内容

ProtoX-AD提出了一种基于原型的自解释框架，用于解决自监督分类式时间序列异常检测（SSC-TSAD）缺乏可解释性的问题。现有SSC-TSAD方法通过变换正常样本训练分类器，虽检测性能优异，但仅输出异常分数，无法揭示异常模式的结构特征。该方法通过学习变换感知的潜在表示和可解释原型，在保持与黑盒方法相当检测精度的同时，能识别并表征不同异常轮廓。实验表明，ProtoX-AD在合成和真实数据集上提供了比现有可解释基线更一致、语义更清晰的解释，并系统分析了变换设计对检测性能和可解释性的影响。其核心贡献在于将原型可解释模型引入TSAD领域，实现了检测精度与可解释性的平衡，为工业故障诊断等关键应用提供了可理解的异常表征工具。
