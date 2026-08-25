---
title: "Semantics or Structure? Auditing Text Sensitivity in Multimodal Time-Series Forecasting"
authors:
  - "Karthik Sridhar"
  - "Atharva Gupta"
  - "Nishant Pradhan"
  - "Murari Mandal"
  - "Dhruv Kumar"
  - "Saurabh Deshpande"
date: "2026-08-23"
arxiv_id: "2608.22321"
arxiv_url: "https://arxiv.org/abs/2608.22321"
pdf_url: "https://arxiv.org/pdf/2608.22321v1"
categories:
  - "cs.CL"
tags:
  - "多模态时间序列预测"
  - "文本敏感性审计"
  - "扰动分析"
  - "可解释性"
  - "多模态基础模型"
  - "Time-MMD基准"
  - "诊断工具包"
relevance_score: 7.5
---

# Semantics or Structure? Auditing Text Sensitivity in Multimodal Time-Series Forecasting

## 原始摘要

Multimodal time-series forecasting has emerged as a promising paradigm in which natural-language context is expected to improve predictive performance. Recent multimodal foundation models, including Aurora, as well as early- and late-fusion approaches such as MM-TSFlib and TaTS, report substantial gains over unimodal baselines on the Time-MMD benchmark, attributing these improvements to textual information. However, whether these models are actually sensitive to the semantic content of the text remains unverified. We address this question through controlled text perturbations, attribution analyses, and probes of Aurora's text pathway. On Time-MMD, swapping each row's text for any other real text (empty, constant, within-domain shuffled, or cross-domain) moves mean MSE by less than $0.5\%$ on all three architectures. The improvement reported in the literature is recovered when a co-shipped numeric column is removed without touching text. We conclude that, on this benchmark and within this family of frozen-encoder architectures, text content is not the operative signal behind the reported gains. To support future work on text integration in multimodal foundation models for structured data, we release our perturbation protocol and evaluation harness as a reusable diagnostic toolkit.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

本研究聚焦多模态时间序列预测中一个关键但被忽视的问题：模型是否真正理解文本语义，还是仅依赖与文本共享融合路径的其他输入信号。研究背景是，流行病学、能源、金融等领域常将数值序列与时间对齐的文本结合，近期Aurora、MM-TSFlib和TaTS等模型在Time-MMD基准上报告了显著优于单模态基线的性能，并将提升归因于文本信息。现有评估方法仅对比多模态与禁用文本分支的单模态基线，只能证明文本通路贡献了信号，无法区分模型是响应文本内容还是固定、内容无关的输出。本文通过受控文本扰动（空字符串、常量占位符、域内打乱、跨域文本）和未来真值模板的oracle条件，系统检验内容敏感性。核心发现是三种架构对任何文本替换的MSE变化均小于0.5%，且文献中的性能提升在移除数据集附带的一个数值列后消失，证明提升源于该数值列而非文本语义。本文要解决的核心问题是：在多模态时间序列基准上，报告的多模态增益是否真正由文本内容驱动，还是由其他混淆因素造成，并为此提供可复用的诊断工具。

### Q2: 有哪些相关研究？

围绕“多模态时间序列预测中文本敏感性”这一主题，相关研究主要分为以下几类：

**方法类**：早期融合（如TaTS，将GPT-2编码的文本与数值历史拼接）、晚期融合（如MM-TSFlib，通过BERT编码后以残差方式注入）以及预训练基础模型（如Aurora，采用可学习查询令牌和交叉注意力机制）。这些工作均声称文本信息能显著提升预测性能，但本文通过受控扰动实验发现，其性能提升主要源于共存的数值列而非文本语义。

**评测类**：Time-MMD基准涵盖农业、气候等九大领域，提供数值序列与时间对齐的文本，是评估多模态时间序列预测的标准测试平台。本文在该基准上系统审计了三种架构的文本通路，发现文本内容置换对均方误差影响不足0.5%，质疑了先前文献中“文本增益”的真实来源。

**诊断工具类**：本文提出的扰动协议和评估框架可复用于未来研究，用于检测模型是否真正利用文本语义，而非偶然的数值相关性。

与现有工作相比，本文的独特贡献在于：不追求新的预测架构，而是通过严谨的归因分析和文本扰动实验，揭示当前多模态时间序列模型对文本语义的“虚假敏感性”，为领域提供了可复现的审计方法论。

### Q3: 论文如何解决这个问题？

