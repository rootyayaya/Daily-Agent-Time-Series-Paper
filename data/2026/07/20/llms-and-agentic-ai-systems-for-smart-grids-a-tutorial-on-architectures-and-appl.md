---
title: "LLMs and Agentic AI Systems for Smart Grids: A Tutorial on Architectures and Applications"
authors:
  - "Daniela Rojas"
  - "Abdulwahab Albassam"
  - "Aidan G. Leung"
  - "Jett Ngo"
  - "Ryan Luo"
  - "Peter R. Quawas"
  - "Junpyung Kim"
  - "Kangkai Liang"
  - "Mansi Nanavati"
  - "Jonathan Mai"
  - "Meng-Chi Tsai"
  - "Yun-Tong Tsai"
  - "Yize Chen"
  - "Yuanyuan Shi"
date: "2026-07-20"
arxiv_id: "2607.18147"
arxiv_url: "https://arxiv.org/abs/2607.18147"
pdf_url: "https://arxiv.org/pdf/2607.18147v1"
categories:
  - "eess.SY"
  - "cs.AI"
tags:
  - "LLM/Agent用于时间序列分析"
  - "智能电网故障诊断"
  - "工具调用与验证"
  - "可解释时间序列报告"
  - "多智能体工作流"
  - "预测性维护"
  - "时序异常检测"
  - "RAG与证据路由"
relevance_score: 8.5
---

# LLMs and Agentic AI Systems for Smart Grids: A Tutorial on Architectures and Applications

## 原始摘要

Large language models (LLMs) and agentic AI systems have evolved from natural language tasks to using external tools to plan, retrieve, and act in technical domains. In smart grids, recent work applies agentic schemes to forecasting, optimization, and control, wrapping trusted solvers behind language interfaces and orchestrating multi-step workflows. The literature lacks a unified approach to designing and evaluating such systems. LLMs can produce numerically plausible yet physically infeasible outputs, evaluation protocols vary across tasks, and the boundary between what the model should and should not compute is implicit. This paper presents a solver-grounded design principle: a numerical result is reported only when it originates from a trusted tool and passes explicit verification. We review the building blocks of LLM and agentic AI systems for power systems: prompting strategies and agentic architectures. We instantiate the principle in four case studies: wind power forecasting, EV charging scheduling, power flow analysis, and contingency diagnosis, each comparing an LLM-only baseline against its solver-grounded counterpart on identical data and metrics. EVAgent reproduces the CVXPY optimum while reducing LLM-only unmet energy by 7.5-9.5x, and GridDebugAgent repairs 17/39 contingency cases while reducing total violations by 52.3%. We propose a four-group evaluation framework spanning task utility, solver-grounded correctness, faithfulness and safe failure, and cost and latency. A consistent division of labor emerges: the agentic system reliably orchestrates, retrieves, and explains, while trusted tools compute and a verification gate decides what is reported.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决大型语言模型（LLM）和智能体AI系统在智能电网应用中缺乏统一设计与评估方法的核心问题。研究背景是LLM已从自然语言任务扩展到使用外部工具进行规划、检索和行动的技术领域，在智能电网中，已有工作将其应用于预测、优化和控制，但现有方法存在明显不足：首先，LLM可能产生数值上看似合理但物理上不可行的输出（如违反基尔霍夫定律、热极限等物理约束），且缺乏内置机制来强制执行这些物理定律；其次，不同任务的评估协议各不相同，缺乏统一标准；最后，模型应该计算什么、不应该计算什么之间的界限模糊不清。因此，本文要解决的核心问题是：如何设计一个可验证的、基于可信求解器的智能电网LLM/智能体系统，确保数值结果仅来自可信工具并通过显式验证，从而避免LLM直接生成物理上不可行的数值，并建立统一的评估框架来比较不同架构的性能。

### Q2: 有哪些相关研究？

相关研究主要分为四类。第一类是领域综述，评估LLM在电力系统任务中的能力与局限，识别出流畅文本与物理可行计算之间的差距，但缺乏构建系统以弥合这一差距的具体指导。第二类是LLM预测与时间序列建模，直接利用LLM进行负荷、风电或EV充电站占用率预测，通过提示或微调提升数据稀缺场景下的泛化性，但输出未经求解器验证。第三类是工具增强型智能体，将LLM与外部求解器、模拟器或验证器结合，如GridMind、Grid-Agent和PowerGraph-LLM，分别用于OPF、违规修复和图上下文学习，但这些系统任务特定且缺乏统一的评估协议。第四类是规划、优化与运行智能体，将LLM嵌入调度、机组组合、需求响应等闭环工作流，如将自然语言转化为求解器就绪的机组组合模型，或结合知识图谱进行可靠性监控。本文与这些工作的核心区别在于提出了“求解器接地”设计原则：数值结果必须源自可信工具并通过显式验证，LLM仅作为编排层。本文还通过四个案例（风电预测、EV调度、潮流分析和故障诊断）在统一数据和指标下对比了纯LLM基线与求解器接地系统，并提出了四组评估框架，填补了现有工作在通用正确性规则和评估协议上的空白。

