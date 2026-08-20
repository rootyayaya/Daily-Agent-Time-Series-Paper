---
title: "Reducing Technician Search Burden: A Multimodal RAG for Cessna 172 Maintenance Manual"
authors:
  - "Seongjun Ha"
  - "Md Rashedul Islam"
  - "Gaurav Nanda"
  - "Damon Lercel"
date: "2026-08-19"
arxiv_id: "2608.18465"
arxiv_url: "https://arxiv.org/abs/2608.18465"
pdf_url: "https://arxiv.org/pdf/2608.18465v1"
categories:
  - "cs.HC"
  - "cs.ET"
  - "cs.IR"
tags:
  - "Multimodal RAG"
  - "Aircraft Maintenance"
  - "ColPali"
  - "Vision-Language Model"
  - "Technical Manual Retrieval"
  - "Interpretability"
  - "Industrial Documentation"
relevance_score: 8.5
---

# Reducing Technician Search Burden: A Multimodal RAG for Cessna 172 Maintenance Manual

## 原始摘要

Proper use of the aircraft maintenance manual is essential for correct maintenance, providing procedures, diagrams, cautions, and specifications. However, technicians often avoid consulting it because it is difficult to navigate and time-consuming under strict schedules. Retrieval augmented generation (RAG) models have recently been introduced in aircraft maintenance, yet existing models focus solely on textual retrieval. This research therefore targeted the Cessna 172 Maintenance Manual (C172-MM), widely used in general aviation, and developed a multimodal manual retriever (MMR) capable of retrieving multimodal manual pages. Retrieval performance was evaluated using synthetic queries covering procedures, diagrams, caution/safety information, and specifications; the MMR achieved 93.37% recall@5. Beyond retrieval, a multimodal RAG (MRAG) pipeline was examined, in which retrieved pages were input to a vision-language model that generated responses to the synthetic queries, achieving 87.20% semantic similarity to ground-truth answers. Three practical feasibilities were also assessed: inference time, operational cost, and interpretability. Average retrieval time for five pages was 11.93 seconds and response generation took 4.95 seconds, at $0.0091 per query, while interpretability was validated through heatmap visualizations. These results indicate that the MRAG pipeline for the C172-MM can reduce the time technicians spend searching manuals and retrieving multimodal information.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文针对航空维修技术人员在查阅维护手册时面临的搜索负担问题。技术人员通常需要花费20%到40%的工作时间在维护手册中搜索信息，而传统的关键词搜索和基于文本的RAG系统难以有效处理包含大量图表、表格和多模态内容的维护手册。论文以塞斯纳172维护手册（C172-MM）为对象，旨在开发一个多模态手册检索器（MMR）和多模态检索增强生成（MRAG）流水线，使技术人员能够通过自然语言查询直接获取相关的维护手册页面（包括文本、图表和表格）以及直接的回答，从而减少搜索时间，提高维护效率和准确性。

### Q2: 有哪些相关研究？

相关研究分为几个方向：一是关于技术人员不使用维护手册的原因研究，如Hobbs指出技术人员花费大量时间搜索信息，Avers等人发现维护信息分散在多个手册和章节中；二是改进维护手册可用性的研究，包括重新设计工作卡（Patel等人）、引入便携式电脑（Drury等人）、开发交互式手册（Gunes等人）、基于本体的方法（Jo等人）；三是最近基于RAG的航空维护助手研究，如Hou等人、Signé等人和Jo等人开发的RAG模型，Jo报告了98%的搜索时间减少。然而，这些RAG模型都局限于文本检索，忽略了图表和表格等视觉信息。本文与这些工作的区别在于，它采用ColPali模型将整个页面作为图像嵌入，实现了真正的多模态检索，并进一步构建了MRAG流水线，将检索到的页面输入视觉语言模型生成直接回答。

### Q3: 论文如何解决这个问题？

论文提出了一种多模态手册检索器（MMR）和多模态检索增强生成（MRAG）流水线。MMR基于ColQwen2-v1.0架构，该架构采用Qwen 2-VL-2b-instruct作为视觉语言模型骨干，通过ColBERT风格的后期交互机制实现查询token与文档patch的细粒度对齐。整个C172-MM手册的961页PDF被直接作为图像嵌入，避免了传统文本提取和分块处理的复杂性。MRAG流水线将MMR检索到的top-5页面输入GPT-4.1视觉语言模型，生成对技术人员查询的直接回答。为了评估，论文使用Claude Sonnet 4.6生成400个合成查询，覆盖四个主要章节组（飞机通用、机身系统、结构、动力装置）和四种任务导向信息类型（程序、图表、警告/安全、规格），并由领域专家进行质量审查。评估包括检索性能（nDCG@5和recall@k）和MRAG响应质量（BERT F-1语义相似度），以及实际可行性（推理时间、运营成本和可解释性）。

### Q4: 论文做了哪些实验？

论文进行了两个主要评估。第一，MMR检索性能评估：使用400个合成查询，MMR在整个手册上达到83.38%的nDCG@5和93.37%的recall@5。按查询类型分析，规格查询表现最佳（nDCG@5为90.39%，recall@5为100%），图表查询相对较弱（recall@5为84%），但随k值增加提升最大。第二，MRAG流水线评估：使用100个查询样本（每种类型25个），GPT-4.1生成的回答与地面真值相比达到87.20%的平均BERT F-1语义相似度。实际可行性方面，平均检索时间为11.93秒，响应生成时间为4.95秒，每查询成本约0.0091美元。可解释性通过热图可视化验证，展示了查询token与检索页面文本的对齐情况。论文还分析了级联错误案例，当MMR检索失败时，VLM会产生幻觉回答。

### Q5: 有什么可以进一步探索的点？

论文指出了几个局限性和未来方向。首先，ColPali模型的页面级嵌入导致跨页上下文断裂，无法捕捉连续页面中的信息，未来可开发处理页面延续的机制。其次，手册中图表页面缺乏文本描述，导致图表查询检索困难，可考虑重构手册或添加图表标题和描述。第三，MMR可能检索到关键词重叠但内容不相关的页面，需要改进语义理解。此外，当前评估仅使用合成查询，未来应使用真实技术人员查询进行验证。实际部署方面，推理时间（约17秒）和成本（每查询0.009美元）仍需优化，可探索开源VLM替代GPT-4.1。最后，该方法可扩展到其他飞机型号和维护手册，并考虑手册定期修订时的重新嵌入策略。

### Q6: 总结一下论文的主要内容

论文针对航空维护手册搜索负担问题，开发了面向塞斯纳172维护手册的多模态检索器（MMR）和多模态检索增强生成（MRAG）流水线。MMR采用ColQwen2-v1.0架构，将整个手册页面作为图像嵌入，实现了93.37%的recall@5检索性能。MRAG流水线将检索到的页面输入GPT-4.1视觉语言模型，生成的回答与地面真值达到87.20%的语义相似度。论文还评估了实际可行性，包括推理时间（约17秒）、运营成本（每查询0.009美元）和可解释性（热图可视化）。研究结果表明，该MRAG流水线能有效减少技术人员搜索手册的时间，支持多模态信息需求，为航空维护领域提供了实用的智能检索和问答解决方案。
