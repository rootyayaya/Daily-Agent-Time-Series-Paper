---
title: "TSRouter: Dynamic Modality-Model Selection for Time Series Reasoning"
authors:
  - "Fangxu Yu"
  - "Tao Feng"
  - "Dehai Min"
  - "Lu Cheng"
  - "Ge Liu"
  - "Tianyi Zhou"
date: "2026-07-09"
arxiv_id: "2607.08940"
arxiv_url: "https://arxiv.org/abs/2607.08940"
pdf_url: "https://arxiv.org/pdf/2607.08940v1"
github_url: "https://github.com/tianyi-lab/TSRouter"
categories:
  - "cs.LG"
tags:
  - "时间序列推理"
  - "动态路由"
  - "模态选择"
  - "模型选择"
  - "LLM"
  - "VLM"
  - "异构图"
  - "成本感知优化"
  - "零样本泛化"
  - "TSRouter"
relevance_score: 9.5
---

# TSRouter: Dynamic Modality-Model Selection for Time Series Reasoning

## 原始摘要

Time series reasoning is essential for real-world problem-solving. While both Large Language Models (LLMs) and Vision-Language Models (VLMs) can reason about time-series data, their capabilities are complementary: LLMs process time series as text sequences and thus preserve exact numerical understanding, but struggle with global patterns, whereas VLMs efficiently capture these patterns by visualizing time series but may lose fine-grained details. Moreover, models vary significantly in task-specific expertise and inference costs. Dynamically selecting the most suitable modality and model for each query is therefore crucial, yet challenging because it requires modeling the complex interactions among tasks, queries, modalities, and models, which carry rich contextual signals. To this end, we introduce TSRouter, a graph-based dynamic routing framework. TSRouter constructs a heterogeneous graph of task, query, modality, and model nodes to contextualize the interactions among query characteristics, modality attributes, and model capabilities. TSRouter formulates routing as a candidate scoring problem, where each modality-model pair is evaluated based on user-defined performance-cost preferences to select the optimal candidate. Comprehensive evaluations on 4 distinct time series reasoning tasks reveal that TSRouter substantially outperforms diverse baselines with 16\% to 46\% relative improvements. Furthermore, TSRouter demonstrates robust zero-shot plug-and-play generalization to unseen models and novel tasks and preserves high performance while reducing computational overhead through cost-aware optimization. Our code is available at https://github.com/tianyi-lab/TSRouter.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列推理在金融、医疗等高风险领域至关重要。现有方法主要依赖大语言模型（LLM）和视觉语言模型（VLM），但两者能力互补却各有局限：LLM将时间序列处理为文本序列，能保留精确数值但难以捕捉全局模式，且面临上下文长度瓶颈和高计算成本；VLM通过可视化高效捕获全局模式，却因图像分辨率限制丢失细粒度数值细节。此外，不同模型在特定任务上的专业性和推理成本差异显著。现有路由方法仅关注模型选择，忽略了模态选择这一关键维度，且最多只能建模一种交互关系（如查询-查询或查询-模型），无法联合建模任务、查询、模态和模型之间的复杂上下文交互，导致路由决策次优。因此，本文旨在解决如何为每个时间序列推理查询动态选择最合适的模态（文本或图像）和模型（LLM或VLM），以充分利用其互补优势，同时平衡性能与计算开销的核心问题。

### Q2: 有哪些相关研究？

在时间序列推理领域，相关研究主要分为三类。**方法类**包括LLMs/VLMs for Time Series，如通过提示和重编程适配LLM，或利用VLM将时间序列转为视觉图。本文指出LLM擅长精确数值理解，VLM擅长全局模式捕捉，但现有工作未动态联合选择模态与模型，TSRouter通过查询级路由实现互补。**评测类**包括LLM Router，如RouterKNN、RouterMLP、GraphRouter等，它们通过查询嵌入或分类器在固定输入模态下选择模型，但仅关注模型选择。本文超越这些方法，将路由扩展为联合模态-模型选择，例如GraphRouter将路由视为查询与模型节点的边预测，无法自然处理双维度选择。**应用类**包括LLM/VLM Reasoning，如提示方法、测试时计算扩展及强化学习内化推理能力，但训练成本高。TSRouter作为轻量级方案，位于LLM与VLM推理交叉点，以最小训练成本利用两者优势。总体而言，TSRouter通过图结构动态路由，在时间序列推理中实现性能与成本平衡，与现有方法在模态选择、联合优化及训练效率上存在显著区别。

