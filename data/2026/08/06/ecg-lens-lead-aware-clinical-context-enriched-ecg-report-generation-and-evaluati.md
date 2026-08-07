---
title: "ECG-LENS: Lead-Aware Clinical Context Enriched ECG Report Generation and Evaluation"
authors:
  - "Akanta Das"
  - "Tasinul Islam Ahon"
  - "Ahmed Mahir Sultan Rumi"
  - "Md Mahbubur Rahman"
  - "Tausif Amim Shadly"
  - "Tanzima Hashem"
date: "2026-08-06"
arxiv_id: "2608.05893"
arxiv_url: "https://arxiv.org/abs/2608.05893"
pdf_url: "https://arxiv.org/pdf/2608.05893v1"
categories:
  - "cs.AI"
tags:
  - "ECG报告生成"
  - "多导联时序建模"
  - "临床文本生成"
  - "GPT-2解码器"
  - "诊断标签评估"
  - "PTB-XL"
  - "MIMIC-IV-ECG"
relevance_score: 7.5
---

# ECG-LENS: Lead-Aware Clinical Context Enriched ECG Report Generation and Evaluation

## 原始摘要

Electrocardiography (ECG) is one of the most widely used non-invasive tools for diagnosing cardiovascular disease, but transforming multi-lead ECG recordings into reliable clinical reports remains challenging. Automating ECG report generation could reduce clinicians' interpretive workload, improve diagnostic efficiency, and expand access to cardiac assessment in underserved communities. Unlike image-based report-generation tasks, ECG interpretation requires the analysis of subtle temporal morphologies, followed by coherent diagnostic reasoning expressed in dense clinical terminology. Existing systems predominantly focus on classification, while current report-generation methods often produce outputs that remain inadequate for practical clinical use. To address these challenges, we propose ECG-LENS, an end-to-end ECG report-generation framework that jointly integrates multi-lead signal modeling, diagnosis-aware representations, and clinically grounded text generation. ECG-LENS combines lead-wise encoders that preserve localized waveform morphology with a global encoder that captures inter-lead dependencies. To guide report generation, we fuse signal representations with clinically enriched textual prompts that condition a GPT-2 decoder. We further introduce an ECG-specific report-preprocessing strategy that helps the model focus on clinically meaningful findings. Finally, because lexical metrics may under- or overestimate report quality, we propose F1-ECGBERT, a BERT-based, ECG-specific metric that measures agreement between diagnostic labels extracted from generated and reference reports. In-domain experiments on PTB-XL and cross-domain evaluation on MIMIC-IV-ECG show that ECG-LENS consistently outperforms state-of-the-art methods, with absolute gains of 4.0%, 6.3%, and 11.5% in METEOR, ROUGE-L, and F1-ECGBERT, respectively, over the strongest baselines.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

心电图（ECG）是诊断心血管疾病最常用的无创工具，但将多导联记录转化为可靠的临床报告仍具挑战。现有深度学习系统多聚焦于疾病分类，输出孤立标签，无法提供临床报告所需的整合性描述（如节律、传导、ST/T改变及受累导联）。尽管影像报告生成已取得进展，ECG报告生成仍滞后，主要因为ECG是多变量时间序列，需联合建模细微时间形态与导联间空间关系，而现有方法往往将全记录压缩为单一表征，丢失导联特异性证据（如II、III、aVF导联ST抬高提示下壁心梗）；同时，直接以全局嵌入条件化语言模型缺乏显式诊断计划，且参考报告存在多语言、缩写等歧义；此外，BLEU、ROUGE等词汇重叠指标无法区分临床关键发现缺失或幻觉。为此，本文提出ECG-LENS框架，通过导联级编码器保留局部形态、全局编码器捕获导联间依赖，结合预测诊断标签构建临床上下文提示引导GPT-2解码，并引入F1-ECGBERT指标评估诊断一致性，以生成临床可用且评估可靠的报告。

### Q2: 有哪些相关研究？

现有研究主要围绕三个方向展开。**方法类**方面，早期工作将ECG解读视为分类任务，直接预测诊断标签，但缺乏对节律、形态和导联异常的细粒度解释；后续自监督方法如ST-MEM和HeartLang通过掩码表示学习或形态-节律层次建模提取表征，多模态方法如MERL和D-BETA则利用临床报告进行跨模态对齐，但这些方法均止步于分类，无法生成连贯的临床叙述。**报告生成类**方面，近期方法分为嵌入式和分词式：MEIT和BiECG-LLM将ECG信号编码为潜在表示或伪标记以条件化语言模型，ECG-Chat则扩展至诊断对话，但这些方法未显式保留导联级诊断上下文，也缺乏结构化的诊断规划。**评测类**方面，现有工作普遍使用BLEU、ROUGE、METEOR和BERTScore等词面相似度指标，无法验证报告中的临床诊断信息是否准确。本文与上述工作的核心区别在于：ECG-LENS首次将导联级编码器与全局编码器结合，显式建模局部波形形态和导联间依赖，并通过临床增强文本提示为解码器提供诊断计划；同时提出F1-ECGBERT这一ECG专用评测指标，从诊断标签一致性角度评估报告质量，弥补了词面指标在临床可靠性评估上的不足。

