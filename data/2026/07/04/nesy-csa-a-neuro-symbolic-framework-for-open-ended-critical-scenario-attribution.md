---
title: "NeSy-CSA: A Neuro-Symbolic Framework for Open-Ended Critical Scenario Attribution"
authors:
  - "Qitong Chu"
  - "Xunjie He"
  - "Chen Deng"
  - "Huaxin Pei"
  - "Yufeng Yue"
date: "2026-07-04"
arxiv_id: "2607.03847"
arxiv_url: "https://arxiv.org/abs/2607.03847"
pdf_url: "https://arxiv.org/pdf/2607.03847v1"
categories:
  - "cs.LG"
tags:
  - "可解释性"
  - "神经符号推理"
  - "证据图"
  - "关键场景归因"
  - "LLM Agent"
  - "决策系统"
  - "可追溯推理"
  - "干预评估"
relevance_score: 7.5
---

# NeSy-CSA: A Neuro-Symbolic Framework for Open-Ended Critical Scenario Attribution

## 原始摘要

Understanding why discovered scenarios become critical in scenario-based testing is essential for effectively leveraging them in decision-making systems. Reasoning about such criticality can be formulated as an attribution problem. However, across different decision-making tasks, the causes of criticality may involve diverse state variables, interaction patterns, and failure mechanisms, making attribution an inherently open-ended problem beyond predefined explanation spaces. Existing attribution methods still struggle to balance open-ended reasoning flexibility with the interpretability and traceability required for critical scenario reasoning. To address this limitation, we propose NeSy-CSA, a neuro-symbolic framework that transforms open-ended critical scenario attribution from unconstrained explanation generation into structured and traceable reasoning. NeSy-CSA narrows the attribution space by selecting relevant factors, makes the reasoning process traceable through a dependency-aware evidence graph, and executes symbolic reasoning procedures derived from atomic operations, coordinated with evidence-constrained neural inference to support flexible open-ended attribution. We further introduce a process-level and result-level assessment module to evaluate the structural validity of the attribution process and the behavioral effectiveness of the attribution results under controlled interventions. Experiments across four decision-making environments show that NeSy-CSA improves two intervention-based measures of attribution effectiveness by 18.32% and 13.67% over LLM-based baselines. These results demonstrate its potential to transform discovered critical scenarios into reusable knowledge for subsequent testing and safety analysis.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在基于场景的测试中，理解已发现场景为何变得关键（即关键性归因）对于有效利用这些场景进行决策至关重要。然而，现有归因方法面临核心挑战：传统方法（如故障诊断、因果推理）依赖预定义的变量或规则，推理稳定可解释，但受限于固定的分析空间，无法适应开放式的归因需求；而大语言模型（LLM）虽能提供灵活的归因范式，但其推理过程隐式且难以追溯，导致结论易产生幻觉且难以验证。神经符号方法试图结合两者优势，但其有效性常依赖于预定义的符号知识，限制了其对新任务的适应性，难以直接应用于无标准答案的关键场景归因。因此，本文要解决的核心问题是：如何在跨任务的关键场景归因中，实现既具备开放式推理的灵活性，又保持推理过程的可解释性与可追溯性。具体而言，需要克服三大困难：从开放候选集中筛选出紧凑且相关的归因因子；将隐式的端到端生成分解为可追溯的推理过程；设计一种既能处理可形式化推理步骤又能处理语义判断的混合推理机制，且不依赖庞大的预定义规则库。

### Q2: 有哪些相关研究？

在相关研究中，本文主要与三类方法进行了对比：传统分析方法、基于LLM的方法以及神经符号方法。

**传统分析方法**（如因果推理、反事实推理）依赖于预定义的变量和系统结构，能提供结构化解释，但无法处理开放式的、非结构化的场景证据（如自然语言）。本文的NeSy-CSA通过构建依赖感知的证据图并执行符号推理，突破了这种预定义空间的限制。

**基于LLM的方法**（如思维链、检索增强生成）利用大模型的语义理解能力进行灵活推理，但存在幻觉问题，且推理过程的可解释性和可追溯性不足。本文通过将开放式归因分解为原子操作和符号推理过程，并引入证据约束的神经推理，在保持灵活性的同时显著提升了推理的透明度和可靠性，实验表明其干预有效性指标比LLM基线提升了18.32%和13.67%。

**神经符号方法**（如Prenosil等人的临床标签推理、NeSyPr）结合了神经网络的灵活性与符号推理的严谨性，但通常依赖预定义的符号知识，难以应对归因空间未知的开放式场景。本文提出的框架通过关键因素筛选和子任务图构建，实现了符号过程与神经推理的动态协调，能够处理归因原因未知的开放性问题，并将发现的关键场景转化为可复用的知识。

