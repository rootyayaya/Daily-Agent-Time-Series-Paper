---
title: "SurvCF(t): Counterfactual Explanations for Survival Analysis in Predictive Maintenance Multivariate Time Series Data"
authors:
  - "Zara Karazian"
  - "Panagiotis Papapetrou"
  - "Sindri Magnússon"
  - "Erik Frisk"
  - "Tony Lindgren"
date: "2026-07-18"
arxiv_id: "2607.16969"
arxiv_url: "https://arxiv.org/abs/2607.16969"
pdf_url: "https://arxiv.org/pdf/2607.16969v1"
categories:
  - "cs.LG"
tags:
  - "可解释时间序列分析"
  - "反事实解释"
  - "预测性维护"
  - "多变量时间序列"
  - "生存分析"
  - "剩余寿命估计"
  - "工业故障诊断"
  - "可操作干预"
relevance_score: 7.5
---

# SurvCF(t): Counterfactual Explanations for Survival Analysis in Predictive Maintenance Multivariate Time Series Data

## 原始摘要

Predictive maintenance relies on accurate Remaining Useful Life estimation, often formulated using survival analysis over multivariate time-series data. While modern deep survival models achieve strong predictive performance, their black-box nature limits their use in safety-critical settings where actionable insight is required. In this work, we introduce \textit{SurvCF(t)}, the first framework for generating counterfactual explanations for survival models operating on time-series data. \textit{SurvCF(t)} identifies minimal, plausible, and temporally consistent changes to an asset's operational history that increase its predicted life time, framing explanation as a constrained optimization problem combining validity, proximity, sparsity, and plausibility. We evaluate the method on multiple benchmarks, including C-MAPSS, N-CMAPSS, and a real-world case study of the Scania Component\_X dataset, demonstrating its ability to produce actionable and interpretable interventions. Our results show that \textit{SurvCF(t)} bridges the gap between survival prediction and prescriptive maintenance, enabling explainable and decision-oriented AI for maintenance strategies.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

预测性维护（PdM）依赖于对设备剩余使用寿命（RUL）的准确估计，这通常基于多变量时间序列数据进行生存分析。尽管现代深度生存模型在预测性能上表现优异，但其“黑箱”特性限制了在安全关键场景中的应用，因为这类场景不仅需要预测，更需要可操作的指导。现有方法存在明显不足：一方面，传统的可解释AI方法（如归因、注意力机制）仅能描述哪些特征重要，却无法给出“如何改变”的处方性建议；另一方面，已有的反事实解释工作主要针对静态表格数据或分类/回归任务，无法处理时间序列的时序依赖性和生存数据特有的删失问题。因此，在工业场景中，当检测到设备存在失效风险时，系统无法提供具体、可行的操作调整方案来延长RUL。本文旨在解决这一核心问题：如何为基于多变量时间序列数据的生存模型生成反事实解释，从而在预测设备寿命的同时，提供最小化、可行且时序一致的操作干预建议，以有效延长设备剩余寿命，弥合预测性维护中“预测”与“处方”之间的鸿沟。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及三个领域：时间序列反事实解释、生存分析及其可解释性，以及预测性维护中的故障诊断。

首先，在**时间序列反事实解释**领域，现有方法可分为三类：基于实例的方法（如NUN、CoMTE、MASCOTS）通过从观测数据中构造反事实来保证合理性；基于优化的方法（如TimeX、AB-CF、Glacier）引入时间正则化项；基于表示或子序列的方法（如DiscoX、CELS、M-CELS）在潜在空间中修改关键时间区域。本文与这些工作的核心区别在于，它们均针对分类或回归任务，而本文首次将反事实解释扩展到生存分析场景，需处理随时间变化的风险函数而非单一预测值。

其次，在**生存分析可解释性**方面，现有工作如Chapfuwa等人和Gupta等人侧重于因果推断与均衡表示学习，Nagpal等人则关注反事实表型分析，但均不生成实例级可操作解释。Kovalev等人和Alabdallah等人虽直接生成反事实解释，但局限于静态协变量的表格数据，无法处理时间序列中的时序依赖与平滑性约束。本文填补了这一空白，提出首个面向多变量时间序列生存模型的反事实框架。

最后，在**预测性维护应用**方面，本文在C-MAPSS、N-CMAPSS及Scania真实数据集上验证，与仅关注预测精度的深度生存模型（如DeepSurv、DeepHit）不同，本文侧重生成最小、合理且时序一致的反事实干预，实现从预测性维护到规范性维护的跨越。

