---
title: "A Cost-Effective Multimodal LLM Reasoning Framework for Question Answering over Irregular Clinical Time Series"
authors:
  - "Frank Nie"
  - "Ethan B Liu"
  - "Yuan Zhu"
  - "Wei Fan"
  - "Jindong Han"
date: "2026-07-28"
arxiv_id: "2607.25947"
arxiv_url: "https://arxiv.org/abs/2607.25947"
pdf_url: "https://arxiv.org/pdf/2607.25947v1"
categories:
  - "cs.AI"
  - "cs.CL"
tags:
  - "Multimodal LLM"
  - "Clinical Time Series"
  - "Question Answering"
  - "Irregular Time Series"
  - "Multi-scale Encoder"
  - "Token Compression"
  - "Instruction Tuning"
  - "Healthcare"
relevance_score: 7.5
---

# A Cost-Effective Multimodal LLM Reasoning Framework for Question Answering over Irregular Clinical Time Series

## 原始摘要

Question answering (QA) over irregular clinical time series (ICTS) plays a pivotal role in a wide range of healthcare applications. Although recent multimodal time-series large language models (LLMs) have shown considerable promise in general-purpose time-series QA, they remain poorly equipped to model the sparsity, asynchrony, and irregular sampling patterns of clinical observations. To fill this gap, we propose ClinPRISM, a cost-effective multimodal LLM reasoning framework for question answering over ICTS data. First, we devise an irregularity-aware multi-scale encoder to capture sparse clinical evidence at diverse temporal scales. Then, we propose a temporal evidence distiller to integrate representations across these scales and compress them into a small number of LLM-compatible tokens. Moreover, we introduce a progressive alignment strategy that sequentially aligns the irregular trajectories with the LLM's textual embedding space. To facilitate training, we construct 30,000 clinical time series paired with multi-scale descriptions, together with 41,000 instruction-tuning instances spanning 11 tasks. Using a 4-billion-parameter LLM backbone, ClinPRISM achieves state-of-the-art performance on the held-out evaluation benchmark while using only 16 time-series tokens and achieving an average inference latency of 0.15 seconds per question.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决不规则临床时间序列（ICTS）问答任务中的核心挑战。研究背景是，ICTS在临床分析和决策中至关重要，但现有模型主要针对分类、预测等预定义任务，无法灵活回答用户关于患者轨迹的自然语言问题。现有方法主要分为三类：文本序列化方法（需大量token且精度低）、表示适配方法（如Time-LLM）以及多模态时间序列LLM（如Chat-TS），但它们都聚焦于规则采样序列，忽略了临床记录的稀疏性、异步性和不规则采样模式。

具体而言，现有方法存在三大不足：第一，无法有效建模不规则时间序列的时变模式和观测过程；第二，临床证据稀疏且分布在多时间尺度上（从全局趋势到局部事件再到单点测量），现有模型难以定位并保留跨尺度证据，同时避免计算冗余；第三，缺乏将不规则时间模式与语言语义对齐的有效监督，且大规模配对数据稀缺。

因此，本文的核心问题是：如何设计一个高效、低成本的多模态LLM推理框架，使其能够处理不规则临床时间序列的稀疏性和异步性，从多尺度证据中提取关键信息，并通过渐进式对齐策略实现时间序列与语言的有效融合，从而在保持低推理延迟（0.15秒/问题）的同时，在11项临床推理任务上取得最优性能。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是文本序列化方法，将数值序列转换为文本提示供LLM直接处理，但这类方法需要大量token且难以保持数值精度。第二类是表示适配方法，如Time-LLM通过文本原型重编程时间序列补丁以利用冻结LLM进行预测，克服了文本序列化的部分局限。第三类是近期出现的多模态时间序列LLM，如Chat-TS和ITFormer，通过可训练token和指令微调连接时间编码器与语言模型。本文与这些工作的核心区别在于：现有方法主要针对规则采样序列，忽略了临床数据的稀疏性和异步性。ClinPRISM专门设计了不规则感知多尺度编码器来捕获不同时间尺度的稀疏临床证据，并通过时间证据蒸馏器将可变长度不规则轨迹压缩为少量LLM兼容token。此外，本文提出了渐进式对齐策略，通过多尺度编码器预训练、层次化描述对齐和QA导向的LLM微调，逐步将不规则时间表示与LLM语义空间对齐。本文还构建了包含30,000条临床轨迹和41,000条指令微调实例的训练资源，覆盖11种任务，这在现有工作中是缺乏的。

### Q3: 论文如何解决这个问题？

