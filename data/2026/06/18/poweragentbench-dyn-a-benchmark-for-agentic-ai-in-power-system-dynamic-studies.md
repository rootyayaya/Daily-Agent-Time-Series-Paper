---
title: "PowerAgentBench-Dyn: A Benchmark for Agentic AI in Power System Dynamic Studies"
authors:
  - "Qian Zhang"
  - "Andrea Pomarico"
  - "Costas Mylonas"
  - "Magda Foti"
  - "Alberto Berizzi"
  - "Le Xie"
date: "2026-06-18"
arxiv_id: "2606.20401"
arxiv_url: "https://arxiv.org/abs/2606.20401"
pdf_url: "https://arxiv.org/pdf/2606.20401v1"
categories:
  - "eess.SY"
tags:
  - "Agentic AI"
  - "LLM Agent"
  - "电力系统动态分析"
  - "基准测试"
  - "工具调用"
  - "语义记忆"
  - "迭代实验"
  - "工程推理"
relevance_score: 6.5
---

# PowerAgentBench-Dyn: A Benchmark for Agentic AI in Power System Dynamic Studies

## 原始摘要

Large Language Model (LLM)-based agents are increasingly being used to automate multi-step engineering work flows by interacting with software tools, interpreting intermediate results, and autonomously planning subsequent actions. Power system dynamic studies represent a particularly promising yet largely unexplored application domain for these agents. Unlike static computational tasks, dynamic studies often require more time on model parameter calibration, engineering judgment, and decision making under constrained action spaces. This paper introduces PowerAgentBench-Dyn, a benchmark designed to evaluate Agentic AI systems on power system dynamic-analysis tasks. The benchmark targets problems that cannot be reduced to a single optimization or coding task, but instead require a type of reasoning, tool usage, and iterative experimentation routinely performed by experienced power system engineers. The proposed framework includes two initial benchmark tasks. The first, the Dynamic Model Quality Review Benchmark, evaluates agents' ability to validate and diagnose dynamic models based on model-quality compliance criteria specified by system operators. The second, the Dynamic Security Risk Screening Benchmark, assesses agents' capability to leverage semantic memory and a limited simulation budget to identify, rank, and analyze the most critical short-circuit contingencies from an unseen fault dataset, as well as propose and evaluate possible mitigation measures. For each task, we define the simulation environment, observation and action spaces, and evaluation metrics. The benchmark is reproducible in a metric-based sense: released cases and simulator settings define a deterministic evaluator, while stochastic agent behavior is assessed over repeated runs using success rates and other metrics. The benchmark supports the development of future Agentic AI for power system operation and planning.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着逆变器资源、储能和数据中心等新型设备接入，电网动态特性日益复杂，近期扰动事件凸显了动态模型质量验证和故障复现等流程的迫切需求。尽管大语言模型（LLM）智能体在稳态分析中展现了自动化多步工作流的潜力，但现有AI方法在动态研究领域仍存在明显不足：传统方法主要依赖监督学习进行暂态稳定评估或故障分类，这些方法在固定数据分布和明确标签下有效，却无法应对日常工程中开放、受约束的决策任务，例如模型参数校准、工程判断以及有限仿真预算下的风险排序。现有工作流瓶颈不在于单一公式求解，而在于一系列需要反复迭代的决策序列，如准备案例、选择扰动、诊断仿真失败、解释图表、在允许范围内调整参数等。因此，本文提出PowerAgentBench-Dyn基准，旨在解决智能体在电力系统动态研究中难以通过确定性脚本或单次优化完成的多轮交互任务，核心挑战在于如何评估智能体在受限动作空间内结合工具使用、语义记忆和工程判断进行迭代实验的能力。

### Q2: 有哪些相关研究？

PowerAgentBench-Dyn的相关研究主要分为三类：

**1. 方法类：LLM Agent 在工程领域的应用**
相关工作包括基于LLM的自动化工作流框架（如AutoGPT、MetaGPT）以及针对特定工程领域的Agent系统（如用于科学计算的ChemCrow、用于软件工程的SWE-bench）。本文与这些工作的区别在于：PowerAgentBench-Dyn专门针对电力系统动态研究这一复杂工程领域，其任务无法简化为单一优化或编码问题，而是需要多轮迭代推理、工具交互和工程判断，且动作空间受严格约束。

**2. 应用类：电力系统AI与自动化**
现有工作包括基于机器学习的动态安全评估（如DSA）、模型参数校准（如PMU数据驱动的参数辨识）以及故障筛选方法（如基于灵敏度的排序）。本文的创新在于：不依赖静态特征向量分类，而是要求Agent像经验丰富的工程师一样，通过交互式仿真、波形分析和迭代实验来完成模型质量审查和安全风险筛查，同时遵循电网运营商制定的合规标准。

**3. 评测类：Agent基准测试**
相关工作包括AgentBench（通用Agent评测）、WebArena（网页交互评测）以及SciBench（科学计算评测）。本文的独特贡献在于：提出了首个针对电力系统动态研究的Agent基准，定义了包含观测空间、约束动作空间、仿真环境、用户约束和隐藏真实值的交互式任务框架（T = (O, A, E, C, G, M)），并采用成功率、诊断准确率、波形拟合度等结果导向指标进行可重复评估。

