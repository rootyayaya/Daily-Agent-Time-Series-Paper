---
title: "Traceable Multi-Agent System for Knowledge-Based Forecasting"
authors:
  - "Junhyeok Kang"
  - "Sangjun Han"
  - "Hyeokjun Choe"
  - "Soonyoung Lee"
date: "2026-08-04"
arxiv_id: "2608.03339"
arxiv_url: "https://arxiv.org/abs/2608.03339"
pdf_url: "https://arxiv.org/pdf/2608.03339v1"
categories:
  - "cs.AI"
tags:
  - "multi-agent forecasting"
  - "traceable diagnosis"
  - "causal loop diagram"
  - "evidence routing"
  - "interpretable time series"
  - "LLM agent workflow"
  - "knowledge-based forecasting"
  - "crude oil price forecasting"
relevance_score: 8.5
---

# Traceable Multi-Agent System for Knowledge-Based Forecasting

## 原始摘要

Enterprise forecasting increasingly relies on autonomous agents that interpret documents, search for data, generate code, and revise models. While this autonomy helps build adaptive forecasting pipelines, it also makes it difficult for practitioners to inspect why a forecast changed, which evidence supported the change, and how data and modeling choices were revised. We present TraceMAS, an interactive demo system for traceable multi-agent forecasting. TraceMAS organizes agent outputs around two causal-loop representations: an Ideal Causal Loop Diagram (Ideal CLD), which captures key factors and their causal relations extracted from domain documents, and a Data-Grounded Causal Loop Diagram (Data-Grounded CLD), which links those factors to internal variables, external data, or documented proxies. The Data-Grounded CLD guides feature construction and model design while preserving the connection between textual evidence, data choices, and model revisions. We demonstrate TraceMAS on crude oil price forecasting. The demo interface allows users to compare forecasting iterations, inspect agent-level revisions, explore causal maps, review feature-data mappings and model architecture, and connect scenario forecasts to market narratives. This demonstration shows how autonomous forecasting agents can retain flexibility while making the evidence-to-forecast process inspectable.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决企业预测中多智能体系统“自主性”与“可追溯性”之间的核心矛盾。研究背景在于，企业预测越来越多地依赖自主智能体完成文档解读、数据检索、代码生成和模型修订等任务，这种自主性虽能构建自适应预测流程，却导致从业者难以审查预测变化的原因、支撑证据以及数据与建模选择的修订过程。

现有方法的不足体现在两方面：一是文本信息驱动的预测方法（如嵌入、提示或跨模态对齐）虽能利用文档知识，但往往隐藏了具体文本证据如何影响变量、特征或模型；二是智能体日志虽保留过程信息，但结构松散，无法有效诊断预测变化的原因。因此，现有方法无法满足企业预测中对证据到预测全链路可检查性的需求。

本文核心问题是：如何在保留多智能体自主性的同时，建立文本证据、数据选择、特征构建和模型修订之间的显式关联，使预测过程可检查、可诊断。为此，论文提出TraceMAS系统，通过理想因果回路图（Ideal CLD）和数据落地因果回路图（Data-Grounded CLD）两种共享表示，组织中间输出，实现从文档知识到预测决策的完整追溯，并以原油价格预测为例验证其有效性。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，文本信息驱动的预测方法通过嵌入、提示或跨模态对齐整合文档，但常将文本证据与变量、特征和模型的关联隐式化；多智能体系统虽能分解任务并迭代修订，但其日志通常非结构化，难以诊断预测变化原因。**应用类**中，企业预测工作流依赖智能体解析报告、检索数据并生成代码，但缺乏对证据到预测全过程的显式追踪。**评测类**工作则侧重预测精度，忽视可审计性。TraceMAS与上述工作的核心区别在于：它引入Ideal CLD和Data-Grounded CLD两种因果环表示，将文本证据、数据选择、特征工程和模型修订组织为可版本化的显式链路，使智能体在保持自主性的同时，允许用户逐层检查“为何预测变化、依据何种证据、如何修订模型”。相比纯文本预测或原始日志，TraceMAS提供了结构化的中间表示，填补了从知识到预测的可追溯性空白。

### Q3: 论文如何解决这个问题？

TraceMAS通过“因果回路图（CLD）为中心”的多智能体协作框架，将文本知识与时序数据建模显式关联，实现可追溯的预测流程。整体架构由1个主智能体（Coordinator）和6个子智能体组成，各角色围绕共享中间产物迭代更新，而非固定流水线。