论文提出了一种名为ClinPRISM的成本效益多模态LLM推理框架，用于解决不规则临床时间序列（ICTS）上的问答任务。其核心方法围绕三个主要模块构建：首先，设计了一个**不规则感知多尺度编码器**，直接在原始记录上从宏观、中观和微观三个时间尺度捕获稀疏临床证据。该编码器采用观测中心接口，将每个有效测量转换为时间戳感知的事件表示，并通过尺度特定的MLP编码，避免了网格重采样或显式插值。宏观尺度通过可学习查询注意力池化和多头自注意力捕获长期趋势和跨变量上下文；中观尺度使用可学习软窗口捕获片段级动态；微观尺度通过缩放点积注意力保留细粒度时间状态。每个尺度都集成了支持感知聚合，通过加权平均和注意力池化结合观测支持度，防止弱支持的局部估计被误判。

其次，**时间证据蒸馏器**将多尺度表示投影到LLM隐藏空间，进行层次化跨尺度融合，并压缩为固定数量的时间令牌（K=16）。它通过尺度投影模块映射各尺度输出，以中观尺度为桥梁进行融合，并使用可学习查询重采样器从有效令牌中提取紧凑的轨迹级证据。最后，**渐进式时间-语言对齐策略**通过三阶段训练实现：第一阶段用自监督学习预训练多尺度编码器；第二阶段冻结编码器和LLM，通过层次化标题对比损失和尺度间一致性损失对齐时间蒸馏器与语言空间；第三阶段先进行面向QA的蒸馏器微调，再联合优化LoRA和蒸馏器。该框架仅使用16个时间令牌和4B参数LLM，实现了0.15秒/问题的推理延迟，并在基准测试上达到最优性能。

### Q4: 论文做了哪些实验？

论文在CLIR-Bench基准上评估了ClinPRISM，该基准包含11个任务，涵盖时间理解、推理、预测和决策四个能力维度，采用多项选择格式并以准确率为指标。对比方法包括闭源LLM（Gemini-2.5-flash、GPT-5.4 mini）、开源通用LLM（如DeepSeek-V4-flash、Qwen3.5-4B等）、时间序列LLM（如TimeOmni-1、TS-Reasoner等）以及使用t-PatchGNN编码器的不规则时间序列LLM基线。主要结果：ClinPRISM（基于Qwen3-4B）以49.83%的宏平均准确率领先所有开源系统，比最强时间序列基线t-PatchGNN高11.18个百分点，比最佳开源通用LLM KiMi-2.6高0.74个百分点，仅落后GPT-5.4 mini 0.32个百分点。消融实验表明，多尺度编码器（宏、中、微观）和渐进式训练策略（三阶段）均有效，移除任一阶段均导致性能下降。使用16个时间序列令牌时性能最佳（49.83%），平均推理延迟为0.15秒/问题。在观测密度鲁棒性测试中，ClinPRISM的相对变化率仅为1.6%，远低于t-PatchGNN的12.7%，表明其对稀疏数据具有强鲁棒性。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于其仅在4B参数LLM上验证，且依赖固定的16个时间序列token，对更长序列或更复杂任务的泛化性存疑。未来可探索：(1) 动态token预算机制，根据序列稀疏度自适应调整token数量，避免信息丢失或冗余；(2) 将渐进对齐策略扩展到多模态（如文本+图像+时序），以处理ICU中更丰富的临床数据；(3) 引入因果推理模块，使模型能区分相关性与因果关系，提升干预决策的可信度；(4) 探索更高效的训练范式，如利用强化学习从临床反馈中优化对齐策略，减少对大规模标注数据的依赖。

### Q6: 总结一下论文的主要内容

该论文提出了一种经济高效的多模态LLM推理框架ClinPRISM，用于解决不规则临床时间序列（ICTS）上的问答问题。核心贡献在于：首先设计了一个不规则感知的多尺度编码器，以捕获不同时间尺度的稀疏临床证据；其次提出时间证据蒸馏器，将多尺度表示压缩为少量LLM兼容的令牌；并引入渐进式对齐策略，逐步将不规则轨迹与LLM文本嵌入空间对齐。为支持训练，论文构建了3万个临床轨迹与多尺度描述配对数据及4.1万个涵盖11类任务的指令微调实例。使用4B参数LLM骨干，ClinPRISM在保留基准上实现了最先进性能，仅需16个时间令牌，平均推理延迟0.15秒/问题。该工作有效解决了ICTS的稀疏性、异步性和不规则采样挑战，为临床时间序列推理提供了高效且经济的解决方案。
