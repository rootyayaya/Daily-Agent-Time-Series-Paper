---
title: "Large Language Models in Process Systems Engineering: Opportunities, Architectures, and Industrial Deployment Challenges"
authors:
  - "Bhushan Gopaluni"
  - "Vidya Kotamraju"
  - "Syon Bhushan"
date: "2026-06-10"
arxiv_id: "2606.11589"
arxiv_url: "https://arxiv.org/abs/2606.11589"
pdf_url: "https://arxiv.org/pdf/2606.11589v1"
categories:
  - "eess.SY"
tags:
  - "LLM"
  - "Process Systems Engineering"
  - "time-series forecasting"
  - "fault detection and diagnosis"
  - "survey"
  - "industrial deployment"
relevance_score: 7.5
---

# Large Language Models in Process Systems Engineering: Opportunities, Architectures, and Industrial Deployment Challenges

## 原始摘要

Large Language Models (LLMs) have rapidly emerged as tools of interest across engineering disciplines, and Process Systems Engineering (PSE) is no exception. This survey provides a systematic review of LLM applications in PSE, organizing the literature into seven categories: (1) process design and engineering, (2) molecular design and synthesis, (3) process modeling and simulation, (4) time-series forecasting, (5) optimization and scheduling, (6) process control, and (7) fault detection and diagnosis. For each category, we summarize the state of the art, identify common methodological approaches, and critically assess demonstrated capabilities versus aspirational claims. We find that LLMs show genuine promise for tasks involving natural language, including querying documentation, synthesizing unstructured knowledge, and enabling flexible human-machine interaction. However, applications requiring real-time execution, constraint satisfaction, or formal safety guarantees remain challenging. We conclude by identifying open problems and productive research directions for the PSE community.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

过程系统工程（PSE）领域长期面临数据丰富但洞察匮乏的困境：现代工厂虽能生成海量传感器与事件数据，但操作员难以将实时数据、维护记录、操作手册等分散在文档、数据库和机构记忆中的信息有效整合。传统方法如基于规则的专家系统、统计过程监控和模型预测控制（MPC）虽在各自功能上表现优异，却各自为政——MPC优化设定点却无法解释推理过程，故障检测系统标记异常却无法关联维护日志中的历史事件，过程历史数据库存储多年数据却需专业查询才能提取信息。分布式控制系统（DCS）、SCADA和制造执行系统（MES）各自承担重要功能却鲜有信息共享。本文旨在系统性地综述大语言模型（LLM）在PSE中的应用，核心解决如何利用LLM的自然语言处理、上下文学习及工具调用能力，构建一个能够桥接这些信息孤岛的认知层——作为操作员与工程系统之间的自然语言接口，以及协调知识系统、仿真工具和数值优化方法的推理层，而非替代经过验证的经典控制方法。

### Q2: 有哪些相关研究？

相关研究主要围绕大语言模型（LLM）在过程系统工程（PSE）中的应用展开，本文将其分为七类：过程设计与工程、分子设计与合成、过程建模与仿真、时间序列预测、优化与调度、过程控制以及故障检测与诊断。在方法层面，现有工作多基于Transformer架构，利用自注意力机制处理序列数据，并采用GPT-style的因果注意力实现自回归生成。本文与这些工作的关系在于，它系统性地综述了LLM在PSE各领域的应用现状，并批判性地评估了实际能力与宣称潜力之间的差距。区别在于，本文不仅总结了现有方法（如ReAct工具增强代理、检索增强生成RAG、思维链提示等），还深入分析了LLM的固有局限（如幻觉、延迟、缺乏形式化保证、不透明性及训练数据依赖），并指出这些局限应指导系统设计，而非回避应用。在应用类研究中，LLM在自然语言处理任务（如文档查询、知识综合、人机交互）中展现出真实潜力，但在实时执行、约束满足或安全保证方面仍面临挑战。本文还识别了开放问题，为PSE社区指明了研究方向，强调LLM应作为推理引擎或解释器，与传统方法协同工作。

### Q3: 论文如何解决这个问题？

论文通过系统性地梳理大语言模型（LLM）在过程系统工程（PSE）七个核心领域的应用，提出了一种“分层协同”的架构范式。核心方法并非让LLM直接替代传统数值计算或控制算法，而是将其定位为“语言驱动的智能编排层”，与领域专用工具（如模拟器、优化器、控制器）形成混合架构。

