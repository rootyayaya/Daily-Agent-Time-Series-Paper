---
title: "RAG-HAR+: Towards Cost-Efficient LLM-Based Human Activity Recognition for Edge Deployment"
authors:
  - "Hansi Karunarathna"
  - "Nirhoshan Sivaroopan"
  - "Chamara Madarasingha"
  - "Anura Jayasumana"
  - "Kanchana Thilakarathna"
date: "2026-07-29"
arxiv_id: "2607.26631"
arxiv_url: "https://arxiv.org/abs/2607.26631"
pdf_url: "https://arxiv.org/pdf/2607.26631v1"
categories:
  - "cs.LG"
  - "cs.IR"
tags:
  - "RAG"
  - "LLM-based classification"
  - "human activity recognition"
  - "retrieval-augmented generation"
  - "edge deployment"
  - "training-free"
  - "agent"
  - "cost optimization"
  - "wearable sensors"
relevance_score: 7.5
---

# RAG-HAR+: Towards Cost-Efficient LLM-Based Human Activity Recognition for Edge Deployment

## 原始摘要

Human Activity Recognition (HAR) from wearable sensors supports applications in healthcare, rehabilitation, fitness tracking, and smart environments. Yet, existing deep learning approaches require dataset-specific training, large labeled corpora, and repeated adaptation to new sensor settings or activity taxonomies. Retrieval-Augmented Generation for Human Activity Recognition (RAG-HAR) addresses this by framing HAR as a training-free, retrieval-augmented task, in which statistical descriptions of sensor windows are used to retrieve similar labeled examples that guide LLM-based classification. We introduce RAG-HAR+, a retrieval-first and cost-optimized extension that strengthens retrieval while reducing dependence on LLM-based inference. RAG-HAR+ uses an offline Retrieval Designer Agent to design dataset-specific feature groups from a diverse pool of motion descriptors, enabling sensor windows to be compared using features better aligned with dataset-specific activity patterns. During inference, RAG-HAR+ uses majority voting over retrieved neighbors for samples with strong retrieval evidence and defers only uncertain cases to an LLM-based Ambiguity Resolver Agent. Across six HAR benchmarks, RAG-HAR+ maintains competitive or improved performance while reducing LLM usage, token consumption, and inference time. We further extend the RAG-HAR mobile prototype to demonstrate the practical feasibility of retrieval-first, LLM-assisted HAR in mobile sensing scenarios.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决基于可穿戴传感器的人类活动识别（HAR）在边缘部署中面临的成本与效率瓶颈问题。研究背景是，现有深度学习HAR方法依赖数据集特定训练、大量标注数据，且难以适应传感器设置或活动分类的变化。虽然大语言模型（LLM）具备语义知识与泛化能力，但原始传感器数据无法直接输入LLM，且LLM缺乏活动特定知识。此前提出的RAG-HAR方法通过检索增强生成实现免训练HAR，但存在两大不足：一是检索表示固定，使用统一的统计描述符，无法捕捉不同活动（如周期性运动与静态姿势）的区分性特征；二是每个测试样本都需调用LLM，导致高昂的令牌成本、网络延迟和连接依赖，在持续流式数据推理中成为部署的主要障碍。本文提出RAG-HAR+，核心是将LLM从在线分类器转变为离线检索设计器，通过一次性的离线阶段设计数据集特定的多向量检索组，在线阶段仅对检索邻居投票不确定的模糊样本调用LLM作为歧义解析器，从而大幅降低LLM使用率（89.3-99.9%），在保持或提升性能的同时实现成本高效的边缘部署。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是**基于LLM的传感器推理方法**，如SensorLLM使用通道特定token和任务感知微调，LLM4HAR结合传感器适配与效率模块，PH-LLM在专家案例和可穿戴数据上微调。这些方法需要微调或任务特定适配，缺乏训练自由特性，限制了向新传感器配置或活动分类的迁移能力。第二类是**直接提示方法**，如HARGPT避免训练但细粒度活动和高维传感器输入上性能下降。第三类是**检索增强生成（RAG）方法**，本文的RAG-HAR+属于此类。与先前工作RAG-HAR相比，RAG-HAR+的改进在于：1）使用LLM引导的离线检索设计器Agent从多样化特征池中构建数据集特定特征组，替代固定统计视图；2）采用检索优先策略，对强证据样本直接通过邻居投票分类，仅将模糊案例交由LLM模糊解析器Agent处理，从而显著降低LLM调用次数、令牌消耗和推理时间。此外，RAG-HAR+还扩展了移动端原型，验证了在边缘部署场景中检索优先、LLM辅助的HAR方案的可行性。

### Q3: 论文如何解决这个问题？

