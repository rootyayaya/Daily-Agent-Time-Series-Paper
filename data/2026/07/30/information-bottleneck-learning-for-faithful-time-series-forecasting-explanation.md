---
title: "Information Bottleneck Learning for Faithful Time Series Forecasting Explanations"
authors:
  - "Xu Zheng"
  - "Wei Cheng"
  - "Zhuomin Chen"
  - "Mo Sha"
  - "Jingchao Ni"
  - "Dongsheng Luo"
date: "2026-07-30"
arxiv_id: "2607.28124"
arxiv_url: "https://arxiv.org/abs/2607.28124"
pdf_url: "https://arxiv.org/pdf/2607.28124v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "可解释时间序列预测"
  - "信息瓶颈"
  - "忠实性解释"
  - "多变量时间序列"
  - "内在可解释模型"
relevance_score: 7.5
---

# Information Bottleneck Learning for Faithful Time Series Forecasting Explanations

## 原始摘要

As forecasts increasingly drive decisions in fields such as energy, transportation, and healthcare, understanding the historical data behind these predictions has become as crucial as the predictions themselves. Although existing interpretable-by-design forecasters reveal their internal structures, they offer no guarantee that these structures faithfully reflect the underlying evidence driving the predictions. In contrast, while faithfulness-oriented methods explicitly verify model behavior, they are almost exclusively designed for post-hoc classification tasks. To bridge this gap, we propose IB-Forecast, an inherently interpretable multivariate time-series forecasting framework. It decomposes forecasting into a learned periodic component and a residual component computed with explainable masks over input tokens. With a budget-constrained information bottleneck, end-to-end optimization enables users to directly control explanation sparsity. With a rigorous faithfulness evaluation protocol, extensive experiments demonstrate that IB-Forecast matches the forecasting error of leading black-box models while providing faithful explanations at no additional inference cost. Furthermore, under a matched sparsity budget, these native explanations consistently surpass gradient-based, occlusion-based, and optimization-based baselines across all evaluated datasets. Ultimately, whereas the native explanations of existing interpretable forecasters exhibit poor faithfulness, IB-Forecast guarantees high explanation fidelity, requiring only 14-20% of the observations to deliver low-error predictions.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

本文聚焦于多元时间序列预测中的可解释性问题。研究背景在于，随着预测模型在能源、交通、医疗等关键决策场景中的广泛应用，理解预测所依据的历史证据变得与预测精度同等重要。现有方法存在明显不足：一类是内在可解释的预测架构（如N-BEATS、TFT等），虽能展示内部结构，但无法保证这些结构真实反映驱动预测的底层证据，其解释忠实性缺乏系统评估；另一类是面向忠实性的事后归因方法，主要针对分类任务设计，直接迁移到多步预测面临困难——预测需建模持续水平、尺度、周期结构及跨变量和未来时段的输入依赖偏差，且事后解释与预测计算脱节，常需评估分布外扰动输入。

本文要解决的核心问题是：如何构建一个内在可解释的多元预测框架，使解释在单次前向传播中自然生成并成为预测计算的一部分，同时通过信息瓶颈机制保证解释的忠实性——即只有被选中的历史输入子集能影响预测偏差读出的，且允许用户直接控制解释稀疏度。该框架需在保持与黑盒模型相当预测精度的前提下，提供高保真解释，并证明准确预测往往只需少量关键历史观测。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，可解释性设计模型如N-BEATS、NHiTS通过可解释基分解预测，DLinear提供线性映射，TFT暴露变量选择权重，PatchDecomp展示逐块贡献，ProSeNet和ProtoTS利用原型相似性，概念瓶颈Transformer使用命名概念。但这些方法均未验证暴露结构是否忠实反映预测依据。**后验解释类**包括梯度法、扰动法（Dynamask、ExtremalMask、ContraLSP）以及信息瓶颈解释器（TimeX、TimeX++），它们主要面向分类任务，且后验解释可能与模型实际计算不一致。**信息瓶颈与随机门控类**中，GSAT将信息瓶颈引入图学习，其随机注意力机制是本文门控目标的蓝本。

本文与上述工作的核心区别在于：一是提出**内在可解释**的多元时间序列预测框架IB-Forecast，而非后验解释；二是将预测分解为周期成分和带可解释掩码的残差成分，通过预算约束信息瓶颈实现端到端优化，直接控制解释稀疏度；三是严格评估解释忠实性，证明其匹配黑盒模型误差的同时提供高保真解释，而现有可解释预测器原生解释的忠实性普遍较差。

### Q3: 论文如何解决这个问题？

