---
title: "Deploying a Control-Logic LLM Assistant in Air-Gapped Power Plants: Lessons in Source Authority and Bounded Retrieval"
authors:
  - "Yiwei Fu"
  - "Nicholas Gabriel"
date: "2026-11-16"
arxiv_id: "2611.20398"
arxiv_url: "https://arxiv.org/abs/2611.20398"
pdf_url: "https://arxiv.org/pdf/2611.20398v1"
categories:
  - "cs.AI"
tags:
  - "工业控制逻辑"
  - "LLM助手"
  - "工具调用"
  - "知识图谱"
  - "证据检索"
  - "有界检索"
  - "气隙环境"
  - "操作员辅助"
  - "确定性执行"
  - "回退意图分类"
relevance_score: 6.5
---

# Deploying a Control-Logic LLM Assistant in Air-Gapped Power Plants: Lessons in Source Authority and Bounded Retrieval

## 原始摘要

Deploying Large Language Model (LLM) assistants in industrial operational technology environments poses constraints largely absent from cloud applications: site policies restrict engineering and operational data from leaving the plant, on-premises compute is limited, and incorrect causal attribution can mislead incident response. We report lessons from deploying a control-logic evidence layer that underpins a broader on-premises operator assistance system at two gas power plants. Two prototypes revealed where generative models added avoidable uncertainty and cost. The first used a Vision Language Model (VLM) to reconstruct control topology from PDF printouts routinely exchanged by engineers. Across the full 6,979-page document, extraction reached 0.51 connection precision and required 3.1 hours on 4xH200 GPUs; consultation with controls engineers then revealed a native structured export from the authoring system. The second used an LLM tool-calling agent to plan repeatedly over eight predefined graph operations. In a controlled benchmark of 40 template-generated questions, replacing this agent with explicit execution plans reduced mean token use by 20x and median latency by 3x, with identical retrieved node sets across repeated runs. The deployed design ingests the authoritative export into a versioned knowledge graph, executes bounded graph operations in fixed software, and confines the local LLM to fallback intent classification and evidence-grounded explanation. At one site, the graph contains 221K nodes across seven controllers. Our experience suggests a practical division of labor for high-consequence AI: LLMs interpret natural-language requests and explain results, while deterministic software constructs and retrieves technical evidence grounded in authoritative sources. Abstention, entity disambiguation, graph versioning, and read-only integration provide additional safeguards.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决在气隙（air-gapped）工业电厂环境中部署LLM助手时，如何可靠地构建和检索控制逻辑证据的问题。研究背景是：电厂控制逻辑由数万个传感器、功能块和信号依赖构成，跳闸或报警后工程师需沿控制逻辑逆向追溯因果链，单是追溯就可能耗费数小时并依赖资深专家经验；而OT网络禁止数据外传、本地算力受限，且错误的因果归因会误导事故响应，因此必须本地化、版本化并保持精确信号路径。现有方法存在明显不足：工业知识图谱很少暴露可执行的块级逻辑，而agentic图系统面向更开放的查询空间，均未直接处理这一组合；作者的两个原型也暴露了生成模型的代价——用VLM从6,979页PDF重建拓扑仅达0.51连接精度且耗时3.1小时，用LLM工具调用代理反复规划图操作则token消耗高、延迟大。本文的核心问题是：如何划分生成模型与确定性软件的职责边界，即让LLM仅负责自然语言意图理解与证据解释，而由图构建与检索由基于权威导出的确定性软件完成，从而在气隙电厂中实现有界、可追溯、可弃权的控制逻辑证据检索。

### Q2: 有哪些相关研究？

本文相关工作可分为三类。方法类方面，制造知识图谱通常融合生命周期、设备、过程与事件数据，或基于AutomationML等标准构建结构；诊断知识图谱则匹配历史服务告警中的模式。这些表示无法暴露可执行的块级依赖，难以追踪保护信号在控制器逻辑中的传播路径。最接近的工作从PLC代码中提取告警相关逻辑再做统计根因学习，而本文则将完整生产规模的控制逻辑表示为可直接遍历的证据源。自然语言访问结构化数据常用text-to-SQL或text-to-Cypher，GraphRAG与Think-on-Graph将多跳检索部分交给模型推理，Multi-Agent GraphRAG增加模式校验、实体验证与查询精化，但其最佳基准配置准确率仅77%。这些方法面向更开放、更广的查询空间；本文部署的接口只暴露八个已知操作，遍历可表达为固定计划，生成式规划在此接口下只增加可变失败模式而无额外表达力。应用与评测类方面，根因方法从监控指标、异常传播或工业时间序列推断图结构，LLM智能体在从原始观测诊断事件时表现有限。本文指出这些方法与自身互补：运行时数据确立事件中发生了什么，而本文图谱揭示观测状况可传播所经的编程依赖。

### Q3: 论文如何解决这个问题？

