---
title: "Beyond Top-K: Replacing Black-Box Retrieval with Interpretable Agentic Operations"
authors:
  - "Sagar Tamang"
  - "Ayush Vyas"
  - "Tabarakul Hazarika"
date: "2026-08-06"
arxiv_id: "2608.06305"
arxiv_url: "https://arxiv.org/abs/2608.06305"
pdf_url: "https://arxiv.org/pdf/2608.06305v2"
github_url: "https://github.com/twospoon/READ"
categories:
  - "cs.AI"
  - "cs.CL"
  - "cs.IR"
tags:
  - "Agentic RAG"
  - "Interpretable Retrieval"
  - "Document Search"
  - "Model Context Protocol"
  - "Audit Trail"
  - "Financial Documents"
  - "Tool Use"
  - "Evidence Routing"
relevance_score: 6.5
---

# Beyond Top-K: Replacing Black-Box Retrieval with Interpretable Agentic Operations

## 原始摘要

Retrieval-augmented generation over long documents is dominated by one design: chunk the text, embed the chunks, and surface the top-k nearest neighbours of the query. We argue that for an important class of documents -- financial statements, audit reports, regulatory returns -- this design is structurally unsound, and we make the argument measurable. On a 780-page government financial report, 86.8% of content lines are table rows, thousands of near-identical figures compete in one embedding space, and a figure inherits its unit from a header a median of 13 lines above it -- so a chunk boundary routinely separates a number from whether it is in lakh or crore, an error of two orders of magnitude. A table-aware chunker built as a steelman fixes the unit problem but leaves 27-30% of numeric chunks with no fiscal-year header at every chunk size we tried. We propose READ (Reliable Embedding-free Agentic Document-search), in which an agent reads the raw document through three deterministic operations -- normalized lexical search, structural navigation, and bounded span reads -- exposed over the Model Context Protocol, so a trajectory is a replayable audit trail, not an opaque similarity score. On 51 verified questions READ answers 58.8% against dense retrieval's 15.7% (p_Holm = 2 x 10^-5) -- or 35.3% tuned, which READ still leads by 23.5 points (p_Holm = 0.017). An agent given the same loop but a top-k tool reaches only 27.5%, locating the gain in the interface rather than in iteration. We also report what the evidence does not support: BM25 is statistically indistinguishable from READ, so our result separates embedding-based from embedding-free retrieval, not agentic from lexical search.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决长文档检索增强生成（RAG）中“分块-嵌入-取Top-K”这一主流范式在精确性关键文档上的结构性失效问题。研究背景聚焦于财务报表、审计报告等表格密集型文档，其具有高度表格化、数字近重复密集、语义依赖版面布局（如单位与财年由远处表头决定）三大特性。

现有方法的不足在于：传统稠密检索将上下文截断为相似度排序的片段，机制不透明且无法验证；分块会割裂数字与其单位/财年表头的关联，导致数量级错误（如“lakh”与“crore”相差百倍）；即使采用表格感知分块器（steelman基线），仍无法解决27-30%数字块缺失财年表头的问题，且检索过程不可审计、不可回放。

本文核心问题是：能否用可解释的智能体操作替代黑盒Top-K检索，实现对原始文档的确定性读取，从而在精确性关键文档上显著提升问答准确率，同时提供可重放的审计轨迹？作者提出READ系统，通过归一化词法搜索、结构导航和受限跨度读取三种确定性操作，经MCP协议暴露给智能体，旨在验证嵌入无关的检索接口是否优于稠密检索，并区分性能提升源于接口设计而非单纯迭代次数。

### Q2: 有哪些相关研究？

相关研究主要围绕检索增强生成（RAG）的改进展开。方法类工作中，密集检索（如Dense Passage Retrieval）及其变体（late-interaction、稀疏扩展）是主流基线，但BEIR基准已显示BM25等词法匹配在零样本下竞争力强。针对长文档，Self-RAG等自适应方案虽优化检索时机，仍依赖索引维护。应用类研究聚焦表格密集型文档：SpreadsheetLLM通过压缩表格适配上下文，FRTR构建多粒度嵌入融合，但均需复杂语料定制索引。评测类工作如grep与向量检索的系统对比（Agentless、SWE-agent）表明词法工具在代码库和对话记忆中更优，BrowseComp-Plus上的直接语料交互也优于检索API。

本文与上述工作的区别在于：一是领域聚焦单一超长表格文档（如780页财务报告），而非多文档语料；二是任务要求精确数值且需计算推导，非简单检索；三是处理PDF转换噪声，这是干净语料上未出现的挑战；四是强调可解释性，将确定性操作轨迹作为审计日志，满足金融监管需求。与Chronos等记忆增强系统相比，READ通过MCP协议将工具暴露为可复现的审计轨迹，而非黑盒相似度分数。

### Q3: 论文如何解决这个问题？

