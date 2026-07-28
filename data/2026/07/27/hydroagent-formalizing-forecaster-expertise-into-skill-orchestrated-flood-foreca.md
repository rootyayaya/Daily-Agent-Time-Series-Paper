---
title: "HydroAgent: Formalizing Forecaster Expertise into Skill-Orchestrated Flood Forecasting Workflows"
authors:
  - "Qingyi Yang"
  - "Siqian Qiu"
  - "Bing Li"
  - "Xu Shan"
  - "Jia Feng"
  - "Shunan Zhou"
  - "Xudong Zhou"
  - "Tiantian Xing"
  - "Jiale Guo"
  - "Xiaoyi Dong"
  - "Gaoyu Liu"
  - "Xiaohuan Liu"
  - "Haiqing Pu"
  - "Qingwen Deng"
  - "Xun Zhang"
  - "Zhongrun Xiang"
  - "Haiyang Qian"
  - "Ying Yan"
  - "Yongkang Xu"
  - "Nuo Lei"
date: "2026-07-27"
arxiv_id: "2607.23983"
arxiv_url: "https://arxiv.org/abs/2607.23983"
pdf_url: "https://arxiv.org/pdf/2607.23983v1"
categories:
  - "physics.geo-ph"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "LLM/Agent 工作流"
  - "Skill-MoE"
  - "水文预报"
  - "可解释诊断"
  - "专家知识形式化"
  - "规则约束推理"
  - "模型驱动工作流"
  - "多智能体协作"
  - "可追溯诊断链"
relevance_score: 8.5
---

# HydroAgent: Formalizing Forecaster Expertise into Skill-Orchestrated Flood Forecasting Workflows

## 原始摘要

Operational flood forecasting depends on tacit forecaster expertise that is difficult to formalize, audit, and transfer. Although artificial intelligence methods have advanced flood prediction and model-error correction, most existing studies have not explicitly represented the tacit expert rules, review checkpoints, and workflow constraints that connect model outputs to operational warning decisions. To address this issue, we propose HydroAgent, a skill-orchestrated agent framework that embeds Large Language Models (LLMs) into a model-driven flood forecasting workflow, where each skill encodes explicit rules to bound LLM reasoning. We validated its effectiveness using five state-of-the-art LLMs in the South Yamhill River basin. Our results demonstrate that prior judgment captures observed peak flow and flood volume within 5% tolerance in 10 and 11 out of 14 events, with 5-fold cross-validation over 129 events yielding Pearson correlations of 0.62 and 0.84. Building on a high-baseline scheme library (average KGE 0.890), the guided scheme selection further improves KGE by 0.023-0.154, with simulated peak flow and flood volume falling within the prior judgment ranges for 14 and 13 out of 14 events. All five tested LLMs successfully execute the HydroAgent workflow with comparable judgment accuracy (40%-80%), while showing moderate performance variation and substantial cost differences. HydroAgent does not aim to replace human forecasters; instead, it translates their tacit expertise into an auditable and reproducible workflow, streamlining analytical steps and supporting more informed decision-making. This skill-orchestrated paradigm demonstrates how explicit rule boundaries can guide language model reasoning to complement physically based simulation in next-generation flood forecasting.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决当前洪水预报中一个核心瓶颈：预报员的隐性专业知识难以被形式化、审计和转移。研究背景是，尽管基于物理的水文模型和深度学习（如LSTM）在洪水预测中取得进展，但实际运行中仍依赖“预报员在环”范式，即预报员需根据经验对模型输出进行主观判断和调整。现有方法的不足体现在两方面：一是传统水文模型和深度学习模型（包括物理信息深度学习）的可解释性差，常作为黑箱输入-输出映射，其预测可能违背水文物理规律，难以获得信任；二是基于大语言模型（LLM）的应用多局限于单步工具调用或问答任务，缺乏将专家经验、模型计算与多阶段推理流程整合的编排能力。因此，本文要解决的核心问题是：如何将预报员隐性的、主观的专家判断（如方案理解、先验判断、审查节点等）显式地编码为可执行、可审计的工作流，从而构建一个既能利用LLM的推理能力，又能通过显式规则边界约束其行为、并与物理模型协同的智能体框架。HydroAgent的提出正是为了将隐性专业知识转化为可复现的、可审计的流程，而非取代人类预报员。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是传统水文模型与深度学习预测方法，如基于过程的降雨-径流模型和LSTM等，这些方法在流量预测上表现优异，但缺乏对预报员隐性知识的显式建模，且输出难以解释。本文与之区别在于，不直接替代这些模型，而是通过技能编排框架将专家判断与数值模型结合，提升可审计性。第二类是物理信息深度学习，它通过引入物理约束提高预测一致性和泛化能力，但仍局限于输入-输出映射，缺乏推理透明性。本文则利用LLM的自然语言推理能力，在结构化工作流中生成可解释的判断轨迹。第三类是LLM/Agent在水利领域的应用，包括提示式辅助、事后报告、问答及单任务工具调用（如模型校准、调度）。这些工作缺乏多阶段工作流编排能力。本文提出的HydroAgent首次将技能编排范式引入洪水预报，通过显式规则边界约束LLM推理，实现专家知识、数值计算与语言模型推理的集成，形成可审计、可复现的操作流程。

