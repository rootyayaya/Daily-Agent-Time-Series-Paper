---
title: "Explainable Post-Disaster Grid Observability Recovery Using Human-Oversight Agentic LLMs"
authors:
  - "Biswas Rudra Jyoti Arka"
  - "Sadman Sakib"
  - "Md. Zahidul Islam"
  - "Shamsun Nahar Edib"
date: "2026-09-15"
arxiv_id: "2609.16774"
arxiv_url: "https://arxiv.org/abs/2609.16774"
pdf_url: "https://arxiv.org/pdf/2609.16774v1"
categories:
  - "eess.SY"
tags:
  - "Agentic Time Series"
  - "LLM Agent"
  - "Tool Calling"
  - "可解释性"
  - "故障诊断"
  - "工业传感器"
  - "电力系统"
  - "PMU恢复"
  - "人类监督"
  - "可追溯诊断链"
relevance_score: 8.5
---

# Explainable Post-Disaster Grid Observability Recovery Using Human-Oversight Agentic LLMs

## 原始摘要

Post-disaster phasor measurement unit (PMU) outages reduce power-system observability and degrade operator situational awareness, requiring sequential restoration under limited resources. Existing PMU restoration methods based on optimization or heuristics can generate restoration schedules, but they often provide limited support for explanation, traceability, and operator interaction. This paper proposes an agentic tool-calling framework orchestrated by a large language model (LLM) for post-disaster PMU restoration and grid observability recovery. In this framework, the LLM does not directly solve the restoration optimization problem; instead, it coordinates validated backend tools required for post-disaster restoration, including observability assessment, restoration planning, state updates, and operator verification. The framework also maintains a structured tool-call history and execution context that keep restoration decisions traceable and explainable, while enabling context-aware operator question answering during the restoration process. Simulation results on IEEE 30-bus and IEEE 57-bus systems show that the proposed framework achieves observability recovery comparable to a mixed-integer linear programming (MILP) solution, while providing tool-grounded explanations, interactive operator support, and human-overseen execution.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决灾后电力系统相量测量单元（PMU）故障后，如何在有限资源下进行序贯恢复并保持电网可观测性的问题。研究背景是：飓风、山火或网络物理攻击等极端事件可能导致多个PMU同时失效，而PMU提供的GPS同步相量数据是广域监测、状态估计和保护控制的关键基础。一旦多个PMU失效，系统可观测性急剧下降，调度员在最需要态势感知的灾后时刻反而“失明”。由于抢修人员、备件和通信资源有限，PMU无法一次性全部恢复，因此恢复顺序直接决定可观测性恢复的速度，本质上是一个序贯决策问题。现有方法主要依赖混合整数线性规划、贪心算法或启发式方法，虽然能计算出恢复序列，但通常作为独立优化模块运行，只输出恢复决策，缺乏对决策原因的解释、过程的可追溯性以及与调度员的交互能力。在实际灾后运行中，调度员往往需要理解为何某个PMU或区域被优先恢复，并融入自身经验进行人工监督。因此，本文要解决的核心问题是：在保证可观测性恢复效果不劣于MILP的前提下，构建一个面向调度员的、可解释、可追溯、可交互且支持人工监督的PMU恢复决策支持框架，而非仅仅输出一个恢复序列。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，现有PMU恢复方法多基于混合整数线性规划（MILP）、贪心算法或启发式方法，能在目标函数与约束明确时有效计算恢复序列，但通常作为独立优化模块运行，缺乏解释、追溯与交互支持。应用类方面，近期已有研究将智能体AI（Agentic AI）用于电力系统分析任务，如交流最优潮流、预想事故分析和互联研究，但尚未涉及传感器恢复问题。评测类方面，本文在IEEE 30节点和57节点系统上，将所提框架与MILP解进行对比，验证其在可观测性恢复上的相当性能。

与上述工作的关系和区别在于：本文不直接用LLM求解恢复优化问题，而是将LLM作为工作流编排器与解释接口，通过受控工具调用协调可观测性评估、恢复规划、状态更新和操作员验证等后端工具，并维护结构化工具调用历史与执行上下文。相比传统MILP或启发式方法，本文额外提供了工具支撑的解释、交互式问答和人工监督执行能力；相比已有智能体AI电力系统应用，本文首次将智能体LLM框架拓展至灾后PMU恢复与电网可观测性恢复场景。

### Q3: 论文如何解决这个问题？

该论文提出了一种由大语言模型（LLM）编排的智能体工具调用框架，用于灾后PMU恢复与电网可观测性重建。其核心思想是：LLM不直接求解恢复优化问题，而是作为受控的编排接口，协调经过验证的后端确定性工具完成恢复任务。

