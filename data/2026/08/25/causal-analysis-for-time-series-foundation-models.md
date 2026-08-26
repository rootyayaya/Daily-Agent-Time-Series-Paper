---
title: "Causal Analysis for Time Series Foundation Models"
authors:
  - "Mathis Jander"
  - "Wouter van Heeswijk"
  - "Martijn Mes"
date: "2026-08-25"
arxiv_id: "2608.24303"
arxiv_url: "https://arxiv.org/abs/2608.24303"
pdf_url: "https://arxiv.org/pdf/2608.24303v1"
categories:
  - "cs.LG"
tags:
  - "Time Series Foundation Models"
  - "Causal Analysis"
  - "Model Bias"
  - "Failure Mode"
  - "Synthetic Data"
  - "Model Validation"
  - "Chronos-2"
  - "TimesFM-2.5"
relevance_score: 6.5
---

# Causal Analysis for Time Series Foundation Models

## 原始摘要

Transitioning from bespoke time series models towards time series foundation models changes the relationship of model and application from one-to-one to one-to-many. This shift introduces concentration risk as many, potentially high-risk, forecasting applications are exposed to the same biases and failure modes of a single time series foundation model. At the same time, this centralization allows for economies of scale in model development and validation. In this study we investigate how biases and failure modes of time series foundation models can be identified before deployment. We propose a causal analysis framework to investigate the ability of a time series foundation model to preserve time series patterns. To achieve this, we intervene on parameterized synthetic time series generators and measure the corresponding change in model output under ceteris paribus conditions. We apply our causal analysis framework to Chronos-2 and TimesFM-2.5 and test them across six distinct time series patterns. We find safe configurations for trend and harmonic oscillation patterns. The results also indicate a bias in both models towards overestimating persistence, sudden failures for both models against the regime switch pattern and failure for TimesFM-2.5 against the energy-release pattern. Our review of the original works for both models indicates that the findings might be explained by the data used for pretraining. We conclude our study with suggestions for further model development, recommendations for application-specific model selection, and a discussion of limitations and further research directions.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着时间序列基础模型（如Chronos-2和TimesFM-2.5）的兴起，预测模型的开发与部署从“一对一”的定制模式转向“一对多”的通用模式。这种转变虽然带来了规模经济，却也引入了新的风险：由于大量下游应用共享同一模型，模型的偏差和失效模式可能被集中放大，影响范围远超传统定制模型。然而，现有研究缺乏系统性的方法，在模型部署前识别这些潜在问题。本文旨在解决这一核心问题：如何通过因果分析框架，在部署前识别时间序列基础模型在保留时间序列模式方面的偏差与失效模式。具体而言，作者通过对参数化的合成时间序列生成器进行干预，并在其他条件不变的情况下测量模型输出的变化，从而评估模型对六种不同时间序列模式的响应。该研究不仅填补了基础模型可解释性与安全性评估的空白，还为下游应用中的模型选择提供了实证依据。

### Q2: 有哪些相关研究？

相关研究主要分为以下几类：

**模型基准评测类**：Chronos-2和TimesFM-2.5的原始研究通过Monash、Darts等基准数据集与其他模型进行预测精度对比。本文指出这类评测类似“体内测试”，无法隔离具体因素（如训练数据、架构）对性能差异的因果贡献，也难以判断结论对未来数据的适用性。

**时间序列因果推断类**：已有工作如Granger因果和Pearl结构因果模型，旨在从时间序列数据中推断变量间的因果关系，但本文强调这些方法用于发现数据中的因果机制，而非评估模型行为，因此对“干预数据生成过程以测试模型”这一目标尚属空白。

**可解释AI类**：SHAP、LIME和部分依赖图（PDP）等方法可量化输入与输出的关系，其中PDP通过改变特征值观察输出变化，与本文的干预思路相近。但本文指出这些方法针对表格数据设计，对时间序列而言，干预应作用于数据生成过程的模式（如趋势、季节性），而非已实现的样本值。

**鲁棒性分析类**：相关研究分为输入损坏（噪声、对抗攻击）和分布偏移两类。本文认为这些方法修改观测值而非控制生成过程，无法揭示模型在未损坏样本上的固有偏差；且对时间序列基础模型而言，训练分布的定义本身就很模糊。

综上，本文填补了方法论空白：借鉴药理和汽车工程的分阶段测试范式，提出在“体外”条件下对参数化生成器进行因果干预，以识别时间序列基础模型的偏差与失效模式。

### Q3: 论文如何解决这个问题？

