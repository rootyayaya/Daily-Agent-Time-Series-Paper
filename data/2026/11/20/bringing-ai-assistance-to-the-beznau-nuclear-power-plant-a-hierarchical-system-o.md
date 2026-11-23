---
title: "Bringing AI Assistance to the Beznau Nuclear Power Plant: A Hierarchical System of LLM Agents for Reactor Monitoring"
authors:
  - "Wenqi Zhou"
  - "Leonardo Baldo"
  - "Edwin Kolbe"
  - "Manuel Arias Chao"
date: "2026-11-20"
arxiv_id: "2611.27556"
arxiv_url: "https://arxiv.org/abs/2611.27556"
pdf_url: "https://arxiv.org/pdf/2611.27556v1"
categories:
  - "cs.MA"
  - "cs.AI"
tags:
  - "LLM Agents"
  - "Hierarchical Multi-Agent"
  - "Industrial Monitoring"
  - "Nuclear Power Plant"
  - "Reactor Monitoring"
  - "Anomaly Investigation"
  - "Traceability"
  - "Evidence Routing"
  - "Domain Expertise as Procedures"
  - "Advisory System"
  - "Tool Use"
  - "Read-only Access"
  - "SAP Systems"
  - "Safety-critical AI"
  - "Organizational Lessons"
relevance_score: 8.5
---

# Bringing AI Assistance to the Beznau Nuclear Power Plant: A Hierarchical System of LLM Agents for Reactor Monitoring

## 原始摘要

Beznau Unit 1 in Switzerland, in operation since 1969, is the most experienced nuclear reactor still running worldwide. Five decades of incremental modernization have left its monitoring systems, alarm logs, variable catalogs, technical specifications and investigation reports in separate silos that were never designed to be queried together. As a result, investigating a core instrumentation anomaly means slow, manual gathering of knowledge scattered across databases, documents, and experienced colleagues. We present a hierarchical multi-agent assistant built on large language models (LLMs) to support these investigations and reduce the need for tedious manual searches in SAP systems. An orchestrating agent breaks down an engineer's question and hands the parts to specialized sub-agents, each with read-only access to one source. Domain expertise is written as natural-language procedures that plant engineers can read, review and revise. The system is strictly advisory, with every answer traced back to its sources. We also report organizational lessons from introducing agentic AI into a culture built on safety, traceability and conservative change. Beyond the technical architecture, the Beznau case study examines how an assistant can be introduced into a setting where evidence must be traceable, changes carefully reviewed, and operational decisions retained by plant personnel, paving the way for the responsible use of agentic AI in industrial plant monitoring.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决核电厂（尤其是运行超过半个世纪的老旧机组）在反应堆监测与仪表异常调查中，知识高度分散、人工检索效率低下的问题。以瑞士Beznau 1号机组为例，其监测系统、报警日志、变量目录、技术规格书和调查报告分属不同“信息孤岛”，从未被设计为可联合查询；工程师调查一次堆芯仪表异常，往往需要跨多个数据库、文档和资深同事经验进行缓慢的手工取证，SAP系统中的繁琐搜索尤其耗时。现有LLM/RAG及多智能体方法虽已用于工业维护和核工程文档检索，但多停留在文档、仿真或实验环境，尚未在真实商业核电厂运行场景中部署，且难以满足安全关键、强监管环境对来源可追溯、访问受控、推理可复现和人工保留最终判断权的严格要求。因此，本文的核心问题是：如何构建一个分层多智能体助手，由编排智能体分解工程师问题并调度只读访问各类厂内数据源的专用子智能体，将分散的运行数据与工程记录纳入统一调查流程，同时以自然语言程序表达领域知识供工程师审阅修订，确保每个回答可回溯来源、系统仅作建议性辅助，并总结在安全优先文化中引入智能体AI的组织经验。

### Q2: 有哪些相关研究？

相关研究可分为三类。方法类方面，检索增强生成（RAG）为LLM提供外部检索材料，智能体工具调用则让模型选择操作并依据返回结果推进后续步骤；编排式多智能体架构以协调者分解任务、分派给专家智能体，Magentic-One给出通用实现。工业维护应用类方面，MindRAG结合多模态检索与LLM智能体支持状态监测工作流，MAKG引入协作智能体与知识图谱检索回答设备维护问题，Farahani等用LLM规划器协调数据准备、分析与维护建议等专家智能体，Gong等按问题复杂度路由诊断问题，Schall通过编排器与基于工厂文档的验证层将监测智能体接入过程自动化。核工程应用类方面，RADIANT-LLM以多模态架构从技术文档中保留页面与图源检索，Lee等在反应堆模拟器中考察LLM智能体执行任务，AROMA-GPT通过专用分析工具连接物理数字孪生，Lim等将类似方案扩展到带数字孪生的热工流体实验设施。本文与上述工作的区别在于：将分层多智能体助手部署到真实商业核电厂（Beznau 1号机组）的在役调查流程中，跨运行数据、报警日志、变量定义、技术规格与历史报告等多源异构记录进行只读检索与协同分析，并以工程师可读可改的自然语言规程约束智能体行为，强调来源可追溯与人员保留最终判断，从而把此前限于文档、仿真或实验环境的验证推进到运行电厂场景。

