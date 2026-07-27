---
title: "When Language Models Meet NeuroGraphs: Exploring Enhanced Agentic LLM Framework Towards Brain Network Analysis"
authors:
  - "Jiaxing Li"
  - "Rui Dong"
  - "Muyao Tang"
  - "Youyong Kong"
date: "2026-07-24"
arxiv_id: "2607.22082"
arxiv_url: "https://arxiv.org/abs/2607.22082"
pdf_url: "https://arxiv.org/pdf/2607.22082v1"
categories:
  - "cs.MA"
tags:
  - "Agentic LLM"
  - "时间序列报告"
  - "可解释诊断"
  - "知识检索增强"
  - "反思与验证"
  - "图到语义描述"
  - "脑网络分析"
  - "多步推理"
relevance_score: 8.5
---

# When Language Models Meet NeuroGraphs: Exploring Enhanced Agentic LLM Framework Towards Brain Network Analysis

## 原始摘要

Brain network analysis is crucial for understanding cognition and neurological disorders, yet existing deep learning methods mainly treat connectome analysis as a graph-to-logit classification problem, offering limited explanatory reasoning. Large language models (LLMs) provide a promising interface for knowledge-intensive scientific analysis, but directly applying general-purpose LLMs to brain networks remains challenging due to the structure-language gap, limited neuroscience grounding, and overconfident positive predictions. In this paper, we propose \textbf{BrainAgent}, an agentic LLM framework for knowledge-enhanced brain network analysis. BrainAgent reformulates connectome classification as an iterative process of topology-aware understanding, external retrieval, reasoning, and reflection. Specifically, it first converts raw brain networks into compact multi-level structural descriptions through brain-specific analysis tools, then retrieves relevant neuroscience knowledge and task-specific cases to ground the reasoning process, and finally generates structured predictions with reflective verification. Experiments on four public rs-fMRI datasets show that BrainAgent consistently improves different closed-source and open-source LLM backbones over direct prompting and standard reasoning baselines. Further ablation and interpretability analyses demonstrate the effectiveness of each component and show that BrainAgent produces more comprehensive, multi-level, and verifiable explanations.These results indicate that agentic LLMs provide a practical route toward interpretable and knowledge-grounded brain network analysis.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

脑网络分析对于理解认知功能和神经系统疾病至关重要，但现有深度学习方法主要将连接组分析视为一个“图到类别”的分类问题，提供有限的解释性推理。尽管大语言模型（LLM）为知识密集型科学分析提供了有前景的接口，但直接将通用LLM应用于脑网络面临三大挑战：首先，存在结构-语言鸿沟，即非欧几里得图结构（包含全局拓扑、社区组织和区域语义）难以被线性文本输入有效表征；其次，存在领域知识鸿沟，通用LLM缺乏神经影像学证据的显式支撑，可能生成生物学上不合理的解释；最后，存在正向预测偏差，直接提示的LLM倾向于过度预测疾病类别，导致高灵敏度但低特异度，这在医学筛查场景中尤为不利。为此，本文提出BrainAgent，一个针对脑网络分析的智能体LLM框架。它将连接组分类重新定义为拓扑感知理解、外部知识检索、推理与反思的迭代过程，旨在通过工具增强的交互和领域知识检索，弥合结构-语言与领域知识鸿沟，并缓解预测偏差，从而实现可解释、知识驱动的脑网络分析。

### Q2: 有哪些相关研究？

相关研究主要分为三类：

1. **传统图神经网络方法**：如GNNs和标准化的脑网络GNN基准，将脑网络分析视为有监督的图分类任务，学习判别性图表示。本文指出其局限性在于缺乏可解释性、泛化能力差，仅能提供事后显著性或区域可视化。

2. **LLM增强范式**：如BrainPrompt利用LLM生成多级提示增强传统GNN，BrainGFM通过图掩码自编码和对比学习将基础模型思想迁移到图预训练。这些方法虽改进了表示学习，但未将LLM作为交互式推理引擎直接分析个体脑图。

3. **通用Agent框架**：如检索增强生成（RAG）和工具使用框架（ReAct），允许LLM与外部环境交互。本文指出直接应用这些框架到脑网络分析不足，因为所需证据是图结构、个体特异且受生物学约束的。

本文提出的BrainAgent是首个针对脑网络的专用Agent框架，通过拓扑感知理解、神经科学知识检索、案例检索和反思机制，将脑网络分析重构为迭代推理过程，弥补了上述方法的可解释性、知识融合和校准性缺陷。

### Q3: 论文如何解决这个问题？

