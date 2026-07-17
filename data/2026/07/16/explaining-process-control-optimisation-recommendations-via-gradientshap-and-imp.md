---
title: "Explaining Process Control Optimisation Recommendations via GradientSHAP and Implicit Differentiation"
authors:
  - "Paul Darm"
  - "Cem Alpturk"
  - "Kenneth Ulrich"
  - "William Duncan"
  - "Ali Anwar"
  - "Annalisa Riccardi"
date: "2026-07-16"
arxiv_id: "2607.14970"
arxiv_url: "https://arxiv.org/abs/2607.14970"
pdf_url: "https://arxiv.org/pdf/2607.14970v1"
categories:
  - "cs.AI"
tags:
  - "可解释AI"
  - "SHAP"
  - "隐函数定理"
  - "工业过程优化"
  - "自然语言解释生成"
  - "LLM"
  - "GradientSHAP"
  - "实时解释"
relevance_score: 7.5
---

# Explaining Process Control Optimisation Recommendations via GradientSHAP and Implicit Differentiation

## 原始摘要

Automated optimisation is increasingly adopted in industrial processes, yet a trust gap persists between engineers who design these algorithms and operators who must act on their recommendations. Explainable AI methods like SHAP (SHapley Additive exPlanations) have transformed interpretability for machine learning predictions; optimisation outputs could benefit from similar techniques. We present an approach that integrates Implicit Function Theorem (IFT) based sensitivity analysis with SHAP attribution and narrative generation via Large Language Models (LLM), producing explanations tailored for operators. Our approach leverages IFT to compute exact parameter sensitivities $\partial p^*/\partial x$ from the optimality conditions, enabling efficient GradientSHAP computation. For an industrial High Pressure Grinding Roll (HPGR) control optimisation problem with 22 features, we achieve equivalent SHAP attributions (correlation $>$0.99 with KernelSHAP) with over 40$\times$ speedup, enabling real-time natural language explanations. We validate on industrial scenarios and present feedback from domain experts on generated explanations.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在现代工业过程中，自动化优化控制虽能显著提升经济与效率，但操作人员对算法推荐的不信任构成关键障碍。尤其在矿物加工等高安全、高设备约束场景中，操作者需要理解优化建议的成因（如“为何今日推荐更高压力？”）才能安全验证并执行。现有可解释人工智能（XAI）方法如SHAP虽在机器学习预测中成功实现特征归因，但直接应用于优化输出面临两大不足：一是传统SHAP计算（如KernelSHAP）需大量模型评估，在实时工业场景中效率低下；二是优化问题的梯度信息难以直接获取，限制了GradientSHAP等高效方法的适用。本文核心解决两个问题：首先，通过隐函数定理（IFT）从最优性条件中解析推导参数灵敏度∂p*/∂x，实现优化输出的高效梯度计算；其次，将GradientSHAP归因结果与LLM结合，生成面向操作人员的自然语言解释。该方法在22维特征的工业高压辊磨机（HPGR）控制优化问题上，以KernelSHAP超过40倍的速度获得相关性>0.99的等效归因，并通过领域专家反馈验证了解释的有效性。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及三个类别：可解释机器学习、优化可解释性以及可微优化。

首先，在可解释机器学习领域，SHAP 和 GradientSHAP 是核心方法，前者基于博弈论提供特征归因，后者通过路径积分提升效率。LIME 则通过局部代理模型进行解释。Henkel 等人将 SHAP 应用于模型预测控制，Martens 等人展示了 LLM 将数值归因转化为自然语言叙述的能力。本文利用 GradientSHAP 的高效性，并借鉴 LLM 生成叙述的思路，但将其应用于优化输出而非模型预测。

其次，在优化可解释性方面，该领域尚处初期。Korikov 等人通过逆优化探索反事实解释，Biemans 等人提出基于 LIME 的采样方法为供应链调度生成特征重要性，但每次解释需多次求解优化问题。本文与这些工作的核心区别在于，通过隐式微分仅需一次求解即可获得精确灵敏度，从而避免了多次重优化的计算开销，实现了超过 40 倍的加速。

最后，可微优化领域通常将优化问题作为可微组件嵌入学习系统，利用隐函数定理计算梯度。本文创新性地将这一技术从端到端学习场景迁移至解释生成，利用最优性条件计算精确的参数灵敏度，为 GradientSHAP 提供了高效计算基础。总体而言，本文融合了上述三类工作的优势，首次实现了对工业过程控制优化建议的实时、可解释的自然语言解释。