论文通过设计系统的文本扰动协议和归因分析，揭示了多模态时间序列预测模型对文本语义内容不敏感的核心问题。整体框架包含三个关键模块：

**扰动协议模块**：构建六种文本条件（原始、空文本、固定占位符、同域打乱、跨域替换、Oracle数值文本），在保持数值输入完全一致的前提下，逐一替换文本列。通过配对相对变化量Δi（基于MSE）和95%自助置信区间（10,000次重采样），在9个领域、4个预测时域、3个随机种子和8种骨干网络上进行严格统计检验。

**归因分析模块**：对Aurora模型的文本编码路径进行探针分析，追踪文本token在模型内部的表征变化，验证编码器是否真正利用文本语义信息。

**消融实验模块**：关键创新在于发现文献中报告的性能提升源于数据集中附带的一个数值列被移除，而非文本内容本身。当保留该数值列时，所有文本扰动条件下的MSE变化均小于0.5%，证明文本语义对预测结果无实质影响。

技术核心在于严谨的对照实验设计：通过控制变量法隔离文本因素，使用跨域文本破坏主题相关性，用同域打乱破坏时间对齐，从而区分文本存在性、内容、对齐和主题四个维度的影响。最终结论指出，在冻结编码器架构下，文本通道实际处于“语义盲区”，模型主要依赖数值特征进行预测。该研究还开源了可复用的诊断工具包，为后续多模态时间序列研究提供了验证基准。

### Q4: 论文做了哪些实验？

论文在Time-MMD基准上对三种多模态时间序列预测架构（Aurora、MM-TSFlib、TaTS）进行了系统性文本敏感性审计实验。实验设置包括9个领域、4个预测视界、3个随机种子，对训练方法使用8种骨干网络。核心实验是五种文本扰动：空文本、常量文本、域内打乱、跨域替换和Oracle（未来真实值文本），同时设置无文本单模态基线作为对照。

主要结果以均方误差（MSE）和相对变化率（Δ%）呈现。关键发现是：所有文本扰动对三种模型的影响均小于0.5%，其中TaTS变化不超过±0.001%，Aurora不超过±0.05%，MM-TSFlib最大仅+0.16%。相比之下，移除文本路径的单模态基线导致MM-TSFlib误差增加1.87%、TaTS增加7.54%，证实多模态提升真实存在，但并非源于文本语义内容。跨骨干网络分析显示，文本扰动影响始终一致（TaTS±0.01%，MM-TSFlib±2.4%），而结构列效应则随骨干变化显著（TaTS从+1.2%到+15.0%）。实验表明文献报告的提升主要来自伴随的数值列而非文本内容。

### Q5: 有什么可以进一步探索的点？

本文的审计聚焦于Time-MMD基准和三类冻结编码器架构，结论虽有力，但存在明显边界：端到端训练的编码器未被覆盖，其文本通路可能通过梯度更新真正习得语义表征，因此未来首要方向是扩展至可训练模型，验证文本敏感性是否随训练动态涌现。其次，当前文本扰动多为同域或跨域替换，语义多样性不足，构建每行信息量更高、语义区分度更强的语料库，才能为编码器提供“可读”的信号。第三，论文提出的方向性预言（如“即将急剧上升”）比数值预言更贴近语义本质，但受子词分词瓶颈限制，未来可引入更细粒度的数值-文本对齐机制或连续向量提示，绕过分词损失。此外，审计协议可推广至其他多模态基准（如医疗或金融时序），并探索文本通路与数值列共路由的因果解耦方法，例如通过对抗训练或互信息最小化强制文本编码器独立于数值先验。最后，将诊断工具整合进模型选择流程，作为标准测试项，能有效防止“伪文本增益”误导后续研究。

### Q6: 总结一下论文的主要内容

本文针对多模态时间序列预测中文本语义贡献的未验证问题展开研究。现有模型（如Aurora、MM-TSFlib、TaTS）在Time-MMD基准上报告了文本带来的性能提升，但作者质疑这些提升是否真正源于文本内容。通过设计五类文本扰动实验（空文本、常量、域内打乱、跨域替换及未来真值模板），在保持数值输入不变的情况下，发现所有模型的MSE变化均小于0.5%，表明模型对文本语义完全不敏感。进一步分析揭示，文献中报告的提升实际来自数据集附带的一个数值列，而非文本内容。该研究首次系统审计了多模态时间序列模型的内容敏感性，提供了可复用的扰动协议和评估工具包，对推动文本集成方法的可靠评估具有重要意义。
