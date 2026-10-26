---
title: "DMAIC-Bench: From Self-Reflection to Self-Restraint for Agents in Multi-Stage Analytical Tasks"
authors:
  - "Shan Peng"
  - "Shuaiqi Cheng"
  - "Miao Peng"
  - "Chenyi Zi"
  - "Jia Li"
date: "2026-10-23"
arxiv_id: "2610.32305"
arxiv_url: "https://arxiv.org/abs/2610.32305"
pdf_url: "https://arxiv.org/pdf/2610.32305v1"
github_url: "https://github.com/psptpx/DMAIC-Bench-public"
categories:
  - "cs.AI"
  - "cs.CL"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "LLM Agent"
  - "自反思"
  - "自我约束"
  - "多阶段分析"
  - "工业诊断"
  - "证据路由"
  - "基准测试"
  - "决策制定"
  - "可解释诊断"
relevance_score: 7.5
---

# DMAIC-Bench: From Self-Reflection to Self-Restraint for Agents in Multi-Stage Analytical Tasks

## 原始摘要

Multi-stage analytical tasks require LLM agents to use intermediate evidence to decide whether to continue, redirect or stop. Self-reflection, in which an agent critiques its output, is widely studied, yet a critique does not show whether evidence changed the next action. We call that capability self-restraint. Existing agent benchmarks largely measure task completion or output quality and leave it untested. DMAIC-Bench evaluates it with 97 seeded tasks across 15 industrial cases in four sectors, built around Lean Six Sigma's explicit statistical prerequisites. Paired counterfactual variants require opposite actions at the same workflow position, distinguishing warranted restraint from indiscriminate stopping. We assess execution traces with a private scorer and final claims through independent expert review. Across 13 models from six providers, execution-level routing accuracy averages 92% on matched GO decisions and 19% on NO-GO decisions, counting any forbidden downstream computation as a route error. Execution traces show agents reporting correct diagnostics before performing analyses that those results disallow. Separately, blinded expert review of the 11 audited agents estimates that reports act on invalid evidence at 47% of reached NO-GO decisions, with an interval from 31% to 61%. Explicit stopping permission helps some models without consistently restoring correct decisions at both GO and NO-GO forks. Sixteen life-sciences tasks in bulk ribonucleic acid sequencing (RNA-seq) and case-control genome-wide association studies (GWAS) show that the same framework can evaluate evidence-dependent decisions beyond industrial workflows. Project code and data are available at: https://github.com/psptpx/DMAIC-Bench-public.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注多阶段分析任务中LLM智能体如何依据中间证据决定是否继续、转向或停止的问题。研究背景是：在科学与工程的多阶段分析流程中，中间检查用于确认后续分析的前提是否成立，一旦前提失败仍继续执行，即使下游计算本身正确，也会得出无效结论。然而现有智能体基准多以任务完成率或最终产物质量评分，无法衡量智能体是否根据中间结果的有效性来调整下一步行动。作者将“不顾有效性持续调用工具”的倾向称为行动偏差，并提出“自我约束”能力——即计算出的证据是否真正改变下一步动作，这与仅让模型自我批评的自我反思不同。本文的核心问题是：智能体能否在多阶段分析任务中利用计算得到的证据，在继续、转向和停止之间做出正确选择。为此作者构建了DMAIC-Bench，基于精益六西格玛的显式统计前提，设计97个任务、15个工业案例，并用配对反事实变体区分“有依据的停止”与“一律拒绝”，同时通过执行轨迹评分和独立专家评审检验智能体是否在诊断正确后仍执行了前提所禁止的分析。

### Q2: 有哪些相关研究？

相关研究可分为三类。方法类方面，Reflexion、Self-Refine、CRITIC等通过反思或外部反馈修正输出，但自我纠错依赖反馈质量；DMAIC-Bench指出“批判”不等于“证据改变下一步行动”，提出并测量self-restraint。弃权类方面，选择性问答、拒绝感知微调及AgentAbstain、Agentic Abstention等考察模糊、缺信息或冲突目标下的弃权与升级；区别在于DMAIC-Bench在同一工作流位置构造配对反事实变体，仅计算值不同，从而隔离“正确诊断是否真正约束下一步动作”。评测类方面，SWE-bench、MLE-bench、PaperBench、Terminal-Bench评估完成产物，τ-bench测试交互式工具使用，StatQA、P-Bench、StatEval考察统计推理与推断错误，SDBench、SOP-Bench关注流程依从；这些基准多衡量任务完成或输出质量，未直接评分“计算出的诊断是否许可下一分析”。运行时管控方面，Shielding与guardrail约束不安全动作，AI-control研究不可信策略下的监控；DMAIC-Bench中数据管家仅强制前置条件，当诊断与被禁止分析共享同一批次时，克制决策仍由智能体承担。