### Q3: 论文如何解决这个问题？

HydroAgent通过一个三层的技能编排框架解决洪水预报中专家隐性知识难以形式化的问题。核心架构分为：**技能层**定义操作规则、输入输出契约和质量约束；**LLM层**负责解析事件上下文、协调工作流并生成可解释文本，但不直接计算水文数值；**工具层**执行确定性评分、模型校准、模拟和文档生成。这种分离确保语言模型不验证自身数值输出，执行器不决定业务逻辑含义。

主要模块包括五个步骤：方案准备（步骤0）将历史洪水按洪峰量级分类，使用DDS算法为每类独立校准新安江模型参数，形成类型索引的参数库；场景判断（步骤1）是推理核心，包含语义解析、六维相似度检索（总降雨量权重最大，满分13分）、专家规则推理（模拟校正和边界处理）和物理红线验证（径流系数约束0.05-1.1）；方案选择（步骤2）根据先验区间匹配参数集运行XAJ模拟；滚动预报（步骤3）随实时数据更新模拟；预警公告（步骤4）生成报告。每个步骤后设置专家审核节点，通过结构化JSON接口传递信息。

创新点在于：将技能定义为静态编写的自包含过程规范（SKILL.md文件），包含指令、工具、资源和输出契约四部分，采用渐进式披露原则仅预加载轻量元数据；通过显式规则边界约束LLM推理，而非用端到端黑箱替代物理模型；在步骤1中实现基于物理约束的模拟校正和边界处理，将专家经验转化为可审计、可复现的工作流。

### Q4: 论文做了哪些实验？

论文在南亚姆希尔河流域开展了一系列实验。实验设置包括：使用1995-2024年129次历史洪水事件进行5折交叉验证，以及2020-2024年14次洪水事件的独立验证。基准测试对比了五种最先进的大语言模型（DeepSeek-v3.2、Qwen-3.6-plus、GPT-5.4、Gemini-3.1-pro-preview和Claude-opus-4.6）。主要结果如下：在Step 1情景判断中，GPT-5.4对14次事件的峰值流量和洪水体积的命中率（5%容忍度内）分别为10/14和11/14；5折交叉验证的皮尔逊相关系数分别为0.62和0.84。在Step 2方案选择中，基于平均KGE为0.890的高基线方案库，引导选择进一步将KGE提升了0.023-0.154，14次事件中分别有14次和13次的模拟峰值流量和洪水体积落在Step 1判断范围内。五种LLM均能成功执行HydroAgent工作流，判断准确率相当（40%-80%），但运行时间和成本差异显著（DeepSeek约30元，Claude-opus-4.6约390元）。实验还发现，所有模型对Type I类洪水表现最差（命中率27%-53%），且Step 1的误判会传播至Step 2导致性能下降。

### Q5: 有什么可以进一步探索的点？

**局限性：** 当前HydroAgent的Step 1判断在罕见极端事件（如Type V洪水）和历史无相似案例（如1996年极端洪峰）上表现不佳，导致误差传播至Step 2，影响整体预报精度。此外，框架仅在单一流域验证，缺乏跨气候区、水文响应类型和流域尺度的泛化性测试，且未在实时运行环境中经受时间压力、不确定降雨预报和不完整观测的考验。

**未来研究方向：** 1) **增强长尾事件处理能力**：可引入主动学习或对抗生成网络，为罕见事件合成虚拟历史案例，或设计混合专家系统，在LLM判断置信度低时自动切换至物理模型或统计极值方法。2) **多流域与实时部署**：需在多个不同水文特征的流域进行实时洪水季测试，收集预报员交互反馈，动态更新案例库和本地化技能。3) **技能标准化与社区共享**：建立水文技能的版本控制、质量评估和基准测试体系，促进跨机构复用。4) **LLM成本与稳定性优化**：探索轻量级模型或模型蒸馏，在保持精度前提下降低推理成本；同时研究如何通过技能约束进一步抑制LLM的采样随机性。

### Q6: 总结一下论文的主要内容

HydroAgent提出了一种技能编排的智能体框架，将大语言模型嵌入到模型驱动的洪水预报工作流中。其核心贡献在于首次形式化地表达了预报员的隐性专家经验，将其转化为可审计、可复现的显式规则和操作步骤。该方法通过将专家判断（如先验判断）编码为可执行的技能，并设置明确的规则边界来约束LLM的推理，从而连接模型输出与预警决策。在South Yamhill River流域的验证表明，该框架能有效捕捉洪峰和洪量，且基于高基线方案库的引导式方案选择可进一步提升模型性能。所有测试的LLM均能成功执行工作流，判断准确率在40%-80%之间。HydroAgent的意义在于不取代人类预报员，而是将隐性专业知识转化为可审计的工作流，为下一代洪水预报中物理模型与语言模型推理的互补提供了新范式。
