---
title: "Symbolic Separation: Grounding Deep Agents in Knowledge Graphs for Trustworthy Operational Data Analytics"
authors:
  - "Baibek Davletiyarov"
  - "Junaid Ahmed Khan"
  - "Andrea Bartolini"
date: "2026-09-15"
arxiv_id: "2609.17107"
arxiv_url: "https://arxiv.org/abs/2609.17107"
pdf_url: "https://arxiv.org/pdf/2609.17107v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Knowledge Graph"
  - "Deep Agent"
  - "Operational Data Analytics"
  - "Neurosymbolic"
  - "LLM Tool Use"
  - "Virtual Knowledge Graph"
  - "Data Center Telemetry"
  - "Industry 4.0"
  - "Trustworthy AI"
  - "Symbolic Separation"
  - "Deterministic Validation"
relevance_score: 8.5
---

# Symbolic Separation: Grounding Deep Agents in Knowledge Graphs for Trustworthy Operational Data Analytics

## 原始摘要

Generative AI promises natural language access to the massive numerical telemetry of data centers and Industry 4.0 installations, yet text-to-query and tool-using agents stay unreliable: even frontier models answer little more than half of real-world database questions, and far fewer of the multi-step, operational ones, because the LLM must compose how heterogeneous sources relate and hallucinates the relations, not just the fields. We propose symbolic separation: a deep agent reasons freely but may act on data only through an ontology-constrained Virtual Knowledge Graph with deterministic pre-execution validation. Unlike a tool API's interface contract, this domain-semantic contract turns a complex question into one validated graph traversal instead of LLM-inferred joins. Instantiated as the Neurosymbolic Deep Analyst and evaluated on 49.9 TB of superconputer telemetry against a rigid workflow and a non-symbolic ablation, it raises end-to-end task success from 43% to 86%, prevents silent data-integrity errors that no syntactic check catches, and cuts token cost by 2.4x, letting a smaller on-premise model outperform a larger one.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决生成式AI在数据中心与工业4.0运维数据分析中不可靠的核心问题。背景上，IoT和工业4.0产生了海量异构的数值遥测数据，但用户需同时具备领域、部署和查询语言三重专业知识，LLM被视为降低门槛的自然接口。然而现有方法存在明显不足：纯概率模型会幻觉出不存在的实体和关系，无法跟踪私有schema；text-to-database仍是开放难题，GPT-4在BIRD上执行准确率仅40.08%，远低于人类专家的92.96%，且残余错误以语义错误为主；在时序运维遥测上，最先进的数据智能体对无状态查询约73%，有状态查询仅约34%，异常查询仅约10%，失败集中于schema混淆和表列选择错误。作者此前的EXASAGE虽用本体和虚拟知识图谱将自然语言转为SPARQL，达到93.6%准确率，但它是刚性单次工作流：实体抽取依赖固定类别的正则表达式，无法泛化到未字面出现的概念术语和灵活时间表述，且无恢复机制，最终验证只捕获语法错误，语义错误会静默执行返回错误数据。因此本文要解决的核心问题是：在深度智能体日益自主的背景下，如何让智能体在真实时序数据库上可信地行动。具体化为两个研究问题：将EXASAGE封装为工具是否足以吸收其刚性，还是必须重构其内部架构；以及现代LLM驱动的深度智能体能否自行导航真实时序数据库，还是根本上需要数据的符号化表示。为此作者提出“符号分离”设计，让智能体在神经层自由推理，但只能通过本体约束的虚拟知识图谱这一符号层访问数据，在查询发出前进行确定性验证，从而在结构上阻止智能体虚构数据关系，实现可信的数据分析智能体。

### Q2: 有哪些相关研究？

相关研究可按四类梳理。方法类上，KG-RAG（如KAPING）将三元组检索后交给LLM自由生成，KG只提供信息而不约束输出；Think-on-Graph、Reasoning-on-Graphs让LLM在推理中遍历KG，提升忠实度但最终答案仍由模型自由生成，关系组合仍源于LLM。语义解析类text-to-SQL要求LLM自行编写join，缺乏本体级确定性校验，GPT-4在BIRD上仅40.08%执行准确率；语法约束解码（GCD）只保证语法合法，无法阻止引用不存在表或违反约束。语义层/工具调用类通过本体映射的工具API强制接口契约，但跨调用关系逻辑仍由LLM推断，属中等符号分离。OBDA/VKG类中，SPINACH用LLM生成SPARQL，错误分析显示约70%失败源于关系获取与组合而非语法；EXASAGE及其VKG-chatbot是唯一面向数值时序遥测的VKG方案，报告93.6%图查询准确率，但仅基于1K个模板生成查询，端到端泛化受限。评测类工作显示数据代理在简单查询上约73%成功，而状态型仅34%、异常检测仅10%，失败集中于模式混淆与时间窗选择。Agentic模式方面，ReAct、Reflexion、deep agents及MCP提供实现基础。本文区别在于：首次命名“符号分离”，提出领域语义契约而非接口契约，用确定性本体一致性校验器在执行前拒绝违规，并将其嵌入深度代理，面向数值运维遥测，实现86%端到端成功率。

