---
title: "FreSia: Frequency-Semantic Instantiation and Alignment for Multivariate Time Series Analysis"
authors:
  - "Yubo Wang"
  - "Hui He"
  - "Hezhe Qiao"
  - "Guoqing Ji"
  - "Zhendong Niu"
date: "2026-10-05"
arxiv_id: "2610.05726"
arxiv_url: "https://arxiv.org/abs/2610.05726"
pdf_url: "https://arxiv.org/pdf/2610.05726v1"
categories:
  - "cs.AI"
tags:
  - "LLM for Time Series"
  - "Multivariate Time Series"
  - "Frequency-Domain Prompting"
  - "Semantic Alignment"
  - "Time Series Forecasting"
  - "Anomaly Detection"
  - "Time-Frequency Fusion"
  - "Prompt Engineering"
  - "Multimodal Time Series"
  - "LLM Semantic Space"
relevance_score: 7.5
---

# FreSia: Frequency-Semantic Instantiation and Alignment for Multivariate Time Series Analysis

## 原始摘要

Large Language Models (LLMs) have shown strong potential in multivariate time series forecasting and anomaly detection. Existing studies predominantly inject temporal information into LLMs via direct numerical tokenization or heuristic textual descriptions. However, LLMs still face difficulty in perceiving the underlying structural patterns of numerical time series, particularly the seasonal and trend components obscured by discrete numerical tokens. To bridge this gap, we propose FreSia, a frequency-aware framework that establishes an effective alignment between the semantic space of LLMs and the frequency space of time series. Specifically, FGPrompt, a Frequency-Guided Prompt mechanism within FreSia, distills the frequency-domain structures of time series and projects them into prompts tailored to the semantic space of LLMs. Furthermore, we introduce a Global-driven Context Learning (GCL) component, which uses a global CLS-driven probe to generate global context to bridge the time-frequency domain gap and fuse the multi-modal information. Experiments on eight forecasting benchmarks show that FreSia achieves average improvements of 13.48% and 8.06% in MSE and MAE, respectively.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决现有基于大语言模型（LLM）的多变量时间序列分析方法在表示对齐上的核心缺陷。研究背景方面，LLM 已在时间序列预测与异常检测中展现出潜力，现有方法主要依赖直接数值序列化或启发式文本描述，将时序信息注入 LLM。然而，这类方法存在明显的表示不匹配：原始数值是稠密、连续、尺度敏感且对分词不友好的，而 LLM 预训练于离散语言 token，擅长语义与逻辑关系建模，却难以从离散数值 token 中感知时间序列的潜在结构模式，尤其是被掩盖的季节性与趋势成分。频域分析虽能提供周期与谐波等结构化中间表示，但如何将其有效转化为 LLM 可理解的语义空间仍未被充分解决。本文的核心问题是：如何建立 LLM 语义空间与时间序列频域空间之间的有效对齐，使 LLM 能够感知数值序列背后的频率结构。为此，作者提出 FreSia 框架，通过频率引导提示（FGPrompt）将 Top-K 主导频率蒸馏为结构化频谱原语并投影到 LLM 语义空间，同时引入全局驱动上下文学习（GCL）组件，利用 CLS 探针生成全局上下文，弥合时域与频域之间的表示鸿沟，从而提升预测与异常检测性能。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，TimesNet、PatchTST、iTransformer等通过时序二维变化、patch表示和多变量注意力建模时序依赖；频域方向有FEDformer、FredFormer、FilterNet、ReFocus、TimeKAN、FDNet、MTCMD等，它们结合季节-趋势分解、频率滤波或频带建模，但大多仍停留在数值表示空间。应用类方面，异常检测有AnomalyTransformer、GCAD、TimeRadar、Graph-MoE等，视觉异常检测有AdaCLIP等。评测类方面，有面向复杂视角光照条件的视觉异常检测基准。与LLM结合的工作包括S²IP-LLM、LLM4TS、ChatTime、Time-LLM、TimeCMA、LLM-TPF、UniTime、GPT4MTS、STG-LLM、ITFormer、Context-Alignment、TimeCAP、LLMAD、TSINR等，它们通过提示学习、参数高效对齐或文本描述注入时序信息。本文区别在于：FreSia将主导频谱结构转化为语义周期描述符，并通过FGPrompt和GCL实现LLM语义空间与频域空间的对齐，用于预测与基于重构的异常检测。

### Q3: 论文如何解决这个问题？

