---
title: "Agentic RCA for Internet-Scale Services Using Constrained Creativity"
authors:
  - "Sayan Sinha"
  - "Vipul Harsh"
  - "B. Aditya Prakash"
  - "Vyas Sekar"
  - "Hui Zhang"
date: "2026-10-06"
arxiv_id: "2610.08622"
arxiv_url: "https://arxiv.org/abs/2610.08622"
pdf_url: "https://arxiv.org/pdf/2610.08622v1"
categories:
  - "cs.NI"
  - "cs.AI"
tags:
  - "Agentic RCA"
  - "LLM Agent"
  - "Constrained Creativity"
  - "Root Cause Analysis"
  - "Internet-Scale Services"
  - "Explainable Diagnosis"
  - "Domain-Specific Language"
  - "Verifiable Output"
  - "Cost Efficiency"
  - "Failure Troubleshooting"
relevance_score: 7.5
---

# Agentic RCA for Internet-Scale Services Using Constrained Creativity

## 原始摘要

System administrators of Internet-scale services need to resolve failure incidents to maintain reliability of such services. Ideally, we want a troubleshooting system to be: (1) expressive to known and unknown incidents with high accuracy; (2) cost efficient at scale; (3) explainable to provide actionable insights operators can act on; and (4) entail low effort from the operators. Unfortunately, most existing systems, including emerging LLM-assisted agentic workflows and structured frameworks for authoring diverse RCA algorithms fall short of achieving all four requirements. We present E4, a novel agentic system for troubleshooting for Internet-scale services. E4 embodies the paradigm of constrained creativity that combines the best of LLM-assisted automation and exploration with the explainability and efficiency of a structured approach. Instead of allowing an LLM agent to write arbitrary code or generate arbitrary responses, we provide the agent a restricted DSL to generate its response via simple loop-free data flow programs. This DSL, equipped with high level operators for troubleshooting, makes E4's output accurate, verifiable and explainable. On a mix of synthetic and real-world workloads, E4 achieves up to 62% better accuracy compared to state-of-the-art solutions, while providing more explainable responses at up to 12x reduced cost.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决互联网规模服务中根因分析（RCA）系统难以同时满足四项关键需求的问题。随着现代互联网服务规模扩大，KPI异常频发，运维人员需要自动化诊断系统来快速定位根因并采取缓解措施。理想系统应具备：对已知和未知事件的高表达力与高准确率、大规模下的成本效率、可解释性以提供可操作的洞察，以及低使用门槛。

然而，现有方法均无法同时满足这四点。基于签名的专用算法和ML方法虽高效可解释，但表达力有限，难以覆盖多样化和未来事件；结构化数据分析框架虽灵活可解释，但需要分析师投入大量精力编写查询和工作流；LLM辅助的智能体系统虽具表达力，却易产生不准确、幻觉和不可验证的逻辑，且token和数据成本高昂，可解释性差。论文通过定性对比表明，每类方法只能满足部分需求。

因此，本文提出E4系统，核心问题是：如何结合LLM辅助自动化的表达力与结构化方法的高效性和可解释性，构建一个能同时满足表达力、效率、可解释性和低门槛四项要求的RCA系统。其思路是采用“约束创造力”范式，限制LLM仅生成受限DSL中的无循环数据流程序，而非任意代码或响应，从而在保持灵活性的同时确保输出的准确、可验证和可解释。

### Q2: 有哪些相关研究？

现有研究大致可分为三类。第一类是专用算法，如 Sage、Murphy 等，针对客户端或后端特定故障类型设计定制算法，可解释且高效，但表达能力有限、开发成本高。第二类是结构化数据分析/RCA 工作流框架，如 ExplainIt! 提供声明式 SQL 接口探索和排序候选原因，MoCE 将假设探索表达为算子 DAG 并复用计算。这类框架灵活且可解释，但仍需分析师手动提供查询、工作流或新分析方法。第三类是 LLM 辅助的 RCA 智能体，又分两个子类：工作流引导型智能体（如 LLexus、StepFly）用预定义流程约束调查，易理解但表达受限；编码型智能体（如 Terminus、RCA-Agent）可按需生成新分析代码，表达能力强但代码和推理轨迹难以审查，且存在幻觉、死胡同探索和 token 成本高的问题。本文 E4 与上述工作均不同：它借鉴结构化框架思想，但用 LLM 组合分析 DAG 并在需要时合成新算子；同时以受限 DSL 约束 LLM 输出，从而在表达能力、效率、可解释性和低使用成本四个维度上同时满足要求，而现有各类方法均只能满足其中部分。

