---
title: "Learning Evidence-Grounded Reasoning for Context-Aware Time Series Forecasting"
authors:
  - "Xingpeng Gao"
  - "Mingyue Cheng"
  - "Daoyu Wang"
  - "Huajian Zhang"
  - "Xiaoyu Tao"
date: "2026-11-09"
arxiv_id: "2611.12285"
arxiv_url: "https://arxiv.org/abs/2611.12285"
pdf_url: "https://arxiv.org/pdf/2611.12285v1"
categories:
  - "cs.LG"
tags:
  - "LLM时间序列预测"
  - "证据推理"
  - "思维链"
  - "强化学习"
  - "上下文特征"
  - "可解释预测"
  - "多教师蒸馏"
  - "数据平衡"
  - "多域基准"
relevance_score: 8.5
---

# Learning Evidence-Grounded Reasoning for Context-Aware Time Series Forecasting

## 原始摘要

LLM-driven time series forecasting has become increasingly promising by leveraging contextual features to generate future values directly or refine forecast priors. However, incorporating contextual features alone does not ensure that models can identify which features matter for forecasting and understand what they suggest about future dynamics. We argue that the fundamental challenge is how to extract predictive evidence from contextual features and when and how to leverage it to guide forecasting decisions. In this paper, we propose CastReasoner, an evidence-grounded reasoning model for context-aware time series forecasting. Specifically, CastReasoner uses a structured chain of thought (CoT) to extract predictive evidence from contextual features, infer the future dynamics suggested by this evidence, and assess these dynamics against the forecast prior to guide adaptive forecasting decisions. To enable this capability, we design a reasoning-centric two-stage post-training framework including supervised fine-tuning (SFT) and reinforcement learning (RL). First, we synthesize reasoning trajectories through controllable multi-teacher guidance and select high-quality ones using a novel student-aware difficulty metric. Second, we design fine-grained multi-objective rewards to further improve reasoning and forecasting. To address heterogeneous learning needs across domains in both stages, we introduce a convergence-guided data balancing strategy. Through this two-stage training, CastReasoner improves both reasoning quality and predictive accuracy. Extensive experiments across multi-domain forecasting benchmarks demonstrate that CastReasoner achieves superior forecasting performance.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是LLM驱动的上下文感知时间序列预测问题。近年来，利用大语言模型结合外生变量、日历信息和领域知识等上下文特征进行预测成为有前景的方向，现有方法主要沿两条路线展开：一是直接由历史模式与上下文影响生成未来值，二是对来自独立预测器（如时间序列基础模型）的预测先验进行修正。然而，论文指出，仅仅把上下文特征纳入模型，并不能保证模型识别出哪些特征对预测真正重要，也无法理解这些特征对未来动态意味着什么。缺乏这种依据支撑时，推理可能遗漏关键线索或引入误导信息，从而损害逐时刻的预测生成或修正。因此，本文认为核心挑战在于：如何从上下文特征中提取预测证据，以及何时、如何利用这些证据来指导预测决策。具体而言，证据提取需要结合目标历史判断哪些上下文与目标和预测视野相关，区分有用证据与冗余或误导信息；证据还需用于推断未来变化的时间、方向和幅度，并在存在预测先验时判断哪些影响已被先验捕捉、何处需要调整。为此，作者提出CastReasoner，通过结构化思维链提取预测证据、推断其暗示的未来动态，并与预测先验对照，以决定保留、修正还是重建预测，从而连接上下文解释与自适应预测策略及完整数值预测。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类。方法类方面，早期LLM时间序列预测将数值历史视为语言序列，通过文本补全实现预测；随后出现重编程（将历史模式映射到预训练语言模型嵌入空间）、符号离散化（使数值兼容上下文描述）和向量注入示例（通过上下文学习适配冻结LLM）等工作。应用类方面，研究逐步从表示历史扩展到引入外部影响：语言知识用于建模目标序列与外生变量的交互，检索方法引入相关序列与文本支持跨城市预测，地理图像提供空间信息辅助交通预测；事件驱动预测则解读外部报告并用反思精炼预测，近期时间推理通过中间分析连接观测模式与未来行为。评测与训练类方面，后训练日益关注数值预测背后的推理过程：监督适配用合成轨迹示范时间分析先于数值预测，强化学习以预测专用多目标奖励评估轨迹，过程可验证标注进一步检查中间推理，修订轨迹与可验证奖励教模型依据多模态上下文保留、修订或舍弃基础模型先验。与上述工作不同，本文指出连接上下文证据与预测先验、以及区间特定预测决策的监督仍有限，故提出CastReasoner，以兼顾准确性与学生可学性的示范选择加细粒度奖励强化学习来构建证据接地的推理。

### Q3: 论文如何解决这个问题？

