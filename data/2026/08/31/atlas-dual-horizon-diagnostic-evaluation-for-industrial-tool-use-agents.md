---
title: "ATLAS: Dual-Horizon Diagnostic Evaluation for Industrial Tool-Use Agents"
authors:
  - "Wei Chen"
  - "Peilun Zhou"
  - "Zhaoyu Hu"
  - "Jiajun Chai"
  - "Zhongni Hou"
  - "Yufei Zhang"
  - "Derong Xu"
  - "Guojun Yin"
  - "Wei Lin"
  - "Zhi Zheng"
  - "Tong Xu"
date: "2026-08-31"
arxiv_id: "2608.30685"
arxiv_url: "https://arxiv.org/abs/2608.30685"
pdf_url: "https://arxiv.org/pdf/2608.30685v1"
categories:
  - "cs.AI"
tags:
  - "LLM Agent 评估"
  - "工具调用诊断"
  - "双视野评估框架"
  - "工业应用"
  - "轨迹级诊断"
  - "交互级诊断"
  - "LLM judge 校准"
  - "策略优化"
relevance_score: 7.5
---

# ATLAS: Dual-Horizon Diagnostic Evaluation for Industrial Tool-Use Agents

## 原始摘要

Large language model (LLM) agents are increasingly deployed in user-facing services that require iterative tool use under dynamic business conditions. Reliable evaluation is essential for sustained improvement: it must reveal capability deficiencies, inform priorities, and assess interventions. Yet industrial agent service unfolds both through the iterative trajectory of a current request and through continued user interaction. Final-outcome assessment can therefore obscure where deficiencies arise and whether later service remains aligned with context from earlier exchanges. We propose ATLAS, a dual-horizon diagnostic evaluation framework for industrial tool-use agents. At the request horizon, trajectory-wise diagnostic signals relate deficiencies to execution locations and capability concerns. At the interaction horizon, user-wise signals assess whether service remains responsive across continued interaction. Together, these views provide structured diagnostic evidence for analyzing execution deficiencies and sustained service behavior. ATLAS instantiates them as executable signals with explicit evidence scopes and decision boundaries. LLM judge interfaces are calibrated against high-confidence references from real business logs; when needed, their decision behavior is distilled into efficient diagnostic models for lower-latency, lower-cost evaluation. The resulting feedback supports policy optimization. We evaluate ATLAS on Meituan Xiaotuan production traffic. Offline experiments assess diagnostic-signal fidelity and replay-based policy improvement, while online A/B experiments show concurrent gains in user engagement, downstream business outcomes, and sampled human-audit quality.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

大型语言模型智能体在工业场景（如美团小团）中部署时，现有评估方法主要依赖最终任务结果或单轮交互质量，无法满足持续迭代优化的需求。其不足体现在三方面：一是执行轨迹中的复合错误难以定位，早期偏差会累积影响最终服务；二是动态业务条件下，看似合理的响应可能掩盖过时或不准确的信息；三是跨轮交互中，上下文（如用户意图、约束、修正）的延续性未被评估，导致服务偏离用户需求。因此，本文提出ATLAS双视野诊断评估框架，核心解决两个问题：在请求视野内，通过轨迹级诊断信号定位执行位置（如思考反思、工具调用、响应生成）及能力缺陷（如相关性、事实性、及时性），明确“哪里出错”和“为何出错”；在交互视野内，通过用户级信号评估持续服务是否响应演进需求。该框架旨在将诊断证据转化为可执行的优化反馈，支持策略迭代，并通过校准的LLM评判器与蒸馏模型实现高效评估，最终提升工业智能体的服务质量和用户参与度。

### Q2: 有哪些相关研究？

ATLAS的相关研究可从三个维度梳理。**方法类**上，AgentEval通过依赖感知DAG对工业工作流进行步骤级评估与故障分析，Agent-RewardBench则聚焦感知、规划、安全等能力的奖励建模；ATLAS区别于它们，将评估对象明确划分为请求级执行轨迹与交互级持续服务，并设计可执行的双视诊断信号。**评测类**中，MobilityBench、MindDR、RecRMBench和CLQT分别在出行、深度研究、推荐和投资管理场景中构建部署对齐的评测基准，RubricsTree针对个人健康智能体提出结构化标准；ATLAS的独特之处在于同时覆盖单次请求内的缺陷定位与跨交互的服务延续性，而非仅关注单一任务片段。**优化类**方面，过程奖励模型为推理步骤分配信用，Rubrics to Tokens将评分标准转化为细粒度训练信号，金融和具身领域也采用多维反馈进行闭环强化学习；ATLAS则强调校准后的诊断信号作为“语义接口”贯穿评估-优化-再评估的完整循环，使信号在迭代中保持诊断意义，而非仅作为聚合报告或单一奖励。整体上，ATLAS整合了过程敏感分析、部署对齐评测与多维反馈优化，但以双时间视界和信号连续性为核心创新。

### Q3: 论文如何解决这个问题？

