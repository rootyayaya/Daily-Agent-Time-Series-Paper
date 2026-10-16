---
title: "Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure"
authors:
  - "Pradipta Ghosh"
  - "Gaurav Mitra"
  - "Shripad Nadgowda"
  - "Akshil Shah"
  - "Junyu Liu"
  - "Canturk Isci"
  - "Syamla Bandla"
  - "Xinyao Hu"
  - "Onkar Deshpande"
  - "Anik Dasgupta"
date: "2026-10-15"
arxiv_id: "2610.21281"
arxiv_url: "https://arxiv.org/abs/2610.21281"
pdf_url: "https://arxiv.org/pdf/2610.21281v1"
categories:
  - "cs.AI"
  - "cs.MA"
tags:
  - "Agentic RCA"
  - "Root Cause Analysis"
  - "LLM Agent"
  - "Evidence Routing"
  - "Incident Knowledge Graph"
  - "Human-in-the-loop"
  - "Skill Adaptation"
  - "Tool Use"
  - "Multi-agent"
  - "Verifier"
  - "Industrial Diagnosis"
  - "Large-Scale Infrastructure"
  - "Observability"
  - "Groundedness"
  - "Workflow"
relevance_score: 8.5
---

# Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure

## 原始摘要

Root-cause analysis (RCA) in large-scale distributed systems is challenging because a single symptom can cross service, data, configuration, compute, and organizational boundaries. Responders must assemble incomplete evidence and coordinate experts who hold different parts of the causal path. Generic language-model agents do not solve this problem through tool access alone: they can use stale or mistimed context, interpret failed queries as absent symptoms, report unsupported system state, and overload observability services designed for human-paced use.
  We present Diviner (Domain-Informed Verifiable Incident Navigation through Evidence and Review), an agentic RCA system operating at Meta and organized around a four-stage reliability lifecycle. Encode combines a large corpus of reviewed incidents with service-owner expertise to produce scoped, versioned skills, workflows, typed tools, and an incident knowledge graph. Execute uses an adaptive Lead and context-isolated workers to apply relevant knowledge to point-in-time evidence and maintain evidence-linked hypotheses. Evaluate compares saved investigation trajectories with responder-reviewed outcomes to measure exact cause, useful direction, and Groundedness. Adapt uses recurring gaps and on-call feedback to derive focused operational- knowledge updates, admitting them only after replay, quality checks, and owner approval.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

大规模分布式系统中的根因分析（RCA）极具挑战：单一症状可能跨越服务、数据、配置、计算和组织边界，故障组件与致因组件往往相距甚远，且各组件独立演化，导致故障在不同层间延迟显现。响应者需拼凑不完整证据，并协调掌握因果链不同环节的多方专家。现有通用语言模型智能体仅靠工具接入无法解决该问题：它们可能使用过时或时机不当的上下文，将查询失败误判为症状缺失，报告无依据的系统状态，并使人机节奏设计的可观测服务过载。此外，RCA并非普通任务补全问题——没有稳定仓库、确定性测试套件或带已知答案的干净任务集，必要证据随事件演进而变化，且强基准或编码性能未必能转化为可靠的事件调查能力。本文提出Diviner，一个在Meta大规模基础设施上运行的智能体RCA系统，其核心问题是：如何通过受治理的知识、显式证据语义、有界执行和人工把关的更新，实现可靠的RCA智能体，即“受治理的不确定性消减”，使推理保持自适应的同时，允许使用的知识、证据准入和持久知识变更均保持范围受限且可归因。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，Mystery Machine、Eadro、DiagFusion 等跨信号诊断工作结合 traces、logs、metrics 与依赖结构定位异常组件，但其分析依赖预定义的遥测模式与故障类别，难以处理观测者意见不一致的灰色故障。ESRO 等经验检索系统将实时告警与历史故障图结合，检索可能原因与缓解措施，但相似事件只能作为假设来源，不能证明当前系统状态。应用类方面，监控告警、仪表盘与 runbook 可自动化已知症状的重复检查，但前提是团队已预判故障模式并编码正确标识符，无法在证据推翻预期路径时选择新的跨系统查询。评测类方面，现有编码智能体基准依赖稳定工作区与可重复的构建/测试信号，而 RCA 缺乏确定性路径与验证器，基于准确率的评测会奖励猜测而非弃权。本文与上述工作的区别在于：Diviner 不局限于执行固定诊断路径或检索历史经验，而是通过 Encode、Execute、Evaluate、Adapt 四阶段生命周期，将服务所有者编写的版本化技能、工作流与类型化工具同证据链接的假设更新、轨迹评测和受治理的知识更新结合起来，实现开放式、可验证且人类保留最终权限的根因分析。

### Q3: 论文如何解决这个问题？

