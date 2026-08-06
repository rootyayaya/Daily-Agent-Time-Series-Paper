---
title: "IMFACT: Counterfactual Explanations for Time Series via Intrinsic Mode Function Substitution"
authors:
  - "Udo Schlegel"
  - "Julian Rakuschek"
  - "Thomas Seidl"
  - "Andreas Holzinger"
  - "Tobias Schreck"
  - "Javier Del Ser"
date: "2026-08-05"
arxiv_id: "2608.04777"
arxiv_url: "https://arxiv.org/abs/2608.04777"
pdf_url: "https://arxiv.org/pdf/2608.04777v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "counterfactual explanations"
  - "time series"
  - "empirical mode decomposition"
  - "intrinsic mode functions"
  - "model-agnostic"
  - "plausibility"
  - "interpretability"
  - "fault detection"
relevance_score: 6.5
---

# IMFACT: Counterfactual Explanations for Time Series via Intrinsic Mode Function Substitution

## 原始摘要

Oscillatory signals, such as vibration, carry class-discriminative information in specific frequency bands; perturbing them in raw feature space for counterfactual analysis easily destroys their temporal structure and produces physically implausible results. In this work, we introduce IMFACT (IMF-based counterfACTuals), a model-agnostic framework for generating plausible counterfactual explanations for time series classifiers that operates in the decomposition space of Empirical Mode Decomposition. An input signal is split into Intrinsic Mode Functions (IMFs), and selected IMFs are progressively substituted with those of a Nearest Unlike Neighbour (NUN) until the classifier flips to the target class. We evaluate six IMF-selection strategies and a multi-NUN cycling extension on two UCR benchmarks (FaultDetectionA, FruitFlies). The variance-based strategy with three NUNs outperforms two prominent baseline techniques on reliability and plausibility metrics, while cycling across three NUNs yields the best proximity across both datasets.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在工业预测性维护、医疗诊断等高风险场景中，可解释性是可靠部署机器学习模型的必要前提。反事实解释作为事后解释方法，能回答“对输入做最小改动以改变预测结果”的问题，对决策支持至关重要。然而，对于振动等振荡信号，类别判别信息编码在特定频带中，现有方法（如Wachter、Native Guide、Glacier）直接在原始特征空间或学习到的潜空间中进行扰动，容易破坏信号的时序结构，产生违反频率约束、幅度越界或物理上不合理的波形，导致解释不可信。

本文提出IMFACT框架，核心创新在于将反事实生成的扰动空间从原始信号值转移到经验模态分解（EMD）的分解空间。通过将输入信号分解为固有模态函数（IMF），并逐步用最近异类样本（NUN）的IMF替换选中的IMF，直到分类器翻转至目标类别，从而在保留信号物理可解释的频率特性的同时生成反事实。该方法解决了现有方法在振荡信号上生成的反事实缺乏物理合理性和结构保真度的核心问题，实现了有效性与邻近性、合理性的平衡。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，Wachter等人提出基于梯度优化的模型无关反事实生成基线，但易产生全局弥散扰动；Native Guide通过最近异类样本（NUN）和类激活图引导扰动，保持时间连贯性；Glacier利用潜空间约束的梯度搜索；MASCOTS在符号特征空间操作，但难以处理长序列。**应用类**方面，Schlegel等人提出人机协同的反事实解释方法，侧重交互式诊断场景。**综述类**中，Schlegel和Seidl系统梳理了时间序列反事实方法，分为优化、进化、实例、潜空间、分段和混合六类，指出时间连贯性、合理性和可操作性为核心挑战。

本文与上述工作的核心区别在于：现有方法均在原始特征空间或潜空间扰动，未显式利用信号分解结构。IMFACT首次将经验模态分解（EMD）产生的固有模态函数（IMF）作为扰动空间，通过替换IMF实现反事实生成，既保留了信号的物理可解释性，又避免了原始空间扰动破坏振荡结构的问题。与Native Guide相比，IMFACT不依赖类激活图，而是通过IMF选择策略实现稀疏扰动；与MASCOTS相比，IMFACT能高效处理长序列。该工作填补了信号分解作为反事实扰动空间的空白，为振荡信号的可解释故障诊断提供了新范式。

### Q3: 论文如何解决这个问题？

