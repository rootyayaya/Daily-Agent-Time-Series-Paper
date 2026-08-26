---
title: "STRIVE: Multi-Agent Structured Temporal Reasoning with Integrated Verification for Longitudinal Radiology Report Generation"
authors:
  - "Junyeong Maeng"
  - "Eunsong Kang"
  - "Heung-Il Suk"
date: "2026-08-25"
arxiv_id: "2608.24237"
arxiv_url: "https://arxiv.org/abs/2608.24237"
pdf_url: "https://arxiv.org/pdf/2608.24237v1"
categories:
  - "cs.AI"
tags:
  - "Multi-Agent Reasoning"
  - "Temporal Reasoning"
  - "Verification"
  - "Longitudinal Report Generation"
  - "Structured Reasoning"
  - "LLM Agent"
  - "Clinical NLP"
  - "Evidence Routing"
  - "Reinforcement Learning"
  - "GRPO"
relevance_score: 8.5
---

# STRIVE: Multi-Agent Structured Temporal Reasoning with Integrated Verification for Longitudinal Radiology Report Generation

## 原始摘要

Longitudinal radiology report generation (LRRG) requires identifying both current findings and their changes relative to a prior study. Existing methods jointly model diagnosis, attribute estimation, temporal comparison, and language generation within implicit representations, which can cause task interference, obscure the evidence underlying each decision, and limit error traceability. They also model progression states as independent labels, ignoring their ordered structure and thus treating missed changes and direction reversals equally. We present STRIVE, Multi-Agent Structured Temporal Reasoning with Integrated Verification for LRRG, which decomposes clinical reasoning into specialized Diagnosis, Attribute, and Temporal Change Agents that produce explicit intermediate evidence. In particular, the Temporal Change Agent is further post-trained using Progression-Aware GRPO, a verifiable, shaped reward that assigns partial credit to direction-preserving errors while scoring direction reversals lowest. STRIVE performs verification at two stages: a deterministic Consistency Gate reconciles the agent outputs before report generation, and a Validation Agent checks whether the generated report is supported by the aggregated clinical evidence. On Longitudinal-MIMIC, STRIVE attains the best clinical efficacy among recent methods and more than doubles Longitudinal Change Concordance (LCC), a measure of temporal agreement with the reference report, over the strongest baseline.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

纵向放射学报告生成（LRRG）旨在识别当前影像发现及其相对于既往检查的变化，但现有方法存在两大核心缺陷。首先，主流方法将诊断、属性估计、时间比较和语言生成隐式耦合在共享表征中，导致任务间相互干扰：生成任务偏好平滑语义空间，而临床决策需要离散约束空间，联合优化会扭曲中间证据，且错误难以追溯至具体推理环节。其次，现有方法将进展状态（如新增、消退、加重、稳定）建模为独立标签，完全忽略其有序方向性结构，导致“漏报进展”（将加重误判为稳定）与“方向反转”（将加重误判为减轻）被同等对待，而后者临床危害显著更大。此外，缺乏直接评估时间变化一致性的指标。为此，本文提出STRIVE框架，通过分解为诊断、属性、时间变化三个专用智能体生成显式中间证据，并引入进展感知GRPO奖励区分方向性错误，配合一致性门控和验证智能体确保最终报告忠于临床证据，从而解决任务干扰、状态结构缺失和证据可追溯性不足的核心问题。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**：传统RRG方法（如PriorRG）仅建模单次影像，忽略跨时间变化；LRRG方法中，BiOTPrompt利用双向最优传输捕捉非对称斑块级变化，MARE动态对齐病灶区域并推理视觉与文本演变关系，TIM则分离空间表征与进展建模。这些方法均将诊断、属性估计和时间比较编码于隐式表示中，导致任务干扰且错误难溯源。**多智能体类**：CogRad和RadAgents将单次影像解读分解为分诊、区域分析、报告撰写和验证等专门智能体，但均未显式建模跨时间变化。**评测类**：Longitudinal-MIMIC基准及LCC指标用于评估时间一致性。STRIVE的独特之处在于：首次将时间变化判断作为独立智能体输出，并通过Progression-Aware GRPO奖励建模进展状态的顺序结构（方向逆转惩罚最重），同时引入确定性一致性门控和验证智能体进行双重校验，弥补了现有方法在可解释性和错误追踪上的不足。

### Q3: 论文如何解决这个问题？

STRIVE通过多智能体任务分解与两阶段验证机制，系统性地解决了纵向放射学报告生成中的任务干扰、证据不透明和错误难追踪问题。

