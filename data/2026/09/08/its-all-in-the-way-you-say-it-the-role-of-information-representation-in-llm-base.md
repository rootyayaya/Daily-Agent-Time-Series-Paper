---
title: "It's All in the Way You Say It: The Role of Information Representation in LLM-Based Glycemic-Event Prediction"
authors:
  - "Andrea Apicella"
  - "Pasquale Arpaia"
  - "Matteo Orefice"
  - "Andrea Pollastro"
  - "Roberto Prevete"
date: "2026-09-08"
arxiv_id: "2609.08772"
arxiv_url: "https://arxiv.org/abs/2609.08772"
pdf_url: "https://arxiv.org/pdf/2609.08772v1"
categories:
  - "cs.AI"
tags:
  - "LLM for time series"
  - "physiological time-series prediction"
  - "glycemic-event prediction"
  - "prompt-based inference"
  - "information representation"
  - "zero-shot and few-shot learning"
  - "OhioT1DM dataset"
  - "type 1 diabetes"
  - "clinical decision support"
relevance_score: 7.5
---

# It's All in the Way You Say It: The Role of Information Representation in LLM-Based Glycemic-Event Prediction

## 原始摘要

Large Language Models (LLMs) are increasingly being investigated for physiological time-series prediction, yet their effectiveness may depend not only on the model itself, but also on how physiological information is represented and presented at inference time. This study investigates prompt-based general-purpose LLMs for postprandial hyperglycemia and hypoglycemia prediction in individuals with type 1 diabetes. Using the OhioT1DM dataset, we evaluate multiple open-weight LLMs under zero-shot and few-shot inference across prediction horizons of 30, 60, and 90 minutes. The analysis varies both the textual representation of the available physiological information and the amount of information exposed to the model, ranging from glucose observations alone to derived descriptors and additional contextual variables related to insulin, meals, carbohydrates, and physical activity. Performance is compared with conventional patient-specific supervised models and with Gluco-LLM, a language-model-based architecture explicitly adapted to glucose time-series forecasting. Results show a marked task-dependent behavior. Conventional supervised models achieve the strongest performance for hyperglycemia prediction, whereas the best observed prompt-based LLM configurations improve performance for hypoglycemia across all investigated horizons. The effectiveness of prompt-based inference is also strongly influenced by how physiological information is represented, while providing additional contextual information does not lead to a systematic improvement. Overall, these findings highlight physiological information representation as a central design factor in prompt-based LLM approaches to glycemic-event prediction.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于1型糖尿病（T1D）患者餐后高血糖和低血糖事件的预测问题，旨在系统探究基于提示（prompt）的通用大语言模型（LLM）在该任务中的有效性及其关键影响因素。研究背景在于，尽管LLM已被越来越多地应用于生理时间序列预测，但其性能不仅取决于模型本身，更依赖于生理信息在推理时如何被表征和呈现。现有方法主要分为两类：一是通过任务特定优化将预训练LLM适配于时间序列预测（如Gluco-LLM），二是直接通过提示查询通用LLM并与传统监督学习比较。然而，这些研究均未深入回答一个根本性问题：生理信息应以何种形式（如原始序列、结构化描述符或自然语言叙述）呈现给LLM，以及需要提供多少信息量才能支撑可靠的临床预测。为此，本文利用OhioT1DM数据集，在零样本和少样本条件下，系统比较了不同信息表征策略（Raw、Structured、Narrative）和信息维度（仅CGM衍生描述符或附加胰岛素、膳食等上下文变量）对预测性能的影响，并与传统患者特定监督模型及Gluco-LLM进行对比。核心目标是厘清信息表征与信息量如何影响提示型LLM的血糖事件预测能力，从而为设计更有效的LLM临床预测系统提供实证依据。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，Cui等人提出患者特异性LSTM模型，联合预测餐后高/低血糖事件，本文沿用其事件定义与30分钟预测协议；Gruver等人提出LLMTime，将数值序列文本化实现零样本预测，本文继承其提示范式但聚焦生理信号；Alredaini等人及Lara-Abelenda等人分别通过文本提示微调LLM或采用Time-LLM重编程进行血糖预测，本文与之区别在于不微调模型，仅评估通用LLM在零/少样本下的表现。**架构类**中，Li等人的Gluco-LLM和Mahmoudi等人的DiabLLM均基于Time-LLM/Chronos，通过可训练重编程模块适配CGM数据，本文对比了这类专用架构与纯提示方法的性能差异。**应用与评测类**中，Gao等人的GlyLLM和Healey等人的工作分别面向T2D个性化评估及CGM数据对话分析，Ding等人探讨了临床信息表征对预测的影响，但均未系统研究信息表征方式对T1D餐后事件预测的作用。本文首次专门考察提示中生理信息的文本化形式与类型（如仅血糖值、衍生描述符、情境变量）对LLM预测性能的影响，填补了该空白。