整体框架包含以下关键组件：**系统指令**定义LLM角色、工具调用顺序、停止条件和接地规则；**用户任务提示**启动具体恢复案例；**LLM智能体**将操作员请求转化为合规的工具调用，并解释工具输出；**执行器**作为LLM与后端函数之间的接口层，验证工具名称与参数、从上下文补全缺失字段、执行后端函数并更新上下文；**后端工具**执行所有数值计算、MILP求解、可观测性检查和状态更新；**上下文记忆**存储工具输入输出、PMU状态、区域评分、预算、已执行动作、可观测性状态及操作员反馈；**人类操作员**在每个恢复动作应用前进行审查、批准或修改。

后端模块化工具包括：partition_network（基于k-medoids聚类进行区域划分）、zone_weights（分配区域重要性权重）、generate_failure_scenario（模拟灾后PMU故障）、compute_zone_scores_and_budgets（计算区域优先级评分并分配恢复预算）、propose_restoration（求解滚动时域MILP并生成恢复方案）、apply_restoration（提交经操作员批准的恢复更新）、check_total_observability（计算区域级和全网可观测性）、evaluate_tieline_observability（检查区间联络线PMU覆盖）。

创新点在于：一是将电力系统恢复计算与LLM编排分离，确保决策基于电力系统物理约束，减少LLM无依据输出；二是维护结构化工具调用历史和双形式上下文（LLM可见消息历史与执行器侧上下文字典），实现决策可追溯与可解释；三是LLM在每次工具调用后基于工具输出生成自然语言理由，解释与恢复步骤同步产生而非事后附加；四是支持操作员在环审查与交互式问答，实现人机协同的恢复执行。

### Q4: 论文做了哪些实验？

论文在IEEE 30节点和57节点系统上进行了多场景仿真验证，考虑30%、50%、70%、90%四种PMU故障率，恢复预算1–4，分区数1–4，MILP预测时域H=3，LLM采用GPT-4o mini。实验包括：一是工具调用轨迹与多轮操作员问答，验证可解释性与交互支持；二是LLM生成理由与人工参考理由的一致性检查，选取57节点3分区预算4故障率90%和30节点4分区预算3故障率90%两个场景，结果显示所有迭代理由均与人工参考的预算分配逻辑一致；三是恢复性能评估，观测到每步恢复后可观性逐步提升直至完全恢复，预算越大所需步数越少，故障率越高步数越多；四是运行时间评估，每步决策仅需数秒，包含LLM编排与后端优化；五是与独立MILP对比，57节点在90%故障率下平均步数差距7.76%，70%故障率下为0%，预算增至3–4时步数差距降至3.57%，30节点系统步数差距为0%且完成率100%；六是消融实验，一次性提示LLM不可靠，无工具迭代LLM需多61%步数，基于LLM预算推理仅提升20–30%可观性，而所提框架实现100%可观性且步骤可追溯。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：一是实验仅基于IEEE 30节点和57节点静态故障场景，未考虑负荷波动、连锁故障、通信延迟等动态运行条件；二是当工具返回不完整结果或MILP求解存在最优性间隙时，框架缺乏明确的兜底与修复机制；三是LLM作为编排器仍带来额外推理开销与潜在幻觉风险。未来可从以下方向探索：其一，引入时序感知的滚动优化与在线学习，使恢复策略适应灾后演化的拓扑与量测变化；其二，设计多智能体分工架构，让规划、验证、解释由不同LLM角色承担并交叉校验，降低单点错误；其三，研究轻量化或蒸馏模型以压缩LLM开销，并建立工具调用可信度评估与不确定性量化机制；其四，将人类监督从“事后确认”扩展为可调节自主级别的混合 initiative 交互，结合认知负荷实验验证其对操作员情境意识的实际提升。

### Q6: 总结一下论文的主要内容

本文针对灾后PMU故障导致电网可观测性下降、现有恢复方法缺乏可解释性与人机交互的问题，提出了一种由大语言模型（LLM）编排的智能体工具调用框架。该框架的核心思路是让LLM不直接求解恢复优化问题，而是作为工作流协调者，调用经过验证的后端工具，包括可观测性评估、恢复规划、状态更新和操作员验证，并维护结构化的工具调用历史与执行上下文，使恢复决策可追溯、可解释，同时支持上下文感知的操作员问答。在IEEE 30节点和57节点系统上的仿真表明，该框架的可观测性恢复效果与混合整数线性规划（MILP）方案相当，同时提供了基于工具的解释、交互式操作支持和人工监督执行能力，为灾后电网恢复提供了一种兼顾性能与可解释性的新范式。
