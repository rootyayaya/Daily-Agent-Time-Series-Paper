---
title: "LLM-Guided ODE Discovery and Parameter Inference from Small-Cohort Aggregate Data"
authors:
  - "Hanning Yang"
  - "Meropi Karakioulaki"
  - "Lennart Purucker"
  - "Tim Litwin"
  - "Cristina Has"
  - "Moritz Hess"
date: "2026-07-01"
arxiv_id: "2607.00733"
arxiv_url: "https://arxiv.org/abs/2607.00733"
pdf_url: "https://arxiv.org/pdf/2607.00733v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "LLM/Agent"
  - "ODE发现"
  - "参数推断"
  - "小样本数据"
  - "临床诊断"
  - "工具增强推理"
  - "诊断-更新循环"
  - "可解释建模"
  - "群体统计"
  - "隐私保护"
relevance_score: 7.5
---

# LLM-Guided ODE Discovery and Parameter Inference from Small-Cohort Aggregate Data

## 原始摘要

Mechanistic modeling via ordinary differential equations (ODEs) provides interpretable descriptions of complex dynamics and enables inference of underlying mechanisms, which is particularly valuable in clinical settings. However, in rare diseases, both the structure and parameters of the model are typically unknown, while individual-level data is scarce, noisy, heterogeneous, and subject to privacy constraints. In such settings, population-level summary statistics provide a practical privacy-preserving data representation, while capturing heterogeneity further requires modeling parameters as distributions rather than fixed values. Yet no existing method jointly discovers ODE structure and refines parameter distributions solely from summary statistics. We present AgentODE, an end-to-end framework that addresses this gap. An LLM proposes candidate ODE structures, while a tool-augmented inference agent iteratively refines parameter distributions through a diagnosis--update loop, operating on population-level summary statistics alone. We evaluate AgentODE on three benchmark problems across different fields and two clinical datasets, including the rare disease recessive dystrophic epidermolysis bullosa (RDEB), with only 231 observations across 46 patients. AgentODE recovers functionally consistent ODE structures across all settings, and experiments on RDEB demonstrates that in sparse and noisy data settings reasoning from summary statistics promotes mechanistically principled structure discovery, whereas baselines with individual-level data access recover implausible structures despite better predictive performance. AgentODE opens new possibilities for mechanistic modeling of rare diseases directly from population-level summary statistics, where data scarcity and privacy constraints have traditionally limited such analyses.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决在罕见病等小样本、高噪声、隐私受限的临床场景中，如何仅从群体层面的汇总统计量（而非个体级数据）联合发现常微分方程（ODE）的结构并推断参数分布的问题。研究背景是：ODE模型能提供可解释的动力学描述，但传统方法依赖专家知识或密集个体数据。现有方法的不足包括：符号回归等自动结构发现方法需要个体级数据；基于LLM的ODE发现方法同样依赖个体数据拟合；而群体建模方法（如非线性混合效应模型）需要预先指定模型结构。因此，现有方法无法仅从汇总统计量同时完成结构发现和参数分布推断。本文核心问题是：在数据稀疏、噪声大且隐私受限的条件下，如何利用LLM的科学知识检索、代码生成和视觉推理能力，通过代理循环（诊断-更新）从群体汇总统计量中迭代发现ODE结构并推断参数分布，从而避免对个体级数据的依赖，同时防止过拟合个体噪声，最终实现机制合理的罕见病动力学建模。

### Q2: 有哪些相关研究？

本文的相关研究主要分为三类。**方法类**中，经典方法如符号回归（PySR）和稀疏识别（SINDy）能从数据中恢复方程，但依赖个体级数据且需预定义算子库；神经ODE和通用微分方程虽灵活但依赖不可解释的神经组件。LLM-based方法如LLM-SR、LaSR、LLM4ED、D3和KeplerAgent利用LLM引导方程发现，但仍需个体级数据评估。**应用类**中，非线性混合效应模型虽能处理群体异质性，但需预定义ODE结构。**评测类**中，基于模拟的推断方法（如近似贝叶斯计算、序列神经似然）通过汇总统计量进行参数推断，但计算成本高且输出可解释性差。本文AgentODE是首个从群体级汇总统计量中联合发现ODE结构并推断参数分布的方法，与上述方法的关键区别在于：它无需个体级数据，通过LLM提议结构、工具增强的推理代理迭代诊断-更新参数分布，在罕见病等小样本场景下能发现机制合理的结构，而基线方法虽预测性能更优但结构不可解释。

### Q3: 论文如何解决这个问题？

AgentODE 通过一个由 LLM 驱动的双循环框架，仅从群体级汇总统计量中联合发现 ODE 结构并推断参数分布。其核心架构包含两个紧密耦合的模块：

