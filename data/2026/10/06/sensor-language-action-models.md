---
title: "Sensor-Language-Action Models"
authors:
  - "Yuekai Xu"
  - "Zitao Shuai"
  - "Yuzhe Yang"
date: "2026-10-06"
arxiv_id: "2610.08244"
arxiv_url: "https://arxiv.org/abs/2610.08244"
pdf_url: "https://arxiv.org/pdf/2610.08244v1"
categories:
  - "cs.AI"
tags:
  - "Sensor-Language-Action"
  - "多模态传感器"
  - "自然语言接口"
  - "动作预测"
  - "动作解释"
  - "可解释性"
  - "证据接地"
  - "零样本泛化"
  - "临床预测"
  - "手术室"
  - "代谢健康"
  - "基准数据集"
  - "时序语义报告"
relevance_score: 8.5
---

# Sensor-Language-Action Models

## 原始摘要

Sensors are useful not only for understanding the world but also for deciding what to do next. Existing sensor models however largely stop at perception: they recognize states or predict outcomes, leaving actions modeled separately through task-specific and often closed label spaces. We introduce Sensor-Language-Action (SLA) modeling, a framework that connects multimodal sensor observations, natural language, and actions within a unified model. SLA uses language as a semantic interface between sensing and acting, allowing heterogeneous actions to be represented, predicted, and explained while remaining grounded in the underlying sensor evidence. We build a large-scale SLA benchmark consisting of datasets that span more than 116,000 individuals, 79 sensor modalities, and 60 action groups, together with a multi-faceted captioning pipeline that aligns user context, sensor dynamics, and action evidence. Building on this framework, we present OpenSLA, a unified SLA model for hierarchical action prediction, state understanding, and action explanation. Extensive experiments on real-world tasks in clinical prediction, operating rooms, and metabolic health verify its superior performance over the state-of-the-art. OpenSLA also demonstrates intriguing capabilities including language-guided evidence grounding and zero-shot generalization to unseen actions and cohorts.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

现有传感器模型主要停留在感知层面：早期方法将传感器信号映射到固定标签或预测结果，近期的传感器-语言模型虽能生成更丰富的语义描述并对传感器观测进行开放式推理，但这些进展大多止步于“行动”之前。下游决策仍被建模为彼此独立的预测问题，每个任务各有自己的形式化定义和动作空间，导致异构传感器证据、上下文信息与多样化行动之间缺乏统一的关联机制。自然语言恰好可以作为连接感知与行动的桥梁：不同于固定标签，语言能同时表达任务意图、个体上下文、生理状态和行动语义，从而将异构的传感器-行动问题统一表示。因此，本文提出的核心问题是：能否通过一个统一框架对传感器数据、语言和行动进行联合建模？为此，作者提出Sensor-Language-Action（SLA）建模范式，并实例化为OpenSLA——首个联合建模传感器观测、语言与行动的通用框架，将传感器智能从理解观测扩展到推理并解释其支持的各类行动。

### Q2: 有哪些相关研究？

本文的相关研究主要可分为三类。第一类是传感器-动作建模，传统方法多将传感器信号直接映射到动作标签，或引入文本上下文作为条件，但难以灵活融合异构个体信息。本文以语言作为传感与动作之间的语义接口，统一表示、预测和解释异构动作。第二类是传感器与时序基础模型，涵盖通用时序模型及面向ECG、PPG、连续血糖监测、可穿戴和睡眠等生理信号的专用模型，但它们主要聚焦状态理解，而非将传感器动态转化为动作语义。本文通过共享的传感器-语言-动作接口联合建模观测、语言上下文与动作，弥补这一空白。第三类是传感器-语言建模，如SensorLM、SleepLM利用配对传感器-文本数据和多级描述进行对齐，OpenTSLM则将时序编码器与预训练LLM结合以支持零样本交互。这些工作主要面向传感器-文本对齐而非动作相关语义，且数据与建模流程有限。本文提出多层面描述生成流程，覆盖个体上下文与动作证据，并构建更大规模、跨临床、手术室与日常场景的SLA基准与OpenSLA模型，在动作预测、状态理解与解释上优于现有方法。

