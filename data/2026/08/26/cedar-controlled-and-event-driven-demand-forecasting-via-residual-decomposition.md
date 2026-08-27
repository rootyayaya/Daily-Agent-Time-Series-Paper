---
title: "CEDAR: Controlled and Event-Driven Demand Forecasting via Residual Decomposition"
authors:
  - "Junjie Meng"
  - "Ranxu Zhang"
  - "Zi-an Zhang"
  - "Shujun Liu"
  - "Xiaoning Qi"
  - "Xiaozhou Xu"
  - "Yanyong Zhang"
  - "Hui Xiong"
  - "Chao Wang"
date: "2026-08-26"
arxiv_id: "2608.25871"
arxiv_url: "https://arxiv.org/abs/2608.25871"
pdf_url: "https://arxiv.org/pdf/2608.25871v1"
categories:
  - "cs.LG"
tags:
  - "Time Series Forecasting"
  - "Decision-Conditioned Forecasting"
  - "LLM-Assisted Event Alignment"
  - "Residual Decomposition"
  - "E-commerce Demand Forecasting"
  - "Counterfactual Simulation"
  - "Action-Conditioned Transformer"
relevance_score: 7.5
---

# CEDAR: Controlled and Event-Driven Demand Forecasting via Residual Decomposition

## 原始摘要

Forecasting in large-scale e-commerce marketplaces is increasingly required to support planning: merchants need to evaluate sales outcomes under future action sequences such as budget schedules, rather than passively predicting what happens next. However, most existing time series forecasting (TSF) approaches remain inherently passive. Even when incorporating operational decisions as auxiliary covariates, they typically optimize for correlation-based extrapolation under historical policies. This design suffers from autoregressive inertia and conflates endogenous market evolution with decision-induced transitions, leading to policy-insensitive rollouts and unreliable counterfactual analysis. To bridge this gap, we propose CEDAR (Controlled and Event-Driven Demand forecasting via Action-aware Residual decomposition), a two-stage framework for robust decision-conditioned simulation. In Stage I, an Action-Interleaved Transformer learns controllable action-conditioned state transitions for rollout under planned interventions. In Stage II, a Residual Correction Module leverages external event signals and LLM-assisted text representations to align noisy event descriptions with product context and correct event-driven deviations. Our study is enabled by a large-scale real-world dataset from Alibaba 1688, comprising approximately 32 million product trajectories with paired state-action sequences and aligned event signals. Extensive offline experiments and online controlled experiments in production demonstrate that CEDAR consistently improves simulation accuracy over strong TSF baselines and delivers practical gains for real-world budget planning.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在大规模电商平台（如阿里巴巴1688）中，商家需要根据未来的预算安排、促销活动等行动计划来评估销售结果，因此预测的核心从“被动预测未来”转向“决策条件模拟”——即在给定历史状态/动作和未来动作序列下，模拟需求轨迹。然而，现有时间序列预测（TSF）方法本质上是被动的：即使将运营决策作为协变量融入，它们仍基于历史策略进行相关性外推，存在两大缺陷：一是自回归惯性导致对反事实动作计划不敏感；二是将内生市场演化与决策引发的转变混为一谈，无法区分动作效应与非平稳外生冲击。这种设计导致策略不敏感的滚动预测和不可靠的反事实分析，难以支撑真实预算规划。为此，本文提出CEDAR框架，通过两阶段解耦解决核心问题：第一阶段用动作交织Transformer显式建模动作驱动的状态转移（s_{t-1}→a_t→s_t），确保在新型动作序列下滚动稳定；第二阶段用残差校正模块结合外部事件信号和LLM文本表示，分离并校正非平稳外生冲击，避免动作效应被错误归因。最终实现可靠的决策条件模拟，提升电商预算规划的实用效果。

### Q2: 有哪些相关研究？

时间序列预测（TSF）方法经历了从统计模型、循环神经网络到Transformer架构及大规模基础模型的演进。Informer、Autoformer、FEDformer、PatchTST和iTransformer等代表性工作分别通过稀疏注意力、分解机制、频域学习和补丁化表示提升了预测性能。另一条并行研究线关注协变量融合，其中Temporal Fusion Transformer（TFT）通过变量选择网络和门控机制整合历史观测与已知未来输入，但其本质仍是协变量条件预测，建模$p(s_{t+1}|s_{\le t}, a_{\le t})$，缺乏显式的动作条件状态转移学习，在策略偏移下鲁棒性不足。

离线强化学习领域，Decision Transformer（DT）开创了条件序列建模范式，Trajectory Transformer及后续的Online DT、QDT、VDT等扩展通过返回条件、优势加权和价值正则化提升了控制性能，但这些方法旨在学习隐式最优策略，而非显式可控的状态转移机制，不适用于商户预算规划中多策略对比的what-if仿真需求。

因果生成建模方面，DoFlow强调引入因果流以实现鲁棒的干预和反事实时间序列预测，但CEDAR与之不同，其核心是分离内生市场动态与动作诱导转移，通过两阶段残差分解框架显式学习动作条件转移算子，并结合外部事件信号与LLM文本表示进行偏差校正。相比TFT的协变量融合和DT的策略推断，CEDAR聚焦于决策条件下的稳定多步轨迹仿真，更契合电商场景中策略评估与反事实分析的实际需求。

