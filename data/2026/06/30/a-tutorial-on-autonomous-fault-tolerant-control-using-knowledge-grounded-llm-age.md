---
title: "A Tutorial on Autonomous Fault-Tolerant Control Using Knowledge-Grounded LLM Agents"
authors:
  - "Javal Vyas"
  - "Milapji Singh Gill"
  - "Artan Markaj"
  - "Felix Gehlhoff"
  - "Mehmet Mercangöz"
date: "2026-06-30"
arxiv_id: "2606.31635"
arxiv_url: "https://arxiv.org/abs/2606.31635"
pdf_url: "https://arxiv.org/pdf/2606.31635v1"
categories:
  - "eess.SY"
  - "cs.AI"
  - "cs.MA"
tags:
  - "LLM Agent"
  - "故障诊断"
  - "故障恢复"
  - "可解释性"
  - "外部验证器"
  - "工业过程控制"
  - "知识注入"
  - "约束规划"
relevance_score: 7.5
---

# A Tutorial on Autonomous Fault-Tolerant Control Using Knowledge-Grounded LLM Agents

## 原始摘要

Fault recovery in process plants still relies heavily on plant operators, especially when faults fall outside predefined supervisory logic. Operators interpret alarms, procedures, P\&IDs, interlocks, and process trends, then decide how to move the plant to a safe operating mode without triggering a shutdown. This paper examines how Large Language Model (LLM) agents can support such recovery decisions. The proposed framework treats the LLM as a constrained supervisory planner. It uses plant-specific knowledge to propose recovery actions, and every proposal is checked by an external validator (symbolic or simulation-based) before actuation. The paper develops three design dimensions for applying the framework: the recovery patterns for which LLM agents are useful, the validation strategies that separate admissible from inadmissible proposals, and the deployment constraints imposed by latency, knowledge engineering, safety integration, and model lifecycle management. To make the framework directly usable, two openly available executable Python environments are provided. Both re-implement established case studies, a modular mixing module and a continuous stirred-tank reactor, extended with configurable faults and defined interfaces for custom recovery and validation methods.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

过程工业中的故障恢复仍严重依赖操作员手动决策，尤其当故障超出预定义监督逻辑时。现有容错控制方法（如鲁棒控制、监督重构和基于模型的决策逻辑）虽能提供确定性响应，但仅能处理设计阶段预期的故障，对未预期故障缺乏鲁棒性。大型语言模型（LLM）虽能利用异构知识（如P&ID、因果矩阵、操作规程）生成候选恢复动作，但其随机性导致直接作为控制器不可靠，可能产生幻觉、提出不可行动作或忽略执行器限制。因此，核心问题是如何将经典容错控制方法与LLM安全结合，构建一个可复用的框架，通过固定接口实现知识检索、动作生成、验证和回退逻辑，使不同恢复与验证方法能在统一假设下比较。本文提出将LLM作为受约束的监督规划器，其提议基于工厂特定知识并通过外部验证器（符号或仿真）检查后才执行，从而在保持语义灵活性的同时避免直接控制风险。

### Q2: 有哪些相关研究？

该论文的相关研究主要分为两类。第一类是主动容错控制（Active FTC）领域，这是一个成熟的研究方向，涵盖基于观测器的残差生成、监督重构、模型预测恢复和基于学习的控制等方法。本文与这些工作的区别在于，它不提出新的底层控制算法，而是利用LLM作为约束性监督规划器，专注于处理未在预定义逻辑中枚举的故障，并强调通过外部验证器确保安全性。第二类是LLM与智能体架构在控制任务中的应用，包括建筑自动化中的直接动作选择、工业自动化中的监督编排以及操作员辅助界面。这些工作通常针对单一任务和单一工厂，缺乏与工业故障恢复所需安全机制的集成，且提案很少经过动力学或可接受性约束验证。本文的贡献在于提供了一个通用框架和可执行环境，明确界定了LLM的适用场景（如需要解释未预枚举的工厂知识、动作空间为监督层而非低层控制），并遵循“有界提议者”原则，将LLM作为无执行权限的规划器，所有提案需经外部验证器检查。此外，本文还开发了三个设计维度（恢复模式、验证策略、部署约束），并提供了两个开源Python环境（模块化混合模块和连续搅拌反应器）作为案例研究。

### Q3: 论文如何解决这个问题？

