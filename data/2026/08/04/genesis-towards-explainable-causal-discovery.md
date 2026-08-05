---
title: "GENESIS: Towards Explainable Causal Discovery"
authors:
  - "Abhinav Thorat"
  - "Ravi Kumar Kolla"
  - "Vishak K Bhat"
  - "Harsh Vardhan Singh Chauhan"
  - "Niranjan Pedanekar"
date: "2026-08-04"
arxiv_id: "2608.03868"
arxiv_url: "https://arxiv.org/abs/2608.03868"
pdf_url: "https://arxiv.org/pdf/2608.03868v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Causal Discovery"
  - "LLM-assisted hybrid methods"
  - "Decision Traceability"
  - "Explainable AI"
  - "Markov Blanket"
  - "Domain Knowledge Integration"
  - "Graph Construction"
  - "Structural Motifs"
  - "Time Series Analysis"
  - "Interpretable Decision Points"
relevance_score: 7.5
---

# GENESIS: Towards Explainable Causal Discovery

## 原始摘要

Causal Discovery (CD) from observational data faces two fundamental challenges. First, purely statistical methods often lack the power to resolve structural ambiguities in low-sample regimes. Second, although LLM-assisted hybrid approaches improve structure recovery through semantic reasoning, the influence of that reasoning on individual edge decisions remains largely opaque. Consequently, existing hybrid methods fail to satisfy a fundamental requirement: explaining why a particular edge is included or excluded in the learned directed acyclic graph (DAG). This is critical in real-world applications, where no ground-truth DAG exists and every structural decision must be independently justified. We formalize this requirement as decision traceability, requiring every inferred edge to be supported by auditable statistical evidence, Markov Blanket consistency, or explicit domain reasoning. We propose GENESIS, an explainable hybrid CD framework that decomposes graph construction into interpretable decision points. GENESIS first identifies and scores three-node structural motifs, including chains, forks, and colliders, to establish transparent structural priors, then progressively refines the graph by integrating these priors with observational evidence, invoking domain knowledge only when statistical evidence is insufficient. By design, every edge decision is resolved through an auditable source of evidence. Experiments show that GENESIS achieves 100% decision traceability across all settings, establishing explainability as a first-class objective in causal discovery. Despite this additional requirement, GENESIS consistently outperforms purely statistical CD methods on the majority of benchmark datasets across all sample regimes in terms of Structural Hamming Distance (SHD), while achieving performance comparable to state-of-the-art LLM-assisted approaches.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

本文聚焦于因果发现（Causal Discovery, CD）中一个被长期忽视的核心问题：决策可追溯性（decision traceability）。研究背景在于，从观测数据中恢复因果图是干预推理和根因分析的基础，但现有方法存在两大不足。其一，纯统计方法（如PC、NOTEARS、LiNGAM等）在低样本量下难以解决结构歧义，且其边级决策过程不透明——约束方法缺乏对检验成败的显式解释，评分方法优化全局目标却无法说明单条边的取舍依据。其二，新兴的LLM辅助混合方法虽能利用语义先验提升结构恢复效果，但将语义推理与统计证据紧密耦合，无法区分某条边是来自数据支撑、语义先验还是模型预训练知识，导致最终DAG缺乏可审计性。这在无真实因果图的实际应用中尤为致命，因为每个结构决策都必须能独立辩护。为此，本文形式化定义了决策可追溯性，要求每条推断边必须有可审计的统计证据、马尔可夫毯一致性或显式领域推理支持。基于此，提出GENESIS框架，将图构建分解为可解释的决策点：先识别并评分三节点结构基元（链、叉、对撞），再渐进整合统计证据与语义先验，仅在统计不足时调用领域知识。其核心目标是让可解释性成为因果发现的一等公民，而非事后附加，从而在保证100%决策可追溯的同时，不牺牲结构恢复精度。

### Q2: 有哪些相关研究？

相关研究主要分为两大类。**传统因果发现方法**包括基于约束的PC算法、基于评分的CaMML和NOTEARS，以及可识别函数模型如LiNGAM、DirectLiNGAM和SCORE。这些方法依赖统计检验或优化目标推断因果结构，但缺乏对边缘决策的透明解释，难以满足可审计性要求。GENESIS通过可解释的三节点结构（链、叉、碰撞器）逐步构建图，并用统计证据、马尔可夫毯一致性和领域知识渐进解决不确定边缘，从而实现了决策可追溯性。

**LLM辅助因果发现方法**是另一类相关工作，例如利用LLM推断变量因果顺序以约束结构学习，或通过LLM-CD从变量描述预测因果边/图结构作为先验。这些方法虽展示了语义知识的价值，但主要依赖成对边缘预测或全局排序假设，易受马尔可夫等价类歧义和语义先验与数据冲突的影响。GENESIS的独特之处在于生成三节点结构级假设，并逐步用观测数据验证，确保每条保留边缘同时获得语义推理和实证支持，形成完整可审计的决策链。此外，GENESIS将可解释性作为一等目标，在多数数据集上优于纯统计方法，性能与最先进的LLM辅助方法相当，这是现有工作未系统解决的。

### Q3: 论文如何解决这个问题？

