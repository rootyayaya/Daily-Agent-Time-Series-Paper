---
title: "Structured Frequency-Domain Evidence for LLM-Based Time-Series Anomaly Detection"
authors:
  - "Jungwook Seo"
  - "Sangwon Son"
  - "Minjeong Kim"
  - "Seungmin Han"
  - "Seojin Yoo"
  - "Sungyong Baik"
date: "2026-08-25"
arxiv_id: "2608.24113"
arxiv_url: "https://arxiv.org/abs/2608.24113"
pdf_url: "https://arxiv.org/pdf/2608.24113v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "LLM-based time-series anomaly detection"
  - "frequency-domain evidence"
  - "zero-shot TSAD"
  - "evidence augmentation"
  - "FFT"
  - "AnomLLM"
  - "TSB-AD-U"
  - "multimodal LLM"
  - "time-series interpretation"
relevance_score: 8.5
---

# Structured Frequency-Domain Evidence for LLM-Based Time-Series Anomaly Detection

## 原始摘要

Time-series anomalies can appear not only as pointwise deviations but also as changes in recurring temporal structure, such as shifted periodicity or localized oscillatory fluctuations. However, existing LLM-based time-series anomaly detection methods mainly expose time-domain evidence through indexed values, plots, or de-seasonalized representations, leaving spectral structure implicit. We propose an evidence-augmented zero-shot TSAD framework that preserves indexed de-seasonalized observations while adding compact frequency-domain evidence computed with the Fast Fourier Transform (FFT). The evidence is constructed at two resolutions: global frequency-domain evidence summarizes sequence-level periodic context, while local frequency-domain evidence captures time-localized spectral departures. Experiments on AnomLLM with InternVL2-LLaMA3-76B, Qwen2.5-VL-72B-Instruct, Gemini-2.5-Flash, and GPT-4o, together with evaluation on the TSB-AD-U subset, show that explicit frequency-domain evidence improves LLM-based TSAD baselines. These results suggest that frequency-domain evidence can complement indexed and de-seasonalized time-domain inputs for zero-shot LLM-based TSAD.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列异常不仅表现为点值偏离，还可能体现为周期性结构的变化，如周期移位或局部振荡波动，这类异常天然与频率特征相关。然而，现有基于大语言模型（LLM）的时间序列异常检测方法主要依赖时域证据——通过索引数值、可视化图表或去季节化序列来呈现信息，虽然能帮助模型理解时间顺序和区间边界，却未显式地概括频谱属性（如主周期、谱能量分布或时变频率变化），导致频谱结构信息隐式缺失。

此外，传统频率感知的TSAD方法通常将频谱信息编码进特定模型架构或监督训练流程中，而非作为可直接供通用LLM利用的输入证据，形成了表示层面的证据鸿沟。本文旨在解决这一核心问题：如何将显式的频域证据构建为输入级表征，使零样本LLM能够直接基于频谱信息进行异常定位。具体而言，作者提出一种无需训练的证据增强框架，利用快速傅里叶变换（FFT）生成全局频域证据（概括序列级周期背景）和局部频域证据（捕捉时间窗口内的谱偏离），与索引化的去季节化时域观测相结合，从而在不依赖预定义异常类别或辅助监督的情况下，提升LLM对周期性结构异常检测的准确性与可解释性。

### Q2: 有哪些相关研究？

相关研究主要围绕LLM在时间序列异常检测（TSAD）中的应用，可分为三类。**方法类**：现有工作如AnomLLM等，主要依赖时间域证据（索引值、绘图、去季节化表示）进行零样本检测，但忽略了频域结构；本文首次提出显式频域证据增强框架，通过FFT构建全局与局部两级频谱摘要，弥补了LLM从纯时间域输入中难以恢复周期信息的缺陷。**诊断/评测类**：TSB-AD-U等基准用于评估TSAD性能，但缺乏对频域推理能力的隔离测试；本文设计了合成正弦波探针（单频、多频、局部频率变化），系统验证了LLM在隐式频域推理上的不足，并证明全局证据提升序列级频率恢复、局部证据改善异常定位，与TSAD结果一致。**应用类**：多模态LLM（如InternVL2-LLaMA3、Qwen2.5-VL、GPT-4o）被用于零样本TSAD，但均未显式利用频谱信息；本文在多个模型上验证了频域证据的通用增益。与这些工作相比，本文的核心区别在于将频域信息作为结构化、可解释的外部证据显式注入，而非依赖模型隐式推断，从而显著提升了对周期性变化类异常的检测能力。

