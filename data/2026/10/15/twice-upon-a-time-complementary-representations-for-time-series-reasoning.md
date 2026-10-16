---
title: "Twice Upon a Time: Complementary Representations for Time-Series Reasoning"
authors:
  - "Hedi Zisling"
  - "Liran Nochumsohn"
  - "Ilan Naiman"
  - "Mihir Parmar"
  - "Omri Azencot"
date: "2026-10-15"
arxiv_id: "2610.22327"
arxiv_url: "https://arxiv.org/abs/2610.22327"
pdf_url: "https://arxiv.org/pdf/2610.22327v1"
categories:
  - "cs.LG"
  - "cs.AI"
  - "cs.CL"
tags:
  - "Time Series Language Models"
  - "Complementary Representations"
  - "Delay Embedding"
  - "Visual Encoding"
  - "Multi-level Feature Fusion"
  - "Time Series Reasoning"
  - "TSRBench"
  - "Multivariate Time Series"
  - "Qwen3-VL"
  - "Invariance Analysis"
relevance_score: 7.5
---

# Twice Upon a Time: Complementary Representations for Time-Series Reasoning

## 原始摘要

Time Series Language Models (TSLMs) enable language-based understanding and reasoning over temporal data, yet a fundamental question remains: what information should their time-series representations preserve, and what variation should they factor out? Existing TSLMs typically expose the language model to a single representation, imposing a fixed inductive bias across downstream tasks. We instead introduce complementary representations as a design principle for time-series reasoning. Our model combines two visual views: line plots preserve absolute measurements and the observed coordinate frame, while normalized delay embeddings factor out positive amplitude rescaling and offsets while exposing temporal structure. Dedicated visual encoders integrate both views into a shared language model through visual tokens and multi-level feature fusion. Evaluation-time interventions verify that the two views exhibit distinct invariance profiles, while single-view ablations show that their combination is particularly beneficial beyond basic perception, with the large gains in prediction and reasoning. Built on Qwen3-VL-8B, our dual-view model improves overall TSRBench accuracy from 44.5% with line plots alone to 53.2%, substantially exceeding the strongest evaluated dedicated TSLM baseline at 36.7%. It further achieves 89.9% accuracy on TSExam and 86.8% numerical accuracy on multivariate ChatTS alignment. Together, these results demonstrate that complementary representations provide an effective design principle for general-purpose TSLMs, enabling models to exploit temporal structure without sacrificing access to the original measurement frame.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列语言模型（TSLM）旨在将大语言模型的推理与交互能力扩展到时序数据，但一个核心问题尚未解决：时序信号应以何种表示形式输入语言模型？现有方法通常只采用单一表示，例如将数值序列化为文本、学习专用时序嵌入，或把时序编码器特征投影到语言模型空间。这些做法施加了固定的归纳偏置：保留绝对幅度与坐标系的表示利于定量读取，而归一化表示则抑制绝对尺度、突出相对结构与动态模式。近期研究表明，仅将时序画成折线图就能让通用视觉语言模型获得较强的时序理解能力，说明表示方式本身而非模型规模或训练策略，才是决定时序推理能力的关键因素。然而，单一表示难以同时满足两类需求：既需要原始测量框架以支持定量问答，又需要剥离幅度与偏移以暴露时间结构。因此，本文要解决的核心问题是：能否通过互补表示提升通用时序推理？具体而言，本文提出以折线图与归一化延迟嵌入两种互补视觉视图作为设计原则，并构建双塔TSLM，使模型在不牺牲原始测量框架的前提下充分利用时间结构，从而在感知、预测、推理与决策等任务上取得更优表现。

### Q2: 有哪些相关研究？

本文的相关研究主要分为两大类。

**时间序列表示类。** 经典方法将时序转换到频域、时频域、递归图或延迟嵌入等替代坐标系，以暴露不同信号结构。Wang与Oates提出Gramian角场和马尔可夫转移场，将时序编码为二维图像用于分类与插补；近期工作进一步证明基于延迟嵌入和短时傅里叶变换的图像化表示可作为时序与视觉扩散模型之间的有效接口。这些工作说明替代表示能揭示有用且不同的结构，但本文的区别在于：不再为特定预测或生成任务选择单一表示，而是联合组合互补表示以服务通用时序推理，让模型同时保留不同信息并诱导不同不变性。

**时序语言模型（TSLM）类。** 早期工作聚焦预测，通过文本序列化、文本提示或表示对齐与重编程来适配语言模型。近期研究将范式扩展到自然语言理解与推理：ChatTS通过指令微调将学习到的时序嵌入与LLM对齐；OpenTSLM探索软提示与交叉注意力接口；TimeOmni-1直接在语言模型token空间表示数值序列；TS-Reasoner将预训练时序基础模型与LLM对齐。此外，评测研究表明通用视觉语言模型以折线图形式即可有效推理时序。与这些工作不同，现有TSLM大多只向语言模型暴露单一主表示，而本文强调表示作为互补归纳偏置的来源，联合提供保留不同信息、具有不同不变性的多视图。

