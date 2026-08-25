---
title: "HiMA-MDD: A Hierarchical Multi-Agent Harness for Interpretable Multimodal Depression Detection in Clinical Interviews"
authors:
  - "Ao Chen"
  - "Xiaojiang Peng"
date: "2026-08-22"
arxiv_id: "2608.21868"
arxiv_url: "https://arxiv.org/abs/2608.21868"
pdf_url: "https://arxiv.org/pdf/2608.21868v1"
categories:
  - "cs.AI"
tags:
  - "多智能体系统"
  - "分层证据路由"
  - "可解释诊断"
  - "临床访谈分析"
  - "LLM工作流编排"
  - "证据追踪"
  - "PHQ-8评估"
  - "多模态融合"
relevance_score: 8.5
---

# HiMA-MDD: A Hierarchical Multi-Agent Harness for Interpretable Multimodal Depression Detection in Clinical Interviews

## 原始摘要

Depression assessment from multimodal clinical interviews requires integrating dispersed evidence from multiple symptoms into a coherent PHQ-8 profile. This process is hierarchical: relevant evidence is often sparse and context-dependent within local question-answer exchanges, multiple exchanges jointly support symptom-level judgments, and the final assessment depends on the coherence of the complete symptom profile. Existing LLM systems either process interviews holistically or distribute work across generic agent roles; neither design necessarily provides an explicit orchestration mechanism that coordinates evidence access, item-score authority, bounded feedback, and state recording across these levels. To address this gap, we introduce HiMA-MDD, a hierarchical multi-agent harness that aligns this assessment hierarchy with three agent layers. After non-agentic preprocessing constructs context-preserving multimodal QA units, Layer 1 identifies candidate QA-to-item relations and supports bounded item-grounded evidence routing. Layer 2 assigns symptom groups to operational factor specialists, with one specialist responsible for each provisional item score. Layer 3 audits the complete provisional profile, requests at most one round of targeted revision, and reconstructs the verified PHQ-8 profile. This layered design naturally yields a Hierarchical Evidence Trace, preserves all intermediate evidence, judgments, and revisions for auditability. The final item scores then deterministically produce the total score and screening decision. Using Qwen2.5-72B-Instruct as the harness backbone, our experiments on E-DAIC demonstrate that HiMA-MDD outperforms the compared state-of-the-art methods.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

抑郁症评估在临床访谈中需要将多模态信息整合为PHQ-8症状画像，这一过程天然具有层级性：局部问答中的证据稀疏且依赖上下文，多个问答共同支撑症状判断，最终评估取决于完整症状画像的一致性。然而，现有方法存在明显不足：整体式预测器将访谈扁平化为单一输出，隐式处理证据归因，仅在输出端套用PHQ-8结构；而面向功能的多智能体系统虽分配了提问、评分等角色，却未明确各智能体的证据访问权限，也未将评分责任与PHQ-8条目结构对齐。更关键的是，多模态访谈、症状推理与最终评估处于不同粒度层级，现有系统缺乏显式编排机制来协调跨层级的证据访问、评分授权与全局修订，作者将此称为“层级鸿沟”。本文核心问题正是弥合这一鸿沟，通过设计HiMA-MDD层级多智能体框架，将评估层级与三层智能体结构对齐，显式管控证据访问边界、条目评分单一所有权、受限反馈传播及中间状态记录，从而生成可审计的层级证据轨迹，实现从局部多模态问答到完整PHQ-8画像的可解释、可验证的抑郁评估。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，早期系统直接从完整访谈预测总分或筛查标签，近期工作引入LLM转录表征、面部表情特征和多模态大模型；部分研究转向细粒度预测，如以问卷条目或子分数为目标、从访谈文本完成标准化问卷、或为单个条目分别检索证据，并通过问题层级或结构图组织长访谈、生成PHQ感知的症状摘要。**多智能体类**包括MDAgents（按任务复杂度调整临床决策团队）、AgentMental（分配提问生成、应答评估、评分和信息更新）、MAGI（围绕结构化精神访谈协调专业角色）及AI精神科助理（整合评估、判断、评分和审查智能体）。**心理测量类**研究探讨PHQ-9内部结构，如单因子、相关双因子（认知/情感与躯体）、双因子模型及四组组织（情感、躯体、内化、感觉运动）。

本文与上述工作的区别在于：现有LLM系统要么整体处理访谈，要么按通用角色分工，缺乏显式协调机制来管理证据访问、条目评分权限、有界反馈和状态记录。HiMA-MDD以PHQ-8测量过程为组织原则，通过三层智能体层级（证据路由、因子专家、整体审计）将评估层级与智能体职责对齐，而非仅依赖角色专业化。与心理测量文献不同，本文不提出或验证新因子模型，而是将四组组织作为操作性的责任映射，并评估不同推理粒度。其核心创新在于将症状证据作为显式控制接口的一部分，而非仅作为输入表征或检索结果，同时生成可审计的层级证据追踪。

### Q3: 论文如何解决这个问题？

