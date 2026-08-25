---
title: "LLM-based Agents for Forecasting and Prediction: Methods, Training, Evaluation, and Applications"
authors:
  - "Xiaogang Xu"
  - "Jiaqi Tang"
  - "Jianmin Chen"
  - "Yingying Yan"
  - "Zhenchao Tang"
  - "Xiangxin Zhou"
  - "Xiaobin Hu"
  - "Wei Wei"
  - "Jinfeng Wu"
  - "Qifeng Chen"
  - "Lu Zhou"
  - "Jiafei Wu"
  - "Zhe Liu"
  - "Jianwei Yin"
  - "Weimin Zheng"
date: "2026-08-24"
arxiv_id: "2608.23058"
arxiv_url: "https://arxiv.org/abs/2608.23058"
pdf_url: "https://arxiv.org/pdf/2608.23058v1"
categories:
  - "cs.AI"
tags:
  - "LLM-based Forecasting Agents"
  - "Time Series Forecasting"
  - "Tool-Augmented Agents"
  - "Retrieval-Augmented Generation"
  - "Hybrid LLM-Statistical Models"
  - "Evidence Retrieval"
  - "Evaluation Protocols"
  - "Distribution Shift"
  - "Benchmark Contamination"
  - "Financial Forecasting"
  - "Weather Forecasting"
  - "Health Forecasting"
  - "Energy Forecasting"
  - "Operations Forecasting"
relevance_score: 9.5
---

# LLM-based Agents for Forecasting and Prediction: Methods, Training, Evaluation, and Applications

## 原始摘要

Large language models (LLMs) now support forecasting systems that combine language-based reasoning with temporal data, evidence retrieval, external tools, and iterative prediction. We investigate LLM-based forecasting agents, meaning systems in which a language model contributes to a scored prediction about a future or currently unobserved target. We organize architectures into three groups. Standalone LLM workflows operate on encoded time series or event context. Tool- and retrieval-augmented agents incorporate external evidence. Hybrid systems pair LLMs with statistical or foundation models. We then review training methods and evaluation protocols. We examine negative as well as positive evidence, including sensitivity to small input perturbations, ablations in which the LLM component does not improve accuracy, and benchmark gains that may reflect contamination instead of temporal reasoning. We cover applications in finance, weather, health, energy, and operations, and we summarize the benchmarks and datasets used for evaluation. The evidence indicates that measurement is a central limitation. Future work requires calibration under distribution shift, contamination-resistant live evaluation, explicit reporting of cost and accuracy together, and methods for handling feedback between deployed forecasts and the outcomes being forecast.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文旨在系统性地梳理和评估基于大语言模型（LLM）的智能体在预测与预报任务中的方法、训练、评估与应用，核心问题是：在何种条件下，语言组件能够显著提升预测性能，从而证明其高昂的计算成本是合理的。

研究背景方面，传统预测依赖统计模型和深度网络，而LLM带来了语义推理能力，可处理新闻、政策等非结构化证据。然而，现有方法存在明显不足：一是缺乏统一框架，各研究在架构设计、评估标准上差异巨大；二是证据混杂，部分消融实验显示移除LLM组件后预测精度不变甚至提升，说明语言模型并非总是有效；三是评估存在严重缺陷，包括预训练数据污染、时间泄漏、推理成本未报告等问题，导致基准成绩可能虚高。

因此，本文要解决的核心问题是：如何严格界定LLM预测智能体的能力边界，建立可信的评估协议（如抗污染测试、校准验证），并明确在金融、医疗、能源等实际应用中，何时值得为语言推理能力付出额外计算代价。论文通过统一证据标准，同时审视正面与负面结果，为这一领域提供系统性的方法论指导。

### Q2: 有哪些相关研究？

相关研究可归为以下几类：

**方法类**：本文系统梳理了LLM预测智能体的三类架构——独立LLM工作流（直接编码时间序列或事件上下文）、工具/检索增强智能体（整合外部证据）、混合系统（LLM与统计或基础模型结合）。与现有工作相比，本文更强调架构分类的系统性，而非仅提出单一新方法。

**基线类**：数值预测方面，经典ARIMA、状态空间模型、M4/M5竞赛中的梯度提升树集成仍是强基线；时间序列基础模型（如Chronos、TimesFM）作为专用基线，规模远小于前沿LLM。事件预测方面，众包、超级预测者、Autocast系统及市场预测构成判断性基线。本文明确指出，许多LLM方法在这些基线上并未展现显著优势，甚至对输入扰动敏感、准确率低于统计方法。

**评测类**：本文重点批判现有评测协议，指出基准增益可能源于数据污染而非时序推理能力，强调需要抗污染的实时评测、分布偏移下的校准以及成本-精度联合报告。这与仅关注基准分数的现有评测研究形成鲜明对比。