BrainAgent通过一个智能体LLM框架将脑网络分析重构为迭代推理过程，核心方法包括三个模块：理解模块、多轮智能体迭代模块和反思验证模块。

首先，理解模块将原始脑网络转换为紧凑的多层级结构描述。它通过将脑网络序列化为三元组（源区域、目标区域、连接强度），并按节点度排序保留拓扑重要性。随后调用分析函数提取通用图属性（度、密度、聚类系数）和脑网络特定属性（小世界性、全局效率），生成区域级、子图级和图级特征，减少token消耗并增强拓扑感知。

其次，多轮智能体迭代模块采用“思考-报告-行动-观察”循环。每轮中，LLM先推理当前上下文，生成简洁报告总结关键信息，通过路由器选择外部工具（脑网络分析函数、神经科学知识检索HARK、任务案例检索CARD），并将工具返回的观察融入下一轮推理。HARK通过层级检索（先基于脑区重叠的粗检索，再基于语义相似度的细检索）从权威知识库中获取领域知识；CARD则通过双模态相似度（图编码器提取的图级相似度与文本报告相似度的加权融合）检索历史案例，提供上下文证据。

最后，分析阶段包含反思模块：验证预测标签是否与图证据、检索知识和历史案例一致，若存在矛盾或过度自信则要求LLM修正，最终输出结构化结果（预测标签、支持理由、置信度）。创新点在于将脑网络分析从黑盒分类转为可解释的知识驱动推理，通过工具调用、外部知识检索和反思机制弥补通用LLM与脑网络分析之间的结构-语言鸿沟和领域知识缺失。

### Q4: 论文做了哪些实验？

论文在四个公开rs-fMRI脑网络数据集（ABIDE、ADHD、HCP、Rest-meta-MDD）上进行了实验，每个数据集均为二分类任务，包含90个脑区。实验设置中，20%样本作为测试集，其余用于检索库构建。对比方法包括直接提示（Direct）、思维链（CoT）、反思（Reflection）以及提出的BrainAgent框架。使用闭源模型（DeepSeek v3.2、Qwen3 Max、Gemini 3.1）和开源模型（Qwen3.5-35B、Qwen3.5-9B、Gemma4-26B）作为骨干，评估指标为准确率、召回率和精确率，并报告pass@1和pass@3结果。主要结果显示：直接提示存在严重正类预测偏差（召回率接近100%但准确率低），CoT改进有限，Reflection有一定效果，而BrainAgent在所有数据集和骨干模型上显著提升准确率和精确率。例如，在ABIDE上，Gemini 3.1的BrainAgent pass@1准确率达70.25%（直接提示为59.35%），pass@3达82.93%。消融实验表明，移除任何组件（理解、HARK、CARD、反思）均导致性能下降，其中移除CARD或反思影响最大。此外，BrainAgent在多个最新LLM（如GPT 5.3、Grok 4）上均能提升精确率，证明其作为通用即插即用框架的有效性。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：仅依赖AAL图谱的90个脑区，未探索不同图谱或高分辨率连接；pass@1准确率仍有限，说明无训练LLM在专业任务上存在瓶颈；仅处理二分类任务，未扩展到多分类或回归。未来可从以下方向探索：1) 引入多图谱融合或多模态数据（如结构MRI、基因表达），增强拓扑描述；2) 结合轻量级微调（如LoRA）或知识蒸馏，在保持可解释性的同时提升pass@1性能；3) 设计动态检索策略，根据样本难度自适应调用外部知识；4) 扩展到疾病亚型分类、治疗反应预测等更复杂临床任务；5) 集成因果推理模块，从脑网络差异中挖掘潜在生物标志物。

### Q6: 总结一下论文的主要内容

本文提出BrainAgent，一种面向脑网络分析的智能体LLM框架。核心贡献在于将脑连接组分类重新定义为迭代推理过程，包括拓扑感知理解、外部知识检索、推理与反思，以解决通用LLM直接应用于脑网络时的结构-语言鸿沟、领域知识缺失和正向预测偏差问题。方法上，BrainAgent首先通过脑专用分析工具将原始脑网络转化为多层级结构描述，然后检索相关神经科学知识和任务案例以支撑推理，最后生成结构化预测并辅以反思验证。在四个公共rs-fMRI数据集上的实验表明，BrainAgent显著优于直接提示和标准推理基线，能提升预测性能、减少正向预测偏差，并产生更全面、多层次且可验证的解释。该工作的重要意义在于证明了智能体LLM为实现可解释、知识驱动的脑网络分析提供了实用路径。