### Q3: 论文如何解决这个问题？

论文提出DMAIC-Bench这一基准框架，核心在于将“自我约束”（self-restraint）从抽象的自我反思中剥离出来，转化为可测量、可反事实检验的执行决策能力。整体框架由三部分组成：一是受守卫的决策图（guarded graph）G=(V,E,Φ)，将分析阶段与终止动作建模为节点，边表示允许的转移，谓词Φ对上游诊断结果施加统计前置条件（如量具guard采用AIAG MSA-4标准，要求SV_gauge≤0.30且ndc≥5），据此生成97个种子任务与参考路线，并通过配对反事实变体在同一工作流位置要求相反的GO/NO-GO动作，从而区分“有依据的克制”与“无差别停止”。二是共享执行框架（harness），在隔离容器中运行固定版本的科研Python库且无网络，内置数据管家提供request、declare、provision、status四类操作，仅provision消耗有限查询预算，并依据审计日志校验数据访问前置条件；真实标签存放于代理不可达的独立验证容器中。三是双层评估：私有评分器将执行轨迹与参考路线比对，计算分支级路由准确率，并以方法召回、精确率、数值保真与路由准确率的调和平均构成奖励，引入误用惩罚U和完整性门控I（若访问被扣留数据则奖励归零）；最终报告则由独立专家盲审。创新点在于以反事实配对分叉检验证据是否真正改变下一步动作，将“正当早停”计为有效路线完成，并把该框架扩展至RNA-seq与GWAS等生命科学任务，验证其跨领域适用性。

### Q4: 论文做了哪些实验？

论文构建了DMAIC-Bench基准，包含15个工业案例、97个种子任务和175个节点，覆盖四个行业、五个DMAIC阶段和29种方法，参考路线平均含6.0次分析和3.1个分级决策，其中300个决策中有284个受上游分析约束。任务分为A-go、B-divert、C-stop三类，后两类共需转向或停止。实验评估了来自六家提供商的13个模型，采用私有评分器评估执行轨迹，并由独立专家盲审最终报告。主要结果：在匹配的GO决策上执行级路由准确率平均为92%，但在NO-GO决策上仅19%，任何被禁止的下游计算均计为路由错误；轨迹显示智能体常先报告正确诊断，随后仍执行这些结果所禁止的分析。对11个受审智能体的盲审估计，在到达的NO-GO决策中有47%的报告基于无效证据行动，置信区间为31%至61%。显式停止许可对部分模型有帮助，但不能在GO和NO-GO分叉处一致恢复正确决策。此外，16个生命科学任务（批量RNA-seq和病例对照GWAS）表明该框架可评估工业流程之外的证据依赖决策。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三。其一，评测集中于DMAIC工业流程与少量生命科学任务，未来可扩展到更多领域（如临床、金融风控），检验“证据驱动停止”能力的领域泛化性。其二，论文只测“是否按证据行动”，未深入分析失败机理：为何模型能正确报告诊断却仍执行被禁止的下游计算，是规划与执行解耦、工具调用惯性还是上下文遗忘所致，值得做消融与轨迹级归因。其三，干预手段有限，显式停止许可效果不稳定，可探索在Agent架构层面引入前置条件校验器、证据-动作一致性约束或轻量强化学习，使“自我约束”内化为策略而非提示。此外，配对反事实任务可进一步细化为多级部分失败场景，并研究误停（过度保守）与漏停的代价权衡。

### Q6: 总结一下论文的主要内容

论文针对多阶段分析任务中LLM智能体能否依据中间证据决定继续、转向或停止这一问题，提出“自我约束”能力概念，即计算证据是否真正改变下一步行动，区别于仅对输出进行批判的自我反思。为此作者构建DMAIC-Bench基准，基于精益六西格玛的显式统计前提，包含15个工业案例、97个任务，并设置40对反事实变体，在同一流程位置要求相反动作，以区分合理停止与盲目拒绝；同时用私有评分器检查执行轨迹，并由独立专家评审最终结论。对13个模型的评估显示，匹配的继续决策准确率平均92%，而禁止继续决策仅19%，且智能体常在正确报告诊断后仍执行被禁止的分析；专家评审估计47%的到达禁止决策仍基于无效证据行动。论文还验证了该框架可扩展到RNA-seq和GWAS等生命科学任务，揭示了智能体自我约束的显著缺口。