### Q3: 论文如何解决这个问题？

TSRouter通过构建异构图动态路由框架解决时间序列推理中的模态-模型选择问题。核心方法是将路由形式化为候选评分问题，架构包含四个关键组件：首先，构建由任务节点、查询节点、模态节点和模型节点组成的异构图，所有节点特征通过预训练文本编码器初始化，其中查询节点融合了问题文本和时间序列统计摘要。其次，设计五种关系边：任务-查询边、查询-模态边、模态-模型边、查询-模型边以及基于余弦相似度的查询-查询边，使相似查询在消息传递中共享信息。然后，采用异构图表转换器（HGT）堆叠层进行表示学习，通过类型感知的多头注意力机制捕获不同节点间的结构化交互模式，并应用残差连接稳定优化。最后，通过元素级乘法融合查询与候选（模态+模型）表示，经两层MLP输出评分，训练时使用KL散度最小化预测分布与基于有效性分数（准确率与归一化成本的凸组合）的软目标分布之间的差异。创新点包括：1）首次联合建模任务、查询、模态和模型的复杂交互关系；2）支持成本感知优化，通过α参数平衡性能与计算开销；3）具备零样本泛化能力，新任务或新模型只需插入对应节点即可自动路由。实验表明该方法在四个推理任务上相对基线提升16%-46%。

### Q4: 论文做了哪些实验？

论文在TSRBench测试集上进行了实验，该测试集包含感知、推理、预测和决策4类时间序列推理任务，共15个子任务，4125个案例。数据按7:1:2划分为训练、验证和测试集。对比方法包括两类：基于规则的方法（选择最大LLM或VLM）和基于学习的方法（Hybrid LLM、RouterDC、CausalLMRouter、EloRouter、MFRouter、KNNRouter等）。主要评估指标为准确率和API成本（美元）。TSRouter在整体准确率上达到51.33%，相对所有基线提升16%-46%（如Hybrid LLM为44.07%），成本仅0.73美元。在泛化实验中，TSRouter对未见模型（新增Qwen3.5-397B-A17B和Kimi-K2.5）准确率提升至53.5%，对未见任务（相关性预测和插补）也全面领先（相关性预测准确率31.38%，插补MSE 0.56）。消融实验表明，去除异构图、查询-查询边、MLP评分头或模态-模型边均导致准确率显著下降（如整体准确率降至46.25%-48.55%）。超参数分析显示，2层GNN、嵌入维度64、k=60时性能最优。成本-准确率权衡实验表明，TSRouter在不同成本偏好下均能主导帕累托前沿。

### Q5: 有什么可以进一步探索的点？

TSRouter在动态路由方面取得了显著进展，但仍存在若干可探索的方向。首先，其异构图构建依赖预定义的节点和边关系，对于未见过的模态（如触觉信号）或新兴模型架构的泛化能力可能受限，未来可引入元学习或在线图结构更新机制。其次，当前路由决策主要基于任务-查询-模态-模型的静态特征，未充分利用历史路由反馈进行在线优化，可结合强化学习实现自适应策略调整。第三，成本感知优化仅考虑推理开销，未纳入模型训练或微调成本，在持续学习场景下可能不够高效。此外，论文实验集中于四个推理任务，对更复杂的多步推理或长序列预测场景的鲁棒性有待验证。改进思路包括：设计可动态扩展的异构图框架，支持新节点类型的自动接入；引入基于对比学习的跨模态表征对齐，提升路由对细粒度语义的捕捉能力；探索联邦学习环境下的分布式路由策略，平衡隐私与性能。

### Q6: 总结一下论文的主要内容

TSRouter 提出了一种面向时间序列推理的动态模态-模型选择框架。该框架针对大型语言模型（LLM）处理文本序列时保留精确数值但难以捕捉全局模式，而视觉语言模型（VLM）可视化时序数据时能高效捕获模式却可能丢失细节的互补性问题，通过构建包含任务、查询、模态和模型节点的异构图，建模四者间的复杂交互。TSRouter将路由选择转化为候选评分问题，基于用户定义的性能-成本偏好评估每个模态-模型对，从而动态选择最优组合。在4个不同的时间序列推理任务上，TSRouter相比多种基线方法实现了16%到46%的相对性能提升，并展现出强大的零样本泛化能力，能直接应用于未见过的模型和新任务，同时通过成本感知优化在保持高性能的同时降低计算开销。该工作为时间序列推理中的模态与模型动态选择提供了有效解决方案。
