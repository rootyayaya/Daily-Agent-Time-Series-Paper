---
title: "Evolutionary Feature Engineering for Structured Data"
authors:
  - "Ege Onur Taga"
  - "Yilin Zhuang"
  - "M. Emrullah Ildiz"
  - "Petros Mol"
  - "Abhimanyu Das"
  - "Karthik Duraisamy"
  - "Samet Oymak"
date: "2026-07-02"
arxiv_id: "2607.01548"
arxiv_url: "https://arxiv.org/abs/2607.01548"
pdf_url: "https://arxiv.org/pdf/2607.01548v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "LLM-based evolution"
  - "feature engineering"
  - "time series forecasting"
  - "tabular prediction"
  - "interpretability"
  - "time series foundation model"
  - "Chronos-2"
  - "EFE-Time"
  - "EFE-Tab"
relevance_score: 6.5
---

# Evolutionary Feature Engineering for Structured Data

## 原始摘要

Large language models are increasingly used as open-ended search operators in evolutionary optimization. We introduce Evolutionary Feature Engineering (EFE), a framework for using LLM-based evolution to discover preprocessing transformations for structured data. EFE represents transformations as Python programs with a standardized fit/transform interface, allowing them to be inserted directly into existing machine learning pipelines. During evolution, candidate programs are refined using dataset context, summary statistics, and downstream performance feedback on validation set. We instantiate EFE in two settings. For time-series forecasting, EFE-Time learns invertible, dataset-specific normalizations that improve off-the-shelf time-series foundation models. It reduces forecasting errors (MASE, WQL, MAE) 3% or more when averaged across datasets and improvements are as much as 19% on the COVID-Deaths dataset. Notably, these improvements occur with recent TSFMs such as Chronos-2. For tabular prediction, EFE-Tab evolves compact feature programs that add useful interpretable features and remove redundant ones, improving or matching existing LLM-based feature-engineering methods. We found EFE-Tab to be particularly effective on classical decision trees, where small sets of evolved features yield competitive accuracy while preserving interpretability. Overall, EFE demonstrates that LLM-based evolution can improve both accuracy and interpretability when automatically tackling structured data.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决结构化数据（时间序列和表格数据）中特征工程自动化的问题。研究背景是，虽然特征工程能显著提升模型性能，但传统方法依赖人工专家经验，难以预先指定针对特定数据集和下游模型的最优变换。现有方法如固定预处理库（如RevIN）或基于LLM的特征工程（如CAAFE、LLM-FE）存在不足：前者规则固定，无法适应所有数据模式（如趋势、尺度、异常值）；后者虽能生成特征，但未充分结合进化搜索与可逆变换，且对时间序列的时序约束和表格数据的可解释性关注不足。本文核心问题是：能否利用LLM驱动的进化搜索，自动发现针对结构化数据的可执行预处理程序，同时提升预测精度和模型可解释性？为此，作者提出EFE框架，将特征工程转化为进化搜索Python程序的过程，通过下游任务性能反馈和数据集上下文引导LLM生成变换。具体地，EFE-Time为时间序列基础模型进化可逆的归一化程序，EFE-Tab为表格数据进化简洁且可解释的特征程序，旨在平衡预测改进与特征复杂度。

### Q2: 有哪些相关研究？

相关研究可分为三类。**方法类**：CAAFE利用数据集描述生成语义特征交互，OCTree结合LLM推理与浅层决策树反馈，LLM-FE采用FunSearch式进化搜索优化表格特征变换程序。本文EFE与LLM-FE最接近，但区别在于：1）EFE同时覆盖时间序列与表格数据；2）为时间序列设计了可逆归一化程序（含fit/transform/inverse_transform接口）；3）遵循AlphaEvolve的全程序优化范式，而非仅优化特征变换片段。**应用类**：ELATE使用进化LLM搜索生成时间序列协变量，但未涉及可逆归一化，且因无可用代码库未作对比。**评测类**：GIFT-Eval提供时间序列基准，本文在其上验证EFE-Time对Chronos-2等基础模型的提升效果。与现有工作相比，EFE的核心创新在于将可逆归一化程序作为进化目标，使时间序列基础模型能在变换空间操作后逆变换回原始空间，同时通过惩罚复杂度实现表格特征的简约生成，特别适合保持下游模型可解释性的场景。

### Q3: 论文如何解决这个问题？