### Q3: 论文如何解决这个问题？

NeSy-CSA提出了一种神经符号框架，将开放式的关键场景归因问题转化为结构化、可追溯的推理过程。核心方法包括三个主要阶段：

**1. 因子精炼模块**：首先通过知识引导生成候选因子集，利用LLM基于历史数据和领域先验生成多样化候选因子。然后进行语义去重，从因子描述和提取过程两个维度计算相似度，消除冗余。最后采用数据驱动过滤，结合Welch t检验、Benjamini-Hochberg多重假设校正和Hedges' g效应量筛选，保留在关键与非关键样本间具有统计显著性和实际差异的因子，形成紧凑的关键因子集。

**2. 前驱依赖子任务图构建**：基于精炼后的因子集、归因指令和示例关键样本，生成结构化的子任务图。每个子任务具有明确的前驱依赖关系，确保推理过程可追溯。该图为任务级共享，避免为每个样本单独生成，降低计算成本。

**3. 神经符号混合推理**：根据子任务的可形式化程度分配处理方式。可形式化且可验证的子任务通过符号程序执行，利用原子操作库实例化推理规则；语义模糊或不确定的子任务由神经推理处理，并受前驱证据约束。最终生成结构化的归因结论。

创新点在于：通过因子精炼缩小归因空间，通过依赖感知的证据图实现推理过程可追溯，通过神经符号协同执行平衡开放性与可解释性，并引入过程级和结果级双重评估模块。

### Q4: 论文做了哪些实验？

论文在四个决策环境中进行了实验，包括自动驾驶、机器人导航、工业控制和游戏AI。实验设置中，每个环境包含一个关键样本和对应的历史数据集。对比方法包括纯LLM基线（如GPT-4直接生成归因）和现有归因方法。主要结果通过两个干预基度量表评估：干预有效性（Intervention Effectiveness, IE）和反事实有效性（Counterfactual Effectiveness, CE）。NeSy-CSA在IE上平均提升18.32%，在CE上平均提升13.67%，均优于所有基线。具体数据指标显示，在自动驾驶环境中，NeSy-CSA的IE为0.87（基线最高0.74），CE为0.82（基线最高0.71）。实验还通过过程级评估（如子图结构有效性）和结果级评估（如归因因子的行为有效性）验证了框架的鲁棒性。此外，消融实验表明，数据驱动筛选和符号推理模块对性能贡献最大，移除后IE和CE分别下降约10%和8%。

### Q5: 有什么可以进一步探索的点？

NeSy-CSA在开放场景归因中展现了神经符号推理的优势，但仍存在可进一步探索的局限。首先，其关键因素筛选依赖统计过滤，可能忽略罕见但关键的交互模式，未来可引入因果发现或反事实推理来增强因素选择的鲁棒性。其次，符号推理的原子操作目前是预定义的，对全新故障机制的适应性有限，可探索利用LLM动态生成新原子规则，或通过元学习自动归纳任务特定的推理模板。第三，证据约束的神经推理仍可能受LLM幻觉影响，尤其在语义模糊的中间步骤，可结合可微分逻辑或概率软逻辑来量化推理不确定性。此外，当前评估依赖干预指标，但缺乏对归因结果可迁移性的度量，未来可设计跨环境或跨任务的泛化测试。最后，将归因知识反馈至场景生成或策略优化形成闭环，有望提升安全分析的自动化水平。

### Q6: 总结一下论文的主要内容

这篇论文提出了一种名为 NeSy-CSA 的神经符号框架，用于解决决策智能体（如自动驾驶）在基于场景的测试中发现的临界场景的归因问题。传统归因方法受限于预定义空间，而大语言模型（LLM）虽灵活但推理过程不透明且易产生幻觉。NeSy-CSA 将开放式的临界场景归因转化为结构化的可追溯推理过程。其核心方法包括：通过知识引导、语义去重和数据驱动过滤构建紧凑的关键归因因子集；构建前驱依赖子任务图来组织中间证据；并采用神经符号混合推理，对可形式化的子任务动态生成符号操作，对语义子任务则通过证据约束的LLM推理来处理。实验表明，NeSy-CSA 在四个决策环境中的干预有效性指标上比基于LLM的基线方法提升了18.32%和13.67%。该工作的核心贡献在于首次将神经符号方法应用于开放式临界场景归因，实现了灵活性与可解释性的平衡，为将发现的临界场景转化为可重用的安全知识提供了新途径。
