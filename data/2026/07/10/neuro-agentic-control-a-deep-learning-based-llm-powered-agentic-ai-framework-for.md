---
title: "Neuro-Agentic Control: A Deep Learning-based LLM-Powered Agentic AI Framework for Controlling Security Controls"
authors:
  - "Saroj Gopali"
  - "Bipin Chhetri"
  - "Deepika Giri"
  - "Sima Siami-Namini"
  - "Akbar Siami Namin"
date: "2026-07-10"
arxiv_id: "2607.09076"
arxiv_url: "https://arxiv.org/abs/2607.09076"
pdf_url: "https://arxiv.org/pdf/2607.09076v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Time-Series Foundation Model"
  - "LLM Planner"
  - "Counterfactual Physics Injection"
  - "Industrial IoT"
  - "Anomaly Detection"
  - "Closed-Loop Control"
  - "Safety Verification"
  - "Neuro-Agentic Control"
  - "Secure Water Treatment (SWaT)"
relevance_score: 9.5
---

# Neuro-Agentic Control: A Deep Learning-based LLM-Powered Agentic AI Framework for Controlling Security Controls

## 原始摘要

Cyberattacks on operational technology are increasingly causing costly downtime and physical damage, exposing the limitations of traditional rule-based monitoring in industrial IoT environments. While Large Language Models (LLMs) have strong semantic reasoning abilities to assist in decision support, their hallucinatory nature presents unacceptable safety liabilities for closed-loop control. This paper introduces a neuro-agentic control framework, a novel architecture that couples an LLM-based planner (i.e., such as Gemini 2.5 Flash-Lite) with a pre-trained Time-Series Foundation Model (TimesFM), to achieve physics-grounded autonomous defense. The paper introduces a ``Counterfactual Physics Injection'' mechanism that simulates the impact of LLM-proposed interventions within the numerical latent space of the foundation model before actuation, while allowing the system to reject hallucinatory or unsafe actions. Evaluated on an industrial dataset (e.g., the Secure Water Treatment (SWaT)) in the context of stochastic attack scenarios, the framework exhibited better performance compared to LSTM and TCN baselines. The Neuro-Agentic Loop prevented five breaches (33.3%) below the threshold versus LSTM (26.7%) and TCN (13.3%), with zero physically invalid (hallucinated) actions executed. These results demonstrate the efficacy of using foundation models as deterministic ``Sentinels'' to safeguard agentic AI in critical infrastructure.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决工业物联网环境中，传统基于规则的监控方法无法有效应对日益复杂的网络攻击，以及现有大语言模型（LLM）在闭环控制中因幻觉特性而带来的安全隐患问题。研究背景是，针对操作技术的网络攻击正导致高昂的停机成本和物理损坏，而工业物联网中设备数量庞大，人工监控不可行。现有方法的不足包括：大多数基于LLM的智能系统仅用于离线辅助（如模型推荐），无法参与安全关键过程的闭环控制；同时，LLM的幻觉特性可能导致不安全的控制动作，在关键基础设施中是不可接受的。本文的核心问题是：如何设计一个既能利用LLM强大的语义推理能力进行自主决策，又能确保控制动作物理可行且安全的闭环控制框架。为此，论文提出了神经智能体控制框架，通过结合LLM规划器与时间序列基础模型（TimesFM），并引入“反事实物理注入”机制，在动作执行前模拟其物理影响，从而拒绝幻觉或不安全动作，实现物理约束下的自主防御。

### Q2: 有哪些相关研究？

本文的相关研究主要分为时间序列预测方法、LLM幻觉评测与反事实生成、以及LLM Agent框架三大类。

在时间序列预测方法方面，相关工作包括TimeXer（一种融入外生变量的模块化Transformer）和DBLoss（基于指数移动平均的分解损失函数）。本文与它们的区别在于，不追求提升基础预测精度，而是利用预训练的TimesFM作为“哨兵”，在物理潜空间中验证LLM提议的动作，确保控制的安全性。

在LLM幻觉评测与反事实生成方面，Kim等人构建了医学幻觉基准，发现通用模型如Gemini 2.5 Pro在链式思维提示下可达97%无幻觉率；Bhattacharjee等人提出了零样本LLM引导的反事实生成框架。本文的“反事实物理注入”机制借鉴了反事实思想，但将其应用于实时控制场景，通过物理约束拒绝幻觉动作，这与前两者静态或离线评估的性质有本质区别。

在LLM Agent框架方面，Ang等人提出了TS-Agent，用于自动化金融时间序列工作流。本文与TS-Agent类似，均采用LLM作为规划器，但本文聚焦于工业控制这一安全关键场景，并创新性地引入了神经-智能体循环，通过基础模型在物理层面进行实时防护，解决了TS-Agent在安全关键场景下的行为不确定性。

### Q3: 论文如何解决这个问题？