论文的核心思路是把“解释”和“取证”严格分工：LLM 只负责理解自然语言请求与解释检索结果，而技术证据的构建与检索完全交给确定性软件，并以权威数据源为唯一依据。

整体框架包含两条流水线。其一是图构建流水线：直接摄取 GE Vernova Mark VIe ToolboxST 导出的 Block Pin Report CSV（每台控制器超 10 万行），单遍解析出 Block、Signal 实体，按 Device|Program|Task|Block 复合键消歧（如 RUNG_1 出现在 150 多个上下文中），生成 FEEDS_INTO / WRITES_TO 信号流边与 CONTAINS 执行层级边，并把方程作为 Block 属性存储；整图在笔记本上 10 秒内完成，单站点含 7 台控制器、22.1 万节点。其二是查询流水线：分类（正则快路径 + LLM 兜底，识别 8 类查询）→ 实体解析（精确/包含匹配，歧义时返回候选让用户澄清）→ 固定 Cypher 执行器（BFS/最短路径，限制深度≤10、前沿≤8、节点≤150、路径≤16，并标记截断）→ LLM 基于证据合成解释，每查询至多两次模型调用。

创新点在于：用版本化知识图谱作为权威源与语言接口之间可检查的“契约”；以有界图操作替代 LLM 工具调用规划（基准中 token 降 20 倍、延迟降 3 倍且结果稳定）；把 pin 元数据折叠为边属性，将信号步长从 4 跳降为 2 跳；辅以拒答、实体消歧、图版本化与只读集成等安全措施。

### Q4: 论文做了哪些实验？

论文围绕两个“模型优先”原型与最终部署设计开展了实验。首先是VLM从控制逻辑PDF重建拓扑的实验：对某燃气电厂单台GE Vernova控制器（Block Pin Report共168,220行）的6,979页PDF逐页图像化抽取，Qwen 3.5-397B-A17B在全文上仅达0.51连接精度、36%方程准确率，4×H200耗时3.1小时（约124美元）；Gemini 3.1 Pro在共享样本上连接精度0.24、方程准确率4%。相比之下，原生Block Pin Report不到10秒即完成导入。其次是工具调用Agent与有界执行计划的受控对比：两者均用Qwen 3.5-35B-A3B-FP8、同一知识图谱与合成提示，基准为围绕一个报警的6,860节点邻域中模板生成的40个问题、覆盖8种图操作、各运行3次，用DeepEval GEval评分。有界方案答案正确率94%（Agent 85%），中位延迟4.8s对14.2s，p95为12.7s对108.6s，平均token 1.2K对24K，数据库往返2.0对9.1，跨运行检索节点Jaccard为1.0对0.61。此外构建全厂七控制器图谱（221,406节点、402,240边），笔记本上构建时间小于30秒，并回溯重放了2025年10月CBV跳闸案例。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在：评测仅覆盖单一厂商的控制格式，查询基准是基于单一报警的模板生成问题，LLM 回答由 LLM 裁判而非独立人工评审，且现场证据仅为一次回溯性事故重放，缺乏对操作员响应时间或机组可用率等真实运行指标的测量。未来可探索的方向包括：一是开展跨厂商、跨控制格式的泛化验证，检验知识图谱构建与有界图操作在异构工程导出上的可移植性；二是引入本地隐私保护的运行指标采集，在不违反隔离策略的前提下量化助手对事故响应效率的实际影响；三是面向历史数据做时序推理，将确定性依赖图与运行时证据更紧密地结合，辅助判断“哪个可能条件实际发生”。此外，可研究图谱版本演进下的增量重建与变更影响分析、更强的实体消歧与弃权校准机制，以及让 LLM 仅承担意图分类与证据解释时的可解释性与不确定性量化，从而在保持只读、可追溯边界的同时提升辅助决策的可信度。

### Q6: 总结一下论文的主要内容

论文针对空隔离（air-gapped）电厂中部署LLM助手面临的约束——数据不得出厂、本地算力有限、错误因果归因可能误导事故响应——提出并验证了一种“控制逻辑证据层”的设计。问题定义是：如何在不牺牲可靠性的前提下，让LLM辅助操作员检索和解释控制逻辑证据。方法上，作者通过两个原型揭示生成模型的局限：用VLM从6979页PDF重建控制拓扑仅达0.51连接精度、耗时3.1小时；用LLM工具调用代理反复规划八种图操作，在40题基准中，改为显式执行计划后token用量降低20倍、中位延迟降低3倍，且检索节点集完全一致。最终部署方案将权威导出数据摄入版本化知识图谱（单站点含221K节点、七个控制器），由确定性软件执行有界图操作，LLM仅负责意图分类与基于证据的解释，并辅以弃答、实体消歧、图版本化和只读集成等保障。结论是：高风险工业AI应让LLM负责语言理解与解释，确定性软件负责构建和检索权威证据。