### Q3: 论文如何解决这个问题？

本研究通过系统比较三类方法，揭示了信息表征在基于大语言模型的血糖事件预测中的核心作用。整体框架包含三个并行分支：传统监督学习模型直接处理数值生理输入；Gluco-LLM通过专用时间序列适配管道处理数值数据；而核心的提示词框架则保持通用大语言模型参数完全不变，仅将生理信息转化为文本形式输入。

在提示词框架内，论文设计了两个关键维度。第一是信息表征方式，包括三种策略：Raw直接序列化原始CGM序列；Structured将CGM派生描述符组织为键值对；Narrative则用自然语言描述这些特征。第二是信息量设置，在Structured和Narrative下区分仅含CGM派生特征（如均值、标准差、斜率、目标范围内时间占比等）与额外补充情境变量（如活性胰岛素、活性碳水、基础率、餐次信息、体力活动时长等）两种条件。

该设计的精妙之处在于：由于模型参数固定，任何性能差异都纯粹源于输入信息的表征形式和内容变化。通过控制变量比较——同信息量下对比Structured与Narrative可考察语言形式影响，同表征下对比两种信息量可评估情境信息贡献——实现了对提示词工程各因素的解耦分析。任务采用餐后高/低血糖二元分类与回归两种形式，预测时域为30/60/90分钟，确保三类方法在完全对齐的条件下公平比较。这一框架使研究者能够独立于模型适配，纯粹探究信息表征对提示词推理效果的影响机制。

### Q4: 论文做了哪些实验？

本研究基于OhioT1DM数据集，针对1型糖尿病患者餐后高血糖和低血糖事件预测开展实验。实验设置涵盖30、60、90分钟三个预测时域，采用零样本和少样本推理模式，评估多个开源大语言模型。对比方法包括三类：传统患者特异性监督学习模型、未修改参数的通用的基于提示的LLM、以及专门适配血糖时间序列的Gluco-LLM架构。

在提示框架内，实验系统变化两个维度：一是信息表示方式（Raw直接序列化CGM数据、Structured键值对描述符、Narrative自然语言描述）；二是信息量设置（仅CGM衍生描述符 vs 增加胰岛素、碳水摄入、餐时、体力活动等上下文变量）。预测任务采用直接分类和回归后阈值化两种形式。

主要结果显示任务依赖性显著：传统监督模型在高血糖预测上表现最优，而最优提示配置的LLM在所有预测时域上均提升低血糖预测性能。信息表示方式对提示推理效果影响强烈，但增加上下文信息并未带来系统性改进。该研究强调生理信息表示方式是提示型LLM血糖事件预测的核心设计因素。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三方面：一是仅依赖OhioT1DM单一数据集，样本量和患者异质性有限，结论的泛化性存疑；二是未深入探索LLM推理失败时的错误模式与临床可解释性，例如模型是否依赖虚假相关性；三是prompt设计仍属手工工程，缺乏自适应机制。

未来可从以下方向拓展：其一，引入多中心、跨人群数据，并测试不同CGM设备与采样频率下的鲁棒性；其二，设计动态信息筛选模块，让LLM根据当前血糖趋势自主选择最相关的上下文变量，而非固定输入；其三，探索将LLM的置信度与临床风险阈值结合，构建人机协同的预警框架；其四，借鉴Gluco-LLM的适应策略，发展轻量级提示微调或低秩适配方法，在保持零样本泛化能力的同时提升任务特异性；最后，可尝试将时间序列编码为结构化事件图或符号序列，减少自然语言歧义对数值推理的干扰。

### Q6: 总结一下论文的主要内容

本研究系统探讨了基于提示的大型语言模型（LLM）在1型糖尿病患者餐后高血糖与低血糖事件预测中的表现，重点关注生理信息表征方式对推理效果的影响。利用OhioT1DM数据集，作者在30、60、90分钟预测窗口下，对多种开源LLM进行零样本与少样本测试，比较了原始序列、结构化键值对和自然语言叙述三种信息表征，以及仅含血糖衍生特征或额外加入胰岛素、膳食等上下文变量的信息量设置。结果显示，任务依赖性显著：传统监督模型在高血糖预测上最优，而提示型LLM在低血糖预测上全面超越基线；信息表征方式对性能影响显著，但增加上下文信息并无系统性增益。相比专门适配的Gluco-LLM，通用LLM虽在部分场景具备竞争力，但整体仍有差距。该研究强调，生理信息的文本表征是设计基于提示的血糖事件预测系统的核心因素，为构建更可及、可解释的LLM医疗决策工具提供了实证依据。
