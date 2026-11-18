---
title: "An Explainable Agentic AI Framework for Distribution System Load Restoration"
authors:
  - "S. M. Monzurul Hoque Chowdhury"
  - "Qinghua Li"
date: "2026-11-17"
arxiv_id: "2611.22016"
arxiv_url: "https://arxiv.org/abs/2611.22016"
pdf_url: "https://arxiv.org/pdf/2611.22016v1"
categories:
  - "eess.SY"
tags:
  - "多智能体系统"
  - "LLM智能体"
  - "可解释AI"
  - "决策仲裁"
  - "记忆反馈"
  - "解释生成"
  - "电力系统恢复"
  - "时序决策"
  - "可行性验证"
  - "工业诊断"
relevance_score: 7.5
---

# An Explainable Agentic AI Framework for Distribution System Load Restoration

## 原始摘要

Distribution system load restoration is a sequential decision-making problem in which restoration actions must maximize served load, prioritize critical loads, and preserve power-flow feasibility. This paper proposes an explainable agentic artificial intelligence (AI) framework for distribution system load restoration. The proposed framework uses multiple large language model (LLM) agents for planner guidance, strategic plan generation, decision arbitration, memory-based feedback, and explanation generation. Unlike unconstrained LLM-based control, the proposed method restricts agent decisions to feasible restoration actions and evaluates all candidate plans using deterministic AC power-flow feasibility checks. The framework is evaluated on IEEE 33-bus and 69-bus distribution feeders, as well as a larger IEEE 118-bus test case, and compared against reinforcement learning and planning baselines. The results show that the proposed agentic framework achieves better restoration performance while producing structured explanations for operator-facing decision support. A direct comparison with a Single-LLM-Agent baseline further shows that the proposed multi-agent decomposition improves weighted restored load and critical-load recovery compared with a monolithic LLM decision structure.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决配电网故障后负荷恢复过程中，如何兼顾恢复决策质量与运行人员可解释性的问题。研究背景是：配电网在故障、停电或极端天气后，需要按顺序决定负荷供电、馈线修复、联络开关操作和分布式电源启动等动作，目标是最大化恢复负荷、优先保障关键负荷，同时避免电压越限、线路过载和潮流不可行。现有方法中，优化与图搜索方法决策严谨但依赖详细建模，在大规模停电场景下计算代价高；强化学习等学习方法虽能适应场景，却难以向运行人员提供清晰解释。近年来大语言模型为推理型决策支持带来新机会，但直接把 LLM 当作电网控制器存在明显不足：其输出可能包含无效动作、忽略物理约束，无法保证可行性，并带来可靠性与安全性风险。因此，本文的核心问题是：如何构建一个受约束的智能体框架，使 LLM 仅负责计划级推理与解释，而所有候选动作均限制在可行动作集合内，并通过确定性 AC 潮流校验保证执行可行性；同时通过多智能体分解（规划引导、策略生成、决策仲裁、记忆反馈和解释生成）提升恢复性能，并为运行人员提供结构化决策依据。

### Q2: 有哪些相关研究？

本文的相关研究主要可分为三类。方法类方面，配电网恢复已有数学优化（鲁棒优化、随机规划）、图搜索、规则方法、强化学习及混合学习-控制方法；其中图强化学习用于序贯恢复，强化学习还用于关键负荷恢复、微网辅助恢复与网络重构，多智能体深度强化学习结合无效动作掩码或动作空间约简提升恢复与重构决策。这些工作侧重学习控制策略，而非LLM规划、记忆与面向操作员的解释。优化与混合方法为恢复可行性、关键负荷恢复提供基础，但多不提供结构化自然语言理由。应用与工具类方面，LLM已被用于电力系统仿真、分析、优化、图推理、自主研究工作流与多智能体求解器协调，表明连接外部工具与确定性求解器后LLM可支持电力任务。评测与框架类方面，ReAct、AutoGen、CAMEL、Reflexion、Toolformer、HuggingGPT等LLM智能体框架展示了推理、多智能体协调、工具使用、反馈与任务编排能力，但均未处理可行动作约束与AC潮流可行性下的负荷恢复。本文区别在于首次提出受约束的可解释智能体LLM恢复框架，将可行动作生成、拓扑感知动作筛选、多步规划、确定性AC潮流校验、记忆反馈与操作员解释集成于物理感知恢复回路，并与单LLM智能体基线对比验证多智能体分解优势。

### Q3: 论文如何解决这个问题？

