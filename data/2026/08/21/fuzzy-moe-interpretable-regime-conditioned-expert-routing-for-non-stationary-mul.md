---
title: "Fuzzy-MoE: Interpretable Regime-Conditioned Expert Routing for Non-Stationary Multivariate Time Series Forecasting"
authors:
  - "Lan Guo"
  - "Jie Xiao"
  - "Zhao Su"
  - "Jun Shen"
  - "Haoran Li"
  - "Weixia Ma"
  - "Qingguo Zhou"
  - "Binbin Yong"
date: "2026-08-21"
arxiv_id: "2608.20761"
arxiv_url: "https://arxiv.org/abs/2608.20761"
pdf_url: "https://arxiv.org/pdf/2608.20761v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Mixture-of-Experts"
  - "Interpretable Routing"
  - "Non-Stationary Time Series"
  - "Multivariate Forecasting"
  - "Fuzzy Logic"
  - "Latent State Identification"
  - "Expert Selection"
  - "Mechanism Transparency"
relevance_score: 7.5
---

# Fuzzy-MoE: Interpretable Regime-Conditioned Expert Routing for Non-Stationary Multivariate Time Series Forecasting

## 原始摘要

In non-stationary multivariate time series, different variables and samples often exhibit heterogeneous latent dynamic states, while existing deep forecasting models usually compress them into a unified end-to-end mapping, leading to suboptimal modeling of time-varying dynamics and limited interpretability regarding which forecasting mechanism is activated under different latent states. To overcome these limitations, we reformulate time series forecasting as a unified framework of latent temporal state identification and interpretable expert routing, and propose Fuzzy-MoE, a fuzzy logic-based dynamic Mixture-of-Experts model. Fuzzy-MoE consists of multiple parallel expert mapping networks and a dual-view fuzzy router. By jointly exploiting local convolutional dynamics and global segmented statistics, the router infers latent temporal states and computes expert activation strengths through learnable Gaussian membership functions, enabling explicit IF-THEN rule-based expert selection. This fine-grained routing strategy allows different variables within the same sequence to activate different experts, effectively capturing heterogeneous temporal dynamics while improving model interpretability. Experimental results on multiple public time series benchmark datasets show that Fuzzy-MoE significantly outperforms mainstream forecasting methods in forecasting accuracy. Moreover, fuzzy memberships and rule activations provide interpretable routing diagnostics, demonstrating the effectiveness of the proposed framework in both forecasting performance and mechanism transparency. Unlike traditional MoE models that use black-box routing, Fuzzy-MoE`s routing is based on clear, interpretable fuzzy rules. This makes the expert selection transparent and traceable.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

非平稳多元时间序列预测在众多实际应用中至关重要，但其固有的异质性——即不同时间片段和同一观测窗口内不同变量往往呈现不同的潜在动态状态——构成了核心挑战。现有深度预测模型通常将所有输入压缩进一个统一的端到端映射，无法显式识别当前输入受哪种潜在状态支配，导致对时变动态的建模次优。近期基于混合专家（MoE）的方法虽引入多个专家网络以覆盖不同模式子空间，但其路由机制仍依赖黑盒线性投影加Softmax门控，不仅缺乏可解释性（无法回答“为何选择该专家”），还易出现门控坍缩问题，即少数专家主导所有输入而其余专家退化，严重限制了模型在高风险领域的可信度与可部署性。为此，本文重新定义预测任务，提出Fuzzy-MoE框架，将预测转化为“潜在时间状态识别+可解释专家路由”的两阶段过程。其核心创新在于设计双视角模糊路由器，融合局部卷积动态与全局分段统计，通过可学习高斯隶属函数生成显式IF-THEN规则，实现样本-通道级别的细粒度专家分配，使同一序列中不同变量可激活不同专家，从而在提升预测精度的同时提供完全可追溯的决策路径，解决现有方法在动态异质性建模与机制透明度上的双重不足。

### Q2: 有哪些相关研究？

时间序列预测的相关研究可分为三类。**传统与机器学习方法**（如ARIMA、SVR）仅能处理平稳线性数据或依赖手工特征，无法捕捉深层非线性时序模式。**深度预测模型**是主流方向：Transformer类（PatchTST、iTransformer）通过自注意力建模全局依赖，TimesNet利用傅里叶变换捕获周期变化，Autoformer和FEDformer分别引入自相关和频域增强。但这些模型均采用单一映射网络，难以适应非平稳序列中变量和片段间的异质动态状态。**可解释性与MoE方法**方面，后验解释（如注意力可视化）常与实际决策脱节；内在可解释模型（如TFT）仅停留在输入重要性归因层面。MoE模型（Switch Transformer、GLaM）虽通过多专家扩展容量，但现有时间序列MoE的门控机制本质是黑盒线性投影加Softmax，缺乏细粒度模糊条件规则。部分分布漂移感知模型虽按聚类分配专家，但可解释性仅限简单模式匹配。

本文与上述工作的核心区别在于：Fuzzy-MoE首次将模糊逻辑引入MoE路由，通过局部卷积与全局分段统计的双重视角推断潜在时序状态，用可学习高斯隶属函数生成显式IF-THEN规则，实现变量级细粒度专家分配。相比黑盒门控和简单聚类匹配，该方法既捕获了异质动态，又提供了可追溯的路由诊断，填补了可解释MoE在非平稳多变量预测中的空白。

### Q3: 论文如何解决这个问题？

Fuzzy-MoE通过将非平稳多元时间序列预测重构为“潜在时序状态识别+可解释专家路由”的统一框架来解决传统端到端模型难以捕捉异质动态状态且缺乏可解释性的问题。整体架构包含五个核心模块：输入归一化与分段、双视角状态特征提取、双视角模糊路由、专家映射网络以及加权融合与输出恢复。

在特征提取阶段，模型采用两条互补路径：局部卷积路径利用1D卷积独立提取每个变量的短期模式和突变特征；全局分段统计路径通过计算各段均值捕捉长期趋势和周期特性。核心创新在于双视角模糊路由器，它由卷积模糊门和全局模糊门组成，每个门包含三个步骤：首先通过多层投影网络将高维特征映射到低维可解释模糊变量空间；然后为每个专家维护可学习的高斯隶属函数参数（中心和标准差），计算样本对各专家条件的隶属度，并通过乘积T范数聚合得到规则触发强度；最后对具有明确物理语义的触发强度施加温度缩放的Softmax归一化生成门控权重。

该方法的关键创新点包括：一是以样本-通道粒度独立生成专家权重，使同一序列中不同变量可激活不同专家；二是用可解释的模糊规则替代传统MoE的黑盒路由，使专家选择过程透明可追溯；三是每个专家采用自适应残差结构，在线性和非线性时序拟合间动态平衡。整个框架将预测过程分解为可独立检查的“状态识别”和“专家预测”两个阶段，显著提升了模型的可解释性和预测精度。

### Q4: 论文做了哪些实验？

论文在6个公开数据集（ETTh1、ETTh2、ETTm1、ETTm2、Weather、Electricity）上进行了多组实验，预测长度设为96、192、336、720。以MSE和MAE为评估指标，对比了7个主流基线模型：WPMixer、SDE、TimeMixer、iTransformer、Time-MoE、PatchTST和DLinear。实验设置方面，模糊变量维度为3，使用SGD优化器（初始学习率2e-5），训练200轮，dropout为0.05，batch size为64，在单张NVIDIA 3090 GPU上运行。

主要结果显示Fuzzy-MoE在绝大多数设置下取得最优或次优性能。以Electricity数据集720步预测为例，Fuzzy-MoE达到MSE=0.203、MAE=0.294，相比iTransformer（MSE=0.228、MAE=0.313）分别降低10.96%和6.07%的误差。

此外，论文还进行了多项分析实验：在ETTh2上可视化专家路由权重，验证模糊门控能避免专家坍缩并促进专家特化；通过删除不同激活强度的模糊规则进行消融，发现删除高激活规则导致MAE显著上升（ETTh1上ΔMAE=0.012），而删除低激活规则影响极小（ΔMAE=0.001），证明规则有效性；对模糊温度参数τ进行敏感性分析，发现τ=5时性能最优；t-SNE可视化显示局部与全局分支融合后的表征更具判别性；将模糊门控替换为传统MLP门控的对比实验表明，模糊门控在ETTh2的96步预测中MSE降低10.56%、MAE降低7.73%，验证了模糊路由机制的优势。

### Q5: 有什么可以进一步探索的点？

Fuzzy-MoE虽在非平稳多变量预测中表现优异，但其局限性也为后续研究提供了明确方向。首先，当前模糊规则基于离线静态数据提取，难以应对概念漂移或在线流式场景，未来可引入在线参数更新或增量式规则演化机制，使路由决策自适应新数据分布。其次，双视图路由依赖卷积与分段统计，对超长序列或高频噪声可能不够鲁棒，可探索更细粒度的状态表征（如基于Transformer的隐状态分解）以提升规则判别力。再者，全量专家激活带来计算开销，稀疏激活（如Top-k门控）与模糊规则的结合值得尝试，但需保持规则可解释性。此外，当前规则以固定高斯隶属度函数表达，可考虑学习可微的模糊逻辑算子，使规则更贴合数据非线性。最后，该框架虽为通用路由模板，但跨领域迁移（如金融、医疗）时需验证规则的可移植性，未来可设计元学习机制以快速适配新任务。

### Q6: 总结一下论文的主要内容

本文提出Fuzzy-MoE，一个基于模糊逻辑的可解释混合专家模型，用于非平稳多元时间序列预测。传统深度模型将预测视为端到端映射，难以捕捉不同变量和样本的异质动态状态，且路由机制缺乏可解释性。Fuzzy-MoE将预测重构为潜在时序状态识别与可解释专家路由的统一框架，通过双视角模糊路由器（局部卷积动态与全局分段统计）提取状态线索，利用可学习高斯隶属函数生成显式IF-THEN规则，实现样本-通道级别的专家分配。实验表明，该方法在ETT、Weather和Electricity等基准数据集上显著优于主流预测方法，且模糊隶属度与规则激活提供了可追溯的路由诊断，验证了模型在预测精度与机制透明度上的双重优势。