论文提出 CastReasoner，一个面向上下文感知时间序列预测的“证据锚定推理”模型，核心在于让模型从上下文特征中抽取预测证据，并据此指导对预测先验的自适应修正。整体框架上，模型以固定提示序列化输入（目标历史、预测期可用上下文特征、Chronos-2 生成的预测先验），由 LLM 生成结构化思维链，再解析出完整数值预测。推理链分为三阶段：证据分析识别外生变量、日历信号与领域信息中对未来动态有影响的条件，推断变化的方向、强度、起始、持续与形态，并与先验区间对比找出已体现、低估、高估或错位的效应；策略选择据此决定保留（retain）、有界修正（revise）还是重构（reconstruct）先验；预测构建则将策略与证据转化为全部 H 步数值，并记录策略、证据、方法与预测的完整轨迹。

为训练该能力，作者设计以推理为中心的两阶段后训练：先用四个教师模型（DeepSeek、GPT、GLM、Claude）在相同输入下生成多样化推理轨迹，按 MAE 过滤无效候选，并提出学生感知难度（SAD）指标——结合冻结学生模型下 token 的排名与负对数概率，在 MAE 最优的两个候选中择优，兼顾准确性与可学习性；随后用 GRPO 强化学习，设计格式、预测精度、超越简单基线、区间级先验修正、教师推理偏好五类细粒度多目标奖励。针对跨域学习需求异质，提出收敛引导的数据平衡策略，以试点模型各域收敛步长的平方根确定采样配额，并在 SFT 与 RL 两阶段固定使用。创新点在于将证据抽取、动态推断与先验干预显式串联为可解释推理链，并以学生感知轨迹筛选与多目标奖励实现推理质量与预测精度的联合提升。

### Q4: 论文做了哪些实验？

论文在八个数据集上评估预测精度，并分析推理与训练组件及上下文证据对预测决策的影响。长期预测使用GEFCom2014的Load、Price、Solar、Wind四个能源数据集；短期预测使用UCI的Bike Sharing、Beijing Multi-Site Air Quality、Hierarchical Sales和MetroPT-3，覆盖城市出行、环境、零售和工业监测领域，指标为nMAE和nMSE。对比方法分四类：统计方法ARIMA、Prophet；深度学习方法PatchTST、iTransformer、TimeXer、TiDE；基础模型Chronos-bolt、Chronos-2、TimesFM-2.5、Moirai、Sundial；推理LLM包括TimeReasoner、Time-R1、PostTime。主结果用Qwen3.5-9B，辅助实验用4B，SFT用2000条轨迹训练3轮，GRPO强化学习2轮，在四块80GB H100上训练。结果表明CastReasoner在全部八个数据集上nMAE和nMSE均排名第一，十六项指标全面优于次优的PostTime；在MetroPT-3上较PostTime降低30.1%的nMSE，在Wind上较Chronos-2先验降低37.5%的nMAE和58.2%的nMSE。消融显示去掉证据分析影响最大，去掉SFT比去掉RL退化更明显；推理轨迹干预中原始轨迹最优，损坏轨迹最差；多教师监督和结合学生可学习性的轨迹选择均优于单教师与随机/仅精度选择；奖励消融中精度奖励最关键；证据分组分析显示无证据时78.8%选择保留先验，局部证据倾向修正（65.9%），广泛影响时重建比例从19.0%升至42.1%。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有以下几点。其一，模型依赖Qwen3.5-9B等大模型与四张H100训练，推理成本高、部署门槛大，未来可探索蒸馏到小模型或轻量化推理路径，并验证0.8B等小容量模型在证据抽取上的稳定性。其二，证据分组依赖四个教师LLM投票标注，存在主观性与标注噪声，可引入可验证的客观证据标签或不确定性建模，提升证据识别的可靠性。其三，实验集中于能源、环境、零售、工业监测，缺乏高频、多变量强耦合或极端事件场景，未来可扩展到故障预警、突变检测等任务，检验证据推理在分布漂移下的鲁棒性。其四，当前"保留/修正/重构"三策略较为粗粒度，可探索更细粒度的区间级干预与置信度校准，并结合在线学习实现先验与证据的动态融合。此外，教师轨迹合成与收敛引导数据平衡策略可进一步研究跨域迁移与课程式训练，降低对多教师标注的依赖。

### Q6: 总结一下论文的主要内容

论文针对上下文感知时间序列预测中的核心问题：仅引入上下文特征并不能保证模型识别出对预测真正重要的证据，也难以理解这些证据对未来的含义。作者将问题定义为如何从上下文特征中提取预测证据，并决定何时、如何利用证据指导预测决策。为此提出CastReasoner，一种基于证据推理的LLM预测模型，采用结构化思维链分三阶段工作：证据分析、策略选择（保留、修正或重建预测先验）、预测构建。为训练该能力，设计了以推理为中心的两阶段后训练框架：先通过多教师可控生成与“学生感知难度”指标筛选高质量推理轨迹进行SFT，再用细粒度多目标奖励（格式、精度、超越基线、区间修正、教师偏好）进行GRPO强化学习，并用收敛引导的数据平衡策略应对跨域异构学习需求。在能源、城市出行、空气质量、零售、工业监测等八个真实数据集上，CastReasoner在全部指标上优于统计、深度学习和推理LLM基线，消融实验验证了三阶段推理、SFT与RL及各奖励项的互补作用，表明连贯的中间推理能有效将上下文证据转化为数值预测。