### Q3: 论文如何解决这个问题？

论文的核心思路是用“互补表示”替代单一表示，让语言模型同时看到保留绝对测量框架的线图视图和剥离正幅值缩放与偏移的归一化延迟嵌入视图。整体框架以 Qwen3-VL-8B 为语言模型骨干，每个时间序列被渲染成两个视觉视图，分别送入专用视觉编码器，再投影到共享语言模型表示空间。线图视图由 Qwen3-VL 原生视觉管线处理，保留原始数值范围和坐标轴信息，输出约 230 个 plot token；延迟嵌入视图则把重叠时间窗堆叠成图像，使周期表现为平行条纹、趋势表现为平滑梯度，由 DINOv3 ViT-L/16 编码，经两层投影得到 64 个 delay token。为增强融合，论文把 DeepStack 机制扩展到延迟流，从 DINOv3 第 6、12、18 层抽取多级特征，分别投影后注入语言模型前三层，与线图流的多级特征在同一层但不同 token 位置相加。两个视图以独立视觉跨度、由 vision_start 和 vision_end 包裹，与文本查询一起进入同一自回归语言模型，实现输入级融合而非集成或独立头。训练分两阶段：第一阶段冻结语言模型和 Qwen 视觉编码器，只训练 DINOv3 上的 LoRA 及投影模块，用描述数据对齐延迟流；第二阶段合并 DINOv3 适配器，冻结整个视觉通路，对语言模型加 LoRA 进行时间序列问答指令微调。创新点在于把互补表示作为设计原则，通过双视图与多级融合让模型既保留原始测量框架，又利用与正幅值变换无关的时间结构，从而在预测和推理任务上显著提升。

### Q4: 论文做了哪些实验？

论文在三个基准上评估模型：TSRBench（4125道多选题，覆盖感知、推理、预测、决策共15个任务）、TSExam（746道题，涵盖模式识别、噪声理解、异常检测、相似性与因果）以及ChatTS（单变量与多变量序列的类别/数值对齐及高层推理）。对比方法包括通用视觉语言模型Qwen3-VL-8B（自身骨干）与GPT-5（大模型参考），以及专用TSLM基线ChatTS-14B、TS-Reasoner-7B、TimeOmni-1-7B。主要结果：双视图模型在TSRBench总体准确率从仅折线图的44.5%提升至53.2%，显著超过最强专用TSLM基线的36.7%；在TSExam上达89.9%，在ChatTS多变量对齐上数值准确率达86.8%。消融实验显示，仅Delay视图为40.5%，仅Plot视图为45.2%，Delay+Delay为42.6%，Plot+Plot为44.8%，均低于双视图组合，验证了互补表示在预测与推理任务上的增益。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：其一，互补表示目前仅以“线图+归一化延迟嵌入”这一种组合形式实现，未探索其他不变性维度（如周期性、趋势、多尺度结构）的表示设计；其二，评估集中于多项选择与对齐任务，缺乏对真实工业场景中噪声、缺失值、非平稳分布的鲁棒性验证；其三，双视图融合依赖视觉编码器，计算开销与推理延迟未充分讨论。未来可探索：一是自适应视图选择机制，让模型根据任务动态决定保留或丢弃绝对坐标信息，而非固定融合；二是将互补表示原则扩展到多变量通道间关系与频域表示，构建更丰富的“不变性字典”；三是引入可解释性分析，量化每个视图对具体推理步骤的贡献，从而指导表示设计；四是结合因果推断，区分时间序列中的虚假相关与真实因果结构，提升决策任务可靠性。

### Q6: 总结一下论文的主要内容

本论文探讨时间序列语言模型（TSLM）应保留何种信息、忽略何种变化这一核心问题。现有方法通常仅采用单一表示，施加固定的归纳偏置。作者提出“互补表示”设计原则，构建双视图模型：折线图保留绝对测量值与坐标框架，归一化延迟嵌入则消除正幅度缩放与偏移，突出时间结构。两个专用视觉编码器通过视觉token与多层特征融合接入共享语言模型。基于Qwen3-VL-8B，该模型在TSRBench上总体准确率从单折线图的44.5%提升至53.2%，远超最强专用TSLM基线36.7%；在TSExam上达89.9%，多变量ChatTS数值对齐达86.8%。评估干预验证两视图具有不同不变性，消融表明组合在预测与推理任务上增益显著。结论是互补表示是通用TSLM的有效设计原则，使模型既能利用时间结构，又不丢失原始测量框架。
