---
title: "Industrial-Instruction: An End-to-End Framework for Building Instruction-Tuning and Benchmark Datasets from Industrial Technical Reports"
authors:
  - "Parsa Bakhtiari"
  - "Hassan Bashiri"
  - "Alireza Khalilipour"
  - "Masoud Nasiripour"
  - "Moharram Challenger"
date: "2026-08-24"
arxiv_id: "2608.22817"
arxiv_url: "https://arxiv.org/abs/2608.22817"
pdf_url: "https://arxiv.org/pdf/2608.22817v1"
github_url: "https://github.com/parssky/industrial-instruction"
categories:
  - "cs.CL"
tags:
  - "Industrial Technical Reports"
  - "Instruction Tuning"
  - "QA Benchmark"
  - "Semantic Retrieval"
  - "Evidence Grounding"
  - "LLM Fine-tuning"
  - "Document Understanding"
  - "Layout-aware Extraction"
  - "Multi-document Reasoning"
  - "Open vs Closed LLM"
relevance_score: 7.5
---

# Industrial-Instruction: An End-to-End Framework for Building Instruction-Tuning and Benchmark Datasets from Industrial Technical Reports

## 原始摘要

Industrial technical reports contain high-value knowledge for maintenance, troubleshooting, and product engineering, but their heterogeneous structure (dense prose, specifications, tables) makes them difficult to index and reason over with standard retrieval and QA pipelines, and no public instruction-tuning or benchmark datasets are built from such documents. We address this gap with Industrial-Instruction, contributing (i) two open QA datasets built from real industrial technical reports and (ii) the end-to-end pipeline that produces them. Using 906 public Panasonic documents (7,525 pages), we apply layout-aware extraction, build a semantic retrieval index, and synthesize multiple-choice QA grounded in retrieved evidence under five query-document relationships (irrelevant retrieval, single-/multi-document support, single-/multi-document answer). After filtering an initial 23.9k generated samples, each dataset provides approximately 13.6k QA pairs with source documents and a held-out benchmark split. Fine-tuning small open LLMs (under 10B parameters) improves Set-Match Accuracy from 28.5% to 42.0% and F1 from 46.6% to 63.5% on the Panasonic benchmark. We release two parallel versions built by the same pipeline: one generated with the open-weight Qwen3-30B-A3B-Instruct model and one with the closed, API-based Claude-Opus-4.6 model, enabling a direct comparison of open- versus frontier-model data generation. The Claude-Opus-4.6 dataset yields a cleaner raw corpus and larger fine-tuning gains, at roughly two orders of magnitude higher cost. MMLU evaluation shows models trained on the Claude-Opus-4.6 data retain essentially all general knowledge, versus a small but measurable forgetting effect for the Qwen-generated data. Together, these datasets and pipeline offer a practical, reproducible path toward scalable industrial benchmarks and training data from real-world documentation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业技术报告蕴含丰富的维护、故障诊断与产品工程知识，但其结构异构（密集文本、规格说明、表格混杂），标准检索与问答流程难以有效索引和推理，且目前缺乏基于此类文档构建的公开指令微调与基准数据集。现有大语言模型虽在通用领域表现优异，却缺乏工业所需的深度专业知识，在工业基准如FailureSensorIQ上准确率仅约53.5%，而基于通用数据集微调的小模型准确率更低至29%。此外，工业领域存在“工业鸿沟”：模型知识广度有余而深度不足、沟通风格不匹配专家需求、通用评估标准不适用。现有研究多聚焦超大模型，对计算成本低、易于工业部署的小模型（<10B参数）关注不足。本文核心问题是：如何从真实工业技术报告中系统化构建高质量的指令微调与基准数据集，以弥合小规模语言模型与工业专业知识之间的鸿沟，并探究开源与前沿闭源模型作为数据生成器的效果差异。

### Q2: 有哪些相关研究？

相关研究主要围绕工业领域大语言模型的评测与数据构建展开。首先，FailureSensorIQ是一项代表性评测工作，基于ISO文档自动生成8,296道专家筛选的多选题，覆盖电机、汽轮机等10类资产，聚焦故障模式与传感器数据的双向映射，最佳模型准确率仅53%，且问题表述变化可使性能降至12%。本文与其区别在于，FailureSensorIQ侧重评测模型内部逻辑的鲁棒性，而Industrial-Instruction专注于从技术报告构建指令微调与基准数据集，并强调端到端流程的可复现性。

其次，针对工业混合数据（文本与表格）处理，D. Min等人比较了Markdown模板、模板序列化、传统预训练模型（如BART）及LLM四种表转文本方法，发现领域微调下LLM和预训练模型更优，而RAG场景中Markdown格式检索对齐效果最佳。本文的布局感知提取与语义索引构建与该工作互补，但更关注多文档问答关系（如无关检索、单/多文档支持）的合成策略。

此外，H. Femmer等人提出的QuRE数据集包含2,111条来自奔驰的真实工业需求，标注了弱词质量，用于评估LLM生成需求与真实数据的复杂度差距。本文与其区别在于，QuRE聚焦需求工程的质量评估，而本文面向技术报告的知识抽取与问答，且通过微调实验验证了数据对模型性能的实际提升。总体而言，本文填补了工业技术报告缺乏公开指令微调与基准数据的空白，并与上述工作在评测设计、混合数据处理及数据真实性方面形成互补。

