---
title: "Zero-Shot Time-Series Question Answering via Decoupled Perception and Reasoning"
authors:
  - "Jing Xie"
  - "Haochen Yuan"
  - "Yunbo Wang"
date: "2026-10-04"
arxiv_id: "2610.04942"
arxiv_url: "https://arxiv.org/abs/2610.04942"
pdf_url: "https://arxiv.org/pdf/2610.04942v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Time-Series Question Answering"
  - "Zero-Shot"
  - "Tool Selection"
  - "Tool Calling"
  - "Memory"
  - "Feedback Loop"
  - "Iterative Re-perception"
  - "Decoupled Perception and Reasoning"
  - "Time-Series Perception State"
  - "LLM Agent"
  - "Numerical Feature Extraction"
  - "Semantic Reasoning"
relevance_score: 8.5
---

# Zero-Shot Time-Series Question Answering via Decoupled Perception and Reasoning

## 原始摘要

Time-series question answering (TSQA) requires grounding linguistic queries and diverse answer formats in complex numerical observations. However, existing methods heavily overfit to specific datasets and struggle to generalize when input series, question contexts, and answer requirements shift simultaneously. To address this challenge, we propose TSHarness, an agentic framework that establishes a decoupled workflow for cross-dataset zero-shot TSQA. At its core, TSHarness divides and conquers numerical perception and contextual reasoning via a structured Time-Series Perception State (TPS). Guided by a reusable memory of analytical knowledge, a learned Tool Selector adaptively invokes numerical tools to extract salient statistical and temporal features into the TPS. The answering agent then performs semantic reasoning over the TPS to generate target outputs, triggering iterative re-perception through the feedback loop when evidence is deemed insufficient. By separating numerical feature extraction from question-specific reasoning, TSHarness eliminates the need for target-side training or answer feedback, providing a generalizable, cost-efficient foundation for zero-shot TSQA.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列问答（TSQA）旨在将数值观测转化为关于时序模式、事件、预测与决策的答案。现有方法通常依赖数值-文本对齐和任务特定训练来获得时序能力，但这类模型在单一数据集上的性能提升难以可靠迁移到其他数据集。本文认为，这一迁移鸿沟源于主流范式将 TSQA 视为单体任务，把数值感知与数据集特定的答案生成紧密耦合，导致端到端模型在零样本场景下同时面临两类分布偏移：一是输入序列在采样率、序列长度、缺失模式与通道维度上的感知偏移；二是问题语义与答案要求共同变化的上下文偏移，涵盖多选、判断及有序标签等异构评测标准。这些并发偏移从根本上阻碍了跨域知识复用：基于学习的方法其微调参数过拟合源数据集相关性，造成参数复用失败；基于智能体的方法所存储的分析流程与记忆又难以泛化到差异显著的基准，造成分析复用失败。因此，本文的核心问题是在跨数据集零样本迁移的严格设定下，如何解耦连续数值感知与上下文相关推理，使源域开发的分析能力无需目标侧微调或答案反馈即可动态重组，从而在未见基准上实现稳健泛化。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，ChatTime通过扩展词表将数值观测与语言连接，Time-MQA采用上下文问答训练，ChatTS利用合成对齐数据，TimeOmni-1则通过奖励引导训练增强推理能力；这些工作多依赖目标侧训练或数据对齐，而TSHarness无需目标侧训练或答案反馈，通过TPS显式分离数值感知与问题推理。应用与框架类方面，TS-Agent结合数值工具与证据收集验证，AION组织时间接地工作流与审查，KairosAgent从预测反馈中学习推理-预测交互，TimeClaw整合时间工具、能力演化与情景检索。TSHarness与TimeClaw最为接近，但聚焦于感知与回答之间证据传递的结构，TPS为序列属性提供稳定字段结构，使回答器可自适应调整解释与证据请求。评测类方面，近期基准揭示了时间序列适配LLM的跨域弱点，并区分尺度选择、定位与跨区间整合能力。此外，思维链提示、工具增强智能体、规划-执行分离及基于奖励的LLM工具使用策略等通用智能体研究，也为TSHarness的编排与RL工具选择器提供了基础。

### Q3: 论文如何解决这个问题？

论文提出的核心方法是TSHarness，一个面向跨数据集零样本时间序列问答的智能体框架，其关键思想是“解耦感知与推理”。整体流程为：先由Perceiver在程序性记忆引导下生成初始工具执行计划，经Tool Selector校验与精炼后，调用数值工具从原始序列中提取统计与时序特征，写入结构化的Time-Series Perception State（TPS）；随后Answerer在TPS证据与问题上下文上进行语义推理，若证据不足则发起针对性再感知请求，形成迭代闭环，直到证据充分或预算耗尽，最终按答案规范κ合成输出。

