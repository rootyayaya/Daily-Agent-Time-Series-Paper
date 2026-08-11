---
title: "GALA: Graph-Augmented LLM Agents for Root Cause Analysis and Incident Response in Microservices"
authors:
  - "Yifang Tian"
  - "Yaming Liu"
  - "Zichun Chong"
  - "Zihang Huang"
  - "Yiran Li"
  - "Hans-Arno Jacobsen"
date: "2026-08-10"
arxiv_id: "2608.08968"
arxiv_url: "https://arxiv.org/abs/2608.08968"
pdf_url: "https://arxiv.org/pdf/2608.08968v1"
categories:
  - "cs.SE"
  - "cs.AI"
tags:
  - "LLM Agent"
  - "Root Cause Analysis"
  - "Microservices"
  - "Graph-Augmented"
  - "Multi-modal Telemetry"
  - "Incident Response"
  - "SURE-Score"
  - "Trace and Graph Structure"
  - "Diagnosis"
  - "Actionable Recommendations"
relevance_score: 8.5
---

# GALA: Graph-Augmented LLM Agents for Root Cause Analysis and Incident Response in Microservices

## 原始摘要

Microservice root cause analysis (RCA) requires correlating failures across heterogeneous telemetry within complex service dependency graphs. Existing methods often rely on a single telemetry modality; recent LLM-based approaches can suffer from unconstrained exploration and hallucination; and most systems stop at fault ranking without producing actionable incident response. We present GALA+, a graph-augmented LLM agentic framework centered on graph-guided investigation, which uses service dependencies to bound exploration and refine diagnosis through localized multi-modal evidence. For initial hypothesis generation, GALA+ combines complementary telemetry signals with STRIX, a novel trace- and graph-structure-aware scoring module. GALA+ then produces ranked diagnoses, incident summaries, and stratified action recommendations. We further introduce SURE-Score, a human-guided evaluation framework co-developed with industry SRE experts for assessing RCA-specific output quality beyond conventional text similarity metrics. On two microservice benchmarks, GALA+ consistently achieves the strongest overall results, surpassing the best LLM-based baseline by more than 25 percentage points in AC@1, while also receiving the highest ratings from both SURE-Score and independent human SRE evaluation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

微服务架构的广泛采用带来了复杂的运维挑战：当故障发生时，告警服务往往并非真正根因，需要跨服务依赖图关联多模态遥测数据才能定位。现有方法存在三方面不足：一是统计方法仅依赖单一模态或静态启发式，无法捕捉动态故障模式；二是多模态融合方法将异构数据压缩为统一表示，丢失了区分传播受害者和真实根因的模态特异性信号；三是基于LLM的智能体推理缺乏拓扑约束，容易在全局服务空间中无界探索，导致高搜索开销、幻觉和假设漂移。此外，大多数系统止步于故障排序，无法生成可操作的应急响应，且现有NLG评估指标（如BLEU、ROUGE）无法衡量因果合理性和运维特异性。

本文核心问题是：如何设计一个拓扑约束的LLM智能体框架，在服务依赖图引导下进行有界探索，融合多模态证据生成精准的根因排序，同时输出结构化的故障传播解释和分层处置建议，并建立面向RCA场景的专用评估体系。GALA+通过图引导调查机制和STRIX评分模块解决上述问题，在基准测试中AC@1显著超越最强基线25个百分点以上。

### Q2: 有哪些相关研究？

在方法层面，相关工作可分为三类。第一类是统计与启发式方法，如基于指标相关性、拓扑传播的故障定位，但多依赖单一模态或静态规则，难以捕捉动态故障模式。第二类是多模态融合方法，将指标、日志、追踪等异构数据统一表征，但可能丢失区分传播受害节点与真实根因的模态特定信号。第三类是LLM/Agent方法，如ReAct、Chain-of-Thought等，虽具备多步推理能力，但无约束探索易导致搜索空间过大、幻觉和假设漂移。GALA+的核心区别在于：用服务依赖图约束Agent探索边界，结合指标排序与STRIX追踪-拓扑评分生成双信号候选集，并输出分层处置建议，而非仅做根因排序。

在评测层面，现有工作多采用BLEU、ROUGE等文本相似度指标，无法评估因果合理性与运维可操作性。本文与SRE专家共同提出SURE-Score，从因果性、可解释性、操作具体性等维度评估RCA输出质量，填补了该评测缺口。

在应用层面，本文聚焦微服务RCA与事件响应，与仅做故障定位的系统不同，GALA+同时生成根因排名、事件摘要和分层行动建议，直接支持SRE的完整处置流程。

### Q3: 论文如何解决这个问题？

