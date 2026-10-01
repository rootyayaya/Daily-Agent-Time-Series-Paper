---
title: "Skill-Based AI Agents for Power-System Studies"
authors:
  - "Pavel Etingov"
  - "Shuchismita Biswas"
date: "2026-09-30"
arxiv_id: "2609.40272"
arxiv_url: "https://arxiv.org/abs/2609.40272"
pdf_url: "https://arxiv.org/pdf/2609.40272v1"
categories:
  - "eess.SY"
tags:
  - "Agentic AI"
  - "MCP"
  - "Skill-based Agents"
  - "Power System Studies"
  - "Dynamic Simulation"
  - "Model Validation"
  - "Multi-Agent Orchestration"
  - "Industrial Fault Diagnosis"
relevance_score: 8.5
---

# Skill-Based AI Agents for Power-System Studies

## 原始摘要

This paper describes a skill-based agentic framework for power-system studies using Model Context Protocol (MCP)-connected engineering tools. A custom MCP server was developed to expose Siemens PTI PSSE functions for power-flow analysis, dynamic simulation, result extraction, and model-validation workflows. Two implementation pathways built on a programmable OpenAI Agents software development kit (SDK) and a Claude Code command-line interface (CLI) were evaluated, both using reusable skills, subagents, MCP tools, data-repository connections, and local shell/Python execution. Both frontier-model-based implementations successfully executed representative study tasks. Success was evaluated based on task completion, output accuracy, and the need for human expert interventions. Results based on public datasets show that agentic systems can greatly accelerate power system dynamic simulation process for transmission planning studies leveraging industry-grade simulation platforms. This points toward a shift in transmission planning practice, where agentic systems could handle routine simulation setup and result extraction, allowing engineers to focus expert judgment on scenario design and interpretation rather than tool operation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文针对电力系统规划与运行支持研究中端到端工作流高度手动化、工具专用且依赖专家知识的问题，提出了一种基于技能（skill）的智能体框架。典型电力系统研究涉及大量耗时任务，包括为多场景准备潮流案例、评估稳态与稳定性、配置动态仿真输入、选择故障或扰动、评估敏感性案例、提取与分析仿真结果以及撰写工程报告。尽管已有成熟的商业和开源工具支持其中许多步骤，但整个流程仍然需要人工操作、依赖特定工具且高度依赖专家经验，导致可扩展性差、决策支持不及时，并消耗大量人力资源。随着电网运行日益复杂，需要评估的运行条件、场景和不确定性因素不断增加，这一挑战愈发突出。论文旨在利用大语言模型（LLM）和智能体AI系统，通过结构化工作流部分自动化这些研究过程，减少工程时间并提高流程一致性。其核心思路是让LLM智能体不替代经过验证的电力系统分析与仿真工具，而是通过MCP（Model Context Protocol）连接这些工具，以技能模块编码领域知识，实现可复用、可审计的任务编排。

### Q2: 有哪些相关研究？

论文引用了多个相关研究方向。在智能体AI用于电力系统方面，文献[7]提供了电气电力系统工程中智能体AI系统的广泛综述，强调安全、可靠和可问责的智能体设计需求。文献[8]展示了LLM可以适应使用先前未见过的工具执行仿真任务，而文献[9]提出了更全面的反馈驱动多智能体框架，将这一方向扩展到更广泛的电力系统仿真研究。文献[10]探索了配电网分析的可靠智能体方法，包括自适应检索、过程生成和工具使用监督。文献[11]研究了将LLM语义推理与数值求解器集成用于电网违规检测和修复。PowerAgent项目的开源工作，包括PowerMCP和PowerSkills，已开始通过MCP服务器暴露电力系统工具，并将电力系统过程编码为可复用智能体技能[12][13]。此外，文献[14]探索了GridFM概念，即在不同电网数据和拓扑上预训练的模型可支持潮流相关应用和其他下游电网分析任务的可迁移表示。与这些工作相比，本文的独特贡献在于将技能编码、MCP工具集成和多智能体编排结合到一个面向工业级仿真平台（PSS®E）的完整框架中，并通过两种实现路径（OpenAI Agents SDK和Claude Code CLI）进行了对比评估。

### Q3: 论文如何解决这个问题？

