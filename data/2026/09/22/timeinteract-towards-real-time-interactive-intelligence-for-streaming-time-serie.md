---
title: "TimeInteract: Towards Real-Time Interactive Intelligence for Streaming Time Series"
authors:
  - "Sheng Pan"
  - "Yongli Gu"
  - "Yiqing Guo"
  - "Warren Jin"
  - "Bo Du"
  - "Shirui Pan"
  - "Ming Jin"
date: "2026-09-22"
arxiv_id: "2609.26389"
arxiv_url: "https://arxiv.org/abs/2609.26389"
pdf_url: "https://arxiv.org/pdf/2609.26389v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Streaming Time Series"
  - "Time-Series Language Models"
  - "Interactive Intelligence"
  - "Real-Time Anomaly Detection"
  - "Response Triggering"
  - "Dual-View Encoder"
  - "Decoupled Inference"
  - "StreamTSI-34K"
  - "Agentic Time Series"
  - "Semantic Report Generation"
relevance_score: 8.5
---

# TimeInteract: Towards Real-Time Interactive Intelligence for Streaming Time Series

## 原始摘要

Real-world time series evolve continuously, with meaningful changes potentially emerging at any moment. However, existing time-series language models (TSLMs) remain inherently static. They either receive complete sequences for offline processing or alternate between streaming input and response generation, which prevents processing of new observations during interaction. We introduce a new regime, Time-Series Interaction: a model continuously perceives incoming time-series observations and user intent, autonomously decides when to remain silent or respond, and continues processing new observations during response generation. To realize this, we develop TimeInteract with three key designs: a dual-view streaming TS encoder that captures local variations and historical dynamics, a response control mechanism that learns when to trigger a response, and a decoupled streaming inference mechanism that separates control from response generation to avoid blocking subsequent observations. We further formulate a hierarchy of interaction capabilities, progressing from Understanding to Adaptivity. Based on this hierarchy, we construct StreamTSI-34K, a large-scale streaming TS interaction dataset with 34,588 episodes and 77,505 responses across synthetic and real-world time series in single- and multi-turn settings. Across all four interaction levels, TimeInteract consistently outperforms existing LLMs, VLMs, and TSLMs, with gains of up to 23.92 points on challenging tasks. It also improves response triggering while achieving near-zero stream stall and up to $2.15\times$ inference speedup.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决流式时间序列场景下大语言模型无法实现实时交互的问题。在医疗监控、工业系统、金融市场等领域，时间序列数据持续增量到达，用户意图也可能随时变化，因此模型需要持续跟踪数据流并及时响应。然而，现有时间序列语言模型（TSLM）本质上是静态的：离线TS语言模型需等待完整序列输入后才生成响应，在高频流上延迟显著；交错式流模型虽能增量处理输入，但响应生成仍会阻塞后续观测的接收，导致输入与输出耦合，无法真正做到实时交互。此外，该领域还缺乏系统化的任务定义和大规模流式交互数据。本文的核心目标是提出一种新的“时间序列交互”范式，使模型能够持续感知流入的观测和用户意图，自主决定何时保持沉默或响应，并在生成响应的同时继续处理新观测。为此，作者提出TimeInteract模型，通过双视角流式编码器、响应触发机制和解耦式流式推理机制，将流处理与响应生成解耦，并构建了能力层级和StreamTSI-34K大规模数据集，以系统评估和推动流式时间序列交互能力的发展。

### Q2: 有哪些相关研究？

现有相关研究主要可分为三类。方法类方面，基于LLM的时间序列分析工作将预训练LLM的知识迁移到预测、异常检测等任务，并进一步扩展到基于语言的时间序列理解，如TSLM通过文本输入或时间表示与语言交错来支持描述、问答与时间推理，近期还涉及多轮分析工作流。但这些方法大多依赖预先完整可获得的时间序列上下文，而非在交互过程中持续到达和演化的观测。应用类方面，流式多模态交互在音频和视频领域发展迅速，如流式ASR、口语对话系统通过增量处理降低延迟，Audio Interaction Model统一了感知、响应决策与生成，JoyAI-VL-Interaction进一步学习何时响应、沉默或委派。评测类方面，现有工作多针对音频、视频交互构建基准，缺乏面向流式时间序列的交互数据集与能力层级。与上述工作不同，本文首次提出面向流式时间序列的交互模型TimeInteract，并构建StreamTSI-34K数据集，定义从理解到自适应的交互能力层级，实现持续感知、自主决定响应时机且生成时不阻塞后续观测。

