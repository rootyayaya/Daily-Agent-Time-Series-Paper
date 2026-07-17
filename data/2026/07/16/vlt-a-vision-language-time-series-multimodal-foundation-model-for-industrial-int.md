---
title: "VLT: A Vision-Language-Time Series Multimodal Foundation Model for Industrial Intelligence"
authors:
  - "Haiteng Wang"
  - "Jingheng Yan"
  - "Xiaokang Wang"
  - "Lei Ren"
date: "2026-07-16"
arxiv_id: "2607.14510"
arxiv_url: "https://arxiv.org/abs/2607.14510"
pdf_url: "https://arxiv.org/pdf/2607.14510v1"
categories:
  - "cs.AI"
tags:
  - "多模态基础模型"
  - "时间序列-文本联合建模"
  - "工业故障诊断"
  - "频域视觉桥接"
  - "Time-MoE"
  - "少样本学习"
  - "鲁棒性"
  - "泛化性"
relevance_score: 7.5
---

# VLT: A Vision-Language-Time Series Multimodal Foundation Model for Industrial Intelligence

## 原始摘要

Industrial time series serve as the foundation for Prognostics and Health Management (PHM) to ensure the reliability and safety of industrial equipment such as aero-engines. However, existing approaches are typically limited to single-modality modeling, which restricts their generalization in complex scenarios. Although recent advances in large language models (LLMs) provide new opportunities for multimodal learning, bridging continuous time-series signals and discrete textual semantics remains an open challenge. To this end, we propose VLT, a multimodal foundation model that jointly models time-series, frequency-spectrum visual representations, and textual knowledge. A key insight is to utilize the frequency spectrum as a visual bridge to connect continuous temporal signals with discrete semantics. Specifically, a Time-aware Mixture-of-Experts (Time-MoE) is designed to capture heterogeneous temporal dynamics, while a Frequency-Text Augmented Learner enables joint modeling of spectral and semantic features within a shared representation space. Furthermore, a time-centric gradient alignment mechanism is introduced to mitigate cross-modal optimization conflicts via gradient normalization and reliability-aware dynamic reweighting. Extensive experiments on multiple industrial datasets demonstrate that VLT outperforms state-of-the-art methods, achieving superior robustness and generalization under few-shot, noisy, and incomplete-modality settings.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业时间序列是航空发动机等工业设备预测与健康管理（PHM）的基础。现有方法通常局限于单模态建模，限制了其在复杂场景下的泛化能力。尽管大语言模型（LLM）为多模态学习提供了新机遇，但弥合连续时间序列信号与离散文本语义之间的鸿沟仍是一个开放挑战。现有方法主要分为三类：任务特定的深度学习方法，虽在域内数据表现良好，但在分布偏移或未见工况下性能下降；将LLM作为特征编码器的方法，直接映射数值信号未能充分利用LLM的语义推理能力；将时间序列转化为语言提示的方法，会导致细粒度时序信息丢失。本文旨在解决两个核心问题：1）异构连续-离散多模态统一表征，时间序列、图像和文本在结构、语义和时间连续性上存在根本差异，强制将连续时间序列转化为离散文本表征会导致时序动态信息损失；2）多模态对齐收敛冲突，主导模态（通常是时间序列）收敛更快、梯度更大，会抑制其他模态的学习，导致过拟合和欠拟合，降低融合性能。为此，本文提出VLT，首个联合建模时间、视觉和文本信息的多模态基础模型，通过引入频谱视觉表征作为连接工业时序信号与语义推理的桥梁，并设计时间感知混合专家、频率-文本增强学习器和时间中心梯度对齐机制，实现鲁棒且泛化的工业智能。

### Q2: 有哪些相关研究？

在时间序列分析与工业智能领域，相关研究主要分为以下几类：

1. **传统深度学习方法**：包括RNN、CNN及其混合模型（如CNN-LSTM、CNN-BiLSTM-AT），以及Transformer架构。这些方法专注于单模态数值传感器数据，用于故障诊断和剩余寿命预测。本文VLT与之的区别在于，VLT引入了多模态融合，突破了单模态建模的局限，提升了在少样本、噪声等复杂场景下的泛化能力。

2. **基于LLM的时间序列方法**：一类将时间序列视为类语言序列直接使用预训练LLM（如One-Fits-All、PromptCast、Time-LLM），另一类通过跨模态对齐将时间序列转换为文本或图像。此外，还有原生时间序列基础模型（如Chronos、Timer）。VLT与这些工作的区别在于，它并非简单借用LLM，而是专门设计了Time-MoE和频率-文本增强学习器，实现时间序列、频谱视觉和文本的联合建模。

