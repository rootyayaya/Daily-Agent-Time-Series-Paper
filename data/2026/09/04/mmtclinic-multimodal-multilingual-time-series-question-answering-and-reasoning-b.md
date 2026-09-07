---
title: "MMTClinic: Multimodal, Multilingual Time Series Question Answering and Reasoning Benchmark for Clinical Domain"
authors:
  - "Sourav Malakar"
  - "Harshit Nigam"
  - "Akash Ghosh"
  - "Sriparna Saha"
  - "Amlan Chakrabarti"
  - "Saptarsi Goswami"
  - "Priti Singh"
date: "2026-09-04"
arxiv_id: "2609.04842"
arxiv_url: "https://arxiv.org/abs/2609.04842"
pdf_url: "https://arxiv.org/pdf/2609.04842v1"
categories:
  - "cs.CL"
  - "cs.AI"
tags:
  - "clinical time series"
  - "multimodal QA"
  - "multilingual benchmark"
  - "LLM evaluation"
  - "time series reasoning"
  - "physiological signals"
  - "mortality prediction"
  - "heart rate forecasting"
  - "SOFA score estimation"
  - "chain-of-thought"
relevance_score: 7.5
---

# MMTClinic: Multimodal, Multilingual Time Series Question Answering and Reasoning Benchmark for Clinical Domain

## 原始摘要

Time-series data in clinical settings is crucial for capturing dynamic changes in a patient's health over time, enabling timely diagnosis, personalized treatment, and early detection of critical events. However, the development of clinically reliable and linguistically inclusive medical AI systems remains a significant challenge, primarily due to the lack of multimodal, multilingual, and time-series-grounded benchmarks that reflect the complexity of real-world clinical scenarios. To fill this gap, we present MMTClinic, a benchmark designed to evaluate large language models (LLMs) on complex reasoning and question-answering tasks involving clinical time-series. MMTClinic combines text, medical images, and multivariate physiological signals and includes 30,000 QA pairs (15,000 multiple choice questions (MCQs) and 15,000 open-ended questions) across five languages: English, Hindi, Bengali, Marathi, and Tamil. These questions cover three important clinical tasks---mortality prediction, heart rate forecasting, and SOFA score estimation. We evaluate 13 state-of-the-art LLMs in zero-shot, few-shot, and chain-of-thought settings. Our evaluation reveals notable differences in model performance across tasks, languages, and modalities, highlighting current limitations in clinical reasoning capabilities. MMTClinic provides a valuable resource for advancing multilingual, multimodal, and time-series-aware medical AI research. The dataset will be made publicly available on successful acceptance of the work.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

本文聚焦于临床时间序列推理基准的缺失问题。研究背景是：尽管大语言模型在医疗文本和图文任务中表现优异，但真实ICU场景依赖多模态生理信号（如心率、血压）的动态变化，现有模型难以联合理解数值序列、临床文本和图像。现有基准存在三类不足：一是仅含原始信号的单选题，缺乏临床文本和影像；二是文本+时间序列数据集不含视觉模态且非选择题形式；三是包含文本、信号和影像的综合数据集仅支持开放式问答，且影像局限于静态X光片。更重要的是，所有现有基准均为英文单语，无法评估多语言临床推理能力。因此，本文提出MMTClinic基准，首次将临床文本、医学图像和多变量时间序列统一纳入多选题与开放式推理框架，覆盖英语、印地语、孟加拉语、马拉地语和泰米尔语五种语言，包含3万个问答对，针对ICU死亡率预测、心率趋势预测和SOFA评分估计三项任务，以填补多语言、多模态时间序列临床推理评估的空白。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**：大量工作探索LLM在医疗、教育、法律等领域的通用适配，但多数仅针对文本，如MedExpQA和IndicQA揭示了非英语环境下医学推理的不足；另有研究专门针对印度语言的多模态医学查询分析、多智能体推理及代码混合临床摘要，但均未纳入生理时间序列。**应用类**：多模态临床理解研究（如多模态问题摘要、临床文档摘要、医学检索）整合了文本与静态影像（如X光片），却缺乏对多变量生理信号动态趋势的建模。**评测类**：现有基准如MedQA、MedMCQA主要依赖多选题，难以评估复杂临床推理（如鉴别诊断、治疗规划）。

本文与上述工作的核心区别在于：首次将多变量临床时间序列与文本、影像统一纳入评测，引入开放式问答任务以弥补多选题的局限，并覆盖五种语言，从而同时填补时间序列、多模态和多语言三个空白。相较于仅关注静态图像或纯文本推理的既有研究，MMTClinic强调时序动态推理，为临床AI提供了更贴近真实场景的评测资源。

### Q3: 论文如何解决这个问题？

