---
title: "Personalized Federated Sparse Adaptation of Time-Series Foundation Models"
authors:
  - "Priyanka Nihalchandani"
  - "Naman Srivastava"
  - "Varun Ojha"
  - "Pandarasamy Arjunan"
date: "2026-08-05"
arxiv_id: "2608.04695"
arxiv_url: "https://arxiv.org/abs/2608.04695"
pdf_url: "https://arxiv.org/pdf/2608.04695v1"
categories:
  - "cs.LG"
  - "cs.AI"
  - "stat.ML"
tags:
  - "Time-Series Foundation Models"
  - "Federated Learning"
  - "Mixture-of-Experts"
  - "Sparse Adaptation"
  - "Building Energy Forecasting"
  - "Personalization"
  - "Heterogeneous Temporal MoE"
  - "Routing"
relevance_score: 7.5
---

# Personalized Federated Sparse Adaptation of Time-Series Foundation Models

## 原始摘要

Federated adaptation of time-series foundation models (TSFMs) is attractive for building energy forecasting because meter data are private, distributed, and highly non-IID. However, a single parameter-sharing strategy is unlikely to serve all pretrained TSFMs or building clients: fully shared adapters can suppress building-specific temporal behavior, while fully local adaptation discards cross-building transfer. We propose a personalized federated sparse adaptation framework with a heterogeneous temporal mixture-of-experts (MoE) adapter placed after the pretrained TSFM representation. A sequence-level router maps each 168-hour context window to a top-$k$ subset of experts specialized for periodicity, long-range interactions, local variation, trend-residual structure, and multi-resolution behavior. We compare global FL, local training, and personalized FL variants with globally shared or client-private expert banks. Across 50 buildings and three TSFM backbones, personalization consistently outperforms Global FL-MoE and Local MoE, while the best sparse-adaptation strategy varies by backbone and metric. Routing behavior further reveals client-level expert specialization, expert concentration, and near-uniform routing across backbones, showing that federated TSFM adaptation should be both client-aware and backbone-aware.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列基础模型（TSFMs）在建筑能耗预测中展现出强大的迁移能力，但建筑级电表数据因隐私和所有权限制难以集中训练，联邦学习（FL）成为自然选择。然而，现有方法面临核心矛盾：完全共享适配器会抹平建筑特有的时间动态（如 occupancy 节奏、季节敏感性），而完全本地训练则丢弃跨建筑的可迁移知识。这种高度非独立同分布（non-IID）的客户端分布，使得单一参数共享策略无法适配所有预训练 TSFM 或建筑客户端。本文旨在解决“如何在联邦框架下实现个性化稀疏适配”这一核心问题——即在不共享原始数据的前提下，通过设计一个异构时间专家混合（MoE）适配器，利用序列级路由将每个168小时上下文窗口映射到专门捕捉周期性、长程交互、局部变化、趋势残差和多分辨率行为的 top-k 专家子集，从而在共享与本地化之间取得平衡。作者进一步探究不同 TSFM 骨干（MOMENT、Chronos-2、Moirai）下最优适配策略的差异性，并揭示专家利用模式，证明联邦 TSFM 适配必须同时考虑客户端特性和骨干网络特性，而非采用通用流程。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**上，时间序列基础模型（TSFM）如MOMENT、Chronos、Moirai通过大规模预训练学习可迁移表示，本文沿用其作为骨干网络，但聚焦于联邦场景下的稀疏适配，而非零样本或全量微调。**联邦与个性化学习类**中，FedAvg在非独立同分布数据下性能退化，个性化联邦学习（如分离共享表示与客户端私有参数）被广泛探索，近期如pFedDKS引入选择性知识共享。本文区别于这些工作之处在于：首次系统研究预训练TSFM的稀疏专家适配器在联邦建筑能耗场景中应如何共享或个性化，而非仅调整头部或正则化目标。**稀疏专家与时序归纳偏置类**中，稀疏混合专家（MoE）已用于联邦能源预测，但现有专家库多为通用设计。本文创新性地将专家显式编码为周期性、长程依赖、局部变化、趋势残差和多分辨率五种时序归纳偏置，并分析路由行为以揭示骨干网络和客户端对专家的利用模式。总体而言，本文填补了“TSFM + 联邦个性化 + 稀疏时序专家”交叉领域的空白，强调适配策略需同时感知客户端数据分布和骨干网络架构。

### Q3: 论文如何解决这个问题？

论文提出了一种个性化联邦稀疏适配框架，用于解决时间序列基础模型在建筑能耗预测中面临的数据非独立同分布和客户端异质性问题。其核心思想是在冻结的预训练骨干网络之后引入一个轻量级的稀疏混合专家适配器，通过残差更新机制对表征进行个性化调整。

