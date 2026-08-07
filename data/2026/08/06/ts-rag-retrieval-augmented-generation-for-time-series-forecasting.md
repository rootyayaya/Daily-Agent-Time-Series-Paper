---
title: "TS-RAG: Retrieval Augmented Generation for Time Series Forecasting"
authors:
  - "Yixiong Xiao"
  - "Congxi Xiao"
  - "Jingbo Zhou"
date: "2026-08-06"
arxiv_id: "2608.06223"
arxiv_url: "https://arxiv.org/abs/2608.06223"
pdf_url: "https://arxiv.org/pdf/2608.06223v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Retrieval-Augmented Generation"
  - "Time Series Forecasting"
  - "Reference Tokens"
  - "Similar Sequence Retrieval"
  - "TS-RAG"
relevance_score: 8.5
---

# TS-RAG: Retrieval Augmented Generation for Time Series Forecasting

## 原始摘要

While deep learning models, particularly transformer-based architectures, have shown impressive performance in time series forecasting, the application of retrieval-augmented generation (RAG) in this domain remains limited. Since RAG has proven effective in enhancing the capabilities of large language models by incorporating relevant external information, retrieving similar time series sequences as references might also improve accuracy in time series forecasting tasks. However, most time series models are constrained by limited training data, smaller parameter scales, and a lack of the extensive generative capabilities found in large language models. Simply concatenating reference sequences into the prompt, as done in language models, may not yield the expected results. To address these challenges, we propose a novel approach, TS-RAG, which leverages RAG to enhance forecasting performance. The framework introduces specially designed reference tokens to effectively fuse information from the input sequence with that from retrieved similar sequences, enabling a more robust capture of complex temporal dynamics. Experimental results demonstrate that TS-RAG achieves consistent state-of-the-art performance across several real-world forecasting benchmarks.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列预测在金融、医疗、能源等领域至关重要，基于Transformer的深度模型虽能捕捉长程依赖和复杂时序模式，但现有研究主要聚焦于改进模型训练（如多尺度混合、时间成像），对利用检索增强机制提升预测精度的探索相对匮乏。检索增强生成（RAG）在NLP中已证明能通过引入外部相关知识显著增强大语言模型能力，自然启发我们将类似思路拓展至时间序列领域——通过检索与当前输入相似的历史序列作为参考，有望帮助模型更精准地关注关键动态模式。

然而，直接照搬LLM中“拼接参考序列到提示”的做法在时序模型中难以奏效，原因在于：多数时序模型参数规模小、训练数据有限，缺乏LLM强大的生成与泛化能力，简单拼接无法实现有效信息融合。此外，传统相似性检索方法（如动态时间规整DTW）计算开销大，严重制约推理效率与实时应用。

为此，本文提出TS-RAG框架，核心创新在于设计专门的参考令牌（reference tokens），将输入序列与检索到的相似序列信息进行深度融合，从而稳健捕捉复杂时间动态；同时采用向量检索技术替代DTW，大幅降低计算成本，兼顾预测精度与推理速度。该工作旨在弥合检索增强技术与时间序列预测之间的鸿沟，为利用外部参考信息提升预测性能开辟新途径。

### Q2: 有哪些相关研究？

本文的相关研究主要分为以下几类：

**方法类**：传统深度学习方法（CNN、RNN/LSTM/GRU）用于提取局部或长期时序依赖，但存在梯度消失和计算效率问题；Transformer变体（LogTrans、Informer、Autoformer、FedFormer）通过自注意力机制提升长程建模能力，但面临大规模数据扩展瓶颈；轻量级MLP模型（如基于分解和多周期分析）在效率与精度间取得平衡。本文与这些工作的区别在于，TS-RAG并非仅依赖模型内部参数，而是显式引入检索增强机制，弥补纯参数化模型对罕见模式的适应不足。

**基础模型类**：TimeGPT-1、ForecastPFN、TimesFM、MOIRAI（基于LOTSA数据集）和Tiny Time Mixers等时间序列基础模型通过大规模预训练实现零样本预测。本文指出这些模型仍依赖隐式知识，而TS-RAG通过检索外部相似序列，动态注入显式参考信息，提升对非平稳和未见模式的泛化能力。

**检索增强类**：NLP中的RAG（如问答、摘要）和视觉/结构化数据中的检索方法（如最近邻、原型学习）启发了时序检索研究。早期工作如ReTime引入关系检索，RAFT提出显式检索模块选择相似历史模式。本文与RAFT的关键区别在于，TS-RAG设计了专门的参考token，将输入序列与检索序列深度融合，而非简单拼接，从而更有效地捕获复杂时序动态，并在多个基准上取得一致最优性能。

