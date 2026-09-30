---
title: "Can Language Models Learn to Forecast Stock Prices"
authors:
  - "Jiacheng Guo"
  - "Suozhi Huang"
  - "Shuzhen Li"
  - "Yunlong Gao"
  - "Zerui Cheng"
  - "Jason Ge"
  - "Shushu Liang"
  - "Zihao Li"
  - "Hao Lu"
  - "Ming Yin"
  - "Shilong Liu"
  - "Jiashuo Liu"
  - "Xu Kuang"
  - "Mengdi Wang"
date: "2026-09-29"
arxiv_id: "2609.36914"
arxiv_url: "https://arxiv.org/abs/2609.36914"
pdf_url: "https://arxiv.org/pdf/2609.36914v1"
categories:
  - "cs.CL"
tags:
  - "LLM Agent"
  - "Tool Use"
  - "Time Series Forecasting"
  - "Financial Forecasting"
  - "Post-training"
  - "Reinforcement Learning"
  - "PPO"
  - "Evidence Gathering"
  - "Numerical Judgment"
  - "Chronological Sandbox"
relevance_score: 7.5
---

# Can Language Models Learn to Forecast Stock Prices

## 原始摘要

Post-training has been shown to significantly improve language models' performance on tasks with verifiable outcomes, including mathematical reasoning, software engineering, and computer use. However, whether the same approach can improve forecasting in financial markets is much less clear. Compared with tasks with verifiable outcomes, not only are realized returns noisy, but even what constitutes a relevant information set for making effective predictions is not obvious a priori: the model must decide which observations to gather and then commit to a numerical judgment before the outcome is known. We study this question in a chronological stock-price sandbox, where a language model gathers price, volume, relative-performance, and market-context evidence and predicts a future return. We post-train Qwen3-4B with supervised fine-tuning (SFT) on tool-use demonstrations, then proximal policy optimization (PPO) with a terminal reward given by the forecast score against the realized return. The resulting AURA-4B more than doubles the starting direction--magnitude score, from 20.94 to 43.31, and is comparable to frontier language models on this benchmark. Conditional magnitude agreement rises from 33.3 to 66.2, while directional accuracy changes from 62.9 to 65.4. SFT expands tool use, and PPO further increases the share of ranking and market-context queries. These results show that post-training can substantially improve financial forecasting performance, together with changes in how the model investigates the market, on this outcome-selected benchmark.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是：在结果可验证任务上已被证明有效的后训练方法，能否迁移到结果噪声大、且相关信息集并不先验明确的金融预测场景。股票价格预测与数学推理、软件工程等任务不同：已实现收益本身噪声很高，预测误差可能来自证据选择、证据解读或后续市场波动，最终得分无法直接指出哪次查询或观察真正有用。因此，模型必须自行决定收集哪些价格、成交量、相对表现和市场背景信息，并在结果未知前给出数值判断。现有语言模型预测研究虽已探索证据收集和利用已实现结果训练，但核心问题仍未回答：后训练能否实质提升语言模型使用工具预测未来股价的能力？本文构建市场分析沙盒和按时间顺序划分的股票预测基准，对Qwen3-4B先做工具使用示范的SFT，再用PPO以已实现收益的终端奖励优化，以分离示范学习与结果优化的增益，并观察模型调查市场行为的变化。

### Q2: 有哪些相关研究？

本文的相关研究可分为四类。方法类方面，LLMTime、Time-LLM、Chronos将语言模型用于零样本或适配式时间序列预测，Kronos则针对金融K线数据做预训练；LEAP与基于检索聚合的事件预测工作通过分解证据并汇总为概率预测。应用类方面，BloombergGPT、FinGPT将语言建模适配到金融任务，FinRL提供强化学习交易框架，FinMem则引入结构化记忆的语言智能体。评测类方面，StockBench评估序贯股票交易，Agent Market Arena在真实股票与加密市场评测智能体，KTD-Fin结合匿名化市场输入与组合归因，QuantEval和FrontierFinance分别覆盖量化知识与投资研究工作流。后训练类方面，DeepSeek-R1、SWE-Master、ComputerRL等利用可验证结果提升推理与交互能力，Future-as-Label和Mantic将结果反馈用于事件预测。与上述工作不同，本文在时序股票沙盒中让模型通过工具收集价格、成交量、相对表现与市场背景证据，并同时用SFT和PPO对调查轨迹与数值预测进行后训练，从而在同一环境中比较现有系统并训练预测模型。

### Q3: 论文如何解决这个问题？

