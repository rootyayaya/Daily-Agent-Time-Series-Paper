---
title: "Efficient Test-Time Scaling for LLM-based Time Series Forecasting"
authors:
  - "Xuan-May Le"
  - "Minh-Tuan Tran"
  - "Ling Luo"
  - "Uwe Aickelin"
  - "Dinh Phung"
  - "Trung Le"
date: "2026-08-09"
arxiv_id: "2608.08675"
arxiv_url: "https://arxiv.org/abs/2608.08675"
pdf_url: "https://arxiv.org/pdf/2608.08675v1"
github_url: "https://github.com/xuanmay2701/SCALER"
categories:
  - "cs.LG"
tags:
  - "LLM-based time series forecasting"
  - "test-time scaling"
  - "coarse-to-fine refinement"
  - "iterative residual token refinement"
  - "long-term forecasting"
  - "zero-shot forecasting"
  - "efficient inference"
  - "shape modeling"
relevance_score: 7.5
---

# Efficient Test-Time Scaling for LLM-based Time Series Forecasting

## 原始摘要

Long-term time series forecasting benefits from preserving global structure such as trends and seasonality. Recent LLM-based forecasters often improve accuracy through test-time scaling (e.g., iterative refinement), but these methods are computationally expensive and increasingly prone to global-shape mismatch as the prediction horizon extends. We propose SCALER, a coarse-to-fine forecasting framework that first employs a lightweight Transformer tailored to long-term shape modeling to predict a coarse representation of future dynamics. This predicted shape then serves as a compact guide for an LLM to perform test-time scaling via iterative coarse-to-fine residual token refinement, while processing substantially fewer tokens at each step. By guiding refinement with an explicit future-shape prediction, SCALER reduces reliance on long description prompts, and its fixed-step refinement avoids costly reward-model-based selection, further lowering computational overhead. Experimental results demonstrate that SCALER outperforms strong forecasting baselines in long-term, short-term and zero-shot forecasting while significantly reducing the inference cost associated with scaled LLM for time series forecasting. Code: https://github.com/xuanmay2701/SCALER.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

长期时间序列预测在金融、医疗、能源等领域至关重要，需同时捕捉趋势、季节性等全局结构与局部细节。现有方法存在明显不足：传统深度学习模型虽能建模全局模式，但难以兼顾多尺度动态；LLM预测器将预测视为直接序列映射，缺乏中间推理，长序列下易产生形状漂移；而现有测试时扩展方法（如迭代细化）虽提升精度，但计算成本随预测长度急剧增长，且反复局部修正会累积为全局形状失真，过度依赖长提示或基于奖励模型的候选选择进一步加剧开销。

本文提出SCALER框架，核心解决“如何在长时预测中实现高效且形状一致的测试时扩展”这一问题。其创新在于两阶段粗到细设计：第一阶段用轻量Transformer预测未来粗粒度形状（低频结构），第二阶段由预训练LLM基于该形状锚点进行固定步数的残差细化，仅处理紧凑token块。该设计将全局结构预测与局部细化解耦，既避免LLM处理冗长输入，又通过显式形状约束抑制长程漂移，同时固定步数调度免去奖励模型选择，实现7倍推理加速与精度提升。

### Q2: 有哪些相关研究？

时间序列预测领域的研究可大致分为四类。**传统与深度学习方法**：包括ARMA/ARIMA等统计模型，以及Informer、Autoformer、PatchTST、iTransformer等Transformer变体，还有DLinear、TimeMixer等轻量线性基线。这些方法擅长保持趋势和季节性等全局结构，但难以捕捉局部细节和不确定性。**生成式方法**：如TimeGrad、D3VAE、TSDdiff等扩散模型，以及ARMD的自回归滑动窗口策略，能更好地恢复局部变化，但长程迭代易累积误差导致全局漂移。**LLM基础模型预测**：TimeLLM、PromptCast、LLMTime、AutoTimes等方法利用预训练LLM的语义理解能力，通过提示词或参数微调（如FPT、CALF）实现预测，但多数依赖长提示或复杂适配，计算开销大。**测试时扩展与迭代精化**：通过采样多个未来路径、奖励模型选择或迭代修正提升精度，但成本随预测长度快速增长，且局部编辑可能扭曲全局形状。

SCALER与上述工作的核心区别在于：它采用粗到细的两阶段设计，先用轻量Transformer预测全局形状，再引导LLM进行固定步数的残差token精化，既避免了长提示依赖，又无需奖励模型选择，显著降低了推理成本，同时通过显式形状锚定防止长程漂移。

### Q3: 论文如何解决这个问题？

SCALER提出了一种“由粗到细”的两阶段测试时扩展框架，以解决现有LLM预测器在长时程预测中计算开销大且易出现全局形状失配的问题。