### Q3: 论文如何解决这个问题？

论文提出了一套端到端的数据集构建框架，用于从工业技术报告中自动生成指令微调与基准测试数据。整体流程分为四个核心阶段：**文档解析与清洗**、**语义检索索引构建**、**基于检索场景的QA合成**以及**质量过滤与基准划分**。

在文档解析阶段，作者对比了规则型与学习型方法后，选用视觉语言模型Dots.OCR将PDF页面转换为Markdown格式，同时输出JSON结构（含区域类型与文本）和JPG图像，以兼顾表格、复杂布局的语义保留。针对模型在密集表格区域出现的幻觉和定位误差，人工识别并剔除了291页提取失败的页面，随后过滤掉空白或重复的370页，仅保留文本与表格数据，移除所有图像，确保纯文本语言模型的可处理性。

在检索索引构建中，采用EmbeddingGemma（300M参数，支持768→128维降维）作为嵌入模型，配合FAISS向量库实现高效的语义检索。基于该检索系统，作者设计了五种真实场景下的查询-文档关系：无关文档（r0）、单/多文档支持（r1/r2）与单/多文档直接答案（r3/r4），使生成的QA对能覆盖幻觉抑制、多步推理与信息整合等实际需求。

QA合成阶段使用Qwen3-30B-A3B-Instruct（开源）与Claude-Opus-4.6（闭源API）两个大模型，通过包含文档内容与随机指令的提示模板，生成多样化的多项选择题。最终从初始23.9k样本中过滤得到约13.6k高质量QA对，并划分出独立的基准测试集。

该框架的核心创新在于：一是首次构建了基于真实工业技术报告的开源QA数据集；二是提出了可复现的端到端流水线，支持布局感知提取、语义检索与多场景QA合成；三是通过对比开源与闭源模型的数据生成效果，揭示了成本与质量之间的权衡关系。

### Q4: 论文做了哪些实验？

论文构建了完整的实验框架，包含数据质量评估与模型微调验证两部分。实验设置上，将每个数据集划分为训练集和测试集，先评估基座模型在测试集上的表现，再用训练集进行微调，最后在Panasonic基准和外部FailureSensorIQ数据集上双重验证。评估指标采用Exact-Match（字符级严格匹配）和Set-Match Accuracy（集合匹配准确率）及F1分数。

对比方法包括：未微调的基座模型、基于Qwen3-30B-A3B-Instruct生成数据微调的模型、基于Claude-Opus-4.6生成数据微调的模型。主要结果：在Panasonic基准上，微调后的小型开源模型（<10B参数）将Set-Match Accuracy从28.5%提升至42.0%，F1从46.6%提升至63.5%。Claude-Opus-4.6数据生成的模型微调增益更大，且MMLU评估显示其几乎不损失通用知识，而Qwen生成数据训练的模型出现轻微遗忘效应。在FailureSensorIQ外部数据集上同样验证了微调效果，但具体数值未在文中详述。实验还对比了两种数据生成成本：Claude-Opus-4.6版本虽然数据质量更高，但成本约为Qwen版本的100倍。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从以下几方面展开：首先，当前数据集仅基于Panasonic单一来源，领域覆盖有限，未来可扩展至更多工业厂商和垂直行业（如能源、航空）以增强泛化性。其次，QA生成依赖LLM的合成质量，虽经过滤但仍可能存在噪声或事实偏差，可引入人工专家审核或基于规则的一致性校验来提升标注可靠性。第三，当前仅评估了10B以下小模型，未来可探索更大规模模型或混合检索增强策略（如结合图结构索引表格关系）以提升复杂多文档推理能力。此外，MMLU显示Qwen数据存在轻微遗忘，可研究参数高效微调（如LoRA）或领域自适应预训练来缓解灾难性遗忘。最后，可考虑将数据集用于训练工业专用Agent，结合工具调用和实时传感器数据，实现从静态QA到动态故障诊断的闭环，并构建多轮交互式评测基准。

### Q6: 总结一下论文的主要内容

本文针对工业技术报告结构异构、知识分散、缺乏公开指令微调与基准数据集的问题，提出了Industrial-Instruction框架。该框架基于906份松下公开文档（7525页），通过布局感知提取、语义检索索引构建和基于证据的多选题生成，构建了两个包含约1.36万QA对的开源数据集，并划分出独立基准测试集。数据集覆盖五种查询-文档关系，包括无关检索、单/多文档支持及单/多文档答案。实验表明，在小于10B参数的小型开源模型上微调后，Set-Match Accuracy从28.5%提升至42.0%，F1从46.6%提升至63.5%。研究还对比了开放权重模型Qwen3-30B与闭源API模型Claude-Opus-4.6生成数据的效果，发现后者数据质量更优、微调增益更大，但成本高出约两个数量级，且MMLU评测显示其几乎不损失通用知识。该工作为工业领域可扩展基准构建和模型训练提供了可复现的端到端路径。
