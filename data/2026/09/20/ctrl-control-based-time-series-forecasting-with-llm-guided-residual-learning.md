---
title: "CTRL: Control-Based Time Series Forecasting with LLM-Guided Residual Learning"
authors:
  - "Minkyoung Kim"
  - "Daeun Ji"
  - "Yohan Lee"
  - "Beomsoo Kim"
  - "Beakcheol Jang"
date: "2026-09-20"
arxiv_id: "2609.23257"
arxiv_url: "https://arxiv.org/abs/2609.23257"
pdf_url: "https://arxiv.org/pdf/2609.23257v1"
categories:
  - "cs.LG"
  - "cs.CL"
tags:
  - "LLM-based Time Series Forecasting"
  - "Residual Learning"
  - "Test-Time Adaptation"
  - "Distribution Shift"
  - "Decomposed Temporal Components"
  - "Control Signals"
  - "Frozen Backbone"
  - "LLM Agent as Controller"
  - "Non-stationary Time Series"
relevance_score: 7.5
---

# CTRL: Control-Based Time Series Forecasting with LLM-Guided Residual Learning

## 原始摘要

Time series forecasting underpins critical decision-making across diverse domains. While large language models (LLMs) offer promising reasoning capabilities, existing LLM-based time series forecasting approaches either reduce them to numerical predictors that bypass their strengths, or allow direct forecast generation that destabilizes predictions in non-stationary settings. We introduce CTRL, a framework that decouples semantic reasoning from quantitative prediction. A frozen backbone generates base forecasts, while specialized LLM agents function as controllers that analyze backbone prediction errors through decomposed trend, seasonal, and irregular components, grounding reasoning in interpretable temporal structure. Each agent outputs compact control signals that a lightweight residual decoder translates into forecast corrections. CTRL incorporates label-free test-time adaptation that detects distribution shift from input statistics alone and readapts control signals with only 3-24 LLM calls via caching. CTRL is explicitly designed to improve robustness under non-stationary temporal dynamics and distribution shift, while remaining competitive on highly stationary time series where adaptive correction provides limited additional benefit.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列预测在公共健康、金融、制造和能源等领域的数据驱动决策中至关重要。近年来，大语言模型（LLM）被引入该领域，以期借助其长程依赖建模与语义抽象能力捕捉非平稳和事件驱动环境下的潜在时序动态。然而，现有基于LLM的预测框架存在两个结构性局限：其一，许多基于提示的方法将LLM退化为类Transformer的数值预测器，仅对数值序列进行分词并输出预测值，未能发挥其上下文推理与动态适应能力；其二，当LLM直接生成数值输出时，可能破坏时序骨干模型的稳定性，放大噪声并削弱在复杂时序场景中的泛化能力。尽管TEMPO、CALF、TimeCMA等模型通过分解趋势、季节与不规则成分或跨模态对齐提升了可解释性，但仍将LLM表示直接耦合到预测生成过程。本文提出CTRL框架，旨在将语义推理与定量预测解耦：由冻结的骨干模型生成基础预测，专门的LLM智能体作为控制器，通过STL分解对比分析骨干预测误差，输出紧凑的控制信号，再由轻量残差解码器转化为预测修正。CTRL还引入无标签的测试时自适应机制，仅凭输入统计量检测分布偏移，并以3–24次LLM调用完成控制信号重适应，从而在非平稳动态与分布偏移下提升鲁棒性，同时在高度平稳序列上保持竞争力。

### Q2: 有哪些相关研究？

现有研究大致可分为三类。方法类中，Reprogramming 将时间序列转为文本兼容表示并由部分微调的 LLM 处理，PromptCast 把预测建模为自然语言补全，TEMPO 对趋势、季节与残差分量做提示表示，CALF 与 TimeCMA 通过微调实现语义嵌入与时序特征对齐；这些方法多把 LLM 当作数值预测器，限制了其比较推理能力。CTRL 则让 LLM 诊断误差并生成控制信号，把数值计算交给专用解码器。应用类中，引入外生文本信息的研究依赖固定表示，难以适应动态时序；FPT 表明冻结 GPT-2 仅调位置嵌入即可有竞争力，LLMTime 将预测视为下一 token 预测实现零样本预测，但它们主要用 LLM 做模式映射，未激活推理。评测与适应类中，ResCAL 利用自相关预测误差但需单独训练估计模块，TENT、SAR 等基于梯度的测试时适应需更新参数，评估协议也不同；CTRL 则无需梯度与参数更新，仅凭输入统计检测分布偏移，并通过 LLM 推理调整策略。

### Q3: 论文如何解决这个问题？

CTRL 的核心思路是将“语义推理”与“数值预测”解耦，让 LLM 只做擅长的事——诊断误差、生成控制策略，而把精确数值计算交给专门的模块。整体框架分三阶段。