整体框架包含三个主要模块：首先是预训练骨干网络（MOMENT、Chronos-2或Moirai），用于提取隐藏表征；其次是核心的异构时间混合专家适配器，包含五个具有互补归纳偏置的专家——傅里叶专家捕捉周期性、注意力专家建模长程交互、卷积专家处理局部多尺度变化、分解专家分离趋势与残差、小波专家提取时频特征；最后是序列级路由器，通过对上下文窗口的隐藏表征进行池化，为每个168小时窗口选择top-k个最相关的专家。

该方法的创新点体现在三个方面：一是采用序列级稀疏路由而非补丁级路由，使专家选择更稳定且易于解释；二是设计了共享与私有的灵活参数划分策略，支持全局共享专家库或客户端私有专家库两种变体；三是引入可学习的残差门控机制，确保适配器初始时仅作为轻微修正，不破坏预训练表征。训练过程采用联邦优化，共享参数通过样本加权FedAvg聚合，私有参数在本地更新，最终通过冻结共享参数、仅微调私有参数完成个性化。此外，还引入了负载均衡和路由正则化损失，防止专家坍缩。

### Q4: 论文做了哪些实验？

实验基于ASHRAE Great Energy Predictor III数据集中50栋非住宅建筑的每小时用电数据，每栋建筑作为一个联邦客户端，形成非IID跨建筑预测基准。数据按时间顺序划分50%训练、25%验证、25%测试，使用168小时上下文窗口预测未来24小时。评估采用NRMSE和sMAPE指标，报告50个客户的中位值。

实验在三个预训练时间序列基础模型（MOMENT-1-large、Chronos-2、Moirai-1.1-R-small）上评估，对比零样本、全局FL-MoE、本地MoE、无MoE的PFL、共享专家PFL-MoE、私有专家PFL-MoE及LoRA变体。联邦训练设置15轮通信、20%客户端参与率、每客户端5个本地epoch，采用覆盖优先的客户端选择策略和FedAvg聚合。

主要结果显示个性化变体相对全局FL-MoE降低NRMSE：MOMENT降低8.2%（最佳12.769）、Chronos-2降低7.1%（最佳10.559）、Moirai降低12.5%（最佳12.429）。私有专家PFL-MoE在统计检验中显著优于全局FL-MoE。消融实验涵盖专家库组成（四专家变体）、路由稀疏度（top-1/2/5）、优化器（FedProx）、客户端选择和LoRA适配。路由行为分析显示MOMENT展现建筑特定专家选择，Chronos-2集中选择少数专家，Moirai均匀使用专家库。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：其一，专家路由策略依赖预定义的专家类型（如周期性、长程交互等），可能无法覆盖所有建筑负载的动态模式；其二，实验仅基于50栋建筑和三种TSFM骨干，结论的泛化性有待验证；其三，当前框架未考虑客户端计算/通信资源异构性，稀疏专家选择可能不适用于资源受限场景；其四，路由决策缺乏可解释性分析，难以理解专家选择与建筑特征（如气候、用途）的因果关联。

未来可从以下方向探索：一是设计元学习或在线学习机制，让路由器和专家分配策略能根据新客户端数据流自适应调整，避免静态专家库的局限；二是引入因果推断或注意力可视化，揭示专家选择与建筑物理特性的深层关系，提升模型可信度；三是结合差分隐私或安全聚合，在保持个性化效果的同时强化隐私保障；四是探索跨领域迁移，将骨干感知的个性化联邦适配框架推广到交通、医疗等其它时间序列任务，验证其通用性；五是研究通信-精度帕累托最优的稀疏化策略，例如基于梯度贡献度动态剪枝专家参数，降低联邦通信开销。

### Q6: 总结一下论文的主要内容

该论文提出了一种面向时间序列基础模型（TSFM）的个性化联邦稀疏适配框架，用于解决建筑能耗预测中数据隐私、分布非独立同分布（non-IID）及客户端异质性问题。方法在预训练TSFM表示后引入异构时间混合专家（MoE）适配器，通过序列级路由器将168小时上下文窗口映射到针对周期性、长程交互、局部变化、趋势残差及多分辨率行为的top-k专家子集，并对比全局共享与客户端私有专家库的联邦学习变体。在50栋建筑和三种TSFM骨干上的实验表明，个性化适配始终优于全局联邦MoE，且多数情况下优于局部训练；最优稀疏策略因骨干网络和评估指标而异。路由分析揭示了客户端级专家专业化、专家集中度及跨骨干近似均匀路由现象，证明联邦TSFM适配需同时考虑客户端感知与骨干感知，且不存在普适的最优个性化策略，未来需动态学习专家共享程度。
