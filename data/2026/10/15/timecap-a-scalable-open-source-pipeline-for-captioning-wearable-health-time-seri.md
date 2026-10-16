---
title: "TimeCap: A Scalable Open-Source Pipeline for Captioning Wearable Health Time-Series Data"
authors:
  - "Max Rosenblattl"
  - "Milana Gurbanova"
  - "Karl Aurel Deck"
  - "Narayan Schuetz"
  - "Thomas Kaar"
  - "Manuel Milling"
  - "Nicolas Zumarraga"
  - "Ning Wang"
  - "Kelly W. Zhang"
  - "Anders Johnson"
  - "Robert Jakob"
  - "Björn W. Schuller"
  - "Elgar Fleisch"
  - "Daniel Seung Kim"
  - "Allan Lawrie"
  - "Patrick Langer"
  - "Maxwell A. Xu"
  - "Euan Ashley"
  - "Paul Schmiedmayer"
date: "2026-10-15"
arxiv_id: "2610.21274"
arxiv_url: "https://arxiv.org/abs/2610.21274"
pdf_url: "https://arxiv.org/pdf/2610.21274v1"
github_url: "https://github.com/SchmiedmayerLab/TimeCAP"
categories:
  - "cs.LG"
  - "cs.CL"
tags:
  - "时间序列描述生成"
  - "可穿戴健康数据"
  - "TSLM"
  - "确定性标注流水线"
  - "多模态时序"
  - "数据集构建"
  - "Agentic Time Series"
relevance_score: 8.5
---

# TimeCap: A Scalable Open-Source Pipeline for Captioning Wearable Health Time-Series Data

## 原始摘要

Time-series data generated continuously across industrial, environmental, and especially health domains produce multimodal signals whose scale and heterogeneity make their processing and interpretation particularly challenging. Time-Series Language Models (TSLMs) promise scalable interpretation of these signals, yet remain bottlenecked by a fundamental lack of text-annotated time series pairs that are signal-grounded, reproducible, and extensible across modalities and schemas. Existing paired corpora are either closed or limited in scale and modality coverage. Annotation with large language models could scale them up, but its outputs cannot be regenerated exactly, which prevents others from re-deriving, extending, or auditing the resulting corpus. To address this, we release TimeCap, an open deterministic captioning pipeline with three reusable extractor tiers and a cross-channel synthesis layer that operates directly on the signal with no language model in the loop, extensible to new schemas by writing channel definitions alone. This positions TimeCap as a reproducible mechanism for future dataset generation rather than a one-off release. Applying TimeCap to OpenMHC, the MyHeart Counts wearable dataset, yields MHCap, the largest open caption layer for multimodal wearable time-series data. MHCap spans 19 Apple HealthKit channels and 7,005,763 captions over 908,944 person-days. To showcase the impact of the corpus, we train OpenTSLM, a time-series language model, on MHCap and benchmark on health-outcome prediction. Caption-augmented training (OpenTSLM-Cap) outperforms a label-only baseline on 29 of 32 per-user binary evaluations across 8 tasks.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文针对时间序列语言模型（TSLM）训练中一个核心瓶颈：缺乏大规模、信号接地（signal-grounded）、可复现且可扩展的文本-时间序列配对语料。现有配对语料要么闭源，要么规模有限、模态覆盖窄。使用大语言模型进行标注虽然可以扩大规模，但其输出无法精确复现，导致他人无法重新推导、扩展或审计生成的语料库。这一可复现性缺陷严重阻碍了TSLM在工业、环境和健康等领域的可扩展解释能力。论文旨在提供一个开放、确定性的标注流水线TimeCap，能够直接从原始信号生成文本描述，无需LLM参与，从而支持未来数据集的可持续生成，并以此构建大规模可穿戴健康时序描述语料MHCap，验证其对TSLM训练的增益。

### Q2: 有哪些相关研究？

