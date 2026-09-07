---
title: "Large Language Models for HVAC Operations in Building Energy Systems: A Critical Review of Methods, Applications, and Deployment Readiness"
authors:
  - "Alexander Neubauer"
  - "Tianzhen Hong"
  - "Han Li"
  - "Mengbo Yu"
  - "Amin Darbandi"
  - "Yannick Fürst"
  - "Martin Kriegel"
date: "2026-09-04"
arxiv_id: "2609.05314"
arxiv_url: "https://arxiv.org/abs/2609.05314"
pdf_url: "https://arxiv.org/pdf/2609.05314v1"
categories:
  - "cs.AI"
  - "cs.CL"
  - "eess.SY"
tags:
  - "LLM for HVAC"
  - "Building Energy Systems"
  - "Time Series Report"
  - "Semantic Description"
  - "LLM/Agent for Fault Diagnosis"
  - "Predictive Maintenance"
  - "Sensor Data Interpretation"
  - "Deployment Readiness"
  - "Human-in-the-loop"
  - "Critical Review"
relevance_score: 8.5
---

# Large Language Models for HVAC Operations in Building Energy Systems: A Critical Review of Methods, Applications, and Deployment Readiness

## 原始摘要

Building automation systems generate rich sensor data yet remain insight-poor because heterogeneous point naming, missing metadata, and fragmented documentation obstruct their operational use. This systematic review analyses and codes 66 peer-reviewed studies on large language models (LLMs) for HVAC operations published between 2023 and March 2026. Each study is classified across five application families and three LLM method families and assessed for evidence realism, deployment readiness, and the responsibility boundary between the LLM and physical HVAC decisions. The corpus is concentrated in building energy modelling (BEM, 32 of 66 papers), while load forecasting remains too sparse for subfield-level conclusions. Only four studies reach pilot-level evidence, and none reports sustained operational deployment. No study was classified as ready-now for industry adoption; three were near-term and 63 research-only. Nevertheless, several bounded, human-in-the-loop uses merit near-term trials, including point-name normalisation, document-grounded operator support, BEM workflow assistance, and advisory interfaces around physics-based controllers. Conventional machine learning (ML), model predictive control (MPC), reinforcement learning (RL) and ontology-based tools remain more adopted for high-frequency control, short-horizon numerical forecasting, and well-posed ontology mapping, while autonomous agentic operation and unvalidated occupant proxies remain research-stage. Current evidence therefore supports LLMs primarily as semantic and workflow layers rather than autonomous HVAC controllers. Future work should prioritise field-validated benchmarks, orchestration evaluation under operational constraints, and LLM-MPC/RL architectures with bounded latency and verifiable safety properties.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决建筑自动化系统“数据丰富但洞察贫乏”的核心矛盾。研究背景在于，现代建筑虽产生海量传感器数据，但异构的点命名、缺失的元数据及碎片化的文档严重阻碍了数据在故障诊断、控制优化等运维任务中的直接利用。现有方法如模型预测控制（MPC）和强化学习（RL）虽在仿真中表现优异，却因信任（黑箱难解释）、集成（数据管道不畅）和治理（责任与审计困难）三大壁垒而难以大规模落地。

现有LLM在暖通空调（HVAC）领域的研究虽快速增长，但缺乏系统性的部署就绪度评估，导致从业者无法区分哪些应用适合有界现场使用、哪些仍需验证。本文通过系统综述66篇研究，构建了应用×方法的分析框架，核心问题是明确LLM在建筑运维中究竟能扮演何种可信角色——是作为连接碎片化信息的语义与工作流层，辅助而非替代物理控制器，而非盲目追求端到端的自主控制。其根本目的在于划清技术可行性与部署防御性之间的界限，为行业提供基于证据的、安全负责的采用指南。

### Q2: 有哪些相关研究？

相关研究可分为以下几类：

**方法类**：大量工作探索LLM在HVAC中的三种适配方式——直接提示（M1）、检索增强生成（M2）和微调（M3），但多数停留在概念验证。与本文不同，这些研究往往只展示单点能力（如自然语言查询），缺乏系统性的方法对比和部署评估。

**应用类**：最集中的是建筑能耗建模（BEM，32/66篇），如用LLM辅助EnergyPlus模型搭建、参数校准和仿真结果解释。其次是故障检测与诊断（FDD），利用LLM理解设备日志和报警文本。少数研究涉及负荷预测，但样本量不足以支撑子领域结论。本文与这些工作的区别在于：不局限于单一应用，而是跨五个应用族进行统一编码和横向比较。

**评测与综述类**：已有综述多关注LLM在智能建筑中的潜力，但本文是首个系统编码66篇研究、按证据真实性和部署就绪度严格评估的工作。相比早期乐观展望，本文更强调责任边界（LLM与物理控制决策的划分）和部署现实。