RAG-HAR+通过引入检索优先和成本优化的架构来解决传统HAR方法依赖数据集特定训练、大量标注数据和频繁模型适配的问题。其核心方法是将HAR重构为无需训练、检索增强的任务，主要包含两大创新组件。

整体框架分为离线设计和在线推理两个阶段。在离线阶段，**Retrieval Designer Agent**利用LLM从包含统计、时间、频谱、运动强度和信号形状的候选特征池中，通过多轮迭代优化为每个数据集设计三个互补的特征组。每轮迭代中，Agent根据验证集上的检索F1分数和RAG命中率反馈，生成改进提示来调整特征选择，最终得到数据集特定的最优特征组配置。

在线推理阶段采用**检索优先策略**。首先对查询窗口计算三个特征组的向量，通过多向量检索和加权重排序获取Top-q近邻。关键创新在于**选择性回退机制**：当近邻标签多数投票结果唯一时直接输出预测，仅当出现平局（多个标签得票相同）时才将样本路由至**Ambiguity Resolver Agent**进行LLM推理。这种设计大幅减少了LLM调用次数，同时保持了对困难样本的推理能力。

技术实现上，RAG-HAR+通过Z-score标准化和滑动窗口预处理传感器数据，使用近似最近邻搜索进行高效检索，并通过验证集网格搜索优化各特征组的检索权重。整个框架无需训练或微调深度学习模型，仅需配置检索管道参数。

### Q4: 论文做了哪些实验？

论文在6个公开HAR基准数据集上评估了RAG-HAR+：USC-HAD、PAMAP2、MHEALTH、GOTOV、HHAR和Skoda，涵盖单IMU、多位置体戴传感器、智能手表和高维工业传感器阵列等场景。实验遵循与RAG-HAR相同的预处理、窗口化、索引和测试协议以保证公平比较。对比方法包括非LLM基线（如Triplet LSTM、DeepConvLSTM、ADFE等）和LLM基线（如Sensor-LLM、HARGPT、RAG-HAR等）。主要结果：RAG-HAR+在USC-HAD（F1 60.12）、MHEALTH（F1 98.19）、HHAR（F1 61.02）和Skoda（F1 97.74）上超越RAG-HAR，在PAMAP2（F1 90.60）和GOTOV（F1 75.97）上略低但保持竞争力。关键数据指标：RAG-HAR+将在线LLM token使用量从220.8M降至5M（减少97.7%），每样本token和推理延迟大幅降低。离线特征设计阶段总token仅132,176（约$0.075）。检索投票贡献了大部分F1，歧义解析器仅提升0.1-3.3个百分点。

### Q5: 有什么可以进一步探索的点？

RAG-HAR+在降低LLM调用成本方面表现优异，但仍存在若干可探索的方向。首先，其检索质量高度依赖预定义的特征池和离线设计的特征组，但特征组的设计仅基于数据集整体统计，未考虑不同活动类别间的特征差异，未来可引入类别级或样本级的自适应特征选择机制。其次，当前模糊判定仅依赖多数投票的平局情况，可探索更精细的不确定性量化方法（如检索邻居的置信度分布或特征空间距离），以更准确地决定何时调用LLM。此外，论文仅评估了单一LLM（gpt-5-mini），未来可研究不同规模或开源LLM在边缘部署中的成本-性能权衡。最后，当前原型仅验证了移动场景的可行性，但未深入分析实时流式数据下的延迟和能耗，可进一步优化检索索引结构（如分层索引或近似最近邻搜索）以降低内存和计算开销，并探索模型压缩或知识蒸馏技术以适配更受限的边缘设备。

### Q6: 总结一下论文的主要内容

本文提出RAG-HAR+，一种面向边缘部署的、基于检索增强生成（RAG）的、低成本人体活动识别（HAR）框架。核心贡献在于将LLM的使用从在线分类器重构为两阶段过程：离线阶段，一个检索设计智能体（Retrieval Designer Agent）利用LLM为每个数据集自适应地设计紧凑的多向量特征组（统计、时域、频域、信号形状），以提升检索表征的判别力；在线阶段，仅当检索邻居的多数投票结果不明确时，才调用LLM作为模糊解析智能体（Ambiguity Resolver Agent）进行决策。该方法解决了现有RAG-HAR中固定检索特征和每样本均需LLM推理的高成本问题。在六个HAR基准数据集上，RAG-HAR+在保持或提升性能的同时，将在线LLM调用量减少了89.3%-99.9%，显著降低了令牌消耗和推理延迟。该工作证明了“检索优先、LLM辅助”的HAR范式在资源受限的边缘设备上的可行性与高效性，为训练免费、可泛化的低成本HAR部署提供了新路径。
