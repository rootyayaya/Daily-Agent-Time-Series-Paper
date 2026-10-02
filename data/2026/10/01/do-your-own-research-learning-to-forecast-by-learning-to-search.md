---
title: "Do Your Own Research: Learning to Forecast by Learning to Search"
authors:
  - "Yusuf Afifi"
  - "Artur Kiulian"
  - "Anton Polishko"
  - "Mykola Khandoga"
  - "Hamudi Naanaa"
  - "Alina Krasnobrizha"
date: "2026-10-01"
arxiv_id: "2610.01955"
arxiv_url: "https://arxiv.org/abs/2610.01955"
pdf_url: "https://arxiv.org/pdf/2610.01955v1"
github_url: "https://github.com/afifi-yusuf/prime-forecast"
categories:
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "LLM Forecasting"
  - "Reinforcement Learning"
  - "Evidence Gathering"
  - "Tool Use"
  - "Financial Time Series"
  - "Temporal Reasoning"
  - "GRPO"
  - "Brier Score"
  - "Search Discipline"
relevance_score: 7.5
---

# Do Your Own Research: Learning to Forecast by Learning to Search

## 原始摘要

Outcome-based reinforcement learning can train language models to forecast real-world events, but prior forecasting work either freezes research context before training or deploys agentic research only at test time, so the skill of gathering evidence is never shaped by the reward. We introduce an agentic forecasting environment, dataset, and harness built from 2,100+ resolved Polymarket questions; the agent acquires its own context at rollout time (web search, page reading, and financial time series, all restricted by layered leak filtering to information published before each question's cutoff), and we train Qwen3.5-35B-A3B (3B active parameters) on it with single-epoch GRPO under a Brier-score reward. Training changes how the agent interacts with information: calibration improves 30-40%, and search attempts fall from 3.8 to 2.25 per rollout as evidence discipline is learned. Evaluated in an identical harness against four frontier models, the trained policy also finishes ahead of every frontier model tested at evidence-based forecasting, including Claude Opus 4.5 (soft-Brier 0.254 vs. 0.256, n=265), at about 5% of the inference cost, and its margin is widest on the hardest questions, the ones the crowd itself had not decided. We release the environment, dataset, and per-rollout records as a reusable harness for temporal forecasting agents.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决的核心问题是：如何让语言模型在真实世界事件预测中，真正学会“自主研究”这一技能，而不是仅在测试阶段临时调用检索工具，或依赖训练前冻结的静态研究上下文。

研究背景方面，Polymarket 等预测市场提供了大量带有明确截止时间和可验证结果的历史问题，为基于结果的强化学习提供了理想的训练信号。已有工作表明，用结果奖励训练模型可以提升预测能力，但这些方法要么在训练前把检索到的新闻标题或预生成的研究报告固定下来，要么只在推理阶段让冻结的模型进行多轮工具调用。前者导致模型无法通过策略改进弥补提示中缺失的信息，性能被一次性收集的上下文质量所限制；后者则使“收集证据”的能力从未被奖励信号塑造。

因此，本文要解决的关键问题是：将多轮搜索与预测的智能体流程直接嵌入强化学习训练循环，在严格的时间泄漏过滤下，让模型在 rollout 时自主决定搜什么、读哪些页面、拉取哪些时间序列，并通过 Brier 分数奖励来优化其搜索查询、证据权衡和校准能力，从而把上下文获取本身变成一个可学习的时间序列预测技能。

### Q2: 有哪些相关研究？

相关研究主要分为三类。方法类方面，DeepSeek-R1 证明了可验证奖励强化学习能激励推理能力，Search-R1 进一步将搜索纳入 RL 循环；本文借鉴这一思路，但关键区别在于把多轮“搜索—阅读—预测”脚手架整体放入训练循环，并针对已解决的历史预测问题做严格的时间泄漏过滤，使检索行为本身被奖励塑造。应用类方面，早期工作用结果型 RL 在 1 万条已解决 Polymarket 问题上训练 14B 模型，或微调 gpt-oss-120b 逼近 Gemini 3 Pro，但二者都在训练前冻结研究上下文（粘贴标题或预生成研究阶段），性能受限于一次性收集的信息质量；本文则让智能体在 rollout 时自行获取上下文，包括网页搜索、页面阅读和金融时间序列，从而突破冻结上下文的天花板。评测类方面，已有工作在测试时引入多轮工具调用与显式信念状态更新，但冻结模型、仅优化检索脚手架，通常只能接近群体准确率；本文在相同 harness 下对训练前后策略与四个前沿模型做同工具、同过滤、同轮次预算的对比，并聚焦不提供市场价格的“基于证据的预测”，在困难问题上优势最明显。此外，与从固定数值窗口预测的时间序列基础模型不同，本文让智能体自行选择上下文，把上下文获取本身作为可学习的时间序列技能。

### Q3: 论文如何解决这个问题？

论文的核心思路是把“预测”从静态的上下文推理问题，重构为可训练的智能体研究过程。整体框架由三部分组成：一是基于2100余个已结算Polymarket问题构建的智能体预测环境与数据集；二是带多层防泄漏过滤的预截止信息环境；三是基于结果奖励的强化学习训练流程。

在架构上，智能体在每轮任务中面对一个二元问题、结算标准和预测截止日期，需在截止前信息约束下进行多轮工具调用，包括网页搜索、URL阅读与摘要、截断至截止日的金融时间序列、修订日期维基百科、趋势外推工具，最终提交概率与理由。系统提示要求显式维护信念状态，每次工具调用都携带更新后的概率和证据列表，从而形成可审计的概率更新轨迹。

防泄漏是方法有效性的关键，检索内容需通过三层过滤：预测市场域名黑名单、基于发布日期的启发式过滤、以及由Claude Haiku逐条判断保留或丢弃，以拦截无日期页面和间接结果泄露。

训练目标采用严格适当的Brier分数奖励，提交概率p获得1-(p-y)^2，未提交仅得0.55。策略在隐藏市场价格工具的条件下，用单轮GRPO和LoRA微调Qwen3.5-35B-A3B，仅3B激活参数。创新点在于让“收集证据”这一技能直接由奖励塑造，而非冻结上下文或仅在测试时启用研究，从而同时提升校准度并减少搜索次数。

### Q4: 论文做了哪些实验？

论文在统一的智能体环境中进行了系统性实验。实验设置上，所有策略（训练后的Qwen3.5-35B-A3B、未训练基座、Claude Opus 4.5、Claude Sonnet 4.5、Gemini 3.1 Pro、Gemini 3.6 Flash）使用相同工具、泄漏过滤、轮次与搜索预算；Qwen策略由训练平台推理栈服务，前沿模型通过API代理运行。数据集来自2100+个已解决的Polymarket问题，测试集为265题，并预先声明了104个截止价格在[0.30,0.70]的不确定子集。评价指标为soft-Brier和ECE，均越低越好，且不访问市场价格。主要结果：训练策略在证据型预测上超过所有前沿模型，soft-Brier为0.254，略胜Claude Opus 4.5的0.256，领先Sonnet、Gemini Pro和Flash约0.019–0.032，推理成本仅约5%。在困难子集上优势扩大，训练策略0.274，领先Opus 0.007、Sonnet 0.021、Pro/Flash 0.042–0.045。训练还使ECE从0.185降至0.128（约31%），提交率从79%升至约100%，每次rollout搜索次数从3.8降至2.25。

### Q5: 有什么可以进一步探索的点？

论文的局限首先在于任务形态单一：目前仅覆盖二元预测市场，而现实决策常涉及多类别、连续值与结构化结果，Brier 奖励难以直接迁移。其次，动作空间受限，agent 只能搜索和读网页，无法调用沙箱内的定量模型、代码执行或统计工具，这限制了它在需要数值建模的问题上的上限。第三，训练仅单轮 GRPO，未探索多轮迭代、课程学习或更大规模策略，也未系统分析奖励稀疏与搜索行为退化的边界。未来可探索：将环境扩展到分类与序数结果，设计合适的严格proper scoring rule；允许 agent 自主构建并运行量化模型，把工具使用纳入奖励塑形；研究搜索预算与准确率的权衡曲线，避免“少搜即好”的捷径；以及跨市场、跨时间的泛化与泄漏鲁棒性验证。此外，可引入不确定性感知的停止准则，让模型学会何时停止研究，这对实际部署尤为关键。

### Q6: 总结一下论文的主要内容

本论文研究如何训练语言模型进行真实事件预测。现有工作要么在训练前冻结研究上下文，要么仅在测试时部署智能体研究，导致“收集证据”这一技能从未被奖励信号塑造。为此，作者构建了基于2100多个已结算Polymarket问题的智能体预测环境、数据集与评测框架，智能体在 rollout 时自行获取上下文（网络搜索、页面阅读、金融时间序列），并通过分层泄漏过滤限制为问题截止前发布的信息。作者用单轮 GRPO 和 Brier 分数奖励训练 Qwen3.5-35B-A3B（激活参数3B）。结果显示：校准提升30-40%，每次 rollout 的搜索次数从3.8降至2.25，表明模型学会了证据纪律；在相同框架下，其基于证据的预测优于包括 Claude Opus 4.5 在内的所有前沿模型（soft-Brier 0.254 对 0.256），推理成本仅约5%，且在人群本身未决的最难问题上优势最大。论文开源了环境、数据集与逐次 rollout 记录，为时间预测智能体提供可复用框架。