**对比基线**：传统ML、MPC、RL和本体论方法在高频控制、数值预测和结构化映射上仍占主导。本文明确指出LLM更适合作为语义和工作流层，而非替代这些成熟工具，这与多数将LLM视为通用控制器的研究形成关键区别。

### Q3: 论文如何解决这个问题？

该论文通过系统性文献综述和证据编码框架，而非提出新算法，来解决LLM在HVAC运维中部署证据不足的问题。核心方法是构建一个二维分析网格：五个应用类别（A1故障诊断、A2负荷预测、A3建筑能耗建模、A4控制优化、A5热舒适与 occupant 交互）乘以三个LLM方法族（M1提示/微调、M2上下文接地编排、M3多模态视觉语言模型）。

整体框架包含四个贡献模块：一是对66篇研究进行结构化编码，绘制应用-方法分布图并追踪从M1向M2的范式转移；二是部署就绪度评估，依据证据真实性、闭环验证状态、角色边界和LLM与物理决策的责任边界，将研究分为"现成可用""近期可行"和"仅限研究"三档；三是安全感知的失败模式分析，识别幻觉、检索不完整、工具误用、延迟和错误传播等风险；四是实践指南，筛选出五个低风险、有界、人在回路的近期可用场景。

关键技术在于区分"技术可行性"与"部署可辩护性"，引入证据真实性分类和闭环验证状态作为核心评估维度。创新点包括：明确LLM在HVAC中的定位是语义和工作流层而非自主控制器；提出责任边界框架区分LLM输出与物理决策的权限；识别出BEM领域研究集中（32/66）而负荷预测证据不足的结构性缺口；并指出传统ML/MPC/RL在高频控制和数值预测中仍占优，而LLM应聚焦点名称标准化、文档问答、BEM辅助和咨询式界面等有界任务。

### Q4: 论文做了哪些实验？

该论文是一项系统性综述，而非实验性研究，因此未开展传统意义上的新实验。其“实验”体现为对2023至2026年间66篇同行评审研究的结构化编码与分析。分析框架包含五个应用类别（A1故障检测与诊断、A2负荷预测、A3建筑能耗建模、A4控制与优化、A5热舒适与 occupant 交互）和三个LLM方法类别（M1提示/微调、M2上下文编排、M3多模态）。主要发现包括：语料集中于建筑能耗建模（32/66篇），负荷预测研究过少难以得出子领域结论；仅4项研究达到试点级证据，无一项报告持续实际部署；部署成熟度评估显示0项“可立即采用”，3项“近期可行”，63项“仅限研究”。对比分析表明，传统ML、MPC、RL和本体工具在高频控制、短期数值预测和良好定义的本体映射中仍更成熟。关键结论是LLM主要适合作为语义和工作流层（如点名称规范化、文档支持的运维辅助），而非自主HVAC控制器，且标准指标（F1、R²、节能百分比）不足以表征部署就绪度。

### Q5: 有什么可以进一步探索的点？

该综述揭示了LLM在HVAC运维中的核心瓶颈：从仿真到现场部署的鸿沟。未来探索可从三方面突破：一是构建跨建筑类型的标准化现场基准测试集，统一评估点名称规范化、故障诊断等任务的语义准确性与延迟指标，解决当前语料库中模拟与真实数据混杂导致的结论碎片化问题；二是探索LLM与MPC/RL的混合架构，让LLM负责语义理解与任务编排，而高频控制仍由传统算法执行，重点研究两者间的安全切换机制与异常回退策略；三是开发可验证的“人在回路”评估框架，量化操作员对LLM建议的信任度与决策质量提升，同时引入形式化验证方法确保LLM输出在物理约束内的安全性。此外，多模态融合（如处理设备手册中的图表与传感器时序数据）和跨语言文档理解也是值得深挖的方向。

### Q6: 总结一下论文的主要内容

该论文系统综述了2023至2026年间66篇关于大语言模型（LLM）用于暖通空调（HVAC）运行的同行评审研究，构建了五类应用（故障诊断、负荷预测、建筑能耗建模、控制优化、热舒适）与三类方法（提示微调、上下文编排、多模态）的分析框架。核心贡献在于：通过证据现实性、闭环验证和责任边界三维度评估部署成熟度，发现仅4项研究达到试点级证据，无一项实现持续实际部署，63项仍属纯研究阶段。当前证据支持LLM主要作为语义和工作流层（如点名称标准化、文档问答、建模辅助），而非自主控制器；高频控制、数值预测等任务仍以传统ML、MPC、RL和本体工具为优。论文强调物理约束与安全关键性，指出标准指标不足以表征部署就绪度，并提出五项适合近期试验的低风险人机协同角色及四项未来工作优先方向，为行业提供了区分技术可行性与部署防御性的实用指南。