IMFACT通过将反事实搜索从原始时间序列空间转移到经验模态分解（EMD）的固有模态函数（IMF）空间，解决了直接扰动原始特征会破坏振荡信号时间结构的问题。其核心框架包含四个阶段：首先，从训练集中检索目标类别的最近异类邻居（NUN）作为参考；其次，对查询信号和NUN分别进行EMD分解，得到按频率从高到低排列的IMF集合，并对齐IMF数量；然后，按照特定策略依次选择IMF，将查询的IMF替换为NUN的对应IMF，每替换一个就查询分类器，直到预测翻转为目标类别；最后，将未替换的IMF、替换后的IMF和查询自身的残差相加，生成反事实样本。

在IMF选择策略上，论文提出了六种方法，包括基于功率谱密度JS散度的距离策略、基于类间方差差异的方差策略、只选最强和最弱IMF的极值策略、从粗到细逐步解锁IMF的粗到细策略等。其中方差策略表现最优，因为它假设类间方差差异最大的模态携带最强的判别信息。此外，论文还引入了多NUN扩展，通过循环或最近邻策略从多个NUN中选取IMF，减少对单一邻居的依赖。

该方法的创新点在于：在分解空间中进行可解释的频带级扰动，保留残差以维持整体趋势，通过贪心逐次替换保证稀疏性，且查询预算仅与IMF数量线性相关而非信号长度，显著提高了计算效率。

### Q4: 论文做了哪些实验？

实验使用两个UCR基准数据集：FaultDetectionA（机电驱动系统振动信号，三分类）和FruitFlies（果蝇振翅信号，物种分类），采用SimpleCNN作为黑箱分类器（F1分别为0.99和0.87）。每个数据集随机选取50个测试实例，对比Wachter、Native Guide和Glacier三种基线方法，评估指标包括有效性、平均L2距离、改变百分比、范围有效性、自相关保持和运行时间。

主要结果：IMFACT在两个数据集上均达到100%有效性，是唯一在所有数据集上保持完全有效的方法。在FaultDetectionA上，Glacier的L2最低（8.788）但FruitFlies上有效性崩溃至36%；Wachter有效性仅58%和30%；Native Guide虽有效但运行时间比IMFACT慢约19倍。IMFACT在FruitFlies上取得最佳L2（0.922）和自相关（0.987），范围有效性达0.984，运行时间稳定在0.24-0.39秒。消融实验显示，variance策略最弱，distance+3个NUN+cycle为推荐默认配置。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从以下几个层面展开：

首先，当前评估仅基于两个数据集的采样子集和SimpleCNN架构，未来应在更多UCR基准、完整数据集及ResNet、InceptionTime、Transformer等深度模型上验证泛化性，并报告多种子置信区间。其次，方法局限于单变量序列，扩展至多变量需设计跨通道IMF对齐机制，这是重要突破口。

核心机制层面，EMD的模态混叠问题导致查询与NUN的IMF索引不对应物理意义，零填充启发式无法根治，可探索集成EMD或变分模态分解（VMD）以缓解。此外，贪心逐IMF替换无法保证全局最优，未来可引入组合优化或强化学习搜索更稀疏、更近的反事实。

计算效率上，方差策略虽迭代少但单步代价高，VMD或并行化可降低开销。评估指标需补充密度度量、对抗可检测性和人工评分，以更全面衡量真实性。最后，当前策略选择依赖数据集，未来应研究自适应策略选择机制，或设计统一默认配置，减少人工调参需求。

### Q6: 总结一下论文的主要内容

IMFACT提出了一种基于经验模态分解（EMD）的模型无关反事实解释框架，用于时间序列分类器。其核心思想是将输入信号分解为内在模态函数（IMFs），并逐步用最近异类样本（NUN）的对应IMF替换选定分量，直至分类器翻转至目标类别。该方法避免了在原始特征空间直接扰动导致的时序结构破坏和物理不可解释性问题。在FaultDetectionA和FruitFlies两个UCR基准上，评估了六种IMF选择策略及多NUN循环扩展。结果表明，基于方差策略配合三个NUN在可靠性和合理性上优于Wachter、Native Guide和Glacier等基线，且多NUN循环在邻近性上表现最佳。IMFACT是唯一在两个数据集上达到完全有效性的方法，同时保持较低且稳定的运行时间。该工作证明了信号分解原生扰动空间对生成物理合理的时间序列反事实解释的有效性，尤其适用于振动等频域判别信息关键的场景。
