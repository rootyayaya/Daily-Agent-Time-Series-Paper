---
title: "Tracing the Evidence Behind Zero-Shot Time-Series Forecasting: A Source-First Taxonomy and Audit Framework"
authors:
  - "Delun Kong"
  - "Wanyun Ling"
  - "Chenxi Liu"
  - "Ziyue Li"
date: "2026-09-18"
arxiv_id: "2609.21425"
arxiv_url: "https://arxiv.org/abs/2609.21425"
pdf_url: "https://arxiv.org/pdf/2609.21425v1"
categories:
  - "cs.LG"
tags:
  - "零样本时间序列预测"
  - "证据溯源"
  - "审计框架"
  - "检索增强预测"
  - "LLM先验"
  - "时间序列基础模型"
  - "基准测试"
  - "可解释性"
relevance_score: 6.5
---

# Tracing the Evidence Behind Zero-Shot Time-Series Forecasting: A Source-First Taxonomy and Audit Framework

## 原始摘要

Zero-shot time-series forecasting (TSF) is often described as forecasting without target-specific parameter updates, but that training-status condition does not specify what evidence the system may use. A frozen language model prompted with serialized values, a time-series model pretrained on broad forecasting corpora, and a retrieval-augmented forecaster may all satisfy the no-update condition while drawing on different transferable evidence. This paper argues that zero-shot TSF should therefore be governed as an evidence-access claim. We propose a source-first taxonomy that separates three primary evidence sources---frozen LLM prior reuse, parametric time-series pretraining, and retrieval-augmented external memory---from the architectures that implement them. After the source is identified, four additional audit questions remain: task interface, forecast object and scoring, prediction-time context, and resource budget. The resulting agenda is to make zero-shot leaderboards auditable by reporting evidence boundaries and interface assumptions alongside scores, so that benchmark progress reflects transferable forecasting capability rather than undisclosed changes in context, memory, or budget.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注零样本时间序列预测（zero-shot TSF）评测中的可比性与可信度问题。研究背景是：随着时间序列基础模型兴起，大量系统被冠以“零样本”标签，但该标签通常只说明模型参数未在目标序列上更新，并未说明系统在评测前或预测时可访问哪些证据。现有方法存在明显不足：LLMTime 通过数值序列化调用冻结语言模型先验，Chronos 将可迁移预测结构编码进参数，TimeRAF 则在预测时从外部时间序列记忆中检索，它们都满足“不更新参数”的条件，却依赖完全不同的证据来源。而已有综述多按架构、数据类别或模型家族组织，无法揭示这种证据边界差异，导致排行榜上的分数可能回答的是不同问题。因此，本文的核心问题是：如何将零样本 TSF 重新界定为一种“证据访问声明”，并据此建立可审计的分类与披露框架。具体而言，论文提出以证据来源优先的分类法，区分冻结 LLM 先验复用、参数化时间序列预训练和检索增强外部记忆三类来源，并进一步识别任务接口、预测对象与评分、预测时上下文、资源预算四个审计条件，最终形成最低披露清单和基准治理议程，使零样本排行榜能够报告证据边界与接口假设，从而让评测进展真正反映可迁移的预测能力。

### Q2: 有哪些相关研究？

围绕零样本时间序列预测，本文梳理了三类主要相关研究，并按“证据来源”而非架构进行归类。

第一类是冻结LLM先验复用。LLMTime将数值序列化为数字字符串，把预测转化为下一token续写，依赖预训练语言模型先验；LSTPrompt通过长短期任务分解与提示设计改进零样本适配，但证据来源仍是冻结的语言模型先验，提示只改变任务接口。

第二类是参数化预训练。Lag-Llama、TimesFM、Chronos、MOIRAI、Time-MoE等通过大规模真实或合成时序语料预训练，将可迁移预测结构存入模型权重；TTM、Mamba4Cast、TiRex、Reverso侧重架构或训练设计带来的归纳偏置；ChatTime通过跨模态对齐将时序与文本统一到同一模型，但能力仍在评估前写入参数。

第三类是检索增强外部记忆。TimeRAF用可学习检索器与通道提示融合检索候选；TS-RAG检索语义相似的上下文—未来对并融合未来模式证据；Cross-RAG用查询—检索交叉注意力过滤无关样本。

与这些工作不同，本文不提出新预测模型，而是提出“来源优先”分类与审计框架，强调零样本榜单应披露证据边界、任务接口、预测对象、上下文与资源预算，使评测反映可迁移预测能力而非未披露的上下文、记忆或预算变化。

