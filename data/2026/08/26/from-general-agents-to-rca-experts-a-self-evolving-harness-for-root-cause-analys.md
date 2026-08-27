---
title: "From General Agents to RCA Experts: A Self-Evolving Harness for Root Cause Analysis"
authors:
  - "Haiyu Huang"
  - "Jiewei Lyu"
  - "Zhihan Jiang"
  - "Jinyang Liu"
  - "Xiao He"
  - "Tieying Zhang"
  - "Wu Xiang"
  - "Michael R. Lyu"
date: "2026-08-26"
arxiv_id: "2608.25661"
arxiv_url: "https://arxiv.org/abs/2608.25661"
pdf_url: "https://arxiv.org/pdf/2608.25661v1"
categories:
  - "cs.SE"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Root Cause Analysis"
  - "Self-Evolving Agent"
  - "LLM-based Diagnosis"
  - "Tool Use"
  - "Verification"
  - "Industrial Deployment"
  - "Experience Accumulation"
  - "Harness Design"
  - "Multi-agent Reasoning"
relevance_score: 9.5
---

# From General Agents to RCA Experts: A Self-Evolving Harness for Root Cause Analysis

## 原始摘要

Automated root cause analysis (RCA) with large language models (LLMs) has drawn growing attention. Today, SREs typically automate RCA with LLMs in one of two ways: directly using a general-purpose agent (e.g., Codex or Claude Code) for diagnosis, or building a specialized RCA agent from scratch. As mainstream general agents grow more capable and iterate quickly, our quantitative study finds that the former now often surpasses the latter. Its accuracy, however, still falls short of production needs, and this gap stems mainly from the external adaptation layer outside the agent's general capabilities, namely the harness. We therefore argue that LLM-based RCA should focus on this external harness, reusing the strong general capabilities of a modern agent rather than rebuilding an agent from scratch. A key capability of such a harness is to self-evolve, accumulating system-specific experience from past diagnoses so that it gets better the more it is used. We introduce OpsHarness, a self-evolving RCA harness that turns diagnosis experience into reusable expertise. Its data plane combines layered operational knowledge with an idea-card tool library, while its control plane coordinates setup, diagnosis, evolution, and verification. During evolution, OpsHarness contrasts successful and failed trajectories, converts their evidence into atomic proposals, and admits updates only through a dual-gate verification process designed to prevent overfitting and regression. Across two public benchmarks and an industrial deployment, OpsHarness achieves 59.0\% top-1 accuracy, improving over a bare general agent by 63.4\% and over baseline RCA agents by 4.02$\times$.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在现代微服务架构中，故障根因分析（RCA）是站点可靠性工程中极具时间压力的任务。现有方法主要分为两类：一是直接使用通用智能体（如Codex）进行诊断，二是从零构建专用RCA智能体。然而，定量研究表明，随着通用智能体能力的快速迭代，前者已普遍超越后者，但其准确率仍远未达到生产要求。论文指出，这一差距并非源于模型通用能力不足，而是外部适配层（即harness）缺乏诊断专业知识和系统特定经验，如同新入职的工程师虽具备推理能力却不熟悉目标系统。现有专用RCA智能体从零重建智能体循环、规划等通用机制，既难以超越成熟的通用框架，又无法积累跨故障的可复用经验。因此，本文的核心问题是：如何构建一个能自我进化的外部harness，复用通用智能体的强大能力，同时从历史诊断中持续提炼系统特定知识、工具和最佳实践，从而不断提升RCA准确率，实现从通用智能体到RCA专家的转变。

### Q2: 有哪些相关研究？

基于论文内容，相关研究可分为以下几类：

**方法类**：经典RCA方法依赖依赖图、因果推断或频谱分析（如MicroRCA、Sage、Eadro、BARO）。基于LLM的RCA方法则构建专用智能体，如RCAgent、RCA-Agent处理多模态遥测数据，mABC和Flow-of-Action在SOP下协调角色专用智能体，RCACopilot、Xpert等从工单和日志辅助事件管理。这些方法均从零设计专用智能体并适配单一系统，无法利用快速迭代的通用智能体，且框架固定、难以泛化到未见场景。

**智能体工程类**：CoALA定义了智能体组件，近期综述将智能体构建形式化为将能力外部化到记忆、技能和工具中。通用编码智能体（如Claude Code、Codex、OpenCode）已提供成熟的工具调用、代码执行和长程规划能力，但在特定任务上仍需外部harness层增强。开发领域已有Superpowers和OMX等外部harness，但运维领域尚属空白。

**与本文关系**：OpsHarness是首个自进化的外部RCA harness，区别于上述从零构建专用智能体的方法，它复用通用智能体的强能力，通过外部harness层实现任务适配，并具备持续自我进化能力，弥补了运维领域外部harness的缺失。

### Q3: 论文如何解决这个问题？

