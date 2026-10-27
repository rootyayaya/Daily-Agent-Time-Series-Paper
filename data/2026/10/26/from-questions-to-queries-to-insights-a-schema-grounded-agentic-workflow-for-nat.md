---
title: "From Questions to Queries to Insights: A Schema-Grounded Agentic Workflow for Natural-Language Crash Data Analysis"
authors:
  - "Jingwen Zhu"
  - "Keshu Wu"
  - "Steven T. Parker"
  - "Bin Ran"
  - "David A. Noyce"
date: "2026-10-26"
arxiv_id: "2610.35054"
arxiv_url: "https://arxiv.org/abs/2610.35054"
pdf_url: "https://arxiv.org/pdf/2610.35054v1"
categories:
  - "cs.CL"
tags:
  - "Agentic Workflow"
  - "Schema-Grounded"
  - "Natural-Language Query"
  - "SQL Generation"
  - "Verification"
  - "Iterative Repair"
  - "Local LLM"
  - "Crash Data Analysis"
  - "Domain Knowledge Base"
  - "Auditable Intermediate Outputs"
relevance_score: 7.5
---

# From Questions to Queries to Insights: A Schema-Grounded Agentic Workflow for Natural-Language Crash Data Analysis

## 原始摘要

Transportation agencies maintain extensive crash databases to identify safety priorities, evaluate countermeasures, and guide resource allocation. Making these data accessible to practitioners requires flexible ways to translate analytical questions into reliable results. Existing dashboards support predefined analyses, while additional requests often depend on specialists who understand database queries, coded fields, and agency conventions. This study presents CrashDB-QA, a fully local, schema-grounded agentic workflow that enables natural-language analysis of crash databases. Specialized components interpret questions, generate and validate read-only SQL, execute queries, and explain the results. A shared knowledge base grounds query construction in the agency's data dictionary and safety-analysis conventions, while recorded intermediate outputs support inspection and auditing. An optional extension, CrashDB-QA+, checks the alignment among the question, query, and execution result and supplies evidence for iterative repair. We evaluate the workflow on a frozen snapshot of 4.4 million Wisconsin crash records using a new benchmark of 300 questions across ten analytical categories and nine local open-weight models. Domain grounding substantially improves query accuracy, and a code-specialized 7B model provides the best accuracy-latency balance among the tested models. Compositional analyses remain more difficult than routine retrieval, particularly comparisons between groups or periods. Verification improves performance when the Judge uses authoritative field definitions and the Refiner receives execution evidence, whereas additional checking alone offers no consistent benefit. These findings demonstrate the potential of locally deployed, domain-grounded workflows to broaden access to crash analysis and identify the reasoning and verification capabilities needed for reliable use.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决的核心问题是：如何让交通安全领域的从业者无需依赖技术专家，就能用自然语言可靠地查询和分析大规模事故数据库。研究背景方面，交通机构维护着数百万条事故记录，用于识别高风险地点、评估对策和分配资源，但现有仪表板和可视化平台只能支持预定义分析，超出预设范围的问题往往需要懂SQL、熟悉编码字段和机构规范的专家来编写查询，这种依赖限制了从业者探索数据和追问后续问题的能力。现有方法存在两方面不足：一是通用Text-to-SQL方法虽能将自然语言转为查询，但在事故分析中，仅把词语匹配到列名远远不够，生成的查询可能成功执行却分析上错误，例如遗漏严重度加权、错误分组或对两组误用同一条件；二是自我纠错缺乏外部反馈时不可靠，且敏感事故记录可能禁止使用外部托管的模型。因此本文要解决的核心问题是：构建一个完全本地部署、以机构数据字典和安全分析规范为 grounding 的智能体工作流，将分析意图与字段含义、编码值和度量构造规则相连接，并通过确定性只读控制与基于执行证据的验证修复机制，确保生成的查询及其结果在分析上正确、可审计且可追溯。

### Q2: 有哪些相关研究？

本文的相关研究可归纳为三类。方法类方面，Text-to-SQL 研究是核心基础，包括模式感知的神经模型与基于 LLM 的方法，以及 Spider、BIRD 等基准，并涵盖查询分解、模式链接、多模型协作与纠错等策略；此外，推理与工具使用、候选一致性、迭代精化及模型自评等机制也被广泛探讨，但已有工作指出无外部反馈的自我纠错并不可靠。应用类方面，LLM 在交通领域已用于信号控制、时空预测、工具增强的交通分析及车联网数据解读；在交通安全中则涉及研究辅助、事故叙述分析、致因识别、严重度推断、事故记录建模、风险评估与隐私筛查，并有研究用 LLM 修正二次事故编码、关联叙述与路面状况记录。评测类方面，某大学交通中心原型实现了对全州事故库的自然语言查询与图表生成，但仅作演示、缺乏系统性准确率评估；交通领域评测还揭示了预测准确率与专家一致性之间的差异。本文与上述工作的区别在于：现有 Text-to-SQL 方法难以处理事故分析中“可执行但错误”的查询，而交通领域应用多停留在演示或单一任务；本文提出完全本地、模式接地的智能体工作流，结合权威数据字典与安全分析惯例，配合只读约束、可审计中间输出及执行证据驱动的校验修复，并构建 300 题、十类分析任务的执行级基准进行系统评测。