论文提出了一种名为“神经-智能体控制框架”（Neuro-Agentic Control Framework）的架构，将基于LLM的规划器（如Gemini 2.5 Flash-Lite）与预训练的时间序列基础模型（TimesFM）耦合，以实现物理可解释的自主防御。核心方法是“反事实物理注入”（Counterfactual Physics Injection）机制，在动作执行前，先在基础模型的数值潜空间中模拟LLM提议干预的物理影响，从而拒绝幻觉或不安全动作。

整体框架是一个两阶段控制系统，称为“神经-智能体循环”（Neuro-Agentic Loop）。主要模块包括：
1. **哨兵（Sentinel）**：使用TimesFM持续预测未来时间序列，若预测峰值超过安全阈值，则触发主动控制。
2. **架构师（Architect）**：在触发后，通过RAG增强提示（包含系统手册、执行器限制和安全阈值）生成k个候选干预策略（JSON格式，包含动作类型、幅度和持续时间）。
3. **反事实物理注入**：将每个候选策略转化为对TimesFM预测的数值扰动。对于时间步t，若t小于干预持续时间δ，则预测值增加μ·(t+1)（累积排放效应）；若t≥δ，则增加μ·δ（维持最终水平）。这确保了干预影响未来预测而非不可改变的过去。
4. **确定性风险评估**：计算每个反事实预测的最大值作为模拟风险，选择最小化风险的动作。若所有候选策略的模拟风险均超过无动作基线，则系统默认“监控”，拒绝LLM提议。

关键技术包括：冻结TimesFM权重用于纯推理，利用其预训练的时间动态知识；LLM输出受约束为结构化JSON，并验证物理可行性（如负幅度、边界内）；通过RAG知识库（如SWaT操作手册）增强LLM的语义推理。创新点在于将LLM的语义推理与基础模型的数值预测结合，通过反事实模拟实现安全关键决策，确保零物理无效（幻觉）动作执行。

### Q4: 论文做了哪些实验？

论文在SWaT数据集（14,996个数据点，78列，聚焦LIT301水位变量）上进行了实验，采用70%训练、15%验证、15%测试的划分，使用720步回看窗口预测未来24步。对比方法包括LSTM（2层64单元，Dropout 0.2）和TCN（4层25单元，Kernel size 3），均以batch size 32、10 epochs、学习率1e-3训练。在15次随机试验中注入三种攻击：突发尖峰（+150mm/20步）、渐进漂移（+100mm/100步）和高噪声（+80mm/50步）。主要指标为风险降低（ΔR）和幻觉拒绝率（HRR）。

结果显示，Neuro-Agentic框架在15次试验中成功阻止了5次越限（33.3%），优于LSTM的4次（26.7%）和TCN的2次（13.3%）。Neuro-Agentic的平均风险降低为48.51单位（标准差64.54），远高于LSTM的16.77（标准差28.85）和TCN的20.29（标准差25.74）。关键数据：Neuro-Agentic在第10次试验中实现最大风险降低215.38单位（初始峰值1118.59降至903.21），而LSTM和TCN的最大风险降低分别为67.39和52.96。最重要的是，Neuro-Agentic在所有15次试验中均未执行任何幻觉（物理无效）动作（HRR=100%），而LSTM和TCN的幻觉拒绝情况未明确报告。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面。首先，其“反事实物理注入”机制采用线性扰动近似阀门/泵效应，无法捕捉液压瞬变、传感器延迟等非线性动态，未来可替换为高保真数字孪生或校准仿真器以提升物理保真度。其次，当前基线对比不够全面，缺少与纯TimesFM消融实验及L2M-AID等LLM防御框架的直接对比，需在共享攻击场景下建立更公平的评估体系。最后，1.5-2.5秒的控制周期在单水箱场景可接受，但扩展到多传感器、多执行器系统时，候选策略组合爆炸会导致推理延迟超线性增长，需探索并行反事实模拟或分层决策架构来优化实时性。此外，可引入在线微调机制，使TimesFM能适应设备老化或工况漂移，并利用多模态数据（如振动、温度）增强Sentinel对物理异常的分辨能力，从而在保持零幻觉执行的同时进一步降低误拒率。

### Q6: 总结一下论文的主要内容

这篇论文提出了一种名为“神经-智能体控制”的新型框架，旨在解决工业物联网中传统规则监控的局限性以及大语言模型在闭环控制中的幻觉风险。核心贡献在于将基于LLM的规划器（如Gemini 2.5 Flash-Lite）与预训练的时间序列基础模型TimesFM耦合，并引入“反事实物理注入”机制。该机制在基础模型的数值潜空间中模拟LLM提议干预的物理影响，从而在执行前过滤掉幻觉或不安全动作，实现物理约束下的自主防御。在SWaT数据集上的随机攻击场景评估表明，该框架在阈值以下的事故预防率（33.3%）优于LSTM（26.7%）和TCN（13.3%），且执行了零次物理无效的幻觉动作。该研究的意义在于，通过将基础模型作为确定性“哨兵”，成功将LLM从不可靠的预测器转变为可解释、安全约束的规划器，为关键基础设施中的智能体AI安全应用提供了可行方案。
