---
title: "MemFuse: Multi-Source Memory Fusion from Fragmented Observations"
authors:
  - "Chao Li"
  - "Yuanfa Li"
  - "Wenhao Wu"
  - "Xule Liu"
  - "Zhi Wang"
  - "Kun Shao"
date: "2026-08-19"
arxiv_id: "2608.18704"
arxiv_url: "https://arxiv.org/abs/2608.18704"
pdf_url: "https://arxiv.org/pdf/2608.18704v1"
categories:
  - "cs.CL"
  - "cs.AI"
tags:
  - "multi-source memory fusion"
  - "long-term memory"
  - "agent memory"
  - "evidence traceability"
  - "temporal reasoning"
  - "cross-source evidence fusion"
  - "benchmark"
  - "LLM agents"
relevance_score: 7.5
---

# MemFuse: Multi-Source Memory Fusion from Fragmented Observations

## 原始摘要

Long-term memory is essential for agents that operate across extended interactions, yet existing memory systems and benchmarks predominantly focus on single-source textual histories. In realistic settings, however, relevant information is often fragmented across applications and devices, as well as across users and time, requiring agents to integrate dispersed observations into coherent episodic memories while preserving their source provenance. To address these gaps, we introduce **MemFuseBench**, a benchmark for *multi-source memory fusion*. MemFuseBench is built with a Scene-to-Sensor pipeline that synthesizes controllable scenarios into source-tagged observations, evidence-grounded questions, and adversarial distractors. It enables systematic evaluation of temporal reasoning, cross-source evidence fusion, and robustness to noise. We further propose **MemFuse**, a structured memory system that preserves source-level evidence in event-layer atomic memory and organizes related atomic events into cluster-layer fused memory within a causal fusion graph. During retrieval, MemFuse retrieves and organizes related evidence fragments while maintaining traceability to original source events. Experiments on MemFuseBench show that MemFuse achieves the best overall performance among the evaluated memory systems under all three LLM settings and consistently improves performance on questions requiring cross-source evidence fusion.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

长期记忆系统对智能体在长时间交互中维持上下文至关重要，但现有记忆系统和基准测试主要聚焦于单一来源的文本历史，忽略了现实场景中信息常分散于多个应用、设备、用户和时间片段。这种碎片化观测导致同一事件可能由不同来源的互补信息构成，而现有方法无法有效整合这些分散的语义事件，同时保留其来源可追溯性。此外，当前基准测试多评估对话回忆、时间更新或长上下文推理，缺乏对跨来源证据融合和噪声鲁棒性的系统测试，难以衡量智能体能否从不同来源恢复互补观测并构建连贯的情景记忆。为此，本文提出MemFuseBench基准，通过场景到传感器管道生成带来源标签的观测、基于证据的问题和对抗性干扰项，以系统评估时间推理、跨来源融合和噪声鲁棒性。同时，提出MemFuse结构化记忆系统，在事件层保留原子级来源证据，并在因果融合图中将相关原子事件组织为簇层融合记忆，检索时兼顾紧凑簇记忆与可追溯源事件，从而解决多来源记忆融合的核心问题。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**长期智能体记忆系统**方面，现有工作如LoCoMo、LongMemEval等将交互历史存储为记录、摘要或层级记忆单元，近期也有结构化或图记忆方法用于连接相关经验并支持多步检索，但主要假设对话或交互历史，而非跨设备的碎片化观测。**记忆评测基准**方面，EverMemBench和GroupMemBench扩展至长期交互与多方对话，LifeBench和SMMBench虽引入异构数字痕迹或多模态证据，更接近真实场景，但未聚焦于分布式事件片段的链接、融合与溯源。**多源记忆融合**方面，事件中心资源与生活日志系统将异构记录组织为事件结构，多传感器融合研究关注信号级注册与估计，但均未从智能体记忆角度解决原子级溯源与分组检索问题。本文的MemFuseBench通过场景到传感器流水线生成带来源标签的观测，填补了评测空白；MemFuse系统则在事件层保留原子证据、在簇层构建因果融合图，实现了跨源证据的可追溯融合，与上述工作在问题设定、方法设计和评测目标上均有本质区别。

### Q3: 论文如何解决这个问题？

MemFuse通过构建一个双层的因果融合图记忆系统来解决多源碎片化观测下的长期记忆融合问题。其核心设计是将来源溯源与记忆聚合解耦，分为事件层原子记忆和簇层融合记忆两个层次。

