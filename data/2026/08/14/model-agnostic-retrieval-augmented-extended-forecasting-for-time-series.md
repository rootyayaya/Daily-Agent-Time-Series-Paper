---
title: "Model-agnostic Retrieval-Augmented Extended Forecasting for time series"
authors:
  - "Juan Pablo Villa Serna"
  - "Rohan Asthana"
  - "Vasileios Belagiannis"
date: "2026-08-14"
arxiv_id: "2608.14054"
arxiv_url: "https://arxiv.org/abs/2608.14054"
pdf_url: "https://arxiv.org/pdf/2608.14054v1"
categories:
  - "cs.LG"
tags:
  - "Retrieval-Augmented Forecasting"
  - "Time Series Foundation Models"
  - "RAG for Time Series"
  - "Model-Agnostic Adaptation"
  - "Zero-shot Forecasting"
  - "Domain Adaptation"
  - "Efficient Inference"
relevance_score: 7.5
---

# Model-agnostic Retrieval-Augmented Extended Forecasting for time series

## 原始摘要

Time series forecasting with pretrained foundation models has demonstrated strong zero-shot capabilities. However, achieving optimal performance on time series with short or negligible historical data in domain-specific applications typically requires adaptation via either fine-tuning or RAG. While fine-tuning is effective, it incurs substantial computational costs. This work explores RAG within univariate time series (Retrieval Augmented Generation) as a more efficient alternative, in particular RAF (Retrieval Augmented Forecasting), and introduces RAEF (Retrieval-Augmented Extended Forecasting), a model-agnostic method built upon RAF. RAEF incorporates key refinements to the retrieval and aggregation mechanisms: (1) direct retrieval in input-space rather than embedding-space, reducing inference overhead, and (2) concatenation-based aggregation that preserves temporal structure instead of averaging. Empirical evaluation across multiple benchmark datasets demonstrates that RAEF outperforms RAF in both accuracy and inference overhead. Furthermore, comprehensive comparisons with zero-shot and fine-tuned foundation models show that RAEF achieves competitive or superior performance to fine-tuning while avoiding its computational burden, establishing it as a practical and scalable approach for domain adaptation in time series forecasting.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列预测在金融、能源、医疗等领域至关重要，预训练基础模型虽具备零样本能力，但在历史数据稀缺的领域场景下性能不佳，需通过微调或检索增强生成（RAG）进行领域适配。现有方法存在明显不足：微调虽有效但计算成本高昂，与模型规模和数据集大小成正比；而现有时间序列RAG方法（如TimeRAF、RATD等）多依赖定制架构或领域训练，缺乏模型无关性。仅有的模型无关方法中，FinSrag依赖大语言模型导致计算开销接近微调，RAF虽通过嵌入空间检索并平均检索样本的未来成分，但这种平均策略会稀释关键时间模式，限制其有效性。

本文提出RAEF（检索增强扩展预测），一种模型无关的时间序列预测方法，旨在解决RAF的两大局限：一是直接在输入空间而非嵌入空间进行检索，将推理开销降低四倍；二是采用拼接而非平均的聚合方式，保留检索样本的时间结构。核心目标是实现无需微调即可达到甚至超越微调性能的领域适配，同时避免计算负担，为时间序列预测提供实用且可扩展的RAG方案。

### Q2: 有哪些相关研究？

时间序列预测中的相关研究主要分为以下几类：

**方法类**：本文与RAF（Retrieval Augmented Forecasting）关系最密切。RAF通过嵌入空间检索相似样本并平均其未来值，而RAEF直接在输入空间检索，并采用拼接聚合替代平均，保留时间结构。其他方法如TimeRAF、RATD、RAFT和TS-RAG需要定制架构或领域训练，缺乏模型无关性；FinSrag虽模型无关但依赖LLM，计算开销接近微调。

**基础模型类**：本文基于Moirai、Chronos-T5和Chronos-Bolt等预训练基础模型，这些模型（如Moirai、TimesFM、PatchTST）具备零样本能力，但在历史数据不足时性能受限，RAEF通过检索增强弥补这一缺陷。

**评测类**：本文首次系统对比了RAG与微调在时间序列任务中的表现，在六个基准数据集上验证RAEF优于RAF（MASE提升11-16% vs 1-7%），且达到或超过微调效果，同时计算开销更低。

与现有工作的核心区别在于：RAEF无需修改模型架构或训练参数，仅通过输入空间检索和拼接聚合实现高效领域自适应，避免了微调的高成本和嵌入检索的额外开销。

### Q3: 论文如何解决这个问题？

