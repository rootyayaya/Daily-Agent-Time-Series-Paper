---
title: "ReasonCast: Towards Explainable Time Series Forecasting with Reasoning"
authors:
  - "Seunghan Lee"
  - "Jun Seo"
  - "Jaehoon Lee"
  - "Junhyeok Kang"
  - "Sangjun Han"
  - "Sungdong Yoo"
  - "Minjae Kim"
  - "Tae Yoon Lim"
  - "Dongwan Kang"
  - "Hwanil Choi"
  - "Soonyoung Lee"
  - "Wonbin Ahn"
date: "2026-08-03"
arxiv_id: "2608.01875"
arxiv_url: "https://arxiv.org/abs/2608.01875"
pdf_url: "https://arxiv.org/pdf/2608.01875v1"
github_url: "https://github.com/seunghan96/reasoncast"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "time series forecasting"
  - "explainable AI"
  - "LLM"
  - "reasoning chain"
  - "unified model"
  - "benchmark"
  - "causal reasoning"
  - "task fusion"
  - "interpretability"
  - "autoregressive generation"
relevance_score: 9.5
---

# ReasonCast: Towards Explainable Time Series Forecasting with Reasoning

## 原始摘要

Most time series (TS) models are specialized for a single task, either understanding (i.e., returning text answers about a TS) or generation (i.e., returning a numeric forecast). Only recently have unified models begun to handle the two within a single architecture. Even these models, however, produce the two outputs as task-separated paths and cannot predict a series and explain why that prediction arises within a single coherent response. In this paper, we argue for a task-fused model that jointly produces 1) prediction (generation) and 2) selfexplanation (understanding), thereby integrating 1) numerical TS forecasting and 2) interpretable text reasoning within a single response. To enable the systematic study of this capability, we present both a benchmark and a recipe that jointly address the two tasks. The benchmark, ReasonTS-Bench, identifies five fundamental patterns underlying TS and enables the joint evaluation of both tasks. ReasonCast, our recipe for finetuning any LLM to perform both tasks jointly, yields a model that generates a reasoning chain and a forecast together in a single autoregressive pass. Extensive experiments show that ReasonCast outperforms both LLMs and TS models on prediction accuracy while producing verifiable, causal reasoning. Code is available at: https://github.com/seunghan96/reasoncast.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列（TS）模型传统上被专门设计用于单一任务：要么是理解（以文本形式解释序列），要么是生成（输出数值预测）。尽管近期出现了在单一架构内同时处理这两种任务的统一模型，但它们仍将两个输出作为任务分离的路径，无法在单个连贯响应中同时预测序列并解释预测产生的原因。现有方法中，理解与生成是“加法式”组合（U+G），而非“乘法式”融合（U×G），即预测与解释相互独立、缺乏因果关联。这导致可解释时间序列AI的关键需求未被满足：实际应用中，用户往往需要在依据预测采取行动前理解其背后的原理。本文旨在填补这一空白，提出一个统一框架，将数值预测与可解释的文本推理整合为单一自回归过程，使模型首先生成推理链，再基于该推理链生成预测，从而让解释因果性地引导预测，而非事后的辩护。为此，论文同时引入了基准ReasonTS-Bench（基于五种基本时间序列模式，支持预测与解释的联合评估）和训练方案ReasonCast（可微调任意LLM以联合执行两项任务），以系统性地研究这一能力。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类：

**方法类（TS预测模型）**：包括DLinear、PatchTST、TimesNet、iTransformer等传统预测模型，以及Chronos、Moirai、TimesFM、VisionTS、Time-MoE等基础模型。这些模型仅输出数值预测，缺乏文本解释能力。本文的ReasonCast在预测基础上增加了可验证的因果推理链，突破了纯数值输出的局限。

**理解类（TS推理模型）**：ChatTS、Time-MQA、S2TS-LLM、Thoth、PATRA等工作让LLM理解时间序列并回答文本问题，但无法生成数值预测。ReasonCast将理解与生成融合，在单一自回归过程中同时输出预测和解释，而非像这些模型那样仅处理文本。

**统一模型（理解+生成）**：TimeOmni-1、ChatTime、FinSTaR、TimeOmni-VL等虽统一了两种任务，但将预测和解释作为分离的任务路径或条件独立分支，用户需分别选择提示。ReasonCast的关键区别在于任务融合——预测与推理链在同一响应中联合生成，推理直接服务于预测的因果解释。此外，AlphaCast等智能体方法通过多轮工作流编排冻结LLM，而ReasonCast是端到端微调的单模型。

**评测类**：现有TS基准多聚焦单一任务，本文提出的ReasonTS-Bench首次系统评估联合预测与解释能力，覆盖五种基本时间序列模式，填补了该评测空白。

