---
title: "LLM-Driven Multi-Agent Control for Skill-Based Smart Manufacturing"
authors:
  - "Kay Köhle"
  - "Darko Anicic"
  - "Thomas A. Runkler"
  - "René Graf"
date: "2026-10-01"
arxiv_id: "2610.01364"
arxiv_url: "https://arxiv.org/abs/2610.01364"
pdf_url: "https://arxiv.org/pdf/2610.01364v1"
categories:
  - "cs.MA"
  - "cs.AI"
  - "eess.SY"
tags:
  - "LLM-based multi-agent"
  - "smart manufacturing"
  - "fault diagnosis"
  - "MCP tool server"
  - "OPC UA"
  - "MQTT"
  - "emergent fault diagnosis"
  - "agent architecture comparison"
  - "industrial automation"
  - "real-time state injection"
relevance_score: 8.5
---

# LLM-Driven Multi-Agent Control for Skill-Based Smart Manufacturing

## 原始摘要

Factories are shifting toward smaller lot sizes with high product customization, requiring frequent re-programming of flexible and reconfigurable automation systems. LLM-based agents can be deployed in two complementary roles: Offline, they generate deterministic production sequences, reducing programming effort; online, they operate live machines and handle unforeseen runtime faults that static programs cannot anticipate. We propose a solution in which each factory module is paired with a dedicated LLM-based agent and an MCP tool server that exposes the module's skills via OPC UA method calls, with agents coordinating over MQTT and grounded by real-time updates of the factory state. We compare three agent architectures (orchestrator, peer-to-peer, and monolithic) across nine production challenges of increasing complexity in a simulation of a physical six-module hexagonal factory, including silent hardware fault detection. The monolithic and peer-to-peer architectures both achieve the highest mean solve rate (93\%), while the orchestrator uniquely resolves a silent conveyor-belt fault in all ten runs by autonomously rerouting plates around the blocked segment. All architectures exhibit emergent fault-diagnosis behavior without any explicit failure-handling logic, establishing standardized MCP tooling, MQTT-based inter-agent communication, and real-time state injection as a viable and reproducible foundation for LLM-programmed smart manufacturing.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着制造业向多品种、小批量、高定制化方向转型，生产系统需要频繁重新编程，传统确定性调度器虽能可靠执行固定生产序列，却要求所有可恢复异常都必须被预先枚举并硬编码。对于“静默硬件故障”——即方法调用返回成功但物理上未产生任何效果——这类故障无法被提前穷举，因而完全落在经典调度模型之外。现有基于LLM的智能体研究虽已展示其控制工业模块、调用OPC UA方法及通过MCP暴露机器技能的能力，但仍存在明显空白：要么采用单体式智能体设计而缺乏标准化工具接口，要么使用自定义事件驱动提示而无结构化智能体间通信协议，要么展示MQTT协调却未将其与OPC UA执行层打通。尚无工作同时结合结构化智能体架构、基于MCP的模块化工具以及OPC UA标准化执行接口。本文的核心问题即在于：如何构建一个可复现的基础框架，使每个工厂模块配备专用LLM智能体与MCP工具服务器，通过OPC UA方法调用暴露技能、经MQTT协调，并注入实时工厂状态，从而在无需显式故障处理逻辑的前提下实现生产序列生成与静默故障的自主诊断与重路由。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法架构类：Lim 等最早将 GPT-4 集成到编排器架构中，通过自然语言函数调用在仿真 CNC 机床上分配 G-code 操作；Zhao 等将多智能体 LLM 系统部署到真实车间，每台机器由含专门模块的智能体控制，并以自然语言协商机器选择。应用与集成类：Xia 等提出面向模块化生产系统的多智能体架构，结合数字孪生与 OPC UA 进行任务规划与执行，是与本文最直接相关的工作；Vieira Da Silva 等利用 MCP 将制造技能暴露为语义增强的 LLM 可调用工具描述，侧重语义互操作与能力建模。评测类：上述工作多依赖专有云 API 与非结构化提示接口，或仅评估单步动作预测，缺乏跨模块故障路由，或只做能力建模而无运行时协调。本文的区别在于：同时结合多智能体架构、基于 MCP 的每智能体工具服务器、OPC UA 标准执行接口与 MQTT 智能体间通信，并在六模块工厂仿真中系统比较三种架构、评估九类生产挑战及静默故障诊断，强调可复现的运行时协调与故障处理能力。