核心设计包含两层CLD表示：**Ideal CLD**由Domain Analyst从领域文档提取关键因素及带方向、时滞的因果假设（如“供应受限→三个月后油价上涨”），Causal Analyst将其综合为纯文本驱动的因果图；**Data-Grounded CLD**则通过Data Engineer检索内部时序数据库、Crawler获取外部代理数据，将Ideal CLD节点映射到实际变量或代理指标，形成可检查的“证据-数据-模型”纽带。

Model Engineer依据Data-Grounded CLD构建特征：因素对应候选特征，文档假设决定滞后阶数、交互项和结构组件。Risk Reviewer持续审查数据泄漏、时间戳错位、单位不一致等问题。Coordinator综合各智能体输出更新Data-Grounded CLD并发布修订请求。每次迭代都会版本化记录CLD、数据映射、特征、审查信号和模型配置，用户可对比不同迭代，追踪从文档证据到最终预测的完整决策链。

创新点在于：将CLD从事后解释工具转变为预测构建过程中的共享工作产物；通过双层CLD分离“理想因果”与“数据可实现因果”，显式暴露数据缺口和代理选择；多智能体角色化设计保留了自主探索灵活性，同时通过版本化轨迹实现全流程可审计性。

### Q4: 论文做了哪些实验？

TraceMAS的演示实验聚焦于原油价格预测场景，采用交互式界面展示多智能体预测流程的可追溯性。实验设置围绕迭代式预测工作流展开，用户可选择不同迭代版本，查看智能体级修订摘要、因果图、特征-数据映射、模型架构、情景预测表现及市场叙事。系统通过Domain Analyst提取文档中的关键因素，Causal Analyst构建理想因果回路图（Ideal CLD），Data Engineer与Crawler将因素关联至内部时序数据库、外部数据源或文档代理，Coordinator更新数据落地因果回路图（Data-Grounded CLD）以指导建模。

实验未采用标准基准数据集，而是基于原油市场报告和企业时序数据库进行案例演示。对比方法体现为不同迭代间的因果图更新、代理替换及特征修订。主要结果包括：直接因素（如供需平衡）转化为市场状态特征，带时滞的关系生成滞后特征，内部库缺失因素（如地缘政治风险）通过外部指数或新闻代理表征。系统输出验证指标仅供迭代对比，不宣称基准级性能。关键功能包括审查者警告（如代理时间覆盖不足、未来数据泄漏、硬编码值）及因素-证据-特征-模型组件的端到端追溯路径，例如需求相关关系可从市场评论追溯到进口序列再到滞后需求特征。

### Q5: 有什么可以进一步探索的点？

TraceMAS在可追溯性上迈出了重要一步，但仍存在若干可探索的深化方向。首先，当前CLD的构建高度依赖LLM从文档中抽取因果关系的准确性，缺乏对因果方向、强度及潜在冲突证据的量化校验机制，未来可引入因果发现算法或人工反馈回路来增强CLD的可靠性。其次，Data-Grounded CLD将抽象因素映射到数据变量时，代理的映射决策可能带有主观性，且未充分处理数据缺失或代理变量选择偏差的问题，可探索基于不确定性量化的映射置信度评估。第三，系统目前主要支持事后检查，缺乏对预测偏差的主动预警或根因定位能力，未来可结合反事实推理，在预测偏离预期时自动回溯CLD中哪些节点或数据映射导致了偏差。此外，多代理间的协作与冲突消解机制尚未深入，例如不同代理对同一因素给出矛盾证据时如何裁决。最后，当前演示局限于原油价格单一场景，可扩展至多行业、多模态数据（如新闻、社交媒体）以验证框架的通用性，并探索用户交互行为数据如何反向优化CLD的迭代生成。

### Q6: 总结一下论文的主要内容

TraceMAS提出了一种面向企业预测的可追溯多智能体系统，旨在解决自主预测流程中“证据到预测”难以审查的问题。该系统构建两种因果回路图：理想因果回路图从领域文档提取关键因素及其因果关系，数据落地因果回路图则将因素映射至内部变量、外部数据或代理指标。数据落地因果回路图指导特征工程与模型设计，同时保留文本证据、数据选择与模型修订间的关联。在原油价格预测演示中，用户可比较迭代结果、检查智能体修订、探索因果图及特征映射，并将情景预测关联至市场叙事。核心贡献在于：在保持智能体自主性的同时，通过结构化的版本化工件（而非仅日志）使领域知识到预测决策的转化过程显式化、可比较，显著提升了智能预测系统的可解释性与审计能力。
