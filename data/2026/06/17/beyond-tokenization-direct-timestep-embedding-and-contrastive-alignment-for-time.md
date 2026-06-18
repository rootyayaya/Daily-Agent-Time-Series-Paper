---
title: "Beyond Tokenization: Direct Timestep Embedding and Contrastive Alignment for Time-Series Question Answering"
authors:
  - "Yafeng Wu"
  - "Huu Hiep Nguyen"
  - "Thin Nguyen"
  - "Hung Le"
date: "2026-06-17"
arxiv_id: "2606.18986"
arxiv_url: "https://arxiv.org/abs/2606.18986"
pdf_url: "https://arxiv.org/pdf/2606.18986v1"
categories:
  - "cs.CL"
  - "cs.AI"
tags:
  - "Time-Series Question Answering"
  - "LLM for Time Series"
  - "Contrastive Learning"
  - "Direct Timestep Embedding"
  - "Semantic Alignment"
  - "Time Series Representation"
  - "Tokenization Bottleneck"
relevance_score: 6.5
---

# Beyond Tokenization: Direct Timestep Embedding and Contrastive Alignment for Time-Series Question Answering

## 原始摘要

Recent advances in large language models (LLMs) have given rise to time-series question answering (TSQA), which formulates time-series analysis as natural-language question answering. However, directly feeding raw numerical series into LLMs suffers from a tokenization bottleneck: Byte Pair Encoding fragments continuous values into unstable tokens whose embeddings lack meaningful metric structure, resulting in the loss of magnitude, scale, and trend information. Prior methods use patch-based encoders that split the series into fixed windows, locking in one granularity that breaks patterns and hides exact timesteps, through a separate module that rarely transfers across datasets with different lengths or sampling rates. To address this challenge, we propose CADE (Contrastive Alignment with Direct Embedding), a novel framework for TSQA built upon two key components: direct timestep embedding and semantic alignment. The proposed framework maps each timestep directly into the LLM embedding space through a point-wise linear encoder and MLP projector, preserving exact index-level access while eliminating the need for patching and padding. To further bridge the semantic gap between time-series and language representations, we introduce a novel one-directional supervised contrastive loss that aligns time-series embeddings with frozen class-name text anchors. Experimental results on the public Time-MQA benchmark demonstrate that our framework consistently improves performance across six TSQA tasks, outperforming both open-source and proprietary LLM baselines.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列分析在医疗、工业、金融等领域至关重要，但传统深度学习方法在泛化性和推理能力上存在局限。近年来，大语言模型（LLM）展现出强大的推理能力，研究者尝试将其用于时间序列问答（TSQA），即让LLM直接基于自然语言问题回答时间序列分析任务。然而，现有方法面临一个核心瓶颈：LLM的Byte Pair Encoding（BPE）分词器无法有效编码连续数值，会将数值（如182.62）分割成不稳定、无度量结构的子词，导致模型丢失数值的大小、尺度和趋势信息。为绕过分词问题，现有方法采用基于分块的编码器，将序列分割成固定窗口，但这会锁定单一时间粒度，破坏跨窗口的模式，且无法精确定位具体时间步，同时引入的独立预训练模块难以在不同长度或采样率的数据集间迁移。本文旨在解决上述问题，提出CADE框架，通过直接时间步嵌入和语义对齐，在保留精确索引级访问的同时，弥合时间序列与语言表示之间的语义鸿沟，从而提升LLM在TSQA任务上的性能。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是提示词方法，如PromptCast和LLMTime，将数值序列序列化为文本提示用于直接预测，但存在数值表示不精确的问题。第二类是多模态架构，如Time-LLM和UniTime，对齐时间表示与语言模型嵌入用于跨域预测，但未充分利用LLM的推理能力。第三类是时间序列问答专用方法，如ChatTS、ChatTime、Time-MQA和ITFormer。ChatTS针对开放端时间序列推理，而非任务导向的多任务设置；ChatTime是预训练基础模型；Time-MQA通过LoRA微调LLM，但直接使用文本分词器处理数值，导致数字分割不稳定；ITFormer采用基于补丁的编码器，固定了时间粒度。本文与这些工作的核心区别在于：提出直接时间步嵌入（点式线性编码器+MLP投影器），避免分词伪影和补丁粒度限制；并引入单向监督对比损失对齐时间序列与冻结类名文本锚点，在六个TSQA任务上统一提升性能。

### Q3: 论文如何解决这个问题？

