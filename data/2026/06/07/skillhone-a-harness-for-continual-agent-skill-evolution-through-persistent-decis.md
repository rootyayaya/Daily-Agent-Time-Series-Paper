---
title: "SkillHone: A Harness for Continual Agent Skill Evolution Through Persistent Decision History"
authors:
  - "Zhiwei Li"
  - "Yong Hu"
date: "2026-06-07"
arxiv_id: "2606.08671"
arxiv_url: "https://arxiv.org/abs/2606.08671"
pdf_url: "https://arxiv.org/pdf/2606.08671v1"
categories:
  - "cs.LG"
tags:
  - "Agent Skill Evolution"
  - "Persistent Decision History"
  - "Continual Learning"
  - "Self-Improvement"
  - "Feedback Optimization"
  - "Multi-Agent Reasoning"
  - "Skill-MoE"
  - "Tool Use"
  - "LLM Agent"
  - "Evidence Routing"
relevance_score: 7.5
---

# SkillHone: A Harness for Continual Agent Skill Evolution Through Persistent Decision History

## 原始摘要

Agent skills extend language-model agents with task-specific procedures, scripts, and references, but the tasks and environments they target continually change. Existing methods improve skills in bounded runs and retain only the final artifact, discarding the decision history that later agents need to interpret prior revisions, evaluations, and rejected alternatives. We introduce SkillHone, a harness for continual agent skill evolution grounded in persistent decision history. SkillHone pairs skill revisions with evaluation-side evidence that supplies practice feedback, recording structured histories of diagnoses, revisions, evidence, and outcomes. Role-separated subagents run candidate skills on practice probes with redacted reporting and propose revisions informed by prior decisions, enabling cross-session refinement without rediscovering past rationale. We evaluate SkillHone on deep-research benchmarks in a raw open-web setting, where agents are not given an integrated search stack and must organize retrieval through portable skills. We compare against a deep-research agent backed by commercial retrieval services. With Qwen3.6-35B-A3B as the evaluation-time backbone, the resulting skills outperform the deep-research agent by 15.8 points on GAIA and 3.2 points on WebWalkerQA-EN, while also exceeding prior skill-evolution methods.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决现有智能体技能进化方法中，由于缺乏持久性决策历史而导致后续维护困难的核心问题。研究背景是，基于大语言模型的智能体通过“技能”（即任务特定的程序、脚本和参考）来扩展能力，但实际部署环境（如API、任务分布）会持续变化，技能需要不断维护和优化。现有方法（如Skill-Creator和Hermes-SE）存在明显不足：它们将技能改进视为一个“有界运行”，只保留最终优化后的技能工件，而丢弃了中间决策历史。这导致后续的智能体在继承最新技能时，无法理解之前修订的动机（如为何诊断某个故障、为何拒绝某些备选方案、以及评估证据如何支撑最终结果），从而可能重复已修复的错误、撤销有用的改动，或基于已过时的反馈继续优化。因此，本文要解决的核心问题是：如何构建一个框架，使得智能体能够在多个开发会话中持续改进技能，同时保留并利用完整的决策历史（包括诊断、修订、评估证据和结果），避免因历史信息丢失导致的低效或退化。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是智能体技能获取与优化，如自动化技能发现、强化学习进化及领域特定技能构建。这些工作聚焦于如何获得有用技能或衡量技能对任务性能的提升，而SkillHone关注技能已存在后，如何随着任务、工具和故障模式变化持续维护，并保留优化上下文以支持未来改进。第二类是提示、系统与技能的优化，包括提示优化、Reflexion式反馈改进、DSPy声明式编译，以及GEPA和Hermes-SE的反思式进化。这些方法在单次优化运行内改进工件，而SkillHone将技能进化视为持续维护过程，后代智能体继承的不只是最新工件，还有结构化的失败、候选修订、评估与结果历史。第三类是多智能体协作与开发工作流，如MetaGPT的角色分工。SkillHone共享角色分离原则，但用于持续技能维护而非一次性工件生产，其子智能体由轻量调度器按需创建，通过权限分离（优化子智能体提议修订，评估子智能体测试并返回脱敏证据）积累可读决策历史，同时减少评估资产向优化侧的泄露。

### Q3: 论文如何解决这个问题？

