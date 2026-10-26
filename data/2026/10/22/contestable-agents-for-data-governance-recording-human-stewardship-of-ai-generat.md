---
title: "Contestable Agents for Data Governance: Recording Human Stewardship of AI-Generated Metadata Across Structured and Unstructured Systems"
authors:
  - "Humza Akhtar"
  - "Brian Freeman"
date: "2026-10-22"
arxiv_id: "2610.31553"
arxiv_url: "https://arxiv.org/abs/2610.31553"
pdf_url: "https://arxiv.org/pdf/2610.31553v1"
categories:
  - "cs.AI"
  - "cs.DB"
  - "cs.HC"
  - "cs.MA"
tags:
  - "LLM Agent"
  - "数据治理"
  - "元数据管理"
  - "可争议决策"
  - "人类监督"
  - "工业物联网"
  - "HVAC"
  - "证据引用"
  - "知识图谱"
  - "Brick Schema"
relevance_score: 6.5
---

# Contestable Agents for Data Governance: Recording Human Stewardship of AI-Generated Metadata Across Structured and Unstructured Systems

## 原始摘要

Industrial organizations hold operational knowledge in structured records, such as telemetry, point lists, and transactions, and in unstructured sources, such as manuals, service notes, communications, and inspection reports. Governance programs often manage these sources separately. Classifying, linking, and documenting them depends on a small group of employees with deep domain knowledge. Agents built on large language models can propose metadata, cite documents, and flag quality issues, but unreviewed proposals can spread errors into downstream systems. A perfunctory approval leaves no record of what a reviewer checked. We present contestable governance: specialist agents produce scored, cited arguments for disputed metadata decisions; a steward can accept, reject, modify, or add arguments before commit; and a governance record retains the evidence, interventions, and outcome. A versioned domain glossary supplies model-specific terms and acronym definitions to the agents. We describe the workflow, a triage path that reserves full argumentation for uncertain proposals while preserving review before commit, the scoring and record models, and a gate that controls which verified decisions become precedent. Two HVAC use cases illustrate the pattern: point classification using Brick Schema class labels, supported by an open reference implementation, and an illustrative warranty failure-mode decision linking claim fields and telemetry to service notes and revisioned bulletins.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决AI代理辅助工业数据治理中“人类监督流于形式、错误难以追溯”的问题。研究背景是：工业组织同时持有结构化数据（遥测、点表、交易记录）和非结构化文档（手册、服务记录、检验报告），但治理程序通常将二者分开管理，分类、关联和文档化高度依赖少数资深员工。随着设备规模扩大，新产线、固件更新和联网站点不断产生需要分类和关联的数据，人工能力难以跟上。现有基于大语言模型的代理虽能提出元数据、引用文档并标记质量问题，但存在明显不足：未经审查的提案会把错误传播到下游系统；一键式审批导致“橡皮图章”现象，审批记录无法说明审查者究竟核查了什么；审查者的纠正往往留在邮件或工单中，代理无法学习，错误反复出现；事后也难以判断某条元数据来自模型、审查者还是批量导入。因此，本文的核心问题是：如何设计一种“可争辩的治理”机制，让代理在提交前提供带评分和引用的论证，让人类管理员能够接受、拒绝、修改或补充论证，并将证据、干预和结果完整记录为可查询、仅追加的治理记录，从而在结构化与非结构化系统之间实现可追溯、可问责的人类监督。

### Q2: 有哪些相关研究？

本文的相关研究可分为四类。治理类：数据治理文献将决策权分配给数据原则、质量、元数据等域，DAMA 知识体系给出 steward 的操作实践，但既有工作将批准结果与推理过程分离存储；Google Goods 系统表明事后推断元数据可扩展，却未保留人工审查痕迹。溯源与元数据标准类：PROV 区分“为何产生”与“数据来源”，FAIR 原则与 datasheets 规定元数据应支持可发现、可复用与文档化，数据质量研究提供适用性维度，本文据此将证据与责任记录在决策近旁。建筑自动化点表映射类：Brick 本体定义设备与点关系，已有方法从名称学习解析规则或跨建筑迁移映射，但名称本身可能误导，需结合手册等非结构化证据，基础模型可读取手册，本文关注如何同时利用两类证据并保持审查者控制。可争议性与论证类：可争议 AI 研究用户如何质疑算法输出，抽象论辩框架及 QBAF（如 DF-QuAD）为论证与支持/攻击关系提供计算表示，近期工作用语言模型生成论证图；本文将其应用于数据治理，并新增保留审查者编辑的存储模型。此外，多智能体 ERP 事件对比研究启发了角色分离与术语注入，但未证明其提升元数据决策的事实正确性。

### Q3: 论文如何解决这个问题？