### Q3: 论文如何解决这个问题？

TS-RAG通过引入检索增强生成机制，将相似历史序列作为外部参考信息融入时间序列预测。整体框架包含四个核心模块：相似性检索、序列编码、注意力融合和预测头。

在检索阶段，模型从历史数据库D中基于相似度函数R检索出N条与输入序列最相关的参考序列。每条检索序列被独立划分为不重叠的patch，并通过共享的嵌入层（权重W_x和偏置b_x）加上位置编码转换为向量表示。

关键创新在于设计了可学习的参考令牌（reference tokens）。每条检索序列对应一个压缩其历史模式特征的参考令牌v_ref，这些令牌被前置拼接在输入序列的patch化表示之前，形成增强的输入嵌入。这种设计避免了简单拼接参考序列带来的信息冗余和噪声干扰，使模型能以更紧凑的方式利用外部知识。

在特征融合方面，模型采用双注意力机制：自注意力捕捉输入序列内部的时间依赖关系，交叉注意力则以输入序列的查询向量去对齐检索序列的键值对，实现选择性信息提取。这种设计使模型能够动态决定从每条参考序列中获取多少有用信息，而不是被动接受全部内容。

最终，融合后的隐藏表示经过前馈网络和预测头输出未来T步的预测值。TS-RAG的核心贡献在于将RAG思想适配到参数规模较小的时间序列模型中，通过参考令牌和交叉注意力机制有效解决了直接拼接参考序列效果不佳的问题，在多个真实世界基准上取得了一致的最优性能。

### Q4: 论文做了哪些实验？

论文在六个公开基准数据集（ETTh1、ETTh2、ETTm1、ETTm2、Electricity、Weather）上进行了长期时间序列预测实验，输入长度固定为96，预测长度分别为96、192、336和720。对比的基线模型包括Informer、Autoformer、FEDformer、PatchTST、TimeXer、iTransformer、RLinear、DLinear、Crossformer、TiDE和TimesNet等。主要结果以MSE和MAE为指标，TS-RAG-CM（考虑通道依赖）在六个数据集上均取得最优或次优性能，平均MSE为0.310、MAE为0.348，全面优于所有基线；TS-RAG（不考虑通道依赖）排名第三，但仍优于iTransformer。

消融实验包含三部分：一是对比直接序列拼接与参考融合机制，TS-RAG-CM在不同预测长度下MSE降低14.2%-18.2%，TS-RAG降低12.1%-16.2%；二是考察检索序列数量，使用单条参考序列效果最佳，2条或4条反而引入噪声导致性能下降；三是比较检索方法，TCN检索性能最优（MSE 0.266/MAE 0.318），检索耗时仅0.004秒，远快于DTW（14.27秒），略慢于欧氏距离（0.002秒）。所有实验在NVIDIA V100 GPU上运行，采用Adam优化器，学习率0.001，结果取五次独立运行的平均值。

### Q5: 有什么可以进一步探索的点？

TS-RAG虽在基准上表现优异，但仍有若干可探索方向。首先，检索策略依赖向量相似度，可能忽略时间序列的相位偏移或尺度差异，未来可引入形状感知的检索（如结合DTW的轻量近似）或学习可判别的时间序列表示。其次，参考token的融合机制较为静态，可尝试自适应门控或跨序列注意力，让模型根据输入动态决定参考信息的权重。第三，当前框架主要面向单步或短期预测，可扩展至多步长或概率预测，并评估检索在长序列中的累积误差影响。此外，对于罕见事件，检索库可能缺乏足够相似样本，可探索生成式数据增强或跨域迁移来丰富参考库。最后，TS-RAG的推理效率虽优于DTW，但大规模检索仍可能成为瓶颈，可研究索引压缩或分层检索策略，以平衡精度与速度。

### Q6: 总结一下论文的主要内容

TS-RAG提出了一种面向时间序列预测的检索增强生成框架，旨在解决现有深度模型因训练数据有限、参数规模小且缺乏生成能力而难以直接应用RAG的问题。该框架通过设计专门的参考令牌，将输入序列与检索到的相似历史序列信息有效融合，从而更稳健地捕捉复杂时间动态。与依赖动态时间规整等昂贵方法不同，TS-RAG采用高效向量检索技术，在保证预测精度的同时显著降低推理成本。在多个真实世界基准上的实验表明，TS-RAG持续取得最先进性能，尤其在数据稀缺或罕见事件场景下优势明显。这项工作弥合了检索增强方法与时间序列预测之间的鸿沟，展示了将NLP思想成功迁移至时间序列领域的潜力，为提升预测准确性和鲁棒性提供了新路径。