ATLAS通过双时间尺度诊断评估框架解决工业工具使用代理评估中的核心问题：传统最终结果评估无法定位缺陷来源，也无法判断后续服务是否与早期交互上下文保持一致。

整体框架包含两个核心模块：请求级（request horizon）和交互级（interaction horizon）诊断。请求级采用结构化诊断矩阵，以执行维度（思考与反思、工具与技能执行、响应生成）为横轴，能力关注点（相关性、事实性、时效性、可靠性、意图与规划）为纵轴，交叉点实例化为细粒度诊断信号，每个信号具有明确的证据范围和决策边界。规范与合规作为独立护栏单独维护。交互级则作为独立的用户级层，评估先前上下文在后续推理、工具使用和响应中是否被正确解析、维护或修正。

关键技术包括：信号实现采用规则与LLM双机制，规则信号处理可编程验证的边界，LLM信号处理需要开放语义推理的场景，提示词包含角色定义、输入规范、决策标准、审查流程和结构化输出五部分。校准流程使用F1指标（阈值0.90）在真实业务日志构建的高置信参考集上验证LLM判断器，通过边界精炼迭代优化。为降低推理成本，采用分组蒸馏策略，按执行维度、能力关注点和输入输出形式三个因素将兼容信号分组，训练高效诊断模型。诊断分数通过局部对象评估聚合形成，保持可解释性。

创新点在于双时间尺度诊断结构、显式证据范围与决策边界的信号设计、以及基于真实流量校准的LLM判断器与蒸馏模型的结合，最终支持策略优化。

### Q4: 论文做了哪些实验？

论文围绕ATLAS框架开展了四组实验（RQ1-RQ4）。实验基于美团小团生产流量构建三个互斥数据集：诊断信号基准集（含41个LLM信号，每信号500-1000条带高置信标签）、离线策略评估集（约2000条查询）和RL优化集（约10000条查询），并采用部署对齐的离线重放环境（真实查询回放、生产接口执行工具调用）。

RQ1比较LLM裁判接口设计，在相同DeepSeek-V4-Pro骨干下，ATLAS Judge（含证据绑定、逐步审查、约束输出）在全部信号组上平均F1达0.952，显著优于Direct Judge（0.800）、Static Rubric（0.826）和Curated Rubric（0.877），尤其在Timeliness（0.961）和Norms & Compliance（0.984）上优势明显。RQ2将17个选定信号蒸馏至Qwen3.5-9B，相比未调优基线平均提升13.2%，部分信号（如Location Constraint）提升达29.2%，接近DeepSeek-V4-Pro教师性能。RQ3在离线重放中验证诊断反馈可提升策略质量（ATLAS分数聚合）。RQ4在线A/B测试显示用户参与度、下游业务指标（如AI消息阅读率、人均停留时长、5秒退出率、有效QV、会话追问率、付费GTV）及人工审计质量（P0幻觉率、ID幻觉率、响应-供给相关性）均获同步改善。所有实验在NVIDIA H20 GPU上运行，RL优化使用Qwen3.6-35B-A3B（32卡，Verl+Megatron+vLLM）。

### Q5: 有什么可以进一步探索的点？

**进一步探索的点：**

论文的ATLAS框架在双视野诊断上表现优异，但仍存在可拓展空间。首先，**信号覆盖的完备性**——当前41个LLM诊断信号虽覆盖六类能力，但未涉及多轮对话中的情感一致性、用户满意度预测等软性指标，可引入用户反馈信号作为补充。其次，**高效诊断模型的泛化性**——蒸馏模型在特定业务场景表现好，但跨领域（如外卖到酒店）迁移能力未知，可探索基于元学习的跨域适配。第三，**诊断信号的动态演化**——业务规则和用户意图随时间变化，静态决策边界可能过时，建议引入在线学习机制定期校准。第四，**多智能体协作场景**——当前评估单智能体，未来可扩展到多智能体协同诊断，分析交互故障的归因。最后，**可解释性增强**——诊断信号虽定位到轨迹位置，但未提供根因推理链，可结合因果推断或思维链生成修复建议，提升反馈的可操作性。

### Q6: 总结一下论文的主要内容

ATLAS提出了一种面向工业工具使用型智能体的双视野诊断评估框架，旨在解决现有评估仅关注最终结果而无法定位能力缺陷的问题。该框架在请求视野内，通过轨迹级诊断信号将缺陷映射到执行位置（如思考反思、工具执行、响应生成）和能力维度（如相关性、事实性、时效性）；在交互视野内，通过用户级信号评估跨轮次服务的持续响应性。ATLAS将诊断结构实例化为具有明确证据范围和决策边界的可执行信号，利用真实业务日志校准LLM评判接口，并可将部分信号蒸馏为高效诊断模型以降低延迟和成本。在美团小团生产流量上的离线实验验证了诊断信号保真度和基于回放的政策优化效果，在线A/B实验显示优化后的策略在用户参与度、下游业务成果和人工审计质量上均有提升，为工业智能体提供了可操作的迭代优化闭环。