3. **工业多模态方法**：如ChatTime、GPT4MTS、DiagLLM等，尝试融合数值与文本或频谱信息。VLT的创新在于引入频率谱作为视觉桥梁，并设计了时间中心梯度对齐机制来解决跨模态优化冲突，从而在工业场景下实现了更鲁棒的多模态融合，优于仅依赖单一模态或简单对齐的方法。

### Q3: 论文如何解决这个问题？

VLT提出了一种三模态融合的基础模型架构，核心创新在于利用频域作为连接连续时间信号与离散语义的视觉桥梁。整体框架包含三个专用编码器分支：时间感知混合专家模块处理原始时序信号，频域视觉学习器将时序转换为伪彩色图像并提取视觉特征，知识学习器通过轻量语言模型编码领域文本提示。关键技术包括：Time-MoE采用稀疏路由机制，为每个样本动态选择最相关的专家以捕获异质性时序动态，并引入平衡正则化防止路由坍塌；频域视觉学习器通过递归图、傅里叶振幅和小波系数三种变换生成多视角频域图像，利用预训练MAE提取视觉表征；知识学习器将时序统计特征与视觉描述组合为文本提示，通过Qwen1.5-0.5B编码器获取语义嵌入。为解决模态不平衡问题，提出时间中心的多模态梯度对齐机制：通过置信度分数评估各分支可靠性，对较弱模态施加自适应梯度增强系数，同时以时序分支梯度范数为基准对其他分支进行归一化；引入跨分支一致性约束，通过可靠性加权促使各模态预测逻辑对齐。最终通过模态注意力融合和时间中心交叉注意力生成联合表征。该架构在少样本、噪声和不完整模态场景下展现出优越的鲁棒性和泛化能力。

### Q4: 论文做了哪些实验？

论文在三个公开工业基准数据集上进行了实验，涵盖发动机剩余寿命预测、电池健康估计和轴承故障诊断。实验设置包括全样本和少样本场景，主要超参数如窗口大小48、批次128、学习率1e-3、训练轮次130等。对比方法包括Time-LLM、GPT4TS、DLinear、PatchTST和TimesNet。回归任务采用RMSE和Score指标，分类任务采用Accuracy和F1-score。主要结果：在全样本回归中，VLT在C-MAPSS四个子集上均取得最低RMSE，如FD001上RMSE为11.47，比第二名PatchTST低约8.7%；在复杂多工况FD002和FD004上优势更显著。电池数据集上，VLT在多数子集取得最优或次优性能。少样本（5%训练数据）实验中，VLT在FD001上RMSE为13.75，远优于Time-LLM的22.75；在FD002上RMSE为26.07，是唯一低于40的方法。轴承故障分类任务中，VLT在1-shot下准确率达88.23%，全样本下达99.33%，均优于FD-MVLLM和LiteFormer等对比方法。

### Q5: 有什么可以进一步探索的点？

该论文提出的VLT模型在工业时序多模态建模上取得了显著进展，但仍存在若干可进一步探索的方向。首先，模型依赖频域作为视觉桥梁，但频域变换可能丢失时域局部突变信息（如轴承冲击信号），未来可引入小波变换或多尺度时频分析以增强对非平稳信号的捕捉能力。其次，Time-MoE的专家数量与Top-k选择为固定超参数，可探索动态路由机制，根据输入信号的复杂度自适应调整专家激活策略。第三，当前文本知识仅通过预训练嵌入注入，缺乏领域本体推理能力，可结合工业知识图谱进行结构化语义对齐，例如将“轴承磨损”与振动频谱的特定频带关联。此外，梯度对齐机制虽缓解了模态冲突，但在极端噪声场景下（信噪比低于0dB）可能失效，可引入对抗训练或不确定性量化来增强鲁棒性。最后，模型在跨设备迁移（如从航空发动机到风力涡轮机）的零样本泛化能力尚未验证，可设计跨域预训练任务（如频谱-文本对比学习）来提升工业基础模型的通用性。

### Q6: 总结一下论文的主要内容

VLT提出了一种面向工业智能的多模态基础模型，首次联合建模时间序列、频谱视觉表示和文本知识。其核心贡献在于利用频谱作为连续时间信号与离散语义之间的视觉桥梁，解决了现有单模态方法泛化性差以及连续-离散模态对齐困难的问题。方法上，VLT设计了时间感知混合专家（Time-MoE）捕获异质时序动态，通过频率-文本增强学习器在共享空间中联合建模频谱与语义特征，并引入以时间为中心的多模态梯度对齐机制，通过梯度归一化和可靠性动态加权缓解跨模态优化冲突。在多个工业数据集（涡扇发动机、电池、轴承）上的实验表明，VLT在少样本、噪声和不完整模态场景下均优于现有方法，显著提升了鲁棒性和泛化能力。该工作为工业智能中的多模态融合与健康管理开辟了新方向。