1.  **外循环：LLM 引导的 ODE 结构发现**：该模块基于 LLM-SR 符号回归框架，由 LLM 根据问题描述和过往经验（存储在“经验缓冲区”中，采用岛屿模型维持多样性）迭代地提出候选 ODE 结构。与直接拟合个体数据的 LLM-SR 不同，AgentODE 的结构评估依赖于内循环的参数推断结果。

2.  **内循环：工具增强的参数推断智能体**：对于每个候选结构，该智能体通过“诊断-更新”循环迭代优化参数分布。它首先利用 LLM 根据候选结构和经验视觉摘要（如均值轨迹、分层轨迹、变量间一阶差分的 Spearman 相关热力图）进行初始推断。随后进入循环：
    *   **诊断**：智能体比较经验与合成数据的视觉摘要，识别差异并生成结构化诊断报告，分析失效模式、严重程度及涉及的变量。
    *   **更新**：基于诊断报告和历史最优参数，智能体推理需调整的参数及方向，更新参数分布。

**关键技术**：
*   **双重评分机制**：采用对数合成似然（logSL）评估同一结构内参数拟合度，并引入均值归一化汇总差异（MNSD）实现跨结构的一致比较，MNSD 基于经验四分位距对差异进行归一化。
*   **汇总统计量设计**：为结构发现选用涵盖分布、自相关、熵、趋势等广泛统计量；为参数推断选用聚焦于分布形状、时间自相关和跨变量依赖性的子集，以应对稀疏噪声数据。

**创新点**：首次实现仅从群体级汇总统计量联合发现 ODE 结构与推断参数分布，通过 LLM 的推理能力与工具增强的智能体循环，在保护隐私的同时，有效处理了罕见病数据稀疏、异质且受隐私约束的挑战。实验表明，该方法能发现功能一致的 ODE 结构，而基于个体数据的基线方法虽预测性能更好，却可能恢复出不可解释的结构。

### Q4: 论文做了哪些实验？

论文在三个合成基准（Apoptosis、Polymer DA Cross-linking、PKPD-Immune）和两个临床数据集（AKI和RDEB）上评估了AgentODE。实验设置包括：合成数据从领域分布中采样初始条件并引入个体间变异性；临床数据来自MIMIC-IV（353条AKI轨迹）和46名RDEB患者（231个观测值）。对比方法包括SINDy、PySR、LLM-SR†（全轨迹访问）、Neural ODE，以及两个消融变体（LLM参数初始化k=5和AgentODE w/o迭代优化）。主要结果：在RMSE指标上，AgentODE在五个数据集中四个取得最佳（如PKPD上0.064 vs Neural ODE的0.685，AKI上2.56 vs 6.162）。消融实验显示，迭代优化显著提升性能（如Polymer上0.689 vs 1.81），而LLM参数初始化在4/5数据集上因参数无效失败。在RDEB上，尽管LLM-SR†和消融变体RMSE更低（0.532和0.628 vs 0.644），但AgentODE恢复了更合理的机制结构，表明摘要级推理能避免过拟合噪声个体数据。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是性能高度依赖LLM先验知识，随着ODE复杂度增加而下降；二是无法替代基于完整轨迹的数值优化，参数可辨识性和分布精炼在数据稀疏下仍是根本挑战；三是恢复的结构仅与群体行为功能一致，而非真实机制。未来可从以下方向探索：引入Meta-Harness式自动优化管线，减少人工设计依赖；构建多智能体“思想社会”，让多个专业Agent联合推理结构与参数，增强诊断-更新循环；探索将群体统计量与少量个体轨迹结合的半监督策略，在保护隐私的同时提升参数辨识度；针对临床场景，需开发与领域专家交互的验证机制，确保发现的机制可解释且可信。此外，可尝试将框架扩展到更复杂的偏微分方程或随机微分方程系统，以应对更广泛的生物医学建模需求。

### Q6: 总结一下论文的主要内容

这篇论文提出了AgentODE，一个端到端框架，用于从群体水平汇总统计量中联合发现常微分方程（ODE）结构并推断参数分布。该方法针对罕见病研究中个体数据稀缺、噪声大、异质性强且受隐私约束的挑战，利用大型语言模型（LLM）提出候选ODE结构，并通过一个工具增强的推理智能体，在仅依赖汇总统计量的诊断-更新循环中迭代优化参数分布。在三个基准问题和两个临床数据集（包括仅有46名患者231个观测值的罕见病RDEB）上的实验表明，AgentODE能恢复功能一致的ODE结构。主要结论是，在稀疏噪声数据下，基于汇总统计量的推理能促进机制上合理的结构发现，而使用个体数据的基线方法虽预测性能更好，却可能恢复不合理结构。该工作的核心贡献在于为数据稀缺和隐私受限的罕见病研究提供了一种隐私保护的机制建模新途径。