### Q3: 论文如何解决这个问题？

论文提出了一套分层多智能体架构来解决核电厂监测知识分散、人工检索效率低的问题。整体框架由一个编排智能体（Orchestrator）和六个专业子智能体组成：核专家智能体（NEA）查阅反应堆监测知识、技术规格与调查报告；报警日志智能体（ALA）检索ANIS报警记录；组织智能体（OA）查询组织架构数据库以定位责任人；系统同步智能体（SSA）检查ANIS与GARDEL数据的一致性；ANIS/GARDEL专家智能体（AEA/GEA）通过语义搜索识别测点名称与变量定义；ANIS/GARDEL监测智能体（AMA/GMA）应用监测程序与分析工具检测异常。

关键技术包括：一是任务分解与协调机制，编排智能体解析工程师的自然语言问题，生成任务清单，按调查依赖关系将子任务分派给相关子智能体，并利用前序智能体返回的信息为后续请求建立上下文；二是自然语言领域程序，将领域知识写成电厂工程师可读、可审、可修订的自然语言流程，指导变量选择、记录查阅与结果解释；三是证据溯源与只读访问，各子智能体仅对单一数据源有只读权限，返回结论时附带来源引用，编排智能体汇总为可追溯的建议性回答。

软件层面，浏览器界面经REST API与后端交互，智能体运行时管理编排与子智能体工作流，后端通过数据库查询访问结构化数据、从向量库检索文档，语言模型经Azure OpenAI服务调用GPT-4o并部署于瑞士境内以保障数据保密，本地追踪平台记录执行轨迹。创新点在于严格建议性定位、证据可追溯、领域程序可人工维护，以及将智能体AI引入以安全与保守变更为核心的组织文化的实践路径。

### Q4: 论文做了哪些实验？

论文的实验以贝兹瑙1号核电站为案例，采用定性演示方式评估“反应堆监测助手”的多智能体工作流。实验设置包括：主协调智能体将工程师问题分解并分派给专用子智能体，各子智能体只读访问单一数据源（GARDEL监测数据、ANIS数据、领域程序文档、历史调查报告等），所有回答均附带可追溯的引用来源。测试场景有三类：一是“你是谁”的能力介绍查询，由主助手直接回答；二是GARDEL异常检测查询，需检索指定时段监测数据，报告数据连续性、检测到的异常数量与时间区间，以及检测器输出与注入的合成故障真值标签的一致性，并附异常分数与真值对比图；三是ANIS数据波动调查，问题故意模糊，需跨异构源检索、分析波动发生、持续时间和时间分布，并结合历史报告解释，核专家智能体参与解读。主要结果显示系统能完成欠定请求的解读、跨源检索、数据分析、可视化与综合，并将观测与历史案例关联；但论文指出这仅为定性演示，检索准确性、分析正确性和对电厂工程师的实用性仍需在更广泛调查集上系统评估，未给出定量指标。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索空间主要体现在三方面。其一，评估范围有限：系统目前仅在试点环境运行，未来需扩展到更广泛的监测场景，系统评估其在真实工程任务中的效用与误报率。其二，智能体协调可靠性尚未充分验证：编排代理与子代理之间的任务分解、证据聚合在复杂查询下可能失效，可探索引入置信度估计、冲突证据仲裁与失败回退机制。其三，领域程序维护成本高：自然语言程序随电厂系统演进需持续更新，可研究程序版本管理、自动一致性检查，甚至由LLM辅助生成候选程序供工程师审阅。此外，当前系统严格只读且仅作建议，未来可在保持人类决策权的前提下探索主动追问、多轮澄清与跨源因果推理；同时可结合可解释性方法，对生成解释进行溯源粒度与不确定性标注，并开展长期人机协作研究，量化其对工程师认知负荷与调查效率的影响。

### Q6: 总结一下论文的主要内容

论文针对瑞士贝兹瑙核电站1号机组（1969年投运、全球最老在运反应堆）的监测困境：五十年渐进式改造使监测系统、报警日志、变量目录、技术规格与调查报告分散于互不联通的孤岛，调查堆芯仪表异常需人工跨库检索。作者提出基于大语言模型的分层多智能体助手：编排智能体将工程师问题拆解并分派给各具只读数据源访问权限的专用子智能体，领域知识以电厂工程师可阅读、审查和修订的自然语言流程书写；系统严格限于咨询性质，每个答案均可溯源至原始出处。主要贡献包括：将多源运行数据与工程记录纳入统一调查流程的编排架构（已在试点环境部署）、可审查的自然语言领域流程、展示智能体任务协调与证据呈现的监测案例，以及将智能体AI引入以安全、可追溯和审慎变革为核心文化的核工程实践的组织经验。结论表明，协调智能体能在保留证据供工程复核的前提下支持异常调查，为智能体AI在工业电厂监测中的负责任应用铺路。
