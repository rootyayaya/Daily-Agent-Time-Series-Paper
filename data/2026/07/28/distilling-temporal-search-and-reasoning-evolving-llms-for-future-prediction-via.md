---
title: "Distilling Temporal Search and Reasoning: Evolving LLMs for Future Prediction via Harness-Assisted Efficient Data Synthesis"
authors:
  - "Wanxu Cai"
  - "Zhengyu Chen"
  - "Huaisheng Zhu"
  - "Wei Wang"
  - "Jingang Wang"
  - "Qiang Xu"
date: "2026-07-28"
arxiv_id: "2607.25554"
arxiv_url: "https://arxiv.org/abs/2607.25554"
pdf_url: "https://arxiv.org/pdf/2607.25554v1"
categories:
  - "cs.AI"
tags:
  - "LLM/Agent用于时间序列分析"
  - "时间推理"
  - "工具集成推理"
  - "数据合成"
  - "自进化"
  - "未来预测"
  - "时间截断"
relevance_score: 7.5
---

# Distilling Temporal Search and Reasoning: Evolving LLMs for Future Prediction via Harness-Assisted Efficient Data Synthesis

## 原始摘要

Future event prediction carries broad social impact yet remains challenging. SOTA approaches augment LLMs with external agent frameworks whose predictive capability vanishes once the harness is removed. While recent Tool-Integrated Reasoning (TIR) internalizes deep search for multi-hop retrieval of facts, forecasting further demands temporal search and reasoning over historical trends and dynamic shifts. The key obstacle is data: historical queries induce temporal leakage that degrades forecasting into retrieval. Prior works either freeze information gathering with static observations, or rely on rejection sampling or unresolved fresh queries that discard vast amounts of data, degrading synthesis efficiency. We propose a time-truncation harness that enforces a temporal cut-off at every turn, enabling TIR-style sampling from historical events, reducing temporal leakage and reliance of rejection sampling or unsolved queries, increasing the sampling efficiency. We further build a large-scale corpus and a process-based metric and show that our harness naturally induces a broader temporal breadth of search and raises the proportion of high-quality data, further increasing the efficiency and reducing the reliance on complex rubrics. Distillation experiments show that students trained on harness-intervened data achieve the best performance, demonstrating harness-assisted model evolving that turns higher quality temporal search and reasoning data into a parametric advancement of the students.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

未来事件预测在社会各领域具有重要影响，但现有方法存在根本性缺陷。当前最先进的方法通过外部代理框架增强LLM，然而一旦移除该框架，预测能力便消失。近期研究尝试通过工具集成推理（TIR）内化深度搜索能力，但深度搜索仅适用于静态事实检索，而预测任务需要的是对历史趋势和动态变化进行时间搜索与推理。核心障碍在于数据：使用历史事件作为查询会导致时间泄漏，使预测退化为信息检索。现有方法要么提供静态观测冻结信息收集过程，要么依赖拒绝采样或未解决的实时查询，导致数据合成效率低下。本文提出一种时间截断机制，在轨迹合成的每一轮强制实施时间截止点，从而限制代理可访问的时间线在历史事件发生之前。该机制直接从历史查询中采样具有更高无泄漏率的轨迹，大幅减少对拒绝采样或查询选择的依赖，提升数据合成效率。通过构建大规模语料库和基于过程的度量指标，本文证明该机制自然诱导更广泛的时间搜索广度并提高高质量数据比例。蒸馏实验表明，使用该机制干预数据训练的学生模型取得了最佳性能，实现了将高质量时间搜索与推理数据转化为参数进步的成功范式。

### Q2: 有哪些相关研究？

相关研究主要分为两类。第一类是外部Agent框架，如Claude Code、Codex、OpenClaw等通用工具，以及Milkyway等预测专用框架，它们通过测试时扩展提升性能，但预测能力随框架移除而消失。本文与这些工作的核心区别在于，本文致力于将预测能力内化到LLM参数中，而非依赖外部框架。

第二类是训练LLM自主执行预测。前沿模型如GLM-5、Kimi-K2.5已支持工具集成推理（TIR），但主要针对通用多跳事实问题。小规模模型方面，Search-r1和DeepDive使用Agent强化学习，MiroThinker v1.7/H1采用验证器推理框架，但均未专门针对未来预测场景。早期工作采用解耦架构分离检索与推理，后续研究利用结果作为监督信号训练模型，但依赖静态数据构建，无法支持训练中的工具集成推理。FutureWorld和Echo通过持续收集未解决预测查询并计算奖励，但面临奖励稀疏和延迟问题，Echo还需领域特定规则进行轨迹选择，成本高昂。

