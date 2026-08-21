---
title: "Rethinking Patch Based Multivariate Time Series Forecasting with Semantic Structured Partitioning"
authors:
  - "Jiazhe Wang"
  - "Zhiquan Huang"
  - "Linjing Xue"
  - "Ming Liu"
  - "Meiwen Li"
  - "Ruijuan Zheng"
date: "2026-08-20"
arxiv_id: "2608.19966"
arxiv_url: "https://arxiv.org/abs/2608.19966"
pdf_url: "https://arxiv.org/pdf/2608.19966v1"
categories:
  - "cs.AI"
tags:
  - "multivariate time series forecasting"
  - "semantic structured partitioning"
  - "patch-based forecasting"
  - "dynamic semantic graph"
  - "importance-aware routing"
  - "expert modeling"
  - "Transformer"
relevance_score: 7.5
---

# Rethinking Patch Based Multivariate Time Series Forecasting with Semantic Structured Partitioning

## 原始摘要

Multivariate time series forecasting (MTSF) is a fundamental task in many real world applications. Existing patch based forecasting methods generally fall into three categories: fixed partitioning, multi-scale partitioning, and extendable partitioning. Fixed partitioning often breaks meaningful temporal boundaries, multi-scale partitioning may introduce redundant representations across scales, and extendable partitioning improves flexibility but still lacks an explicit mechanism for organizing semantic structure and modeling interactions among heterogeneous temporal patterns. To address these limitations, we propose SCPaT, a Transformer based framework built on semantic structured partitioning. SCPaT first decomposes input sequences into semantically consistent units through adaptive semantic unit generation, then constructs a dynamic semantic graph to model directed dependencies among these units and organize them into higher order semantic blocks. Based on these structured representations, an importance aware routing mechanism adaptively dispatches different semantic blocks to different experts for customized modeling. Extensive experiments on 12 real world datasets demonstrate the effectiveness of SCPaT.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

多变量时间序列预测（MTSF）在电力负荷、气象和交通流量等实际应用中至关重要。基于patch的建模方法通过将长序列分割为时间片段来捕捉复杂时序依赖，但现有分割策略存在根本性缺陷：固定分割常破坏有意义的时序边界，难以应对趋势突变；多尺度分割虽能捕捉多粒度信息，却易在跨尺度整合时引入冗余表征，尤其在依赖关系复杂的数据中难以解耦异质动态模式；可扩展分割虽提升灵活性，但依赖启发式规则确定分割粒度，缺乏对高阶依赖和异质模式间交互的显式建模能力。

这些方法的共同本质问题在于：它们都将patch生成视为几何预处理步骤，而非语义建模任务，未能显式考虑时间片段的内在语义一致性，也未建模异质时序模式间的结构化交互关系。当趋势、周期性和突变共存于同一序列时，现有方法缺乏原则性机制来解耦这些成分并建立结构化关联。

为此，本文提出SCPaT框架，通过语义结构化分割构建嵌入语义结构的表征系统：首先自适应生成语义一致的时间单元，再构建动态语义图建模单元间的有向依赖并组织为高阶语义块，最后通过重要性感知路由机制将不同语义块分配给不同专家进行定制化建模，从而系统性地解决现有分割策略在语义保持和结构交互上的核心缺陷。

### Q2: 有哪些相关研究？

相关研究主要围绕基于Transformer的多元时间序列预测方法展开，可分为三类。**固定划分方法**以PatchTST为代表，将序列切分为等长补丁以提升表示效率，但易破坏时间边界、导致语义不一致。**多尺度划分方法**如TimesNet和FEDformer，通过不同尺度捕捉局部与全局模式，但可能引入跨尺度的冗余表示。**可扩展划分方法**如HDMixer，采用长度自适应补丁动态调整边界，增强灵活性，但仍缺乏对语义结构和异质模式间交互的显式建模。此外，iTransformer通过变量维度重组增强跨变量依赖，Pathformer利用多尺度补丁和自适应路径捕获上下文，Fredformer通过频率去偏缓解高频偏差，但这些方法均未从语义结构角度重新定义补丁生成。

与上述工作不同，SCPaT将补丁生成从几何划分问题重构为语义结构问题：通过自适应语义单元生成分解序列，构建动态语义图建模单元间有向依赖，并组织为高阶语义块，再通过重要性感知路由将不同块分配给不同专家。这使其能显式区分趋势、周期和突变等异质动态，并建模其复杂交互，弥补了现有方法在细粒度语义变化和高阶时序依赖建模上的不足。

### Q3: 论文如何解决这个问题？

