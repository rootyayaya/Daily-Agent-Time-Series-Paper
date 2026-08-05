---
title: "TimeRLM: Recursive Language Models Enable Precise Anomaly Localization in Long-Context Time-Series"
authors:
  - "Nicolas Zumarraga"
  - "Lorenzo Steno"
  - "Ning Wang"
  - "Max Rosenblattl"
  - "Thomas Kaar"
  - "Maxwell A. Xu"
  - "Kevin O'Sullivan"
  - "Markus Kreft"
  - "Elgar Fleisch"
  - "Paul Schmiedmayer"
  - "Patrick Langer"
  - "Robert Jakob"
date: "2026-08-04"
arxiv_id: "2608.03391"
arxiv_url: "https://arxiv.org/abs/2608.03391"
pdf_url: "https://arxiv.org/pdf/2608.03391v1"
github_url: "https://github.com/OpenTSLM/TimeRLM"
categories:
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "Recursive Language Models"
  - "Anomaly Localization"
  - "Long-Context Time Series"
  - "Time-Series Language Models"
  - "Reinforcement Learning"
  - "Synthetic Benchmark"
  - "ECG"
  - "Sleep Monitoring"
  - "Software Observability"
relevance_score: 9.5
---

# TimeRLM: Recursive Language Models Enable Precise Anomaly Localization in Long-Context Time-Series

## 原始摘要

Precise anomaly localization over long-context time series is a crucial task in monitoring applications across clinical care, industrial operations, financial services, and logistics, where brief evidence may hide inside long spans of high-frequency data. Time-Series Language Models (TSLMs) are able to ingest time series data and verbalize findings on anomalies in natural language; however, recent benchmarks report a decrease in retrieval performance at long contexts, mirroring failure modes in text, vision, and audio. In the text domain, Recursive Language Models (RLMs) can recover much of this lost performance by keeping context external to the large language model (LLM), allowing the model to query it through code. We present TimeRLM, an RLM formulation for time-series that sequentially manipulates the signal using code and vision capabilities. We further introduce AnomalyXL, a synthetic long-context anomaly localization benchmark with programmatically injected anomalies that require precise retrieval. We implement five different task categories and two variants: AnomalyXL-MCQ and AnomalyXL-Localize. TimeRLM outperforms every evaluated TSLM and single-pass baseline on four of the five AnomalyXL-Localize tasks, reaching 0.682 IoU on localization and 0.745 on classify-with-evidence, versus at most 0.329 and 0.072 across all baselines. We post-train TimeRLM using reinforcement learning. The resulting model further improves performance and requires approximately one-third as many agent interaction turns as its untrained base model to produce a final answer. On unseen real-world ECG, sleep and software observability recordings, the post-trained TimeRLM retains or improves performance, surpassing TSLMs despite being trained exclusively on synthetic data. Our findings suggest recursive interaction with time-series is an effective approach for long-horizon retrieval.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

长上下文时间序列中的精确异常定位是临床监护、工业运维、金融和物流等监测应用中的关键任务，但现有方法面临显著挑战。尽管时间序列语言模型（TSLM）能原生处理时序数据并以自然语言描述异常，近期基准测试表明其在长上下文场景下的检索性能急剧下降，与文本、视觉和音频领域的失败模式一致。现有TSLM均采用单次前向传播方式，将整个序列一次性编码进上下文，导致细粒度事件被淹没在冗长信号中。同时，已有长时序问答基准要么局限于短上下文分类，要么将定位任务简化为多选题，回避了真实场景所需的精确时间检索。虽然文本领域的递归语言模型（RLM）通过将上下文外置、用代码查询的方式恢复了长上下文性能，但时间序列领域尚缺乏一种通用的、无需训练的、可直接访问原始信号的递归交互方案。为此，本文提出TimeRLM，将时间序列作为外部变量，通过沙盒Python环境多轮查询和操作信号，结合代码与视觉能力进行推理，并引入AnomalyXL基准以精确评估长上下文异常定位能力，核心目标是解决单次TSLM在长序列上精确检索能力崩溃的问题。

### Q2: 有哪些相关研究？

在时间序列异常定位领域，相关研究主要分为三类。**方法类**：Time-Series Language Models（TSLMs）如ITFormer、OpenTSLM-Flamingo采用固定潜在压缩或全分辨率适配器处理长序列，但存在压缩比增大或二次计算开销问题；另有工作结合冻结时间序列基础模型与渲染图表的VLM进行推理。本文的TimeRLM通过递归语言模型（RLM）将上下文外部化，用代码查询信号，避免了直接长上下文输入的性能衰减。**应用类**：传统异常检测聚焦滑动窗口评分，近期LLM范式用自然语言解释异常段，但评测多在短、预分割数据上。本文提出AnomalyXL长上下文基准，含MCQ和定位两种变体，更贴近实际监测需求。**评测与Agent类**：TimeSeriesScientist、ARTS等用代码编排专用工具，ARTIST用强化学习学习段选择，但均未针对长上下文递归检索。TimeRLM的独特之处在于递归操作信号、结合代码与视觉能力，并通过强化学习后训练提升效率，在合成及真实数据上超越现有TSLM基线。