### Q3: 论文如何解决这个问题？

论文提出TimeInteract框架，将流式时间序列交互建模为持续感知、自主决策与异步响应的闭环过程。整体架构包含三个核心模块。第一，双参考归一化与快慢流编码器：对每个新到达的时间块，同时构造当前视图（用当前块统计量归一化，突出局部变化）和历史视图（用累积历史统计量归一化，反映相对历史漂移），再分别送入两个独立的Mamba编码器。快流更新率α_F大于慢流α_S，使快流快速响应近期变化、慢流长期保留历史动态，且SSM状态跨块持久化，实现增量编码而无需回看全部历史。第二，响应控制与潜在计划：控制头根据因果上下文预测silent或respond，仅在respond时由Plan头生成紧凑的连续Plan token，作为响应的压缩表示并留在控制历史中，供后续决策使用，从而无需等待完整回复即可继续处理新观测。第三，解耦流式推理：将推理拆分为持久的控制流与临时的响应流，共享同一LLM但使用独立KV缓存。当触发响应时，通过KV forking把缓存复制为控制分支和响应分支，响应异步生成，新观测继续扩展控制分支，实现近零流阻塞与最高2.15倍加速。训练上采用Full-to-Plan蒸馏，让Plan token保留后续交互所需信息，并设计三阶段流水线逐步学习交互格式、响应时机与大规模多轮流式交互。

### Q4: 论文做了哪些实验？

论文围绕新提出的“时间序列交互”范式开展了系统实验。实验设置上，覆盖理解、持久性、主动性和适应性四个交互层级，分别在单轮和多轮对话场景下评估，并额外考察实时效率。数据集为作者构建的 StreamTSI-34K，包含34,588个交互片段和77,505条响应，涵盖合成与真实时间序列。对比方法分三类：通用LLM（Qwen2.5-7B-Instruct、Mistral-7B-Instruct-v0.3、Qwen3-14B）、视觉语言模型（Qwen2.5-VL-7B、InternVL3.5-8B）和时间序列语言模型（ChatTS、TimeOmni-1）。评价指标包括语义正确性SC、指令完成率IFR、触发精确率/召回率/F1及NQ-F1，以及TTFT和完成延迟等效率指标。主要结果：TimeInteract在四个交互层级均排名第一，单轮UGA提升22.22分，多轮提升23.92分；多轮下性能稳定，如IQA从67.34降至64.56、PTW从45.95降至38.03；响应触发取得最高F1和NQ-F1，而InternVL3.5-8B多轮召回达98.24但精确率仅23.66，TimeOmni-1则过于保守；同时实现近零流阻塞和最高2.15倍推理加速。

### Q5: 有什么可以进一步探索的点？

当前工作的局限主要在于：交互能力层级仍以理解与自适应为主，尚未覆盖推理、规划、多模态协同等更高阶能力；响应触发机制依赖学习式控制，在概念漂移或分布外流数据上可能误触发或漏触发；解耦推理虽避免阻塞，但控制与生成模块的协同优化仍不充分。未来可探索：一是引入记忆与反思机制，使模型在长流中积累事件因果链，支持跨时段推理；二是将触发决策建模为风险敏感的最优停止问题，结合不确定性估计动态调整沉默/响应阈值；三是扩展到多变量、多模态流（如日志、图结构、文本事件）的联合交互；四是研究在线持续学习与用户反馈闭环，使模型在交互中自适应更新而不遗忘；五是建立更贴近工业场景的评测基准，如故障预警、人机协同诊断等，检验实时交互智能的实际价值。

### Q6: 总结一下论文的主要内容

论文针对现有时间序列语言模型在流式场景下无法实时交互的问题，提出了“时间序列交互”这一新范式：模型持续感知流入的观测与用户意图，自主决定沉默或响应，并在生成回复的同时继续处理新观测。为实现该目标，作者设计了TimeInteract，包含双视角流式编码器、响应触发控制机制以及解耦流式推理机制，使控制与生成分离，避免阻塞后续输入。论文还构建了从理解到自适应的四级交互能力层级，并发布大规模数据集StreamTSI-34K，含34,588个交互片段和77,505条响应。实验表明，TimeInteract在四个交互层级上均优于现有LLM、VLM和TSLM，最高提升23.92分，同时实现近零流停滞和最高2.15倍推理加速。