SCPaT提出了一种基于语义结构化分区的Transformer框架，核心思想是将多变量时间序列分解为语义一致的单元，并建模它们之间的有向依赖关系。整体框架包含四个主要模块：

**语义向量编码器**：首先通过多尺度时间卷积（不同核大小和膨胀因子）提取局部时序特征，再利用可学习的融合权重自适应整合多尺度信息。随后基于局部方差准则进行自适应语义单元划分——在平稳区域分配较长单元，在剧烈变化区域分配较短单元，每个单元通过均值池化和两层MLP编码为固定维度的语义表示。

**动态语义图构建**：提出可微分的传递熵（Transfer Entropy）替代指标来量化语义单元间的有向依赖强度。该指标通过3层MLP学习条件互信息代理，并计算样本标准差以抑制不稳定依赖。基于此构建稀疏有向图（保留Top-K边），再通过最大化有向加权模块度进行图聚类，形成高阶语义块。

**语义块路由**：每个语义块通过注意力机制聚合单元表示，并附加块统计特征（规模、出入强度、时间跨度）。块间邻接图通过均值聚合邻居信息，最终由重要性感知路由机制将不同语义块分配给不同的专家网络进行定制化建模。

**创新点**在于：1）用方差引导的自适应分区替代固定补丁划分，保留语义边界；2）用可学习的传递熵代理捕获非对称非线性依赖，优于相关矩阵方法；3）通过模块度聚类组织高阶结构，配合路由机制实现异构时序模式的差异化建模。整个框架端到端训练，聚类步骤无参数，避免非平滑优化问题。

### Q4: 论文做了哪些实验？

论文在12个公开基准数据集上进行了长短期预测实验。长期预测使用ETTh1/ETTh2/ETTm1/ETTm2、Weather、Traffic、Electricity和Solar共8个数据集，输入长度固定为96，预测长度H∈{96,192,336,720}；短期预测使用PEMS03/04/07/08四个交通流数据集。对比方法涵盖9种代表性基线：Transformer类（PatchTST、iTransformer、DUET、MSPatch、Crossformer）、CNN类（TimesNet）、GNN类（MSGNet）、MLP类（HDMixer）及LSTM。所有模型在PyTorch 2.1.2下统一实现，使用单张RTX 4090D GPU，基线采用原论文最优超参数重新训练，SCPaT通过网格搜索选择语义偏置参数。评估指标为MSE和MAE。主要结果：SCPaT在ETTh1、ETTh2、ETTm1、ETTm2、Weather、Traffic、Electricity、Solar等多数数据集和预测长度上取得最优或次优结果，例如ETTh1在H=96时MSE为0.370（优于MSPatch的0.372），Electricity在H=96时MSE为0.139（显著优于DUET的0.148），Traffic在H=96时MSE为0.393（优于DUET的0.395）。SCPaT在长短期预测任务中均展现出稳定优势，尤其在复杂多元时序上表现突出。

### Q5: 有什么可以进一步探索的点？

SCPaT虽在语义分区上有所突破，但仍有若干可探索空间。首先，语义单元生成依赖自适应算法，其可解释性较弱，未来可引入显式的领域知识（如物理规则或业务周期）作为约束，增强分区的可理解性与鲁棒性。其次，动态语义图的构建与更新计算开销较大，尤其在长序列或高频场景下，可探索图稀疏化或增量学习策略以提升效率。第三，当前专家路由机制基于重要性权重，但未考虑专家间的协同或冲突，可设计元学习层来动态调整专家组合。此外，SCPaT在非平稳或分布漂移数据上的表现未充分验证，未来可结合在线适应或因果发现技术，提升跨域泛化能力。最后，将语义块与多模态信号（如外部事件）融合，或能进一步丰富时序表征，值得尝试。

### Q6: 总结一下论文的主要内容

本文针对多元时间序列预测中现有patch分割策略的局限性，提出了一种基于语义结构化分割的Transformer框架SCPaT。现有方法分为固定分割、多尺度分割和可扩展分割三类，但均未显式建模时间段的语义一致性和异构模式间的高阶结构交互。SCPaT首先通过自适应语义单元生成将输入序列分解为语义一致的单元，随后构建动态语义图以建模单元间的有向依赖关系，并将其组织为高阶语义块。最后，基于重要性感知的路由机制将不同语义块自适应分配给不同专家进行定制化建模。在12个真实数据集上的实验表明，SCPaT在长期和短期预测任务中均达到最先进性能。该工作的核心贡献在于将patch生成从几何预处理提升为语义建模任务，系统分析了现有策略的不足，并提出了融合层次语义块与路由机制的创新框架，为复杂时间序列预测提供了新思路。
