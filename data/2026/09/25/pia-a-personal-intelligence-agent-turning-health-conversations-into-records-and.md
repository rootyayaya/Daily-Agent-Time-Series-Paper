---
title: "PIA: A Personal Intelligence Agent Turning Health Conversations into Records and Records into Understanding"
authors:
  - "Jeonghun Yoon"
  - "Dongchan Kim"
  - "Hongyeon Yu"
  - "Young-Bum Kim"
  - "Jaegul Choo"
date: "2026-09-25"
arxiv_id: "2609.31255"
arxiv_url: "https://arxiv.org/abs/2609.31255"
pdf_url: "https://arxiv.org/pdf/2609.31255v1"
categories:
  - "cs.CL"
tags:
  - "Agentic Time Series"
  - "Personal Health Agent"
  - "Memory Harness"
  - "Temporal Reasoning"
  - "Knowledge Graph"
  - "Clinical Records"
  - "Natural Language Understanding"
  - "Causal Trajectory"
  - "LLM Agent"
  - "Health Monitoring"
relevance_score: 7.5
---

# PIA: A Personal Intelligence Agent Turning Health Conversations into Records and Records into Understanding

## 原始摘要

General-purpose agent memory summarizes conversations: it extracts salient snippets, embeds them, and retrieves the top-k into the prompt. A health agent cannot run on summaries: a dose becomes a sentence, "since last week" is resolved at the model's discretion, and a three-month glucose trend cannot be answered by text similarity. We present PIA, a personal intelligence agent deployed alongside a consumer health agent. PIA receives the agent's natural-language requests, decides for itself whether and how to write or read, and turns conversations into typed clinical records and records into a synthesized understanding of the user. Its memory harness consists of four controls -- extraction, memory, retrieval, and understanding -- each a domain-agnostic mechanism with a pluggable health module: schema, medical alias dictionary, knowledge graph, and temporal rules. We show how the same query receives a different answer as the memory injected into the response context deepens from one-dimensional recall, to a two-dimensional health snapshot, to a three-dimensional trajectory with causality, and report lessons from operation: self-reported health data are missing not at random, question phrasing governs the quality of synthesized understanding, and nearly a third of candidate causal links are structural noise that rules alone remove.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

通用智能体的记忆机制通常依赖对话摘要：抽取显著片段、向量化存储、检索 top-k 注入提示词。然而，这种范式无法支撑健康智能体的需求。首先，健康记录被扁平化——"每天晚饭后服用一剂 Amosartan"必须保留为药物、频率、时间等结构化字段，因为它需要被查询和聚合，而非被回忆。其次，时间被模型随意推断——"三天前我体重 80 公斤"需要区分事件日期与提及日期，若由模型自行计算，"过去三个月体重如何变化"便没有可靠答案。第三，用户被记录却未被理解——"我的糖尿病指标正常吗"需要系统知道空腹血糖和 HbA1c 属于糖尿病范畴，即便用户从未提及该词，而数千行数据也无法靠检索几条记录来理解。

因此，本文提出 PIA（Personal Intelligence Agent），一个部署于消费级健康智能体旁的个人智能体，旨在弥补上述三个缺口。PIA 接收健康智能体的自然语言请求，自主决定是否以及如何读写，将对话转化为带类型的临床记录，并将记录综合为对用户的整体理解。其核心问题是：如何构建一套记忆框架，使点状观察转化为纵向病史，并让智能体真正"理解"用户而非仅仅"记住"用户。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，Mem0、Zep、LangMem和MemGPT是代表性通用智能体记忆系统，它们将显著记忆存入向量、图或分层存储，并在长时程基准上评测。这些系统允许开发者声明实体类型（如药物类型），但不提供背后的处理管线，例如摄入与用药方案规则的区分、基于医学词典的失败关闭式校验以及确定性时间运算。应用类方面，FHIR和OMOP面向机构级数据交换与队列分析，而非处理“睡前吃了拉面”这类个人日常健康对话。PIA与上述工作的关系是：其联想记忆直接采用开源Hindsight引擎，包括事实抽取到世界与经验网络、因果链接、整合为观察以及基于语义、关键词和图索引的召回。本文的贡献位于Hindsight两侧：类型化记录系统与规范化器、时间解析器、记忆门控与知识图谱接地、带重水合和硬边界的结构化检索、读取门控/路由器、问题契约以及上下文包。区别在于，PIA面向消费级健康智能体，强调将对话转为类型化临床记录并合成用户理解，而非通用摘要或机构数据交换。

