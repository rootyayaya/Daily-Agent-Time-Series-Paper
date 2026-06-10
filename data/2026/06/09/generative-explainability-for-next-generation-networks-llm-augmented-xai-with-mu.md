---
title: "Generative Explainability for Next-Generation Networks: LLM-Augmented XAI with Mutual Feature Interactions"
authors:
  - "Kiarash Rezaei"
  - "Omran Ayoub"
  - "Sebastian Troia"
  - "Francesco Lelli"
  - "Paolo Monti"
  - "Carlos Natalino"
date: "2026-06-09"
arxiv_id: "2606.10942"
arxiv_url: "https://arxiv.org/abs/2606.10942"
pdf_url: "https://arxiv.org/pdf/2606.10942v1"
categories:
  - "cs.NI"
  - "cs.AI"
  - "cs.LG"
tags:
  - "LLM-augmented XAI"
  - "自然语言报告生成"
  - "特征交互"
  - "SHAP"
  - "网络故障诊断"
  - "可解释时间序列"
  - "可解释性"
  - "QoT估计"
relevance_score: 7.5
---

# Generative Explainability for Next-Generation Networks: LLM-Augmented XAI with Mutual Feature Interactions

## 原始摘要

As artificial intelligence and machine learning (AI/ML) models become integral to network operations, their lack of transparency poses a significant barrier to operator trust. Existing explainable artificial intelligence (XAI) techniques often fail to bridge this gap for non-specialists, producing technical outputs that are difficult to translate into actionable insights. This paper presents a framework specifically designed to address this shortcoming. It leverages a moderately sized large language model (LLM) and extends beyond the standard use of SHapley Additive exPlanations (SHAP) feature influence values. The framework employs a structured prompt enriched with mutual feature interaction data to generate human-understandable natural language explanations. To validate our framework, we performed an empirical evaluation on an optical quality of transmission (QoT) estimation use case with human evaluators. We collected independent performance evaluations from specialists, which showed a high inter-evaluator agreement. Compared to a state-of-the-art baseline that uses only SHAP feature influence values in a straightforward prompt, our approach improves the explanation usefulness and scope by 12.2% and 6.2%, while achieving 97.5% correctness.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着人工智能和机器学习模型在网络运营中的广泛应用，其缺乏透明度成为阻碍运营商信任的主要障碍。现有可解释人工智能（XAI）技术，如SHAP，虽能提供特征重要性排名，但其输出形式高度技术化，包含大量原始多维数据（如特征影响值和交互值），需要深厚的领域知识和XAI专业知识才能解读，难以转化为非专业人士可理解的、可操作的见解。这导致工程师在模型做出反直觉决策（如拒绝看似可行的光路）时，无法快速理解其背后的逻辑，从而难以判断决策是基于有效模式还是模型错误。本文旨在解决这一核心问题：弥合技术性XAI输出与人类可理解、可操作解释之间的鸿沟。为此，论文提出一个框架，利用中等规模的大语言模型（LLM），通过结合SHAP特征影响值和互特征交互值的结构化提示，生成自然语言解释。该框架以光网络传输质量（QoT）估计为案例，旨在让网络工程师无需深入技术细节即可理解模型决策，从而提升信任度、支持人工验证或干预，最终实现更安全高效的网络运营。

### Q2: 有哪些相关研究？

相关研究主要集中在利用大语言模型（LLM）增强可解释人工智能（XAI）领域，尤其关注将SHAP值等技术输出转化为自然语言解释。Zeng等人展示了LLM能有效将SHAP值翻译为自然语言解释，在医疗等应用领域表现出接近人类水平的解释能力。在通信网络领域，有研究将LLM与SHAP结合用于网络自动化系统的可解释性，例如提出结合异常检测、SHAP根因分析和LLM生成纠正动作的管道用于6G微服务环境管理。然而，这些工作存在局限：评估依赖自动指标（如BERT、ROUGE）而非人工评估，且使用传统LLM（如Llama2-70B、ChatGPT 3.5-175B）缺乏推理能力，仅依赖孤立SHAP值，忽略了特征交互信息。在光传输质量（QoT）估计场景中，ChatGPT 3.5通过直接提示和自我反思仅达到65%的正确率。本文与这些工作的区别在于：首次引入推理型LLM（中等参数规模）替代传统LLM，并创新性地在结构化提示中融入SHAP互特征交互值，超越了仅使用单一SHAP值的基线方法。通过人工评估验证，本文方法在解释有用性、范围和正确性上分别提升12.2%、6.2%和97.5%，弥补了现有工作在特征交互和推理能力上的不足。

