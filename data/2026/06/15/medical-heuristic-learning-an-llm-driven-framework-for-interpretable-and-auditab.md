---
title: "Medical Heuristic Learning: An LLM-Driven Framework for Interpretable and Auditable Clinical Decision Rules"
authors:
  - "Wei Xu"
  - "Ke Yang"
  - "Gang Luo"
  - "Keli Zheng"
  - "Lingyan Hu"
  - "Jing Wang"
  - "Kefeng Li"
date: "2026-06-15"
arxiv_id: "2606.16337"
arxiv_url: "https://arxiv.org/abs/2606.16337"
pdf_url: "https://arxiv.org/pdf/2606.16337v1"
categories:
  - "cs.AI"
  - "cs.HC"
  - "cs.LG"
tags:
  - "LLM-driven workflow"
  - "interpretable decision rules"
  - "clinical tabular data"
  - "rule synthesis"
  - "iterative refinement"
  - "continual learning"
  - "small-sample learning"
  - "class imbalance"
  - "feature evolution"
  - "auditable AI"
relevance_score: 7.5
---

# Medical Heuristic Learning: An LLM-Driven Framework for Interpretable and Auditable Clinical Decision Rules

## 原始摘要

Predictive modeling for clinical tabular data is central to clinical decision support and therefore requires not only strong predictive performance but also transparent decision logic. Although deep learning and tree-based ensemble methods can achieve high accuracy, their black-box nature remains a major obstacle to clinical deployment. This challenge is further compounded by common characteristics of medical data, including limited sample sizes, severe class imbalance, and feature evolution arising from changes in diagnostic criteria and clinical documentation. To address these issues, we propose Medical Heuristic Learning (MHL), an instantiation of the learning-beyond-gradients paradigm for clinical tabular prediction. Instead of relying on neural network weight updates, MHL uses a large language model (LLM)-driven workflow that integrates statistical probes, medical knowledge probes, rule synthesis, and code-level iterative refinement to optimize a deterministic and executable decision system. The resulting model is expressed not as opaque parameters, but as versioned pure-Python decision rules that are explicitly interpretable, fully auditable, and clinically grounded. MHL also supports continual learning by starting from previously validated rules and iteratively revising them using updated feature information under data drift or feature evolution. Comprehensive experiments on medical datasets show that MHL achieves performance comparable to state-of-the-art methods while maintaining strong behavior in small-sample and highly imbalanced settings. The results further indicate that this explicit rule update mechanism can help alleviate catastrophic forgetting under feature evolution. Overall, these findings suggest that non-gradient-based heuristic systems offer a transparent and adaptable alternative for high-stakes clinical decision support.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决临床表格数据预测中预测性能与可解释性之间的核心矛盾。研究背景是，尽管深度学习与树集成方法在临床决策支持中能取得高精度，但其“黑箱”特性严重阻碍了临床部署。现有方法的不足主要体现在三个方面：第一，深度网络等黑箱模型依赖SHAP、LIME等事后解释工具，但这些工具对建模选择和输入扰动敏感，无法提供稳定可靠的临床洞见；第二，医疗数据常具有小样本、严重类别不平衡以及因诊断标准变化导致的特征演化等特点，基于梯度优化的模型在此类数据上容易不稳定且难以直接适应新特征空间；第三，传统模型在应对数据漂移或特征演化时，通过迁移学习更新容易引发灾难性遗忘。因此，本文要解决的核心问题是：如何构建一个既具备与黑箱模型相当预测性能，又具有完全可解释性、可审计性，并能适应医疗数据动态变化（如特征演化）的临床决策规则系统。

### Q2: 有哪些相关研究？

本文的相关研究主要分为以下几类：

1. **可解释机器学习方法**：包括线性模型、浅层决策树等传统可解释模型，以及SHAP、LIME等事后解释工具。本文指出这些方法存在局限性：简单模型性能不足，而事后解释工具对输入扰动敏感、稳定性差。MHL通过直接生成可读的Python决策规则，实现了内在可解释性，避免了事后解释的不稳定性。

2. **黑盒预测模型**：包括深度神经网络和树集成方法（如XGBoost、随机森林）。这些方法在复杂任务上性能优异，但存在“黑箱”问题，难以在临床高风险场景中部署。MHL在性能上与之相当，但提供了完全透明的决策逻辑，解决了临床部署的核心障碍。

3. **启发式学习与规则学习**：传统启发式算法（如粒子群优化、蚁群优化）和规则学习系统（如决策树、规则归纳）。本文提出的MHL属于“学习超越梯度”范式，利用LLM作为规则生成代理，在显式程序空间而非数值参数空间进行优化，实现了规则的可迭代、可审计更新。

4. **持续学习与灾难性遗忘缓解**：相关研究包括弹性权重巩固（EWC）、记忆重放等方法。MHL通过从已验证规则集出发、进行显式规则修订来适应数据漂移和特征演化，避免了梯度更新导致的灾难性遗忘，提供了一种新颖的持续学习机制。

5. **LLM驱动的自动化机器学习**：如使用LLM进行代码生成、特征工程等。MHL将LLM作为结构化工作流中的规则合成与迭代引擎，而非开放式的编码代理，更适用于医疗领域对约束和可审计性的要求。

### Q3: 论文如何解决这个问题？

