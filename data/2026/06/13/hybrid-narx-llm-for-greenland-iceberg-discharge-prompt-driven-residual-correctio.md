---
title: "Hybrid NARX-LLM for Greenland Iceberg Discharge: Prompt-Driven Residual Correction"
authors:
  - "Yiquan Gao"
  - "Duohui Xu"
date: "2026-06-13"
arxiv_id: "2606.15288"
arxiv_url: "https://arxiv.org/abs/2606.15288"
pdf_url: "https://arxiv.org/pdf/2606.15288v1"
categories:
  - "cs.LG"
  - "cs.AI"
  - "physics.ao-ph"
tags:
  - "LLM for Time Series"
  - "Residual Correction"
  - "Physics-Informed Prompt"
  - "Hybrid NARX-LLM"
  - "Interpretable Time Series"
  - "Climate Forecasting"
  - "Zero-Shot Reasoning"
relevance_score: 7.5
---

# Hybrid NARX-LLM for Greenland Iceberg Discharge: Prompt-Driven Residual Correction

## 原始摘要

Greenland iceberg discharge exhibits complex nonlinear dynamics with limited observability, challenging traditional predictive models. We present a Hybrid NARX-LLM framework that combines a nonlinear autoregressive model with exogenous inputs (NARX) and a large language model (LLM) for residual correction. We further propose a Physics-Informed Prompt (PIP) method that transforms unstructured physical knowledge into structured prompts for zero-shot in-context reasoning. The primary objective is to explore the corrective potential of this framework for modeling Greenland iceberg discharge, rather than merely optimizing predictive accuracy. The NARX component captures intrinsic temporal dependencies, while the LLM, guided by PIP, encodes glacier dynamics and environmental drivers and perceives key trend patterns to correct systematic prediction errors. This integration allows the model to reason about unmodeled factors and produce interpretable residuals, enhancing overall predictive accuracy. Applied to Greenland iceberg discharge time series, our approach addresses extreme events that are difficult to predict due to rare variations and nonstationary trends, a limitation often overlooked by traditional methods. By fusing structured time-series modeling with knowledge-driven foundation AI, the framework offers a scalable and interpretable pathway to bridge data-limited climate forecasting with physics-informed LLM reasoning. The code is available.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

格陵兰冰盖质量损失是近几十年来全球海平面上升的主要贡献者之一，其中冰山崩解通量（冰排放）的准确预测对理解冰-海相互作用至关重要。然而，冰山排放受非线性、部分观测的冰-海洋过程控制，表现出强非平稳性和有限可预测性。现有方法存在明显不足：广泛使用的NARX模型虽能捕捉非线性时间依赖，但对分布偏移敏感且存在固有预测延迟；物理模型受限于崩解动力学的简化表示；而数据驱动模型因冰山排放数据集稀缺，易过拟合，且仅依赖表面物质平衡、北大西洋涛动等稀疏输入变量，缺失关键变量导致性能偏差。因此，本文要解决的核心问题是：在不增加数据样本或信息性输入变量的前提下，如何提升冰山排放的预测性能？为此，论文提出混合NARX-LLM框架，利用NARX进行基线预测，并引入大语言模型进行残差校正。同时提出物理知识提示方法，将非结构化冰川学知识转化为结构化提示，引导LLM进行零样本上下文推理，从而校正系统预测误差，增强对极端事件的预测能力，并提升模型的可解释性和鲁棒性。

### Q2: 有哪些相关研究？

在相关研究中，本文主要涉及三个类别：**冰山水文建模**、**残差修正方法**和**大语言模型（LLM）辅助气候预测**。

1. **冰山水文建模**：传统物理模型依赖简化的“崩解定律”，难以捕捉峡湾地形等复杂交互；数据驱动方法易过拟合且无法预测极端事件。本文通过NARX模型捕捉时序依赖，并引入LLM进行残差修正，弥补了物理模型与纯数据驱动方法的不足。

2. **残差修正方法**：现有研究将残差修正作为迭代优化（如Boosting）或动态校准工具，用于提升预测精度。本文创新地将LLM作为残差修正器，通过物理信息提示（PIP）引导其编码冰川动力学与环境驱动因素，从而校正NARX模型未建模的非线性与长期趋势。

3. **LLM辅助气候预测**：近期工作如ClimaQA评估LLM科学可靠性，Zephyrus等智能体系统用于气象任务。本文首次将LLM推理应用于冰山水文预测，利用其上下文推理能力处理非平稳动态，区别于现有LLM在气候领域的文本或自动化工作流应用。