**整体框架**上，论文将LLM的应用分为三个层次：1) **表示与交互层**：利用文本化流程表示（如eSFILES、知识图谱）和自然语言接口，实现工程师与复杂PSE工具的直观交互（如查询P&ID、生成流程图）。2) **推理与编排层**：LLM作为“大脑”，负责理解自然语言指令、分解任务、调用外部工具（如Aspen Plus模拟器、优化求解器）并综合结果。例如，在过程设计中，LLM通过“规划-执行”Agent工作流，将自然语言描述逐步转化为可执行的仿真或设计步骤。3) **验证与执行层**：所有LLM生成的建议（如控制设定点、故障恢复序列）必须经过专用工具的验证（如仿真器验证可行性、MPC控制器执行约束优化）或人工专家审核，确保安全性与可靠性。

**关键技术**包括：1) **文本化流程表示**：如eSFILES和SFILES，将拓扑结构、参数等编码为文本序列，使Transformer模型可处理。2) **检索增强生成（RAG）**：将LLM与知识图谱、历史数据库（如DEXPI标准）结合，减少幻觉，提升回答的工程准确性。3) **重编程（Reprogramming）**：如Time-LLM，将时间序列数据映射到冻结语言模型的嵌入空间，利用其预训练的序列模式知识进行零样本预测。4) **多Agent系统**：如用于故障诊断的Argos或过程优化的多Agent框架，不同Agent分别负责约束提取、参数验证、仿真执行等，协同完成复杂任务。

**创新点**在于明确指出LLM在PSE中的真实价值边界：其优势在于处理非结构化语言、解释异常、协调多步恢复和整合跨域信息（如将传感器异常与维修日志关联），而非直接进行实时控制或数值求解。论文提出的“LLM提议-专用工具验证-人类监督”的混合架构，为工业部署提供了务实且安全的路径。

### Q4: 论文做了哪些实验？

论文围绕大语言模型（LLMs）在过程系统工程（PSE）中的应用，在七个方向进行了实验评估。实验设置涵盖从合成数据预训练到工业案例验证，主要数据集包括SFILES、Simona（约1000条过程描述）、LOTSA（270亿观测值）等。对比方法包括传统机器学习模型（如PCA、ARIMA）、专用时间序列模型（如PatchTST、iTransformer）以及经典控制方法（PID、MPC）。主要结果：在过程设计方面，控制结构预测达到74.8-89.2%的top-5准确率；HAZOP分析中F1>86%，但仅19-37%的场景语义有效。分子设计方面，微调GPT-3可匹配或超越专用模型。时间序列预测中，LLMTime零样本性能与专用模型相当，Time-LLM在标准基准上达到SOTA。故障诊断中，知识图谱增强的LLM达到98.5%准确率。过程控制中，LLM代理在实验室温度控制上表现与PID相当，但延迟为500-5000ms，远高于PID的微秒级。优化方面，多代理框架在氢脱烷基案例中显著降低计算成本。总体而言，LLMs在语言密集型任务（如查询、解释）中表现突出，但在实时执行、约束满足和安全保障方面仍存在挑战。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：LLM在实时执行、约束满足和安全保证方面能力不足，且存在幻觉、延迟和缺乏形式化验证等问题。未来可探索的方向包括：1) 开发混合架构，将LLM作为监督推理层，与传统MPC、PID等控制器协同工作，LLM负责自然语言交互和知识综合，而传统方法负责实时控制和约束保证；2) 研究更可靠的检索增强生成（RAG）技术，结合领域知识图谱和数字孪生，减少幻觉并提升故障诊断的可解释性；3) 探索轻量化LLM的本地部署，结合模型压缩和硬件加速，降低延迟以满足部分工业实时需求；4) 构建可验证的LLM工作流，通过仿真环境预验证LLM建议的动作，再执行于实际过程，从而在保持灵活性的同时引入安全护栏。

### Q6: 总结一下论文的主要内容

这篇综述系统性地探讨了大语言模型（LLM）在过程系统工程（PSE）中的应用。其核心贡献在于，它并非简单罗列应用，而是提出了一个关键论点：LLM 的最佳定位是作为“监督层”或“认知接口”，而非替代经典控制方法。论文将现有文献分为七个领域（过程设计、分子设计、建模与仿真、时间序列预测、优化调度、过程控制、故障诊断），并逐一评估了其真实能力与夸大之词。主要结论是：LLM 在处理自然语言、综合非结构化知识（如操作手册、日志）以及实现灵活的人机交互方面展现了巨大潜力；然而，在需要实时执行、严格约束保证或安全认证的任务（如实时控制、数值优化）中，LLM 表现不佳，无法取代经过验证的数值方法。该研究为 PSE 社区指明了富有成效的研究方向，即利用 LLM 作为协调器，桥接数据孤岛，增强而非取代现有的工程系统。
