---
title: "Forecast-Dojo: Replayable Environments for Benchmarking and Training LLM Forecasting Agents"
authors:
  - "Liqin Ye"
  - "Haorui Wang"
  - "Fardin Ahmed"
  - "Rongzhi Zhang"
  - "Yuan He"
  - "Ziyuan Lin"
  - "Yanbin Yin"
  - "Jing Peng"
  - "Michael Galarnyk"
  - "Sudheer Chava"
  - "Chao Zhang"
date: "2026-09-24"
arxiv_id: "2609.28876"
arxiv_url: "https://arxiv.org/abs/2609.28876"
pdf_url: "https://arxiv.org/pdf/2609.28876v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "LLM Agent"
  - "时序预测"
  - "可回放环境"
  - "工具调用"
  - "记忆机制"
  - "预测市场"
  - "新闻检索"
  - "基准测试"
  - "监督微调"
  - "反馈优化"
relevance_score: 7.5
---

# Forecast-Dojo: Replayable Environments for Benchmarking and Training LLM Forecasting Agents

## 原始摘要

We introduce Forecast-Dojo, a replayable environment for benchmarking and training LLM forecasting agents. It combines resolved prediction-market questions with dated news, allowing agents to research an event and revisit their predictions at successive historical dates. The same tasks and tools support repeated evaluation, collection of training interactions, and feedback from recorded outcomes without waiting for new events to resolve. Forecast-Dojo contains 1,568 Polymarket events, split by time into training and evaluation periods, and 18.8M dated news articles. In an evaluation of 12 models, research tools lower Brier score for all 12. Forecasts also improve as events unfold, with the largest gains at steps where more newly dated evidence is recorded. Every model still trails historical market forecasts in both Brier score and accuracy. A belief notebook carried between dates lowers research cost but does not consistently improve forecast quality. Beyond evaluation, Forecast-Dojo provides interaction trajectories and outcome feedback for agent learning, with supervised fine-tuning as a proof of concept.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决 LLM 预测智能体在评测与训练中缺乏可重放、时间对齐环境的问题。研究背景是：LLM 智能体正被用于预测真实事件，而预测本质上是时间依赖的——随着新证据出现，同一问题在不同时间构成不同的预测任务，智能体需要不断更新信念。现有基准各有不足：实时基准使用未解决问题，问题随世界自然演化，但依赖真实时钟，无法为后发布的模型重建过去的预测条件，且结果需等到事件解决才能评分，拖慢评测并使训练不可行；历史基准虽能重建过去的信息截止点、立即评分并复用，但通常只在单一历史时点评估，无法沿时间多次重访同一问题。因此，本文提出 Forecast-Dojo，将已解决的预测市场问题与带日期的新闻结合，把每个事件重放为固定序列的历史预测步骤：智能体在每一步只能检索该日期之前的新闻并提交概率预测，环境保留真实结果用于即时评分但绝不泄露给智能体。其核心目标是构建一个既可复现评测、又能收集交互轨迹与结果反馈用于训练的统一环境，从而在相同任务和信息截止条件下公平比较模型，并支持监督微调等智能体学习。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，ForecastQA通过时间限制新闻，Autocast将预测问题与带日期文章及历史人类预测配对；Bench to the Future使用冻结研究语料，BTF-2记录轨迹以区分信息收集与判断；MIRAI提供基于代码的事件与新闻访问；WorldReasoner评估结果、证据与推理质量；FutureSim研究回放世界中的长程适应。应用类方面，ForecastBench与FutureX收集未解决事件的预测，另有工作评估重复预测、宏观经济即时预测与模拟市场决策。评测与训练环境类方面，MLE-Dojo提供可执行的机器学习工程任务与反馈，近期方法采用强化学习、基于结果的微调及新闻衍生问题。

与这些工作相比，本文的区别在于：使用已解决事件支持可重复研究与即时结果反馈，并将市场概率排除在预测提示之外；把时间推进作为实验设计的一部分，在每个事件固定的历史检查点上回放，生成所有智能体共享的匹配纵向轨迹，从而在相同信息状态下比较模型并受控研究预测质量随新证据的变化；同时提供共享任务与工具接口，用于收集研究交互并在独立事件上评估智能体，SFT实验仅作为该接口的一种用法示例。

### Q3: 论文如何解决这个问题？

Forecast-Dojo 的核心思路是将预测建模为可重放、可交互的序列决策任务，而非一次性问答。整体框架由三部分构成：事件与信息语料、交互式预测运行时、以及评估与学习记录。