### Q3: 论文如何解决这个问题？

该论文提出SurvCF(t)框架，通过两阶段方法为多变量时间序列的生存模型生成反事实解释。整体框架分为生存模型训练和反事实生成两部分。

**核心方法**：首先，采用离散时间生存分析建模，使用LSTM网络将固定长度时间窗口映射为条件风险向量h(X)∈(0,1)^T_max，通过累积乘积计算生存函数和预测剩余寿命(RUL)。训练时采用截断对数似然损失，并利用GroupKFold交叉验证防止数据泄露。

**反事实生成**：将问题形式化为约束优化，目标函数包含四个关键项：(1) 有效性项，通过铰链损失推动预测RUL达到用户指定的改进目标（含过冲系数κ）；(2) 邻近性项，结合L2范数和时间平滑正则化（一阶差分算子）保持扰动微小且时序一致；(3) 合理性项，基于马氏距离的铰链损失确保扰动不偏离训练分布；(4) 稀疏性通过后处理实现，采用Growing-Spheres特征选择，按特征平均扰动幅度排序并贪婪地恢复非必要修改。

**关键技术**：可编辑特征掩码M_e确保仅修改可控变量；箱型约束将扰动限制在训练分位数范围内；Adam优化器直接优化连续扰动矩阵Z。最终输出仅修改必要特征且满足RUL提升阈值的稀疏反事实解释X*。该框架首次将反事实解释引入时间序列生存分析，实现从预测性维护到规范性维护的跨越。

### Q4: 论文做了哪些实验？

论文在三个公开的预测性维护基准上评估了SurvCF(t)框架。实验设置包括：使用C-MAPSS的FD001子集（24通道传感器数据，窗口长度w=20，时间步长dt=5，在cycle=250处人为删失），N-CMAPSS的DS01-DS03子集（1Hz采样率，聚合为每周期摘要，窗口L=20，dt=2，在cycle=65处删失），以及Scania Component_X真实数据集（33,000+辆卡车，保留非直方图计数器和97个直方图列，窗口L=20，dt=10，处理不规则时间戳）。对比方法未明确提及，但框架通过优化有效性、邻近性、稀疏性和合理性四个反事实属性进行评价。主要结果：SurvCF(t)能在所有数据集上生成最小、合理且时间一致的反事实解释，通过扰动可操作通道延长预测的剩余使用寿命（RUL）。关键数据指标包括：在不同RUL改进目标下的有效性（反事实是否成功延长寿命）、邻近性（扰动幅度）、稀疏性（扰动通道数量）和合理性（扰动是否符合物理规律）。可编辑集消融实验量化了操作现实性与反事实能力之间的权衡，证明该方法能桥接生存预测与规范性维护的差距。

### Q5: 有什么可以进一步探索的点？

该工作首次将反事实解释引入生存分析时序预测维护，但仍存在若干可探索方向。首先，当前优化目标中“有效性”仅考虑延长寿命，未区分不同故障模式或维修成本权重，未来可引入多目标优化，平衡寿命延长与操作代价。其次，反事实生成依赖预定义的时间窗口，对长期依赖或突发性退化模式（如早期故障）的捕捉能力有限，可尝试结合注意力机制或时序Transformer自适应识别关键干预区间。此外，方法在C-MAPSS等合成数据上表现良好，但真实工业场景中传感器噪声、缺失值及非平稳工况会显著影响反事实的鲁棒性，需设计对抗训练或贝叶斯不确定性量化。最后，当前解释仅面向单个资产，未来可扩展至多资产协同场景，生成考虑系统级约束（如产线平衡）的联合反事实策略，从而提升决策实用性。

### Q6: 总结一下论文的主要内容

SurvCF(t)提出首个针对工业预测性维护中生存分析模型的反事实解释框架，旨在解决黑箱模型缺乏可操作指导的问题。其核心贡献在于将反事实解释从静态表格数据扩展到多变量时间序列的生存分析场景，通过最小、合理且时序一致的输入修改来提升预测的剩余使用寿命。方法上，将反事实生成形式化为约束优化问题，同时优化有效性、接近性、稀疏性和合理性，并利用生存模型输出作为目标。在C-MAPSS、N-CMAPSS及真实Scania数据集上的实验表明，该方法能生成可解释的干预建议，有效弥合了生存预测与规范性维护之间的鸿沟，为安全关键系统提供了决策导向的可解释AI方案。
