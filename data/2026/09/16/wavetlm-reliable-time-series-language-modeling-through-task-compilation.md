---
title: "WaveTLM: Reliable Time-Series Language Modeling through Task Compilation"
authors:
  - "Jiahui Chen"
  - "Bingke Zhu"
  - "Hongyu Pan"
  - "Yingying Chen"
date: "2026-09-16"
arxiv_id: "2609.18812"
arxiv_url: "https://arxiv.org/abs/2609.18812"
pdf_url: "https://arxiv.org/pdf/2609.18812v1"
categories:
  - "cs.LG"
tags:
  - "Time-Series Language Modeling"
  - "Task Compilation"
  - "Reliable Output Generation"
  - "Contract-Grounded Benchmark"
  - "ExecTS-QA"
  - "WaveTLM"
  - "Compiler-Executor Architecture"
  - "Anomaly Detection"
  - "Forecasting"
  - "Imputation"
  - "Classification"
  - "Waveform Analysis"
  - "LLM for Time Series"
  - "Structured Output"
  - "Task-Native Executors"
  - "Reliability"
  - "Hallucination Mitigation"
  - "Industrial Diagnosis"
relevance_score: 8.5
---

# WaveTLM: Reliable Time-Series Language Modeling through Task Compilation

## 原始摘要

Time-series language models provide a shared natural-language interface across temporal tasks, but plausible text does not guarantee reliable task outputs. Responses may appear reasonable while hallucinating the required object: numerical sequences can violate shape, scale, channel order, or temporal alignment, and textual decisions can fall outside the legal label space. We formulate reliable time-series language modeling, separating task-object reliability from predictive quality. We introduce ExecTS-QA, a contract-grounded benchmark spanning forecasting, imputation, classification, anomaly detection, and waveform analysis. We further propose WaveTLM, a unified compiler-executor model whose task compiler transforms user requests, visible arguments, and wave-grounded evidence into typed task states, while task-native executors construct numerical tensors, legal decisions, or structured records. On ExecTS-QA, a single WaveTLM checkpoint achieves 99.40% contract-valid coverage, compared with 37.83% for the strongest evaluated string-first baseline, while retaining balanced predictive performance across all five task families. Evaluations on SciTS, TSQA, IRTS-ToolBench, and ARFBench provide additional evidence of transfer. The code, construction scripts, and ExecTS-QA dataset will be publicly released upon publication. These results show that task compilation can convert plausible language generation into reliable time-series outputs.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决时间序列语言模型（TS-LLM）中“任务对象幻觉”这一可靠性问题。研究背景是，自然语言接口为异构时间序列任务提供了统一访问方式，但生成看似合理的文本并不等于输出可靠的任务结果。现有字符串优先的方法依赖自由形式生成后再解析，容易产生违反形状、尺度、通道顺序或时间对齐的数值序列，或输出超出合法标签空间的文本决策。JSON模式、语法约束解码等表面控制手段虽能提升可解析性，却无法决定预测视野、掩码对齐、逆归一化、通道语义或合法标签等关键约束。核心问题是：这些约束由请求、时序输入和任务协议共同决定，同一观测序列在预测、插补、分类等任务中需要不同的输出对象，而自由解码难以强制和验证这些要求。因此，本文提出将可靠时间序列语言建模形式化为“编译后执行”，通过任务编译器将请求、可见参数和波形证据映射为类型化任务状态，再由任务原生执行器构造数值张量、合法决策或结构化记录，从而把语言生成转化为可靠的任务输出。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是原生时序建模工作，如任务专用架构、时序基础模型和多任务模型，它们直接在固定时序接口下构造数值张量，输出头具备结构保证，但通常假设任务输入已知，而非从自然语言请求中推断所需操作与对象。WaveTLM 保留了原生对象构造能力，但将其置于由请求驱动的任务编译器之后。第二类是面向时序的语言模型，已有工作将预训练语言模型用作时序骨干、表征学习器或预测器，并通过提示或共享问答接口提供预测与理解能力，验证了语义先验与异构任务访问的价值。然而这些协议主要衡量预测误差、答案准确率或响应级质量，未将“完整响应是否实例化评测器要求的原生对象”作为全分母可靠性属性单独考察。WaveTLM 则将这种结构可靠性与任务特定预测效用分离。第三类是时序问答与可靠性评测，TSQA、SciTS、IRTS-ToolBench 和 ARFBench 通过通用问答或推理协议拓展了时序评测。ExecTS-QA 与之互补，重点测试语言面向模型能否在无需评测器修复的情况下生成契约有效的未来张量、掩码对齐值集、合法决策或结构化波形记录。

### Q3: 论文如何解决这个问题？

WaveTLM 将可靠时间序列语言建模重新定义为“任务对象可靠性”问题，即模型不仅要生成看似合理的文本，还必须构造出符合任务契约的合法对象（数值张量、合法决策或结构化记录）。其核心是一个编译器-执行器架构。

