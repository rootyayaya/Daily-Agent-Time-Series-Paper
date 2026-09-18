---
title: "Semantic Layer Induction from Raw Telemetry via Hierarchical LLM and RAG Abstraction"
authors:
  - "Yuanzhe Jia"
  - "Ali Anaissi"
date: "2026-09-17"
arxiv_id: "2609.19615"
arxiv_url: "https://arxiv.org/abs/2609.19615"
pdf_url: "https://arxiv.org/pdf/2609.19615v1"
categories:
  - "cs.CL"
  - "cs.AI"
  - "cs.IR"
  - "cs.SE"
tags:
  - "LLM"
  - "RAG"
  - "telemetry"
  - "semantic layer"
  - "hierarchical abstraction"
  - "LLM-as-Judge"
  - "industrial logs"
  - "unsupervised"
  - "semantic clustering"
  - "canonical naming"
relevance_score: 7.5
---

# Semantic Layer Induction from Raw Telemetry via Hierarchical LLM and RAG Abstraction

## 原始摘要

Modern applications generate massive volumes of raw telemetry data, but translating those noisy, heterogeneous event streams into actionable business insights remains a fundamental challenge. Data engineers and analysts expend substantial effort reconciling semantic discrepancies, hand-crafting parsing logics, and maintaining fragile mappings between raw data and business KPIs. In this paper, we present an end-to-end framework that fully automates the construction of a business semantic layer from application raw logs. Our approach introduces a two-stage semantic abstraction: first, high-level business features are identified via LLM inference augmented with domain-specific industry knowledge; second, fine-grained business nodes are derived through a structured pipeline comprising data refinement, hybrid retrieval, multi-stage filtering, semantic clustering, and canonical naming. Evaluation on production-scale telemetry demonstrates that our system improves human-assessed semantic quality from 50 to 80+ on a 100-point scale, reduces maintenance effort by 80%, filters out 74% of noise, and achieves 0.87 Cohen's kappa via an integrated LLM-as-Judge evaluation, enabling continuous, scalable quality assurance. Overall, our work distinguishes itself from prior work by addressing the novel problem of business semantic layer induction from raw telemetry, operating without labeled training data or manual rule engineering.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

现代应用每天产生海量原始遥测数据，但将这些嘈杂、异构的事件流转化为可操作的业务洞察仍是一项根本性挑战。其核心困难不仅在于数据规模，更在于语义异构性：同一用户行为（如“搜索商品”）在不同平台和版本中可能被记录为 search_click、search_submit、button_click 等不同事件，参数与模式各异。这种碎片化迫使数据工程师和分析师陷入无休止的手工映射、逐仪表盘定制 SQL 逻辑以及跨团队关于“遥测数据到底意味着什么”的争论，企业往往需维护数千个自定义解析器，耗费大量工程时间。

现有方法均存在明显不足：手工构建解析器虽精确但脆弱且难以跨异构日志格式扩展；基于语法的解析方法能提取模板却缺乏业务语义理解；监督学习方法需要为每个埋点大量标注数据，难以适应快速迭代的应用；近期基于 LLM 的日志解析方法也主要停留在语法级模板提取，而非向业务概念的语义映射。

因此，本文要解决的核心问题是：在没有标注训练数据、也无需人工规则工程的前提下，如何从原始遥测数据中自动归纳出一个稳定的业务语义层，即从原始日志到可直接对齐客户需求与业务目标的可解释洞察之间的规范化映射。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，传统日志解析方法如Drain、LogParser通过聚类和频繁模式挖掘提取日志模板，但仅停留在语法层面，不理解语义；LogParser-LLM等基于LLM的解析器提升了语义感知能力，但仍聚焦模板抽取与字段命名，而非将日志映射到业务语义概念；Matryoshka等工作用LLM生成语义感知解析器，但目标是映射到安全schema用于威胁检测。应用类方面，过程挖掘领域探索了语义感知的事件日志分析，但多分析已有日志而非从原始遥测构建；数据管理领域如Hoseini等综述了数据湖语义管理，Bian等、Zhao等研究了知识图谱构建与本体学习，Kropshofer等、Tonnarelli等考察了数据目录工具，但这些方法依赖预定义本体，难以应对多平台命名异构，且需额外转换才能聚合为业务KPI。评测与RAG类方面，EventRAG、TM-RAG、GenDFIR将RAG用于事件知识图谱、时间线本体和网络取证等任务，证明结构化检索有助推理，但均面向任务特定的一次性查询。本文区别在于：首次提出从原始遥测归纳业务语义层这一新问题，无需标注数据或人工规则，并用RAG检索候选映射规则以构建可复用、可泛化的语义层。

