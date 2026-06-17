---
title: "Closing the Feedback Loop: From Experience Extraction to Insight Governance in Verbal Reinforcement Learning"
authors:
  - "Yanwei Cui"
  - "Xing Zhang"
  - "Yulong Zhang"
  - "Li Shao"
  - "Xiaofeng Shi"
  - "Guanghui Wang"
  - "Peiyang He"
date: "2026-06-16"
arxiv_id: "2606.17591"
arxiv_url: "https://arxiv.org/abs/2606.17591"
pdf_url: "https://arxiv.org/pdf/2606.17591v1"
categories:
  - "cs.AI"
tags:
  - "verbal reinforcement learning"
  - "LLM agent"
  - "feedback loop"
  - "insight governance"
  - "experience extraction"
  - "non-stationary environment"
  - "financial forecasting"
relevance_score: 6.5
---

# Closing the Feedback Loop: From Experience Extraction to Insight Governance in Verbal Reinforcement Learning

## 原始摘要

Training-free verbal reinforcement learning enables LLM agents to learn from world feedback -- objective signals such as dynamic task outcomes, market returns, or demand forecasts -- by extracting verbal rules from experience and injecting them as context, updating the agent's behavior without parameter changes. However, in non-stationary environments these agents face a retention-forgetting dilemma: retaining stale insights causes negative transfer, while discarding them causes catastrophic forgetting when conditions recur. We identify four requirements for navigating this dilemma -- outcome-driven evaluation, persistent structured evidence, non-monotonic knowledge lifecycle, and compositional governance -- and show that existing methods invest heavily in experience extraction while underinvesting in insight governance. We propose a three-layer architecture -- rules, evidence, and skills -- connected by a feedback-driven curation loop that closes the governance gap. Rules capture distilled experience from world outcomes; evidence logs track each rule's reliability across episodes; skills govern which rules to apply, how to resolve conflicts, and when to abstain. On financial forecasting as a case study, where world feedback is naturally abundant, noisy, and non-stationary, we show that the same accumulated experience either degrades performance below the zero-shot baseline or dramatically improves accuracy and risk-adjusted returns, depending on whether the curation loop is present.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决在非平稳环境中，基于世界反馈的免训练语言强化学习智能体所面临的“保留-遗忘困境”。研究背景是，大型语言模型智能体通过从世界反馈（如动态任务结果、市场回报）中提取语言规则并注入上下文来学习，无需参数更新。现有方法虽在经验提取上投入巨大，但忽视了经验治理，导致智能体在非平稳环境中陷入两难：保留过时规则会引发负迁移，而丢弃规则又会在条件重现时造成灾难性遗忘。论文的核心问题是，如何设计一个治理机制，使智能体能够动态评估、结构化存储并组合运用经验，从而在非平稳反馈中持续改进，而非因经验积累而性能退化。为此，论文提出了一个由规则、证据和技能组成的三层架构，通过反馈驱动的策展循环来弥合经验提取与洞察治理之间的鸿沟。

### Q2: 有哪些相关研究？

相关研究可分为三类。**方法类**中，Reflective Accumulation 提取经验但无后续评估，导致规则过时；Reflective Refinement 引入重要性评分但修改时破坏证据链；Trajectory-Informed Tips 通过因果归因实现评估，但缺乏跨回合证据积累；Meta-MDP Experience Library 采用两级评估并保留失败知识，但证据追踪不足。本文与这些方法的核心区别在于，它们侧重经验提取而忽视治理，本文则通过反馈驱动的策展循环（规则-证据-技能三层架构）系统性地满足四项要求（R1-R4）。**评测类**中，SkillsBench 发现策展技能显著提升性能而自生成技能反而下降，本文将其静态发现扩展为动态环境下的连续治理。**基础设施类**中，Hindsight 通过意见网络追踪信念强度但丢弃结构化证据；IMPACT-CYCLE 利用依赖图实现持久证据与非单调更新，但限于单会话事实修正；AGM 信念修正框架提供形式化保证，Kumiho 实现其操作化。本文在这些记忆系统之上构建了连接世界反馈与存储知识的策展循环，管理的是信任而非记忆本身。

### Q3: 论文如何解决这个问题？

该论文提出了一种三层的反馈驱动策展架构，以解决无训练语言反馈强化学习中经验保留与遗忘的困境。核心方法围绕规则、证据和技能三个层次构建，并通过批评者-提议者-策展者流水线形成闭环。

