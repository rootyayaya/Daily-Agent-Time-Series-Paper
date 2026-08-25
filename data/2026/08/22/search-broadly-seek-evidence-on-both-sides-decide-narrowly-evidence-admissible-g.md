---
title: "Search Broadly, Seek Evidence on Both Sides, Decide Narrowly: Evidence-Admissible GraphRAG for Longitudinal Clinical Event Verification"
authors:
  - "Xingtao Lin"
  - "Yubo Feng"
  - "Weixin Liu"
  - "Hangqi Ren"
  - "Junchao Zhou"
  - "Caiwan Sun"
  - "You Chen"
date: "2026-08-22"
arxiv_id: "2608.22062"
arxiv_url: "https://arxiv.org/abs/2608.22062"
pdf_url: "https://arxiv.org/pdf/2608.22062v1"
categories:
  - "cs.AI"
tags:
  - "GraphRAG"
  - "证据路由"
  - "事件验证"
  - "临床时间序列"
  - "可追溯诊断链"
  - "证据合约"
  - "时间序列报告"
  - "多源证据融合"
  - "LLM/Agent"
  - "医疗诊断"
relevance_score: 7.5
---

# Search Broadly, Seek Evidence on Both Sides, Decide Narrowly: Evidence-Admissible GraphRAG for Longitudinal Clinical Event Verification

## 原始摘要

Longitudinal clinical event-relation verification determines whether a patient record supports a specified relation among two or more clinical events. This task is challenging because evidence is distributed across structured records, notes, laboratory trajectories, encounters, and time, while negation, temporal mismatch, repeated documentation, and conflicting findings can make retrieved information appear relevant without establishing the relation.
  We present MedEventGraph-RAG, an evidence-admissible framework that represents event occurrences in a patient-specific graph and links each occurrence to source evidence, including structured rows, note spans, timestamps, and numerical trajectories. Given a verification query specifying events, relation, and clinical scope, the graph guides discovery of candidate event chains and retrieves evidence from both supporting and contradicting sides. A query-specific evidence contract filters information by patient identity, scope, occurrence binding, and source traceability before a separate assessor determines supported, conflicting, refuted, or insufficient outcomes.
  Across ten protocols on i2b2, n2c2, MIMIC-IV, and LUNGUAGE, MedEventGraph-RAG achieves balanced accuracies of 78.6, 67.3, and 96.8 on temporal, medication-adverse-event, and recorded-order verification, improving over the strongest matched baselines by 26.9, 4.9, and 30.4 points. Under evidence masking, it reaches 92.2 balanced accuracy with no false-support predictions. When intermediate events are hidden, it recovers complete source-traceable event chains in 57.9% of i2b2 and 70.0% of LUNGUAGE cases. These results show that separating broad evidence discovery from narrow evidence-admissible assessment improves longitudinal clinical verification and reduces unsupported conclusions.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

临床事件关系验证是电子健康记录分析中的关键任务，但现有方法面临三重挑战：证据分散于结构化表格、叙事文本、检验轨迹等多源异构数据中，且常被否定表述、时间错配、重复记录和矛盾发现干扰。传统RAG系统仅追求相关性检索，无法区分“表面相关”与“真正支持关系”的证据，导致检索预算被冗余提及耗尽，关键跨就诊事件链缺失；同时，检索到的内容可能是否定、修饰或回溯性提及，方向性不明；即便找到相关事件，也可能来自不兼容的就诊时段或无法溯源到原始记录。本文提出MedEventGraph-RAG框架，核心创新在于将“广泛证据发现”与“严格证据判定”分离：通过患者特定事件图链接每个事件到源头证据，主动检索支持与矛盾两侧信息，并设计查询特定的证据契约，在患者身份、临床范围、事件绑定和来源可追溯性四个维度过滤证据，最终由独立评估器判定支持、矛盾、反驳或证据不足。该框架解决了现有方法在纵向临床验证中证据链不完整、虚假支持结论频发、无法处理矛盾证据等核心问题。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，图增强与自适应RAG（如GraphRAG、混合图-向量检索、迭代图-文档搜索）通过关系扩展和结构感知提升候选发现能力，但未区分“检索信号”与“判定证据”；临床领域变体引入医学知识、患者病史或时间结构，却仍将两者混用。**应用类**聚焦临床事件抽取、时序预测与纵向检索，常依赖领域微调LLM（如BioGPT、ClinicalBERT）增强语言理解，但缺乏对证据可采纳性的显式约束。**评测类**工作多在i2b2、n2c2等基准上验证关系分类或时序推理，但未针对“证据遮蔽”或“中间事件隐藏”等对抗性场景设计评估协议。

本文与上述工作的核心区别在于：提出**证据可采纳边界**，将图检索的广度（支持与矛盾两侧证据）与判定阶段的严格证据契约（患者身份、时间范围、来源可溯性）解耦，并拒绝使用实例级记忆以避免跨记录信息泄漏。相比仅优化检索召回或生成质量的基线，该方法在时间、药物-不良事件、医嘱验证上分别提升26.9、4.9、30.4个平衡准确率点，且在证据遮蔽下实现零虚假支持预测，凸显了“广检索-严判定”范式对纵向临床验证的独特价值。

