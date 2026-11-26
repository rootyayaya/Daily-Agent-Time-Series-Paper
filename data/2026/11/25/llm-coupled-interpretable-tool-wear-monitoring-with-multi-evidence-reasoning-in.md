---
title: "LLM-coupled interpretable tool wear monitoring with multi-evidence reasoning in CNC machining"
authors:
  - "Yuntong Chen"
  - "Yingqi Li"
  - "Qiwen Shen"
  - "Guobin Zhao"
  - "Xitian Tian"
  - "Lijiang Huang"
date: "2026-11-25"
arxiv_id: "2611.34270"
arxiv_url: "https://arxiv.org/abs/2611.34270"
pdf_url: "https://arxiv.org/pdf/2611.34270v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Tool Wear Monitoring"
  - "LLM-based Reasoning"
  - "Interpretable Diagnosis"
  - "Multi-Evidence Reasoning"
  - "CNC Machining"
  - "Predictive Maintenance"
  - "Structured Evidence Interface"
relevance_score: 8.5
---

# LLM-coupled interpretable tool wear monitoring with multi-evidence reasoning in CNC machining

## 原始摘要

Interpretable tool wear assessment in CNC machining is challenging. Existing diagnostic models have high accuracy but provide limited guidance for tool replacement. This study proposes a two layer framework combining deep learning wear classification and LLM assisted reasoning. The first layer uses PCA Loading feature selection and optimized GRU to recognize three wear states, achieving 98.38 percent macro F1 score on the PHM2010 dataset. The second layer uses LLMs to generate natural language reports and replacement suggestions from classification results and feature trends. Engineer evaluation shows the reports outperform rule templates. Cross dataset tests on NASA milling data support the generalizability of this framework.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文聚焦于CNC加工中刀具磨损评估的可解释性与决策支持问题。尽管现有基于深度学习的诊断模型在基准数据集上能达到95%以上的分类准确率，但其输出通常是数值预测、概率向量或抽象特征表示，对现场操作人员决定“是否更换刀具”和“何时更换”缺乏直接指导。可解释AI方法（如SHAP、LIME）虽能提供特征归因，但输出仍是数值分数或图表，需要专业知识才能转化为操作建议。此外，在安全关键的制造环境中，LLM生成内容的事实可靠性是额外工程挑战。因此，论文旨在构建一个两层框架，将确定性诊断计算与LLM辅助的多证据推理相结合，把分类结果、特征归因、时序趋势和置信度等证据综合成自然语言报告和可操作建议，同时通过结构化证据接口约束LLM的事实内容，确保可靠性。

### Q2: 有哪些相关研究？

相关工作主要分为三支。第一支是数据驱动的刀具磨损监测：传统方法包括直接测量和间接信号推断，深度学习方面有CNN、LSTM、GRU、Transformer等架构，以及多域特征提取和元启发式超参数优化（如PSO、GA）。第二支是可解释AI在故障诊断中的应用：SHAP、LIME等后验归因方法被广泛用于量化特征贡献，但有综述指出这些方法在结果级和最终用户可解释性上存在显著差距。第三支是LLM在故障诊断与PHM中的应用：包括将时序数据对齐到LLM进行故障分类、领域轻量级LLM、知识图谱驱动诊断、物理约束多模态LLM，以及可信多智能体LLM框架。然而，现有LLM方法主要利用LLM提升分类精度，如何将多源诊断证据（特征归因、时序趋势、置信度）综合成操作员级可解释推理仍未被充分探索，且缺乏结构化机制将LLM推理锚定在预计算诊断证据上。本文通过两层架构和结构化证据接口填补这一空白。

### Q3: 论文如何解决这个问题？

