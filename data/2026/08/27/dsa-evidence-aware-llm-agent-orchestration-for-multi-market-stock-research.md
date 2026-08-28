---
title: "DSA: Evidence-Aware LLM-Agent Orchestration for Multi-Market Stock Research"
authors:
  - "Linsen Zhu"
  - "Yi Shi"
date: "2026-08-27"
arxiv_id: "2608.26990"
arxiv_url: "https://arxiv.org/abs/2608.26990"
pdf_url: "https://arxiv.org/pdf/2608.26990v1"
github_url: "https://github.com/ZhuLinsen/daily_stock_analysis"
categories:
  - "cs.AI"
  - "cs.MA"
tags:
  - "Agentic Time Series"
  - "LLM Agent"
  - "Stock Research"
  - "Evidence-Aware Orchestration"
  - "Multi-Agent System"
  - "Risk Control"
  - "Report Generation"
  - "Model Routing"
  - "Strategy Skills"
  - "Financial Analysis"
relevance_score: 8.5
---

# DSA: Evidence-Aware LLM-Agent Orchestration for Multi-Market Stock Research

## 原始摘要

Large language models can summarize financial information, but an operational stock-research system must first assemble heterogeneous evidence, expose unavailable data and model capabilities, and control how generated opinions affect a final report. We present DSA, an evidence-aware orchestration framework for multi-market stock research with large language model (LLM) agents. DSA organizes the workflow into evidence acquisition, structured context construction, model-routed analysis, optional role and Strategy Skill reasoning, and report generation with selected context and diagnostics. A default report profile and an optional agentic profile share evidence and model-routing services but use profile-specific output validation and risk safeguards. In the agentic profile, core role outputs are processed by role-specific parsers, whereas Strategy Skill opinions undergo an additional signal-eligibility partition before synthesis; disagreement is supplied explicitly to the decision agent, followed by a conservative risk override. The reference implementation includes six regional market paths, fifteen bundled Strategy Skills, hosted and local model routes, and multiple execution and delivery surfaces. At a frozen software snapshot, a selected manifest of 1,457 portable offline backend contract tests passed; 596 cases were retrospectively mapped to six contract families central to the reported LLM-agent architecture. This evidence establishes implementation conformance for the tested software contracts, not superior report quality, forecasting accuracy, or investment returns.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文针对多市场股票研究中，大语言模型（LLM）在生成最终报告前需要整合异构证据、暴露数据缺失和模型能力差异，并控制生成观点对报告影响的问题。现有系统往往将股票研究简化为问答任务，忽略了证据获取、上下文构建、模型路由、角色分工和风险控制等操作性问题。DSA框架旨在提供一个证据感知的编排框架，将工作流组织为证据获取、结构化上下文构建、模型路由分析、可选角色和策略技能推理、以及报告生成五个阶段。它区分默认报告配置和代理配置，共享证据和模型路由服务，但采用不同的输出验证和风险保障机制，确保系统在异构市场和模型环境下可重复运行，同时避免将不可用数据视为中性证据或让生成观点未经控制地影响最终决策。论文强调这是一个系统与工件报告，而非宣称在报告质量或投资回报上优于其他方法。

### Q2: 有哪些相关研究？

相关研究分为几类：金融语言模型和工具使用代理，如FinGPT（开放金融语言模型资源）、FinAgent（多模态市场信息、记忆和工具）、FinMem（分层记忆和角色设计）；专业化和协作式金融代理，如FinRobot（分层平台）、FinCon（经理-分析师层级）、TradingAgents（模拟交易公司角色）、AlphaAgents（基于角色的股票选择）；通用代理框架和金融评估，如ReAct（推理与行动结合）、AutoGen和AgentScope（多代理协调）、FinRL和FinRL-Meta（交易环境）、FinToolBench（工具使用评估）。DSA与这些工作的区别在于，它专注于一个操作性研究系统中市场证据、模型路由、核心代理、可选策略扩展和报告生成共存时的控制问题，并采用默认报告路径和代理路径的双配置设计，评估重点是软件契约符合性而非交易绩效。

