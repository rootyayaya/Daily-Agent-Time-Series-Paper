---
title: "RAG-TRACE: Tracing Measurement Evidence and Diagnostic Completeness in AI-Generated ECG Reports"
authors:
  - "Elyas Irankhah"
  - "Shahed Salehzehi"
  - "Parisa Hosseini"
date: "2026-11-01"
arxiv_id: "2611.01409"
arxiv_url: "https://arxiv.org/abs/2611.01409"
pdf_url: "https://arxiv.org/pdf/2611.01409v1"
github_url: "https://github.com/Elyasirankhah/RAG-TRACE"
categories:
  - "cs.CL"
tags:
  - "RAG"
  - "ECG报告生成"
  - "证据可追溯性"
  - "测量验证"
  - "临床诊断完整性"
  - "LLM评估"
relevance_score: 8.5
---

# RAG-TRACE: Tracing Measurement Evidence and Diagnostic Completeness in AI-Generated ECG Reports

## 原始摘要

Purpose: Retrieval-augmented generation (RAG) can introduce electrocardiogram (ECG) criteria that lack patient-specific measurement support. This study evaluates the reliability of retrieved diagnostic criteria in AI-generated ECG reports. Methods: We analyzed 1,083 human-validated PTB-XL patient records using a library of 47 criteria cards, including 33 without numeric verification rules. Language models generated structured reports with and without retrieval. Criterion applicability was evaluated using Marquette 12SL measurements, with independent assessment using Uni-G and comparison against expert-validated diagnostic labels. Results: Keyword retrieval introduced untestable or measurement-disconfirmed criteria in 46.8% of GPT-4.1-mini reports. A deterministic verification rule withdrew 647 criterion applications, including 639 without numeric checks, while preserving 268 of 269 applications independently supported by Uni-G. Restricting retrieval to 14 testable criteria reduced the initial unsupported-criterion rate to 13.8%. Under matched instructions and an identical output schema, retrieval increased unsupported-criterion reports from 17.4% to 31.1%, while hypertrophy recall remained unchanged at 62.6%. Conclusion: These findings identify a fundamental limitation of retrieval-based clinical report generation: retrieved criteria do not necessarily provide valid patient-specific evidence. Measurement-based verification can reduce unsupported criterion applications, but diagnostic validity requires independent assessment.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文聚焦于检索增强生成（RAG）在临床报告生成中的可靠性问题，特别是AI生成心电图（ECG）报告时，检索到的诊断标准可能缺乏患者特异性测量证据的支持。具体而言，RAG可能引入无法通过患者实际测量数据验证的标准，导致报告包含不支持的诊断声明。研究旨在评估检索到的诊断标准在AI生成ECG报告中的可靠性，并探索通过确定性验证规则来减少无支持标准应用的方法，同时强调诊断有效性需要独立评估。

### Q2: 有哪些相关研究？

相关研究涉及RAG在医疗领域的应用、ECG自动诊断、以及临床报告生成的可信度评估。RAG已被用于增强LLM的医学知识，但可能引入不匹配患者数据的标准。ECG诊断标准通常基于测量阈值（如电压、间期），而现有RAG系统较少验证检索内容与患者测量的兼容性。此外，研究还涉及诊断完整性评估，如使用独立工具（Uni-G）和专家标注（PTB-XL）进行交叉验证。本文在此基础上，首次系统量化了RAG在ECG报告中引入无支持标准的比例，并提出基于测量规则的验证框架。

### Q3: 论文如何解决这个问题？

论文构建了一个包含47张标准卡片的库（其中33张无数字验证规则），对1,083份PTB-XL患者记录使用语言模型生成结构化报告（有无检索对比）。采用Marquette 12SL测量值评估标准适用性，并引入确定性验证规则：若标准要求数值条件（如电压>1.0mV），则检查患者测量是否满足；若无数字规则，则标记为不可测试。规则撤回了647次标准应用（其中639次无数字检查），同时保留了268/269次被Uni-G独立支持的应用。进一步限制检索仅使用14条可测试标准，将无支持标准率从46.8%降至13.8%。实验还比较了检索与无检索在相同指令和输出模式下的差异，发现检索反而使无支持报告从17.4%增至31.1%，而 hypertrophy 召回率保持62.6%不变。

### Q4: 论文做了哪些实验？

实验使用1,083份人类验证的PTB-XL记录，47张标准卡片（33张无数字规则）。语言模型（GPT-4.1-mini）生成结构化报告，分有/无检索两组。评估指标包括：无支持标准应用率（通过Marquette 12SL测量验证）、Uni-G独立支持率、以及诊断标签对比。主要结果：关键词检索导致46.8%报告包含不可测试或测量不支持的标准；确定性规则撤回647次应用（639次无数字检查），保留268/269次Uni-G支持的应用；限制检索至14条可测试标准后，无支持率降至13.8%；在匹配指令和输出模式下，检索使无支持报告从17.4%升至31.1%，hypertrophy召回率不变（62.6%）。结论表明检索标准不一定提供有效患者证据，测量验证可减少无支持应用，但诊断有效性需独立评估。

### Q5: 有什么可以进一步探索的点？

局限性包括：仅评估了一种语言模型（GPT-4.1-mini）和单一ECG数据集（PTB-XL），泛化性需验证；验证规则依赖Marquette 12SL测量，可能受测量误差影响；未探索动态检索策略或标准库的自动扩展。未来方向：整合多模态证据（如波形特征）增强验证；开发自适应检索机制，根据患者测量过滤标准；将验证框架扩展到其他临床领域（如影像报告）；研究LLM自我反思与验证器结合，实现端到端可追溯诊断链；探索多智能体协作进行证据路由和诊断完整性检查。

### Q6: 总结一下论文的主要内容

论文评估了RAG在AI生成ECG报告中的可靠性，发现检索到的诊断标准常缺乏患者特异性测量支持（46.8%报告含无支持标准）。提出基于Marquette 12SL测量的确定性验证规则，撤回647次无支持应用（639次无数字检查），保留268/269次Uni-G支持的应用。限制检索至可测试标准后，无支持率降至13.8%。实验表明检索反而增加无支持报告（17.4%→31.1%），而诊断召回不变。结论强调检索标准不一定提供有效证据，测量验证可减少无支持应用，但诊断有效性需独立评估。该工作为临床报告生成的可追溯性和证据验证提供了重要启示。