GENESIS通过三阶段渐进式流水线解决因果发现中决策不可追溯的问题，将图构建分解为可审计的决策点。整体框架包含三个核心模块：

**LLM Explorer**：利用节点元数据M，通过LLM生成三类三节点结构基元（链、叉、对撞），每个基元附带语义置信度p(m|LLM)，最多提取5n个基元以控制复杂度。这些基元作为可解释的结构先验，比成对关系提供更丰富的约束信息。

**Data Explorer**：对观测数据D进行双重验证。边置信度通过加权融合四种统计信号（条件独立性检验、BIC评分、ANM和LiNGAM函数因果模型）计算；基元置信度则评估其隐含的条件独立约束是否与数据一致。随后通过组合分数s(e,m)融合LLM与数据证据，以低阈值λ_low保证召回率，识别出中间分数或证据冲突的不确定边集E₂。

**Edge Resolution**：对不确定边进行两级精化。首先通过马尔可夫毯一致性过滤——取数据驱动MB（IAMB算法）与LLM推导MB的交集，要求边的两端互在对方MB中；未解决的边进入反事实LLM裁决阶段，由假设LLM枚举五种竞争性结构解释（直接边、两种中介路径、长链、混淆结构），再由Judge LLM基于统计证据进行反事实推理，输出KEEP或DISCARD的二元决策。

创新点在于：以三节点基元作为LLM与统计证据融合的基本推理单元，通过渐进式验证确保每条边最终由统计证据、MB一致性或领域推理三类可审计证据之一支持，从设计上保证100%决策可追溯性。实验表明，在满足可解释性约束的同时，GENESIS在多数基准数据集上SHD指标优于纯统计方法，与最先进的LLM辅助方法性能相当。

### Q4: 论文做了哪些实验？

论文在五个标准贝叶斯网络基准数据集（Asia、Cancer、Child、Earthquake、Survey）上评估了GENESIS框架，这些数据集覆盖不同图规模和结构复杂度。实验设置包括从真实DAG生成1000、2500和5000个样本的观测数据，每个设置运行6次取均值±标准差。

对比方法分为两类：传统统计方法（PC、NOTEARS、SCORE、CaMML、Direct-LiNGAM）和LLM辅助方法（CausalOrder、LLM-CD、SLLM-CD）。评估指标为结构汉明距离（SHD）和决策可追溯性。

主要结果：GENESIS在所有设置下实现100%决策可追溯性，每条边都有明确证据来源（统计证据、马尔可夫毯一致性或LLM推理）。在SHD方面，GENESIS在多数基准数据集上优于所有纯统计方法，例如在Cancer数据集（n=5000）上SHD为0.00，而PC为2.00、NOTEARS为4.00；在Earthquake上同样达到0.00。与LLM辅助方法相比，GENESIS性能相当或更优，如Survey数据集上GENESIS为1.83，优于LLM-CD的1.50但接近CausalOrder的1.50。在复杂数据集Child上，GENESIS（6.67）显著优于SCORE（172.00）和Direct-LiNGAM（54.50），仅略逊于CaMML（1.67）。GENESIS在不同样本量下表现稳定，且随数据增加持续受益。

### Q5: 有什么可以进一步探索的点？

GENESIS将决策可追溯性作为因果发现的一等目标，但仍存在若干可探索方向。首先，其可解释性依赖于三节点基序（链、叉、对撞）的识别，但真实系统中高阶交互（如四节点环、隐变量导致的伪相关）难以被此类局部结构捕获，未来可扩展至更大规模子图或引入隐变量检测机制。其次，LLM领域知识仅在统计证据不足时调用，但“不足”的阈值设定缺乏自适应标准，可尝试基于不确定性量化（如贝叶斯置信区间）动态调整触发条件，减少人为干预。第三，当前决策溯源仅区分统计/马尔可夫毯/领域知识三类证据，未量化不同证据间的冲突程度，可设计证据融合评分函数，对矛盾信号进行加权仲裁。此外，GENESIS在基准数据集上的SHD优势尚不显著，可探索将决策可追溯性作为正则化项融入端到端神经因果发现，而非事后解释。最后，面向工业故障诊断，可引入时序干预反馈（如在线实验）来验证边缘决策的因果稳健性，形成“发现-解释-验证”闭环，提升实际部署中的可信度。

### Q6: 总结一下论文的主要内容

GENESIS提出了一种可解释的混合因果发现框架，旨在解决传统统计方法在低样本下结构歧义性高、以及LLM辅助方法决策过程不透明的问题。论文形式化了“决策可追溯性”需求，要求每条边的纳入或排除必须由统计证据、马尔可夫毯一致性或显式领域推理支持。方法上，GENESIS首先识别并评分三元结构基元（链、叉、对撞），建立透明结构先验，再逐步整合观测证据，仅在统计证据不足时调用领域知识。实验表明，GENESIS在所有设置下实现100%决策可追溯性，同时在多数基准数据集上优于纯统计方法，并与最先进的LLM辅助方法性能相当。其核心贡献在于将可解释性提升为因果发现的一等目标，在保证结构准确性的同时，为每个因果决策提供可审计的明确依据，对无真实图标注的工业故障诊断等实际应用具有重要意义。