FreSia 的核心思路是在 LLM 的语义空间与时间序列的频率空间之间建立有效对齐，从而让模型能够感知被离散数值 token 掩盖的季节性与趋势结构。整体框架由三个组件构成：FGPrompt、TSEncoder 和 Global-driven Context Learning（GCL）。

首先是 FGPrompt 频率引导提示机制。它对输入序列做 FFT 提取主导频率，将对应周期映射为日、周、月等语义周期描述符；同时用线性拟合估计趋势、用一阶差分变异系数刻画波动性，并按量化规则转成“强上升趋势”“高波动”等语言描述符，拼装成结构化提示文本。该文本经冻结的 GPT-2 编码得到语义嵌入，训练与推理时只需缓存嵌入，无需在线调用 LLM。

其次是频率池与门控融合。引入可学习的频率池表示时序动态的结构原型，以频率幅值和相位特征为查询检索相关向量，再与 LLM 语义嵌入拼接后经门控网络得到融合权重，加权融合为软提示，兼顾离散语言 token 与连续数值特征。

第三是 TSEncoder 与 GCL。TSEncoder 采用 patching 策略并前置可学习 CLS token，提取局部 patch 表示和全局 CLS 表示。GCL 用 CLS 表示经双变换头生成实例级偏移，对软提示的 Key/Value 做残差校准，使语义先验条件化于当前数值状态；随后以数值特征为 Query、校准后的语义嵌入为 Key/Value 做交叉注意力，经残差连接和预测头输出结果。训练采用 Huber 损失增强对异常值的鲁棒性。创新点在于频率语义实例化、频率池检索门控融合以及 CLS 驱动的全局上下文校准对齐。

### Q4: 论文做了哪些实验？

论文在八个预测基准（ETTh1/h2、ETTm1/m2、Exchange、Weather、Electricity、ILI）和五个异常检测数据集（SMD、PSM、SWaT、MSL、SMAP）上进行了实验。预测任务采用MSE和MAE指标，对比了LangTime、TimeCMA、Time-LLM、UniTime、OFA、iTransformer、TimesNet、RLinear等八种基线；异常检测采用精确率、召回率和F1，对比了FPT、TimesNet、LightTS、DLinear、TSINR、AnomalyTransformer。预测方面，FreSia在八个数据集上平均MSE和MAE分别提升13.48%和8.06%，其中ILI数据集MSE/MAE为1.563/0.779，较最强基线降低约18.7%和15.4%；ETTh2、Weather、Exchange也取得更优结果。异常检测平均精确率91.58%、召回率85.58%、F1为88.36%，较FPT提升2.59个百分点，并在SMD、SWaT、MSL、SMAP四个数据集上取得最佳F1。此外还进行了频率池大小敏感性分析，以及LLM、TSE、PE、CA、CLS、Pool等模块的消融实验，验证各组件贡献。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索空间主要体现在三方面。其一，频率池大小需人工调参，且对结果敏感，未来可研究自适应或可学习的频率池构建机制，避免冗余与信息缺失的权衡困境。其二，当前频率-语义对齐主要依赖全局CLS探针与提示投影，缺乏对局部突变、非平稳成分的显式建模，可引入时频联合注意力或小波等多分辨率分解，增强对非周期异常的感知。其三，实验集中于预测与重建式异常检测，尚未验证在分类、插补、少样本迁移等任务上的泛化性。此外，LLM骨干带来的计算开销较大，可探索轻量化蒸馏或仅微调频率适配模块。改进思路包括：将频率提示与文本提示做对比学习式对齐，提升跨域鲁棒性；引入不确定性估计以区分趋势与噪声；以及在真实工业在线流式场景中验证增量更新能力。

### Q6: 总结一下论文的主要内容

论文针对现有多变量时间序列分析方法难以让大语言模型感知数值序列中隐含的季节性与趋势结构这一问题，提出频率感知框架FreSia。其核心思路是在LLM语义空间与时间序列频率空间之间建立对齐：通过FGPrompt机制利用FFT提取主导频率，将周期、趋势、波动等特征转化为自然语言描述并编码为语义提示；同时构建可学习频率池，以频谱幅度和相位为查询检索结构化原型，并通过门控机制与语义嵌入融合。此外，引入全局驱动上下文学习模块，利用CLS探针生成实例级偏移，对提示空间进行校准，再经交叉注意力融合时频多模态表示。实验表明，FreSia在八个预测基准上MSE和MAE平均分别改善13.48%和8.06%，并在五个异常检测数据集上取得最优平均F1，验证了频率-语义对齐在两类任务中的有效性与泛化能力。
