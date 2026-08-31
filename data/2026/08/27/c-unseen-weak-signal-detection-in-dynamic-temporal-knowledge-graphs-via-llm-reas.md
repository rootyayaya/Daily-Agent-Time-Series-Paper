---
title: "C-Unseen: Weak Signal Detection in Dynamic Temporal Knowledge Graphs via LLM Reasoning"
authors:
  - "Yassir Lairgi"
  - "Ludovic Moncla"
  - "Khalid Benabdeslem"
  - "Rémy Cazabet"
  - "Pierre Cléau"
date: "2026-08-27"
arxiv_id: "2608.26870"
arxiv_url: "https://arxiv.org/abs/2608.26870"
pdf_url: "https://arxiv.org/pdf/2608.26870v1"
categories:
  - "cs.AI"
  - "cs.CL"
  - "cs.SI"
tags:
  - "Dynamic Temporal Knowledge Graphs"
  - "Weak Signal Detection"
  - "LLM Reasoning"
  - "Chain-of-Thought"
  - "Rare Subgraph Extraction"
  - "Temporal Persistence Tracking"
  - "Self-Interpretable Framework"
relevance_score: 6.5
---

# C-Unseen: Weak Signal Detection in Dynamic Temporal Knowledge Graphs via LLM Reasoning

## 原始摘要

Weak signals are early, low-visibility indicators that precede significant changes before those changes become established. Existing detection methods, based on keyword frequency, topic modeling, or untyped graph topology, fail to capture the semantic and relational structure through which such signals manifest. In this paper, we propose C-Unseen, a self-interpretable framework for weak signal detection in Dynamic Temporal Knowledge Graphs (DTKGs). We define a weak signal as a rare, semantically coherent subgraph that proliferates across consecutive TKG snapshots. The framework operates through two modules: a Rare Subgraphs Extractor, in which an LLM identifies subgraphs whose content is in tension with the dominant snapshot narrative via chain-of-thought reasoning, and a Weak Signal Alerter, in which the persistence of these rare subgraphs is tracked across time steps to isolate true weak signals. Experimental results demonstrate that C-Unseen outperforms keyword-, topic-, and graph-based baselines.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

弱信号检测是战略决策中的关键问题，指在重大变化完全显现前捕捉其早期、低可见性的征兆。现有方法主要分为三类：基于关键词频率的方法仅统计词项分布，无法捕捉实体间语义关联；基于主题建模的方法将文档简化为主题分布，丢失了丰富的领域知识；基于图拓扑的方法虽能建模结构演化，但仅适用于无类型图，无法表达命名实体、类型化关系及语义演化过程。尽管动态时序知识图谱（DTKG）能同时保留语义与时间信息，但将其应用于弱信号检测面临两大挑战：一是构建DTKG传统上依赖领域特定流程和大量人工标注；二是现有TKG推理方法偏向频繁模式，聚焦链接预测而非新兴信号识别。本文首次提出DTKG中弱信号的形式化定义——一种在连续快照中增殖的稀有语义连贯子图，并构建C-Unseen框架，通过LLM链式推理提取与主导叙事相悖的稀有子图，再跨时间步追踪其持续性以识别真实弱信号，从而弥合了语义结构建模与动态演化检测之间的鸿沟。

### Q2: 有哪些相关研究？

相关研究主要分为四类：

**1. 关键词频率类方法**：早期工作基于TF-IDF提取候选关键词，通过低出现频率（DoV）和高增长率（DoD）双重标准识别弱信号，并投影到BCG矩阵辅助解释。本文指出这类方法丢失了词语的上下文语义。

**2. 主题建模类方法**：假设弱信号是与主流主题不相交的小簇，采用LDA及其动态扩展、主题链追踪，以及BERTopic/BERTrend等Transformer模型。本文认为这些方法停留在主题粒度，无法捕捉主题内实体间的关联结构。

**3. 图结构类方法**：早期构建关键词共现图，利用介数、度中心性、最小生成树、3-clique和密度指标检测结构异常；BEAM框架枚举图元（graphlets）并追踪其计数序列的速度与加速度。本文指出这些方法基于同质无类型图，未利用实体和关系的语义类型。

**4. TKG推理与LLM方法**：RE-GCN等链路预测模型通过邻域聚合稀释了稀疏交互，DPCL-Diff假设新事件与旧事件相似，LLM-DA和GenTKG偏向频繁模式，均缺乏针对弱信号的稀有性评分机制。

**本文区别**：C-Unseen首次在动态时序知识图谱中定义弱信号为“跨快照增殖的稀有语义一致子图”，利用LLM链式推理识别与主流叙事冲突的子图，并跟踪其时间持续性，同时克服了上述四类方法在语义、关系结构、类型化和稀有性检测上的局限。

### Q3: 论文如何解决这个问题？

C-Unseen提出了一种基于LLM推理的自解释框架，用于在动态时序知识图谱（DTKG）中检测弱信号。其核心创新在于将弱信号定义为“在连续快照中持续存在且语义连贯的稀有子图”，并通过两个模块实现检测。

