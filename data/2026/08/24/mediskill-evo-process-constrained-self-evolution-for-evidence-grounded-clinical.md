---
title: "MediSkill-Evo: Process-Constrained Self-Evolution for Evidence-Grounded Clinical Interaction"
authors:
  - "Ruoyu Wu"
  - "Shenfu Xie"
  - "Yinqian Sun"
  - "Haibo Tong"
  - "Feifei Zhao"
date: "2026-08-24"
arxiv_id: "2608.23397"
arxiv_url: "https://arxiv.org/abs/2608.23397"
pdf_url: "https://arxiv.org/pdf/2608.23397v1"
categories:
  - "cs.AI"
tags:
  - "Clinical Agent"
  - "Self-Evolution"
  - "Process-Constrained Reasoning"
  - "Evidence Grounding"
  - "Skill Bank"
  - "Process Rules"
  - "Symbolic Schemas"
  - "Measurement Procedures"
  - "Safety-Prioritized Critic"
  - "Tool Interface"
  - "Diagnosis Accuracy"
  - "Treatment-Intent Coverage"
  - "Partial Observability"
  - "Agentic Workflow"
relevance_score: 7.5
---

# MediSkill-Evo: Process-Constrained Self-Evolution for Evidence-Grounded Clinical Interaction

## 原始摘要

Interactive clinical agents must gather decisive evidence and convert it into grounded actions under partial observability. A correct final diagnosis alone does not show that an agent respected evidence and care-process constraints. We introduce MediSkill-Evo, a clinical agent that evolves governed process knowledge without backbone fine-tuning. It separates experience into four typed banks for clinical skills, process rules, symbolic schemas, and measurement procedures. Provenance, support, replay, and controller-defined safety checks govern publication to a frozen test-time snapshot. A Process-Constrained Preference Harness binds evidence to its source, rejects controller-invalid candidates, and ranks actions with a safety-prioritized Clinical Process Critic. We evaluate complete agent systems across two backbone endpoints and six controlled stress dimensions under the same Doctor-turn limit. On 300 held-out Qwen encounters, MediSkill-Evo improves diagnosis accuracy from 61.33 percent to 69.00 percent and treatment-intent coverage from 33.62 percent to 66.44 percent, while reducing automatically scored critical failures from 31.00 percent to 16.33 percent relative to AgentClinic. On 180 hard-isolation conditions derived from 30 cases, target recovery reaches 93.61 percent under patient-behavior pressure, 100.00 percent for temporal evidence, and 92.22 percent for triage red flags. An exploratory 100-case MedSAM comparison evaluates request-gated tool-interface feasibility. These results provide descriptive end-to-end evidence for the complete system on fixed evaluation suites, not causal evidence for an individual bank or clinical validation of the automatic judge.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

该论文旨在解决临床交互智能体在部分可观测环境下，如何从经验中自我进化以生成有证据支撑且符合安全约束的医疗决策的问题。研究背景是现有医疗智能体虽能进行多轮诊断对话，但仅追求最终诊断正确性，忽略了证据获取过程与护理流程约束，导致“正确标签掩盖不安全轨迹”的现象。

现有方法如AgentClinic、MDAgents等虽建立了交互式诊疗范式，但存在三点不足：一是缺乏对轨迹知识的分类型管理，无法区分临床技能、流程规则、符号模式等不同认知角色的知识；二是知识发布机制不严谨，推断或缺失信息可能被静默当作观测事实；三是决策时未将证据来源与行动绑定，难以保证安全优先级。

核心问题是：如何在不微调骨干模型的前提下，通过类型依赖的验证机制和决策权威控制，使智能体从历史轨迹中提取的演化知识既能提升诊断准确率，又能严格遵循证据边界与护理义务。MediSkill-Evo提出四类知识库存储和过程约束偏好框架，将知识类型与验证范围、决策权限关联，实现安全、可追溯的临床交互进化。

### Q2: 有哪些相关研究？

相关研究可分为三类。**方法类**中，Reflexion通过存储语言反馈改进策略，ExPeL整合跨试验洞察，Voyager、ICAL和Agent Workflow Memory将经验蒸馏为可执行技能或工作流，MemP维护可更新的程序性指令，SkillWeaver通过实践发现可复用技能，MemBench区分事实性与反思性记忆并评估效率。本文与这些工作的区别在于，MediSkill-Evo不依赖骨干微调，而是将经验按认知角色分为四类记忆库，并让工件类型同时控制验证方式、检索范围和决策权威，而非仅做结构化记忆或工作流存储。

**应用类**中，AgentClinic模拟部分可观测的医患交互，MDAgents按复杂度调整协作，EHRAgent和MMedAgent连接EHR代码与多模态工具，MEDDxAgent协调模块化诊断，AI Hospital和3MDBench评估多轮症状采集与多模态远程医疗。本文的独特之处在于强调“不可用检查不等于阴性结果”，并通过过程约束偏好框架将证据绑定到来源，拒绝违反控制器约束的候选动作。