### Q3: 论文如何解决这个问题？

论文提出 CrashDB-QA，一个完全本地部署、以数据库模式（schema）为锚定的智能体工作流，把自然语言问题转化为可靠的碰撞数据分析结果。整体框架以“数据库执行边界”为组织核心，采用预定义编排的 agentic 工作流：语言模型只负责需要语言理解的任务（意图抽取、SQL 生成、结果评估、解释），而模式检索、查询校验、数据库执行和反馈组装由确定性组件完成，执行顺序与重试次数由代码控制，从而保证可预测的数据库访问并留下可审计的中间输出轨迹。

核心由六个组件构成：Interpreter 将问题解析为结构化意图（度量、过滤、分组、时间、排序）；Schema Linker 基于知识库中的字段描述、关联词和列名做词法打分检索相关列，并对严重度等语言加规则补充；Generator 在问题、意图、链接列知识、分析约定和重试反馈的约束下生成只读 SQL；Validator 与 Executor 以确定性方式校验并执行查询；Explainer 用通俗语言解释结果。关键支撑是共享知识库 K，包含列级知识（描述、存储取值/格式、关联词）与分析约定（如“无某因素”“致命事故”“事故占比”“最严重”对应的 SQL 模式），通过面向模式的 RAG 在需要处注入，解决 INJSVR 等缩写字段含义不明、易产生“可执行但错误”查询的问题。

创新点是可选的 CrashDB-QA+ 扩展：在生成与解释之间插入 Judge 和 Refiner，联合检查问题—查询—结果三者对齐，Judge 依据权威字段定义与相关备选列给出通过/失败判定及评分，Refiner 携带执行证据进行迭代修复；实验表明这种带领域依据的验证才有效，单纯增加检查并无稳定收益。

### Q4: 论文做了哪些实验？

论文在威斯康星州440万条事故记录的冻结快照上评估CrashDB-QA工作流，构建了包含300个问题的新基准CrashDB-QA Benchmark，覆盖十个分析类别（C1–C5检索层：计数、分组汇总、排名、时间趋势、空间汇总；C6–C10推理层：季节性、多条件过滤、严重度加权、对比、归一化比率），每类30题，参考答案经起草—双人审核—仲裁流程构建并以执行匹配评分。实验对比了九个本地开源权重模型，包括代码专用7B模型等。主要结果：领域知识库接地显著提升查询准确率；代码专用7B模型在准确率与延迟之间取得最佳平衡；组合式分析（尤其组间或时段对比）比常规检索更难；验证环节仅在Judge使用权威字段定义、Refiner获得执行证据时带来提升，单纯增加检查无一致收益。基准还关注“可执行但错误”的查询，按类别诊断失败模式。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三：其一，评测仅基于威斯康星州4.4百万条事故快照与300题基准，跨州、跨机构数据字典与安全分析惯例的迁移性尚未验证，未来可构建多机构联合基准检验模式接地（schema grounding）的泛化能力。其二，组合式分析（组间/时段比较）仍显著难于常规检索，说明多步推理与查询分解是瓶颈，可引入查询分解规划、子查询复用与中间结果自校验机制。其三，验证环节的效果高度依赖Judge是否掌握权威字段定义、Refiner是否获得执行证据，单纯增加检查无益，未来可研究证据驱动的选择性验证策略，按问题复杂度动态分配验证预算以平衡准确率与延迟。此外，当前仅支持只读SQL与结果解释，可扩展至因果推断、趋势预警与可视化生成，并引入人机协同的审计反馈闭环，让领域专家修正沉淀回知识库，持续提升本地小模型的可靠性。

### Q6: 总结一下论文的主要内容

论文针对交通机构维护的大规模事故数据库难以被非技术从业者直接查询的问题，提出CrashDB-QA——一个完全本地部署、以数据库模式为知识基础的智能体工作流。系统由解释器、模式链接器、SQL生成器、验证器、执行器和解释器六个组件构成，并共享一个融合数据字典、字段编码与分析惯例的知识库，将自然语言问题转化为只读SQL并给出结果解释；可选扩展CrashDB-QA+增加Judge与Refiner，检查问题、查询与执行结果的一致性并迭代修复。作者在440万条威斯康星州事故记录的冻结快照上，用覆盖十类分析任务的300题基准和九个本地开源模型进行评估。结果表明：领域知识 grounding 显著提升查询准确率，代码专用7B模型在准确率与延迟间取得最佳平衡；涉及分组或时段比较的组合分析仍明显难于常规检索；只有当Judge依据权威字段定义、Refiner获得执行证据时，验证才带来稳定收益。该工作展示了本地化、领域 grounded 工作流在扩大事故分析可及性方面的潜力，并揭示了可靠使用所需的推理与验证能力。
