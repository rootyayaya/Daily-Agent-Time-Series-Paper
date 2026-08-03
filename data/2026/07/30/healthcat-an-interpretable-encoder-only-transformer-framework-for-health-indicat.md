---
title: "HealthCAT: An Interpretable Encoder-only Transformer Framework for Health Indicator Prediction and Temporal Interpretation of Wearable Sensor Data"
authors:
  - "Xiaotong Yu"
  - "Joshua Y. Kim"
  - "HaeJin Lee"
  - "Kalina Yacef"
date: "2026-07-30"
arxiv_id: "2607.27635"
arxiv_url: "https://arxiv.org/abs/2607.27635"
pdf_url: "https://arxiv.org/pdf/2607.27635v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "可解释时间序列分析"
  - "可穿戴传感器"
  - "健康指标预测"
  - "Transformer"
  - "时间步级解释"
  - "注意力机制"
relevance_score: 6.5
---

# HealthCAT: An Interpretable Encoder-only Transformer Framework for Health Indicator Prediction and Temporal Interpretation of Wearable Sensor Data

## 原始摘要

Wearable sensors continuously capture fine-grained multivariate time-series data, providing opportunities to model behavioural patterns associated with health outcomes. However, existing deep learning methods prioritise predictive accuracy over interpretability, limiting their application in health research. In this study, we present HealthCAT, a flexible framework that integrates an Encoder-only Transformer with an Attentive Class Activation Token (AttentiveCAT) to generate class-specific, time-step-level interpretations. These interpretations can be mapped back onto behavioural cycles that are relevant to the domain (e.g., time-of-day), supporting individual-level analysis of wearable sensor data. We evaluated HealthCAT using two real-world wearable sensor datasets (306 participants in total). HealthCAT outperformed deep learning baselines by up to 17\% in F1-score and 12\% in accuracy on both datasets ($p<0.05$). In masking experiments, the time steps identified by HealthCAT carried significantly more predictive value than random selection across all masking conditions ($p<0.05$), indicating that the identified time steps are predictively informative. By coupling predictive performance with validated time-step-level interpretability, HealthCAT moves wearable sensor analysis beyond aggregated metrics towards temporal patterns that support health monitoring, behavioural pattern analysis, and intervention design in health research. The significance of this work is that it enables accurate prediction of health indicators from wearable sensor data while providing insights into when and how physical activity patterns occur, rather than relying solely on aggregated summary measures.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

wearable传感器持续采集细粒度多变量时间序列数据，为建模与健康结局相关的行为模式提供了机会。然而，现有深度学习方法过度侧重预测精度而忽视可解释性，这限制了它们在健康研究中的应用。传统健康研究常将传感器数据降维为聚合指标（如每日步数或总中高强度活动时间），虽作为金标准有价值，却丢失了“何时”与“如何”影响健康结果的时间动态信息。尽管深度学习在可穿戴数据识别任务（如活动识别、睡眠分期）上表现优异，但在健康结局预测中，仅识别活动类型远远不够，还需提供活动发生的时间、强度及时间证据的稳定性，以支撑反馈或干预设计。当前方法缺乏细粒度的时间步级解释，导致聚合特征与时间特征之间存在鸿沟。为此，本文提出HealthCAT框架，集成Encoder-only Transformer与Attentive Class Activation Token，为每个时间步生成类别特定的重要性分数，实现时间步级可解释性，并映射回行为周期（如昼夜节律）支持个体层面分析。核心问题是：如何在保证预测性能的同时，提供经过验证的时间步级解释，使可穿戴数据分析超越聚合指标，揭示健康相关行为的时间模式。

### Q2: 有哪些相关研究？

相关研究主要分为以下几类：

**方法类**：基于深度学习的时序建模方法，包括LSTM、GRU、Transformer及其变体，如DeepSleepNet（CNN+Bi-LSTM用于睡眠分期）、CNN-based心律失常检测、Encoder-only Transformer等。这些方法追求预测精度，但缺乏可解释性。本文HealthCAT采用Encoder-only Transformer架构，但创新性地引入AttentiveCAT机制，实现类别特定的时间步级解释，与上述方法形成本质区别。

**可解释性方法类**：包括自注意力可视化、GradCAM、DeepSHAP、LIME等后验解释工具。这些方法存在局限性：注意力可视化非类别特定且不反映决策边界；GradCAM不适用于序列模型；DeepSHAP计算昂贵且难以定位到具体时间步；LIME无法达到时间步级粒度。HealthCAT通过AttentiveCAT将类别激活与自注意力结合，生成类别特定的时间步重要性分数，克服了这些方法的不足。

**应用类**：可穿戴传感器在健康领域的应用，如人类活动识别、睡眠分期、健康结果筛查等。现有工作多聚焦于信号数据（EEG、ECG、PPG），对可穿戴多变量时序数据关注不足，且缺乏时间粒度的解释。本文针对可穿戴传感器数据，将时间步映射回行为周期（如一天中的时段），支持个体层面分析，填补了这一空白。