架构上包含三个主要组件：一是工具增强的数值感知模块，工具声明其支持的分析、输入要求与输出字段，可直接作用于原始数值数组，保留细粒度时间索引；二是TPS状态，由静态核心C、动态扩展D_r和证据需求集Q组成，核心记录元数据、统计摘要、时序原语与LLM摘要，扩展记录问题特定的分析请求、返回证据、来源标识与覆盖状态，从而将客观数值属性与任务特定推理隔离；三是基于强化学习的Tool Selector，将工具选择建模为MDP，以Perceiver提案为先验，用轻量评分网络调整工具纳入概率，并以PPO优化，奖励同时考虑答案正确性与工具执行成本。

创新点在于：通过TPS实现数值感知与语义推理的解耦，使系统仅依赖源数据集构建工具库、记忆库与策略参数，跨数据集迁移时全部冻结，无需目标侧训练或答案反馈；Answerer可主动触发迭代再感知，实现证据驱动的自适应分析；Tool Selector在保证正确性的同时降低冗余工具调用，提升零样本迁移的泛化性与成本效率。

### Q4: 论文做了哪些实验？

论文在六个基准上评估TSQA任务：TSRBench、Time-MQA、ChatTime、CaTSBench、TSAQA和TimeOmni-1。其中TSRBench作为源基准用于构建harness，其余五个用于跨数据集零样本评估。实验分两种设置：分布内评估使用TSRBench的10%测试划分；零样本评估将TSRBench开发的harness直接部署到五个目标基准，每个基准随机采样412个QA样本，覆盖不同问题类型，且无目标侧训练、调优或参考答案反馈。

对比方法分三组：任务专用模型（ChatTime、Time-MQA检查点）、智能体方法（CoT、ReAct、TimeClaw）以及GPT-5.6-sol和Qwen3.8-27B两种骨干模型。指标为各基准原生解析和评分协议下的准确率，无效或格式违规回答严格判错。

主要结果：在TSRBench上，Qwen3.8-27B骨干下准确率从43.69%提升至62.62%，GPT-5.6-sol下从66.75%提升至72.09%。零样本迁移中，Qwen3.8-27B下五个目标基准全部提升，ChatTime增益最大（74.13%→96.10%），Time-MQA、CaTSBench、TSAQA、TimeOmni分别提升7.77、3.64、7.28、4.13个百分点。消融实验显示，移除数值工具使平均目标准确率从74.61%降至63.06%，移除记忆影响较小（74.76%）。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于：其一，Memory 组件在跨数据集零样本迁移中增益有限，甚至略低于无 Memory 版本，说明分析知识高度依赖源域，难以泛化到新问题类型；其二，TimeOmni 上出现负迁移，且 TSAQA、TimeOmni 的答案精炼净增益为负，表明对开放式、多模态或长时序推理任务，TPS 的统计特征提取可能不足以支撑语义推理；其三，Tool Selector 的精度-效率权衡仍以源域策略为基础，未在目标域自适应调整。

未来可从三方面探索：一是构建域无关的层次化记忆，将分析知识抽象为可迁移的元规则而非具体工具调用模板；二是引入不确定性估计，让 Answerer 主动判断何时需要重感知，减少无效循环；三是将 TPS 扩展为多模态状态，纳入频域、事件序列或文本元数据，以覆盖 TimeOmni 类任务。此外，可探索工具选择策略的在线元学习，在零样本部署时利用少量无标注反馈动态调整调用预算。

### Q6: 总结一下论文的主要内容

论文针对时间序列问答（TSQA）中现有方法因感知与推理耦合而难以跨数据集泛化的问题，提出TSHarness智能体框架。其核心思路是将数值感知与上下文推理解耦，通过结构化时间序列感知状态（TPS）作为中间表示：由Perceiver在可复用分析记忆引导下调用数值工具，提取统计与时间特征填入TPS；Answerer基于TPS进行语义推理生成答案，并在证据不足时触发迭代式再感知反馈循环。此外，论文设计轻量级强化学习工具选择器，在答案正确性与执行开销间取得平衡，剔除冗余工具调用。实验在TSRBench上构建系统，零样本迁移至五个异构目标基准，无需目标端训练或答案反馈。结果表明，TSHarness在开源与闭源骨干模型上均显著优于同骨干基线，消融实验证实数值工具是跨数据集迁移的关键贡献，记忆则主要利于构建域内。该工作为跨数据集零样本TSQA提供了可泛化、低成本的新范式。