整体框架包含四个主要模块。第一是候选检索模块，对每个新到达的原子事件，系统会从已有记忆库中检索相关的原子事件和融合记忆作为候选集，限定决策范围。第二是智能体融合规划模块，融合智能体通过两阶段决策：先利用信息寻求工具（如SearchMemory和GetPackMembers）主动收集跨源证据，再提出融合操作计划，操作类型包括创建边、创建/更新融合节点、移除成员等五种原子操作。第三是规则验证与图提交模块，采用规则验证器检查每个操作的合法性和一致性，任何违规都会导致整个计划被拒绝，防止错误操作污染持久记忆。第四是融合感知检索模块，通过查询规划、种子检索、类型化图扩展、候选重排序和证据组装五个步骤，利用Belong、Causal、Semantic三类边关系进行图遍历，最终返回可追溯的事件层证据。

创新点在于：一是双层的记忆结构设计，融合摘要仅作为检索入口，答案始终基于源标记事件；二是智能体驱动的在线融合管道，通过工具调用轨迹实现有界的信息寻求；三是类型化关系图支持跨源因果推理，并通过图扩展痕迹进行重排序，优先选择短路径的成员或因果关系证据。

### Q4: 论文做了哪些实验？

论文在MemFuseBench基准上评估了MemFuse记忆系统，采用Scene-to-Sensor流水线生成带来源标签的事件流和证据型问题。实验设置包含三种LLM后端（Qwen3-30B-A3B、GPT-4.1 Mini、Gemini 3.1 Flash Lite），对比方法包括长上下文提示、朴素RAG、Mem0、A-MEM和EverMemOS，所有top-k系统统一使用20项预算，以GPT-4.1 Mini作为评判者计算清单得分。

主要结果：MemFuse在三种LLM设置下均取得最高总体得分（0.4659/0.4574/0.4698），比最强基线高0.0024-0.1461，比朴素RAG高0.1285-0.1481。在诊断类别中，Fusion类差距最大（朴素RAG与长上下文相差0.2047-0.2706），MemFuse可缩小62%-78%的差距，并在Conflict类上持续领先。

消融实验显示，移除agentic检索循环使总体得分下降22.1%（0.1036），移除检索约束下降0.0513，说明检索阶段组件贡献最大；而图结构和融合记忆主要在User Query（0.0609）和Perspective（0.0938）类别上带来针对性提升。

### Q5: 有什么可以进一步探索的点？

当前工作仍存在若干可拓展方向。首先，MemFuseBench 的场景生成依赖预设的“场景-传感器”模板，可能限制了真实世界中跨设备、跨应用碎片化信息的复杂性和多样性，未来可引入更真实的用户行为日志或开放域数据以增强生态效度。其次，MemFuse 的融合过程主要依赖静态聚类和因果图，对动态演化的记忆（如事件时间线漂移、用户意图变化）适应性不足，可探索基于强化学习或在线图更新的自适应融合机制。此外，当前系统对噪声的鲁棒性虽优于基线，但对抗性干扰的生成策略较为单一，未来可引入更细粒度的干扰类型（如语义混淆、跨源矛盾信息）以压力测试记忆系统的判别能力。最后，记忆溯源目前仅停留在事件层，可进一步结合可解释性分析，将融合决策过程映射到原始证据链，以提升用户对Agent推理的信任度。

### Q6: 总结一下论文的主要内容

本文聚焦于智能体长期记忆中的多源信息融合问题，指出现有记忆系统与基准大多仅处理单一文本来源，而现实场景中相关信息常分散于不同应用、设备、用户与时间。为此，作者提出MemFuseBench基准，采用场景到传感器（Scene-to-Sensor）流程合成可控场景，生成带来源标签的观测、基于证据的问题及对抗性干扰项，系统评估时间推理、跨源证据融合与噪声鲁棒性。同时提出MemFuse结构化记忆系统：在事件层以原子记忆保留来源级证据，在簇层通过因果融合图组织相关原子事件形成融合记忆，检索时保持对原始事件的可追溯性。实验表明，在三种LLM设置下，MemFuse综合性能最优，并在跨源证据融合问题上持续提升表现。该工作填补了多源记忆融合基准与方法的空白，为长期智能体记忆研究提供了新方向。
