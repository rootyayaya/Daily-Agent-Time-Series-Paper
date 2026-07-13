---
title: "All Explanations are Wrong, But Many Are Useful: Exploring the Rashomon Explanation Set with Large Language Models"
authors:
  - "Pan Li"
date: "2026-07-10"
arxiv_id: "2607.09502"
arxiv_url: "https://arxiv.org/abs/2607.09502"
pdf_url: "https://arxiv.org/pdf/2607.09502v1"
categories:
  - "cs.LG"
  - "cs.AI"
  - "cs.IR"
tags:
  - "Agentic Time Series"
  - "可解释时序诊断"
  - "LLM/Agent工作流"
  - "自然语言报告生成"
  - "Rashomon解释集"
  - "解释-预测-反思"
  - "工业预测"
  - "时间序列预测"
  - "解释忠实度"
  - "多任务学习"
relevance_score: 8.5
---

# All Explanations are Wrong, But Many Are Useful: Exploring the Rashomon Explanation Set with Large Language Models

## 原始摘要

Explaining machine-learning models is increasingly important for decision-making and consumer trust, yet it is widely believed to come at a cost: existing Explainable AI (XAI) methods suffer from a persistent accuracy-explainability trade-off. We argue that this trade-off is not fundamental, but an artifact of treating explanation and prediction as separate objectives; when properly coupled, they become complementary, so that equipping a model to explain itself improves, rather than degrades, its accuracy. We introduce the Rashomon Explanation paradigm, which builds a set of faithful, prediction-guiding explanations rather than a single one, and prove that this set is generally non-empty and that explanation fidelity bounds the performance of the models it guides. To explore this set, we propose RashomonLLM, an Explanation-Prediction-Reflection agentic workflow that generates explanations in natural language by iteratively aligning them with predictions, and we prove it converges and recovers the full set. Across customer-churn classification, clinical survival regression, and industrial click-through prediction on large-scale live-streaming logs, RashomonLLM significantly outperforms state-of-the-art prediction and XAI baselines on both accuracy and explanation quality, with gains driven by explanation fidelity and robust to distribution shifts, temporal splits, and seeds. Our framework thus advances business performance while laying the groundwork for consumer trust.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文旨在解决可解释人工智能（XAI）领域长期存在的“准确性-可解释性权衡”问题。研究背景是，尽管XAI对建立消费者信任、模型诊断等至关重要，但业界普遍认为，提升模型可解释性会牺牲预测性能。现有方法存在三大不足：第一，任何单一解释方法都无法提供完全有效的解释，因为简化模型必然在某些输入上出错，且易受分布偏移影响；第二，标量解释（如LIME或SHAP的权重）无法有效表示复杂的非线性或条件关系，只能回答“特征重要性”，而无法回答“对谁、在什么条件下、与什么组合时重要”；第三，多数XAI方法（如事后解释）与预测过程脱节，解释不直接贡献于预测性能，因此无法验证其是否揭示了真实数据模式。本文要解决的核心问题是：论证准确性-可解释性并非根本性权衡，而是将解释与预测分离的产物；通过提出“Rashomon解释集”范式，构建一组忠实且能指导预测的解释，并设计基于LLM的Agent工作流RashomonLLM，实现解释与预测的互补，从而同时提升预测准确性和解释质量。

### Q2: 有哪些相关研究？

相关研究主要分为三类：**后处理方法**（如LIME、SHAP、ROLEX）通过特征归因或模型检查事后解释输出，但可能产生虚假或不稳定的解释；**内置方法**（如注意力机制、原型学习）利用可解释模型直接生成解释，但常以牺牲预测精度为代价；**监督方法**需预先提供真实解释标签，成本高昂且难以推广。此外，**基于LLM的方法**（如直接提示或自反思）虽具备易用性、高性能和灵活推理优势，但存在幻觉、上下文敏感和不稳定等问题。

本文与这些工作的核心区别在于：第一，提出**Rashomon解释集合**范式，构建一组忠实且能指导预测的解释而非单一解释，从理论上证明解释保真度与预测性能的互补关系，打破了“精度-可解释性”权衡的固有认知。第二，设计**RashomonLLM**代理工作流，通过“解释-预测-反思”迭代循环，使解释与预测相互对齐，解决了后处理方法的不可靠性、内置方法的精度损失、监督方法对先验标签的依赖以及LLM的幻觉与不稳定问题。实验在客户流失分类、临床生存回归和工业点击率预测等任务上验证了该方法在精度和解释质量上均显著优于现有基线。

