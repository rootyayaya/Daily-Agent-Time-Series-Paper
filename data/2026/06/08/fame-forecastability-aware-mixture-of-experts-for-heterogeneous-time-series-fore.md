---
title: "FAME: Forecastability-Aware Mixture of Experts for Heterogeneous Time Series Forecasting"
authors:
  - "Qianyang Li"
  - "Xingjun Zhang"
  - "Shaoxun Wang"
  - "Tao Peng"
  - "Jia Wei"
date: "2026-06-08"
arxiv_id: "2606.08896"
arxiv_url: "https://arxiv.org/abs/2606.08896"
pdf_url: "https://arxiv.org/pdf/2606.08896v1"
github_url: "https://github.com/hit636/FAME"
categories:
  - "cs.AI"
tags:
  - "Mixture of Experts"
  - "时间序列预测"
  - "异构时间序列"
  - "专家路由"
  - "可预测性"
  - "工业数据集"
  - "零售预测"
  - "稀疏激活"
  - "模型选择"
  - "数据挖掘"
relevance_score: 6.5
---

# FAME: Forecastability-Aware Mixture of Experts for Heterogeneous Time Series Forecasting

## 原始摘要

Large-scale retail and industrial forecasting systems contain many heterogeneous time series whose lifecycle, sparsity, volatility, seasonality, spectral patterns, and contextual sensitivity differ substantially. A single forecasting model rarely performs well across all regimes, while dense ensembles increase inference cost and provide limited insight into expert suitability. This paper studies forecastability-aware expert routing: learning how data characteristics determine the suitability of forecasting experts. We propose \method{}, a sparse mixture-of-experts framework that represents each series with a multidimensional forecastability fingerprint, mines expert-suitability targets from validation performance, and trains a cost-aware sparse router to activate a small budgeted set of experts for each series. Using a production-scale vending-machine sales dataset from Shandong New Beiyang (SNBC), where the forecasting component has been integrated into the replenishment-planning pipeline, together with public retail benchmarks, we show that expert suitability varies systematically across data regimes. On the industrial dataset with 5,000+ machines and 60M+ transactions, \method{} Top-2 reduces MSE by 12.4\% over the strongest single expert, LightGBM, while executing 1.92 experts per series on average. The deployed component produces demand forecasts, while inventory-oriented gains are estimated by an offline replay simulator under a fixed replenishment policy rather than by online intervention. The framework turns heterogeneous sales forecasting from heuristic model selection into data mining of forecastability patterns and expert specialization. Code is available at https://github.com/hit636/FAME

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决大规模异构时间序列预测中“一刀切”模型效果不佳的问题。研究背景是，在零售、工业等实际场景中，存在大量生命周期、稀疏性、波动性、季节性等特征各异的异构时间序列，例如不同产品的销售数据。现有方法的不足在于：单一预测模型（如统计模型、树模型、深度学习模型）无法在所有数据形态下都表现优异，存在“没有免费午餐”的局限；而密集集成模型虽然能提升性能，但会显著增加推理成本，且难以解释每个专家模型的适用性。传统的基于规则的模型选择方法（如作者之前的USFF框架）依赖人工定义的阈值和评分，难以跨产品、区域和生命周期阶段迁移，且无法表达多个专家可能同时适用于同一序列的情况。因此，本文要解决的核心问题是：如何从数据特征出发，学习一个可学习的、连续的、成本感知的专家路由机制，为每条异构时间序列自动、高效地选择最合适的少量预测专家，从而在提升预测精度的同时控制推理成本。

### Q2: 有哪些相关研究？

在时间序列预测领域，相关研究主要分为三类。第一类是**零售预测方法**，包括针对季节性/间歇性序列的统计模型、利用协变量的树模型（如LightGBM）以及处理长历史非线性模式的深度模型。本文与这些方法的核心区别在于，FAME并非设计单一预测器，而是通过可路由的专家混合框架，根据序列特性动态选择最合适的预测器。第二类是**可预测性分析与元学习**，如FFORMA学习基于特征的模型加权权重，以及时间序列元学习将数据描述符与预测精度关联。FAME与它们有三点不同：采用稀疏Top-r激活而非密集组合；从验证损失中挖掘专家适用性作为监督信号；路由由显式的可预测性指纹驱动，保持可解释性。第三类是**混合专家模型（MoE）与AutoML**，如密集MoE和堆叠方法通常执行所有专家且缺乏解释性，AutoML则优化全局性能或返回单一流水线。FAME区别于这些方法：它从可预测性指纹学习可复用路由器，允许多个近优专家共享概率质量，并在显式推理成本约束下最多激活r个专家。此外，基础预测器如TimesFM、Chronos等与FAME互补，可作为高成本专家加入，由路由器判断其成本是否合理。

### Q3: 论文如何解决这个问题？