在任务定义上，每个事件 Q 对应一组互斥结果，并在事件关闭前的有序日期 τ₁<…<τ_T 上设置多个预测步。每一步中，智能体只能访问截至当前日期的信息子集 I_{≤τ_t}，通过搜索、阅读、计算三类工具开展研究，最后输出概率分布 p_{Q,t}。同一步内的研究路径由智能体自主决定，因此同一日期可产生不同轨迹。

在环境实例化上，作者从 Polymarket 选取 1,568 个已解决事件，按时间划分为训练期与评估期，避免同一事件跨集。语料来自 CC-News，经质量过滤、去重后得到约 1,880 万篇带时间戳新闻，并用 Qwen3-Embedding-8B 嵌入、FAISS 索引。为保证时间完整性，文章日期通过结构化元数据级联提取，检索时按 UTC 日期过滤，防止未来信息泄漏。预测日期采用次线性调度，从每个事件中选取 3–10 个步，优先选择市场信念变动大或新闻活动密集的日期。

关键技术包括：记忆机制上区分 memory-free 与 memory-on，后者通过 belief notebook M_t 在步间传递评估摘要；工具接口统一为 search、scrape、python；评估支持 Brier 分数、准确率、ECE、Information-α 等步级与轨迹级指标。创新点在于：同一任务接口同时支持基准评测与训练，交互轨迹 H_t 与结果反馈可被监督微调等学习方法直接消费，实现“可重放环境”下的评估—学习闭环。

### Q4: 论文做了哪些实验？

论文在Forecast-Dojo环境中评估了12个专有与开源模型，测试集为230个留出事件、797个事件-日期对，每个配置进行4次rollout。实验设置三种条件：无工具（单次调用直接预测）、无记忆工具（使用日期受限搜索、文章检索和Python，每个预测日期从全新上下文开始）、有记忆工具（额外传递上一日期的信念笔记本）。对比方法包括均匀分布参考和历史市场概率参考。评价指标为多分类Brier分数、Top-label准确率和Information-α。主要结果：研究工具使全部12个模型的Brier分数下降、准确率提升，例如GPT-5.5的Brier从0.698降至0.564，准确率从43.85%升至57.69%；DeepSeek-V3.2从0.805降至0.655。GPT-5.6 Sol在两种工具设置下Brier最低（0.554和0.546）。所有模型仍落后于市场参考（Brier 0.498、准确率64.5%）。记忆功能降低研究成本，但未持续提升预测质量。此外还进行了纵向分析、证据捕获相关性分析，并以监督微调作为概念验证。

### Q5: 有什么可以进一步探索的点？

论文的局限主要有三点：一是所有模型在Brier分数和准确率上仍落后于历史市场预测，说明LLM智能体尚未真正超越人类集体智慧；二是belief notebook虽降低研究成本，却未稳定提升预测质量，说明跨时间记忆机制的设计仍不成熟；三是监督微调仅作为概念验证，未验证强化学习或在线反馈等更强的学习范式。未来可从以下方向探索：第一，将市场隐含概率作为训练信号而非仅作基线，通过蒸馏或对比学习让智能体逼近市场效率；第二，改进belief notebook的结构化表示，例如引入信念置信度、证据溯源和冲突检测，使其真正服务于推理而非仅作缓存；第三，研究工具调用策略的自适应选择，让智能体学会判断何时需要检索新证据、何时依赖已有信念；第四，扩展到多智能体辩论或协作预测，利用不同模型的互补性；第五，引入因果推理模块，区分相关新闻与真正驱动事件结果的因果因素，从而提升对未见过事件类型的泛化能力。

### Q6: 总结一下论文的主要内容

论文提出了 Forecast-Dojo，一个可重放的环境，用于评测和训练 LLM 预测智能体。其核心问题是：现有预测基准要么依赖实时未解决问题、无法重放，要么只在单一历史时点评估，难以支持跨时间步的受控比较与训练。Forecast-Dojo 将已解决的 Polymarket 事件与带日期的新闻结合，让智能体在事件展开的多个历史日期上研究证据并更新预测。数据集包含 1,568 个事件、6,122 个预测步骤和 1,880 万篇 CC-News 文章，并按时间划分为训练集与评测集。实验评估了 12 个模型，发现研究工具能降低所有模型的 Brier 分数，预测随事件推进而改善，但所有模型仍落后于历史市场预测；信念笔记本可降低研究成本，却未稳定提升预测质量。最后，基于交互轨迹的监督微调验证了该环境用于智能体学习的可行性。