### Q3: 论文如何解决这个问题？

DSA框架采用五阶段证据到报告的工作流：1) 证据获取：通过市场特定适配器检索报价、K线、基本面、公告、新闻和情绪，支持筛选引擎生成候选集；2) 结构化上下文构建：计算技术指标，构建有界证据块，规范化可用性和降级状态（如available、missing、fallback等），保留来源和时间戳元数据；3) 模型和能力路由：在研究工作流之下解析提供商特定请求格式和模型名称，支持托管服务、兼容端点、提供商特定路由和本地模型，能力准入按路由区分；4) 可选角色推理和受控综合：核心角色代理（技术、情报、风险、决策）通过配置编排和角色特定解析，策略技能输出额外经过信号资格分区（O_ext* = {o in O_ext : valid_signal(o)}），决策代理接收保留的角色意见、合格策略意见和显式分歧摘要，随后风险函数可能保守调整初始决策（如将买入降级为持有）；5) 报告和检查记录：两种配置都生成报告，可选持久化上下文和诊断。框架区分默认报告配置（直接验证和保障）和代理配置（角色推理、分歧处理、风险覆盖），并强调模型身份是配置而非嵌入研究逻辑。

### Q4: 论文做了哪些实验？

论文报告了冻结软件快照下的契约测试结果。在Git修订版0ca56cbee2dff5cf23b1fc59c16e2d48e61ba85c（2026年8月26日）上，使用Python 3.10.9、pytest 7.1.2和LiteLLM 1.89.3环境，执行了1,457个可移植离线后端契约测试，全部通过，耗时102.532秒。其中596个案例被回顾性映射到六个契约家族：证据上下文（74个）、模型后端/路由/配置（194个）、代理编排和路由（85个）、运行时事实/分歧/风险/保障（87个）、策略注册表/工具表面（60个）、策略归因和结果生命周期（96个）。测试验证了证据状态区分、模型和工具路由暴露不支持能力状态、核心角色排序和结构化解析、分歧进入决策综合、风险覆盖保守转换等。论文明确表示这些测试证明软件契约符合性，而非报告质量、预测准确性或投资回报。

### Q5: 有什么可以进一步探索的点？

论文指出三个未解决的核心实证问题：1) 默认报告配置和代理配置未在相同点时间股票研究任务上使用盲评或模型辅助评分进行比较；2) 角色分解、证据状态披露、策略技能、分歧处理和风险控制未通过消融研究隔离；3) 模型提供商在报告质量、延迟、令牌使用和成本上的差异未在共同协议下测量。此外，财务回报不在当前评估范围内，因为端点研究报告，需要单独的下游协议将建议转化为订单和收益。未来方向包括使用不可变点时间固定装置、共享任务、盲评、延迟和成本测量以及跨配置消融来评估报告质量，并记录下游结果以支持有界、离线的策略定义修订，如AlphaEvo方向。

### Q6: 总结一下论文的主要内容

论文提出了DSA，一个证据感知的LLM代理编排框架，用于多市场股票研究。DSA组织工作流为证据获取、结构化上下文构建、模型路由分析、可选角色和策略技能推理、以及报告生成五个阶段，提供默认报告配置和代理配置两种执行路径，共享证据和模型路由服务但采用不同的验证和风险机制。核心创新包括：将模型路由与研究逻辑分离，区分核心角色代理和可选策略技能扩展（后者有额外的信号资格分区），显式处理分歧和风险覆盖，以及保留证据状态元数据以避免不可用数据被误认为中性证据。参考实现覆盖六个区域市场、十五个策略技能、多种模型路由和交付表面。论文报告了冻结快照下1,457个契约测试全部通过，其中596个映射到六个契约家族，证明软件契约符合性，但明确不声称在分析或财务有效性上优于其他方法。
