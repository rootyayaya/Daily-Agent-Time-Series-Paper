---
title: "Align-RAG: Alignment Is All You Need for TSFM In-Context Learning"
authors:
  - "Mohammad Asadi"
  - "Soheil Hor"
  - "Bardiya Akhbari"
  - "Jack W. O'Sullivan"
  - "Tahoura Nedaee"
  - "Layne C. Price"
  - "Raviteja Anantha"
  - "Euan Ashley"
  - "Ehsan Adeli"
date: "2026-08-06"
arxiv_id: "2608.05571"
arxiv_url: "https://arxiv.org/abs/2608.05571"
pdf_url: "https://arxiv.org/pdf/2608.05571v1"
github_url: "https://github.com/masadi-99/align-rag"
categories:
  - "cs.LG"
  - "cs.IR"
tags:
  - "Retrieval-Augmented Forecasting"
  - "Time Series Foundation Models"
  - "In-Context Learning"
  - "Training-Free Alignment"
  - "Chronos-Bolt"
  - "Zero-Shot Forecasting"
  - "Closed-Form Alignment"
  - "RAG for Time Series"
relevance_score: 7.5
---

# Align-RAG: Alignment Is All You Need for TSFM In-Context Learning

## 原始摘要

Retrieval-augmented forecasting promises to adapt frozen Time Series Foundation Models (TSFMs) to new domains without fine-tuning, but recent methods typically rely on learned fusion modules, i.e., trained adapters that merge retrieved examples into the backbone's forecast, based on the assumption that frozen backbones cannot dynamically incorporate retrieved context on their own. We show this assumption is unnecessary. We introduce Align-RAG, a training-free method that applies a closed-form per-pair amplitude rescaling and integer-lag phase shift to retrieved past-future windows before they enter a frozen backbone's context. With no learned parameters, Align-RAG outperforms the state-of-the-art trained retrieval adapter on a frozen Chronos-Bolt on all seven datasets of the standard benchmark (avg -3.75% MSE), showing that the gains previously attributed to learned fusion are recoverable without any training. Align-RAG further improves zero-shot MSE on four additional frozen TSFMs with various architectures by 2.5% to 13.7% per backbone with no per-backbone tuning. To probe why alignment helps, we compare the frozen backbone's prediction shift under aligned demonstrations to the closed-form ridge prediction shift on the same pairs. We find that aligned demonstrations induce prediction shifts that track a closed-form ridge predictor on the same pairs, with a future-shuffle control ruling out a futures-averaging account. Together, these results indicate that frozen TSFMs already support dynamic in-context use of retrievals, and that closed-form alignment should be the default baseline for retrieval-augmented forecasting before any fusion module is trained. Code available at: https://github.com/masadi-99/align-rag

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

该论文针对检索增强的时间序列预测中一个普遍但未被验证的假设提出挑战：现有方法（如TS-RAG）认为冻结的时间序列基础模型（TSFM）无法自主利用检索到的上下文，因此必须训练额外的融合模块（如适配器）来整合检索结果。这种设计带来了高昂的训练成本和复杂性。

本文的核心问题是：**冻结的TSFM是否真的需要学习型融合模块才能从检索中获益？** 作者通过提出Align-RAG证明这一假设是不必要的。Align-RAG是一种完全无需训练的方法，仅通过对检索到的“过去-未来”窗口施加闭式振幅缩放和整数滞后相位对齐，使检索到的过去片段与查询匹配，然后直接作为上下文输入冻结的骨干网络。

实验表明，Align-RAG在七个标准数据集上全面超越训练过的TS-RAG适配器（平均MSE降低3.75%），并在四种不同架构的冻结TSFM上均提升零样本性能（2.5%-13.7%）。消融实验显示，对齐操作贡献了绝大部分性能增益，而检索排序的影响不足1个百分点。机制分析进一步揭示，对齐后的演示使冻结骨干的预测偏移与闭式岭回归预测偏移高度相关，且未来打乱控制实验排除了“仅平均未来值”的解释，证明模型确实在利用“过去-未来”对应关系进行动态上下文学习。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，TS-RAG训练自适应检索混合器、TimeRAF训练端到端检索器与通道提示模块、RAFT训练投影与预测头、RATD训练扩散去噪器、TimeRAG插入可学习重编程层，这些方法均在冻结TSFM与检索结果间加入可学习融合模块；而Align-RAG完全无需训练，通过闭式幅值缩放与整数滞后相位平移实现对齐，直接超越最强训练基线TS-RAG。**理论类**工作将上下文学习视为隐式回归，如证明Transformer匹配最小二乘估计或闭式岭回归，Align-RAG借鉴此视角，通过对比冻结骨干在对齐演示下的预测偏移与岭回归预测偏移，揭示其动态利用检索的内在机制。**相似性度量类**包括动态时间规整、k-Shape相位不变聚类、矩阵轮廓等，传统方法将幅值与相位视为噪声先去除，而Align-RAG反其道行之，利用闭式对齐显式校正这些因素以增强检索演示的上下文效用。与这些工作的核心区别在于，Align-RAG证明冻结TSFM本身已具备动态上下文学习能力，无需任何训练适配器，为检索增强预测提供了更简洁且更优的默认基线。