### Q3: 论文如何解决这个问题？

该论文提出了一种结合隐函数定理（IFT）与GradientSHAP的可解释性方法，用于解释工业过程控制优化推荐。核心方法是通过IFT从优化问题的最优性条件中精确计算参数灵敏度∂p*/∂s，即最优参数对输入特征的偏导数。具体而言，对于无约束优化问题，一阶最优条件∇_p L(p*, s)=0定义了隐函数p*(s)，利用隐函数定理，若Hessian矩阵非奇异，则∂p*/∂s = -H^{-1}·∂²L/∂p∂s。通过JAX自动微分高效计算该灵敏度，其计算开销远低于优化求解本身。

在架构设计上，整体框架包含三个主要模块：首先，IFT模块从优化求解器的最优性条件中提取灵敏度；其次，GradientSHAP模块利用这些灵敏度沿基线到实例的路径积分，高效计算SHAP值（与KernelSHAP相关性>0.99，速度提升40倍以上）；最后，LLM模块（GPT-5）将数值SHAP归因转化为操作员友好的自然语言解释，通过提示工程注入HPGR物理知识，确保LLM仅作为数值归因的翻译器而非物理推理器。

关键技术包括：利用IFT实现优化器输出的可微性，使GradientSHAP能直接作用于实际优化器而非代理模型；通过一次Hessian计算和批量处理标量/数组输入实现高效计算；LLM生成解释时严格基于真实SHAP值和优化器推荐参数，避免幻觉。创新点在于将IFT与GradientSHAP结合，首次实现工业优化推荐的高保真实时可解释性，同时通过LLM弥合数值归因与操作员认知之间的鸿沟。

### Q4: 论文做了哪些实验？

实验围绕工业高压辊磨机（HPGR）控制优化问题展开，使用包含22个特征的真实工业场景数据集。主要对比方法为KernelSHAP（基准方法）与基于隐函数定理（IFT）的GradientSHAP。实验设置包括：KernelSHAP分别采用10、100、1000个样本，GradientSHAP采用2、3、5个路径积分样本。关键结果如下：1）收敛性方面，KernelSHAP需要约100个样本才能稳定，而GradientSHAP仅需2-3个样本即可收敛；2）计算速度上，GradientSHAP相比收敛的KernelSHAP（1000样本）实现超过40倍加速（2样本时47.1倍，3样本时45.3倍，5样本时42.2倍）；3）准确性验证中，GradientSHAP与KernelSHAP在标量特征上的SHAP值相关性超过0.99，在20维粒度分布（PSD）数组输入上两者元素级平均SHAP值高度一致，均显示中粒度区间（第7-10箱）对最优参数影响最大。实验还通过领域专家反馈验证了生成解释的实用性。

### Q5: 有什么可以进一步探索的点？

当前方法仅适用于无约束优化问题，无法处理工业场景中常见的约束条件（如设备限幅、安全边界）。未来可扩展至带约束的KKT系统微分，通过隐函数定理处理活动集变化，但需解决非光滑性带来的计算稳定性问题。其次，依赖可微损失函数与过程模型限制了应用范围，可探索利用自动微分框架（如JAX）或神经微分方程替代传统数值优化器。SHAP的局部归因特性导致解释依赖基线选择，可引入对比解释（contrastive explanations）或因果干预方法增强鲁棒性。此外，LLM生成的叙述性解释缺乏形式化验证，建议结合知识图谱约束生成逻辑一致性，并设计用户实验量化解释对操作员决策信任度的影响。工业部署时需考虑实时性，可尝试稀疏化SHAP特征或采用在线近似采样降低计算开销。

### Q6: 总结一下论文的主要内容

该论文提出了一种结合隐函数定理（IFT）与GradientSHAP的方法，用于解释工业过程控制中的优化推荐。核心贡献在于利用IFT从最优性条件中精确计算参数敏感性，从而高效计算SHAP值，相比传统KernelSHAP实现40倍加速且相关性超过0.99。方法进一步集成大语言模型生成面向操作员的自然语言解释，解决了自动化优化算法与操作员之间的信任鸿沟。在高压辊磨机控制优化问题（22个特征）上验证了有效性，并通过领域专家反馈确认了解释的实用性。主要结论表明，该方法适用于可微分的无约束优化问题，未来可扩展至约束优化场景。