### Q3: 论文如何解决这个问题？

该论文提出了一种混合NARX-LLM框架，用于格陵兰冰山排放预测，核心方法是将非线性自回归外生模型（NARX）与大型语言模型（LLM）的残差校正能力相结合。整体框架包含四个主要模块：NARX基线模型、物理信息提示（PIP）方法、LLM零样本上下文推理（ICR）模块和自适应权威控制（AAC）模块。

NARX模型作为数值骨干，通过固定效应和随机效应分解外生物理变量（如表面质量平衡、北大西洋涛动、拉布拉多海海表温度），捕获标准非线性时间依赖关系。PIP方法将非结构化冰川学知识转化为结构化提示模板，包含时间边界、物理状态、模型性能和领域先验四个语义块，将季节性周期、气候变量、历史偏差和专家规则编码为LLM可理解的文本上下文。

LLM零样本推理作为趋势感知智能体，基于PIP生成的上下文向量，以低温度（τ=0.1）并行采样3条独立响应轨迹，通过中位数聚合生成残差校正标量δ。AAC模块包括零状态检查（基于滑动窗口均值和方差判断是否跳过LLM调用）、尖峰检测、动态信任区域和噪声基底饱和边界，确保数值稳定性和生成鲁棒性。

创新点在于：1）将LLM作为残差校正器而非直接预测器，利用其语义理解能力修正NARX的系统性偏差；2）PIP方法实现了物理知识的结构化注入，使LLM能推理未建模因素；3）AAC模块提供了自适应控制机制，在计算效率和预测精度间取得平衡。

### Q4: 论文做了哪些实验？

论文使用1901-2018年格陵兰冰山排放月度数据集（目标变量I48N，输入为SMB、NAO、LSST），按80:20时间分割，以12个月滞后构建NARX格式。基线为单隐层（10单元，Tanh激活）NARX模型，混合模型在此基础上用Qwen2.5-1.5B-Instruct LLM进行残差校正，窗口W=3。主要结果：混合模型在5次独立运行中全面优于基线——RMSE从92.2183降至91.6311，MAE从44.1187降至37.5294（降幅14.94%），R²从0.4461提升至0.4532（±0.0028），EVS从0.4485提升至0.4532。消融实验显示：移除物理状态块导致R²骤降至0.3826（方差±0.0197）；移除时间边界虽微降RMSE（91.3694）但方差扩大；移除模型性能块MAE最优（36.8876）但RMSE恶化；移除领域先验知识使R²降至0.4140。定性分析验证了LLM基于物理状态（如LSST趋势）生成显式推理路径的能力，在极端事件（如1998、2008年峰值）上显著提升追踪精度。

### Q5: 有什么可以进一步探索的点？

基于论文的实验结果与分析，该Hybrid NARX-LLM框架虽在残差校正和可解释性上取得进展，但仍存在若干可进一步探索的方向。首先，模型在极端峰值（如1998和2008年历史最大值）的预测上仍存在系统性低估，表明LLM的零样本推理能力在捕捉罕见极端事件时仍有局限。未来可引入对抗性训练或生成式重采样技术，以增强模型对尾部事件的敏感性。其次，消融实验显示去除“时间边界”块后指标略有提升，暗示当前提示设计可能过度约束了模型的灵活性。可探索动态自适应提示机制，根据预测误差自动调整语义块的权重。此外，当前仅使用Qwen2.5-1.5B模型，可尝试更大规模或领域微调的LLM（如气候领域预训练模型），以提升物理知识编码的深度。最后，框架仅依赖三个环境变量，未来可集成更多高分辨率遥感数据（如冰流速、海冰浓度），并通过多模态LLM融合文本与数值特征，进一步提升对非线性动力学的建模能力。

### Q6: 总结一下论文的主要内容

这篇论文提出了一种混合NARX-LLM框架，用于解决格陵兰冰山排放预测中非线性、非平稳和部分可观测的挑战。核心贡献在于：1) 将非线性自回归外生输入模型（NARX）与大型语言模型（LLM）结合，通过残差校正提升预测性能，而无需额外数据或输入变量；2) 设计了物理信息提示（PIP）方法，将非结构化的冰川学知识转化为结构化自然语言提示，引导LLM进行零样本上下文推理，生成可解释的物理推理路径。主要结论表明，该框架能有效捕捉NARX遗漏的长期物理趋势，校正极端事件预测偏差，并显著提升模型在数据稀缺场景下的鲁棒性和可解释性。其意义在于为数据有限的气候预测提供了一种可扩展的、融合物理知识与基础AI的范式。