**应用类**：覆盖金融、天气、健康、能源和运营等领域，并汇总了相关基准与数据集，为跨领域应用提供了参考框架。

### Q3: 论文如何解决这个问题？

论文通过系统性地梳理和分类LLM-based预测代理的架构设计，提出了一个三维度的分析框架来解决预测问题。核心方法是将现有系统划分为三大类架构：独立LLM工作流、工具与检索增强代理、以及混合系统。

在独立LLM工作流中，论文重点分析了数值编码和序列化策略，如LLMTime采用空格分隔的数字序列实现逐位tokenization，而TOKON通过归一化将每个值映射为单一token，在保持上下文效率的同时提升准确性。提示设计方面，MAP4TS整合数据集级上下文、局部动态和统计特性，STELLA则提取趋势、季节和残差分量作为结构化语义摘要。

工具与检索增强代理通过引入外部证据和可执行工具扩展LLM能力，如TimeClaw提供可执行的时序工具，SEA-TS采用进化算法搜索代码。混合系统则将LLM与统计模型或时间序列基础模型配对，例如通过可逆归一化将数值patch投影到LLM分支，并与时间Transformer融合，保留专用数值通路而非仅依赖文本序列化。

论文的关键创新点包括：提出固定骨干网络比较应结合输入重建任务以分离数值保真度与预测能力；识别出序列化、提示和骨干网络耦合变化导致评估不完整的问题；以及强调测量是核心局限性，需要分布偏移下的校准、抗污染实时评估、成本与精度联合报告等未来方向。

### Q4: 论文做了哪些实验？

论文系统梳理了LLM预测智能体的实验证据，但未开展单一统一实验，而是综述了多篇研究的实验设置与结果。实验设置涵盖三类架构：独立LLM工作流（如LLMTime）、工具/检索增强智能体（如AutoCast）、以及LLM与统计或基础模型混合的系统。数据集覆盖金融、天气、健康、能源和运营等领域，基准包括M4/M5时间序列竞赛、预测锦标赛问题集及零样本基础模型套件。对比方法包括ARIMA、状态空间模型、调优线性模型、Chronos/TimesFM等专用基础模型，以及人类超级预测者和预测市场。

主要结果呈现混合证据：部分LLM智能体在事件预测上接近人群水平，但数值预测常不及统计基线；对输入扰动敏感，消融实验显示LLM组件未必提升精度；基准收益可能源于数据污染而非时序推理。关键指标包括Brier分数、CRPS、pinball loss、MAE/RMSE等。作者强调测量是核心局限，建议未来采用抗污染实时评估、报告成本-精度权衡，并处理部署预测与结果间的反馈循环。

### Q5: 有什么可以进一步探索的点？

论文的核心局限在于评估体系的不完善，这直接制约了该领域的可信发展。未来探索应优先围绕以下几个方向展开：

首先，构建抗污染的动态评估协议是当务之急。现有静态基准易受预训练数据污染，导致性能虚高。应设计“未来不可知”的实时或滚动重放评估机制，确保模型在未见数据上的泛化能力被真实度量，并明确区分其是依赖时间序列推理还是记忆检索。

其次，需要建立成本-精度联合报告标准。当前研究普遍忽略推理成本，导致高算力消耗的复杂Agent看似性能优越，实则性价比极低。未来工作应引入类似“单位成本下的预测增益”的标准化指标，以公平比较不同复杂度架构的实际价值。

此外，探索分布漂移下的校准方法也至关重要。现有模型常表现出过度自信，需结合共形预测或基于Agent反馈的在线校准技术，为金融、医疗等高风险决策提供可靠的不确定性估计。同时，应深入研究预测行为对结果的反身性影响，尤其是在市场或社会动态中，模型预测可能改变被预测的结局，这需要新的理论框架来建模这种闭环反馈。

### Q6: 总结一下论文的主要内容

该论文系统综述了基于大语言模型（LLM）的预测智能体，其核心贡献在于统一了从纯提示词工作流到工具增强、再到混合系统的智能体连续谱系。论文将现有架构分为三类：独立LLM工作流（编码时间序列或事件上下文）、工具与检索增强智能体（整合外部证据）、以及LLM与统计或基础模型配对的混合系统。研究重点审视了训练方法与评估协议，并呈现正反两方面证据：一方面LLM能利用非结构化证据提升预测；另一方面，消融实验显示移除语言模型组件有时精度不变甚至提升，且基准提升可能源于数据污染而非时序推理。主要结论指出，测量是当前核心局限，未来工作需关注分布偏移下的校准、抗污染实时评估、成本与精度联合报告，以及处理部署预测与预测结果间的反馈循环。该综述对金融、天气、健康、能源和运营等应用领域均有覆盖，为智能体预测系统建立了统一的证据标准。
