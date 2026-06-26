---
title: "Forecasting With LLMs: Improved Generalization Through Feature Steering"
authors:
  - "Humzah Merchant"
  - "Bradford Levy"
date: "2026-06-25"
arxiv_id: "2606.27199"
arxiv_url: "https://arxiv.org/abs/2606.27199"
pdf_url: "https://arxiv.org/pdf/2606.27199v1"
categories:
  - "cs.CL"
  - "cs.LG"
tags:
  - "LLM"
  - "时间序列预测"
  - "可解释性"
  - "特征干预"
  - "稀疏自编码器"
  - "前瞻偏差"
  - "时间感知推理"
relevance_score: 6.5
---

# Forecasting With LLMs: Improved Generalization Through Feature Steering

## 原始摘要

Successful forecasting involves identifying patterns between historical and future states of the world which generalize to future observations. We apply LLMs to a variety of forecasting tasks and inspect their internal states using sparse autoencoders to understand whether they appear to rely on time-specific pieces of knowledge versus generalizable patterns. Our analyses identify features associated with both time-aware reasoning and look-ahead-biased reasoning. We then apply the LLMs to an entirely different domain and intervene on these features. We find that amplifying time-awareness features substantially reduces look-ahead bias on forecasting prompts while preserving general reasoning performance. In contrast, steering the candidate look-ahead-bias features does not produce an effect. These results suggest that interpretable temporal features can be used to causally shift LLMs toward more historically grounded reasoning.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决大型语言模型（LLM）在时间序列预测任务中过度依赖记忆而非泛化推理的问题。研究背景是，LLM在预测时可能直接调用训练数据中存储的未来结果（即“事后知识”），而非基于预测时刻可用的历史信息进行推理，这导致模型在样本外预测中表现不佳。现有方法的不足在于：尽管已有研究通过系统提示或微调尝试提升模型的时间感知能力，但缺乏对内部表征机制的深入理解，无法区分“时间感知推理”与“事后偏差推理”对应的具体特征，更无法实现因果层面的干预。本文的核心问题是：能否通过稀疏自编码器识别LLM中与时间感知和事后偏差相关的可解释特征，并通过特征干预（如放大时间感知特征）来减少模型对事后知识的依赖，从而提升其基于历史信息的泛化预测能力。研究在并购和制药预测等零样本外预测任务上验证了该方法，发现放大时间感知特征能显著降低事后偏差，而干预事后偏差特征则无效。

### Q2: 有哪些相关研究？

本文的相关研究主要分为三类。第一类是**稀疏特征与行为干预**，基于稀疏自编码器（SAEs）分解语言模型激活为可解释特征，并通过干预特征（如“金门大桥Claude”实验）实现行为控制。本文将此方法从通用语义和安全行为扩展到时间推理领域，通过放大时间感知特征来减少前瞻偏差。第二类是**时间感知与预测**，研究语言模型是否尊重时间上下文，如通过时间戳条件化建模时变事实，以及Prophet Arena等基准评估实时预测能力。本文在此基础上进一步探究时间推理是否反映在内部特征中，并实现因果干预。第三类是**前瞻偏差缓解**，现有方法包括时间受限模型（如chronologically restricted models）和输入级匿名化，但前者规模小、训练不足，后者降低能力且约束任务。本文采用混合离线-在线方法，通过识别和放大时间感知特征来缓解偏差，与现有方法在机制上显著不同。

### Q3: 论文如何解决这个问题？

论文通过稀疏自编码器（SAE）和特征引导（Feature Steering）技术，解决LLM在时间序列预测中依赖非通用模式（如前瞻偏差）的问题。核心方法分为三步：首先，利用SAE将LLM中间层激活分解为稀疏、可解释的特征向量，每个特征对应特定概念（如时间感知或前瞻偏差）。其次，通过激活对比（activation-contrast）和Neuronpedia标注，从SAE特征中筛选出与时间感知和前瞻偏差相关的候选特征。最后，在推理时对选定特征进行因果干预：通过修改SAE解码前的特征激活值（如放大时间感知特征），将修改后的激活重新注入模型，观察预测行为变化。

