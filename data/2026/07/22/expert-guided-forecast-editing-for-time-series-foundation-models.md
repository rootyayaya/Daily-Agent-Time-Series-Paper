---
title: "Expert-Guided Forecast Editing for Time-Series Foundation Models"
authors:
  - "Hung Le"
  - "Minh Hoang Nguyen"
  - "Manh Nguyen"
  - "Huu Hiep Nguyen"
  - "Dai Do"
date: "2026-07-22"
arxiv_id: "2607.19659"
arxiv_url: "https://arxiv.org/abs/2607.19659"
pdf_url: "https://arxiv.org/pdf/2607.19659v1"
categories:
  - "cs.LG"
tags:
  - "时间序列基础模型"
  - "专家引导"
  - "预测编辑"
  - "趋势-季节分解"
  - "查询预算"
  - "贝叶斯优化"
  - "交叉熵方法"
  - "分子动力学"
relevance_score: 6.5
---

# Expert-Guided Forecast Editing for Time-Series Foundation Models

## 原始摘要

Time-series foundation models can forecast across heterogeneous domains without task-specific training, but their forecasts are fixed once produced and cannot directly incorporate task-specific expert feedback. We study expert-guided forecast editing: a frozen foundation model generates candidate future trajectories, and an expensive expert evaluator scores them to guide forecast revision. Under a tight query budget, two natural strategies sit at opposite ends: best-of-$N$ purely exploits the foundation model's predictive distribution, while optimization approaches mostly explore the forecast horizon as an unstructured high-dimensional vector. Each extreme is individually sub-optimal. We introduce \textbf{DEFT}, an expert-guided forecast editing framework that balances the two by first exploiting the foundation model's predictive samples in a decomposed trend--seasonal space, then exploring around them via component-wise refinement. DEFT queries the expert only on complete trajectories, then reuses scores for the trend and seasonal components that appeared in the queried recombinations. This lets each expert query provide structured component-level feedback while keeping the foundation model frozen. We compare DEFT against direct search approaches, including best-of-$N$, cross-entropy methods, and Bayesian optimization, under matched expert-query budgets. Across two forecasting benchmarks consisting of 78 datasets, three time-series foundation models, four feedback types, and seven query budgets, DEFT consistently improves the effectiveness of expert guidance. A molecular-dynamics case study further suggests that the same principle extends to more physically grounded feedback, supporting the hypothesis that sparse test-time guidance should be spent balancing prior exploitation with structured exploration.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决时间序列基础模型（TFM）在预测中无法直接融入任务特定专家知识的问题。研究背景是，TFM（如Chronos、TimesFM等）虽能跨域预测，但其输出是固定的，无法利用决策者在预测时刻才掌握的上下文、操作或领域知识（如仓库容量上限）。现有方法的不足在于，两种自然策略均存在缺陷：一是“Best-of-N”方法，它纯粹利用TFM的预测分布，在模型先验有偏时效果不佳；二是基于优化的方法（如交叉熵方法、贝叶斯优化），它们将预测视为高维向量进行探索，在小查询预算下容易浪费资源，忽略强先验。本文要解决的核心问题是，如何在有限的专家查询预算下，有效平衡对TFM先验的利用（exploit）与在预测空间中的结构化探索（explore），从而高效地编辑初始预测，使其符合专家反馈。为此，论文提出了DEFT框架，通过分解趋势和季节成分，在利用强锚定轨迹后，进行组件级搜索，并复用专家评分，以实现更高效的预测编辑。

### Q2: 有哪些相关研究？

时间序列基础模型方面，Chronos、TimesFM、Lag-Llama、Moirai、Sundial等模型实现了跨域零样本预测，但预测结果固定且存在性能差距。本文与之互补，保持基础模型冻结，通过少量专家查询编辑其输出。

专家反馈与测试时编辑方面，传统研究关注人类专家利用上下文信息直接调整预测值，而本文中专家仅对完整候选轨迹提供预算评分，DEFT利用这些评分进行结构化输出空间搜索。另一类测试时自适应方法通过延迟观测或在线参数更新修正漂移，但本文场景中未来不可见、模型冻结、反馈仅来自少量专家查询，因此这些方法不适用。本文是首个将专家引导的预测编辑形式化为时间序列模型问题的工作。

查询受限轨迹搜索方面，Best-of-N仅选择最高分候选但不优化；交叉熵方法（CEM）迭代优化采样分布但视轨迹为无结构向量；贝叶斯优化需信任区域应对高维空间。DEFT在分解的趋势-季节成分上搜索，通过查询完整重组轨迹并复用分数实现结构化组件级反馈。

时间序列结构方面，经典分解模型及Autoformer、DLinear等神经网络均利用趋势、季节和残差结构。DEFT不同之处在于，分解并非训练预测器的一部分，而是冻结基础模型预测的测试时编辑表示。