论文提出了一种名为READ（Reliable Embedding-free Agentic Document-search）的可解释智能体检索框架，以替代传统的黑盒top-k向量检索。其核心设计是将文档检索重构为三个确定性操作：归一化词法搜索（search）、结构导航（outline）和有界跨度读取（read），并通过Model Context Protocol（MCP）暴露为工具接口。

整体框架由一个只读MCP服务器构成，服务器状态仅为文档文本，不包含任何嵌入模型或向量索引。三个核心模块各司其职：search对所有行进行归一化匹配（处理数字分组、跨单元格分词等转换伪影），outline提供标题与行号映射，read支持按行号区间读取最多400行内容。智能体在闭环中组合这些操作：先假设词法锚点，搜索后对照大纲检查命中，再读取足够宽的跨度以捕获单位标题，最终提取答案并附带引用位置。

关键创新点有三：其一，read是跨度寻址而非分块寻址，智能体在观察证据位置后动态选择读取区间，可向上扩展以包含单位头，而固定分块无法做到；其二，轨迹完全确定性且可重放，每次操作都是文档与参数的纯函数，第三方可逐行验证证据链；其三，针对转换伪影设计双重归一化影子行，解决了数字分组和跨单元格分词导致的检索失败。实验表明，READ在51个验证问题上达到58.8%准确率，远超稠密检索的15.7%，且增益来自接口设计而非迭代本身。

### Q4: 论文做了哪些实验？

论文在51道验证问题上进行了系统性实验，所有系统共享同一骨干模型（gemini-2.5-pro）、答案格式和成本/延迟核算，仅接口不同。对比系统包括：READ及其两个消融（naive-grep字面匹配、no-outline移除结构导航）、密集检索（bge-base-en-v1.5编码器+表感知分块）、BM25、混合检索（RRF+交叉编码器）、AgenticVec（同循环但用向量搜索工具）、Oracle和LongCtx。问题覆盖六类：单图查找、多行聚合、跨报表算术、结构导航、不可回答探针和转换受限项。

主要结果：READ准确率58.8%，显著优于密集检索的15.7%（Δ=+43.1pp，p_Holm=2×10⁻⁵）、混合检索的29.4%（p=0.016）和AgenticVec的27.5%（p=0.012），证明增益来自接口而非迭代。但BM25达51.0%，与READ无显著差异（Δ=+7.8pp，p=1.00），属功效不足的零结果。密集检索调优后可达35.3%，READ仍领先23.5pp（p=0.017）。按类别看，单图查找差距最大（READ 70.8% vs 密集12.5%），结构导航各类系统相近。READ成本最高（$0.058/题，31.4秒），但失败分析显示密集检索13题未将证据放入上下文，READ仅4题。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从以下维度展开：首先，当前基准仅51个问题且集中于单一财务报告类型，统计功效不足以支撑“READ优于BM25”的结论，未来需扩展至多领域、多语言、更长文档的评测集，并引入更细粒度的错误归因（如区分表格结构损坏、跨页表头继承等）。其次，READ的确定性操作（正则、结构导航、跨度读取）虽可审计，但依赖人工设计的规则，对非表格化或半结构化文档（如合同、科研论文）的泛化性存疑，可探索将操作参数化并利用强化学习自动学习导航策略。第三，论文显示READ的grounded率低于BM25，说明读取更多文本反而引入未支撑数字，未来可设计“证据置信度校验”模块，在生成前对每个数字与已读文本进行交叉验证，或结合小型判别模型过滤幻觉。第四，成本与延迟是实际部署瓶颈，可研究缓存机制、并行化操作调用，或蒸馏一个轻量模型模拟READ的导航行为。最后，BM25与READ的统计无差异暗示纯词法匹配已捕捉大部分结构信息，未来可尝试将READ的操作轨迹作为弱监督信号，训练一个混合检索器，在保留可解释性的同时降低推理开销。

### Q6: 总结一下论文的主要内容

该论文针对长文档检索增强生成中“分块-嵌入-取Top-k”范式的结构性缺陷展开研究，以780页政府财务报告为例，量化了表格密集、数字近重复、单位继承距离远等特征，指出传统方法常因分块边界割裂数字与其单位/财年上下文而导致严重错误。作者提出READ（可靠无嵌入智能体文档搜索）方法，通过三个确定性操作——归一化词法搜索、结构导航和受限跨度读取——让智能体直接读取原始文档，并以MCP协议暴露接口，使轨迹成为可回放的审计线索。在51个验证问题上，READ准确率达58.8%，显著优于稠密检索的15.7%和智能体Top-k检索的27.5%，但BM25与READ无统计显著差异，表明增益来自去嵌入化接口而非智能体循环本身。研究还揭示了PDF转换保真度对所有方法的共同限制，以及稠密检索在数值密集型查询上的系统性失效。
