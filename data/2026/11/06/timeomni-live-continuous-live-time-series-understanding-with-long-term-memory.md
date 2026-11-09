---
title: "TimeOmni-Live: Continuous & Live Time Series Understanding with Long-Term Memory"
authors:
  - "Tong Guan"
  - "Alexander Chemeris"
  - "Yiqing Guo"
  - "Warren Jin"
  - "Zhao Li"
  - "Shirui Pan"
  - "Ming Jin"
date: "2026-11-06"
arxiv_id: "2611.09502"
arxiv_url: "https://arxiv.org/abs/2611.09502"
pdf_url: "https://arxiv.org/pdf/2611.09502v1"
categories:
  - "cs.LG"
tags:
  - "时间序列语言模型"
  - "连续流式理解"
  - "长期记忆"
  - "混合记忆机制"
  - "实时推理"
  - "边缘部署"
  - "时间序列报告生成"
  - "状态保持"
  - "跨窗口推理"
  - "基准数据集"
relevance_score: 8.5
---

# TimeOmni-Live: Continuous & Live Time Series Understanding with Long-Term Memory

## 原始摘要

Existing time series language models predominantly follow an offline, one-shot paradigm: they process fixed-length inputs independently and do not retain past states. This static approach fundamentally misaligns with the continuous nature of real-world streaming applications and fails to maintain the historical context necessary for cross-window reasoning. To bridge this gap, we introduce Continuous & Live Time Series Understanding (CL-TSU), a novel paradigm that shifts the focus toward maintaining a persistent, stateful understanding over open-ended data streams. To systematically evaluate this paradigm, we present LiveTS-Suite, the first comprehensive data suite tailored for CL-TSU, supporting data generation, model training, and systematic evaluation across 18 tasks spanning six core capabilities. It comprises over 5K streams totaling 2.2B timesteps, annotated with 15K specific response events. We further design an evaluation protocol that jointly assesses response timeliness, content accuracy, and computational efficiency. Building on this foundation, we propose TimeOmni-Live, the first live time series understanding model. It integrates a hybrid time series encoding for natively temporal input, a stream-persistent hybrid memory mechanism to effectively preserve exact historical evidence and long-term task states, and an elastic stream-inference synchronization strategy to reduce processing lag. Evaluations show that TimeOmni-Live establishes a strong baseline for CL-TSU, outperforming frontier LLMs (90.0 vs. 79.3 for Opus 5) with only 4B parameters and achieving 206$\times$ lower p95 latency than its backbone. Deployment on a Jetson edge device further shows its ability to support real-time continuous temporal understanding locally at the edge.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决现有时间序列语言模型与真实流式应用场景根本性错配的问题。研究背景在于，时间序列本质上是传感器持续采集的连续模态，但现有研究几乎都采用离线、一次性范式：模型接收固定长度输入窗口，单次调用后即停止，不保留跨窗口的任务状态。这一范式存在两大不足：其一，固定窗口的事后分析无法与测量数据实时到达的应用需求对齐，如毫秒级物联网遥测和分钟级交通调度；其二，它丢弃了窗口边界之外的有价值历史上下文，而洪水风险估计等任务恰恰依赖远距离的历史记录。近年来多模态领域已出现面向连续音视频的持续感知范式，但时间序列智能领域尚缺乏对应的系统化设定与评估。因此，本文提出“连续与实时时间序列理解”（CL-TSU）新范式，核心问题是让模型在开放式数据流上持续运行、随观测与指令动态响应，并保持持久状态以支持跨窗口推理。为此需解决两个关键障碍：一是缺乏专门针对该能力的数据与评估体系，现有实时系统评测只关注时延而忽视历史上下文对后续决策的影响；二是缺乏原生支持连续流处理与长期记忆的统一建模框架，现有基于预定义代码或智能体自动更新代码的方法难以捕捉长期依赖并原生理解时间序列模态。

### Q2: 有哪些相关研究？

本文的相关工作主要分为两类。

**大时间序列模型类**：时间序列基础模型（TSFMs）利用大规模多样语料实现零样本预测与通用分类；时间序列语言模型（TSLMs）及多模态架构将时序数据与LLM对齐以支持理解与复杂推理。但作者指出，这些模型的建模范式本质上仍是“一次性”的。最接近连续场景的ARGOS虽借助LLM智能体生成可执行代码，但其生成过程离线、运行时依赖固定代码，难以在线适应用户，且仅局限于当前时间步附近的局部分析，无法跨顺序输入累积历史证据、不支持跨窗口比较推理。本文则提出CL-TSU范式与TimeOmni-Live模型，实现有状态、持续在线、具备长期记忆的流式时序理解。

**流式多模态模型类**：视觉与音频领域已从静态片段转向持续运行的流式模型，支持在线理解、事件跟踪与主动交互；系统层面如StreamingLLM通过KV缓存淘汰与注意力汇在无限上下文中保持稳定生成。但这些优化侧重以丢弃历史token维持解码效率与低延迟，忽视了保存精确历史证据与长期任务状态的持久记忆机制，且通用多模态模型缺乏对时序波形的原生理解。本文的混合记忆机制与弹性流式推理同步策略正是针对这一空白。