### Q3: 论文如何解决这个问题？

DEFT（Decomposed Expert-guided Forecast）的核心方法是在冻结的时间序列基础模型（TFM）上，通过有限次专家查询来编辑预测结果。其整体框架分为两个阶段，在分解的趋势-季节空间中平衡对TFM先验的利用（Exploit）和结构化探索（Explore）。

**核心架构与关键技术：**
1.  **趋势-季节分解**：将TFM生成的原始预测轨迹分解为平滑趋势分量（通过移动平均）和季节残差分量。这比直接在原始高维空间（H维）搜索更高效，能针对性修正趋势偏移、季节幅度等结构化误差。
2.  **第一阶段：利用先验**：从TFM的B0个预测样本中提取趋势和季节分量池。通过平衡重组（对角线+随机配对）形成B0条完整轨迹，每条轨迹查询专家获取分数。关键创新是**分数复用**：每条轨迹的分数通过最大池化（Max-pooling）分别反馈给其趋势和季节分量，从而用一次查询获得两个分量的效用评估。随后，根据分量效用选出精英分量（Top-ρK），并初始化两个独立的高斯分布（均值来自精英，方差来自全部分量池，以校准搜索范围）。
3.  **第二阶段：探索优化**：进行nr轮交叉熵方法（CEM）优化。每轮从当前高斯分布中采样新的趋势和季节候选，再次平衡重组并查询专家。通过分数复用和精英重拟合（更新高斯分布的均值和标准差），逐步将搜索导向高分区域。整个过程中，始终记录并返回所有查询中得分最高的轨迹。

**创新点**：DEFT通过分解空间和分数复用，让每次专家查询都能提供结构化的分量级反馈，从而在极少的查询预算下（如B=10），比纯利用（Best-of-N）或纯探索（直接CEM）方法更有效地利用专家知识，显著提升编辑效果。

### Q4: 论文做了哪些实验？

论文在实验设置上，使用三个时间序列基础模型（TimesFM、Chronos-2、Moirai-2）作为主干，在ChronosBench（42个数据集）和GIFT-Eval（36个数据集）两个基准测试上共78个数据集进行评估。对比方法包括零样本、随机搜索、Best-of-N（分位数和样本）、直接CEM、TuRBO-1和代理CEM。专家反馈模式有Rating-3、Rating-5、Pairwise和Pairwise-best四种，查询预算B从2到128不等。主要指标为相对MASE、WQL、MAE、MSE及胜率W-ZS和W-Rand。在TimesFM主干上，DEFT在ChronosBench上MASE为0.838（最佳基线0.887），GIFT-Eval上为0.834（最佳基线0.884），W-ZS达94-96%，W-Rand超91%。在Chronos主干上，DEFT胜率最高（W-ZS 85.0%），但ChronosBench的MASE（0.889）略低于Best-of-N（分位数）（0.877）。在Moirai主干上，DEFT全面领先，MASE降至0.849和0.906，MSE降至0.741和0.815。此外，在分子动力学案例中，DEFT在B=128时降低键违例率34%，优于Best-of-N的21%。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：实验中的“专家”信号来自真实未来值，未模拟真实人类专家的噪声、误校准或领域知识；趋势-季节分解假设预测误差主要由水平、趋势和季节成分构成，可能不适用于非周期或高频波动数据。未来可探索的方向包括：1）引入真实人类专家或硬约束检查器验证DEFT的鲁棒性；2）扩展分解框架，支持更复杂的成分（如残差、事件驱动模式）；3）研究自适应查询策略，根据专家反馈动态调整探索-利用平衡；4）将DEFT扩展到多步交互场景，允许专家逐步修正而非一次性评分；5）探索跨模型迁移性，验证该框架是否适用于不同架构的基础模型。此外，可结合主动学习思想，让模型主动询问专家最具信息量的轨迹成分，以进一步提升查询效率。

### Q6: 总结一下论文的主要内容

这篇论文研究了专家引导的时间序列预测编辑问题，即冻结的基础模型生成候选预测，而昂贵的专家评估器在有限查询预算下指导修正。核心贡献是提出DEFT框架，通过先利用基础模型预测分布在趋势-季节分解空间中获取强样本，再围绕它们进行分量级精细探索，平衡了“利用”与“探索”。DEFT仅在完整轨迹上查询专家，但复用查询结果中的分量级反馈。在78个数据集、三个基础模型、四种反馈类型和七种查询预算下，DEFT一致优于最佳N选、交叉熵方法和贝叶斯优化等基线。分子动力学案例表明该原则可推广至物理反馈。主要结论是：在紧查询预算下，稀疏测试时指导应优先平衡先验利用与结构化探索，而非任意高维空间扰动。