**整体框架**：输入为DTKG快照序列，每个快照由带类型实体、关系和五元组（含有效性周期）构成。框架通过两个模块协同工作，利用LLM的链式推理（CoT）能力完成检测。

**模块一：稀有子图提取器**。首先将快照中所有五元组以索引列表形式（主语实体名:类型→谓词(起止时间)→宾语实体名:类型）提示给LLM。LLM分两步推理：第一步生成快照的基线叙事摘要；第二步将每个五元组与基线对比，识别内容与主导叙事相冲突的稀有子图，并排除标签不匹配等数据伪影。随后通过广度优先搜索构建连接子图，保留稀有子图间的结构上下文，其余部分丢弃。

**模块二：弱信号警报器**。将当前连接子图与历史快照的连接子图以相同文本形式提示给LLM。LLM先总结每个历史快照的主题及其稀有五元组的潜在暗示，再判断当前子图是否延续了先前的张力线索。若内容推进了先前存在的冲突，则标记为弱信号，并写回记忆供后续参考，同时已标记的弱信号在后续快照中不再重复展示。

**关键技术**：采用双时间建模区分观测时间与事实有效周期；利用CoT增强LLM推理的可解释性；通过记忆机制实现跨时间步的线索追踪。创新点在于将弱信号检测从关键词/主题/图拓扑层面提升到语义与关系结构层面，且框架完全自解释，无需人工标注。

### Q4: 论文做了哪些实验？

论文构建了首个弱信号检测基准Wiki-OpenAI，基于OpenAI维基百科2015-2025年的773条原子事实（含16条人工补充），标注了5个强信号及22个弱信号、10个佐证事实。实验设置11个年度快照，使用gpt-5.4-mini作为LLM后端，并构造了实体匿名化的Wiki-OpenAI-Anon变体以排除预训练知识影响。

对比方法包括Yoon（关键词）、BERTrend（主题）和BEAM（图结构）三种基线。在检测精度上（RQ1），采用共享锚词匹配阈值k∈{1,2,3}评估，C-Unseen在k=2和k=3时F1最高（0.432和0.271），k=1时覆盖全部5个信号，而BEAM在k=3时无法覆盖任何信号。匿名化后C-Unseen性能仅小幅下降（k=1时F1从0.613降至0.603），证明其依赖结构冲突而非实体知识。

提前量评估（RQ2）显示，C-Unseen在k=3时平均提前1.00年检测，虽低于BERTrend的1.70年，但覆盖4.2个信号（BERTrend仅1.4个），表明其跨信号检测一致性更优。定性分析（RQ3）以SS_DEFENCE_TURN_2025为例，C-Unseen输出带自然语言解释的子图，揭示政策限制与国防利益的结构性张力，而基线仅输出孤立关键词或词袋。消融实验（RQ4）验证了稀有子图提取器和弱信号告警器两个模块的贡献。

### Q5: 有什么可以进一步探索的点？

C-Unseen在弱信号检测上展现了创新性，但仍有几个关键局限值得深入探索。首先，其核心瓶颈在于LLM上下文窗口对大规模DTKG的约束，未来可借鉴图采样或层次化摘要技术，先对快照进行结构压缩，再引导LLM聚焦于高潜力子图区域，而非全量输入。其次，DTKG构建依赖ATOM的few-shot方式，缺乏领域本体约束，容易引入噪声三元组，后续可探索将领域知识图谱或本体规则嵌入ATOM的生成过程，以提升子图提取的精确性。第三，当前基准仅基于单一组织（Wiki-OpenAI），泛化性存疑，未来应在多领域（如金融、医疗）构建标注数据集，并测试跨域迁移能力。此外，弱信号的定义依赖“语义张力”和“跨快照持续性”，但“张力”的量化标准仍较模糊，可尝试引入对比学习或异常度评分来增强可解释性。最后，当前框架对时间动态的建模较浅，未来可结合时序点过程或状态空间模型，捕捉弱信号演变的非线性节奏，从而提升预警的时效性。

### Q6: 总结一下论文的主要内容

C-Unseen提出了一种基于大语言模型推理的弱信号检测框架，用于动态时序知识图谱（DTKG）中的早期预警。弱信号被定义为在连续时间快照中罕见但语义连贯、且持续增殖的子图，其出现往往预示重大变化。现有方法依赖关键词频率、主题模型或未类型化图拓扑，无法捕捉信号背后的语义与关系结构。该框架包含两个模块：罕见子图提取器利用LLM的链式思考推理，识别与快照主导叙事相冲突的内容；弱信号警报器则跨时间步追踪这些罕见子图的持续性，以区分真实弱信号。实验表明，C-Unseen在Wiki-OpenAI基准上优于基于关键词、主题和图的方法，且输出具有自解释性，并在实体匿名化变体上保持性能。该工作为DTKG中的弱信号检测提供了新范式，兼具语义理解与可解释性，但未来需解决大规模快照的上下文窗口限制及跨领域泛化问题。