### Q3: 论文如何解决这个问题？

E4 的核心思路是“约束式创造”（Constrained Creativity），即在 LLM 驱动与结构化方法之间取得平衡。它不允许 LLM 自由生成任意代码或回答，而是要求所有诊断分析都表达为一个受限于特定 DSL 的无环数据流程序（DAG）。该 DSL 提供面向故障诊断的高层算子，如候选生成、候选评分与摘要聚合算子，使输出可验证、可解释且高效。

整体框架分三阶段。第一，Bootstrap：每个部署运行一次，LLM 读取初始算子、示例 playbook、遥测 schema 与任务描述，生成部署专属算子库和 playbook，并用静态验证与合成数据执行检查。第二，Runtime adaptation：每次事故时，agent 先选择已有 playbook 并实例化超参数；若不足，则用现有算子组合新 DAG。验证器检查算子存在性、类型安全、无环性、候选生成算子只能被评分或生成算子消费、程序最终唯一输出。通过后由运行时执行引擎调度 SQL、ML 推理等操作，并缓存中间结果。第三，Evolution：若当前算子库无法解决，LLM 根据失败历史评估诊断缺口，提出新算子并组合 playbook；只有能解决升级事故的新算子才被永久纳入库。

创新点在于：用固定语法约束 LLM 的程序空间，兼顾表达力与可解释性；LLM 从不直接接触遥测数据，只生成 DAG，降低 token 成本并保护数据主权；算子库可随事故演化，避免算子膨胀；DAG 结构天然支持中间结果复用与并行执行。

### Q4: 论文做了哪些实验？

论文在四个公开基准和一个自定义基准上评估了E4系统。数据集包括OpenRCA中的Market、Bank和Telecom部署，以及ORCA-bench，均提供后端遥测数据；此外，作者扩展了DeathStarBench的社交网络应用，加入模拟客户端、属性和会话事件历史，构建了包含64个故障事件的DSB语料库用于客户端诊断。ORCA-bench的窗口从前端KPI异常构建，不使用故障注入时间。对比方法为现有最先进方案（如Terminus等基线）。主要结果显示：E4在所有基准上达到65%–91%的准确率，而基线最高不超过56%；相比Terminus，E4准确率或召回率约为其1.3倍，平均成本降低8.1倍；整体上E4准确率最高提升62%，成本最多降低12倍。实验还分析了故障类型、配方阶段及对工作负载条件的敏感性。

### Q5: 有什么可以进一步探索的点？

E4 的核心局限在于其受限 DSL 的表达能力边界：无循环的数据流程序虽保证了可验证性与低成本，但可能无法覆盖需要迭代推理、时序回溯或跨层因果链追踪的复杂故障场景。此外，论文仅在四个公开基准和一个自建基准上验证，真实互联网规模服务的噪声、概念漂移与多故障并发尚未充分考察。未来可探索的方向包括：一是让 DSL 支持受控的迭代或递归算子，在保持可解释性的前提下提升对深层因果链的表达力；二是引入在线学习机制，使算子库能随新故障模式自动扩展，缓解对人工预定义算子的依赖；三是将约束创造力范式推广到修复阶段，即不仅定位根因，还生成可验证的修复计划；四是研究多智能体协作下的 DSL 组合，让不同 agent 分别负责指标、日志、链路等模态，再通过结构化协议融合结论。这些方向有望在准确性、成本与可解释性之间取得更优平衡。

### Q6: 总结一下论文的主要内容

论文针对互联网规模服务的故障根因分析（RCA）问题，提出理想系统应同时具备表达性、高效性、可解释性和低使用门槛，而现有签名方法、结构化框架及LLM智能体工作流均难以兼顾。为此，作者提出E4系统，其核心思想是"约束性创造"：不让LLM自由生成代码或回答，而是限定其只能生成由受限DSL编写的无环数据流程序，该DSL提供故障排查高层算子，使输出准确、可验证且可解释。E4包含三个阶段：Bootstrap根据部署遥测模式定制算子库与剧本；Runtime adaptation按事件组合DAG进行诊断；Evolution在现有词汇不足时生成新算子并复用。在合成与真实负载上，E4的Top-3根因准确率最高提升62%，成本降低最高达12倍，且响应更具可解释性。