整体框架分为两个核心阶段。**阶段一：粗粒度形状预测**。设计了一个轻量级Transformer模型F，仅从历史序列X预测未来序列的低频粗粒度表示Ŝ¹，该表示通过下采样算子（归一化后插值）得到，捕捉趋势、季节性和状态切换等全局结构。训练时使用MSE损失L_shape监督该形状预测，使其与真实下采样目标S¹对齐。

**阶段二：固定步长多尺度细化**。这是测试时扩展的核心机制。首先，通过共享的多尺度编码器E将历史序列X分块（Patching）并编码为连续token序列Z_I，该编码器利用原型交叉注意力（Prototype-based Cross-Attention）将时间序列块对齐到LLM的嵌入空间。然后，以预测的粗粒度形状token Z_S=[Ŝ¹]初始化上下文，预训练LLM G作为细化器，执行固定K步的由粗到细循环：在第k步，G基于历史token Z_I和当前上下文Z_S预测更细尺度的token块Ŝ^k，并将其追加到Z_S中供下一步使用。尺度集合{Scale_k}从粗（如12、24时间戳）到细（如48、96时间戳）有序排列，形成了测试时计算分配的策略。

关键技术包括：**多尺度残差细化**——每一步只预测当前尺度的残差token，避免重复处理全部序列；**无候选选择**——固定步长循环替代了基于奖励模型的候选生成与筛选，显著降低推理开销；**双重监督**——训练时同时施加尺度级MSE损失L_refine和原始时间序列空间的MSE损失L_ts，确保token级细化与最终重构的一致性。

创新点在于：显式的未来形状预测引导细化过程，减少了对冗长描述提示的依赖；固定步长的多尺度细化策略使推理成本可预测且可控；轻量级形状预测器与LLM细化器分工明确，兼顾全局结构保真与局部细节恢复。

### Q4: 论文做了哪些实验？

论文围绕SCALER框架进行了三组核心实验：长期预测、短期预测和零样本预测。长期预测采用ETTh1/ETTh2/ETTm1/ETTm2、ECL、Traffic、Weather和ILI八个标准多变量数据集，预测长度H∈{96,192,336,720}（ILI为24/36/48/60），以MSE和MAE为指标。短期预测在M3/M4基准上按Year、Quarter、Month、Others四类场景评估sMAPE、MASE和OWA。零样本预测则测试M3→M4和M4→M3两种迁移设置，报告sMAPE。

对比方法包括TimeReasoner、LVICL、AutoTimes、TimeLLM、FPT、DLinear、PatchTST、TimesNet及FEDformer等强基线。主要结果显示：短期预测中SCALER在全部12个场景-指标组合中均获第一，平均sMAPE为11.41，显著优于第二名TimeReasoner的11.558；零样本预测中SCALER在M3→M4平均sMAPE达12.36，M4→M3为13.488，均优于所有基线。长期预测虽未在表格中详列，但摘要指出SCALER在长短期及零样本任务上均超越强基线，同时大幅降低推理成本——其固定步长细化机制避免了奖励模型选择开销，且每步仅处理少量token，验证了粗到细引导策略的有效性。

### Q5: 有什么可以进一步探索的点？

SCALER通过粗到细的框架有效降低了LLM在时间序列预测中的推理成本，但仍存在若干可探索的方向。首先，其粗粒度形状预测依赖轻量Transformer，在极端非平稳或突变场景下可能失真，可引入自适应形状校正机制或不确定性量化来增强鲁棒性。其次，固定步长的残差细化虽高效，但缺乏对复杂动态的适应性，未来可探索基于信息熵或预测置信度的动态步长策略，在关键区间分配更多计算资源。第三，当前方法主要针对单变量或多变量独立建模，对跨变量依赖和层次时间序列的利用不足，可结合图神经网络或层次注意力捕获变量间交互。此外，零样本迁移中形状先验的领域适应性有限，可引入元学习或提示微调来提升跨域泛化。最后，将LLM的推理过程与可解释性结合，通过形状引导生成自然语言解释，有助于增强模型在工业诊断中的可信度。

### Q6: 总结一下论文的主要内容

SCALER提出了一种面向长时序预测的高效测试时扩展框架，旨在解决现有LLM预测器在迭代细化中计算开销大且易产生全局形状漂移的问题。该方法采用两阶段由粗到细的策略：首先，轻量级Transformer预测未来动态的粗粒度表示，捕捉趋势、季节性和状态变化等低频结构；随后，预训练LLM以该形状为锚点，通过固定步数的残差细化逐步生成细粒度token块，避免长提示依赖和奖励模型选择。实验表明，SCALER在长短期及零样本预测中均优于强基线，同时推理速度比标准测试时扩展方法快约7倍，显著降低计算成本并保持全局形状一致性，为LLM时序预测提供了高效且稳定的部署方案。