### Q3: 论文如何解决这个问题？

CEDAR通过两阶段解耦框架解决决策条件模拟中的被动预测与因果混淆问题。整体架构分为Stage I和Stage II两个核心模块。

Stage I提出Action-Interleaved Transformer（AIT），核心创新在于将状态和动作视为对等token，按“状态→动作→下一状态”的因果顺序交错排列，而非简单拼接为协变量。这种结构强制注意力机制学习动作对状态转移的定向影响路径（如a_t→s_t），显式建模可控动力学。AIT采用共享嵌入空间和因果Transformer骨干，通过单步预测损失训练，避免传统模型将内生演化与决策诱导变化混为一谈。

Stage II设计Residual Correction Module，专门捕捉外部事件冲击。首先利用LLM从新闻、节假日等文本中提取结构化热点嵌入，再通过交叉注意力机制将外部事件与商品标题、预测状态、历史状态动态对齐，最后经MLP输出残差修正量。该设计的关键在于交叉注意力使外部事件能按商品语义选择性施加影响（如春节不会错误触发圣诞帽需求），优于简单MLP的均匀处理方式。

两阶段采用解耦训练策略，先稳定学习可控转移算子，再灵活适配非平稳外部扰动。推理时AIT生成初始预测，残差模块叠加修正，并自回归滚动生成多步轨迹。该框架在阿里巴巴1688约3200万商品轨迹数据上验证，显著优于Informer、TFT等基线，尤其长周期模拟中MSE降低40%以上。

### Q4: 论文做了哪些实验？

论文在Alibaba 1688构建的大规模电商数据集（约3200万条产品轨迹，覆盖2024-2025年）上开展实验，每个样本包含15周窗口的9维状态变量（曝光、浏览、收藏、加购、买家数、GMV、广告曝光/点击、询盘）和2维动作变量（折扣率、广告支出），并按三级品类进行z-score归一化。测试集采用2025年最后窗口以评估模型对未见外部冲击的泛化能力。

实验设置包含两种预测任务：给定过去5周预测未来10周，以及给定过去10周预测未来5周。对比方法包括Informer、TFT、PatchTST、PETFormer和Timer-XL等经典及大模型基线，所有模型统一隐藏维度256、4头注意力、5层Transformer，使用4块NVIDIA H20 GPU训练。评估指标采用MSE、MAE和NMSE，每个结果报告5次独立运行的均值±标准差。

主要结果：在next 5任务上，CEDAR的MSE为0.182，相比最强基线PatchTST（0.424）和PETFormer（0.434）分别提升57.1%和58.1%；NMSE降至0.083，改善超56%。在next 10任务上，CEDAR同样最优（MSE 0.414），而Informer等传统模型严重退化（MSE超30）。消融实验验证了各组件有效性：去除AIT预测导致MSE升至0.499，去除产品元数据升至0.466，时间混洗事件信号使next 5 MSE恶化至0.274，两阶段训练优于单阶段（0.471 vs 0.414）。此外，在线生产环境中的预算规划实验表明CEDAR能提升商家参与度和平台表现，案例研究（如“糖葫芦奶皮子”病毒式传播）显示残差校正模块能准确捕捉突发需求峰值。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下方向展开：首先，当前两阶段训练虽隔离了可控与随机扰动，但残差修正模块对LLM事件表征的依赖可能引入语义噪声，未来可探索更鲁棒的事件-商品对齐机制，如引入对比学习或图神经网络建模事件间的时空关联。其次，显式时间嵌入被证明无效，但可尝试将节假日等周期性信号以软约束形式融入损失函数，而非直接注入特征。第三，模型在长时程（next 10）滚动预测中误差累积明显，可考虑引入不确定性量化或扩散模型来抑制自回归漂移。此外，当前仅支持离散动作序列，未来可扩展至连续动作空间（如动态预算调整），并探索元学习以快速适应新店铺或新品类。最后，在线实验虽验证了有效性，但可进一步分析模型在不同政策强度下的反事实可靠性边界，并研究如何将用户行为反馈（如点击、转化）作为辅助信号，提升对市场内生演化的建模能力。

### Q6: 总结一下论文的主要内容

本文提出CEDAR框架，用于解决大规模电商平台中决策条件驱动的需求预测问题。传统时间序列预测方法在应对商家主动干预（如预算调整）时存在自回归惯性，且混淆内生市场演化与决策引发的状态转变。CEDAR采用两阶段架构：第一阶段通过动作交错Transformer，以状态-动作-状态的因果顺序建模可控状态转移，实现干预条件下的稳定推演；第二阶段利用残差校正模块，结合外部事件信号和LLM增强的文本表示，对齐噪声事件描述与产品上下文，修正外生冲击导致的预测偏差。基于阿里巴巴1688约3200万商品轨迹的真实数据集，离线实验和在线A/B测试均表明，CEDAR在模拟精度上显著优于强基线模型，并为实际预算规划带来效率提升。该工作为电商决策模拟提供了新范式，兼具理论价值与工业应用意义。