### Q3: 论文如何解决这个问题？

论文提出了一种以可信求解器为核心的设计原则（solver-grounded design rule），核心思想是：LLM和智能体不应作为数值结果的来源，而应作为接口、任务规划者和编排者，围绕可信计算工具（如潮流求解器、OPF优化器、预测模型等）工作。整体框架分为三个角色：LLM负责解释请求、分解任务、选择工具和解释结果；可信工具执行数值计算；验证门（verification gate）检查输出是否物理和操作上有效。只有当数值结果来自可信工具并通过显式验证时，才被报告。

架构设计上，系统包含四个主要模块：LLM/智能体模块（负责语言交互和任务编排）、工具调用模块（调用PF、OPF等求解器）、验证模块（执行约束满足检查和忠实性检查）以及安全失败机制（当验证不通过时明确报告失败模式而非编造结果）。关键技术包括：结构化提示、少样本学习、思维链提示和检索增强生成（RAG）来改进上下文构建；以及将工具调用自然融入LLM，使其能映射自然语言请求到结构化工具输入。

创新点在于：1）提出了明确的“可信求解器”设计规则，将正确性从语言模型属性转变为整个LLM-工具-验证-智能体系统的属性；2）设计了四组评估框架（任务效用、可信求解器正确性、忠实性与安全失败、成本与延迟）；3）通过四个案例研究（风电预测、EV充电调度、潮流分析、故障诊断）验证了该方法，其中EVAgent在20个基准日实现零硬物理约束违反，GridDebugAgent修复17/39个故障案例并减少52.3%的总违规。

### Q4: 论文做了哪些实验？

论文通过四个案例研究来验证所提出的“求解器接地”设计原则。实验设置包括：将仅使用LLM的基线方法与对应的求解器接地方法在相同数据和指标上进行对比。四个案例研究覆盖了智能电网的不同任务类型：风电功率预测、电动汽车充电调度、潮流分析和应急诊断。主要结果如下：在电动汽车充电调度案例中，EVAgent（求解器接地方法）能够复现CVXPY求解器的最优解，同时将仅使用LLM方法中未满足的能源需求降低了7.5-9.5倍。在应急诊断案例中，GridDebugAgent成功修复了39个应急案例中的17个，并将总违规次数减少了52.3%。实验还提出了一个四组评估框架，涵盖任务效用、求解器接地正确性、忠实性与安全失败、以及成本与延迟。这些结果清晰地展示了求解器接地设计原则的优势：代理系统可靠地编排、检索和解释，而可信工具负责计算，验证门控决定报告什么内容。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：1) 验证门设计仍依赖人工预设规则，缺乏自适应验证机制；2) 修复策略仅支持有限重试，未探索更智能的故障恢复路径；3) 评估框架虽全面但缺乏跨任务统一基准。未来可探索：1) 将物理约束编码为可微分损失函数，实现LLM输出与求解器的端到端联合优化；2) 引入因果推理与反事实分析，增强验证门对异常工况的泛化能力；3) 构建包含多步故障注入的对抗性测试集，评估系统在极端场景下的鲁棒性；4) 开发轻量级代理模型替代部分求解器调用，在保证物理可行性前提下降低延迟；5) 探索多智能体协作中的信任分配机制，使不同代理能动态协商计算与验证职责。

### Q6: 总结一下论文的主要内容

这篇论文提出了一个面向智能电网的“求解器接地”设计原则，即仅当数值结果源自可信工具并通过显式验证时才予以报告。论文将LLM和智能体系统定位为编排层，负责解析请求、规划任务、调用工具和生成响应，而将数值计算交由可信求解器执行，并通过验证门控确保物理可行性。通过在风电预测、电动汽车充电调度、潮流分析和应急诊断四个案例中对比纯LLM基线与求解器接地系统，验证了该原则的有效性：EVAgent在复现CVXPY最优解的同时，将LLM未满足能量降低了7.5-9.5倍；GridDebugAgent修复了17/39个应急案例，总违规减少52.3%。论文还提出了一个四组评估框架（任务效用、求解器接地正确性、忠实性与安全失败、成本与延迟），揭示了纯LLM在物理约束任务中的核心缺陷。该工作为智能电网中负责任地构建和评估LLM/智能体系统提供了统一的设计原则与评估协议，弥合了语言流畅性与物理可行性之间的鸿沟。
