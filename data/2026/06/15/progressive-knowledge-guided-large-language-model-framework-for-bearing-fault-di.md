---
title: "Progressive Knowledge-Guided Large Language Model Framework for Bearing Fault Diagnosis"
authors:
  - "Jinghan Wang"
  - "Gaoliang Peng"
  - "Yanjun Chen"
  - "Wei Zhang"
  - "Wentao Wu"
  - "Tianchen Liu"
date: "2026-06-15"
arxiv_id: "2606.16684"
arxiv_url: "https://arxiv.org/abs/2606.16684"
pdf_url: "https://arxiv.org/pdf/2606.16684v1"
categories:
  - "cs.CL"
tags:
  - "Agentic Time Series"
  - "可解释时间序列分析"
  - "工业故障诊断"
  - "LLM/Agent工作流"
  - "知识引导"
  - "多模态融合"
  - "物理信息特征"
relevance_score: 7.5
---

# Progressive Knowledge-Guided Large Language Model Framework for Bearing Fault Diagnosis

## 原始摘要

Vibration-based bearing fault diagnosis requires resolving three interrelated measurement challenges, including the trade-off between global statistical feature efficiency and local transient signal fidelity, insufficient traceability of measurement features to underlying fault physics, and ineffective multi-source measurement information fusion across diagnostic scales. This paper presents a progressive physics-guided multi-scale vibration signal processing framework that addresses all three challenges within a unified diagnostic pipeline. An 81-dimensional measurement descriptor, derived from bearing kinematic theory and characteristic defect frequencies, establishes a physically traceable feature space enabling real-time fault screening at approximately 20 ms per sample. A fault-adaptive signal segmentation mechanism then directs analytical attention toward fault-relevant waveform regions guided by physics-based priors, without manual feature engineering. Structured fault mechanism knowledge is further encoded implicitly in model parameters during training, enabling autonomous multi-scale measurement fusion without external knowledge dependencies at inference. Validated on four public benchmark datasets under diverse operating conditions, the framework achieves 98.49% diagnostic accuracy with a 12.6-fold reduction in computational cost relative to signal-level baselines. Interpretability analysis confirms that diagnostic feature activations align with established bearing fault mechanics, supporting measurement traceability in safety-critical industrial systems.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文旨在解决基于振动信号的滚动轴承故障诊断中三个相互关联的核心挑战：尺度冲突、知识鸿沟和多尺度融合不足。尺度冲突指全局统计特征（高效但丢失局部瞬态细节）与原始信号处理（保留时间保真度但计算成本高）之间的矛盾。知识鸿沟指纯数据驱动模型缺乏对轴承动力学和故障机制先验的显式编码，导致决策难以追溯至物理原理。多尺度融合不足指独立分阶段流水线缺乏信息流交互，限制了诊断精度和可解释性。论文提出一个渐进式物理引导的多尺度振动信号处理框架，在一个统一诊断流水线中同时解决这三个挑战，旨在实现高精度、可解释且计算高效的工业在线故障诊断，同时满足安全关键系统的可追溯性要求。

### Q2: 有哪些相关研究？

相关工作分为三代。第一代方法结合手工谱特征与浅层分类器（如SVM、随机森林），基于FFT、小波分解等信号处理技术，物理可解释且计算高效，但需大量领域知识且对工况变化敏感。第二代引入深度学习架构（CNN、RNN、LSTM、Transformer）进行自动表示学习，缓解了特征工程瓶颈，但面临尺度冲突和知识鸿沟问题：特征基方法丢弃瞬态信号，端到端信号级处理计算成本高，且纯数据驱动模型缺乏可审计性。第三代尝试融合知识图谱（KG）和领域本体以增强可解释性，但KG集成多为事后标注而非主动引导特征提取，且依赖运行时外部知识库查询，不适合现场部署。最近，LLM方法通过信号到语言转换（如BearLLM）或基于Agent的KG推理实现跨域泛化，但信号文本化牺牲时间保真度，KG集成仍存在推理延迟。本文与这些工作的区别在于：通过物理引导的渐进式流水线，将领域知识显式编码到每个诊断阶段，并在训练时内化知识，消除推理时的外部依赖，同时保持全局效率和局部保真度。