**评测类**中，AgentBench和AgentBoard评估多步进展，AppWorld、T-Eval、ToolSandbox和τ-bench暴露状态转换与工具策略。本文提出FullChain基准和受控硬隔离压力测试，专门针对护理过程失败与安全约束，而非仅关注最终诊断准确率。

### Q3: 论文如何解决这个问题？

MediSkill-Evo通过“四库自进化层”和“过程约束偏好控制框架”两大核心模块解决临床交互智能体在部分可观测环境下的证据获取与过程合规问题。整体框架采用“离线进化+在线冻结”机制：训练轨迹完成后，反射器将经验分类存入临床技能库、过程规则库、符号模式库和测量技能库，每个库包含内容、适用范围、轨迹溯源和生命周期状态，通过合并、验证、发布协议生成不可变快照，验证器检查类型一致性、证据泄漏、控制器安全约束和可重放性，但不对未见案例泛化或临床权威性作保证。

在线推理时，偏好控制框架首先从四库检索状态相关知识，若过程规则触发则直接执行确定性动作；否则生成结构化候选（含动作、目标、理由、预期信息价值、支持证据和安全风险），经符号验证器剔除使用不可用证据或违反安全前提的候选，再由临床过程评判器按阶段权重打分，统一选择公式结合硬约束过滤和软约束惩罚（如重复检查、低效操作），硬无效候选无法通过有限惩罚重新进入。最终响应还需通过模式验证、诊断盲审、风险审计和发布认证，未通过时有限重写后安全终止并升级人工处理。

创新点在于：将知识分为四个独立类型边界，分离内容与决策权；确定性证据语义和注册安全前提优先于轨迹派生规则；偏好表示测试时候选排序而非参数学习；每个推理轨迹绑定确定的知识版本，实现可审计的持续进化。

### Q4: 论文做了哪些实验？

论文在三个固定评估套件上对MediSkill-Evo进行了端到端系统级实验。实验设置采用Qwen3.6-Flash和DeepSeek-V4-Flash两个骨干端点，温度为零，每个配置单次rollout，Doctor回合上限固定（文本任务6次，多模态8次）。

数据集包括：MIMIC-IV衍生的700/300训练/测试文本FullChain交互；420/180条件的受控临床压力基准（覆盖诊断难度、证据完整性、患者行为、治疗安全、时间动态、分诊红旗六维度，采用确定性控制器硬隔离）；NEJM图像集200/100多模态案例。

对比方法包括AgentClinic、无经验库的原始Doctor、Agent-KB、ExPeL、MemP、Reflexion、SkillWeaver和MediSkill-Evo。主要结果：在Qwen端点上，诊断准确率从61.33%提升至69.00%，治疗意图覆盖率从33.62%提升至66.44%，关键失败率从31.00%降至16.33%；DeepSeek端点上安全违规从20.33%降至3.33%，关键失败从52.00%降至33.00%。压力测试中目标恢复率达93.61%（患者行为）、100%（时间证据）、92.22%（分诊红旗）。多模态MedSAM对比验证了请求门控工具接口可行性。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是缺乏对单个记忆库（如技能库、过程规则库）的因果消融分析，无法确定各组件对整体性能的独立贡献；二是自动评估器（Clinical Process Critic）虽能区分过程质量，但未经临床专家校准，其安全性和治疗意图的判定可能偏离真实临床标准；三是仅在两种骨干模型上验证，且未控制内部计算成本，泛化性和效率声明受限。

未来可从以下方向探索：首先，设计逐库消融实验，通过冻结或移除单一银行来量化其因果效应，并引入人类临床医生对评估器输出进行标注校准，建立更可信的自动评判标准；其次，将过程约束从文本扩展到多模态证据（如医学影像、生理信号），探索跨模态的证据溯源与安全门控机制；再次，研究过程知识的动态更新策略，在测试时允许安全地增量学习新技能而非完全冻结；最后，可尝试将过程约束与强化学习结合，在更真实的临床模拟环境中验证其长期适应性和鲁棒性。

### Q6: 总结一下论文的主要内容

MediSkill-Evo提出了一种面向证据 grounded 临床交互的自进化智能体系统，核心在于解决部分可观测条件下智能体必须收集关键证据并转化为合规行动的问题。该系统将经验分为临床技能、流程规则、符号模式与测量程序四类知识库，通过来源追溯、支持度、重放及控制器安全检查实现受控发布。其流程约束偏好框架将证据绑定至来源，拒绝无效候选，并借助安全优先的临床过程评判器排序动作。在300例Qwen对话中，诊断准确率从61.33%提升至69.00%，治疗意图覆盖率从33.62%升至66.44%，关键失败率从31.00%降至16.33%。在180例硬隔离压力测试中，患者行为、时间证据及分诊红旗恢复率分别达93.61%、100%和92.22%。该工作贡献了完整系统设计、压力基准及探索性工具接口，但结果仅为端到端描述性证据，未提供各组件因果效应或临床验证。
