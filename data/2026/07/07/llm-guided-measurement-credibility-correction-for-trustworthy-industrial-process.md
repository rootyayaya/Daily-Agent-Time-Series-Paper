---
title: "LLM-Guided Measurement Credibility Correction for Trustworthy Industrial Process Inference"
authors:
  - "Youcheng Zong"
  - "Runda Jia"
  - "Dakuo He"
date: "2026-07-07"
arxiv_id: "2607.06111"
arxiv_url: "https://arxiv.org/abs/2607.06111"
pdf_url: "https://arxiv.org/pdf/2607.06111v1"
categories:
  - "eess.SY"
  - "cs.AI"
tags:
  - "LLM-Guided Measurement Credibility Correction"
  - "工业过程推理"
  - "测量语义"
  - "可信度校正"
  - "软测量"
  - "预测"
  - "文档语义"
  - "轻量级"
  - "预推理校正"
  - "工业传感器解释"
relevance_score: 9.2
---

# LLM-Guided Measurement Credibility Correction for Trustworthy Industrial Process Inference

## 原始摘要

Industrial prediction and soft sensing depend on credible input measurements. In field deployment, a predictor may receive biased, delayed, stale, or derived measurements that still look plausible. Prediction can then fail before the forecasting backbone becomes the main limitation, because the input window no longer represents the real process. Sensor reconstruction, data reconciliation, and fault-tolerant soft sensing reduce this risk, but they often rely on numerical correlation, alarms, fault labels, or explicit process equations. These assumptions are not always available. A correlated variable can also be an unsafe reference when variables share instruments, derived formulas, soft-sensing chains, or control actions. The key issue is to decide before prediction which external measurements can credibly support the current measurement. To address this issue, this article proposes LLM-Guided Measurement Credibility Correction (MCC). MCC converts measurement meanings in process documents into measurement semantics usable by numerical models. It builds independent process references from semantically qualified external measurements and corrects local measurement conflicts before prediction. The predictor therefore receives a more credible input window. Across multiple complex industrial forecasting and soft-sensing tasks, +MCC achieves average relative MAE reductions of 30.7% on real-test protocols and 80.3% on controlled-corruption protocols. It adds only 0.5--2.0k online parameters, with the slowest +MCC inference time at 0.089 ms/step. These results show that measurement semantics can turn process documents into lightweight pre-inference credibility correction and improve prediction accuracy.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在工业过程预测与软测量中，输入测量的可信度是决定模型性能的关键。然而，现场部署中，传感器漂移、温度滞后、上游仪器误差、派生计算或采样延迟等会导致测量值看似正常却已失真，而传统预测模型无法识别此类隐蔽错误。现有方法如传感器重构、数据调和及容错软测量，通常依赖数值相关性、报警信号、故障标签或显式过程方程，但这些假设在工业现场往往难以满足。更关键的是，数值相关的变量可能因共享仪器、派生公式、软测量链或控制动作而共同失真，此时相关变量并非可靠参考。因此，核心问题在于：如何在预测前判断哪些外部测量值能为当前测量提供可信的支撑证据？本文提出LLM引导的测量可信度校正（MCC），利用大语言模型从过程文档中提取测量语义（如测量方式、单位、过程角色），构建独立的过程参考，在预测前校正局部测量冲突，从而为预测器提供更可信的输入窗口，解决现有方法依赖不可靠数值相关性的根本缺陷。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是工业预测与软测量模型，如循环网络、Transformer及过程图约束的软测量，它们专注于改进模型对测量窗口的利用，但未验证窗口是否真实反映当前过程。本文的MCC在预测前进行输入可信度检查，与这类工作形成互补。第二类是测量验证与故障诊断，包括传感器重构、数据协调、过程故障检测与诊断等。这些方法依赖数值相关性、过程方程或故障标签，而MCC在缺乏这些信息时，通过语义构建独立的外部参考来修正输入。第三类是LLM增强的时间序列与工业应用，如文本增强时间序列、因果表示、零样本诊断等。MCC与这些工作的区别在于，它不将LLM直接嵌入预测循环，而是离线构建测量语义，在线仅执行轻量数值计算，实现高效可信度修正。

### Q3: 论文如何解决这个问题？

论文提出了一种名为LLM引导的测量可信度校正（MCC）方法，用于在工业过程推理前自动识别并修正不可靠的测量值。其核心思想是利用大语言模型（LLM）从过程文档中提取测量语义，构建独立的过程参考，从而在不依赖故障标签或显式方程的情况下实现轻量级可信度校正。

