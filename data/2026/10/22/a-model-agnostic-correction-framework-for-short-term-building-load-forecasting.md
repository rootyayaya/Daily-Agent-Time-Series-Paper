---
title: "A Model-Agnostic Correction Framework for Short-Term Building Load Forecasting"
authors:
  - "Shiqiao Zhou"
  - "Huanbo Lyu"
  - "Holger Schöner"
  - "Zipeng Wu"
  - "Jessica Deuschel"
  - "Freya Wentzel"
  - "IAG Wilson"
  - "Shuo Wang"
date: "2026-10-22"
arxiv_id: "2610.31959"
arxiv_url: "https://arxiv.org/abs/2610.31959"
pdf_url: "https://arxiv.org/pdf/2610.31959v1"
categories:
  - "cs.IR"
  - "cs.LG"
tags:
  - "检索增强时序预测"
  - "模型无关校正框架"
  - "可解释性"
  - "建筑负荷预测"
  - "证据检索"
  - "案例追溯"
relevance_score: 7.5
---

# A Model-Agnostic Correction Framework for Short-Term Building Load Forecasting

## 原始摘要

Short-term building load forecasting remains challenging because load patterns can change rapidly with weather and operating conditions. Data-driven forecasting models may become less reliable when the current operating regime is rare or poorly represented during training, even when similar situations exist elsewhere in the historical record. Recent advances in retrieval-augmented time series forecasting offer a promising way to adapt predictions to changing conditions by directly reusing relevant historical cases at inference time. Motivated by this idea, we propose WeL-RAC, a model-agnostic Weather-Load Retrieval-Augmented Correction framework that explicitly retrieves such evidence at prediction time. WeL-RAC retrieves historical cases that are similar to the current condition based on both recent load states and horizon-aligned weather forecasts. Their observed future load trajectories are then aggregated and used to correct the initial prediction, without retraining or modifying the base forecaster. We evaluate WeL-RAC on 31 building cases across three datasets, eight forecasting backbones, and four horizons from 1 to 18 hours. The framework improves the corresponding base forecasters in 90 of 96 dataset-level comparisons. Beyond accuracy, success and failure case studies further illustrate the framework's interpretability by tracing how retrieved historical evidence improves or degrades forecasts. These findings support explicit historical retrieval as an effective and interpretable complement to the building load forecasting.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决短期建筑负荷预测中数据驱动模型在运行工况变化时可靠性下降的问题。研究背景方面，建筑负荷受天气、 occupancy、HVAC 运行等多因素耦合影响，负荷模式会随天气和运行条件快速变化，短期预测需捕捉这些近端动态，对需求响应、HVAC 调度和模型预测控制至关重要。现有方法（统计、机器学习、深度学习及混合模型）主要在训练阶段将历史信息编码为固定参数，推理时不显式回溯具体历史案例，因此当当前工况在训练分布中罕见或代表性不足时，即使历史记录中存在相似片段，预测也可能失准。持续学习或在线适应虽可更新模型，但需修改参数。相似日与最近邻方法虽利用历史类比，却常依赖单一相似性准则（日历或天气），而建筑负荷相似性本质上是上下文相关的：近期负荷相似的历史片段可能因未来天气不同而演化不同，天气相似片段也可能对应不同运行状态，单一准则检索到的未来轨迹未必与当前预测上下文兼容；且检索到的类比只是近似匹配，单独作为预测不够可靠。因此，本文的核心问题是：如何在不重新训练、不修改基预测器架构与参数的前提下，在推理时显式检索与当前负荷状态和未来天气上下文均兼容的历史案例，用其观测到的未来负荷轨迹对初始预测进行校正，从而提升短期建筑负荷预测在变化工况下的准确性与可解释性。

### Q2: 有哪些相关研究？

相关研究可分为四类。方法类：时间序列预测从指数平滑、ARIMA、状态空间模型发展到SVR、树集成与神经网络，深度学习进一步引入LSTM及Informer、PatchTST等Transformer预测器，近年LLMTime、Time-LLM、TimesFM、Chronos等LLM与基础模型方法探索序列分词与大规模预训练；但多数方法仍是参数化范式，推理依赖有限观测窗口，稀疏但有用的历史工况难以显式调用。检索类：类比预测、最近邻回归、动态时间规整与案例推理是早期源头，模拟集合方法曾用相似历史数值天气预报构建概率预报并扩展至风电预测；RAFT检索训练窗口相似片段及其未来轨迹，TimeRAG、TimeRAF、TS-RAG将检索与LLM或基础模型结合，SARAF平衡相关性与工况多样性并做平稳性感知聚合，SERAF表明数值检索与语义检索互补。应用类：建筑负荷预测涵盖EnergyPlus物理模拟、灰箱RC模型与数据驱动方法，相似日/类比方法依据天气、日历或负荷特征选取历史样本。评测类：上述工作多以精度对比为主。本文区别在于：将双视图检索改造为负荷状态摘要与预报期对齐天气检索，且以免训练、模型无关的后预测校正层形式接入异构预测器，而非独立预测策略或训练数据选择，并在31个建筑案例、8个骨干、4个预测跨度上系统评测，兼顾可解释性。