该论文提出了一种基于知识增强型LLM Agent的自主容错控制框架，将LLM定位为受约束的监督规划器。整体架构分为物理空间和虚拟空间：物理空间保留传统调节回路（可重构控制器与受控过程），虚拟空间则包含LLM Agent系统、知识图谱和数字孪生工具层。核心流程是：故障检测与诊断（FDD）模块将检测到的故障上下文传递给LLM Agent系统，Agent系统通过检索知识图谱中的工厂特定知识（如P&ID、联锁逻辑等）构建提示，LLM据此生成候选恢复动作。关键创新在于引入外部验证器（符号模型或数字孪生）对每个候选动作进行严格校验，只有通过验证的动作才被允许执行，否则将失败原因追加到历史记录中并重新提示LLM，直到达到预设预算后切换至工程安全回退。框架沿三个设计维度展开：恢复模式（离散模式切换、连续设定点调整或混合）、验证策略（基于物理约束、瞬态响应或联锁逻辑）以及部署约束（延迟、知识工程、安全集成和模型生命周期管理）。为便于实践，论文提供了两个开源Python环境（模块化混合模块和连续搅拌反应釜），均扩展了可配置故障和自定义恢复/验证接口。该框架的核心价值在于将LLM的生成能力与工业系统的安全约束解耦，通过外部验证器确保所有动作的物理可行性。

### Q4: 论文做了哪些实验？

论文构建了两个开源的Python实验环境作为框架的测试平台，分别对应两类故障恢复模式。第一个环境是模块化混合单元，基于有限状态机实现，包含三个批次罐(B201-B203)和一个收集罐(B204)。其动作空间为离散的阀门和泵控制，属于模式A（离散监督路由）。可注入故障包括泵故障、泵退化、主管堵塞和泄漏（使主泵排空路径不可用，需切换到旁路泵），以及传感器故障（主路径仍有效，切换旁路为过度反应）。观测信号为罐液位、当前状态和执行器配置。该环境适合测试符号验证器，自定义规划器通过定义接口输入故障类型并返回目标状态和执行器集。

第二个环境是连续搅拌釜反应器(CSTR)，在PID控制下运行，模拟放热反应的物料和能量平衡。其可控元素为反应器温度、液位和入口流量的监督设定点，属于模式B（连续设定点自适应）。可注入故障包括结垢（逐渐降低传热能力，导致冷却阀饱和，需降低入口流量设定点）、泵退化（引起液位漂移）和冷却阀限制。观测信号为连续的温度、液位、流量、执行器位置和质量平衡残差。该环境适合测试基于仿真的验证器，环境本身作为数字孪生，在提案接受前进行滚动验证。自定义恢复方法通过接口输入当前过程快照和故障上下文，返回设定点三元组。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在知识工程成本高、LLM推理能力与部署延迟的权衡、以及安全集成复杂度上。未来可从以下方向探索：1) 自动化知识图谱构建，利用多模态大模型从P&ID图纸、操作手册中自动提取并校验知识，减少人工审核成本；2) 混合推理架构，将LLM的语义理解与符号推理器的因果推理结合，提升故障诊断的鲁棒性，例如用LLM生成候选假设，再用物理模型验证；3) 边缘端轻量化部署，通过模型量化、知识蒸馏或缓存机制降低延迟，满足连续控制回路的实时性要求；4) 对抗鲁棒性增强，针对prompt注入攻击设计输入净化模块或基于语义的异常检测器；5) 在线学习与自适应，使LLM能通过反馈（如validator拒绝结果）持续更新知识库或微调策略，避免静态知识库的覆盖盲区。

### Q6: 总结一下论文的主要内容

这篇教程论文提出了一种基于知识增强的LLM Agent框架，用于实现自主容错控制。核心问题在于化工过程故障恢复高度依赖操作员经验，而现有监督逻辑无法覆盖所有异常。方法上，论文将LLM作为受约束的监督规划器，利用工厂特定知识生成恢复动作，并通过外部验证器（符号或仿真）确保动作可行性。论文从三个设计维度展开：LLM适用的恢复模式、区分可接受与不可接受动作的验证策略，以及延迟、知识工程、安全集成和模型生命周期管理等部署约束。为便于应用，论文提供了两个开源的Python执行环境（模块化混合模块和连续搅拌反应器），支持自定义恢复和验证方法。主要结论是：验证器、知识图谱与现有安全层的集成比模型选择更能决定实际性能。该工作为工业故障恢复的自动化提供了可复现的基准框架，具有重要的工程实践意义。