相关工作主要涉及时间序列语言模型（TSLM）、可穿戴健康数据分析以及多模态数据集构建。TSLM方面，已有研究尝试将时间序列与语言模型结合，用于预测、分类和描述生成，但受限于配对数据稀缺。可穿戴健康领域，WESAD等数据集提供了多模态生理信号，但缺乏大规模文本标注。OpenMHC是My Heart Counts可穿戴数据集的开放版本，包含丰富的Apple HealthKit通道，但未提供文本描述。此外，视觉-语言模型（VLM）的成功启发了时序-语言模型的发展，但时序数据的连续性和异构性带来额外挑战。本文与这些工作的关系在于：它不提出新的TSLM架构，而是通过提供可复现的标注流水线和最大规模的开源描述语料，为TSLM研究奠定数据基础，并展示描述增强训练对健康结果预测的改进。

### Q3: 论文如何解决这个问题？

TimeCap是一个开放、确定性的标注流水线，包含三个可复用的提取器层级和一个跨通道合成层，直接作用于信号，不引入语言模型。三个提取器层级分别为：统计层（提取均值、方差、趋势等数值特征）、结构层（识别峰值、周期、片段等形态特征）和语义层（基于领域知识将特征映射为自然语言描述，如“心率在夜间显著下降”）。跨通道合成层将多个通道的描述整合为连贯的日级报告。流水线通过通道定义文件扩展新模态，只需编写通道定义即可支持新schema。作者将TimeCap应用于OpenMHC数据集，生成MHCap语料，覆盖19个Apple HealthKit通道、908,944人日、7,005,763条描述。然后，使用MHCap训练OpenTSLM（一个时间序列语言模型），在8个健康结果预测任务上进行评估。描述增强训练（OpenTSLM-Cap）在32个每用户二分类评估中的29个上优于仅标签基线。

### Q4: 论文做了哪些实验？

实验主要围绕MHCap语料对TSLM训练的增益展开。作者使用OpenMHC数据集，包含19个Apple HealthKit通道，生成MHCap描述语料。然后训练OpenTSLM模型，对比两种设置：仅使用标签的基线（OpenTSLM-Label）和使用描述增强的模型（OpenTSLM-Cap）。评估在8个健康结果预测任务上进行，包括心血管、代谢、睡眠等领域的二分类任务。每个任务进行每用户二分类评估，共32个评估。结果显示，OpenTSLM-Cap在29/32个评估中优于基线，表明描述增强训练能有效提升模型性能。此外，论文还展示了TimeCap流水线的可扩展性，通过编写通道定义即可支持新模态，并提供了开源代码和数据集。

### Q5: 有什么可以进一步探索的点？

论文的局限性包括：TimeCap目前仅应用于可穿戴健康数据，尚未在工业故障诊断等其他时序领域验证；描述生成基于规则，可能无法覆盖所有复杂模式；MHCap语料虽大，但仅来自单一数据集（OpenMHC），泛化性有待验证。未来方向包括：将TimeCap扩展到工业传感器、环境监测等更多模态；结合LLM进行描述后处理或质量校验，同时保持可复现性；探索描述粒度对TSLM性能的影响；研究如何将描述语料用于少样本或零样本场景；以及开发基于描述的可追溯决策报告系统，支持故障诊断和预测性维护。此外，可以研究描述增强训练对模型可解释性的提升。

### Q6: 总结一下论文的主要内容

本文提出TimeCap，一个开放、确定性的时间序列描述生成流水线，旨在解决TSLM训练中缺乏可复现、可扩展的文本-时序配对语料的问题。TimeCap包含统计、结构和语义三个提取器层级及跨通道合成层，直接处理信号，无需LLM，支持通过通道定义扩展新模态。作者将其应用于OpenMHC可穿戴健康数据集，生成MHCap语料，包含19个通道、908,944人日、7,005,763条描述，是最大的开放多模态可穿戴时序描述层。使用MHCap训练OpenTSLM，在8个健康结果预测任务的32个每用户二分类评估中，描述增强训练在29个上优于仅标签基线。该工作为Agentic Time Series和可解释时序分析提供了可复用的数据生成机制，推动了TSLM在健康等领域的应用。