论文提出“可争议治理”（contestable governance）框架，将LLM智能体生成元数据的过程改造为可审计的人机协作流程。整体分为四个阶段：数据分析阶段，分析器读取点表、模式等结构化输入，收集相关文档与术语表条目，并从先例库中检索相似的历史已核实决策；多智能体论证阶段，多个具有不同证据角色的专家智能体（如分别检查点名、设备手册、文档修订适用性）仅在有证据支撑时提交支持或反对候选的论证，每条论证带有基础分与来源引用，缺失证据不构成对其它候选的支持；人类争议阶段，管理员可接受、拒绝、修改或新增论证，系统每次变更后重新打分，且评审结束前不得提交决策；选择与存储阶段，打分引擎选出最高分候选，终结器解释结果与传播步骤但不选择类别，系统将证据、论证、干预与决策存入治理记录。关键技术包括：采用定量双极论证框架（QBAF），以带符号求和的logistic更新规则迭代计算论证强度，候选的原始边际为支持强度之和减去反对强度之和；引入版本化领域术语表，为智能体提供受控的缩写与设备术语定义并记录版本；设计分诊路径，先用类型化决策模型对高置信度提案快速分类，仅将低置信度提案送入完整论证，同时保留提交前的人工评审；设置先例晋升门控，仅允许已核实记录进入向量索引作为先例，并支持降级。创新点在于将人类评审干预作为一等数据记录，审计者可仅凭存储的论证独立重算类别而无需重跑模型，并通过共享会话标识实现跨结构化与非结构化系统的血缘追溯。

### Q4: 论文做了哪些实验？

论文围绕“可争议治理”工作流开展了两个暖通空调（HVAC）用例实验。第一个是点位分类实验，基于Brick Schema类标签，使用CrewAI智能体、GPT-4o、Voyage AI嵌入和MongoDB构建开源参考实现，数据为含247个点位的合成站点，其中18个被标记为歧义点；按提出的分诊路径，229个点走简短证据审查，18个歧义点走完整论证与审查，且提交前均需人工复核。参考实现对点位AHU-1-DISCH-T运行完整流程：String Matcher仅凭名称倾向discharge air，Documentation Reader引用手册4.2节和附录A支持mixed air，两者初始边际分接近（0.045与0.044）；审查者驳回仅基于缩写的质疑后mixed-air边际升至0.821，再补充4.2节论据后升至1.758，系统最终提交mixed air。第二个是保修故障模式判定示例，使用虚构机组DEMO-AHU（序列号DEMO-2407），整合索赔记录C1、遥测T1、维修笔记N1、服务公告B1和术语表G1，对比sensor drift与damper linkage failure两个候选标签。初始Sensor边际为0.907、Linkage为0.839；审查者以序列号不匹配驳回S3并新增S6后，Sensor边际降至-1.016，Linkage保持0.839，系统选择damper linkage failure。论文强调这些分数为示例性输入，非校准概率或实测准确率。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三：其一，评分机制尚缺理论保证，signed-sum 规则对相关证据（如 S1、S2 同源于 C1）会虚增边际，未来需用 DF-QuAD 等公理化方法做形式化检验，并引入共享溯源识别与决策稳定性测试；其二，跨系统保修记录与晋升门控仍是提案，未测量其对审核工作量与决策质量的影响，可实证评估审核时间、错误提交率与后续反转率；其三，学习闭环未验证——已确认决策回写后，需测量先例对同系列设备的增益、错误先例的扩散范围及固件修订导致先例失效的时点。此外，可探索基于风险的自适应路径：对低风险且证据无歧义的编辑（如拼写修正）自动提交并保留原值与回滚手段，仅在不确定时触发完整论证，从而在可控性与效率间取得平衡。

### Q6: 总结一下论文的主要内容

论文针对工业数据治理中结构化遥测与点表、非结构化手册与服务记录分别管理、分类链接依赖少数专家且LLM智能体直接写入元数据可能扩散错误、人工一键审批缺乏审查记录的问题，提出“可争议治理”模式。其方法为：分析器收集证据与先例，多个专业智能体针对有争议的元数据决策给出带引用、带基础评分的支持或反对论证，采用定量双极论证框架迭代打分；数据管理员在提交前可接受、拒绝、修改或新增论证，系统重新评分后由评分引擎选出最高分候选，最终器仅解释结果与传播步骤，审计者可依据存储论证独立复算。治理记录保存证据、干预与结果，版本化术语表提供模型特定缩写释义，分流机制仅将低置信提案送入完整论证，晋升门控只允许已验证决策成为先例。两个HVAC用例表明，该方法能纠正基于名称的误判并保留纠正理由，在保修故障模式决策中揭示索赔码、遥测、技师记录与公告适用范围之间的冲突，使决策可追溯、可审计、可复用。
