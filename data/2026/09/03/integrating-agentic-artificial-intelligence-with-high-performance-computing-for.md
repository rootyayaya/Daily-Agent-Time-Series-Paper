---
title: "Integrating Agentic Artificial Intelligence with High-Performance Computing for Grid Planning"
authors:
  - "Samim Konjicija"
  - "Slaven Peles"
date: "2026-09-03"
arxiv_id: "2609.04544"
arxiv_url: "https://arxiv.org/abs/2609.04544"
pdf_url: "https://arxiv.org/pdf/2609.04544v1"
categories:
  - "eess.SY"
tags:
  - "Agentic AI"
  - "LLM"
  - "High-Performance Computing"
  - "Power Flow Optimization"
  - "Natural Language Reports"
  - "Autonomous Decision-Making"
  - "Interactive Steering"
  - "Concurrent Exploration"
  - "Grid Planning"
relevance_score: 7.5
---

# Integrating Agentic Artificial Intelligence with High-Performance Computing for Grid Planning

## 原始摘要

We present AgentiGrid, an agentic artificial intelligence (AI) framework that integrates large language models (LLMs) intelligence and high-performance computing (HPC) to streamline and accelerate the multi-scenario power flow studies. AgentiGrid is an autonomous decision-making agent that proposes parameter modifications, invokes analyses through HPC analysis toolkit ExaGO, interprets results, and determines subsequent actions. ExaGO provides multiple power flow applications that can perform deterministic, stochastic and security constrained optimal power flow analyses. AgentiGrid provides backends to multiple LLMs (OpenAI, Anthropic, Ollama, and Ollama cloud) augmented with context specific and task specific prompts. Key features include interactive mid-search steering, goal-type-aware post-search analysis, and concurrent variant exploration for power flow optimization. A Streamlit-based graphical launcher provides real-time visualization of iteration progress and generates reports in natural language. AgentiGrid is capable of autonomously converging transmission constrained alternating current optimal power flow in under 20 iterations, with near-perfect reliability

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

电力系统规划中，工程师常需处理难以形式化为数学优化、但易于用自然语言描述的分析任务（如“找到网络失稳的负荷水平”）。传统做法依赖专家迭代式探索——运行仿真、检查结果、调整参数、重复执行，这一过程耗时且已成为瓶颈，因为并行计算已大幅加速数值分析，人类决策反而拖慢整体效率。

现有基于LLM的电力系统智能体虽已出现，但多数仅充当顾问或按顺序执行单次仿真，存在明显不足：一是顺序式“单步单仿真”设计导致解决一个故障或场景需高额token与时间成本；二是缺乏并行执行能力，未充分利用高性能计算资源；三是缺少对多场景、多故障的并发探索与统一后处理机制。

为此，本文提出AgentiGrid框架，核心问题是如何将LLM的自主决策能力与高性能计算（HPC）的并行仿真能力深度融合，以自动化并加速多场景潮流研究。具体而言，它需解决：如何让智能体自主提出参数修改、调用ExaGO并行分析工具、解读结果并决定后续动作；如何支持交互式中途引导、目标类型感知的后搜索分析及并发变体探索；以及如何在20次迭代内可靠收敛至满足传输约束的交流最优潮流，从而突破人工迭代瓶颈，实现高效、可扩展的电网规划分析。

### Q2: 有哪些相关研究？

本文的相关研究可归为以下几类：

**方法类：LLM智能体与科学计算集成**  
如ChemCrow、Coscientist等将LLM用于实验设计与工具调用，以及针对电力系统的LLM规划框架（如LLM-OPF）。区别在于AgentiGrid不仅调用工具，还深度耦合HPC求解器（ExaGO），实现自主迭代决策、中搜索转向和并发变体探索，而非单次生成或简单工具链。

**应用类：电力系统优化与潮流分析**  
传统研究聚焦于确定性/随机OPF算法（如内点法、Benders分解），以及基于机器学习的代理模型加速潮流计算。AgentiGrid的贡献在于用Agentic AI编排这些成熟求解器，实现多场景自动参数修改、结果解释与收敛控制，将算法能力封装为可交互的智能工作流。

**评测类：LLM在工程任务中的可靠性与交互性**  
已有工作评估LLM在数学推理或代码生成上的表现，但缺乏对工程仿真闭环的评测。本文通过20次迭代内收敛至近完美可靠性、支持自然语言报告生成等指标，展示了Agent在真实物理约束下的实用性与可交互性，填补了该评测空白。

综上，AgentiGrid的核心创新在于将Agentic AI的自主决策与HPC的高保真计算无缝衔接，区别于仅用LLM做前端交互或后端调参的浅层集成。

### Q3: 论文如何解决这个问题？

AgentiGrid通过构建一个三层架构的智能体框架，将LLM的决策能力与HPC的数值计算能力深度耦合，以解决多场景潮流规划中人工迭代效率低下的问题。

