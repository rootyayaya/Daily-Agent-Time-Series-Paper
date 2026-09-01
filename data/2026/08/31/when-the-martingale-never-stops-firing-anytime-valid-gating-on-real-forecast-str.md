---
title: "When the Martingale Never Stops Firing: Anytime-Valid Gating on Real Forecast Streams"
authors:
  - "Weijia Han"
  - "Lisha Qu"
date: "2026-08-31"
arxiv_id: "2608.30502"
arxiv_url: "https://arxiv.org/abs/2608.30502"
pdf_url: "https://arxiv.org/pdf/2608.30502v1"
categories:
  - "cs.LG"
  - "stat.ME"
  - "stat.ML"
tags:
  - "Anytime-valid inference"
  - "Conformal test martingales"
  - "Time series foundation models"
  - "Online monitoring"
  - "Gating mechanism"
  - "Kalman filter"
  - "Forecast streams"
  - "Change detection"
  - "Dependent data"
  - "Null-calibration"
relevance_score: 7.5
---

# When the Martingale Never Stops Firing: Anytime-Valid Gating on Real Forecast Streams

## 原始摘要

Machine learning systems are increasingly corrected while they run, and the decision of when to intervene is increasingly delegated to statistical monitors. Anytime-valid inference promises evidence that can be acted on at any moment, exactly the guarantee this setting needs, and it is moving from theory into deployed monitoring. Conformal test martingales are the change-detection instrument, and Ville's inequality caps their false-alarm probability on exchangeable data. The guarantee is conditional. A deployment inherits it only if the stream it monitors behaves exchangeably. The premise is hardest to satisfy where these monitors are most useful, on dependent data and inside loops where the monitor modifies the learner whose scores it reads. It is also rarely measured. We measure it in a pre-specified case study, where such a monitor gates the online updates of a Kalman adapter correcting frozen time-series foundation models on five forecasting streams. On exchangeable synthetic streams, the same implementation fires in at most 1 of 60 runs. On the real streams, at alpha = 0.05, 135 of 135 clean-stream runs fired. The construction does not explain the firing; the failure comes from the deployed score stream itself. Repeated fires hold the gate's drift response active, and the gated filter amplifies the very transient it was designed to prevent. The component worth keeping makes no validity claim. Huber-style gating of the filter's own updates cuts isolated-spike degradation by an order of magnitude with no dataset specific tuning. Anytime-valid methods proposed for dependent data should therefore be accompanied by null-calibration controls and mechanism traces.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于在线机器学习系统中统计监控器的可靠性问题。研究背景是，随着系统运行中不断被修正，何时干预的决策日益交由统计监控器处理，而“任意有效推断”理论承诺可在任意时刻提供可行动的证据，正从理论走向实际部署，其中共形检验鞅是核心的变点检测工具。

现有方法的不足在于，Ville不等式保证的误报率控制依赖于一个关键前提——被监控的分数流具有可交换性。然而，这一前提在监控器最有用之处（依赖数据、监控器反馈修改学习器的闭环系统）最难满足，且极少被实证检验。

本文要解决的核心问题是：在真实预测流上，这种任意有效门控机制是否真的能兑现其理论保证？通过一个预先指定的案例研究（用鞅门控控制卡尔曼适配器对五个预测流上的冻结时间序列基础模型进行在线修正），作者发现：在可交换的合成流上，实现最多60次运行中触发1次；但在真实流上，α=0.05时135次干净流运行全部触发。这证明失败源于部署的分数流本身，而非构造缺陷，且反复触发会放大本应防止的瞬态。因此，论文强调对依赖数据提出的任意有效方法必须配套零校准控制和机制追踪。

### Q2: 有哪些相关研究？

相关研究主要围绕三个方向展开。**方法类**中，核心是Ville提出的不等式与conformal test martingales，它们为任意时点有效推断提供理论保证，但前提是数据可交换；本文直接检验了这一前提在真实流上的失效。**应用类**方面，已有工作将此类监控器用于在线学习系统的干预决策，如模型漂移检测和自适应更新门控，但多假设流独立或可交换；本文则将其嵌入Kalman适配器，门控冻结的时间序列基础模型，暴露了依赖数据下的脆弱性。**评测类**研究通常侧重合成数据上的错误发现率控制，鲜有在真实流上系统校准；本文通过预注册的案例研究，在5个预测流上对比了合成与真实流的触发率差异，并引入Huber风格门控作为无有效性声明的稳健替代。与这些工作的区别在于：本文不提出新理论，而是实证揭示部署条件不满足时，任意时延有效监控会系统性过触发，并强调需补充零校准控制与机制追踪，而非仅依赖理论保证。

### Q3: 论文如何解决这个问题？

论文通过一个预先设定的案例研究，系统性地揭示了“任意时刻有效推断”（anytime-valid inference）在真实预测流上的前提失效问题，并提出了归因与缓解策略。核心方法包括三个对照臂：完整门控（full gate）、仅Huber门控（Huber-only）和SGD替代驱动（SGD surrogate），以隔离门控各组件的贡献。