### Q3: 论文如何解决这个问题？

论文提出MedEventGraph-RAG框架，核心思路是将“广泛的双向证据发现”与“狭窄的证据可采性评估”严格分离。整体架构包含三个关键模块：

**1. 患者事件图与上下文存储**：将每个病历表示为(kg_p, ctxstore_p)二元组。事件图kg_p仅存储记录在案的事件关系与确定性推导，用于结构导航；上下文存储ctxstore_p则保留每个事件对应的原始结构化行、文本片段或数值轨迹，确保证据可溯源。

**2. 自适应双向发现**：解析查询为(E,R,φ)三元组后，控制器从锚点出发迭代扩展候选事件链。检索同时维护对齐查询（寻找支持证据）和反向查询（寻找否定、时间不匹配、历史/假设性提及等反证）。候选路径通过乘积评分R(P|c)排序，该评分融合图扩散、路径紧凑性、源上下文相关性等信号，但弱信号仅降低优先级而非硬过滤，确保反证不被排除。

**3. 证据契约与隔离评估**：发现结果经证据契约过滤，每项必须满足患者一致性、事件绑定、源可解析性和范围有效性。冻结的证据包B_c仅含可采证据，排除图分数、检索排名等元数据。评估器独立计算支持分S+（时间兼容性、数值证据、判断证据加权）与反驳分S-（仅显式源接地反证），通过阈值映射到supported/conflicting/refuted/insufficient四类判定。

创新点在于：证据契约保证评估的固定包独立性，双向检索确保反证不被遗漏，且检索方向不影响证据极性。实验表明该方法在时序、药物不良事件和医嘱验证任务上显著优于基线，并能恢复完整可溯源事件链。

### Q4: 论文做了哪些实验？

论文在十个协议上进行了系统实验，覆盖四个数据集：i2b2、n2c2、MIMIC-IV和LUNGUAGE。实验设置包括七种基线（B1直接LLM、B2文本RAG、B3仅知识图谱、B4松散混合、B5图-文本耦合检索、B6完整系统、B7带程序记忆），并复现了MedGraphRAG、EHR-RAG、HippoRAG 2等六种公开系统的检索算子。

主要结果：在时间验证（T1）、药物不良事件（T2）和医嘱顺序验证（T3）上，B6达到78.6、67.3和96.8的平衡准确率，分别超过最强基线26.9、4.9和30.4点。在证据掩蔽协议（T5）下达到92.2平衡准确率且零虚假支持；在范围验证（T6）中保持76.3%支持召回率。消融实验显示，双向检索将上下文召回从46.0提升至63.1，隔离评估将虚假支持率从23.3降至15.0。组合查询中，隐藏中间事件时完整溯源链恢复率达57.9%（i2b2）和70.0%（LUNGUAGE）。T9跨语料库均优于基线，MIMIC上提升9.2点（p=.0074）。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从三方面展开：其一，当前框架虽将证据发现与判定分离，但事件链重建率（57.9%-70%）仍显著低于验证准确率，未来可引入因果推理或时序逻辑约束，在链式搜索中动态剪枝矛盾路径，提升隐藏事件恢复的完整性。其二，证据合同依赖人工定义的临床范围与关系类型，可探索用LLM自动生成查询特定的证据边界，并加入跨模态语义对齐（如影像报告与结构化数据），增强对非文本证据的溯源能力。其三，当前评估集中于单一时间点验证，未充分处理事件随时间演化的动态性，可设计增量式图更新机制，使证据链随新数据实时修正。此外，将“证据可采纳性”思想迁移至多智能体辩论或检索增强生成中的事实核查，或引入不确定性量化来区分“证据不足”与“证据冲突”，也是值得深挖的方向。

### Q6: 总结一下论文的主要内容

纵向临床事件关系验证旨在判断患者电子健康记录是否支持特定事件间关系。该任务难点在于证据分散于结构化记录、文本、检验轨迹等多源数据中，且否定、时间错配、重复记录和矛盾发现会干扰判断。为此，本文提出MedEventGraph-RAG框架，将事件发生构建为患者特定图，并关联至源头证据。给定验证查询后，图引导发现候选事件链，同时检索支持和矛盾两方面证据，再由查询特定证据契约过滤信息，最终由独立评估器判定支持、冲突、反驳或证据不足。在i2b2、n2c2、MIMIC-IV和LUNGUAGE十个协议上，该框架在时间、药物不良事件和记录顺序验证中分别达到78.6、67.3和96.8的平衡准确率，较最强基线提升26.9、4.9和30.4个百分点。证据遮蔽下无虚假支持预测，中间事件隐藏时能恢复完整可溯源事件链。结果表明，将广泛证据发现与严格证据可采性评估分离，能显著提升纵向临床验证可靠性并减少无依据结论。