### Q3: 论文如何解决这个问题？

该论文提出RashomonLLM方法，核心是构建一个“解释-预测-反思”（EPR）的LLM智能体工作流，以探索Rashomon解释集。整体框架包含三个LLM智能体，分别对应三个组织理论设计原则：

1. **解释生成智能体**（基于意义建构理论）：负责生成一组多样化的、可指导预测的自然语言解释，而非单一解释。它通过不同配置（如提示模板、上下文）产生候选解释，满足“有用性”标准。

2. **预测智能体**（基于互补性理论）：利用生成的解释来指导预测任务，实现解释与预测的联合优化。该智能体将解释作为输入特征或推理上下文，提升预测准确性，同时解释质量也因预测反馈而改善。

3. **反思智能体**（基于双环学习理论）：持续监控预测失败案例，识别解释中的错误或不足，并触发解释生成智能体进行修正。它采用双环学习机制，不仅调整参数（单环），更会质疑和重构解释框架本身，从而迭代优化整个解释集。

**关键技术**包括：利用LLM的推理能力生成自然语言解释；通过智能体间的迭代对齐（解释→预测→反思→新解释）确保解释忠实度；理论证明该工作流收敛并能恢复完整Rashomon解释集。创新点在于：将解释与预测从分离变为互补，证明解释忠实度能提升预测性能；用LLM智能体探索解释集而非追求单一最优解；在客户流失分类、临床生存回归和工业点击率预测任务上，同时提升准确率和解释质量，且对分布偏移鲁棒。

### Q4: 论文做了哪些实验？

论文在三个任务上进行了实验：客户流失分类（Kaggle Telco数据集）、临床生存回归（METABRIC乳腺癌数据集）和工业点击率预测（快手直播大规模日志）。实验设置包括：将RashomonLLM与多种基线对比，包括传统机器学习模型（逻辑回归、XGBoost）、深度CTR模型（DeepFM、DCN-V2）、可解释模型（EBM）以及后置解释方法（LIME、SHAP）。主要结果：RashomonLLM在所有任务上均显著优于基线，例如在客户流失任务中AUC达到0.89（对比XGBoost的0.84），在生存回归任务中C-index达到0.72（对比DeepSurv的0.68），在点击率预测任务中AUC达到0.78（对比DCN-V2的0.76）。消融实验验证了解释保真度是性能提升的关键驱动因素，且模型对分布偏移、时间分割和随机种子具有鲁棒性。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：Rashomon解释集的理论构建依赖于有限数据下的等价性假设，但实际中可能遗漏关键解释；LLM生成的自然语言解释虽灵活，却缺乏对非线性交互的严格形式化保证；EPR工作流的收敛性证明基于理想化条件，未考虑LLM推理的随机性和计算成本。未来可从三方面探索：一是引入因果推断框架，将Rashomon集与结构因果模型结合，区分相关性与因果性，提升解释的鲁棒性；二是设计混合表示方法，用符号规则或图结构补充LLM的文本输出，增强对复杂条件关系的可验证性；三是优化Agent协作机制，例如加入记忆模块或主动学习策略，减少迭代轮次并降低对LLM的依赖，同时探索多任务联合训练以提升泛化能力。此外，可扩展至多模态时间序列场景，验证框架在异构数据上的适应性。

### Q6: 总结一下论文的主要内容

该论文提出“Rashomon解释”范式，挑战了可解释AI中普遍存在的准确率-可解释性权衡。作者认为，这一权衡并非固有，而是将解释与预测分离的产物。论文核心贡献是证明了当两者恰当耦合时，解释能提升而非损害预测性能。为解决现有XAI方法中“单一解释不可靠”、“标量表示不足”及“解释与预测脱节”三大挑战，论文提出了RashomonLLM，一个基于大语言模型的“解释-预测-反思”智能体工作流。该方法通过迭代优化，构建一个由多个高保真解释组成的“Rashomon解释集”，而非单一解释。理论证明该集合非空且解释保真度能约束模型性能。在客户流失分类、临床生存回归及工业点击率预测等任务上，RashomonLLM在准确率和解释质量上均显著优于现有方法。该工作为兼顾高性能与可解释性提供了新路径，有助于建立消费者信任。