### Q3: 论文如何解决这个问题？

论文将语义层归纳形式化为从原始遥测事件语料中寻找“业务特征—业务节点”二元组集合的问题，并指出直接学习扁平映射存在映射空间大、语义分散、易受平台命名影响等缺陷。为此，作者提出两级层次（Feature→Node）作为归纳偏置，先推理高层业务能力，再细化到具体动作，从而缩小搜索空间并利用行业先验。

整体框架包含五个阶段。第一阶段是数据精炼：先对元数据列进行重要性打分，剔除低分列；再对枚举值做分词、随机串检测与掩码，并用正则合并等价枚举，得到低基数、干净的向量空间。第二阶段是特征识别：对精炼数据分层采样，结合行业标准特征列表作为先验，提示 LLM 生成一两个名词组成、避免 UI 词汇的高层业务特征，并通过覆盖度、词数、相似度门控做质量检查。第三阶段是规则检索：将精炼数据编码为稠密向量，以特征名生成查询向量做相似检索，同时用 BM25 关键词匹配，加权融合后返回 top-k 条件子集，并翻译为 SQL 式谓词。第四阶段是候选规则过滤：先做硬规则过滤（如广告点击、API 错误），再由 LLM 逐条判断是否属于该业务特征。第五阶段是聚类与命名：LLM 将语义等价的规则聚成簇，再按“[名词]+[动词]”格式赋予规范名称，保证同一行为同名、优先通用名。

创新点在于：无需标注数据和人工规则工程；跨阶段共享潜在语义空间，形成反馈约束；以属性级条件而非整事件为检索单元；并用 LLM-as-Judge 实现持续质量评估。

### Q4: 论文做了哪些实验？

论文在真实电商场景下进行了系统评估，数据集来自某在线零售商网站六个月的数百万用户会话日志，覆盖浏览、搜索、加购到购买的全旅程。评估指标包括人工语义正确性评分、噪声过滤率、人工维护工作量削减和LLM-as-Judge与人类专家的一致性（Cohen's kappa）。基线为初始提示工程版本，不含业务特征识别、RAG检索和LLM语义过滤。主要结果：在100个抽样语义映射上，5位专家盲评显示完整流水线平均得分82.3（σ=9.7），显著高于基线51.6（σ=14.2，p<0.01）；业务覆盖率从62%提升至98%，命名一致性从59%提升至96%。硬规则过滤与LLM语义过滤共剔除74%的候选规则噪声，保留26%的规则覆盖超90%语义。人工维护从每周10小时降至约2小时，减少80%；新指标查询从4小时降至25分钟内。在500条人工标注黄金集上，LLM-as-Judge与专家评分的一致性达到Cohen's kappa 0.87。消融实验表明各组件均有贡献，其中嵌入检索、业务特征识别和枚举归一化最为关键，移除后分别下降24.5、18.2和16.3分。

### Q5: 有什么可以进一步探索的点？

尽管该框架在电商生产级遥测数据上表现优异，但仍存在若干可深入探索的方向。首先，其泛化能力受限于单一领域，未来可引入跨域迁移学习，验证在金融、物联网、医疗等异构日志上的适应性。其次，当前语义层构建依赖LLM推理与检索，缺乏因果结构建模，未来可融合因果发现与反事实推理，使语义节点不仅描述“是什么”，还能支持根因定位与干预分析。第三，LLM-as-Judge虽达到0.87 kappa，但仍存在评判偏差与幻觉风险，可探索多模型投票、不确定性量化及人机协同的持续校准机制。此外，语义层的动态演化问题尚未充分讨论，例如业务概念漂移时如何增量更新节点与映射。最后，可引入Agent工作流，让系统自主发现语义缺口、主动请求专家反馈，形成闭环自进化语义层。

### Q6: 总结一下论文的主要内容

本文针对原始遥测数据语义异构、难以直接转化为业务洞察的问题，提出从应用原始日志中自动归纳业务语义层的端到端框架。问题定义为：给定原始遥测事件语料与可选行业分类体系，寻找由业务特征及其对应业务节点构成的分层语义层，且无需标注数据或人工规则。方法上采用两级语义抽象：先通过LLM结合行业知识识别高层业务特征，再经数据精炼、混合检索、多阶段过滤、语义聚类与规范命名生成细粒度业务节点。实验表明，语义质量从50分提升至80分以上，维护工作量减少80%，过滤74%噪声，LLM-as-Judge与人工评估的Cohen's kappa达0.87。该工作首次系统解决原始遥测到业务语义层的归纳问题，显著降低人工维护成本。