第一阶段是控制信号生成。给定冻结的骨干模型（如 DLinear 或 PatchTST）产生的初始预测，CTRL 用 STL 将预测与真值分解为趋势、季节、不规则三个分量，分别交给三个 LLM 智能体分析。趋势智能体关注低频方向与系统性偏差，季节智能体诊断振幅衰减与相位错位，不规则智能体评估高频噪声。每个数值智能体输出紧凑的四维控制向量 [scale, bias, gate, confidence]，不规则智能体则输出自然语言分析并经冻结 GPT-2 投影为嵌入。为增强推理的接地性，智能体接收全局统计、基于 TypiClust 检索的 16 个相似样本（含真实误差），以及当前样本的 STL 对比。整个过程无需微调 LLM，仅需 3 次调用。

第二阶段训练残差解码器。这是唯一通过梯度下降更新的组件，仅约 400K 参数。它保持分量分离，用三个并行 MLP 分别处理趋势、季节、不规则分量，输入为对应分量与拼接后的控制信号，输出修正量并按权重融合，最小化修正后预测与真值的误差。

第三阶段是测试时自适应。CTRL 仅凭输入统计量检测分布漂移，当 STL 统计的 z-score 超过阈值时，通过缓存机制仅用 3-24 次 LLM 调用重新调整控制信号，无需任何真值标签。

创新点在于：将 LLM 定位为控制器而非预测器，输出有界、语义明确；通过 STL 分解实现结构化误差归因；架构上隔离预训练数据，杜绝泄漏；轻量解码器与免标签自适应兼顾鲁棒性与效率。

### Q4: 论文做了哪些实验？

论文在七个多变量基准数据集上进行了实验：ETTh1、ETTh2、ETTm1、ETTm2、Electricity、Weather和Exchange。预测长度H∈{48,96,192,336,720}，输入长度384；Exchange数据集使用H∈{24,48,96,192,336}。CTRL采用DLinear和PatchTST两种骨干架构，残差解码器为2层MLP，使用Llama 3.3 70B生成控制信号，结果取3个种子平均。

对比方法包括骨干基线、LLM-based方法（如TEMPO、CALF、LLMTime、GPT4TS）。主要结果：CTRL在多数数据集-预测长度组合上取得最佳或竞争性性能，提升幅度与训练-测试分布差距相关。ETTh2和ETTm2提升最强，MSE最多降低12%。Exchange上所有预测长度均优于骨干。ECL高维数据上PatchTST在96-336长度最佳。ETTh1和ETTm1提升最多2.5%。Weather上CALF在中程预测优于CTRL。相比LLMTime，CTRL在ETTm2和Weather上MSE降低19.6%-44.3%，MAE降低53.2%-74.2%，且仅需3-24次LLM调用，而LLMTime需N次。消融实验验证了各组件贡献：移除STL上下文、随机控制信号、单Agent等均导致性能下降。CTRL仅需约400K可训练参数，训练时间不到2分钟。

### Q5: 有什么可以进一步探索的点？

CTRL 的主要局限在于长预测视野下骨干误差累积，导致残差修正的不确定性上升，控制信号难以稳定带来增益；同时在高度平稳数据上提升有限，说明其自适应机制的价值主要体现在非平稳与分布漂移场景。未来可探索的方向包括：一是将 CTRL 作为后处理层接入 TimesFM 等大规模基础模型，验证跨模型泛化性；二是设计更鲁棒的多步控制信号，例如引入不确定性感知的残差解码或分层控制，缓解长视野误差放大；三是降低对 LLM 调用的依赖，通过蒸馏或小型控制器实现更低成本的自适应；四是扩展到多变量、概率预测与在线持续学习场景，并系统评估分布漂移检测的敏感性与误报代价。

### Q6: 总结一下论文的主要内容

CTRL 针对现有 LLM 时间序列预测方法的不足——要么将 LLM 降级为数值预测器而浪费其推理能力，要么让 LLM 直接生成预测导致非平稳场景下预测不稳定——提出了一种解耦语义推理与定量预测的框架。其核心思路是：由冻结的骨干模型生成基础预测，专门的 LLM 智能体充当控制器，通过分解趋势、季节和不规则成分来分析骨干预测误差，将推理建立在可解释的时间结构上；每个智能体输出紧凑的控制信号，再由轻量级残差解码器转化为预测修正。CTRL 还引入无标签的测试时自适应机制，仅凭输入统计量检测分布偏移，并通过缓存以 3–24 次 LLM 调用重新调整控制信号。实验表明，CTRL 在非平稳数据集上提升最显著，同时在高度平稳序列上仍具竞争力，可作为应对不可预测分布偏移且无标签场景的实用插件。