论文提出了一种名为进化特征工程（EFE）的框架，通过将大语言模型（LLM）作为进化优化中的变异算子，自动发现结构化数据的预处理变换。核心方法是将数据变换表示为遵循标准fit/transform接口的Python程序，这些程序可直接插入现有机器学习管道。整体框架包含一个进化循环：从恒等变换开始，每次迭代中，提示生成器向LLM提供数据集上下文、统计摘要、先前评估反馈和优秀程序示例，LLM据此提出修改后的变换程序。评估器检查程序的可执行性和无泄漏性，将其插入固定下游模型前，并相对于恒等基线进行评分。评分和反馈返回提示生成器，指导后续候选程序的改进。

主要模块包括：1）**程序表示**：每个候选程序包含fit、transform和post三个操作，分别用于拟合状态、应用变换和后处理。2）**评估协议**：对时间序列任务，使用滚动预测窗口；对表格任务，使用交叉验证折叠。3）**评分函数**：结合验证集性能提升、可靠性、运行时间和复杂度惩罚。4）**搜索策略**：从历史中选择父候选、变异算子和灵感示例，由LLM生成新候选。

创新点在于：1）**LLM驱动的进化搜索**：LLM作为变异算子，利用自然语言理解能力生成有意义的变换，而非随机变异。2）**可逆性约束**：EFE-Time限制搜索近似可逆程序，确保预测在变换空间进行后能正确逆变换回原始空间。3）**双场景适配**：EFE-Time针对时间序列预测，学习数据集特定的可逆归一化（如稳健缩放、去趋势、季节调整），提升基础模型性能；EFE-Tab针对表格预测，进化紧凑特征程序，添加有用可解释特征并移除冗余特征，在保持可解释性的同时提升决策树等模型的准确性。4）**实用导向设计**：评分函数包含复杂度惩罚和运行时间惩罚，防止过度工程化，确保进化出的变换简洁有效。

### Q4: 论文做了哪些实验？

论文在时间序列预测和表格数据预测两个场景下进行了实验。实验设置上，EFE-Time使用Chronos-2作为下游模型，在GIFT-Eval基准的10个数据集（涵盖医疗、能源、金融等领域）上，以验证集MASE改进为选择信号，运行100次迭代，报告MASE、WQL和MAE指标。主要结果：EFE-Time相比恒等变换平均改进3.0%（MASE）、3.6%（WQL）和3.7%（MAE），在CovidDeaths数据集上改进高达19.5%（WQL）。跨模型迁移实验中，针对Chronos-2优化的程序直接用于TimesFM-2.5、Moirai-2-Small和Reverso-Nano，在3个数据集上平均MASE改进超6%，在全部10个数据集上分别改进3.06%、2.25%和2.42%。此外，EFE-Time与微调结合产生加性增益，优于单独使用任一方法。EFE-Tab在TabArena的9个二分类数据集上，以TabPFN-v2为评分模型，与CAAFE和LLM-FE对比，发现其能发现紧凑且有用的特征程序，在经典决策树上保持可解释性的同时达到竞争性精度。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：1) 对部分平稳数据集改进不显著（如SZ_TAXI_15T改进为0%），说明EFE-Time对数据特性敏感；2) 仅使用Claude-Opus-4.6作为LLM骨干，未探索不同LLM的影响；3) 演化迭代次数固定为100，未研究收敛性与迭代数的关系；4) 表格任务仅使用TabPFN作为评分模型，未验证其他基模型。未来可探索：1) 引入自适应停止机制，根据改进幅度动态调整迭代次数；2) 结合多LLM投票或集成策略提升演化稳定性；3) 将EFE扩展到多模态数据预处理；4) 研究可解释性更强的演化程序，如自动生成自然语言描述；5) 探索EFE与模型微调的最佳组合策略，如交替优化预处理和模型参数；6) 在工业故障诊断场景中验证EFE对非平稳、含异常值时间序列的鲁棒性。

### Q6: 总结一下论文的主要内容

本文提出进化特征工程（EFE）框架，利用基于大语言模型的进化搜索自动发现结构化数据的预处理变换。针对时间序列预测，EFE-Time学习可逆的、数据集特定的归一化程序，在多个数据集上将预测误差降低3%以上，在COVID-Deaths数据集上最高达19%，且能提升Chronos-2等基础模型性能。针对表格预测，EFE-Tab进化紧凑的特征程序，在保持可解释性的同时提升决策树等模型的准确率。核心贡献在于：将特征工程形式化为有状态预处理程序的进化搜索，并证明基于LLM的进化能同时提升结构化数据任务的准确性和可解释性。