### Q3: 论文如何解决这个问题？

ECG-LENS通过四个核心组件的协同集成来解决ECG报告生成问题。整体框架采用端到端架构，包含以下主要模块：

**编码模块**采用双路径设计：12个独立的1D ResNet-18编码器分别处理每个导联的时序信号，通过全局平均池化和线性投影保留局部波形形态与导联身份信息；同时，一个全局ResNet-18编码器将12个导联作为多通道输入联合建模，捕获导联间的诊断性依赖关系。两条路径的输出堆叠形成综合ECG表示。

**临床上下文增强模块**利用冻结的预训练分类器MERL获取多标签诊断预测，通过验证集网格搜索确定各类别的置信度阈值，仅保留高置信度预测，并将其映射为符合SCP-ECG标准的规范化临床短语，构成紧凑的诊断提示段落，与ECG表示共同输入解码器。

**报告预处理方案**采用GPT-5.5少样本提示策略，从原始报告中提取核心诊断内容，去除重复、非信息性及管理性文本，同时保持诊断结论与导联关联不变，并由心脏病专家审核，生成标准化训练目标。

**生成模块**使用从零训练的自定义GPT-2解码器，配备基于PTB-XL报告构建的领域专用分词器，以自回归方式逐词生成报告。

创新点在于：导联级与全局编码的互补设计、冻结分类器提供诊断先验的提示机制、临床聚焦的报告预处理，以及F1-ECGBERT评估指标——通过四个BERT分类器分别提取生成报告与参考报告的诊断标签并计算F1分数，实现临床语义层面的质量评估。

### Q4: 论文做了哪些实验？

实验在PTB-XL（21,799条12导联记录）上进行域内训练与测试，并在MIMIC-IV-ECG上做跨域评估。对比方法包括MEIT、ECG-aBcDe、BiECG-LLM、ECG-Chat和HeartLLM。模型采用1D ResNet-18编码器（导联级+全局）和GPT-2风格解码器，在单张RTX 4090上训练。

域内结果中，ECG-LENS在所有指标上领先：BLEU-1/2/3达0.651/0.569/0.501，ROUGE-L和METEOR分别为0.686和0.714，较最强基线BiECG-LLM分别提升12.8%（BLEU-2）、8.5%（ROUGE-L）和3.2%（METEOR）。F1-ECGBERT诊断一致性评估中，ECG-LENS在superclass、subclass、rhythm、form四类分别达0.768、0.745、0.732、0.702，其中superclass较最强基线提升10.9%。

跨域测试中，ECG-LENS仍保持最高分（METEOR 0.701，ROUGE-L 0.612），较基线提升超4%和10%的BLEU增益，证明其泛化能力。消融实验显示，ResNet全局编码器优于Transformer；逐步加入报告预处理、导联级编码和临床提示后，各指标持续提升（BLEU-1从0.475升至0.651，METEOR从0.556升至0.714）。此外，心内科医生评审中67%生成报告完全临床正确。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是受计算资源限制，未系统探索更大容量的编码器/解码器架构，可能制约了表示学习和报告生成的进一步提升；二是模型仍存在少量幻觉或诊断错误，尤其在跨域场景下，临床可靠性有待加强；三是F1-ECGBERT指标虽优于词面相似度，但依赖标签提取的准确性，对复杂诊断表述的覆盖可能不足。

未来可从以下方向深入探索：其一，引入基于医学知识图谱或外部临床规则库的约束解码，在生成阶段显式抑制与生理信号矛盾的内容，降低幻觉率；其二，设计多任务学习框架，将心跳分类、节律异常检测等辅助任务与报告生成联合优化，增强信号-文本对齐的因果一致性；其三，探索基于大语言模型（如LLaMA）的轻量化微调或检索增强生成，利用领域语料提升术语密度和推理逻辑；其四，开发可解释性模块，将导联级注意力权重映射为文本中的关键证据，便于医生校验并提升模型可信度。此外，可扩展至12导联动态心电图或穿戴设备长程数据，验证框架在更复杂临床场景下的泛化能力。

### Q6: 总结一下论文的主要内容

ECG-LENS是一个端到端的心电图（ECG）报告生成框架，旨在解决从多导联ECG信号自动生成临床可靠文本报告的挑战。该问题不同于图像报告生成，需捕捉细微的时序形态并输出密集的临床术语推理。方法上，ECG-LENS结合了导联级编码器保留局部波形形态、全局编码器建模导联间依赖，并通过临床增强的文本提示融合信号表示，条件化GPT-2解码器生成报告。此外，引入ECG专用报告预处理策略聚焦临床有意义发现，并提出F1-ECGBERT指标，基于BERT评估生成与参考报告间诊断标签的一致性，弥补词汇指标的不足。在PTB-XL域内和MIMIC-IV-ECG跨域实验中，ECG-LENS在METEOR、ROUGE-L和F1-ECGBERT上分别超越最强基线4.0%、6.3%和11.5%，且推理仅需约30ms，适合资源受限场景。主要结论表明，该框架显著提升了报告的语义质量和临床可靠性，但仍有少量幻觉错误，未来需探索更大架构和缓解策略。此项工作推进了自动化ECG报告生成的临床实用性。
