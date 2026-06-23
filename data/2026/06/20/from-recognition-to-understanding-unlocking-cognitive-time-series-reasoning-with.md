---
title: "From Recognition to Understanding: Unlocking Cognitive Time Series Reasoning with LLMs"
authors:
  - "Xin Qiu"
  - "Junlong Tong"
  - "Yao Zhang"
  - "Yunpu Ma"
  - "Wei Zhang"
  - "Xiaoyu Shen"
date: "2026-06-20"
arxiv_id: "2606.22126"
arxiv_url: "https://arxiv.org/abs/2606.22126"
pdf_url: "https://arxiv.org/pdf/2606.22126v1"
github_url: "https://github.com/EIT-NLP/CognitiveTSR"
categories:
  - "cs.CL"
tags:
  - "时间序列推理"
  - "认知推理"
  - "多模态对齐"
  - "LLM时间序列"
  - "时序QA"
  - "TSCognition"
  - "TSAlign"
  - "语义理解"
  - "时序报告"
  - "时序语义对齐"
relevance_score: 9.5
---

# From Recognition to Understanding: Unlocking Cognitive Time Series Reasoning with LLMs

## 原始摘要

Time series analysis has recently been coupled with Large Language Models (LLMs) to leverage their reasoning and world knowledge capabilities, yet gains remain limited. We attribute this to a fundamental mismatch between existing task formulations and LLM strengths: most settings reduce time series understanding to curve-fitting systems, focusing on low-level prediction while ignoring the semantic, contextual, and reasoning-intensive nature of real-world temporal decision-making.To address these limitations, we introduce TSCognition, a multimodal benchmark for multi-dimensional time series reasoning. It collects real-world time series and textual information from 15 public sources and constructs approximately 41K QA samples around five cognitive reasoning tasks: Decoding, Grounding, Inferring, Extrapolating, and Acting. Building on this, we further propose TSAlign, a unified framework that encodes time series into compact patch-level representations and aligns them with semantic directions in the LLM embedding space via gated residual injection and multivariate fusion.Experiments show that TSAlign outperforms existing LLM, VLM, and time series QA baselines on TSCognition and the publicly available TimerBed benchmark while substantially reducing computational cost.Code is available at: [https://github.com/EIT-NLP/CognitiveTSR](https://github.com/EIT-NLP/CognitiveTSR)

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决当前将大语言模型（LLM）应用于时间序列分析时存在的根本性错配问题。研究背景是，尽管LLM在自然语言处理中展现了强大的世界知识和推理能力，但在时间序列领域（如预测、分类、异常检测）的应用效果有限。现有方法的不足在于：大多数任务将时间序列理解简化为曲线拟合，聚焦于低层次的模式挖掘（如预测未来点、插值、检测异常），而忽略了真实世界时间序列的随机性、语义性和推理密集型特点。这种任务设定导致LLM的广泛知识、上下文理解和复杂推理能力完全未被利用。本文要解决的核心问题是：如何设计一个能够评估LLM在时间序列上进行高层次认知推理（如解码、接地、推断、外推和行动）的基准数据集，以及如何构建一个高效的对齐框架，将连续的时间序列表示与LLM的离散语言推理空间无缝桥接，从而真正解锁LLM在时间序列分析中的认知推理潜力，而非仅仅将其用作高级曲线拟合器。

### Q2: 有哪些相关研究？

相关研究主要分为两类。第一类是**多模态问答（Multi-Modal QA）**，如视觉-语言基准测试，这些工作将时间序列问题简化为图像理解，但会扭曲时间依赖性；另一类尝试将时间序列离散化或文本化后直接输入LLM，但受限于连续数值与离散符号的固有鸿沟。本文指出这些方法无法处理多变量、多步时间序列推理。第二类是**面向时间序列的语言模型（Language Models for Time Series QA）**，现有工作多将文本作为辅助信号增强预测或分类任务，依赖手工提示或简化设置，且文本化时间序列计算成本高，忽略了时间序列与自然语言之间的模态差异。本文提出的TSCognition基准和TSAlign框架与这些工作的核心区别在于：TSCognition聚焦于认知推理任务（解码、归因、推断、外推、行动），而非低层预测；TSAlign通过门控残差注入和多变量融合将时间序列编码为紧凑的补丁级表示，并与LLM语义空间对齐，从而弥合模态差距，在降低计算成本的同时显著提升推理性能。

### Q3: 论文如何解决这个问题？

论文通过提出TSAlign框架来解决时间序列与LLM推理能力之间的语义鸿沟问题。核心思路是将时间序列编码为与语言空间对齐的紧凑表示，从而让LLM能够直接理解时间序列的语义含义，而非依赖曲线拟合式的低层预测。

整体框架包含三个主要模块。首先是**基于分块的时序编码**，将每个变量的时间序列分割成重叠的补丁序列，通过时序编码器提取每个补丁的嵌入表示，从而捕获局部时间依赖并处理变长序列。其次是**语言空间对齐**，这是关键创新点。由于时序嵌入与语言嵌入空间存在差异，论文对预训练语言模型的嵌入矩阵进行PCA降维，提取主语义方向。然后使用时序嵌入作为查询，主语义方向作为键和值进行注意力对齐，得到语义引导的表示。为了保留原始时序信息，采用**门控残差更新**机制：原始时序嵌入作为主干，语义表示作为受控修正，通过可学习门控控制注入强度，实现逐段语义精炼而不丢失信息。最后是**多变量融合**，针对变量数量不固定的问题，为每个变量计算重要性权重，通过独立门控机制对各变量在每一补丁位置进行加权融合，避免竞争性归一化，使多个信息维度都能贡献。

在推理阶段，将融合后的时序表示通过投影层映射为LLM的临时令牌，与文本问题和候选答案的令牌嵌入拼接，输入LLM进行联合推理。模型采用端到端训练，同时更新时序编码器、投影层和LLM骨干。实验表明，TSAlign在TSCognition和TimerBed基准上优于现有LLM、VLM和时间序列QA基线，同时显著降低了计算成本。

### Q4: 论文做了哪些实验？

论文在TSCognition和TimerBed两个基准上进行了实验。TSCognition包含约41K个QA样本，覆盖解码、接地、推理、外推和行动五类认知推理任务，TimerBed则包含六个数据集（RCW、TEE、ECG、EMG、CTU、HAR），分为简单、复杂和概率三类模式分析任务。对比方法包括通用LLM（GPT-5.1、Qwen2.5-Instruct）、VLM（Qwen2.5-VL）以及时间序列QA方法（ITFormer、Time-MQA、Time-LLM、ChatTS、GPT4TS等），所有方法均以Qwen2.5-Instruct-7B为骨干。主要结果显示：在TSCognition全样本设置下，TSAlign-7B在所有五类任务上均取得最佳准确率（如解码ID 83.1%、推理ID 91.7%），平均超越GPT-5.1达17.7%；在TimerBed上，TSAlign-7B加权平均准确率达64.60%，显著优于传统时间序列模型（如TimesNet 53.28%）和TS-Text方法（如S²IP 52.79%）。消融实验验证了patch级表示、门控残差对齐和门控融合策略的有效性。效率分析显示，TSAlign的token数比视觉输入减少2.96倍，比文本输入减少16.79倍，推理速度分别提升2.23倍和12.31倍。

### Q5: 有什么可以进一步探索的点？

该论文提出的TSCognition基准和TSAlign框架在时间序列推理方面取得了显著进展，但仍存在若干可探索的方向。首先，当前基准主要依赖公开数据集，缺乏对工业场景中高噪声、非平稳、多模态故障信号的覆盖，未来可引入真实工业故障诊断数据（如振动、温度、压力序列）来评估模型在异常检测与根因定位上的认知推理能力。其次，TSAlign的patch-level表示虽然高效，但可能丢失细粒度时序模式（如瞬态冲击特征），可考虑引入可微分时间序列分解模块（趋势-季节-残差）或自适应尺度注意力机制来增强局部敏感度。此外，当前对齐方式依赖静态语义方向，无法动态适应不同推理任务的需求，未来可探索基于任务指令的元学习对齐策略，使LLM能根据问题类型（如因果推断、趋势外推）动态调整嵌入空间。最后，模型在“Acting”任务（如决策建议）上的可解释性仍不足，可结合因果图或反事实推理生成自然语言解释，提升工业场景下的可信度。

### Q6: 总结一下论文的主要内容

这篇论文提出，现有时间序列分析与大语言模型（LLM）的结合存在根本性错配：传统任务将LLM降级为曲线拟合器，未能利用其世界知识和复杂推理能力。为此，论文首先构建了TSCognition基准，这是一个多模态时间序列推理数据集，包含来自15个公开源的约4.1万个问答样本，覆盖解码、接地、推断、外推和行动五种认知推理任务。其次，论文提出TSAlign统一框架，通过将时间序列编码为紧凑的块级表示，并利用门控残差注入与多变量融合将其与LLM嵌入空间的语义方向对齐，从而弥合连续时间序列与离散语言推理空间之间的鸿沟。实验表明，TSAlign在TSCognition和公开TimerBed基准上均优于现有LLM、VLM及时间序列QA基线，同时大幅降低计算开销（比文本输入减少16.8倍token）。核心贡献在于重新定义了时间序列分析任务，从浅层模式预测转向认知推理，并提供了高效的对齐方法，推动了LLM在时间序列领域从“识别”到“理解”的范式转变。