该论文提出的医学启发学习（MHL）框架，通过一个由大语言模型（LLM）驱动的五阶段工作流，替代传统神经网络梯度更新，生成可解释、可审计的确定性决策规则。其核心架构包括以下组件：

1. **统计探针**：从训练集中提取结构化经验信号，输出包含特征排名、描述性统计（均值、标准差、缺失率等）和单变量分析结果（点双列相关系数、Mann-Whitney U检验、卡方检验等）的CSV文件，为规则构建提供量化依据。

2. **医学知识探针**：将统计信号转化为临床可解释的规则设计上下文。它强制输出固定格式的Markdown表格，包含特征、单变量信号摘要、临床原理、建议阈值和证据置信度（高/中/低），确保规则既基于统计关联又具备医学合理性。

3. **初始规则生成**：LLM接收两个探针的输出、任务描述和指标优先级描述，生成可执行的Python分类函数`predict_v0`。该函数必须使用纯Python标准库，每个分支需包含医学注释，且以JSON格式输出版本号、错误分析和完整代码。

4. **迭代规则优化**：通过“数据反馈-规则演化”双通道机制实现。当前规则在训练集上执行后，系统收集误分类样本、退化样本（上一版本正确但当前版本错误的案例）和迭代历史。LLM在严格的最小修改约束下，优先处理退化案例，每次仅调整少量阈值或规则，生成新版本`V_{t+1}`。修改后的代码需通过语法检查和命名规范验证。

5. **持续学习扩展**：在特征演化场景下，MHL从已验证的规则出发，利用更新后的特征信息进行迭代修订，通过显式规则更新机制缓解灾难性遗忘。

**创新点**：完全摒弃梯度更新，将LLM作为受控代码编辑器，每个修改步骤都关联到显式证据（统计信号、临床原理、退化警告），生成版本化的纯Python决策规则。这使得模型不仅具有与SOTA方法相当的性能，还在小样本和高度不平衡场景下表现稳健，同时提供完全透明、可审计的决策逻辑。

### Q4: 论文做了哪些实验？

论文在三个医疗数据集上进行了实验：UK Biobank (UKB) 用于抑郁症预测，CCID 和 MIMIC 用于 ICU 28天死亡率预测。对比方法包括逻辑回归、决策树、XGBoost、LightGBM、MLP 和 FT-Transformer。所有实验重复三次随机种子并报告平均值，默认使用 DeepSeek-V4-Pro 作为 LLM 后端。

主要实验包括：
1. **消融实验**：在 UKB 和 CCID 上比较无探针、仅知识探针、仅统计探针和双探针（S+K）配置。结果显示 S+K 在 F1 指标上最稳定，在低样本量下表现尤为突出。
2. **样本量实验**：训练集大小从 10 到 3000。MHL 在训练样本少于 100 时始终取得最佳 F1（如 UKB 上 n=10 时 F1=0.623），而 LightGBM 和 FT-Transformer 在此情况下崩溃。
3. **类别不平衡实验**：训练集正负比从 1:1 到 50:1 和 1:50。在极端不平衡下，多数基线模型退化为单类预测，而 MHL 在多数设置中保持有意义的混淆矩阵，如 CCID 在 50:1 和 1:50 时均未崩溃。
4. **LLM 后端对比实验**：比较 GPT-5.5、Gemini 3.1-Pro 等六个后端。结果显示无单一后端在所有数据集上占优，GPT-5.5 在 UKB 上最佳（灵敏度 0.899，特异性 0.192），Gemini 3.1-Pro 在 CCID 上领先。
5. **持续学习实验**：在特征演化场景下，MHL 通过保留先前规则并迭代修订，有效缓解了灾难性遗忘。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：1) 仅针对二分类临床表格数据，未扩展到多模态、多分类、生存分析等复杂任务；2) 高维特征空间或复杂交互场景下，规则系统可能面临可读性和维护性挑战；3) LLM后端的选择会影响规则生成和修订轨迹，存在潜在偏差；4) 仅基于离线回顾性数据和模拟特征演化，缺乏前瞻性多中心验证。

未来可探索的方向包括：1) 将MHL框架扩展到多模态数据（如影像+文本）、时序预测和生存分析，验证其通用性；2) 开发规则复杂度控制机制，如自动剪枝或分层规则库，平衡可解释性与表达能力；3) 引入多LLM协作或规则验证模块，减少单一LLM的偏差影响；4) 设计更真实的特征演化模拟环境，并在真实临床工作流中进行前瞻性验证；5) 探索规则更新中的因果推断方法，确保修订逻辑的临床有效性而非仅统计相关性。

### Q6: 总结一下论文的主要内容

这篇论文提出了一种名为医学启发学习（MHL）的框架，旨在解决临床表格数据预测中黑盒模型缺乏可解释性和适应性的问题。MHL采用大语言模型驱动的工作流，通过统计探测、医学知识探测、规则合成和代码级迭代优化，生成可执行、版本化的纯Python决策规则，而非依赖神经网络权重更新。该方法在多个医疗数据集（如UK Biobank、CCID和MIMIC）上实现了与最先进方法相当的预测性能，并在小样本和高度不平衡场景下表现出强鲁棒性。此外，MHL通过从先前验证的规则出发进行迭代修订，有效缓解了数据漂移或特征演化下的灾难性遗忘。核心贡献在于提供了一种透明、可审计且可适应的非梯度启发式学习替代方案，为高风险的临床决策支持系统开辟了新路径。