### Q3: 论文如何解决这个问题？

论文提出Sensor-Language-Action（SLA）建模范式，核心是以自然语言作为感知与行动之间的语义接口，将多模态传感器观测、语言指令与异构动作统一到同一模型中建模。作者首先系统比较了四种语言模型中心范式：多模态LLM零样本推理、VLA式仅动作微调、SensorLM式传感器-语言对齐，以及动作与语言联合微调，实验发现联合微调在动作预测上持续最优，从而确立了SLA范式。在传感器表示如何注入语言主干的问题上，论文对比了LLaVA式适配器、Flamingo式交叉注意力和直接LoRA微调，结果LoRA在多数任务上最强，因此OpenSLA采用LoRA直接适配LLM。

OpenSLA由三个组件构成：一是带结构化动作预测头的LLM主干，在末位隐状态上挂接必要性二分类头、类别多标签头，以及基于文本嵌入相似度的细粒度动作头，支持灵活动作空间；二是分层传感器编码器，先对每个通道独立编码，再通过Hierarchical Memory以递归查询层逐级压缩长时序列，同时用全局查询捕获样本级语义；三是多模态融合解码器，采用门控残差结构，让语言生成分别交叉注意预测动作画像与检索到的传感器证据，从而生成有据可依的解释。训练目标为动作损失与自回归文本损失的加权和，仅优化传感器编码器、融合解码器与LoRA参数。该设计实现了动作预测、状态理解与解释的统一，并支持语言引导的证据定位与零样本泛化。

### Q4: 论文做了哪些实验？

论文围绕提出的SLA建模范式开展了大量实验。实验设置上，构建了大规模SLA基准，覆盖超过116,000名个体、79种传感器模态和60个动作组，并通过多层面描述生成流程对齐用户上下文、传感器动态与动作证据。数据集/基准测试涵盖临床预测、手术室和代谢健康等真实世界任务。对比方法为现有最先进（state-of-the-art）模型。主要结果方面，OpenSLA在临床预测、手术室和代谢健康任务上均取得优于SOTA的性能，验证了统一SLA建模的有效性。此外，OpenSLA还展示了语言引导的证据定位能力，以及对未见动作和未见人群的零样本泛化能力。关键数据指标包括：116,000+个体、79种传感器模态、60个动作组，以及三类真实应用场景。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于：SLA 虽以语言为统一接口，但动作空间仍依赖预定义的动作组与标注体系，对开放世界中连续、长时程、多主体协作动作的建模能力有限；多模态传感器在真实部署中常存在缺失、异步、噪声与隐私约束，当前基准未必充分覆盖这些退化场景；语言作为中间层也可能引入语义偏差，导致解释看似合理却与传感器证据不一致。未来可探索：一是引入因果推断与反事实解释，区分相关性与可执行决策依据；二是发展在线、增量与个性化适应机制，使模型能在少标注甚至无标注的个体上持续学习；三是将动作从离散标签扩展到连续控制与策略学习，并与强化学习、世界模型结合；四是研究隐私保护下的联邦多模态训练与可验证证据溯源；五是建立更严格的评测，检验跨设备、跨人群、跨任务的鲁棒性与公平性。

### Q6: 总结一下论文的主要内容

本论文提出Sensor-Language-Action（SLA）建模框架，旨在解决现有传感器模型仅停留在感知层面、动作建模与感知分离的问题。SLA以自然语言作为传感与行动之间的语义接口，将多模态传感器观测、语言和异构动作统一建模，使动作可被表示、预测和解释，并始终扎根于传感器证据。作者构建了大规模SLA基准，涵盖超11.6万名个体、79种传感器模态、5项任务和60个动作组，并提出多层面标注流水线对齐用户上下文、传感器动态与动作证据。基于此，论文提出OpenSLA统一模型，支持分层动作预测、状态理解与动作解释，采用LoRA直接适配语言主干并设计分层传感器编码器与多模态融合解码器。在临床预测、手术室和代谢健康等真实任务上，OpenSLA优于现有最优方法，并展现出语言引导的证据定位及对未见动作和队列的零样本泛化能力。