论文的核心思路是把LLM从“不受约束的电网控制器”降级为“受限恢复回路中的高层推理器”，用确定性模块守住可行性与物理安全边界。整体框架按“状态→可行动作生成→拓扑感知动作筛选→LLM多智能体规划→AC潮流评估→执行首个动作→状态与记忆更新→解释输出”的闭环运行，并以滚动时域方式反复迭代。

关键组件包括：可行动作集生成器，基于当前拓扑、线路/负荷/联络开关与DG状态构造硬约束动作集，LLM只能从中选择，禁止虚构母线、线路或开关；拓扑感知筛选器，用即时优先级加权恢复量、未来可达负荷增量与关键负荷指示三项加权打分，将候选动作压缩为短名单；五个LLM智能体分工协作——规划引导智能体给出动作偏好与规划时域等软偏置，战略规划智能体仅用短名单动作生成多条多步恢复计划，决策智能体在评估后的计划间仲裁，记忆智能体反馈成功/失败动作与风险模式，解释智能体输出结构化决策解释；确定性AC潮流评估模块在克隆环境中逐条仿真候选计划，校验收敛性、电压与线路负载率约束，仅执行选中计划的第一步。

创新点在于：将动作合法性、候选筛选、计划级推理与物理可行性验证解耦，使LLM专注高层恢复推理与解释；以“先筛选、后规划、再潮流校验”的流水线替代LLM对组合动作空间的暴力搜索；多智能体分解相较单一LLM智能体提升了加权恢复负荷与关键负荷恢复率，同时生成面向运行人员的可解释决策依据。

### Q4: 论文做了哪些实验？

论文在IEEE 33节点、69节点和118节点三个配电馈线系统上评估框架，全部基于pandapower实现。每个系统生成250个恢复场景，划分为200个训练、25个验证和25个测试场景，训练与验证仅用于学习型基线，所有方法在相同的25个留出测试场景上配对评估。恢复过程受有限动作预算约束，分别在T_max=10和T_max=15下测试。可行性检查采用AC潮流，电压约束0.95≤V_i≤1.05、支路负载率≤100%。评价指标为加权恢复负荷L_w和关键负荷恢复量P_crit。对比方法包括DQN-RL、ActorCritic-RL、MCTS-Rollout以及SingleLLMAgent消融基线。主要结果显示，所提方法在全部六种设置下均取得最高L_w，并在六种设置中的五种取得最高P_crit，其余一种与MCTS-Rollout持平。例如IEEE 33节点在T_max=10时L_w为2.82、P_crit为0.53，优于MCTS的2.73/0.50和DQN的1.94/0.27；IEEE 118节点在T_max=15时L_w达4.63、P_crit为0.94。与SingleLLMAgent的对比表明多智能体分解优于单一LLM决策结构。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点：其一，实验仅在标准 IEEE 33/69/118 节点馈线上离线评估，缺乏真实配电网的量测噪声、通信延迟与拓扑动态变化验证，未来可接入硬件在环或实际馈线数据检验鲁棒性；其二，LLM 智能体层依赖结构化 JSON 解析，文中已提及解析失败问题，可探索输出校验、重试与回退机制，并量化推理时延与 token 成本对恢复时限的影响；其三，AC 潮流校验虽保证可行性，但每次候选评估计算开销较大，可研究代理模型或灵敏度筛选加速候选动作生成；其四，多智能体分解的增益目前仅与单 LLM 基线对比，未来可做消融分析各角色贡献，并探索与 RL/MCTS 的混合架构；其五，解释生成的质量尚缺人工评估，可引入调度员用户研究验证解释的可信度与可操作性。

### Q6: 总结一下论文的主要内容

论文针对配电系统故障后的负荷恢复这一顺序决策问题，提出一种可解释的智能体式AI框架。问题定义为在有限时域内选择恢复动作序列，以最大化优先级加权恢复负荷、优先保障关键负荷，并满足AC潮流可行性约束。方法上，框架将恢复推理分解为多个LLM智能体，分别负责规划引导、策略计划生成、决策仲裁、基于记忆的反馈和解释生成；LLM不直接充当无约束电网控制器，其决策被限制在环境提供的可行动作集内，并经过拓扑感知动作筛选和确定性AC潮流校验后才执行，形成滚动时域闭环。主要结论：在IEEE 33、69和118节点系统上，该方法在加权恢复负荷和关键负荷恢复上均优于强化学习、MCTS前瞻搜索及单LLM智能体基线，同时能为调度人员生成结构化决策解释，兼顾了恢复性能、物理安全性与可解释性。