整体框架分为三个有序阶段：离线LLM处理、名义训练与校准、在线校正。主要模块包括：
1. **测量语义提取**：离线阶段，LLM根据过程文档为每个变量生成语义描述，并通过固定文本渲染器和嵌入模型将其转换为冻结的语义方向矩阵U，该矩阵在后续阶段保持不变。
2. **语义感知观测器**：在线阶段，对于每个可校正变量，观测器利用语义矩阵U和可学习的语义权重矩阵Ω_τ，从其他变量的历史测量中构建独立过程参考。通过语义兼容性计算和稀疏路由，确定哪些外部测量值有资格支持目标变量，并聚合得到参考值。
3. **局部不一致性检测与校正**：通过比较当前测量值与独立参考值，计算支持加权的不一致性，并减去背景不一致性以区分真实故障与工况变化。基于校准集上的经验分布，将当前不一致性转换为校正强度，最终通过加权混合得到校正后的测量值。

关键技术包括：语义驱动的变量间路由机制、留一法参考构建、基于校准分布的自适应校正强度计算。创新点在于将LLM的语义理解能力与轻量级数值模型结合，实现了无需在线调用LLM、仅增加0.5-2.0k参数的可信度校正，显著提升了工业预测与软测量的准确性。

### Q4: 论文做了哪些实验？

论文在三个工业过程数据集上进行了实验：钢包预热温度预测、浓密机底流浓度估计和IndPenSim青霉素浓度估计。实验设置采用AdamW优化器，MSE损失函数，最大300轮训练，早停耐心40轮，学习率调度器为ReduceLROnPlateau。对比方法包括GRU、LSTM、Transformer、Informer、Mamba、iTransformer、PatchTST和ModernTCN等8种常见时间序列骨干网络。每个数据集包含两个测试协议：Real Test（原始固定测试集）和Corrupted Test（注入偏差、漂移、增益、尖峰、丢失和全局偏移等6种测量损坏）。主要结果：在24个数据集-骨干网络组合上，+MCC相比Base在Real Test上平均相对MAE降低30.7%，在Corrupted Test上降低80.3%。具体地，在钢包预热数据集上，+MCC在Corrupted Test中将MAE从0.2285降至0.0175（GRU）；在浓密机数据集上，+MCC在Corrupted Test中将MAE从0.0080降至0.0017（GRU）；在IndPenSim数据集上，+MCC在Corrupted Test中将MAE从3.020降至0.823（GRU）。+MCC仅增加0.5-2.0k在线参数，最慢推理时间为0.089 ms/步。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：1）测量语义的构建依赖LLM对过程文档的理解，在文档质量差或变量描述模糊时可能引入噪声；2）观测器仅基于时序相关性选择支持变量，未考虑变量间的因果结构或物理约束；3）修正门采用固定阈值，缺乏对不同程度和类型测量退化的自适应能力；4）仅在三个工业数据集上验证，缺乏对更广泛工业场景（如化工、电力）的泛化性测试。

未来可探索：1）引入因果发现或物理信息网络，使支持变量选择更符合过程机理；2）设计动态修正门，根据测量不确定性或退化程度自适应调整修正强度；3）将MCC与在线学习结合，使观测器能持续适应过程漂移；4）探索多模态语义融合，如将设备维护记录、操作日志与过程文档共同编码；5）研究LLM语义提取的鲁棒性，例如通过对比学习或对抗训练增强对文档噪声的容忍度。

### Q6: 总结一下论文的主要内容

该论文提出了一种名为LLM引导的测量可信度校正（MCC）方法，用于解决工业过程推断中输入测量值不可靠的问题。传统预测模型在面对偏置、延迟或衍生测量值时可能失效，而现有方法依赖数值相关性或过程方程，但相关变量可能因共享仪表或控制回路而不可信。MCC的核心贡献在于利用LLM从过程文档中提取测量语义，构建独立的外部参考，并在预测前校正局部测量冲突。方法包括离线阶段使用LLM生成冻结的测量语义，在线阶段通过数值观察器选择可信外部变量构建过程参考，仅当存在可靠证据时才保守校正。实验表明，MCC在多个复杂工业预测和软测量任务中，平均相对MAE降低30.7%（真实测试）和80.3%（受控污染测试），仅增加0.5-2.0k在线参数，推理时间最慢0.089ms/步。该工作将测量语义转化为轻量级预推断可信度校正，显著提升了预测准确性，具有重要的工业应用价值。