整体框架将临床推理分解为三个角色专业化智能体：诊断智能体（Diagnosis Agent）基于七种冻结的胸部X光专家模型（三种分类专家和四种生成专家）输出显式发现状态（POS/UNC/NEG）；属性智能体（Attribute Agent）利用医学视觉语言模型对阳性发现预测严重程度和位置；时间变化智能体（Temporal Change Agent）结合既往报告、间隔时间、诊断状态和疾病特异性概率，输出六类变化标签（new/increased/stable/decreased/resolved/none）。三者均先经SFT微调，其中时间变化智能体额外采用时间反转数据增强以增强方向一致性。

核心创新在于Progression-Aware GRPO后训练：设计三层结构化奖励（检测层、粗粒度方向层、细粒度状态层），对保持临床方向但细粒度错误的预测给予部分奖励，而对方向反转和遗漏变化给予最低分，从而显式建模变化状态的序数结构。两阶段验证包括：确定性一致性门（Consistency Gate）在生成前修正诊断与变化状态间的逻辑冲突（如NEG与new/increased不兼容），以及验证智能体（Validation Agent）在生成后检查报告是否完整且准确地表达了结构化临床状态（SCS），对缺失或矛盾的发现进行局部编辑。

该方法在Longitudinal-MIMIC上取得最佳临床效能，LCC指标较最强基线提升超过两倍，验证了显式中间证据与结构化奖励的有效性。

### Q4: 论文做了哪些实验？

在 Longitudinal-MIMIC 基准上，STRIVE 与两类方法对比：单图像 RRG（R2Gen、R2GenCMN、R2GenGPT、PromptMRG、EKAGen、GMoD、RADAR、MedRAX）和纵向 RRG（Prefilling、HERGen、STREAM、MLRG、LLM-RG4、HC-LLM、Diff-RRG、PriorRG、MARE、BiOTPrompt、TIM）。测试集含 2,058 个研究。三个临床决策智能体经监督微调，时间变化智能体额外用 Progression-Aware GRPO 优化，报告生成使用冻结的 PriorRG 草稿和 27B 指令微调 LLM。

主要结果：STRIVE 在除 ROUGE-L 外的所有 NLG 指标上最优，CE 指标全面领先（F1=0.620，精确率 0.581，召回率 0.665）。ReXrank 套件中六项指标最优（1/RadCliQ-v1=1.173，BLEU=0.272，SembScore=0.467，RadGraph-F1=0.270，RaTEScore=0.582，GREEN=0.342）。纵向正确性上，LCC-C=0.394、LCC-F=0.283，是强基线（0.193/0.128）的两倍以上。

消融实验显示：移除时间变化智能体使 LCC-C 降至 0.148、LCC-F 降至 0.095；去掉 GRPO 使 LCC-F 降至 0.259；移除验证智能体使 CE-F1 降至 0.615、LCC-C 降至 0.338；移除一致性门使 LCC-C 降至 0.389。用规则投票替代诊断智能体使 CE-F1 降至 0.612，用先前报告替代草稿使 BLEU-1 从 0.466 降至 0.381。

### Q5: 有什么可以进一步探索的点？

STRIVE通过多智能体分解和验证机制显著提升了纵向放射学报告生成的时序一致性，但仍存在若干可探索方向。首先，当前验证依赖确定性规则和单一验证智能体，可引入更细粒度的证据链推理，如让验证智能体对每个临床发现逐条追溯其来源，并利用外部知识库（如医学指南）增强验证的可靠性。其次，Progression-Aware GRPO虽区分了方向性错误，但未建模时间间隔对变化程度的影响，未来可引入连续时间建模或基于时间戳的衰减权重，使变化评估更贴近临床实际。此外，智能体间交互目前是顺序流水线，可探索动态路由或双向协商机制，允许Temporal Change Agent反向修正Diagnosis Agent的初步判断。最后，框架在单一数据集上验证，跨机构、跨模态（如结合影像特征）的泛化性及少样本场景下的鲁棒性值得进一步测试，也可尝试将结构化证据用于可解释的临床决策支持系统。

### Q6: 总结一下论文的主要内容

STRIVE提出了一种面向纵向放射学报告生成（LRRG）的多智能体框架，旨在解决现有方法中临床推理与语言生成隐式耦合、以及进展状态方向关系建模不足的问题。该方法将任务分解为三个专门智能体：诊断智能体判断发现是否存在，属性智能体刻画严重度和位置，时间变化智能体识别相对既往检查的变化。特别地，时间变化智能体采用Progression-Aware GRPO进行后训练，通过分层奖励对方向保持错误给予部分分数，而对方向反转给予最低分。框架还集成了两阶段验证：确定性一致性门控在生成前调和智能体输出冲突，验证智能体在生成后检查报告是否被结构化临床证据支持。在Longitudinal-MIMIC基准上，STRIVE在临床效能指标上优于现有方法，并将纵向变化一致性（LCC）提升至最强基线的两倍以上，显著改善了时间推理的准确性和可追溯性。