### Q3: 论文如何解决这个问题？

论文提出TimeOmni-Live，首个面向连续实时时间序列理解（CL-TSU）的模型，其核心是“读取—决策—重复”的流式推理循环：每步读入新数据块与既有上下文，决定保持沉默或触发响应，响应生成期间后续数据块被缓冲，随后按序处理。整体框架包含三项关键机制。其一，混合时间序列编码：冻结的时序编码器提取波形特征，经可训练适配器对齐到骨干输入维度，同时并行提供时间戳、最大/最小/均值/标准差等文本统计量，兼顾原生时序模式与精确数值。其二，流持久混合记忆：在上下文前缀中同时保存紧凑的文本任务状态（如事件计数、参考阈值）与选定的历史波形嵌入，保留细粒度形状信息；通过提前分叉KV缓存，记忆分支异步更新状态，主分支继续处理剩余数据块，并以重叠块显式携带未提交上下文，避免流处理停顿。其三，弹性流推理同步：响应生成期间缓冲到达的数据块，利用仅需单token的沉默决策快速清空积压、追赶数据流，降低处理滞后。训练上仅更新时序适配器与LoRA参数，采用沉默降权、记忆前缀扰动和可变重叠长度三种策略，分别缓解沉默偏置、防止记忆错误累积、适配不同硬件。创新点在于将离线单次范式转为有状态开放流理解，并以混合记忆与异步同步实现低延迟连续推理。

### Q4: 论文做了哪些实验？

论文围绕连续实时时间序列理解（CL-TSU）开展了多组实验。主实验在LiveTS-Suite上进行，覆盖18个任务、6项核心能力（瞬时条件、序列条件、事件跟踪、事件引用、在线指令、超长可靠性），并区分分布内（ID）与分布外真实测试集（Real）。对比方法包括专有LLM（Opus 5、Sonnet 5）、开源LLM（DeepSeek-V4.1-Flash、MiniMax-M3、Qwen3.8-27B、Qwen3.5-9B/4B）以及时间序列语言模型（TimeOmni-1、TS-Reasoner），基线采用代码执行与反馈驱动课程设置。结果显示，仅4B参数的TimeOmni-Live在ID上取得90.0分，超过最强代码基线Opus 5（79.3）10.7分；OOD Real测试为56.1，优于DeepSeek-V4.1-Flash（50.9）。消融实验表明，混合编码整体最优，移除文本记忆使C3从95.6骤降至30.5，移除波形记忆使C4从93.8降至65.7。泛化实验中，指令改写仅下降1.0分（89.5→88.5），数值偏移下得61.5分优于DeepSeek的54.3；在KPI数据集上Event-F1 PA为0.200（LLMAD为0.053），适配后达0.539（AnomalyTransformer为0.282）。调度消融验证了弹性同步与提前记忆更新对降低延迟的作用，p95延迟较骨干模型低206倍，并可在Jetson边缘设备本地实时运行。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三：其一，LiveTS-Suite 虽覆盖18任务、2.2B时间步，但以合成或半合成流为主，真实工业、医疗等场景的噪声、缺失与概念漂移尚未充分验证，未来可构建跨域真实流基准并引入漂移检测与在线适应评估。其二，混合记忆机制侧重保留精确历史证据与任务状态，但记忆容量、压缩策略与遗忘机制对超长流（百万级以上窗口）的可扩展性仍待研究，可探索分层记忆、检索式记忆与可学习遗忘门控。其三，弹性流推理同步策略降低了延迟，但未系统讨论多流并发、资源受限下的调度与能效权衡；可结合边缘端动态批处理、模型蒸馏与量化，并引入可解释性模块以追踪跨窗口推理依据。此外，当前仅报告4B模型基线，未来可研究记忆与推理的联合预训练目标及人机交互式在线纠错机制。

### Q6: 总结一下论文的主要内容

论文针对现有时间序列语言模型采用离线、一次性处理范式、无法保留历史状态、难以支撑真实流式应用的问题，提出“连续与实时时间序列理解”（CL-TSU）新范式，要求模型在开放式数据流上保持持久、有状态的理解。为系统评估该范式，作者构建首个面向CL-TSU的数据套件LiveTS-Suite，涵盖数据生成、模型训练与评估，包含超5K条流、22亿时间步和1.5万响应事件标注，覆盖六大能力共18项任务，并设计联合衡量响应及时性、内容准确性与计算效率的评估协议。在此基础上提出首个实时时间序列理解模型TimeOmni-Live，融合原生时间输入的混合编码、保留精确历史证据与长期任务状态的流持久混合记忆机制，以及降低处理滞后的弹性流推理同步策略。实验表明其以仅4B参数超越前沿LLM（90.0对79.3），p95延迟较骨干模型低206倍，并可在Jetson边缘设备本地实时运行，为CL-TSU建立了强基线。
