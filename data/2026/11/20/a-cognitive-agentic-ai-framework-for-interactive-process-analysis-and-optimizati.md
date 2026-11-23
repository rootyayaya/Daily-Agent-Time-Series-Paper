---
title: "A Cognitive Agentic AI Framework for Interactive Process Analysis and Optimization"
authors:
  - "Trung Ngoc Trinha"
  - "Roman Tschentscher"
  - "Trong Dong Nguyen"
  - "Trung Thanh Nguyen"
  - "Anna Trubetskaya"
date: "2026-11-20"
arxiv_id: "2611.27725"
arxiv_url: "https://arxiv.org/abs/2611.27725"
pdf_url: "https://arxiv.org/pdf/2611.27725v1"
categories:
  - "cs.MA"
tags:
  - "Agentic AI"
  - "LLM Agent"
  - "Process Optimization"
  - "Bayesian Optimization"
  - "Surrogate Modeling"
  - "Human-in-the-Loop"
  - "Multi-Agent System"
  - "Industrial Fault Diagnosis"
  - "Time Series Analysis"
  - "RAG"
relevance_score: 7.5
---

# A Cognitive Agentic AI Framework for Interactive Process Analysis and Optimization

## 原始摘要

Complex multivariable process analysis and optimization require coordinated access to simulation, structured data, machine learning (ML), optimization, and scientific literature, often across disconnected software tools. We present a Cognitive Agentic AI Framework (CAAF) that enables interactive, iterative process investigation through natural-language prompts within an established flowsheet. Following harness-engineering principles, CAAF assigns task interpretation, planning, knowledge synthesis, and context management to a large language model while delegating numerical calculations to specialized tools. Dedicated providers connect databases, scientific-document retrieval, ML-assisted Bayesian optimization (BO), and COCO process simulation. The framework is demonstrated on methyl acetate production. Guided by successive prompts, an engineer explored multivariable relationships, conducted 4,000 BO iterations to maximize carbon conversion yield (C-Yield) and minimize specific energy cost (C-SEC), refined operating bounds, and verified selected candidates through process simulation. Re-simulation of 16 candidates within the restricted domain showed close agreement with ML predictions, with a mean absolute C-Yield error of 0.0085 (0.85 percentage points). The highest BO-derived C-Yield, verified by COCO, was 0.921 versus approximately 0.81 in the initial dataset, an improvement of about 11 percentage points. CAAF also detects and reports non-converged simulations, excludes invalid outputs, and continues subsequent evaluations. The results demonstrate how human-guided agentic coordination can combine engineering tools for iterative analysis and optimization with rigorous simulation-based verification under a fixed process topology.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文旨在解决复杂多变量工业过程分析与优化中，工程师需要协调使用流程模拟、结构化数据、机器学习模型、优化算法和科学文献等多种异构工具的问题。这些工具通常分散在不同的软件环境中，导致即使对于领域专家，进行高级计算分析也面临技术门槛高、效率低下的挑战。具体而言，传统方法要求工程师具备数据分析、流程模拟、机器学习和编程等多学科技能，这限制了先进计算方法的可及性和效率。此外，虽然大语言模型（LLM）驱动的智能体AI有望通过自然语言交互连接工程知识与计算资源，但过度依赖LLM进行任务抽象、规划和协调可能增加幻觉、决策不一致和工具执行错误的风险，在流程工程中尤为关键，因为数值结果和工程结论必须与物理原理和过程约束保持一致。因此，论文提出一个认知智能体AI框架（CAAF），旨在通过自然语言提示实现交互式、迭代的过程调查，同时将LLM的认知推理与专业工程工具的数值计算分离，确保结果的可追溯性和可靠性，并在固定流程拓扑下支持从多变量分析、优化到基于模拟验证的完整工作流。

### Q2: 有哪些相关研究？

相关研究主要包括以下几个方面：首先，在流程模拟与机器学习结合方面，已有研究将严格流程模拟与ML代理模型和贝叶斯优化（BO）集成，用于全局流程优化和多目标优化，例如基于代理的贝叶斯优化和Aspen HYSYS与人工神经网络集成的过程优化。其次，在LLM与流程工程交互方面，近期研究展示了基于LLM与AVEVA Process Simulation和Aspen Plus的交互，以及用于解释过程控制策略的多智能体方法。更广泛的应用如ChemCrow和Coscientist展示了LLM与科学工具和计算工作流的集成。此外，综述文章强调了基于LLM的多智能体系统在化学工程中协调专业智能体、集成异构工程数据和计算工具、支持复杂工程工作流的潜力，同时指出了可靠性、透明度和系统集成方面的挑战。在可靠性提升方面，harness engineering原则通过建立结构化执行环境（集成智能体编排、受控工具接口、领域知识、记忆和验证机制）来提高LLM智能体的可靠性。最后，人在回路（HITL）范式确保工程专业知识在AI辅助调查中保持核心地位，而非被替代。本文的CAAF框架正是在这些研究基础上，将智能体AI、过程分析、ML辅助贝叶斯优化和基于模拟的验证集成到一个统一的交互式工程框架中。