RAEF针对RAF的两大缺陷提出改进：一是去除嵌入层，直接在原始输入空间进行检索；二是用“候选-残差”混合聚合替代简单平均。

整体框架沿用RAF的“检索-增强-预测”流程。首先，从训练集中构建向量数据库，但不再对查询样本和库中样本做嵌入投影，而是直接计算输入序列间的欧氏距离作为相似度度量，检索出top-k个最相似样本及其对应未来值。这一改动基于时间序列本身已是实值连续向量、欧氏距离可直接度量相似性的观察，省去了嵌入步骤带来的推理开销，同时避免了投影可能造成的信息损失。

在聚合阶段，RAEF引入关键创新：将检索样本按归一化后的距离分数分为候选集（高相关）和残差集（低相关）。候选集样本按分数升序直接沿时间维度拼接，形成包含最相关模式的长序列；残差集则取平均以保留部分信息。这种“拼接+平均”的混合策略既保留了高相关样本的完整时序结构，又控制了序列长度，平衡了信息保留与计算效率。最终增强输入由残差表示、候选拼接序列和归一化后的原始输入依次拼接而成。

此外，RAEF还移除了RAF中的对齐步骤，认为预训练模型可将未对齐的检索样本视为周期性历史模式，从而更自然地捕捉长程时间依赖。整体上，RAEF通过输入空间检索、阈值划分的混合聚合和去对齐设计，在保持检索增强优势的同时显著降低了推理成本，并提升了预测精度。

### Q4: 论文做了哪些实验？

实验在6个基准数据集（ET、Power、Traffic、FredMd、ElectricityUCI、Huawei Cloud）上评估RAEF，以MoiraiMoE为主干（推理时间16ms），并扩展至Chronos-T5和Chronos-Bolt验证模型无关性。设置预测视界F=16，上下文长度C∈{32,64,128}，向量库含10,000训练样本（HNSW索引），阈值d_t=1.0，k=16，采用MASE指标，3个随机种子。对比方法包括：Base（零样本）、Fine-Tuning（全参数微调，学习率1e-4，早停patience=3）、RAF（嵌入空间检索+平均聚合）和RAEF。

主要结果：RAEF在MoiraiMoE上平均提升15.80%（C=32）、11.78%（C=64）、11.26%（C=128），全面优于RAF（7.31%、1.81%、0.78%）和微调（2.75%、3.02%、2.20%）。在Chronos-T5上提升13.88%（C=32）、8.21%（C=64）、13.24%（C=128），Chronos-Bolt在C=128提升3.50%。RAEF在6个数据集中4个达到或超过微调性能，且无需参数更新。消融实验显示：输入空间检索将推理开销从8ms降至2ms；拼接聚合比平均聚合提升显著（15.80% vs 7.31%）；阈值分离贡献额外5.66%提升。d_t=1.0时性能最优（6.77%提升）。短上下文收益更大，C=256时降至6%，C=512时接近0。

### Q5: 有什么可以进一步探索的点？

RAEF在检索与聚合机制上虽有创新，但仍存在若干可探索方向。首先，当前方法仅针对单变量时间序列，如何将检索增强扩展到多变量场景（如捕获跨变量依赖）是重要延伸。其次，直接检索输入空间虽降低开销，但可能对噪声敏感，可考虑引入轻量级特征变换或自适应检索窗口。第三，聚合方式仅用简单拼接，未来可探索基于注意力或学习的加权融合，以更好利用检索样本的互补信息。此外，RAEF依赖外部库质量，当检索库与目标域分布差异大时性能可能下降，可研究动态库更新或检索样本筛选策略。最后，与LLM结合时，可尝试让模型生成检索查询或解释检索结果，增强可解释性与鲁棒性。这些方向有望进一步提升RAEF的泛化能力与实用价值。

### Q6: 总结一下论文的主要内容

本文提出了一种模型无关的检索增强扩展预测框架RAEF，用于提升时间序列基础模型在历史数据稀缺场景下的预测性能。传统微调虽有效但计算成本高，而现有RAG方法在检索效率和时序结构保持上存在不足。RAEF在RAF基础上改进了两点：一是在输入空间直接检索而非嵌入空间，降低推理开销；二是采用拼接式聚合替代平均，保留时间序列的时序结构。实验在六个数据集和三个基础模型上进行，结果显示RAEF相比基线模型在MASE指标上提升11%至16%，并在4/6数据集上达到或超过微调性能，同时避免了计算负担。该工作为资源受限环境下的时间序列领域自适应提供了高效、可扩展的实用方案，具有重要的应用价值。