### Q3: 论文如何解决这个问题？

Align-RAG 的核心思路是证明冻结的时间序列基础模型（TSFM）本身就能动态利用检索到的上下文，无需训练任何融合模块。其方法完全无需训练，通过两个闭式变换对每个检索到的“过去-未来”窗口进行预处理，再送入冻结的骨干网络。

整体框架包含五个组件：**对齐**、**多样化**、**分层层级布局**、**未来混合**和**无演示二次前向**。对齐是核心创新，包含两步：第一步是Wiener风格的仿射缩放，对每个检索对的过去部分拟合一个带正则化的斜率$a_i$和截距$b_i$（$a_i = \sigma_q\sigma_{p_i}/(\sigma_{p_i}^2+(\sigma_q/M)^2)$，$M=5$），使检索过去的均值和方差与查询对齐，并将同一映射应用于对应的未来部分以保持一致性；第二步是整数滞后相位对齐，通过最大化与查询过去的样本互相关（限制$|\tau|\le S/4$）找到最优滞后$\tau_i^*$，并将该滞后同样应用于未来。多样化使用最大边际相关性（$\lambda=0.3$）从20个检索候选中选出10个多样化的邻居。分层层级布局将2个详细演示（过去256步）和8个密集演示（过去32步）打包进2048 token预算，且不截断未来。未来混合以$\beta=0.15$将骨干预测与按检索距离加权的对齐未来进行凸组合；无演示二次前向则对仅查询的预测做同样混合，最终以$\alpha=0.60$加权平均两个结果。

该方法的创新点在于：首次证明冻结TSFM无需训练即可实现检索增强的动态上下文学习，且闭式对齐优于训练过的融合适配器，在七个基准数据集上平均MSE降低3.75%，并在四个额外冻结骨干上提升2.5%-13.7%的零样本性能。

### Q4: 论文做了哪些实验？

论文在7个标准数据集（ETTh1、ETTh2、ETTm1、ETTm2、Weather、Exchange、Electricity）上评估，设置上下文长度S=512、预测步长H=64（附录含H=96/192），以MSE和MAE为指标。主对比使用冻结的Chronos-Bolt-Base，并扩展至Chronos-2、TimesFM-2.0、Moirai和Toto五个骨干模型。

与TS-RAG的正面比较中，Align-RAG在全部7个数据集上MSE更低（平均-3.75%），6/7数据集MAE更优，其中5个小数据集的MSE提升超过2%，且配对bootstrap 95%置信区间严格为正。2×2消融（检索器×对齐）显示：固定对齐时，随机检索仅比排序检索平均多0.84个百分点；固定检索器时，去除对齐导致MSE相对零样本回归20-22个百分点。跨骨干实验显示所有模型平均MSE下降，Moirai获益最大（-13.73%，7/7胜出），TimesFM在4个ETT数据集上最高降12.43%，Toto最不稳定（平均-2.45%）。累积消融表明幅度和相位对齐贡献最大，第二遍共识进一步改善并解决Electricity校准问题。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下方向展开：首先，当前机制证据仅为相关性（ρ_GD=0.45），未来可设计更严格的因果干预实验，如对演示序列进行可控扰动，验证预测偏移是否真正遵循闭式岭回归的等价关系，而非仅方向性一致。其次，现有评估局限于标准单变量TS-RAG基准，应扩展至多变量、含协变量及分布漂移场景，探索对齐操作在高维时空关联中的有效性，例如将幅度缩放与相位平移推广为跨通道对齐矩阵。第三，retriever×alignment消融仅在Chronos-Bolt上验证，需在更多异构骨干（如线性注意力或状态空间模型）上复现，以确认“对齐主导增益”的普适性。此外，可尝试将闭式对齐与轻量级微调结合——先以无训练对齐初始化，再对少量参数进行低秩适应，可能兼顾动态上下文利用与任务特异性。最后，探索对齐的自动化选择，如根据查询与检索窗口的频谱相似度自适应决定是否施加相位平移，避免固定整数滞后带来的次优匹配。

### Q6: 总结一下论文的主要内容

Align-RAG提出一种无需训练的检索增强时间序列预测方法，挑战了“冻结TSFM必须依赖学习融合模块才能利用检索上下文”的既有假设。该方法对检索到的过去-未来窗口施加闭式逐对幅度缩放与整数滞后相位对齐，再送入冻结骨干网络。在标准七数据集基准上，冻结Chronos-Bolt配合Align-RAG全面超越训练过的TS-RAG混合器（平均MSE降低3.75%），并在四种不同架构的冻结TSFM上实现2.5%-13.7%的零样本提升，无需逐骨干调参。行为探针实验显示，对齐后的演示引发的预测偏移与闭式岭回归预测偏移高度相关，而未来洗牌对照排除了单纯未来平均的解释。结论表明，冻结TSFM本身已具备动态上下文学习能力，闭式对齐应作为检索增强预测的默认基线，学习融合主要补偿了缺乏对齐的不足。