### Q3: 论文如何解决这个问题？

该论文通过构建一个交互式基准测试框架来解决电力系统动态研究中智能体评估的难题。核心方法是将每个基准任务形式化为一个交互环境 \(\mathcal{T} = (\mathcal{O}, \mathcal{A}, \mathcal{E}, \mathcal{C}, \mathcal{G}, \mathcal{M})\)，其中包含观察空间、约束动作空间、仿真环境、工程约束、隐藏真值评估器和可选的语义记忆。

整体框架基于四个设计原则：工具接地评估（智能体必须与真实仿真器和分析工具交互）、多轮决策（任务需要多步推理而非单次响应）、工程约束护栏（动作必须遵守预设的参数范围、预算和文件锁定）以及结果导向指标（通过诊断准确率、波形拟合度、排序质量等可靠性指标衡量成功）。

主要模块包括两个基准任务：动态模型质量审查基准，评估智能体根据系统运营商制定的模型质量合规标准验证和诊断动态模型的能力；动态安全风险筛选基准，评估智能体利用语义记忆和有限仿真预算，从未见故障数据中识别、排序和分析最关键的短路故障，并提出缓解措施。每个任务都定义了仿真环境、观察空间、约束动作空间和评估指标。

关键技术在于约束动作空间的设计，通过机器可读的约束文件指定允许的参数、事件修改、最大仿真次数和时间预算，确保智能体行为符合工程实际。基准通过确定性评估器（固定案例和仿真器设置）和随机智能体行为的重复运行（成功率等指标）实现可重复性。创新点在于将电力系统动态研究中需要工程判断、参数校准和迭代实验的复杂任务转化为可量化的基准测试，支持未来智能体在电力系统运行和规划中的应用。

### Q4: 论文做了哪些实验？

论文设计了两个基准实验任务。第一个是动态模型质量审查基准（DMQ Benchmark），实验设置中，智能体需使用DMView和PSS/E动态仿真工具，在5次迭代预算内仅允许修改REECAU1模型的4个增益参数（Kqp, Kqi, Kvp, Kvi）。输入包括修改后的WECC太阳能光伏模型（初始增益(10,50,10,50)导致所有8项测试失败）。对比了Anthropic的Opus 4.8、Sonnet 4.6和Haiku 4.5三个模型，每个运行10次。主要结果：Opus 4.8和Sonnet 4.6均以10/10成功率修复模型，中位迭代次数为1；Haiku 4.5成功率为9/10，中位迭代次数为2。关键指标包括全套测试通过率、波形拟合、LVRT恢复和约束合规性。

第二个是动态安全风险筛查基准（DSR Benchmark），智能体需通过PowerMCP和DIgSILENT PowerFactory，在有限仿真预算内从10个未见过故障中识别并排序最关键的三个故障，并评估缓解措施。输入包括语义记忆和故障数据集。对比了Opus 4.7、Sonnet 4.6、Haiku 4.5、Gemini 3.1 Pro、GPT-5.5和Qwen2.5-Coder-7B。主要结果：Gemini 3.1 Pro和GPT-5.5成功率100%，Opus 4.7和Sonnet 4.6为90%，Haiku 4.5为70%，Qwen7B为0%。关键指标包括Top-3故障识别（L02-25@160ms, L05-06@200ms, B05@180ms）、严重度评分、电压极值、缓解成功率（如SC26是稳定L02-25故障的必要条件）和运行时间（GPT-5.5最快，中位5分43秒）。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在对实际工程复杂性的简化，包括数据保密性、保护模型保真度、电磁暂态/机电暂态模型一致性以及运营商特定标准等关键问题未被充分覆盖。未来可探索的方向包括：扩展动态模型家族（如新能源逆变器模型）、增加电磁暂态案例、引入振荡源定位和PMU数据事件回放等更贴近实际的任务。另一个重要方向是引入人机协同评估机制，在关键决策点设置审批关卡，要求Agent提供证据和不确定性量化，模拟工程师的审核流程。此外，当前基准的随机性评估仅依赖重复运行的成功率，未来可结合更细粒度的推理路径分析，例如通过可解释性工具追踪Agent的决策逻辑，或引入强化学习中的奖励塑形来优化其迭代实验策略。这些改进将推动Agent从“任务执行”向“工程判断”的跨越。

### Q6: 总结一下论文的主要内容

这篇论文提出了PowerAgentBench-Dyn，一个用于评估基于大语言模型（LLM）的智能体在电力系统动态研究中表现的新型基准。核心贡献在于，它针对那些无法简化为单一优化或编码任务、而需要类似经验丰富的工程师进行推理、工具使用和迭代实验的复杂工程问题，定义了标准化的评估框架。方法上，基准包含两个初始任务：动态模型质量审查基准，评估智能体验证和诊断动态模型的能力；动态安全风险筛选基准，评估其利用语义记忆和有限仿真预算，从未知故障数据集中识别、排序关键短路故障并提出缓解措施的能力。主要结论是，该基准通过定义仿真环境、观察与行动空间及可重复的评估指标，为开发未来能够与动态仿真工具交互、支持电力系统运行与规划的智能体AI提供了坚实基础。
