---
title: "Autonomous Structural Discovery Of Bioprocess Dynamics And Kinetics Via LLM-Driven Agents"
authors:
  - "Erdal Aydin"
  - "Yaman Arkun"
date: "2026-10-26"
arxiv_id: "2610.35391"
arxiv_url: "https://arxiv.org/abs/2610.35391"
pdf_url: "https://arxiv.org/pdf/2610.35391v1"
categories:
  - "math.OC"
  - "cs.AI"
tags:
  - "LLM Agent"
  - "RAG"
  - "系统辨识"
  - "动力学模型发现"
  - "生物过程"
  - "主动实验设计"
  - "可解释建模"
  - "闭环诊断"
relevance_score: 7.5
---

# Autonomous Structural Discovery Of Bioprocess Dynamics And Kinetics Via LLM-Driven Agents

## 原始摘要

High-fidelity digital twins in continuous biomanufacturing are often bottlenecked by incomplete kinetic models, while standard data-driven algorithms (e.g., SINDy, PINNs) lack interpretability or impose rigid physical assumptions. This paper introduces a hybrid closed-loop architecture for autonomous kinetic state-space discovery driven by a Large Language Model (LLM) agent. The framework employs a sequential "isolation-peeling" methodology across orthogonal operational regimes. This algorithmic peeling mathematically decouples entangled multiplicative (inhibitory) and additive (catalytic) biological rate law. Grounded in a Two-Level Retrieval-Augmented Generation (RAG) library, the framework utilizes Moving Horizon Estimation (MHE) and logarithmic decomposition to decouple complex cell growth kinetics into orthogonal multiplicative (inhibitory) and additive (regulatory) residual channels. When statistical degeneracy occurs an Active Design of Experiments (DoE) controller dynamically triggers targeted perturbations to decorrelate competing model hypotheses. Evaluated on a continuous stirred-tank reactor exhibiting unmodeled Haldane inhibition, Luong product toxicity, and secondary metabolite autocatalysis, the framework autonomously expanded the state space and recovered ground-truth parameters with under 6% error without a priori kinetic knowledge.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文聚焦于连续生物制造中高保真数字孪生的核心瓶颈：动力学模型结构不完整。传统第一性原理建模需要大量先验知识，而纯数据驱动方法（如 SINDy、PINN）要么缺乏生物可解释性，要么强制假设物理结构正确，无法在模型缺失关键状态或速率定律时自主扩展状态空间。现有参数估计方法（EKF、MHE）也仅在模型结构正确时有效，遇到未建模的抑制、毒性或自催化现象时完全失效。因此，论文要解决的是从参数调优转向动态模型状态空间扩展与结构动力学发现的问题：如何在没有先验动力学知识的情况下，自主检测模型结构缺陷、插入缺失状态（ODE 生成），并辨识真实的非线性动力学拓扑。

### Q2: 有哪些相关研究？

相关工作主要分为四类。第一类是系统辨识与符号回归，如 SINDy 通过稀疏回归从数据中提取控制方程，但常产生缺乏生物意义的高维多项式；del Rio-Chanona 等人的遗传编程框架能恢复动力学速率定律，但候选机制空间需预先定义，不能自主扩展状态空间。第二类是状态估计方法，EKF 和 MHE 擅长跟踪未测量状态和时变参数，但严格依赖模型结构正确。第三类是深度学习与 PINN，神经网络插值精度高但黑箱不可解释，PINN 将微分方程嵌入损失函数，却受结构刚性约束，若模型缺失质量平衡或速率定律错误，会强制数据拟合错误假设。第四类是 LLM 科学智能体，如 Coscientist 可自主规划化学实验，ChemCrow 结合领域工具解决合成任务，RAG 将推理锚定在外部知识库。论文将 LLM 智能体作为核心诊断引擎，结合两级 RAG 库，弥补上述方法在结构性推理上的缺失。

### Q3: 论文如何解决这个问题？

论文提出一个混合闭环架构，核心是 LLM 驱动的自主动力学状态空间发现框架。首先，通过离线稳态实验固定化学计量产率和 Monod 参数，形成刚性锚点。在线阶段，用 MHE 从含噪生物量轨迹中估计比生长速率 μ_obs，并采用 Savitzky-Golay 滤波和 Tikhonov 正则化抑制噪声。接着，利用对数变换将乘性抑制项分解为可加线性残差：E_res = ln(μ_obs,mult) - ln(μ_base) = ln(μ_H) + ln(μ_L)。为解耦竞争机制，设计正交操作 regime（底物抑制、产物毒性、代谢饥饿），通过纯误差驱动 P 控制器迫使反应器进入特定稳态，使结构失配表现为孤立残差。LLM 智能体查询两级 RAG 库：Level 1 为乘性/对数域抑制函数（Haldane、Luong 等），Level 2 为加性/线性域辅助代谢通量（自催化、衰减等）。智能体将候选模型转为 JSON ODE 蓝图，经 MATLAB 执行桥进行锦标赛优化，用 AIC 评分评估。当竞争模型统计退化（ΔAIC < 2.0）时，Active DoE 控制器触发靶向底物扰动以去相关假设。最终重建五维状态空间并恢复真实参数。

### Q4: 论文做了哪些实验？

实验在一个合成 CSTR 上进行，真实植物包含未建模的 Haldane 底物抑制、Luong 产物毒性和次级代谢物自催化。基础模型仅含三个状态（S、X、P）和简单 Monod 生长，缺失次级代谢物 P_s 动态。实验设置七段正交操作 regime：0-50h 基线 Monod，50-150h 底物抑制隔离（S_sp 升至 30），250-500h 产物毒性隔离（P_sp 升至 40），500-800h 代谢饥饿（S_sp 降至 2）触发自催化。测量噪声 σ=0.05，采样间隔 0.5h。MHE 滚动窗口 10 步，λ=0.10。结果显示，框架自主将状态空间从三维扩展到五维，成功识别 Haldane 抑制、Luong 毒性和自催化项，恢复的真实动力学参数误差低于 6%，且无需任何先验动力学知识。

### Q5: 有什么可以进一步探索的点？

局限性包括：框架依赖预定义的两级 RAG 库，若真实物理不在库中，智能体会构造“结构虚构”；加性错觉需人工监督识别；Active DoE 仅在线触发退化干预，整体仍为离线/在线混合架构，未实现完全自主的开放世界发现。未来方向可包括：扩展 RAG 库至开放世界动力学形式，引入自动库演化或符号生成；让 LLM 自主管理常规 regime 切换以减少人工设计；将框架迁移到其他时序诊断场景，如工业设备故障链生成；结合 verifier 和反思机制提升结构假设的可追溯性与鲁棒性。

### Q6: 总结一下论文的主要内容

论文提出一种由 LLM 智能体驱动的自主动力学状态空间发现框架，用于连续生物制造数字孪生。核心创新包括：两级 RAG 知识库组织乘性与加性动力学假设；MHE 与对数分解协议将比生长速率分离为正交的乘性抑制和加性调节残差通道；正交 DoE 与 Active DoE 控制器在统计退化时触发靶向扰动以解耦竞争假设。在含未建模 Haldane 抑制、Luong 毒性和自催化的合成 CSTR 上，框架自主将状态空间从三维扩展到五维，恢复真实参数误差低于 6%。该工作展示了 LLM 智能体作为结构诊断引擎的潜力，为可解释、可追溯的时序动力学发现提供了新范式。