论文提出一个两层框架，通过JSON证据记录接口解耦诊断计算与可解释推理。第一层是证据增强诊断引擎：对三轴振动信号提取多域特征（时域9个、频域3个、时频域16个，共84维），采用PCA-Loading方法选择特征子集（保留原始特征物理可解释性），构建滑动窗口时序序列，使用GRU分类器（经IPSO-SA超参数优化）识别三种磨损状态。该层不仅输出类别标签，还生成结构化证据记录，包括预测状态、softmax置信度、基于单特征消融的特征归因（前5个最重要特征）、时序趋势指标（首末差和线性拟合斜率）、跨模型审查标志（当最大概率低于0.85或GRU与随机森林预测不一致时触发）以及确定性动作代码（REVIEW_NOW/REPLACE/CONTINUE）。第二层是LLM多证据推理层：LLM接收JSON证据记录和提示模板，生成自然语言报告，包含磨损状态总结、各特征解释、趋势行为和与动作代码一致的建议。关键设计是信息边界：LLM不访问原始信号、模型权重或中间状态，所有事实内容由确定性引擎预计算，LLM仅负责多证据推理、上下文解释和针对性建议，从而在安全关键场景中保障事实可靠性。

### Q4: 论文做了哪些实验？

实验主要在PHM2010数据集上进行，使用三个刀具共945个切削行程，按磨损量阈值（0.08/0.13 mm）划分三类。诊断引擎实验包括：特征选择与序列长度联合敏感性分析（3种方法×9种特征数×4种序列长度，共540次GRU训练），确定k=10、N=7的Pareto最优配置，达到98.38%宏F1；六种序列分类架构对比（GRU、LSTM、Bi-LSTM、1D-CNN、Transformer、PatchTST）；六种超参数优化方法对比（随机搜索、BO-TPE、SA、PSO、GA、IPSO-SA），发现性能对优化方法不敏感。LLM推理层评估：在三个LLM上测试事实准确性（数值保真和事实一致性），结果一致；由经验丰富的CNC工程师进行盲评，将LLM报告与基础规则模板和增强规则模板对比，在可操作性、整体质量、清晰度和决策信心四个维度上评分，LLM报告优于两种模板，增强模板恢复了大部分提升，表明证据结构化组织是决策支持价值的主要来源。跨数据集验证在NASA Ames铣削数据集的146条记录上进行，涉及不同工件材料、传感器配置和切削条件，初步证明框架无需修改即可泛化。

### Q5: 有什么可以进一步探索的点？

论文存在若干局限和未来方向。首先，跨数据集验证仅在NASA Ames上初步测试了LLM推理层的可迁移性，诊断引擎未在跨数据集上重新训练或微调，未来需验证整个框架在不同机床和工况下的泛化能力。其次，审查标志的0.85阈值是探索性设定的，未校准最优敏感度-特异度权衡，可进一步研究自适应阈值或基于不确定性的校准方法。第三，特征归因采用单特征消融，虽确定且可复现，但无法捕捉特征间交互效应，可探索更丰富的归因方法（如Shapley交互值）并保持确定性。第四，LLM仅使用DeepSeek V4 Flash，虽在三个LLM上验证了事实准确性，但未探索多LLM协作或工具调用工作流。第五，当前框架是单向流水线，缺乏反馈机制让工程师纠正或LLM自我反思，未来可引入verifier、反思循环或技能自进化机制，提升长期决策支持质量。

### Q6: 总结一下论文的主要内容

本文提出一个用于CNC加工刀具磨损监测的两层可解释框架，将深度学习诊断与LLM辅助推理通过结构化证据接口耦合。第一层诊断引擎对三轴振动信号进行多域特征提取，经PCA-Loading特征选择（10/84特征）和IPSO-SA优化的GRU分类，在PHM2010上达到98.38%宏F1，并生成包含预测状态、置信度、特征归因、时序趋势和审查标志的JSON证据记录。第二层LLM接收证据记录，生成自然语言报告和更换建议，所有事实内容预计算以确保安全关键场景的可靠性。实验表明，三个LLM均保持事实准确性；CNC工程师盲评显示LLM报告优于基础与增强规则模板，且增强模板恢复大部分提升，说明证据结构化组织是决策支持价值的主要来源；NASA Ames跨数据集验证初步证明框架可泛化。该工作为工业故障诊断中LLM与确定性诊断的可靠耦合提供了可借鉴的架构范式。
