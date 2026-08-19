---
title: "Too Sure to Be Safe: Model Calibration for Reliable Log Anomaly Detection"
authors:
  - "Bin Li"
  - "Dongdong Wang"
  - "Siyang Lu"
date: "2026-08-18"
arxiv_id: "2608.17965"
arxiv_url: "https://arxiv.org/abs/2608.17965"
pdf_url: "https://arxiv.org/pdf/2608.17965v1"
categories:
  - "cs.LG"
  - "cs.AI"
  - "cs.SE"
tags:
  - "log anomaly detection"
  - "model calibration"
  - "confidence estimation"
  - "language models"
  - "reliability"
  - "post-hoc framework"
  - "class imbalance"
  - "overconfidence"
relevance_score: 6.5
---

# Too Sure to Be Safe: Model Calibration for Reliable Log Anomaly Detection

## 原始摘要

Online log anomaly detection is critical for maintaining the reliability of large-scale computing systems. Although recent language model-based log anomaly detectors achieve strong detection performance, their confidence estimates remain poorly calibrated. We show that these detectors frequently assign excessive confidence to incorrect predictions, particularly for anomalous logs under severe class imbalance. Moreover, confidence on erroneous predictions remains persistently high even when conventional calibration metrics indicate good calibration, creating a critical reliability gap for operational monitoring systems. To address this issue, we propose Log Reconstruction and Distance (LoRD), a lightweight post-hoc calibration framework for reliable log anomaly detection. LoRD learns prediction-route-specific reliability models from latent representations of correctly classified validation samples and estimates prediction reliability through route-wise reconstruction distances. Based on the estimated reliability, LoRD selectively recalibrates high-risk predictions to suppress overconfident errors while preserving reliable predictions. Extensive experiments on four large-scale log benchmark datasets and multiple language model-based detectors demonstrate that LoRD consistently improves confidence reliability and substantially reduces overconfident anomaly-related errors without sacrificing anomaly detection performance.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在线日志异常检测对大规模系统可靠性至关重要，但现有基于语言模型的检测器虽在准确率上表现优异，其置信度估计却严重失准。研究发现，这些检测器常对错误预测赋予过高置信度，尤其在类别极度不平衡时，异常日志的误判更易被高置信度掩盖。更关键的是，即便传统校准指标（如ECE）显示校准良好，错误预测的置信度仍持续偏高，形成被现有指标忽视的“可靠性鸿沟”。本文核心问题是：如何在保持检测性能的前提下，抑制高置信度的假阴性（异常被误判为正常），同时不削弱可靠的异常告警。为此，作者提出LoRD框架，利用检测器隐层表示，按预测类别分路由训练自编码器，以重构距离作为可靠性信号，对高风险预测选择性重校准，从而在任务导向的校准权衡中显著降低过度自信的错误，提升异常样本的置信度可靠性。

### Q2: 有哪些相关研究？

相关研究主要围绕三个方向展开。**方法类**方面，半监督方法如DeepLog利用LSTM建模正常日志序列，LogAnomaly引入模板语义表示，PLELog通过概率标签减少人工标注；监督方法如基于TextCNN的多粒度卷积模型、LogRobust的注意力循环网络、LightLog的PCA降维与轻量时序卷积，以及NeuralLog和LogLLM等基于预训练语言模型的方法。**应用类**方面，近期工作探索了GPT-2等大模型在日志异常检测中的直接应用。**评测类**方面，模型校准研究分为三类：基于正则化的训练方法（标签平滑、焦点损失等）、不确定性估计方法（MC Dropout、深度集成）和后处理校准方法（温度缩放、Beta缩放等）。

本文与上述工作的核心区别在于：现有日志异常检测方法聚焦于提升检测准确率，却忽视了置信度校准问题；而现有校准方法多针对通用分类任务，未考虑日志异常检测中严重的类别不平衡和异常样本高置信度误判现象。本文首次系统揭示了大模型日志检测器在异常类上的过度自信问题，并提出LoRD这一轻量级后处理框架，通过预测路径特定的重建距离估计可靠性，在不重训练检测器、不牺牲检测性能的前提下，针对性抑制高风险预测的过度自信错误。

### Q3: 论文如何解决这个问题？

LoRD通过一个轻量级的后处理校准框架解决日志异常检测中过度自信错误预测的问题。其核心思想是利用潜在表示来估计预测可靠性，而非直接调整概率分布。