GALA+通过一个四阶段的图增强LLM智能体框架来解决微服务根因分析中的多模态关联、探索失控和缺乏可操作响应等问题。整体框架围绕服务依赖图约束探索过程，将原始遥测数据逐步转化为根因洞察和修复建议。

第一阶段（初始假设生成）采用双模态互补策略：基于指标使用BARO方法通过贝叶斯在线变点检测和因果DAG构建异常传播路径；同时提出创新的STRIX模块，从分布式追踪中构建加权依赖图，计算三个诊断维度——不稳定性（P99/P50尾部延迟比）、中心性（PageRank加权扇入扇出比）和影响度（自身处理延迟占比），并通过倒数排名融合生成拓扑驱动的排序。随后由整合智能体处理两种排序的不对称信息，生成带置信度的统一排名。

第二阶段（Pod中心上下文合成）将每个候选Pod的指标序列化为JSON、提取一跳依赖子图、经LogDistiller过滤日志，组装成token高效的诊断包。第三阶段（图引导智能体推理）并行派发调查智能体，基于诊断包评估根因置信度，若证据不足则按批次随机探索依赖邻居，通过共享记忆累积评估结果，形成有界搜索。第四阶段输出最终排名、事件摘要和分层修复建议。

创新点在于STRIX的图结构感知评分、整合智能体的跨模态证据溯源，以及图约束的定向探索机制，有效避免了传统LLM方法的幻觉和无约束搜索问题。

### Q4: 论文做了哪些实验？

论文在OnlineBoutique（OB）和TrainTicket（TT）两个微服务基准数据集上评估GALA+，分别包含90个故障场景（6种故障类型），另在AegisLab基准（25种故障类型，100个样本）上补充验证。实验使用7种LLM（含GPT-4.1-mini默认骨干、Gemini、Claude等），默认参数为并行分支k=6、剪枝阈值θ=0.6、批大小b=2。

对比方法分两类：非LLM基线（Granger、CausalRCA、BARO、CIRCA、RCD等）和LLM基线（mABC、Flow-of-Action、RCA-Agent、GraphRAG、ReAct等）。主要结果：GALA+在OB上AC@1达74.44%、AC@3达98.89%、MRR为0.854；在TT上AC@1达73.33%、AC@3达85.56%、MRR为0.801，全面超越所有基线。相比最强LLM基线Flow-of-Action（OB上48.35% AC@1），提升超过25个百分点；相比最强非LLM基线CIRCA（OB上66.67% AC@1）和BARO（TT上66.67% AC@1），分别提升7.77和6.66个百分点。消融实验验证各组件贡献，LLM选择实验考察性能与成本权衡，参数敏感性实验分析agentic investigation阶段设置的影响。

### Q5: 有什么可以进一步探索的点？

GALA+在微服务根因分析上取得了显著进展，但仍存在若干可探索的方向。首先，其评估依赖OB和TT两个基准，故障类型有限（六种），且AegisLab仅测试了100个案例，缺乏对罕见、复合故障及真实生产环境的验证，未来可扩展至更丰富、动态的故障场景。其次，图引导的探索虽约束了搜索空间，但可能过度依赖服务依赖图的准确性，当图谱本身存在缺失或动态变化时，诊断性能可能下降，可探索动态图更新或不确定性感知的图推理。第三，当前动作推荐是静态分层的，未考虑修复动作的时序依赖和副作用，未来可引入强化学习或规划算法来生成可执行、可验证的修复策略。此外，SURE-Score虽结合了专家知识，但仍需更多自动化、可扩展的评估维度，以降低人工成本。最后，LLM的推理成本与延迟仍是实际部署的瓶颈，可探索蒸馏小模型或混合推理策略，在保证精度的同时提升效率。

### Q6: 总结一下论文的主要内容

GALA+提出了一种面向微服务根因分析与事件响应的图增强LLM智能体框架。针对现有方法依赖单一遥测模态、LLM推理易产生幻觉与无界探索、以及多数系统止步于故障排序而缺乏可执行响应等核心问题，该框架以服务依赖图约束智能体推理路径，结合基于指标的相关性排序与STRIX评分模块（利用追踪模式和依赖拓扑）生成互补的候选假设集，并通过并行图引导调查机制沿故障传播边进行置信度驱动、深度受限的局部搜索。最终输出排序诊断、结构化事件摘要及分层行动建议。此外，作者与SRE专家共同设计了SURE-Score评估框架，用于衡量RCA输出的因果依据与操作特异性。在OnlineBoutique和TrainTicket两个基准上，GALA+的AC@1分别达74.44%和73.33%，较最优LLM基线提升超25个百分点，并在自动化与人工评估中均获最高评分。该工作统一解决了跨模态关联、拓扑约束推理与可操作响应生成三大挑战，为LLM在可靠性工程中的落地提供了新范式。