整体框架围绕一个门控在线更新机制展开：用符合测试鞅（conformal test martingale）监控冻结时间序列基础模型的预测残差，当鞅超过阈值时触发门控，调整卡尔曼适配器的过程噪声（Q-boost）和遗忘因子。主要模块包括：滑动校准窗口（替代经典协议中的增长袋）、自适应学习的得分流$S_t$、以及触发后重置逻辑。

关键技术发现是：在可交换合成流上，实现仅在60次运行中最多触发1次；但在真实流上，135次干净运行全部触发（$\alpha=0.05$），且SGD替代驱动也全部触发，说明问题不在滤波器得分本身。通过零假设控制（预填充窗口、随机p值、混合和重置逻辑）证明实现本身在可交换输入下保持静默，因此失败源于部署得分流破坏了可交换性前提。

创新点在于：第一，首次量化了真实流上鞅监控的前提失败率；第二，通过机制追踪（mechanism traces）定位到门控的反馈放大效应——重复触发使Q-boost持续保持8-10倍，在天气瞬变事件中放大单步MSE达12倍；第三，提出保留Huber式门控（仅对滤波器自身更新进行鲁棒化）而不做有效性声明，可将孤立尖峰退化降低一个数量级且无需数据集调参。论文强调，针对依赖数据提出的任意时刻有效方法必须附带零假设校准控制和机制追踪。

### Q4: 论文做了哪些实验？

论文围绕“门控机制在真实预测流上的有效性”展开实验，核心是验证基于共形检验鞅的门控在可交换合成数据与真实流上的差异，并剖析组件贡献。

**实验设置**：采用预注册案例研究，用门控控制卡尔曼适配器对冻结时间序列基础模型的在线更新，监测五个预测流（ETTh2、traffic、ETTm1、electricity、weather）。对比方法包括无门控卡尔曼滤波（ungated KF）、仅Huber稳健更新（Huber-only）、完整门控（full gate）、无门控SGD及SGD代理变体。

**主要结果**：在可交换合成流上，门控在60次运行中最多触发1次；但在真实流上，α=0.05时135次干净运行全部触发，表明门控失效源于真实分数流本身。隔离尖峰污染（5%步长，6稳健σ）下，Huber-only将退化从无门控KF的+3.32（ETTh2）降至+0.15，且优于完整门控（+0.24）；在traffic上Huber-only为+0.11 vs 完整门控+0.35。SGD代理在ETTh2和ETTm1上有效，但traffic上劣于无门控SGD。持续污染和水平漂移下所有门控均失效，完整门控在漂移下退化+7.8至+19.3，且合成分段漂移中门控适应更慢。结论：Huber式门控无需有效性声明即可将尖峰退化降低一个数量级，而完整门控的漂移响应反而放大瞬态。

### Q5: 有什么可以进一步探索的点？

论文的核心局限在于：任何“任意有效”的保证都依赖于数据可交换性这一前提，而真实部署流（尤其是受监控系统自身反馈影响的闭环流）几乎必然违反该前提。作者已证明，在135条真实干净流上，所有运行均触发警报，说明该前提失效并非罕见异常，而是常态。因此，未来最关键的探索方向是**开发“前提鲁棒”的监控器**——即不再将可交换性视为既定条件，而是将其作为可在线检验的假设，并设计在前提轻微违反时仍能控制误报率的机制。

其次，论文揭示了“检测-响应”闭环中的危险耦合：门控信号激活的漂移响应反而放大了瞬态扰动。未来应研究**解耦设计**，例如将检测模块与响应策略分离，或为响应策略引入独立的成本约束（如Huber式鲁棒更新），确保即使检测误报，其下游影响也有界。此外，可探索**自适应校准**方法，使监控器在非平稳流上动态调整阈值，而非依赖固定alpha值。

最后，论文强调“机制追踪”与“零校准对照”的必要性，这提示未来工作应建立标准化评估协议，要求任何新方法必须报告其在真实依赖流上的空分布表现及失败模式，而非仅展示合成数据上的理论保证。

### Q6: 总结一下论文的主要内容

本文针对在线部署中“任意时刻有效”的符合检验鞅门控机制进行了实证研究。问题定义上，作者在五个真实预测流上，用该门控机制调节冻结时序基础模型的卡尔曼适配器更新，检验其可交换性前提是否成立。方法上，采用滑动窗口的随机化符合p值与简单混合鞅，并预设了完整协议。主要结论是：在可交换合成流上实现几乎不误报，但在真实干净流上135次运行全部触发警报，前提失效源于部署的得分流本身，而非构造缺陷。更严重的是，重复触发激活漂移响应，放大了天气流上的瞬态异常，导致性能下降达一个数量级。消融实验表明，仅保留Huber式鲁棒更新能有效抑制尖峰退化，而鞅触发的漂移响应反而有害。论文强调，针对依赖数据的任意时刻有效方法应配套零校准控制与机制追踪，并区分有保证与无保证组件。