### Q3: 论文如何解决这个问题？

PIA将通用智能体记忆的“摘要式”范式替换为“临床记录式”范式，其核心是四控制记忆框架（memory harness），每个控制均为领域无关机制，但可插入健康专用模块。

整体架构采用“双副本、单智能体”结构：一个规范化器将对话轮次写入类型化记录系统（HUP），同时同一轮次保留在联想记忆中。每轮通过invoke步骤选择写分支、读分支或两者。读分支上，读门控决定是否需要记忆，读路由器选择结构化检索、联想回忆或二者组合的计划，并先解析请求中的时间表达。HUP在记录变化时离线运行，其输出、静态画像和近期记录构成每轮上下文包。

四个控制分别为：提取控制通过模式约束抽取，将话语强制映射为23种HUP类型，并由确定性非LLM时间解析器将“昨天”等表达转为绝对时间；记忆控制设置临床记忆门，测试结果须与医学别名字典精确匹配才存储，否则排队离线扩展，每条记录携带出处；检索控制实现决策条件化回忆，枚举/值/趋势请求走结构化检索，其余走联想回忆并重水化，且设硬边界——请求特定药物或测试而无匹配时返回空而非相似回退；理解控制由HU引擎实现，通过七个问题对整合记忆进行推理，生成六面动态状态（状态、趋势、风险、目标、约束、偏好），在后台重建，请求时通过上下文包挂载。

创新点在于：将记忆从“日记”提升为“病历”，用模式匹配替代模型裁量，用确定性时间算术替代LLM推断，用问题契约替代模式校验来约束推理边界，并区分事实、注释与合成文本。

### Q4: 论文做了哪些实验？

论文在20个合成用户（741条话语、976条记录）上构建了271个场景的评测套件，包括54个存储、192个路由、24个检索和1个理解场景，真值由三位健康领域专家逐项审核并冻结（414行中381行保留）。评测分两层：确定性探针和四轴（存储、检索、回答、能力）通过/失败判断器，每项测量重复多次独立运行。主要结果：RETAIN门控精度100%、召回89.1%、准确率94.9%；READ路由召回91.0%；读取路由器工具选择准确率91.0%，MRR 0.785，Recall@k 0.763，Precision@k 0.758；存储判断通过率88.3%。在部署记录库的16,122条富化检验结果中，99.7%带标准键、99.2%带概念标签，但仅66.6%有参考范围、64.4%有异常标志。经验教训包括：自报健康数据非随机缺失（9个睡眠夜中8个为“差”）；问题措辞比模式更影响答案质量；近三分之一候选因果链接为结构性噪声，23对中有7对可在统计检验前通过规则剔除。

### Q5: 有什么可以进一步探索的点？

PIA 的局限为后续研究划出了清晰边界。首先，理解阶梯仅第一级“状态摘要”落地，生活状态序列、共识分层关联、基于随访的修正与反事实模拟仍停留在设计阶段，未来需验证这些高层能力在真实数据上的增益与风险。其次，别名精确匹配使记录召回受限于词典覆盖，可探索模糊匹配、嵌入检索与主动澄清相结合，并自动补全参考范围。第三，评估依赖合成用户与 LLM 裁判，真实纵向数据因隐私无法公开，未来可构建隐私保护的联邦评测或脱敏基准。第四，自报数据非随机缺失，均值会偏向“坏日子”，可引入缺失机制建模、逆概率加权或主动询问来纠偏。此外，因果链中近三分之一为结构噪声，说明规则过滤后仍需统计检验与用户确认，避免过度归因。

### Q6: 总结一下论文的主要内容

论文针对通用智能体记忆机制在健康场景中的不足展开研究：通用记忆仅提取对话摘要并依赖文本相似度检索，无法处理剂量、时间指代和长期趋势等临床需求。为此，作者提出PIA——一个与消费级健康智能体协同部署的个人智能体，能够自主决定读写时机，将自然语言对话转化为结构化临床记录，并进一步合成对用户的理解。其记忆框架包含提取、记忆、检索、理解四个控制环节，每环节均为领域无关机制，并配有可插拔健康模块：模式、医学别名词典、知识图谱和时间规则。论文展示了同一查询随记忆深度从一维召回、二维健康快照到三维因果轨迹而得到不同答案，并总结运营经验：自报健康数据非随机缺失、提问措辞影响理解质量、近三分之一候选因果链为结构噪声。结论强调健康智能体需要记录而非摘要，未来工作在于向更高层级攀升。