### Q3: 论文如何解决这个问题？

论文提出 WeL-RAC（Weather-Load Retrieval-Augmented Correction）框架，核心思路是将参数化预测与非参数化证据检索解耦，把检索作为一种轻量级“后预测校正层”附加到任意基预测器上，而不改变其内部结构或训练目标。

整体框架包含三条分支。输入侧为每个预测起点提供三路对齐信息：供基预测器使用的历史负荷-协变量窗口、用于负荷状态匹配的近期负荷窗口，以及用于天气摘要检索的、与预测时域对齐的天气预报。预测分支由任意基模型（线性模型、树模型、神经网络、Transformer 或预训练基础模型）生成初始预测。检索分支则构建两个训练期记忆库：负荷状态库与负荷对齐天气摘要库。

关键技术有三点。其一，双通道查询设计：负荷状态通道用确定性编码器将近期负荷压缩为 9 维统计摘要（当前水平、均值、标准差、极值、净变化、趋势斜率及 5/11 步平均一阶差分），并经标准化与 L2 归一化；天气通道用共享模板算子将天气预报窗口转写为自然语言描述（温度、趋势、湿度、降水、风、湿热风险等），再由冻结文本编码器映射为语义嵌入，从而在“天气情景”层面而非原始变量逐点比较层面进行匹配。其二，两路余弦相似度按权重 λ 融合为统一相似度分数，选出 top-K 历史相似案例，并以温度缩放 softmax 加权聚合其真实未来轨迹，形成经验证据。其三，校正模块将初始预测与聚合证据进行后预测融合，输出最终预测；记忆库仅由训练期构建，避免信息泄漏。

创新点在于：模型无关的可插拔校正机制、负荷状态与对齐天气预报的双重检索、基于文本语义的天气情景匹配，以及可追溯检索证据带来的可解释性。

### Q4: 论文做了哪些实验？

论文在31个建筑案例上评估WeL-RAC，覆盖三个数据集：AlphaBuilding（9个模拟建筑，含Miami、San Francisco、Chicago三种气候及高/标准/低三档能效，每栋17,520条小时记录，使用oracle天气预报）、ASU（12栋校园建筑，2017–2019年，每栋26,280条记录）和UCF（10栋校园建筑，2017–2019年，每栋26,278条记录），后两者使用HRRR 1–18小时预报天气。实验接入八种预测骨干：MLP、LightGBM、LSTM、DLinear、PatchTST、TimeMixer、TimeXer和Chronos-2，预测跨度H=1至18小时，采用相同时间顺序划分与调参流程，对比各骨干的原始预测与检索校正后预测。评价指标为MSE、MAE、R²和MAPE。主要结果：在96组数据集级比较中，有90组取得改进，即框架对绝大多数骨干和案例均带来精度提升；此外通过成功与失败案例研究，追踪检索到的历史证据如何改善或降低预测，展示了框架的可解释性。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有：其一，检索质量高度依赖相似度度量与历史库覆盖度，当历史中缺乏真正可比的工况（如极端天气或新型运行模式）时，检索证据可能误导修正，未来可引入检索置信度估计与“拒绝修正”机制，在证据不足时回退到原预测。其二，当前仅用近期负荷与对齐天气预报构造检索键，未显式建模节假日、 occupancy、设备故障等上下文，可扩展多模态检索键并学习自适应权重。其三，聚合策略较为简单，可探索学习式加权、贝叶斯融合或对检索邻域不确定性建模，输出区间而非点修正。其四，框架为事后修正，未与基模型联合优化，可研究端到端可微检索或在线增量更新历史库以适应概念漂移。最后，可进一步量化可解释性，将检索证据转化为面向运维人员的诊断解释，并在更多建筑类型与更长预测跨度上验证泛化性。

### Q6: 总结一下论文的主要内容

论文针对短期建筑负荷预测中数据驱动模型在罕见或训练分布覆盖不足的运行工况下可靠性下降的问题，提出模型无关的天气—负荷检索增强校正框架WeL-RAC。其核心思路是在推理阶段显式检索历史相似案例，而不修改或重训基础预测器：先由基础预测器生成初始预测，再基于近期负荷状态（数值特征）与预测时段对齐的天气预报（文本摘要语义嵌入）进行双视角相似度匹配，融合后检索Top-K历史案例，聚合其真实未来负荷轨迹，并通过后预测校正模块与初始预测加权融合得到最终结果。实验覆盖三个数据集、31栋建筑、8种预测骨干和1至18小时四个预测步长，在96组数据集级对比中90组优于对应基础模型；案例研究还通过追溯检索证据提升了可解释性。该工作将检索增强校正确立为建筑负荷预测中有效且可解释的补充手段。