整体框架分为三阶段：请求到契约、契约到对象、对象到响应。给定多元序列 X、自然语言请求 q 和可见参数 m，模型首先通过路由器推断任务族 τ̂（预测、插补、分类、异常检测、波形分析五类之一）。每个任务族对应一个确定性契约 C_τ(m)，规定对象类型、形状、对齐方式、尺度、通道顺序、有限值约束以及合法标签域，并注册解析器 π、验证器 ν 和序列化器 σ。

在编译器阶段，语义编码器 f_sem 与 Wave Adapter G_wave 分别产生语言对齐的时序 patch 表示 S 和保留多尺度时域、频域、事件局部及通道信息的原始波形表示 Z_raw，再经元数据嵌入 E_meta 融合。由于不同任务需要同一序列的不同证据，路由条件重采样器通过 CrossAttn 生成任务特定表示 Z̃_τ，最终编译状态 h_τ 包含证据、类型化答案字段 a_τ 和契约 C_τ(m)。

在执行器阶段，连续对象（预测、插补）由数值执行器直接构造张量，避免逐标量自回归生成，并在序列化前反归一化；离散对象（分类、异常检测）限制在注册标签域内；波形分析使用分类、数值和解释字段分离的结构化输出。所有输出都经过原生契约验证、序列化和往返恢复，只有原生对象与恢复对象均满足契约且等价时才视为契约有效。

关键创新在于：将语言生成与对象构造解耦，冻结语言骨干和语义编码器，仅训练 Wave Adapter、重采样器、类型化嵌入、任务执行器和 LoRA 路径；多任务损失联合监督语言生成、答案字段和任务特定目标；推理时不使用任何评估侧信息进行路由纠正、输出修复或标签重映射，从而保证可靠性由编译器-执行器路径自身产生。

### Q4: 论文做了哪些实验？

论文围绕ExecTS-QA基准展开实验，该基准含35,323条训练实例和4,795条评测实例，覆盖预测、插补、分类、异常检测与波形分析五类任务。对比方法包括Qwen3-8B-SFT、Raw ChatTS、ChatTS-SFT，以及作为数值参考的UniTS。核心指标为响应覆盖率RC、候选覆盖率CC、合同有效覆盖率CVC与可靠性产出RY。结果显示，WaveTLM单一检查点取得99.40%的CVC，远高于最强字符串优先基线ChatTS-SFT的37.83%，RY达100%，且对预测515/515、插补261/261、分类868/868、异常检测2592/2592全部构造出合同有效对象。预测效用方面，WaveTLM在分类准确率0.706、波形类别0.713上最优，异常F1为0.847，预测与插补MAE分别为0.337和0.427，优于ChatTS-SFT但略逊于使用原生输入的UniTS。外部评测中，TSQA-50上预测MSE为0.072、分类0.900、异常0.820；IRTS-ToolBench总体63.29；ARFBench总体36.13；SciTS零样本数值成功率100%。消融实验表明，任务原生执行器与任务专用LoRA路径分别提升连续预测与决策任务表现。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于：其一，任务编译器依赖预定义的契约与类型系统，面对开放域、未见任务或模糊用户意图时，能否正确编译尚不明确，跨基准迁移虽有效但仍限于相近任务族。其二，99.40% 的契约有效覆盖率是相对封闭标签空间与固定输出模式的结果，真实工业场景中标签会漂移、通道语义会变化，契约本身可能需要动态演化。其三，论文强调可靠性而弱化预测精度，执行器在长时预测、极端异常等困难样本上的表现仍待检验。

未来可探索：一是让编译器具备契约自省与自动修正能力，从失败案例中归纳新的类型约束；二是引入不确定性量化，在编译失败或证据不足时主动拒答或请求澄清，而非强行输出；三是将波形证据与外部知识、物理约束结合，提升可解释性与跨域泛化；四是把执行器扩展到多模态、多步工具调用与在线学习，验证其在真实工业诊断闭环中的长期可靠性。

### Q6: 总结一下论文的主要内容

论文关注时间序列语言模型的可靠性问题，指出语言生成看似合理并不代表任务输出可靠，模型可能产生“任务对象幻觉”，如数值序列违反形状、尺度、通道顺序或时间对齐，文本决策超出合法标签空间。为此，作者将任务对象可靠性与预测质量分离，提出可靠时间序列语言建模问题，并构建契约驱动的基准ExecTS-QA，覆盖预测、插补、分类、异常检测和波形分析五类任务。方法上提出WaveTLM，一种统一的编译器-执行器模型：任务编译器将用户请求、可见参数和波形证据转化为类型化任务状态，任务原生执行器再构造数值张量、合法决策或结构化记录。实验表明，单个WaveTLM检查点在ExecTS-QA上达到99.40%契约有效覆盖率，而最强字符串优先基线仅为37.83%，同时在五个任务族上保持均衡预测性能，并在SciTS、TSQA、IRTS-ToolBench和ARFBench上展现迁移能力。结论表明，任务编译可将看似合理的语言生成转化为可靠的时间序列输出。