### Q3: 论文如何解决这个问题？

论文提出的核心方案是将每个工厂模块与一个专用LLM智能体配对，并通过MCP工具服务器把模块的OPC UA方法封装为智能体可调用的工具，从而在离线时生成确定性生产序列、在线时操作实际设备并处理运行时故障。整体架构上，每个智能体只掌握工具名称、描述和模式，而MCP服务器独占OPC UA端点地址与方法签名，实现技能与编排逻辑的解耦；模块功能变更只需更新对应MCP服务器，无需改动上层智能体。智能体之间通过MQTT发布/订阅机制通信，天然支持多智能体拓扑与一对多广播。为让LLM推理有据可依，系统维护一个内部状态跟踪器，聚合板件位置、皮带占用、料仓库存和检测结果等事件，并在每次推理前以结构化上下文块注入提示词，既避免LLM从对话历史重建状态，又支持激进的上下文裁剪。此外，工具可用性管理器根据当前状态动态过滤每个智能体的工具列表，防止调用物理上不可行的操作。论文还系统比较了三种架构：编排者架构由中央智能体持有全局视图并委派任务；对等架构让模块智能体直接通信、无中心协调者；单体架构由单一智能体直接控制所有模块。实验表明，单体和P2P架构平均求解率最高达93%，而编排者架构能通过自主重路由绕开被阻塞段，在全部十次运行中解决静默传送带故障，且所有架构都涌现出故障诊断行为，无需显式失败处理逻辑。

### Q4: 论文做了哪些实验？

论文在基于Python的六模块六边形工厂仿真环境中开展了实验，评估多智能体工厂控制器。实验使用Gemma4:31B模型，通过Ollama在本地Nvidia RTX 6000 Pro Blackwell GPU上以Q4_K_M量化推理，温度设为0.3。实验设计了9个复杂度递增的生产挑战，每个挑战运行10次并报告均值：挑战1-6为基础流水线验证，涵盖单类型/多类型订单、单/双模块、旋转、补料和回收流程；挑战7-9为硬件级静默故障，包括全部边1模块缺陷、装配模块静默失效和传送带静默故障。对比了三种智能体架构：编排器、点对点和单体式。主要结果：单体式和点对点架构均达到最高平均解决率93%；编排器架构在全部10次运行中唯一成功解决了传送带静默故障，通过自主将托盘绕开阻塞段重新路由。所有架构均展现出无需显式故障处理逻辑的涌现式故障诊断行为。评估指标包括解决率、完成时间、Token消耗和工具调用次数。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有四点。其一，验证仅在仿真中完成，未考虑传感器噪声、通信延迟等物理世界不确定性，未来可研究部署于工业边缘NPU上的小型量化模型能否维持可靠性能，或让LLM从实时控制器转为生产程序生成器，在仿真中验证后再由人工审核部署。其二，所有通信走本地MQTT，未评估真实网络延迟与带宽约束下的表现。其三，六边形传送带骨架造成物理中心化，天然不利于对等架构，可探索更去中心化的拓扑。其四，可扩展性存疑，更大工厂布局与更复杂模块拓扑尚未验证。此外，针对挑战7的循环失败与挑战9的跨边界故障传播，可引入共享记忆库、全局广播通道或显式故障处理逻辑，并探索混合架构以兼顾全局重规划与局部效率。

### Q6: 总结一下论文的主要内容

本文针对高定制化、小批量生产场景下柔性自动化系统频繁重编程的问题，提出了一种由LLM驱动的多智能体智能制造控制方案。每个工厂模块配备专属LLM智能体和MCP工具服务器，通过OPC UA方法调用暴露模块技能，智能体间通过MQTT协调，并注入实时工厂状态作为决策依据。作者在六模块六边形工厂仿真中对比了编排者、对等和单体三种架构，覆盖九类复杂度递增的生产挑战。结果显示，单体与对等架构平均求解率最高，均为93%；编排者架构虽平均为87%，却能唯一在全部十次运行中自主解决传送带静默故障，通过全局视图重新规划路径绕过阻塞段。消融实验表明实时状态注入对故障诊断至关重要。该研究首次将MCP工具服务器与OPC UA集成于多智能体LLM框架，验证了其作为可复现智能制造基础的可行性。