### Q3: 论文如何解决这个问题？

论文提出一个三阶段渐进式物理引导框架。第一阶段（全局特征诊断）从原始振动信号中提取81维知识增强特征向量，涵盖时域、频域和小波域统计量，每个描述符与故障源周期性一一对应，建立物理可追溯性。这些特征被转换为结构化文本描述，由LoRA微调的ChatGLM-6B处理，输出故障分类和故障先验概率。第二阶段（局部补丁诊断）将原始信号分割为重叠补丁，利用第一阶段先验通过知识引导注意力权重调制补丁嵌入，放大故障相关波形区域。调制后的嵌入由12层LoRA微调GPT-2处理，捕捉局部瞬态动力学。第三阶段（多模态融合）构建异构令牌序列，包括全局特征令牌、局部补丁令牌和知识图谱令牌，由轻量级6层GPT-2处理。关键创新在于：知识图谱令牌在训练时显式包含以引导知识集成，但在推理时被移除，知识内化于模型参数中，消除外部依赖。整个流水线实现约20毫秒/样本的筛选延迟，相对于信号级基线降低12.6倍计算成本。

### Q4: 论文做了哪些实验？

实验在四个公开基准数据集上进行：CWRU（稳定实验室条件，4类）、JNU（转速变化600-1000 rpm，4类）、PU（异构工况，3类）、MFPT（类别不平衡和混合采样率，3类）。采用5折交叉验证评估。主要结果：三阶段框架平均准确率从第一阶段94.33%提升到第二阶段97.90%和融合阶段98.49%。第二阶段比第一阶段平均提升3.57个百分点，融合阶段在三个数据集上进一步提升0.30%-2.01%。JNU数据集上第二阶段提升最大（+10.08%），PU上融合阶段提升最大（+2.01%）。计算效率分析显示，融合阶段训练时间最短（平均39秒/epoch），比第一阶段快12.6倍。可解释性分析通过令牌贡献分布和跨模态注意力可视化验证：补丁令牌主导诊断决策（71.54%-79.89%），KG令牌贡献3.82%-7.52%，且注意力模式与轴承故障力学一致。

### Q5: 有什么可以进一步探索的点？

论文当前验证限于数据集内评估，跨数据集迁移学习是主要未来方向。可探索自适应融合策略以处理复合故障（如内圈与外圈同时故障），以及故障严重程度监测（从分类扩展到退化评估）。轻量级变体用于边缘部署（如进一步压缩模型以适应嵌入式设备）。此外，可引入自进化技能（self-evolving skill）和反思机制，使框架能根据新工况自动调整知识引导权重。在Agent工作流方面，可扩展为多Agent系统，其中不同Agent分别负责特征提取、补丁分析和知识验证，并通过反馈优化实现闭环诊断。最后，可探索将时序基础模型（如TimesFM）与物理引导特征结合，提升跨工况泛化能力。

### Q6: 总结一下论文的主要内容

本文提出一个三阶段渐进式物理引导的振动信号处理框架，用于滚动轴承故障诊断。框架通过81维物理可追溯特征描述符、故障自适应信号分割机制和多模态融合，同时解决了全局特征效率与局部瞬态保真度的尺度冲突、数据驱动模型的知识鸿沟以及多源信息融合不足三大挑战。在四个公开数据集上达到98.49%平均准确率，计算成本降低12.6倍。可解释性分析证实诊断特征激活与轴承故障力学一致。核心贡献在于将物理知识内化于模型参数，消除推理时外部依赖，实现高效、可解释且适合工业在线部署的诊断系统。
