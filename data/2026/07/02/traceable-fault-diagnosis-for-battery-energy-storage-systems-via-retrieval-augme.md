---
title: "Traceable Fault Diagnosis for Battery Energy Storage Systems via Retrieval-Augmented Multi-Agent O&M Assistant"
authors:
  - "Jiangdi Ru"
  - "Bing Li"
  - "Yage Huang"
  - "Ding Wang"
  - "Keru Hua"
date: "2026-07-02"
arxiv_id: "2607.01992"
arxiv_url: "https://arxiv.org/abs/2607.01992"
pdf_url: "https://arxiv.org/pdf/2607.01992v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "可解释时间序列分析"
  - "工业故障诊断"
  - "时序报告生成"
  - "LLM/Agent工作流"
  - "RAG"
  - "多智能体系统"
  - "电池储能系统"
relevance_score: 8.5
---

# Traceable Fault Diagnosis for Battery Energy Storage Systems via Retrieval-Augmented Multi-Agent O&M Assistant

## 原始摘要

Large-scale battery energy storage systems (BESSs) require O&M decisions that combine alarms, cell-level measurements, device topology, diagnostic tables, historical cases, and maintenance documents. Monitoring platforms can flag threshold violations, but they often cannot explain whether voltage inconsistency, resistance drift, short-circuit risk, capacity divergence, or thermal abnormality needs intervention. This digest presents a traceable BESS fault-diagnosis assistant that uses retrieval-augmented multi-agent reasoning to connect operational data, domain knowledge, visual evidence, and report generation. Reliability is improved through BESS-specific task routing, schema-constrained natural-language database access, hybrid text-image retrieval, and evidence-based answer synthesis. Preliminary internal evaluation is reported for routing, database access, and diagnostic reasoning.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文旨在解决大规模电池储能系统（BESS）运维（O&M）中故障诊断的碎片化和不可追溯性问题。当前运维工作流分散：运维人员需要在不同平台查看告警、从时序数据库检索曲线、搜索手册或标准，并咨询专家进行最终判断。数据驱动的电池模型虽能检测异常或估计健康状态（SOH），但通常只输出分数或标签，缺乏可追溯的维护决策。通用大语言模型（LLM）在没有私有知识约束、受控数据库访问、保守风险推理和可审计证据的情况下也不安全。因此，论文提出一个可追溯的BESS故障诊断助手，通过检索增强的多智能体推理，将运行数据、领域知识、视觉证据和报告生成连接起来，形成端到端、可解释的运维决策支持系统。

### Q2: 有哪些相关研究？

相关工作分为两类：电池故障诊断方法和LLM/Agent技术。电池故障诊断方面，模型基础方法（如电化学模型和残差检验）用于小故障检测；统计和数据驱动方法（如高斯过程在线健康监测）用于现场数据分析；不一致性驱动方法强调将电气、热和老化指标转化为可解释的维护动作。LLM/Agent技术方面，RAG（检索增强生成）通过文档检索增强生成，Dense Retrieval和BM25用于语义和精确匹配，多模态RAG支持图像检索。ReAct、Toolformer、Tree-of-Thoughts等连接推理与外部动作，Text-to-SQL研究关注模式链接和约束生成。BatteryAgent结合物理特征、可解释ML和LLM推理进行电池诊断。本文与这些工作的区别在于，它整合了数据库查询、知识检索、可视化和多智能体证据合成，专门针对BESS运维场景，强调可追溯性和证据链。

### Q3: 论文如何解决这个问题？

论文设计了一个多智能体系统架构，核心包括四个部分：1）BESS运维任务模型与复杂度感知路由：将用户请求分为告警分析、时序趋势分析和故障排查三类业务路由，简单任务由单智能体监督器处理（执行数据库查询、检索、图表生成或直接回答），复杂诊断问题进入深度研究路径。2）模式约束的数据库访问：采用“规划-执行”设计，LLM预测业务路由和结构化查询计划（包含表、字段、过滤条件、时间范围等），确定性清理器检查模式白名单和路由-表映射，移除非法字段、标准化别名、限制不安全限制，生成可执行SQL，返回的行转换为证据包。3）混合文本-图像检索：离线将手册、标准、规程和案例解析为文本块并链接图像元数据；在线融合稠密检索和BM25检索，文本提供答案基础，图像提供视觉证据（如规程、形态分析、波形解释）。4）多智能体证据合成：对于高复杂度问题（如跨文档根因分析），监督器分解请求，分派研究者智能体，压缩发现，生成包含结论、证据、风险判断和推荐操作的诊断报告。中间状态被记录用于审计和专家审查。

### Q4: 论文做了哪些实验？

论文进行了初步内部评估，使用匿名化运行数据和私有BESS维护知识库。资源池包含3条业务路由、7个可查询表、99个文档、6741个文本块、717张图像和486个图像链接块。任务集覆盖路由、数据库查询和诊断推理问题。主要实验结果：1）数据库访问方面，模式约束模块实现了100%的SQL就绪计划成功率（即查询计划通过路由/模式检查并可直接转换为可执行SQL），而移除模式验证后成功率为0%，因为原始LLM计划常包含无效字段、路由-表不匹配或不受支持的查询范围。2）路由模块动作准确率70%，质量评分4.44，延迟40.01秒；无路由变体准确率仅20%，质量3.20，延迟87.45秒。3）诊断推理质量评分4.80，延迟95.33秒；无多智能体变体质量3.60，延迟60.99秒。此外，展示了四个代表性案例：微短路风险证据检索、集群级遥测查询与趋势可视化、知识库检索（含文档和图像证据）、以及重复告警和异常分析。

### Q5: 有什么可以进一步探索的点？

论文指出未来方向包括：1）添加详细的现场统计数据和更多专家标注的案例研究，以增强评估的全面性和可信度。2）当前系统在路由、数据库查询和诊断推理上表现良好，但可进一步优化多智能体协作的效率，例如通过自适应任务分解或智能体间通信协议。3）探索自进化技能（self-evolving skill）机制，使系统能从历史诊断案例中学习并改进路由和推理策略。4）引入反馈优化循环，利用运维人员的纠正反馈来微调检索和生成模块。5）扩展到其他工业领域（如风电、光伏）的故障诊断，验证方法的通用性。6）增强可解释性，例如通过可视化证据链和决策路径，帮助运维人员理解诊断结论。

### Q6: 总结一下论文的主要内容

本文提出一个面向电池储能系统（BESS）的可追溯故障诊断运维助手，通过检索增强的多智能体推理将运行数据、领域知识、视觉证据和报告生成整合为端到端系统。核心创新包括：复杂度感知的任务路由、模式约束的自然语言数据库访问、混合文本-图像检索，以及多智能体证据合成。初步内部评估显示，路由模块准确率70%，数据库访问SQL就绪成功率100%，诊断推理质量评分4.80，均优于无路由、无模式验证和无多智能体的消融变体。该系统将LLM、RAG和工具作为支撑机制，以储能安全、运行数据、故障类别和维护动作为中心，为工业运维提供了可解释、可追溯的决策支持，有望提升大规模电池储能系统的运维效率和安全性。