本文提出的时间截断机制通过在每个回合强制时间截止，实现了从历史事件中进行TIR风格采样，减少了时间泄漏和对拒绝采样或未解决查询的依赖，显著提高了数据合成效率，并自然诱导更广泛的时间搜索广度，降低了高质量数据获取成本。

### Q3: 论文如何解决这个问题？

该论文提出了一种时间截断框架（Time-Truncation Harness），以解决时间序列预测中数据合成效率低和时序泄漏的问题。核心方法是构建一个受约束的搜索环境，确保智能体在每一轮交互中只能访问事件发生前的信息。

整体框架包含三个主要组件：1）**时间截断环境**：为每个查询设置截止日期 \(T_{cut} = T_{end} - \Delta_T\)，通过API感知查询重写和后验网页过滤两种方式实现，只返回发布时间不晚于 \(T_{cut}\) 的文档，从根本上消除时序泄漏；2）**对齐系统提示**：在初始提示中注入 \(T_{cut}\) 指令，使智能体的时间上下文与环境保持一致；3）**大规模语料库与过程指标**：基于截断环境采样生成高质量轨迹，并设计基于过程的度量标准来评估数据质量。

关键技术在于：相比静态观察（丧失动态查询能力）、拒绝采样（高丢弃率）和未解决查询（低吞吐量）等现有方法，该框架通过约束环境而非过滤数据，显著提升了采样效率。实验表明，截断环境自然诱导了更广的时间搜索广度，提高了高质量数据比例，且蒸馏训练的学生模型性能最优，实现了从高质量搜索推理数据到参数化进步的模型演化。

### Q4: 论文做了哪些实验？

论文进行了两组主要实验。首先，在数据合成阶段，使用Kimi-K2.5模型在有无时间截断约束（harness）两种设置下生成轨迹，并分析了轨迹质量。在200个随机样本中，有约束组的数据泄漏率（日期泄漏0，内容泄漏23）远低于无约束组（日期泄漏181，内容泄漏101），有效数据比例从7.0%提升至88.5%。有约束组虽准确率下降5%-25%，但工具调用次数显著增加，且查询日期跨度中位数从低于150天提升至超过300天，表明模型被迫进行更广泛的历史搜索与推理。

其次，进行了知识蒸馏实验。学生模型为Qwen3-8B和Qwen3-32B，采用全参数SFT训练。对比方法包括：仅用通用深度搜索轨迹的DeepSearch-SFT、混合无约束预测轨迹的Mix-SFT (w/o harness)和混合有约束预测轨迹的Mix-SFT (w/ harness)。在ForecastBench（5个领域，246个问题）和FutureX（L1-L4难度级别）两个动态基准上评估。主要结果显示，在ForecastBench上，Mix-SFT (w/ harness)在8B和32B骨干上分别取得最低的Brier分数（0.2550和0.1998），相比无约束混合版本性能提升19.48%和22.04%。在FutureX的困难任务（L3-L4）上，有约束混合版本持续领先，8B骨干上提升8.82%-13.46%，32B骨干上提升14.08%-17.74%；但在简单任务（L1-L2）上优势不明显甚至略有下降。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三方面：一是合成数据质量受限于教师模型自身能力；二是未与现有基线方法进行系统性对比，也未追求SOTA性能；三是时间截断机制虽能缓解但无法完全消除时间泄漏。未来可从以下方向探索：首先，扩大学生模型参数量级，验证蒸馏效果是否随模型规模持续提升，这有助于判断该方法向更大模型迁移的可行性。其次，可将该时间截断框架改造为强化学习环境，利用其低泄漏反馈特性进行更干净的轨迹采样和更可靠的奖励计算，从而优化长轨迹时间搜索策略。此外，可尝试引入轻量级基于规则的过滤机制，进一步降低残余时间泄漏比例。最后，建议将该方法扩展到多模态时间序列预测场景，例如结合数值型传感器数据与文本事件描述，以增强工业故障诊断中的时序推理能力。

### Q6: 总结一下论文的主要内容

这篇论文提出了一种时间截断约束框架，用于解决大语言模型（LLM）在时间序列预测中面临的数据泄露和采样效率低下的问题。核心贡献在于通过在每个推理步骤强制时间截止，从历史查询中合成低泄露的预测轨迹，从而将外部时间搜索与推理能力内化为模型参数。方法上，该框架替代了传统的拒绝采样或未解决查询方式，显著提升了采样效率和高质量数据比例。实验表明，基于该框架蒸馏训练的学生模型在预测性能上最优，验证了通过高质量数据合成实现模型能力进化的有效性。该工作推动了LLM在时间序列预测中的可解释性与自主推理能力。