### Q3: 论文如何解决这个问题？

ReasonCast通过一种“路由-推理-预测”的单次自回归生成框架，将时间序列预测与可解释推理统一在同一响应中。其核心设计遵循前向分解：先产生推理链，再基于推理链生成数值预测，确保解释先于并支撑预测结果。

整体流程分为五个步骤：**读取**将时间序列序列化为输入；**路由**选择输出模式，即识别输入遵循的五种基本模式之一（正弦、趋势、自回归、多频、变点），可采用显式路由（首token输出模式类别）或隐式路由（解码器内部选择）；**推理**基于选定模式生成参数估计和规则说明的推理链；**预测**在推理条件下生成数值预测，保持二者互洽；**回退**机制在输入不匹配任何模式时标记为未知，转而外推近期趋势而非强行拟合。

论文提出三种变体：显式路由（默认）、隐式路由和单模式专家（每种模式独立训练作为oracle）。实验表明两种路由变体均优于单模式专家，说明五种基础模式互补，联合学习效果更好。

创新点在于：1）任务融合——将数值预测与文本推理整合为单一连贯响应，而非分离路径；2）ReasonTS-Bench基准——识别五种基础模式并支持联合评估；3）四维评估指标——除传统误差外，还衡量推理保真度（参数估计正确性）、一致性（预测与规则吻合度）和敏感性（对参数变化的因果响应），全面验证了模型的可解释性和因果推理能力。

### Q4: 论文做了哪些实验？

论文构建了ReasonTS-Bench基准，包含五种基本时间序列模式（Sine、Trend、AR、MF、CP），并基于此设计了多组实验。实验设置上，默认使用Qwen2.5-3B-Instruct作为骨干网络进行全量微调，其他骨干网络（Qwen2.5-7B、Llama-3.1-8B、Phi-3.5-mini、Gemma-2-9B）采用全量微调或LoRA，结果取3次随机种子平均。

对比方法包括：平凡预测器、四个专用TS预测模型（DLinear、PatchTST、iTransformer、TimeXer）、统一模型TimeOmni-1，以及四个指令微调LLM骨干（Qwen、Llama、Phi、Gemma），每个LLM均运行少样本和微调两种模式。

主要结果：ReasonCast在所有骨干上显著提升预测精度和推理能力。默认Qwen2.5-3B模型上，MAE从2.223降至0.236，Fidelity从0.252升至0.899，Consistency从0.275升至0.613，Sensitivity从0.138升至0.794。ReasonCast的预测精度甚至超过专用TS模型。消融实验表明，推理先于预测的输出顺序优于相反顺序（误差降低0.070，Fidelity提升55个百分点）。反事实探测显示ReasonCast大幅提升Sensitivity（如Sine从0.270升至0.960）和Stability，证明模型真正因果地读取输入而非记忆。此外，ReasonCast对显式/隐式路由均稳健，联合训练优于五个独立专家模型。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：一是基准测试仅覆盖五种基础时序模式，对复杂真实场景的泛化能力有限；二是推理链的可验证性仍依赖人工判断，缺乏自动化验证机制；三是模型在OOD输入上虽有提升但误差仍偏高，说明推理能力尚未充分泛化。

未来可探索的方向包括：1) 扩展模式库，引入更多非线性、非平稳及多尺度交互模式，提升基准的覆盖度；2) 设计可自动验证推理链正确性的评估指标，如将推理步骤转化为可执行的符号约束或因果图，实现机器可检查的推理；3) 将ReasonCast与检索增强生成结合，使模型能引用外部知识或历史相似案例进行推理；4) 探索推理链的稀疏化与压缩，降低推理开销，同时保持预测精度；5) 引入主动学习机制，让模型在推理不确定时主动请求标注或补充数据，提升对未知模式的适应能力。

### Q6: 总结一下论文的主要内容

本文提出时间序列建模的第四维度——任务融合的理解×生成，即模型在单一自回归输出中同时产生数值预测与可解释的推理链。现有模型虽能统一处理理解与生成任务，但输出路径分离，无法在预测的同时解释原因。为此，作者构建了ReasonTS-Bench基准，基于五种基本时间序列模式，支持逐步可验证的推理链与四项评估指标。方法上，ReasonCast提供一种微调配方，使任意LLM能联合执行预测与自解释，生成连贯的推理和预测结果。实验表明，ReasonCast在预测精度上优于纯LLM与专用TS模型，同时产生可验证的因果推理。该工作填补了可解释时间序列预测的空白，为构建透明、可信的预测系统提供了新范式，但当前基准为单变量合成数据，未来需扩展至多变量与更复杂模式组合。