HiMA-MDD通过一个与PHQ-8测量层级对齐的三层多智能体框架来解决抑郁症检测中的证据整合问题。整体架构由非智能体预处理和三个智能体层级组成，并辅以可选的监督校准接口。

预处理阶段将临床访谈构建为保留上下文的“多模态QA单元”，每个单元包含问题、回答、时间戳和对齐的语音声学特征（eGeMAPS功能集和KintsugiHealth DAM模型估计）。第一层由QA-to-Item Grounding Agent负责，通过LLM相关性映射器建立QA单元与PHQ-8条目间的多对多候选关系，记录证据极性（支持/矛盾/不确定），并由条目感知路由器为每个症状生成Item-Grounded Evidence Bundle，同时施加有界证据访问策略。

第二层将八个症状分组分配给四个并行专家：情感专家（快感缺失、抑郁情绪）、躯体专家（睡眠、疲劳、食欲）、内化专家（低自我价值）和感觉运动专家（注意力、精神运动障碍）。每个条目有且仅有一个专属专家负责产生临时评分，专家输出评分、置信度、引用证据和充分性判断，形成临时PHQ-8档案。

第三层Global Symptom Verification Agent执行三阶段验证：跨因素审计检查无依据评分、时间/频率缺失、躯体-情感混淆等问题；发起至多一轮定向修订请求，仅重跑被指名的专家；最后通过集中式LLM聚合器重建验证档案。原始验证条目分数经固定PHQ-8规则确定性计算总分和筛查决策。

创新点在于：显式编排契约约束证据访问和评分权限；层级化证据追踪保留所有中间判断；至多一轮有界反馈机制；以及可选的贝叶斯岭回归后校准接口，在不重跑智能体的情况下修正序数评分偏差。

### Q4: 论文做了哪些实验？

实验在E-DAIC和DAIC-WOZ两个多模态临床访谈数据集上进行，均含PHQ-8标签。主评估使用E-DAIC测试集，DAIC-WOZ开发集用于鲁棒性分析。输入为ASR转录文本和参与者语音音频，任务预测8个PHQ-8条目分数（0-3分），总和≥10判定为抑郁筛查阳性。

对比方法包括三类：提示基线（Zero-Shot、3-Shot、CoT）、多智能体系统（MDAgents、AgentMental），以及文献报告方法（MLlm-DR、Dep-LLM等）。所有本地方法统一使用Qwen2.5-72B-Instruct骨干和相同评估协议。

主要结果：HiMA-MDD经事后校准后取得最优性能，Total MAE为3.41，RMSE为4.57，筛查准确率0.84，κ=0.63，Macro-F1=0.81，均优于所有对比方法。在DAIC-WOZ上，HiMA-MDD原始输出的筛查准确率（0.857）、κ（0.677）和Macro-F1（0.838）均为最佳。消融实验显示，跨因子审计与定向修订贡献最大，移除后所有指标显著下降；集中式档案重建和声学描述符增强也均有正向作用。推理粒度实验表明，四因子配置在总分估计上最优，两因子配置在筛查一致性上最佳。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从以下角度展开：首先，当前方法依赖单一LLM（Qwen2.5-72B）作为骨干，未充分探索不同规模或开源模型对层级协调鲁棒性的影响，未来可测试更小模型在资源受限场景下的表现，或引入模型集成以增强稳定性。其次，层级证据追踪虽提升了可审计性，但未量化其对抗“幻觉证据”或错误路由的容错能力，可设计对抗性测试或置信度校准机制来强化证据可靠性。再者，当前仅支持一轮修订，对复杂或矛盾症状可能不足，可扩展为动态迭代策略，并引入外部知识库（如DSM-5）辅助验证。此外，E-DAIC数据集规模有限且模态单一（音视频+文本），未来可在多中心、多语言临床数据上验证泛化性，并探索跨文化症状表达的差异。最后，可考虑将层级输出与可解释性可视化工具结合，辅助临床医生快速定位关键证据，甚至反向优化访谈提问策略，形成闭环诊断支持系统。

### Q6: 总结一下论文的主要内容

HiMA-MDD提出了一种分层多智能体框架，用于从多模态临床访谈中进行可解释的PHQ-8抑郁评估。该问题具有层级性：局部问答中的证据稀疏且依赖上下文，多个问答共同支持症状判断，最终评估依赖完整症状画像的一致性。现有LLM系统缺乏跨层级的显式编排机制。方法上，HiMA-MDD通过非智能体预处理构建保留上下文的QA单元，Layer 1识别候选问答与症状条目的关系并进行证据路由，Layer 2分配症状组给专家智能体并负责暂定条目评分，Layer 3审计完整画像并最多请求一轮定向修订，最终生成可验证的PHQ-8画像。该设计自然产生层级证据追踪，保留所有中间证据、判断和修订供审计。基于Qwen2.5-72B-Instruct的实验表明，HiMA-MDD在E-DAIC数据集上优于现有最先进方法，验证了测量对齐治理在组织评估和保持可检查路径方面的有效性。