SkillHone 通过持久化决策历史与角色分离的持续演化框架解决技能退化问题。其核心设计包括两个隔离的仓库：技能仓库存储当前技能包（SKILL.md、脚本、模板等），技能评估仓库存储实践探针、验证器、轨迹和脱敏报告。整体架构由运行时调度器（Dispatcher）动态分配两类子代理：优化子代理（Optimization Subagent）负责诊断失败、提出修订方案并更新技能仓库，但无法访问未脱敏的探针目标或执行轨迹；评估子代理（Evaluation Subagent）运行候选技能、生成脱敏报告，但无权修改技能仓库。这种严格的权限分离防止实践反馈成为直接记忆目标。

关键技术在于将每次开发步骤建模为决策记录 \( h_t = (q_t, r_t, e_t, o_t) \)，其中 \( q_t \) 为诊断，\( r_t \) 为候选修订，\( e_t \) 为脱敏评估证据，\( o_t \) 为接受/拒绝/修订/延迟结果。所有历史记录构成持久决策历史 \( \mathcal{H}_t \)，使后续代理能追溯先前修订的原因、被拒绝的替代方案及评估证据，避免重复推导相同诊断。当环境变化时，优化子代理可检索 \( \mathcal{H}_{<t} \) 判断失败是否为新问题、类似修复是否已尝试过，从而支持跨会话的持续技能演化。

创新点包括：1）用决策记录替代传统版本差异，将文件变更与问题定位、评估证据和决策结果关联；2）通过运行时调度器实现优化与评估的对称隔离，确保实践反馈不直接泄露探针信息；3）持久化历史使代理能审计先前变更并继续改进，无需重新推导诊断。实验表明，基于Qwen3.6-35B-A3B的SkillHone在GAIA和WebWalkerQA-EN上分别超越商业检索驱动的深度研究代理15.8和3.2个百分点。

### Q4: 论文做了哪些实验？

论文在GAIA和WebWalkerQA-EN两个开放域基准上评估了SkillHone。实验设置包括两种场景：**Curated search**（使用商业检索服务的深度研究agent）和**Raw open-web**（无预集成搜索工具，仅通过公共网页和可移植技能包运行）。Raw open-web场景下，所有系统共享同一初始技能池，对比方法包括：直接使用现有技能（Existing-Skills）、内置迭代优化（Skill-Creator）、反思式优化（Hermes-SE）以及SkillHone。开发时控制器为Claude Opus 4.6，执行和评估骨干为Qwen3.6-35B-A3B。

主要结果：在GAIA上，SkillHone平均准确率达64.6%，比深度研究agent高15.8个百分点；在WebWalkerQA-EN上达66.4%，高3.2个百分点。在Raw open-web对比中，SkillHone比Skill-Creator在GAIA和WebWalkerQA-EN上分别提升20.5和28.3个百分点，比Hermes-SE提升14.2和13.4个百分点。增益在困难子集上最为显著，表明SkillHone优化了任务执行流程而非仅检索能力。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是仅针对英文基准测试，缺乏多语言泛化验证；二是当前只支持单一技能的独立演化，无法处理多个相互依赖技能的协同进化；三是评估场景局限于开放网络环境，未涉及工业故障诊断等更复杂的实际应用。未来可探索的方向包括：将SkillHone扩展到多语言环境，验证其跨语言迁移能力；设计多技能联合演化机制，通过技能间的依赖图谱和冲突检测实现协同优化；引入工业时序数据作为实践反馈，结合可解释性分析增强诊断透明度。此外，当前方法依赖固定角色分离的子代理，可尝试引入动态角色分配或元学习策略，使技能演化更适应环境变化。决策历史的持久化存储也可进一步压缩，通过注意力机制筛选关键历史片段，减少冗余计算。

### Q6: 总结一下论文的主要内容

SkillHone提出了一种持续智能体技能演化的框架，解决了现有方法仅保留最终技能而丢弃决策历史的问题。该方法将技能视为可演化的知识包，通过分离角色子智能体（优化与评估）在实践探针上运行候选技能，并记录包含诊断、修订、证据和结果的结构化决策历史。评估时，子智能体基于历史决策提出修订，避免重复发现过往推理。在原始开放网络环境下的深度研究基准测试中，SkillHone无需预集成搜索工具，通过便携技能组织检索。以Qwen3.6-35B-A3B为评估骨干，其技能在GAIA和WebWalkerQA-EN上分别超越商业检索支持的深度研究智能体15.8和3.2个百分点，并优于先前技能演化方法。核心贡献在于证明持久决策历史能帮助智能体将实践反馈转化为更强的技能包，实现跨会话的持续改进。