OpsHarness 的核心思路是**不重新构建专用 Agent，而是构建一个可自我进化的外部“线束”（Harness）**，复用通用 Agent 的强泛化能力，将诊断经验沉淀为系统专属知识。其架构分为数据面和控制面。

**数据面**是随系统演化的状态，包含两部分：
1. **分层运维知识库 K**：分为四层。K0 为通用 RCA 流程背景知识（常驻加载）；K1 为系统画像（schema、组件清单，setup 时自动生成）；K2 为挖掘出的粗粒度工作流骨架（诊断路径）；K3 为细粒度操作节点与正/负规则（如“容器 CPU 飙升会传播到前端”为正规则，“DB 会话数波动不应单独作为依据”为负规则）。K2/K3 构成有向知识图谱，采用渐进式披露，避免上下文过载。
2. **Idea-Card 工具库 T**：以自然语言描述算法思想、伪代码、输入输出契约和适用场景，而非预写死脚本。诊断时 Agent 根据实时 schema 现场编写实现代码，避免硬编码脚本因数据布局差异而失效。

**控制面**包含四个生命周期工作流：
- **Setup**：通过斜杠命令自动采样数据、识别语义列、构建实体清单，生成 K1 画像。
- **Diagnose**：自上而下执行，加载 K0/K1，按需查阅 K2/K3，跨模态交叉验证（指标确认、日志解释、链路展示影响路径），输出排序根因报告。
- **Evolve**：从轨迹中挖掘经验。对正确轨迹提取共性（高频操作提升为 K3 节点、固定代码蒸馏为工具卡、重复顺序提炼为 K2 骨架）；对错误轨迹做对比修正（定位分歧点，生成负规则或更新/删除过时知识）。
- **Verify**：双门验证。内门要求在来源案例上严格更优（准确率不降、成本不增且至少一项严格提升）；外门要求在动态维护的留出测试集上无回归。两门均通过才原子化更新，否则最多细化重试三轮。

**创新点**在于：将 RCA 能力提升从 Agent 内部转向外部线束的自我进化，通过“经验→知识→验证→沉淀”闭环，使系统越用越准，同时用双门机制防止过拟合与性能回退。

### Q4: 论文做了哪些实验？

论文在三个数据集上开展了系统实验：两个公开基准（OpenRCA含335个真实案例，覆盖电信、银行、市场三个企业系统；RCAEval含270个案例，基于Online Boutique、Sock Shop、Train Ticket三个微服务基准，注入CPU、内存、网络等故障）以及一个工业数据集（含773,340个数据点和88个确认异常）。实验采用时间顺序划分，前80%用于自进化或ICL演示检索，后20%作为测试集。

对比方法包括专用RCA智能体（RCA-Agent、mABC）和通用智能体（Codex、Claude Code的直接使用及ICL变体），并搭配四种骨干模型（GPT-5.5、Claude Sonnet 4.6、GLM-5.2、DeepSeek-V4），共24个实例组合。

主要结果：OpsHarness在最终Top-1准确率上达到66.0%（GPT-5.5骨干），相比裸通用智能体提升63.4%，相比基线RCA智能体提升4.02倍。消融实验显示，自进化机制带来显著增益（如GPT-5.5上从52.8%提升至66.0%）。工业部署验证了实际可用性，同时成本分析表明OpsHarness在推理开销上具有竞争力。

### Q5: 有什么可以进一步探索的点？

OpsHarness在自进化机制上仍有明显局限：其知识积累依赖成功与失败轨迹的对比，但对罕见故障或新故障类型的泛化能力有限，且双门验证可能过度过滤有价值但非典型的经验。未来可探索引入在线强化学习，让harness在诊断过程中动态调整策略，而非仅事后演化。此外，当前原子化提案的粒度可能丢失跨案例的关联信息，可尝试构建因果图谱来捕捉故障间的深层依赖。工业部署中，多系统间的知识迁移也是重要方向——如何将A系统的经验安全适配到B系统，需要更精细的域适应机制。最后，成本控制上，可研究分层推理策略，先用轻量模型筛选候选根因，再调用强模型深入验证，以降低对高性能后端的依赖。

### Q6: 总结一下论文的主要内容

本文提出OpsHarness，一种面向根因分析（RCA）的自进化外部代理框架。作者通过定量研究发现，通用代理（如Codex）已超越从零构建的专用RCA代理，但其准确率仍不满足生产需求，差距主要源于外部适配层（即harness）。OpsHarness的核心贡献在于：不重新构建代理，而是复用通用代理的强泛化能力，聚焦于诊断专用的外部层设计。其数据平面包含分层运维知识库和想法卡片工具库，控制平面协调设置、诊断、进化与验证四个流程。自进化机制通过对比成功与失败轨迹，提炼原子化改进提案，并经过双门验证防止过拟合与性能回退。在OpenRCA和RCAEval两个公开基准及工业部署中，OpsHarness达到59.0%的Top-1准确率，相比裸通用代理提升63.4%，相比基线RCA代理提升4.02倍，验证了自进化harness在持续积累系统经验方面的有效性。