整体框架包括三个模块：SAE特征提取模块（将密集激活映射为稀疏特征）、特征筛选模块（结合标注和对比分析定位时间相关特征）、特征引导模块（通过调整特征强度实现因果干预）。创新点在于：1）首次将SAE应用于时间序列预测的可解释性分析，揭示LLM内部存在时间感知和前瞻偏差两类竞争性特征；2）提出通过放大时间感知特征而非抑制前瞻偏差特征来消除偏差，实验表明该方法在跨领域预测中显著降低前瞻偏差，同时保持通用推理性能；3）发现前瞻偏差特征无法被有效引导，暗示其可能由更复杂的交互模式产生。该方法为LLM在时序任务中的可靠泛化提供了可解释的因果干预手段。

### Q4: 论文做了哪些实验？

论文通过两组实验验证了特征引导（Feature Steering）对减少LLM前瞻偏差（Look-Ahead Bias）的效果。实验设置包括：使用Gemma 3 27B和Qwen 3模型，通过稀疏自编码器（SAE）从预测市场数据（Kalshi）中识别时间感知特征（如L40 24283）和前瞻偏差特征（如L31 2450）。主要实验分为两个领域外自由生成任务：1）并购预测（M&A）：基于WRDS数据构建基准，从交易公开前约一年（如2018年2月12日交易，提示日期为2017年1月1日）提示模型预测收购目标，由于样本外可预测性接近零，将提及实际目标视为前瞻偏差；2）制药增长驱动预测：基于截止日期后药物信息被引用的次数标注偏差。对比方法包括放大时间感知特征、抑制前瞻偏差特征，以及无干预基线。主要结果：放大时间感知特征（如Gemma 3的L40 24283）在两项任务中均显著降低前瞻偏差（如并购任务中偏差比例下降约15-20%），而抑制候选前瞻偏差特征未产生因果效果。同时，MMLU CoT和MMLU-Pro CoT（5-shot）性能保持稳定，表明效果非源于模型质量退化。关键数据指标包括前瞻偏差比例和MMLU准确率。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：特征干预仅在单一预测市场数据集上验证，且仅使用稀疏自编码器识别的时间感知特征有效，而前瞻偏差特征未能产生因果效应，说明特征发现机制可能不完整。此外，强干预会降低模型通用性能，表明该方法难以作为独立解决方案。

未来可探索的方向包括：1）在更多时间序列任务（如金融、气象、工业时序）中验证特征的可迁移性，并开发跨域特征对齐方法；2）结合对比学习或因果发现技术，更精确地分离时间感知与前瞻偏差的神经表征；3）探索组合策略的协同效应，例如将中等强度的特征引导与基于时间戳的提示工程、反事实数据增强相结合，在保持通用能力的同时系统性消除偏差；4）研究特征干预的动力学机制，理解为何某些特征可被有效引导而另一些不能，从而设计更鲁棒的干预策略。

### Q6: 总结一下论文的主要内容

该论文研究了如何利用大型语言模型（LLM）进行时间序列预测，并解决其固有的“前瞻偏差”问题。核心贡献在于通过稀疏自编码器（SAE）从LLM内部状态中识别出与“时间感知”和“前瞻偏差”相关的可解释特征。方法上，作者首先让LLM执行多种预测任务，并分析其内部特征；随后，在完全不同的领域中对这些特征进行干预（特征引导）。主要结论是：增强“时间感知”特征能显著减少预测中的前瞻偏差，同时保持通用推理能力；而抑制“前瞻偏差”特征则效果不明显。该研究的意义在于，它揭示了前瞻偏差不仅是记忆后训练数据的结果，更是一种可被因果干预的内部行为倾向，为通过可解释的时序特征引导LLM进行更符合历史逻辑的推理提供了新路径。