FAME提出了一种基于可预测性感知的稀疏专家混合框架，核心思想是通过数据特征动态路由到最合适的预测专家。整体框架包括四个主要模块：指纹提取、专家池构建、专家适用性挖掘和稀疏路由器。

首先，指纹提取模块为每个时间序列生成一个多维度的“可预测性指纹”，涵盖生命周期（如活跃天数）、稀疏性（零比率、ADI、CV²）、波动性（变异系数、突发性）、趋势与季节性强度、频谱特征（熵、频带能量）、元数据（品类、城市）以及上下文敏感性（节假日、天气影响）等8类特征。这些手工设计的特征比纯序列嵌入更鲁棒且可解释。

其次，专家池包含互补的统计模型（SARIMA、Croston）、机器学习模型（LightGBM、XGBoost）和深度学习模型（DLinear、TimesNet）。每个专家在训练集上预训练后，在验证集上计算每个序列的损失，从而生成“专家适用性目标”——可以是硬标签（最优专家）或软标签（通过softmax转换的损失分布）。

稀疏路由器是一个两层MLP，输入是指纹，输出各专家的概率。训练时采用KL散度使路由器分布逼近软适用性目标，并结合预测损失、负载均衡损失（防止专家坍缩）和成本正则化项。推理时采用Top-r预算，只激活概率最高的r个专家（实验中r=2），并对权重归一化融合预测。这种稀疏执行使平均每序列仅激活1.92个专家，大幅降低计算成本。

创新点在于：(1) 将模型选择转化为可预测性模式的数据挖掘问题；(2) 通过指纹实现可解释的路由决策；(3) 成本感知的稀疏路由在工业数据集上比最强单专家LightGBM降低12.4%的MSE。

### Q4: 论文做了哪些实验？

论文在工业数据集和公开零售基准上进行了实验。工业数据集来自山东新北洋（SNBC），包含5000+售货机、约5000种产品和6000万+交易，以产品-终端-天为预测单元，14天为预测周期，按70%/10%/20%划分训练、验证和测试集。对比方法包括10个单专家（SARIMA、Holt-Winters、Prophet、Croston/TSB、线性回归、XGBoost、LightGBM、DLinear、TimeMixer、TimesNet）以及密集集成（均匀集成、FFORMA风格加权、堆叠集成）和路由基线（USFF、聚类后预测、AutoML风格选择、密集软MoE、FAME变体）。主要结果：FAME Top-2在MSE上比最强单专家LightGBM降低12.4%（MSE从1.579降至1.384），MAE从1.348降至1.143，WAPE从0.157降至0.133，平均执行1.92个专家，归一化推理成本2.4。FAME Top-1 MSE降低10.0%，成本感知变体降低11.5%。验证选择的神谕参考MSE降低16.0%。路由质量通过Top-1准确率、Top-2/Top-3神谕召回率、使用熵和神谕差距评估。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：路由器的可解释性分析仍停留在特征重要性层面，未深入揭示专家选择与时间序列动态演化之间的因果关系；且验证仅依赖离线回放模拟，缺乏在线A/B测试对实际库存优化效果的验证。未来可探索的方向包括：1）引入因果推断或反事实推理，量化不同专家选择对下游补货决策的直接影响，实现从“相关性路由”到“因果路由”的升级；2）设计自适应指纹更新机制，使路由决策能随序列生命周期动态调整，避免冷启动阶段因指纹不准确导致的误分配；3）结合大语言模型（LLM）的语义理解能力，将非结构化上下文（如促销文案、天气描述）转化为路由特征，提升对突发性需求模式的响应能力；4）探索多目标路由优化，同时权衡预测精度、计算成本与库存服务水平，构建更贴近工业实践的端到端决策框架。

### Q6: 总结一下论文的主要内容

这篇论文提出了一种名为FAME（Forecastability-Aware Mixture of Experts）的框架，用于解决大规模异构时间序列预测中单一模型难以适应所有数据模式的问题。核心贡献在于将模型选择从启发式规则转化为数据挖掘问题，通过可学习的稀疏专家路由机制，根据每个序列的“可预测性指纹”（包括生命周期、稀疏性、波动性、季节性等特征）动态激活少量最合适的预测专家。方法上，FAME首先提取多维特征，然后基于验证性能挖掘专家适配性目标，并训练一个成本感知的稀疏路由器，在推理时仅调用预算内的Top-r个专家。在山东新北洋（SNBC）的5000+台自动售货机、6000万+交易数据的工业数据集上，FAME Top-2相比最强单一专家LightGBM降低了12.4%的MSE，平均每个序列仅执行1.92个专家。该工作不仅提升了预测精度，还通过可解释的专家选择揭示了不同数据模式与模型专长之间的系统关联，为工业异构预测系统提供了高效、可部署的解决方案。