### Q3: 论文如何解决这个问题？

该论文提出了一种结合大语言模型（LLM）与可解释人工智能（XAI）的框架，旨在为网络运维人员生成自然语言形式的可理解解释，解决传统XAI技术输出过于技术化、难以转化为可操作洞察的问题。

核心方法包括四个模块：AI/ML模型、XAI方法、解释增强模块和仪表盘。首先，AI/ML模型采用XGBoost进行光路传输质量（QoT）估计，输出误码率预测值。其次，XAI方法使用SHAP计算局部特征贡献值（Shapley值），不仅量化单个特征的重要性，还捕捉特征对之间的相互交互作用（即联合影响）。解释增强模块是核心创新点：它设计了一个结构化提示词，将模型预测、SHAP特征影响值以及特征交互分数共同输入到一个中等规模的LLM中。该提示词通过引导LLM将技术性数值转化为人类可读的自然语言解释，从而弥补了数值输出与操作决策之间的鸿沟。最后，仪表盘将SHAP特征影响图、交互矩阵、模型输出与LLM生成的文本解释整合展示，便于专家审查。

关键技术在于利用特征交互信息丰富提示词内容，使LLM能够理解特征间的非线性联合效应，从而生成更准确、更有用的解释。实验表明，与仅使用SHAP特征影响值的基线方法相比，该框架在解释有用性上提升12.2%，解释范围提升6.2%，且正确率达97.5%。整体框架具有模型无关性，可推广至其他AI/ML任务。

### Q4: 论文做了哪些实验？

论文基于光传输质量（QoT）估计场景进行了实证评估。实验设置包括：使用XGBoost回归模型，从数据集中选取12个最具代表性的特征（涉及路径长度、调制格式、线路速率等），按90:10划分训练集和测试集，模型MSE为0.0000、MAE为0.0001。随机抽取40个局部SHAP解释用于实验，采用32.8B参数的4-bit量化版DeepSeek-R1作为LLM，基线方法仅使用SHAP特征影响值进行简单提示。对比方法为仅用SHAP值的基线提示策略，主要结果通过两位独立专家评估（随机顺序、双盲），采用三个指标：正确性（97.5% vs 96.3%）、范围（95.0% vs 88.8%）和有用性（4.38 vs 3.77，满分5）。专家间一致性高：正确性一致率95%（基线93%），范围一致率90%（基线83%）。结果表明，融合互特征交互数据与结构化提示的框架在解释范围上提升6.2%，有用性提升12.2%，正确性提升1.2%。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：1）仅依赖SHAP计算特征交互，计算成本高，难以扩展至大规模网络场景；2）评估仅针对光传输质量估计单一用例，泛化性不足；3）LLM生成的解释虽自然但可能遗漏关键因果逻辑，且未验证对非专家用户的长期信任影响。

未来可探索方向：1）引入LIME或梯度类方法替代SHAP，降低计算开销，同时探索特征交互的近似计算策略；2）设计多任务评估框架，覆盖网络故障诊断、资源调度等更多场景；3）结合因果图或结构方程模型，使LLM解释不仅基于相关性，还能揭示因果机制；4）开发交互式解释系统，允许用户追问并动态更新解释，提升实用性；5）研究LLM解释的鲁棒性，防止对抗性扰动导致误导性输出。

### Q6: 总结一下论文的主要内容

该论文提出一个面向下一代网络的生成式可解释性框架，旨在解决AI/ML模型在运维中缺乏透明度、传统XAI技术输出难以被非专家理解的问题。核心贡献在于：利用中等规模大语言模型（LLM），并超越标准SHAP特征影响值，通过设计包含特征交互信息的结构化提示词，生成人类可理解的自然语言解释。在光传输质量（QoT）估计用例上，经专家评估，该方法相比仅使用SHAP值的基线，解释有用性提升12.2%，范围提升6.2%，正确性达97.5%。主要结论表明，结合特征交互感知上下文的提示词能显著提升解释质量，有助于实现AI/ML模型在真实部署中的可扩展可解释性和信任度。