### Q3: 论文如何解决这个问题？

论文提出认知智能体AI框架（CAAF），其核心架构基于harness engineering原则，将LLM驱动的任务解释、规划、知识合成和上下文管理与数值计算分离。框架包含主智能体、功能智能体、提供者与领域工具、知识合成组件、验证与记忆模块以及知识引导层。主智能体协调调查，解释用户目标并确定所需分析；四个功能智能体（SQL智能体、模拟智能体、优化智能体和RAG摘要智能体）分别将任务转换为对相应提供者的结构化请求。提供者连接SQLite数据库、文档检索管道、基于Python的优化平台和通过Python访问的流程模拟模型（COCO）。知识合成组件（数据分析师智能体、可视化智能体和合成器智能体）将异构工具输出转化为工程解释。验证模块评估任务执行与原始请求的一致性，并利用知识引导层和记忆中的上下文信息。故障处理机制监控模拟执行状态，报告不收敛或执行错误，排除无效输出并继续后续评估。知识引导层提供数据库模式、过程术语、参数关系等上下文，帮助将领域问题转化为可分配的任务。整个框架通过LangGraph编排，使用Gemma 4-31B模型，支持多轮交互和人在回路，工程师通过自然语言提示定义目标、审查中间证据并指导后续分析。

### Q4: 论文做了哪些实验？

论文通过一个甲基乙酸酯（MeAce）生产过程案例研究来演示CAAF。实验设置包括：一个基于COCO的稳态流程模拟模型，两个结构化数据集（约3906个场景案例和2730个DOE案例，共6636个模拟案例，超过216列），一个基于Python的贝叶斯优化平台（支持单目标和多目标优化），以及约121页的PDF文档库用于RAG。实验通过9个连续提示进行交互式调查：首先分析操作参数对C-Yield和C-SEC的影响（结合文献和SQL数据集），生成相关热图和散点图；然后分析长期试点测试数据的时间序列；接着进行4000次迭代的多目标贝叶斯优化以最大化C-Yield和最小化C-SEC；基于工程判断限制压力、反应器长度和分流因子范围后，再次进行4000次迭代优化；最后选择16个候选解用COCO模拟验证。主要结果：在限制域内，16个候选的模拟再评估与ML预测的平均绝对C-Yield误差为0.0085（0.85个百分点）；BO得到的最高C-Yield为0.921，而初始数据集最大值约0.81，提升约11个百分点；框架成功检测并报告不收敛模拟，排除无效输出并继续评估。此外，相关性分析显示反应器温度与C-Yield强正相关（r=0.59），与C-SEC负相关（r=-0.38），压缩机压力与C-SEC正相关（r=0.32）。

### Q5: 有什么可以进一步探索的点？

论文的局限性及未来方向包括：首先，当前案例研究仅涉及单一流程拓扑和特定过程（甲基乙酸酯生产），未来可将框架推广到其他工业过程和多变拓扑场景。其次，验证模块主要关注工作流层面的一致性，未来可增强对LLM推理链的细粒度验证和自动纠错能力。第三，实验仅使用了9个提示和有限的人工交互，未来可探索更复杂的多轮对话、主动学习和自动化假设生成。第四，RAG组件依赖有限的文档库（121页），可扩展至更大规模、多模态的工程知识源。第五，当前优化依赖预训练的代理模型，未来可研究在线学习或自适应代理模型更新机制。第六，故障处理机制仅报告不收敛，未来可集成根因分析和自动调整策略。第七，可探索多智能体协作的更深层次，如智能体间的辩论或竞争性验证以提高可靠性。最后，可开展更系统的用户研究，评估框架对工程师决策效率和质量的实际影响。

### Q6: 总结一下论文的主要内容

本文提出了一个认知智能体AI框架（CAAF），用于在固定流程拓扑下通过自然语言提示进行交互式过程分析与优化。CAAF基于harness engineering原则，将LLM驱动的认知推理（任务解释、规划、知识合成、上下文管理）与专业工程工具的数值计算分离，通过主智能体、功能智能体（SQL、模拟、优化、RAG摘要）、提供者、知识合成、验证与记忆模块以及知识引导层实现协调。框架在甲基乙酸酯生产过程案例中进行了演示，通过9个连续提示完成了从多变量分析、文献检索、时间序列可视化、4000次迭代多目标贝叶斯优化、基于工程判断的搜索域细化到COCO模拟验证的完整工作流。实验结果表明，在限制域内16个候选的模拟验证与ML预测平均绝对误差为0.0085，最高C-Yield从初始约0.81提升至0.921（约11个百分点），且框架能有效处理不收敛模拟。该工作展示了人在回路的智能体协调如何整合互补工程资源，支持迭代过程分析与优化，并将基于代理的优化与严格的模拟验证相结合，为工业过程工程提供了一种可追溯、可靠的AI辅助工作流。