论文提出了一种基于技能的多智能体架构，通过MCP连接的工程工具协调电力系统研究。核心设计包括三个层面：首先，开发了一个自定义MCP服务器，使用FastMCP框架将Siemens PTI PSS®E功能暴露为21个结构化工具，涵盖案例管理、潮流求解、系统数据查询、动态仿真设置、仿真执行和结果提取，以及基于play-in方法的模型验证功能。MCP作为LLM智能体与工程软件之间的接口层，只暴露经过批准的函数，使工具接口模块化、可审计且可跨不同智能体运行时复用。其次，领域知识被编码为可复用技能文件，定义过程、输入、验证检查、工具调用序列、错误处理指令和输出模板，减少对长案例特定提示的依赖。第三，采用多智能体编排：编排智能体接收研究目标，分解为子任务，并委托给专业任务智能体（电力系统研究智能体、模型验证智能体、代码与可视化智能体）。论文实现了两种路径：一是基于OpenAI Agents SDK的Python实现，提供对编排、工具接口和执行逻辑的编程控制；二是基于Claude Code CLI的实现，利用其集成的会话协调、子代理、技能、shell执行和MCP访问能力，减少自定义软件开发。两种实现共享相同的技能定义和MCP服务器，确保一致性。

### Q4: 论文做了哪些实验？

论文通过三个代表性研究流程评估了所提出的框架。第一个是潮流与案例研究任务，包括案例加载、解检查、数据质量审查和摘要报告。第二个是动态仿真，包括扰动设置、仿真执行、通道提取和数值质量检查。第三个是基于play-in方法的电厂和逆变器基资源模型验证，使用同步相量或SCADA测量数据。实验使用公开数据集（Texas 6716节点合成电网），测试了单条自然语言请求驱动完整瞬态稳定性研究的能力，例如：'使用Texas测试系统潮流基础案例和相应基础案例动态记录，为十台发电机设置输出通道并将电压和频率信号保存到通道文件，运行10秒动态仿真，在5秒时在母线111179施加三相故障，5.3秒清除故障，并将结果提取到CSV。'结果表明，两种实现均能成功执行代表性任务。OpenAI Agents SDK实现使用GPT-5.5，Claude Code实现使用Claude Sonnet 4.6，两者在测试任务上表现出定性相似的能力。评估基于任务完成度、输出准确性和人工专家干预需求。Claude Code实现需要更少的自定义软件开发，且更容易检查中间计划、工具调用、生成脚本、日志、输出和执行轨迹。论文也承认这是一项初步概念验证，未进行系统性的多次重复运行统计基准测试。

### Q5: 有什么可以进一步探索的点？

论文指出了多个未来方向。首先，计划扩展MCP功能和技能以支持 contingency analysis、批量动态仿真、模型参数校准、振荡分析和自动报告生成。其次，将评估本地部署和电网边缘部署，使用本地托管模型和安全执行环境，以处理涉及机密规划模型和敏感数据的应用。论文还提到，虽然本研究使用了提供商托管的前沿模型，但本地部署模型可能更适合未来生产实现，尽管它们目前可能在复杂工程任务的推理性能上落后于前沿模型。此外，当前评估是初步的概念验证，缺乏系统性的统计基准测试和多次重复运行，未来需要更严格的实验设计和量化评估。另一个值得探索的方向是事件驱动操作，即通过计划任务或外部渠道在检测到合格扰动事件后触发验证，以及通过API连接外部事件数据源（如PMU签名库）以支持检索和筛选扰动记录。最后，如何将技能模块标准化和共享，以及如何在不同智能体框架之间实现技能的可移植性，也是值得研究的问题。

### Q6: 总结一下论文的主要内容

本文提出了一种基于技能的多智能体框架，用于通过MCP连接的工程工具进行电力系统研究。论文开发了一个自定义MCP服务器，将Siemens PTI PSS®E的潮流分析、动态仿真、结果提取和模型验证功能暴露为21个结构化工具。框架采用多智能体架构，编排智能体将研究目标分解为子任务并委托给专业智能体，领域知识编码为可复用技能文件，定义过程、输入、验证检查和输出模板。论文评估了两种实现路径：基于OpenAI Agents SDK的Python实现和基于Claude Code CLI的实现，两者均使用可复用技能、子代理、MCP工具、数据仓库连接和本地shell/Python执行。在公开数据集上的实验表明，两种实现均能成功执行代表性研究任务，包括单条自然语言请求驱动的完整瞬态稳定性研究和基于play-in方法的电厂模型验证。Claude Code实现需要更少的自定义软件开发，更适合快速原型设计。论文指出，智能体系统可以大幅加速输电规划研究中的电力系统动态仿真过程，使工程师能够将专家判断集中于场景设计和解释，而非工具操作。