整体框架包含三个主要模块：**路由特定重建建模**、**非对称阈值与边界选择**、以及**选择性置信度调整**。首先，LoRD观察到正常和异常预测的可靠样本在潜在空间中遵循不同的分布，因此为每个预测路由（正常/异常）分别训练一个自编码器（编码器-解码器网络），仅使用该路由下正确分类样本的隐藏表示进行训练。对于每个测试样本，计算其隐藏表示与对应路由自编码器重建结果之间的欧氏距离平方，作为可靠性距离——距离越小表示样本越符合该路由的可靠流形。

其次，LoRD为每个路由学习两个阈值（τ₁ < τ₂），将样本划分为低、中、高三个可靠性区域。阈值通过验证集上的目标召回率（R_r）和标记率（ρ_r）非对称选择：正常路由优先覆盖假阴性，异常路由优先保留可靠警报。中间区域被视为不确定区域，采用拒绝选项保持原始置信度不变。

最后，校准策略根据路由和区域组合执行不同操作：正常低距离区域直接赋置信度为1（HardAssign），正常高距离区域通过SoftPull将置信度拉向0.5+ε；异常低距离区域SoftPull向1靠拢，异常高距离区域HardAssign设为0.5+ε。SoftPull的调整强度由样本到最近校准边界的距离决定，边界附近样本仅轻微调整，远离边界的样本被更强地拉向目标值。整个框架保持标签不变，仅调整置信度分数，从而有效抑制过度自信的错误预测，同时不损害检测性能。

### Q4: 论文做了哪些实验？

论文在四个大规模超算日志数据集（BGL、Spirit、Liberty、Thunderbird）上评估了LoRD框架，异常比例覆盖0.49%至32.01%。数据划分采用7:0.5:0.5:2的时间顺序切分（训练/检测验证/选择器验证/测试），其中BGL使用470万条日志，Spirit和Liberty各500万条，Thunderbird使用1000万条。实验对比了五种监督日志异常检测器：TextCNN、LogRobust、LightLog、NeuralLog和GPT2，均在滑动窗口（历史长度10，步长1）下以日志序列级别评估。

主要对比方法包括未校准基线（Uncal）、温度缩放（TempS）、对数缩放（LogS）、Beta缩放（BetaS）、选择性校准（SeleS）和集成方法（Ens.）。核心指标为异常检测的置信度误差（CoE），越低越好。结果显示LoRD在所有数据集和检测器组合上均取得最佳或次佳性能，例如在BGL上，LoRD将TextCNN的CoE从0.977降至0.540，将GPT2从0.998降至0.566；在Spirit和Liberty上多数组合CoE降至0.50-0.60区间，显著优于所有基线。

消融实验验证了LoRD各组件的贡献：移除拒绝区域（w/o Reject）或SoftPull校准（w/o Soft）均导致校准质量下降（D值升高、C值降低），完整LoRD在LogRobust和NeuralLog上均取得最优的异常样本置信度（Abn. CoC）和最低的异常错误置信度（Abn. CoE），同时保持正常样本校准性能。

### Q5: 有什么可以进一步探索的点？

LoRD的局限性与未来探索可从以下几方面展开：首先，其依赖验证集选择阈值和策略参数，在动态日志分布或跨系统迁移时可能失效，可探索自适应阈值或在线校准机制。其次，当前仅利用隐藏表示的重构距离，未充分挖掘时序依赖和语义信息，可引入对比学习或扩散模型增强流形建模。第三，校准策略对异常类高置信度预测直接压至0.5附近，可能过度抑制真实异常，可设计基于不确定性感知的软约束或贝叶斯置信区间。此外，LoRD假设正常与异常流形可分，在概念漂移或新型异常出现时可能误判，可结合持续学习或开放集识别。最后，当前仅校准置信度而不改变标签，未来可探索将可靠性估计融入决策阈值调整或主动学习采样，以提升端到端运维效率。

### Q6: 总结一下论文的主要内容

本文聚焦于基于语言模型的日志异常检测中的置信度校准问题。研究发现，尽管现有检测器在基准测试中表现优异，但其置信度估计严重失准，常对错误预测（尤其是异常日志被误判为正常）赋予过高置信度，且传统校准指标无法揭示这一风险。为此，作者提出LoRD框架，一种轻量级后处理校准方法。LoRD根据检测器输出标签构建两条预测路径，利用自编码器对正确分类样本的隐表示进行重构，以重构距离作为可靠性信号，并针对高风险预测进行选择性重校准，以抑制过度自信的错误，同时保留可靠预测。在四个大规模日志基准数据集和多种检测器上的实验表明，LoRD能持续提升置信度可靠性，显著减少过度自信的异常相关错误，且不牺牲检测性能。该工作首次系统研究了日志异常检测中的置信度校准问题，为构建可靠运维监控系统提供了重要思路。