### Q3: 论文如何解决这个问题？

TimeRLM通过将时间序列异常定位形式化为一个有限时域的序列决策过程，使语言模型能够递归地与信号交互。其核心设计是：将完整的多变量时间序列以JSON格式预置于代码沙箱（REPL）中，模型在每轮交互中可执行Python代码（调用标准数据科学库）或视觉渲染库将信号绘制成图像，从而直接操作未压缩的原始数据，避免长上下文中的信息丢失。模型还可递归调用自身实例（子RLM）处理整个或部分序列，实现分层推理。

整体框架包含三个关键模块：**策略模型**（根LLM）负责生成动作，动作空间由代码执行和终止回答（FINAL）组成；**环境**提供代码执行结果作为观测，并累积交互历史；**奖励函数**基于任务特定的连续指标（如IoU、事件匹配F1）提供可验证的反馈。针对AnomalyXL基准的五类任务（单通道定位、分类、幅度估计、全通道检测、超前滞后分析），模型输出结构化JSON摘要，并通过时间重叠计算和集合匹配进行评分。

创新点在于：1）将RLM范式引入时间序列领域，通过代码查询外部化上下文，突破TSLM在长序列上的检索瓶颈；2）提出AnomalyXL合成基准，包含程序化注入的异常和两种回答格式（MCQ与Localize）；3）采用强化学习后训练，使模型在保持性能的同时将交互轮次减少约三分之二，并在真实ECG、睡眠和软件可观测性数据上展现泛化能力。

### Q4: 论文做了哪些实验？

论文围绕TimeRLM框架开展了系统性实验，涵盖合成基准、真实世界数据和强化学习优化三部分。实验设置上，在AnomalyXL基准（含MCQ和Localize两种任务变体，共5类任务）上，对比了单次LLM（文本/图像）、三种TSLM（ChatTS、OpenTSLM、ITFormer，均基于Qwen3.5-4B）及Toto-1.0-QA-Experimental（32B）等基线，并加入无语言模型的经典特征+梯度提升树基线。主要结果：在AnomalyXL-Localize上，TimeRLM（GPT-5.5图像变体）定位IoU达0.682，分类带证据达0.745，远超最佳基线（分别为0.329和0.072）；在MCQ任务上，TimeRLM在识别和指标任务上领先（0.976和0.921）。强化学习实验中，采用GRPO对Qwen3.5-4B后训练，定位IoU从0.205提升至0.538，且交互轮次减少约三分之二。真实世界零样本测试中，在LTAF心电图和睡眠PSG数据上，TimeRLM保持或超越TSLM性能，尽管仅用合成数据训练。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是AnomalyXL为合成数据，虽然验证了跨域泛化，但真实场景中的噪声模式、多源干扰和标签稀疏性可能削弱其效果；二是当前RLM依赖代码查询和视觉渲染，对高维多变量信号的交互效率仍有提升空间；三是RLM在标量测量任务上增益有限，说明递归交互更适合离散定位而非连续数值估计。

未来可探索的方向包括：将RLM与显式状态空间模型或扩散先验结合，增强对非平稳信号的鲁棒性；引入自适应查询策略，根据信号复杂度动态决定递归深度和子代理数量，减少计算开销；设计更细粒度的奖励函数，在强化学习中融合定位精度与证据可信度，缓解合成到真实的分布偏移；此外，可探索将RLM的代码交互能力扩展到多模态传感器融合场景，并开发可解释的中间查询轨迹，帮助用户理解模型定位依据。

### Q6: 总结一下论文的主要内容

TimeRLM提出了一种递归语言模型框架，用于长上下文时间序列中的精确异常定位。该问题在临床、工业和金融监控中至关重要，但现有TSLM在长序列检索上性能下降。TimeRLM通过代码和视觉能力顺序操作信号，将上下文外部化，使模型能多次查询信号。作者引入AnomalyXL基准，包含五种任务和MCQ/Localize两种变体，并采用强化学习后训练。结果显示，TimeRLM在Localize任务上显著优于所有基线，IoU达0.682，而基线最高仅0.329；后训练模型减少三分之一的交互轮次，且在未见过的真实ECG、睡眠和软件观测数据上保持或提升性能。研究表明，递归交互是长时域检索的有效方法，但MCQ格式会高估模型能力，精确定位需依赖递归查询和子代理机制。