整体框架包含三个主要模块：
1. **规则层**：存储从世界反馈中提取的蒸馏经验，每条规则包含触发条件和纠正动作。规则采用弃用而非删除策略，保留知识以满足非单调生命周期需求。
2. **证据层**：为每条规则维护持久的结构化日志，记录每次评估的回合、结果和条件。采用仅追加设计，证据永不删除或覆盖，即使规则被弃用也保留完整历史轨迹，支持基于结果驱动的评估和持久结构化证据。
3. **技能层**：作为治理层，跨规则读取证据，控制哪些规则进入有限上下文、解决冲突以及何时弃权。技能随证据积累而演化，从试探性策略发展为经过验证的优先级排序和反模式编码，实现组合治理。

反馈闭环通过批评者、提议者和策展者三个角色实现：
- **批评者**：将规则增强推理与零样本基线进行比较，生成比标量成功/失败更丰富的归因评估。
- **提议者**：将批评者评估追加到每条规则的证据日志中，并基于失败模式提出新规则。
- **策展者**：读取跨规则证据，同时做出生命周期和治理决策——弃用持续负面证据的规则，并演化技能以编码优先级排序、冲突解决和反模式。

关键技术创新在于证据日志的持久性和仅追加设计，使得治理决策始终基于完整的历史观察结果，避免了现有方法中规则重写导致证据失效的问题。在金融预测案例中，该方法相比零样本基线显著提升了准确性和风险调整收益。

### Q4: 论文做了哪些实验？

实验以金融预测为案例，采用2013-2016年标普500前5大股票（AAPL、AMZN、FB、GOOGL、MSFT）的日频OHLCV数据作为学习阶段，2017年数据作为测试集，输入为20天K线图，预测未来5天。基础模型为Qwen3-VL-235B，批评者、提议者和策展者使用Claude Sonnet 4.6。对比方法包括：零样本（无上下文）、反思累积（无策展地提取所有规则）、反思精炼（带重要性评分和原地修改，但无持久证据日志和技能治理）。主要指标包括方向准确率、情景准确率、平均每笔收益、夏普比率和最大回撤。

结果显示：反思累积在所有指标上低于零样本（方向准确率46.3% vs 51.2%，夏普比率-0.12），表明无治理的经验有害；反思精炼恢复至接近零样本水平（方向准确率51.1%，夏普比率0.36），但风险调整收益仍下降；而完整策展循环（本文方法）在所有指标上显著提升：方向准确率56.5%（+5.3pp）、情景准确率29.0%、平均收益0.33%、夏普比率1.00（近乎翻倍）、最大回撤降至13.0%（减少60%）。规则库演化显示，策展循环通过持久证据日志和技能治理，使活跃规则数量保持稳定（从5增至11），而未治理的累积规则数达19条，验证了治理机制的有效性。

### Q5: 有什么可以进一步探索的点？

论文的核心局限在于实证验证仅覆盖了单一金融领域（2013-2017牛市），且证据日志以自然语言线性增长，缺乏可扩展性。未来可从三方面探索：一是将治理机制推广到异构世界反馈（如机器人控制信号、延迟奖励），验证证据结构和技能编排模式是否跨领域通用；二是实现元治理——让世界反馈驱动治理机制本身的演化，例如通过强化学习自动设计批判标准、弃用阈值和技能组合策略，形成“学习如何学习”的第二反馈闭环；三是改进证据表示，采用结构化或嵌入化存储替代自然语言日志，并引入时间衰减权重以平衡快速适应与稀有经验保留。此外，可探索非单调知识生命周期在更剧烈非平稳环境（如市场崩盘）中的表现，以及如何通过多智能体协作实现治理规则的涌现。

### Q6: 总结一下论文的主要内容

该论文聚焦于无训练强化学习中LLM Agent在非平稳环境下面临的“保留-遗忘困境”：保留过时经验导致负迁移，丢弃则引发灾难性遗忘。核心贡献在于提出“经验治理”比“经验提取”更为关键，并构建了三层架构（规则、证据、技能）与反馈驱动的策展循环。方法上，规则从世界反馈中提取经验，证据日志追踪规则可靠性，技能负责规则应用、冲突解决与弃权决策。以金融预测为案例，实验表明，相同经验在有无策展循环下结果截然不同：无策展时准确率下降4.9个百分点且夏普比率为负，有策展时准确率提升5.3个百分点、夏普比率翻倍、回撤降低60%。该工作揭示了经验治理是Agent从世界反馈中持续学习的主要瓶颈，为可解释时间序列分析与工业故障诊断中的非平稳适应问题提供了新范式。