论文的核心方法是在一个按时间顺序构建的股票预测沙盒中，对Qwen3-4B进行两阶段后训练。整体框架为：模型接收股票、决策日期、预测期限和当日VWAP，通过调用九类检索工具（个股OHLCV与技术指标、相对表现排名与残差收益、市场与行业上下文）逐步收集证据，最终提交一个对数收益率预测，目标为未来VWAP与当前VWAP之比的对数。评分函数同时考察方向与幅度：方向错误得零分，方向正确则用调和式幅度项奖励接近真实涨跌幅的预测，该分数作为终端奖励。

关键技术分两步。第一阶段为监督微调（SFT）：用GPT-5.4在教师专用上下文中，结合已实现训练收益生成多轮工具调用与数值判断的演示轨迹，共3,631条；学生模型在普通求解提示下学习这些轨迹，损失仅覆盖助手生成的token，包括分析、工具调用和最终预测，从而学会“先调查、后判断”的完整序列。第二阶段为PPO强化学习：SFT模型在训练任务上自行选择查询、观察结果并提交预测，以真实收益计算终端奖励，通过KL惩罚锚定SFT检查点，进行50轮迭代、约3,200个episode，学习率10⁻⁶。

创新点在于：将可验证结果的后训练范式迁移到噪声大、信息集不明确的金融预测；用结果条件化的演示而非独立预测来监督；并让模型在自身预测结果上继续优化，使工具使用行为与最终数值判断质量直接关联。最终AURA-4B的预测分数从20.94提升至43.31，条件幅度一致性从33.3升至66.2。

### Q4: 论文做了哪些实验？

论文在按时间顺序构建的股票价格沙盒中进行实验，语言模型需收集价格、成交量、相对表现和市场背景证据，预测未来收益。实验以Qwen3-4B为基座，先进行工具使用演示的监督微调（SFT），再用PPO以预测得分对实际收益的终端奖励进行后训练，得到AURA-4B。评测基准为240个计分测试任务（共398个任务），对比对象包括9个前沿语言模型（如GLM-5.3、Claude-Fable-5）和4个量化基线（含动量外推）。主要结果：AURA-4B得分从基座20.94提升至43.31，提升106.8%，其中SFT贡献81.2%，PPO再贡献14.2%；在15个系统中排名第三，超过9个前沿模型中的7个及全部量化基线（动量外推42.00）。条件幅度一致性从33.3升至66.2，方向准确率从62.9升至65.4。分期限看，1–10日任务AURA得48.91高于GLM的44.16，21–126日任务得35.87低于GLM的57.40。难度上，易、中、难任务得分分别为59.04、46.49、23.28。行为上，中位工具调用从5增至18（SFT）后降至16，排名与市场背景查询占比从16.2%升至38.0%。

### Q5: 有什么可以进一步探索的点？

论文的局限首先在于评测基准是“结果筛选”的：任务与样本按最终收益挑选，存在幸存者偏差，模型学到的可能是特定历史区间的模式而非可泛化信号。其次，奖励仅基于单次实现收益，噪声极大，PPO 容易过拟合噪声或学到冒险的数值输出。第三，仅用 Qwen3-4B 与单一市场沙盒，跨模型、跨资产、跨市场迁移性未知。未来可探索：一是引入多步、多资产组合预测与风险调整奖励（如夏普比率），降低单点噪声；二是加入反事实与随机化回测，检验策略在未筛选样本上的表现；三是研究工具调用策略与预测准确性的因果联系，而非仅报告相关性；四是引入不确定性校准与置信度输出，让模型在信息不足时选择弃权。此外，可尝试过程奖励、检索增强与记忆机制，并检验模型是否真正学到经济逻辑而非记忆历史价格路径。

### Q6: 总结一下论文的主要内容

本论文探讨语言模型能否通过后训练提升股价预测能力。问题定义上，作者指出金融预测与数学推理等可验证任务不同：实际收益噪声大，且有效信息集并不先验已知，模型需自行决定收集哪些观测并在结果揭晓前给出数值判断。方法上，作者构建了按时间顺序划分的股票价格沙盒与预测基准，让模型收集价格、成交量、相对表现和市场背景证据并预测未来收益；先对Qwen3-4B进行工具使用演示的监督微调（SFT），再用近端策略优化（PPO），以预测得分与已实现收益的对比作为终端奖励。主要结论：AURA-4B的预测得分从20.94提升至43.31，翻倍以上，接近前沿模型水平；条件幅度一致性从33.3升至66.2，方向准确率从62.9微升至65.4；SFT扩大了工具使用，PPO进一步提高了排序与市场背景查询占比至38.0%。这表明结果监督的后训练能显著改善金融预测表现，并改变模型调查市场的方式。