**评测类**：现有研究缺乏对时间解释有效性的验证方法。本文通过掩码实验验证识别的时间步具有显著预测价值，为时序解释提供了新的评测范式。

### Q3: 论文如何解决这个问题？

HealthCAT通过一个三阶段框架解决可解释性问题。第一阶段是预处理，将原始可穿戴传感器数据转换为结构化多元时间序列。针对加速度计数据，计算重力扣除后的信号向量幅度（SVMgs）或标准信号向量幅度（SVM），并根据阈值划分活动强度等级（如MVPA、LPA、SED），再按固定时间步长（如小时或分钟）聚合特征，形成统一的时间序列表示。

第二阶段是核心的可解释提取模块。采用Encoder-only Transformer架构，包含L层堆叠编码器，每层使用多头自注意力、前馈网络、残差连接和层归一化。创新点在于引入Attentive Class Activation Token（AttentiveCAT）机制：首先计算每个时间步的Class Activation Token（CAT），即类别logit对该时间步隐藏表示的梯度与隐藏表示的元素级乘积，反映该时间步对分类决策的贡献；然后结合层内多头注意力权重的平均值，得到注意力加权的CAT分数；最后跨层求和并降维，生成每个时间步的类别特定重要性分数。这种方法同时考虑了时间步自身的特征贡献和其与序列中其他时间步的上下文关系。

第三阶段是领域自适应可视化。通过映射函数将时间步索引映射到领域相关的时间位置（如一天中的小时），并定义领域特征函数提取原始数据中的特定特征（如活动强度），再通过分桶函数将特征值分组。最终可视化值是对共享相同时间位置和特征桶的AttentiveCAT分数取平均，正负值分别表示支持或反对目标类别的证据。

该框架的关键创新在于将注意力机制与梯度加权相结合，生成既反映局部特征贡献又包含全局上下文关系的时间步级解释，且能灵活适配不同健康应用场景。

### Q4: 论文做了哪些实验？

论文围绕三个研究问题展开实验。实验设置上，使用两个真实可穿戴传感器数据集（共306名参与者），通过5折网格搜索交叉验证选择超参数，每个数据集进行10次试验。

**RQ1（预测性能）**：对比HealthCAT与Transformer、GRU、LSTM基线。在Physical Activity数据集上，HealthCAT的F1-score达0.822±0.034，准确率0.826±0.027；在DREAMT数据集上F1-score为0.808±0.036，准确率0.843±0.030，均显著优于所有基线（配对t检验，p<0.05），F1-score最高提升17%，准确率提升12%。

**RQ2（时间步级可解释性）**：通过掩码实验验证AttentiveCAT选择的时间步是否比随机选择更具预测信息。在25%、50%、75%三种掩码比例下，HealthCAT的AttentiveCAT选择在12个模型-掩码组合中10个显著优于随机选择（p<0.05），尤其在75%掩码时差异最大，仅用25%最信息时间步仍保持较高F1-score。

**RQ3（行为模式可视化）**：对两名对比参与者（健康体能组和需改进组）进行案例研究，将时间步重要性分数映射回24小时周期，分别可视化MVPA、LPA、SED三种活动强度的时间贡献模式，展示了个体间差异化的行为时间特征。

### Q5: 有什么可以进一步探索的点？

HealthCAT在可解释性与预测性能上取得了平衡，但仍存在若干可探索的深化方向。首先，当前时间步级解释仅映射到“时段”和“强度”维度，未考虑行为序列的上下文依赖（如连续久坐与间歇活动的差异），未来可引入状态转移图或因果推断，解析行为模式间的动态关联。其次，掩码实验中的“75%恢复”现象虽被归因于噪声过滤，但缺乏对模型鲁棒性边界的系统刻画，可设计对抗性扰动或置信度校准实验，验证解释的稳定性。第三，框架依赖预定义时间分辨率（小时/分钟级），对跨个体生理节律差异（如昼夜颠倒者）适应性不足，建议引入自适应时间分段或个性化粒度选择。此外，当前仅验证了分类任务，可扩展至回归型健康指标（如连续血压）预测，并探索多任务学习以共享跨域时序表征。最后，解释评估仍以预测信息量为主，未结合临床专家标注或用户反馈进行实用性验证，未来可开展人机协作研究，检验解释是否真正辅助干预决策。

### Q6: 总结一下论文的主要内容

HealthCAT提出了一种可解释的编码器-only Transformer框架，用于可穿戴传感器数据的健康指标预测与时间级解释。现有深度学习方法侧重预测精度而忽视可解释性，限制了其在健康研究中的应用。该框架通过引入注意力类激活令牌（AttentiveCAT），为每个时间步生成类别特定的重要性分数，并可映射回行为周期（如昼夜节律），支持个体层面分析。研究在两个真实数据集（共306名参与者）上验证，HealthCAT在F1分数上最高提升17%，准确率提升12%，且掩码实验表明其识别的时间步携带显著更高的预测价值。该方法将预测性能与可验证的时间级解释相结合，推动可穿戴数据分析从聚合指标转向时间模式理解，为健康监测、行为分析和干预设计提供依据，是首个提供时间步级解释的此类研究。