该论文提出的CADE框架通过直接时间步嵌入和语义对齐两个核心组件解决时间序列问答中的分词瓶颈问题。整体框架包含四个模块：线性时间序列编码器、MLP投影器、大语言模型和单向监督对比损失。

核心方法上，首先对每个时间序列独立进行z-score归一化，并保留原始统计特征以文本形式附加到提示中。线性时间序列编码器采用单层线性层将归一化序列直接映射到连续特征空间，实现每个时间步与嵌入的一一对应，避免了分块和填充操作，能够处理任意长度和采样率的序列。MLP投影器通过GELU激活和层归一化将编码特征投影到大语言模型嵌入空间，使时间序列令牌与文本令牌可拼接。

关键技术在于单向监督对比损失，仅应用于分类任务。通过时间维度平均池化获得投影嵌入锚点，维护一个循环记忆队列存储历史样本的投影嵌入和标签，使用冻结的类别名称文本嵌入作为固定锚点。采用监督对比损失拉近同类样本的时间序列嵌入与文本嵌入距离，推远异类样本。总损失为交叉熵损失和对比损失的加权组合，对比损失仅更新编码器和投影器参数。

创新点包括：直接时间步嵌入保留精确索引访问和原生分辨率；单向对比对齐使时间序列嵌入向冻结文本锚点对齐；统计特征文本化补充归一化丢失的绝对数值信息。

### Q4: 论文做了哪些实验？

论文在Time-MQA基准上进行了实验，该基准包含分类、异常检测、真/假、多项选择、预测和插补六项任务。训练集约8,286个样本（每任务约1,400个），测试集约2,376个样本（每任务约400个）。对比方法包括：Time-MQA（LoRA微调LLM）、Time-MQA (Full FT)（全参数微调）、ITFormer（QFormer架构，替换为冻结Time-MoE编码器）、Frozen Time-MoE（冻结预训练编码器）以及内部消融变体（Frozen Random Linear、CADE w/o SupCon）。主要结果：CADE在10个指标中的5个上取得最佳，包括预测FCR（0.598）、预测Own MSE（296,897）、插补Own MSE（25,210）、异常检测准确率（0.8625）和多项选择准确率（0.5315）。在共享MSE上，CADE的预测共享MSE为32,268（低于Frozen Random Linear的29,917），插补共享MSE为5,999（低于Time-MQA (Full FT)的4,313）。消融实验表明：连续线性编码器显著优于BPE分词（如预测FCR从0.46提升至0.596）；随机线性编码器已超越BPE；对比损失进一步提升了异常检测和多项选择性能。超参数实验显示，记忆库大小512和损失权重λ=0.1为最佳设置。

### Q5: 有什么可以进一步探索的点？

论文的局限性和未来研究方向可从以下几个层面展开：首先，当前方法在共享MSE指标上未达最优，说明在“简单样本”上仍有提升空间，未来可探索自适应编码粒度或动态投影策略，以平衡不同难度样本的表征质量。其次，单方向对比损失仅对齐时间序列与类别名锚点，未建模序列内部的时间依赖关系，可引入时序对比学习（如相邻/非相邻时间步对比）或层次化对齐（局部模式+全局语义）。第三，线性编码器虽简洁高效，但可能无法捕捉多尺度或非平稳模式，未来可设计轻量级可学习滤波器组或频率域嵌入。此外，当前仅在单一LLM（Qwen-3-0.6B）上验证，需在更大规模模型（如7B/13B）及多语言场景下测试泛化性。最后，Memory bank大小和对比损失权重对性能敏感，可探索自适应调节机制或基于课程学习的动态调度策略。

### Q6: 总结一下论文的主要内容

该论文针对时间序列问答（TSQA）中原始数值序列直接输入大语言模型（LLM）导致的“分词瓶颈”问题，提出了一种名为CADE（对比对齐与直接嵌入）的新框架。核心贡献在于：一是提出直接时间步嵌入，通过逐点线性编码器和MLP投影器将每个时间步直接映射到LLM嵌入空间，保留了精确的索引级访问，避免了传统分块编码带来的粒度锁定和模式破坏；二是引入单向监督对比损失，将时间序列嵌入与冻结的类名文本锚点进行语义对齐，弥合了序列与语言表征间的语义鸿沟。在Time-MQA基准上的实验表明，CADE在六个TSQA任务上均优于开源和专有LLM基线，证明了其有效性和通用性。该工作为时间序列分析与LLM的深度融合提供了新范式，具有重要的理论意义和实际应用价值。