整体框架分为三层：**Agent Loop Controller**（智能体循环控制器）负责管理迭代流程，组装包含系统提示、网络元数据、目标陈述、搜索日志、最新结果、操作指令和错误反馈等最多七个部分的动态提示词，并解析LLM返回的JSON格式命令；**Analysis Orchestrator**（分析编排器）作为中间层，负责验证并应用修改命令到Matpower格式的电网文件副本，调用ExaGO的HPC仿真程序（如PFLOW、OPFLOW、SCOPFLOW等），解析输出并检查约束违规；**ExaGO Applications**作为底层HPC引擎执行确定性、随机性和安全约束最优潮流分析。

关键技术包括：**并发变体探索**机制，通过引入explore和select两种新动作，让LLM单次迭代生成2-8个独立变体方案，利用ThreadPoolExecutor并行仿真，再通过Pareto前沿分析筛选最优解，从而将LLM推理延迟（20-30秒）分摊到多个仿真任务上，显著提升效率；**目标类型感知的后搜索分析**，通过最终LLM调用将搜索目标分类为成本最小化、可行性边界、约束满足或参数探索四种类型，避免朴素“最低成本”启发式在边界搜索场景下的误判；**交互式中途引导**功能，支持用户通过线程安全队列在运行中注入augment或replace模式的指令，实时调整搜索方向。

创新点在于将LLM作为优化器而非单纯的自然语言接口，结合HPC的精确物理仿真，实现了自主收敛的输电约束交流最优潮流计算，通常在20次迭代内即可达到接近完美的可靠性，并支持多LLM后端（OpenAI、Anthropic、Ollama等）和Streamlit图形化实时监控。

### Q4: 论文做了哪些实验？

实验在ACTIVSg200合成200节点电网（伊利诺伊区域输电系统）上进行，包含246条支路、200个负荷和49台发电机。硬件为Intel Core i7-13650HX（14核）和32GB内存。研究设计了三个目标任务：经济调度优化（pflow）、N-1安全约束分析（SCOPFLOW）和风电随机场景评估（SOPFLOW），对比了四个LLM后端：Claude Sonnet 4.6、GPT-5.4、GLM-5.1和DeepSeek-V4-Pro，所有任务迭代预算20次，温度0.3。

主要结果：在pflow任务中，Sonnet和GPT正确识别基准已最优（$27,564），而GLM和DeepSeek通过机组组合分别降低成本36.9%（$17,398）和34.9%（$17,941）。SCOPFLOW任务中，所有模型均识别出187→189线路为最关键N-1故障（成本增加21.6%），但仅Sonnet未能发现29→30线路的不可行性，且所有模型遗漏了15→16线路。SOPFLOW任务中，所有代理仅用3次迭代即完成，均识别出152号母线最敏感，GPT和GLM额外识别出15个敏感母线。

结果显示GPT-5.4迭代最多但最准确，Sonnet迭代最少但遗漏关键故障，DeepSeek最严谨但消耗最高，GLM最经济高效。主要局限包括对不可行性检测不足和提示词顺序影响优先级判断。

### Q5: 有什么可以进一步探索的点？

论文当前局限于200节点系统，首要局限是扩展性未知。未来应系统评估随系统规模增大（如数千节点）时，迭代次数、求解时间及token消耗的变化趋势，并验证框架在更大、更复杂电网中的鲁棒性。其次，当前基于文件的数据存储会成为性能瓶颈，需引入数据库以优化日志管理与数据检索，支撑大规模并发探索。此外，RAG（检索增强生成）能力尚浅，可扩展知识库以提升LLM对电网物理约束和案例经验的理解，减少无效探索。从方法看，“LLM作为优化器”虽可行，但缺乏对决策可解释性的量化分析，未来可结合可解释AI技术追踪每次参数修改的因果逻辑。我建议引入混合决策机制，即LLM负责全局策略与异常诊断，而将数值优化子问题交由传统求解器，以提升收敛保证。同时，可探索多智能体协作模式，让不同LLM实例分别负责场景生成、约束校验与结果审计，增强任务分解效率。最后，当前交互式引导依赖人工介入，未来可研究自动识别收敛停滞并动态调整提示策略的自适应机制，减少人工监督成本。

### Q6: 总结一下论文的主要内容

AgentiGrid是一个将大语言模型智能与高性能计算相结合的智能体框架，旨在加速电力系统多场景潮流分析。该框架采用三层架构，包括智能体循环控制器、分析协调器和ExaGO高性能计算应用层，支持六种潮流及最优潮流分析。

方法上，AgentiGrid利用LLM作为优化引擎，通过迭代方式自主提出参数修改、调用仿真分析、解释结果并决定后续行动。其创新点包括并发变体探索机制、交互式中途引导、目标类型感知的后搜索分析，以及基于Streamlit的可视化界面。

在ACTIVSg200电网上的实验表明，该框架能在20次迭代内自主收敛，四种LLM后端均能可靠完成确定性、安全约束和随机最优潮流分析任务。研究验证了“LLM作为优化器”范式在难以形式化的电力系统分析任务中的实际可行性，为智能体AI与并行计算在电网规划中的结合提供了有效方案。