IB-Forecast通过一个四阶段的可解释框架解决时间序列预测中的解释忠实性问题。核心思想是将预测分解为结构上下文和窗口特定偏差两部分，并仅用被选中的偏差token生成预测，从而保证解释与预测因果一致。

框架首先对每个通道进行实例级归一化（去除均值和标准差），再减去一个可学习的季节轮廓查找表Q，得到仅含窗口特定信息的偏差矩阵D。然后将D分割为patch×channel的token，通过共享线性嵌入和位置编码映射为向量表示。门控网络使用Transformer编码器对token进行上下文建模，经线性头输出每个token的开启概率。训练时采用带Gumbel噪声的hard-Concrete估计器实现二值化掩码的梯度传播，推理时则直接以0.5为阈值确定性选择。被选中的token经通道级前馈网络读出未来偏差，最后叠加季节轮廓并反归一化恢复原始尺度。

训练目标包含四项：预测误差、稀疏性KL正则、用户指定预算的均方约束（控制解释稀疏度）、以及时间连续性TV正则。创新点在于：掩码直接作用于偏差空间而非原始值，使关闭token对应“遵循季节模式”的合理分布内假设；门控评分与预测在同一前向传播中完成，零额外推理成本；通过预算约束实现用户可控的稀疏性。实验表明仅需14-20%的观测即可达到与黑盒模型相当的预测精度，且解释忠实性显著优于梯度、遮挡和优化基线。

### Q4: 论文做了哪些实验？

实验在6个标准多元时间序列基准（ETTh1、ETTh2、ETTm1、ETTm2、Weather、Electricity）上进行，回看窗口96，预测长度{96,192,336,720}。对比方法分两组：自解释模型（TFT、PatchDecomp、DLinear、ProtoTS）和黑盒SOTA（TQNet、CycleNet、iTransformer、PatchTST、TimesNet）；解释性对比包括梯度、IG、TIMING、遮挡、随机及DynaMask、ExtremalMask等后验方法。采用MSE/MAE衡量精度，用匹配预算保真度（comprehensiveness@k减sufficiency@k）评估解释质量。

主要结果：IB-Forecast在MSE上全面优于所有自解释模型，整体比PatchDecomp低约4%、比DLinear低18%；与黑盒TQNet统计持平（Δ=0.2%），在ETTh1上最优。保真度方面，在13.9%-20.4%稀疏度下，IB-Forecast在三个数据集上得分最高（0.848-0.950），远超最强后验基线Occlusion（0.637-0.820）和优化方法DynaMask（≤0.39）。消融实验显示，移除门控基座或硬门控会严重破坏解释（得分降至0.62或-1.0），移除周期分量Q导致MSE上升10%。稀疏性分析表明，仅读取13-20%输入即可保持与全输入接近的精度（MSE差距≤3.5%）。

### Q5: 有什么可以进一步探索的点？

IB-Forecast通过信息瓶颈机制实现了高保真解释，但仍存在若干可探索空间。首先，其掩码选择基于token级输入，未充分建模多变量间的动态因果关系，未来可引入图神经网络或因果发现模块，显式学习变量间交互，提升解释的因果语义。其次，当前方法侧重周期性分解与残差掩码，对非平稳、长程依赖的时间序列（如突发性事件）解释鲁棒性不足，可探索将频域信息或状态空间模型融入瓶颈设计。第三，信息瓶颈的预算约束是全局静态的，实际场景中不同时间窗口的解释复杂度应自适应变化，可设计动态预算分配机制。此外，论文仅验证了预测误差与保真度，未评估解释对下游决策（如异常根因定位）的实际效用，建议引入人类-in-the-loop实验或因果干预测试。最后，将IB-Forecast扩展至多模态数据（如文本日志+数值序列）或在线学习场景，也是值得尝试的方向。

### Q6: 总结一下论文的主要内容

本文提出IB-Forecast，一个内在可解释的多变量时间序列预测框架，旨在解决现有可解释预测器无法保证解释忠实性的问题。方法上，将预测分解为可学习的周期成分和基于可解释掩码的残差成分，通过预算约束的信息瓶颈实现端到端优化，允许用户直接控制解释稀疏度。实验表明，IB-Forecast在匹配黑盒模型预测误差的同时，无需额外推理成本即可提供忠实解释；在相同稀疏度预算下，其原生解释在多个数据集上一致优于基于梯度、遮挡和优化的基线。关键结论是，仅需14-20%的观测数据即可实现低误差预测，而现有可解释预测器的原生解释忠实性较差。该工作为可解释预测提供了严格的忠实性评估协议和匹配预算评估方法，弥合了内在可解释性与后验解释方法之间的鸿沟，对能源、交通和医疗等依赖预测决策的领域具有重要意义。