### Q3: 论文如何解决这个问题？

论文提出的核心方法是“符号分离”（Symbolic Separation），其关键思想是让深度智能体自由推理，但只能通过一个受本体约束的虚拟知识图谱（VKG）来访问数据，并在执行前进行确定性验证。整体架构以容器化服务形式部署，通过MCP协议通信，包含三类容器：主容器承载协调器、技能和两个子智能体；DataRetriever容器承载符号检索子智能体Querier；CodeAgent容器承载代码分析子智能体。协调器只负责规划与委派，将多步请求分解为有序任务，先派发给Querier检索，再交给CodeAgent在隔离沙箱中分析绘图，最后汇总呈现。

关键技术包括：第一，VKG按需在数据湖上物化，将作业—节点、节点—传感器—读数、节点—机架—房间等关系预先连接为RDF图，使复杂问题转化为一次经本体验证的图遍历，而非让LLM自行推断连接。第二，确定性验证器在查询执行前拒绝任何引用本体中不存在的类、属性或域/范围组合的SPARQL查询，从而拦截幻觉构造。第三，Querier通过MCP暴露exasage_query、exasage_clarify、exasage_download_csv三个工具，保证原始遥测数据永不进入推理层。第四，CodeAgent采用嵌套容器化与gVisor运行时，按用户隔离沙箱，无外网连接，并静态审计高风险导入。第五，MetricsExpert技能以markdown形式注入协调器提示，用于将自然语言指标描述解析为精确指标名。创新点在于用领域语义契约替代工具API的接口契约，将LLM推断的连接变为一次验证过的图遍历，从而把端到端任务成功率从43%提升到86%，并减少2.4倍token消耗。

### Q4: 论文做了哪些实验？

论文在49.9 TB超级计算机遥测数据上开展实验，包含两组查询：一组是复杂多轮数据分析查询（数据检索+统计后处理+可视化），另一组是仅检索查询。对比方法包括刚性单次工作流EXASAGE基线、非符号化深度分析代理（消融）以及SoA基线。主要结果：端到端分析任务上，所提系统配合Qwen3.6-35B-A3B成功率达86%，而EXASAGE基线仅7%，非符号化深度分析代理为43%；仅检索查询上达到88%准确率，优于SoA基线；所提Querier中位token消耗比最佳替代配置低2.4倍，产生零幻觉输出，并表现出快速失败重试行为，避免无效计算。这些结果验证了符号分离设计——将符号管道分解为专注的专用子代理，而非在单体提示上增加代理循环——是实现准确可信分析代理的关键。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：一是评测仅基于M100单一超算数据集与49.9 TB遥测，跨数据中心、跨工业场景的泛化性未验证；二是本体需人工构建与维护，面对schema漂移或新插件接入时成本高、易失配；三是验证器只保证本体一致性，无法捕捉语义正确但业务上无意义的查询（如错误时间窗、错误基线）。未来可探索：其一，用LLM辅助本体半自动演化与schema对齐，降低领域建模门槛；其二，将确定性验证扩展到时间语义层，引入时间窗口、采样率、单位与因果约束的校验；其三，研究验证失败时的可解释反馈与自动修复回路，让agent从拒绝中学习而非仅报错；其四，构建多站点、多模态（日志+指标+事件）的端到端基准，检验符号分离在异构与在线漂移下的鲁棒性；其五，探索VKG子图缓存与增量物化，进一步压缩延迟与token开销，使小模型在边缘侧也可可信运行。

### Q6: 总结一下论文的主要内容

本论文针对生成式AI在数据中心与工业4.0运维遥测分析中不可靠的问题，提出“符号分离”设计理念：深度智能体在神经层自由推理，但只能通过本体约束的虚拟知识图谱访问数据，并在执行前进行确定性验证。其核心贡献是将复杂问题转化为一次经过验证的图遍历，而非依赖LLM推断跨源连接关系，从而防止语义幻觉。作者实现了神经符号深度分析师系统，在49.9TB超级计算机遥测数据上评估，端到端任务成功率从43%提升至86%，检索准确率达88%，token消耗降低2.4倍，且零幻觉输出。结论表明，将符号管道分解为专注的子智能体，而非在单体提示上增加智能体循环，是构建可信运维数据分析智能体的关键。