Diviner 解决该问题的核心思路，是把“通用工具型 LLM Agent”改造成受治理、可验证、人在环的工业级 RCA 系统，并用四阶段可靠性生命周期把诊断知识的生产、使用、评估和更新闭环起来。

整体框架为 Encode → Execute → Evaluate → Adapt。Encode 阶段把已复盘事故语料与服务负责人经验蒸馏为失败签名，并构建事故知识图谱（IKG）；同时把专家流程封装为技能、工作流和类型化工具，登记其范围、所有者、版本、来源与启用状态。IKG 用 DRAMA-1B 将上下文、症状、因果机制、缓解建议分别编码为四类语义视图，配合 FAISS 检索与结构化因子过滤，历史先例只作为假设生成器，必须由当前证据验证。

Execute 阶段采用事件驱动的 Lead–worker 架构：Lead 根据告警、范围和初步症状检索适用工作流与 IKG 先例，实例化为调查计划；独立 worker 在隔离上下文中并发执行技能，只返回结构化观察结果。Lead 可动态增删、重排或剪枝分支，但不能改写已登记工作流。系统显式维护假设状态（支持/反驳/未决），并区分数据、有效空结果、部分结果与失败，避免把查询失败误判为症状缺失。运行时 Review Agent 在结论输出前检查证据引用、冲突与未决测试，必要时返回具体问题继续核查；若证据不足，则输出带明确缺口的部分评估。

Evaluate 阶段用 DivinerEval 与 Agent Judge 从精确根因、有用方向和 Groundedness 三个维度评分。Adapt 阶段将反复出现的缺口映射到最小可更新工件，经结构校验、配对回放、质量与延迟回归检查后，由所有者审批发布，实现人类治理下的持续适应。

### Q4: 论文做了哪些实验？

论文围绕Diviner系统开展了基于Meta真实生产环境的评估实验。实验设置上，采用DivinerEval框架，将缓解后的检查点调查轨迹与响应者审核记录组成的参考结果进行关联，并通过覆盖门控排除无可靠参考或不可审查轨迹的案例。评估由缓解后Agent Judge从三个维度打分：Exact RCA（是否识别出经审核的因果机制）、Direction（是否有效缩小调查方向至正确子系统或故障机制）、Groundedness（主张与假设变化是否依据正确来源、范围、时间和工具结果的引用证据）。数据集来自Meta大规模分布式系统的事件语料，包括大量经审核的事件记录、服务所有者专业知识和事件知识图谱。对比方法方面，论文将Diviner与通用语言模型智能体进行对比，指出后者仅靠工具访问无法解决上下文过时、将失败查询误判为无症状、报告无依据系统状态等问题。主要结果以Agent Judge输出的评分、理由、支持或矛盾记录及工件关联的失败标签呈现，专家审计这些记录并在发现系统性错误时修订版本化评分标准。关键指标为Exact RCA、Direction和Groundedness三个维度的评分。

### Q5: 有什么可以进一步探索的点？

论文的局限首先体现在Adapt环节：回放无法复现真实环境的权限、限流、并发与时序，因此更新后的知识能否在线上持久有效，仍需后续真实事件检验，反馈闭环存在滞后。其次，人工审批虽保证可靠性，却可能成为规模化瓶颈，且评估指标（精确根因、有用方向、Groundedness）对"部分正确"的刻画仍较粗。未来可探索：一是构建更真实的仿真或影子执行环境，缩小回放与线上的差距；二是引入置信度校准与自动降级机制，让低风险更新走快速通道、高风险更新保留人工闸门；三是将知识图谱与技能版本做因果消融，量化每个artifact对诊断准确率的边际贡献，避免知识冗余；四是支持跨组织、跨租户的知识迁移与冲突消解；五是研究Agent Judge与人类评审不一致时的仲裁策略，把评估标准本身也当作可学习对象。

### Q6: 总结一下论文的主要内容

论文针对大规模分布式系统中根因分析（RCA）跨服务、跨组织、证据不完整的难题，提出智能体系统 Diviner。作者指出，通用 LLM 智能体仅靠工具调用不足以可靠诊断，可能误用过期上下文、将查询失败当作症状缺失，并给可观测性系统带来过载。Diviner 以四阶段可靠性生命周期组织：Encode 将已复盘事件与服务专家知识编码为受治理、带版本和范围的故障签名、技能、工作流、类型化工具及事件知识图谱；Execute 由自适应 Lead 与上下文隔离的 worker 基于实时证据开展调查，维护证据关联的假设；Evaluate 用保存轨迹与人工复盘结果对比，衡量精确根因、有用方向和证据支撑度；Adapt 依据反复出现的缺口生成知识更新，经回放、质量检查和负责人审批后才生效。在 Meta 的实践表明，Diviner 已支持数千起事件，45% 评分案例找到精确根因，60% 提供有用方向，平均 Groundedness 达 80%，并将检测到缓解时间降低约 52%。