### Q3: 论文如何解决这个问题？

该论文提出了一种基于显式频域证据增强的零样本时间序列异常检测框架，旨在弥补现有LLM方法仅依赖时域索引值或去季节化表示、隐含频谱结构信息不足的缺陷。整体框架包含三个核心模块：全局频域证据、局部窗口频域证据和证据融合预测模块。

全局频域证据通过对完整去季节化序列应用快速傅里叶变换（FFT），提取四个紧凑描述符：主导周期、最强频谱峰、全局频谱熵以及低/高频能量比。这些描述符共同构成序列级周期参考，用于判断局部频谱偏离是否相对于整体周期模式异常。

局部频域证据采用滑动窗口策略，将序列划分为重叠窗口，对每个窗口计算主导局部频率和局部频谱熵，并以（起始索引，结束索引，主导频率，频谱熵）四元组形式呈现。这些元组提供时间定位的频谱偏离线索，但仅作为辅助证据而非异常边界。

最终预测阶段将索引化去季节化序列、全局频域证据、局部频域证据以及可选的时序图整合为单一提示包输入LLM，通过区间预测方式输出异常区间集合。该设计的创新点在于：一是显式构造频域证据，避免LLM从数值中隐式推断周期结构；二是全局与局部双分辨率设计，兼顾整体周期背景与局部节奏变化；三是证据仅作为辅助支持，不替代时域主证据，保持去季节化表示的定位优势。实验在AnomLLM框架下验证了该方法对多种LLM基线的提升效果。

### Q4: 论文做了哪些实验？

论文在AnomLLM和TSB-AD-U两个基准上评估了所提出的频域证据增强零样本时间序列异常检测方法。实验设置包括四种多模态大模型：InternVL2-LLaMA3-76B、Qwen2.5-VL-72B-Instruct、Gemini-2.5-Flash和GPT-4o，采用标准指标和隶属度指标（精确率、召回率、F1）进行评估。

在AnomLLM主实验中，对比了AnomLLM提示变体、LLM-TSAD基线及朴素预测器。结果显示，加入频域证据后，所有模型在标准F1和隶属度F1上均优于LLM-TSAD。例如，Qwen2.5在文本+视觉设置下标准F1从67.56提升至73.70，隶属度F1从81.87提升至91.39；GPT-4o的隶属度F1从80.11提升至87.35。

消融实验验证了局部频域证据（LF）和全局频域证据（GF）的互补作用，添加GF后所有模型标准F1均提升。类型分析显示，频域证据对频率变化和趋势偏移异常增益最大。在TSB-AD-U子集上，使用Gemini-2.5-Flash时，本方法标准F1达40.26，优于LLM-TSAD的36.85，隶属度F1保持可比（80.35 vs 80.15）。

### Q5: 有什么可以进一步探索的点？

当前工作虽验证了频域证据对LLM时间序列异常检测的有效性，但仍存在若干可深化的方向。首先，零样本异常定位的精度有限，且模型对频域、时域及视觉证据的依赖机制尚不明确，未来可引入基于注意力归因或因果干预的分析，揭示LLM内部决策路径。其次，当前全局与局部频域特征仅通过FFT提取，可尝试自适应频带选择或小波变换以捕捉非平稳信号的时变谱结构。此外，证据融合方式较为简单，可设计可学习的跨模态融合模块，或利用多轮对话让模型逐步修正预测。最后，现有评估集中于TSB-AD-U子集，未来可扩展至更多工业场景，并探索频域证据在少样本微调或在线检测中的潜力，以增强泛化性与实时性。

### Q6: 总结一下论文的主要内容

本文提出了一种面向LLM的时间序列异常检测增强框架，旨在解决现有方法仅依赖时域证据（如索引值、去季节化表示）而忽略频域结构的问题。该框架在保留索引化去季节化观测的同时，利用快速傅里叶变换（FFT）构建紧凑的频域证据，分为全局和局部两个分辨率：全局证据概括序列级周期上下文，局部证据捕捉时间局部的频谱偏离。实验基于AnomLLM，结合InternVL2-LLaMA3-76B、Qwen2.5-VL-72B-Instruct、Gemini-2.5-Flash和GPT-4o等多模态LLM，并在TSB-AD-U子集上评估，结果表明显式频域证据能显著提升LLM基线的异常检测性能，尤其对涉及节奏、周期或渐变时间变化的异常有效。该工作证实频域证据可作为时域输入的互补，为零样本LLM时间序列异常检测提供了新思路，并启发未来面向更长或多元序列的自适应频域证据构建。