### Q3: 论文如何解决这个问题？

论文的核心主张是：零样本时间序列预测不应被定义为“无目标参数更新”，而应被治理为一种“证据访问声明”。为此，作者提出了一套“来源优先”的分类法与审计框架。

整体框架分为两层。第一层按可迁移证据的存储或访问位置，将零样本TSF划分为三大来源：冻结LLM先验复用、参数化时间序列预训练、检索增强外部记忆。第二层则说明证据如何进入预测：数值序列化与预测感知提示暴露冻结LLM先验；大规模真实或合成时序预训练将预测结构存入权重；检索增强方法在预测时引入外部样例或模式。分类对象是“报告的预测配置”而非模型家族，次要证据通道单独报告。

在具体分支中，冻结LLM分支以LLMTime为代表，将数值编码为数字串并视为下一token续写；LSTPrompt通过长短时提示改变任务接口，但证据来源仍是冻结先验。参数化分支涵盖Lag-Llama、TimesFM、Chronos、MOIRAI、Time-MoE等，其可迁移预测证据来自预训练参数；归纳偏置导向的TTM、Mamba4Cast、TiRex、Reverso，以及跨模态对齐的ChatTime也归入此类。检索增强分支包括TimeRAF、TS-RAG和Cross-RAG，分别采用可学习检索、检索模式融合和查询—检索交叉注意力，其外部记忆在预测时实质性地改变可用证据。

创新点在于：提出以证据来源而非架构组织方法；识别出四个剩余审计问题——任务接口、预测对象与评分、预测时上下文、资源预算；并主张排行榜应同时报告证据边界与接口假设，使基准进步反映可迁移预测能力，而非未披露的上下文、记忆或预算变化。

### Q4: 论文做了哪些实验？

论文并未开展传统意义上的实证实验，而是以概念分析和配置级审计为主。作者选取三个代表性零样本时间序列预测方法——LLMTime、Chronos和TimeRAF——作为案例，分别对应冻结LLM先验复用、参数化时间序列预训练和检索增强外部记忆三类证据来源，并依据四项审计问题（任务接口、预测对象与评分、预测时上下文、资源预算）对其已报告配置进行对比分析。分析表明，三者虽同属“零样本”标签，但在序列化方式、采样预算、检索库规模与候选数量等维度上差异显著，导致分数不可直接比较。论文还引用GIFT-Eval的基准维度（领域、频率、变量结构、预测长度）说明模型侧披露的不足，并借鉴NLP中关于开发选择与计算预算差异的教训，提出按证据访问划分比较赛道（封闭证据、声明检索、开放证据）及诊断性消融的研究议程。主要“结果”是论证性结论：仅凭准确率无法判断性能提升来自可迁移能力还是接口、上下文、评分对象或资源预算的未披露变化，故排行榜行应被视为条件性证据契约。

### Q5: 有什么可以进一步探索的点？

论文的核心局限在于：它主要提出了审计框架与分类学，却未给出可操作的量化指标或实证验证，例如如何度量“证据边界”的松紧程度、如何为不同证据来源设计公平的评分归一化。未来可探索的方向包括：一是构建证据感知的基准测试，在同一任务上系统消融预训练权重、检索记忆、提示接口和协变量通道，量化各证据源对预测增益的边际贡献；二是研究证据泄漏的自动检测方法，例如通过时间戳审计或反事实检索实验识别隐式外部记忆；三是探索跨证据源的公平比较机制，如按“证据预算”而非仅按参数量对齐模型；四是将该审计逻辑扩展到多模态与在线学习场景，检验证据边界随时间漂移时的鲁棒性。此外，可尝试用因果推断框架形式化“证据—预测”的归因关系，使零样本排行榜从单一分数转向可验证的证据契约。

### Q6: 总结一下论文的主要内容

论文指出，零样本时间序列预测常被简单定义为“不更新目标参数”，但这一定义无法说明系统实际使用了哪些可迁移证据。为此，作者提出“证据访问”视角，并构建以证据来源为先的分类体系，将零样本时间序列预测分为三类：冻结大语言模型先验复用、参数化时间序列预训练，以及检索增强的外部记忆，并将其与具体架构区分开。在识别证据来源后，论文进一步提出四个审计维度：任务接口、预测对象与评分方式、预测时上下文以及资源预算。其核心贡献在于把零样本预测从单纯的排行榜分数转变为可审计的证据声明，要求同时报告证据边界与接口假设。结论认为，只有如此，基准进展才能真实反映可迁移的预测能力，而非未披露的上下文、记忆或预算变化。