该论文提出了一种基于因果分析的框架，用于在部署前系统性地识别时间序列基础模型的偏差和失效模式。核心思路是将参数化生成器、基础模型和因果推断逻辑形式化，构建从生成器参数到模型输出的有向无环图（θ → y → M(y)），并利用Pearl的do算子对目标参数进行干预，同时保持其他参数和噪声序列不变，从而在严格“其他条件相同”（ceteris paribus）的条件下，隔离单一参数变化对模型输出的因果效应。

整体框架包含三个主要模块：**参数化生成器**（如随机游走、AR(1)、谐波振荡器等六种模式）、**待测基础模型**（Chronos-2和TimesFM-2.5），以及**参数统计量**（如均值、自回归系数、FFT主频等）。通过干预参数（剂量）并测量输入输出轨迹的统计量变化（响应），建立剂量-响应关系，从而量化模型对特定时间序列模式的保真度。

关键技术包括：对每个生成器设置特定的干预扫描范围（如AR(1)的β从-0.5到0.98），使用50次独立噪声实现来确保统计可靠性，并采用专门的统计工具（如statsmodels、scipy.signal.welch、ruptures.Pelt、fbm和hurst库）估计响应指标。创新点在于：将因果干预思想引入时间序列基础模型评估，能够区分模型输出变化是源于参数真实变化还是模型自身的系统性偏差，从而识别出模型在趋势、谐波、机制转换等模式上的安全配置和失效边界。该方法还通过对比预训练数据分布，为模型偏差提供了可解释性归因。

### Q4: 论文做了哪些实验？

实验基于参数化合成时间序列生成器，对Chronos-2和TimesFM-2.5两个基础模型进行因果干预分析。实验设置6种时间序列模式（随机游走、AR(1)过程、谐波振荡、机制切换、能量释放、分数布朗运动），每种模式设置6个干预值，每个干预值使用50个噪声实现（n=50），共300个样本/模型。对比方法为模型输出与真实轨迹的参数统计量δ(y)分布及散点一致性。

主要结果：(1) 随机游走：两模型均平滑噪声，Chronos-2漂移参数保持优于TimesFM-2.5；(2) AR(1)：两模型均高估一阶自相关（0<β<0.85时），存在持续性偏差；(3) 谐波振荡：两模型完美保持波长，仅振幅有微小变化；(4) 机制切换：Chronos-2在τ≥50、TimesFM-2.5在τ≥25时失效，前者低估τ而后者高估；(5) 能量释放：Chronos-2全程保持阈值模式，TimesFM-2.5在κ≥25时开始平滑，κ≥50时完全丢失；(6) 分数布朗运动：两模型均高估Hurst指数（H<0.5时平滑化），Chronos-2偏差略小。整体上，两模型在趋势和周期模式上安全，但存在持续性高估偏差及特定模式失效问题。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从以下几方面展开：首先，当前因果分析框架仅针对六种时间序列模式，且使用参数化合成数据，缺乏对真实世界复杂动态（如多模式耦合、非平稳性）的覆盖，未来可扩展至更丰富的模式库与真实数据集验证，以增强结论的生态效度。其次，干预分析仅关注模型输出变化，未深入模型内部表征或注意力机制，后续可结合可解释性工具（如归因分析、激活模式探测）揭示偏差的神经机制。再者，训练数据偏差的推断仅基于文献回顾，缺乏对预训练数据分布的量化控制，建议开发可控的合成预训练策略，系统评估数据多样性对失败模式的影响。此外，当前研究聚焦单变量预测，多变量与长时程预测的因果鲁棒性尚待探索。最后，可设计自适应模型选择框架，将模式识别与因果边界检测结合，为高风险应用提供动态安全评估，并探索在线干预或微调机制以缓解已识别的系统性偏差。

### Q6: 总结一下论文的主要内容

本文针对时间序列基础模型从“一对一”定制模式转向“一对多”通用模式所引发的集中风险，提出了一种因果分析框架，用于在部署前识别模型的偏差与失效模式。该框架通过对参数化合成时间序列生成器进行干预，并在其余条件不变的情况下测量模型输出的变化，从而评估模型对时间序列模式的保持能力。作者将该框架应用于Chronos-2和TimesFM-2.5，测试了六种不同的时间序列模式。研究发现：两种模型均存在高估持续性的偏差；在机制切换模式上出现突然失效；TimesFM-2.5在能量释放模式上表现失败。这些发现可能与预训练数据有关。研究为下游应用的模型选择及未来模型开发提供了建议，并讨论了局限性与未来方向，具有重要的实践指导意义。