MMTClinic通过系统化的四步构建流程来解决临床时间序列多模态、多语言推理评估缺失的问题。首先，从PhysioNet 2012挑战数据集中提取ICU患者前48小时的多变量生理信号（42项指标），经过去除缺失率超35%的样本、多项式插值填补和小时级重采样等预处理，同时生成数值型CSV和可视化PNG图像两种模态数据。

其次，采用医学专家设计的few-shot提示策略，利用GPT-4生成15,000道多选题和15,000道开放式推理题，覆盖死亡率预测、心率预测和SOFA评分估计三大临床任务。所有ground-truth答案直接取自原始数据集，确保客观性。随后通过Google Translate将英文QA对翻译为印地语、孟加拉语、马拉地语和泰米尔语，并由母语语言学家进行人工校对。

在质量控制环节，采用双评分机制：7位医学专家从临床相关性（0-5分）评估，10位语言学家从语言质量评分，仅保留双方评分均≥3.5的样本。约70%的样本经4位医学专家独立复核，平均评分达4.2-4.5，验证了临床准确性和推理逻辑性。

该基准的独特之处在于设计了四种多模态评估设置：文本+时间序列（MCQ）、文本+图像+时间序列（MCQ）及其对应的推理版本，系统考察LLM在不同模态组合下的临床推理能力。最终构建了包含30,000个QA对、5种语言、3项临床任务的综合评估资源，为多语言多模态医疗AI研究提供了标准化测试平台。

### Q4: 论文做了哪些实验？

论文构建了MMTClinic基准，包含30,000个QA对（15,000道多选题和15,000道开放式问题），覆盖英语、印地语、孟加拉语、马拉地语和泰米尔语五种语言，涉及死亡率预测、心率预测和SOFA评分估计三项临床任务。实验设置了四种模态组合：文本+时间序列的多选和推理任务，以及文本+时间序列+图像的多选和推理任务。

评估了13个模型，分为纯文本模型（如Mistral 7B、Qwen 2.5 7B、DeepSeek R1-LLaMA 3 8B、LLaMA 3.1 70B、Qwen 3 30B、QWQ 32B、GPT-4.1 nano、Gemini 2 Flash）和多模态模型（如Qwen 2.5 VL 7B/72B、LLaMA 3.2 11B Vision、Gemma 3 27B）。在零样本、少样本和思维链三种设置下评估。

主要结果显示：在文本+时间序列任务中，开源模型表现优异，DeepSeek-R1-LLaMA-8B在推理任务中达71%，Qwen 3-235B达76%；加入图像后性能普遍下降，GPT-4.1-nano在多选任务中表现最佳（约46%），Qwen 2.5-VL-7B在推理任务中略胜GPT-4.1-nano（33% vs 32%）。任务难度上，SOFA估计最难，死亡率预测相对容易。语言方面，英语表现最好，泰米尔语最差，专有模型跨语言稳定性更强。DeepSeek-R1在思维链提示下达到98.36%的最高准确率。

### Q5: 有什么可以进一步探索的点？

MMTClinic在语言覆盖、数据来源、模态丰富度及评估方式上仍存在显著拓展空间。首先，仅涵盖五种印度语言且依赖单一ICU数据集，未来可引入更多低资源语言及多中心、跨机构的生理信号数据，以检验模型的泛化能力与领域偏移鲁棒性。其次，视觉模态局限于折线图，可探索融合X光片、CT等影像与波形图，构建更贴近真实临床的多模态推理场景。评估方面，仅用准确率难以反映模型的可信度与安全性，建议引入校准误差、临床风险指标及专家评分体系；同时，离散答案格式限制了深层推理的度量，未来可设计开放式解释生成任务，结合可解释性分析评估推理链条的合理性。此外，机器翻译可能引入语义偏差，可尝试基于本地语言的专家重写或对比不同翻译策略的影响。最后，当前任务集中于预测与评分，未来可扩展至治疗建议、用药决策等更复杂的临床推理任务，并探索多轮对话式诊断场景，以推动医学AI向实用化、安全化方向发展。

### Q6: 总结一下论文的主要内容

MMTClinic是一个面向临床领域、评估大语言模型在多模态与多语言时间序列推理能力的基准数据集。它整合了文本、医学图像和多变量生理信号，覆盖英语、印地语、孟加拉语、马拉地语和泰米尔语五种语言，包含3万对问答（1.5万道选择题和1.5万道开放题），聚焦死亡预测、心率预测和SOFA评分估计三项临床任务。研究对13个先进LLM在零样本、少样本和思维链场景下进行了评测，发现开源模型在纯时间序列推理上表现良好，而专有模型在复杂多模态任务中更优；但所有模型在视觉-语言推理和区域语言任务上均出现稳定性能下降，反映出多模态整合与跨语言泛化仍存在根本性局限。该基准为推进多语言、多模态且具备时间序列感知能力的医疗AI研究提供了可靠基础，数据集将在论文接收后公开。
