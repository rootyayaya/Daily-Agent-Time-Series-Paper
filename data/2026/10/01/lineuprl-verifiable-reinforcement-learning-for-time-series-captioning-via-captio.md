---
title: "LineupRL: Verifiable Reinforcement Learning for Time Series Captioning via Caption-to-Series Identification"
authors:
  - "Haochen Zhang"
  - "Laura Yao"
  - "Zachary Plotkin"
  - "Gengwei Zhang"
  - "Tianlong Chen"
date: "2026-10-01"
arxiv_id: "2610.01800"
arxiv_url: "https://arxiv.org/abs/2610.01800"
pdf_url: "https://arxiv.org/pdf/2610.01800v1"
categories:
  - "cs.AI"
tags:
  - "TimeSeries2Report"
  - "Time Series Captioning"
  - "LLM Verifier"
  - "Reinforcement Learning with Verifiable Rewards"
  - "Caption-to-Series Identification"
  - "Natural Language Report Generation"
  - "Semantic Description"
  - "Signal-to-Language Bridge"
  - "Reward Hacking Resistance"
  - "Vision Language Model"
  - "Time Series Understanding"
relevance_score: 8.5
---

# LineupRL: Verifiable Reinforcement Learning for Time Series Captioning via Caption-to-Series Identification

## 原始摘要

Time series captioning is a fundamental step in time series understanding and can also serve as the bridge between signal and natural language. Supervised fine-tuning (SFT) relies on a larger model's captions and cannot exceed their quality. Reinforcement learning (RL) can, but its rewards were designed for other modalities and other tasks, and they transfer poorly to open-ended generation in the time series domain. We address this by proposing LineupRL, a reinforcement learning with verifiable rewards (RLVR) pipeline whose reward is caption-to-series identification. The reward model is a frozen large language model (LLM) verifier that reads the generated caption and the candidate time series as raw values, never the chart, and must pick the described time series from multiple distractors. Matching is a far lighter demand on the verifier than writing questions or judging a caption, so an off-the-shelf LLM can supply the reward. Across two captioning benchmarks, and on forecasting and reconstruction where the predictor sees only the caption, LineupRL outperforms SFT and RL baselines on every metric. The 3B vision language model (VLM) trained by LineupRL also outperforms, at 1/24 of the parameters, the 72B VLM whose captions the SFT baseline is distilled from. Our case study shows that LineupRL resists reward hacking, and that the captioner it trains both traces the trend and names the values at key points.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列描述（time series captioning）是连接信号与自然语言的关键任务，在医疗、金融和气候等领域有重要应用。现有方法主要依赖监督微调（SFT），但 SFT 存在两个根本缺陷：其一，它受限于监督数据的质量，学生模型无法超越合成参考描述的教师模型，还会继承其“看似合理但错误”的陈述；其二，它泛化能力差，容易记忆参考描述而非真正学会读图，导致“无根据描述”（ungrounded captioning）——语言流畅却遗漏时间序列的关键特征。强化学习（RL）虽可摆脱配对数据依赖并改善泛化，但现有奖励设计均不适用于时间序列：LLM-as-judge 奖励不可验证、易被奖励黑客攻击；answerability 奖励需要模型具备较强的时间序列理解能力来出题和判题，而当前模型尚不具备。因此，本文要解决的核心问题是：如何为时间序列描述任务设计一种可验证的强化学习奖励，使其同时满足三个条件——抵抗奖励黑客、仅需现有 LLM/VLM 能提供的匹配能力、并能奖励时间序列中重要且独特的特征。为此，作者提出 LineupRL，以“描述到序列识别”作为可验证奖励，通过冻结 LLM 在统计匹配的干扰项中选出被描述序列，从而训练出更 grounded 的描述模型。

### Q2: 有哪些相关研究？

时间序列描述（captioning）的相关研究可按三类梳理。

**方法类**：早期为规则化数据到文本系统及数据驱动模型，受限于固定规则或输出格式。随后LLM、VLM与TSLM实现开放式生成，近期工作通过SFT在合成的时间序列-描述对上微调。但SFT受监督数据质量上限约束，且易记忆参考描述、泛化差，本文称之为“无根基描述”。RL方面，图像描述常用的LLM-as-judge奖励不可验证、易被奖励黑客攻击；answerability奖励则要求模型具备较强时间序列理解能力来出题和判答，当前模型难以满足。

**应用类**：描述文本被用于领域报告、预测解释与临床预测，如新生儿重症监护中文本摘要优于趋势图。

**评测类**：CaTS-Bench、BEDTime等基准从数值细节、蕴含关系、序列-描述识别等角度评测。

本文与上述工作的区别在于：提出LineupRL，以“描述到序列识别”作为可验证奖励，由冻结LLM在统计匹配的干扰项中选出被描述序列，无需参考描述，同时规避奖励黑客与高理解门槛，并在蕴含、识别、预测与重建充分性上全面超越SFT与RL基线。

### Q3: 论文如何解决这个问题？

论文提出LineupRL，一种基于可验证奖励的强化学习（RLVR）流水线，其核心创新在于将“描述到序列的识别”作为奖励信号。整体框架包含三个组件：VLM描述器、冻结的LLM验证器以及负样本选择机制。描述器读取时间序列的折线图并生成自然语言描述；验证器接收该描述与K个候选序列（以原始数值列表形式呈现，而非图表），需从中定位被描述的序列。由于匹配任务比生成或评判描述更轻量，现成的LLM即可胜任验证器角色。关键技术包括：其一，为消除位置偏差，将真实序列依次置于K个位置各查询一次，以正确识别比例作为奖励，并缩放为r=λ·acc；其二，负样本从同长度的真实序列池中选取，通过匹配均值、标准差、最小值、最大值等汇总统计量并限制与目标序列的重叠比例，构造高难度干扰项，避免信息泄漏；其三，训练时对每个序列采样一组描述，采用RLOO估计器进行策略梯度更新，并以留一法基线降低方差。创新点在于：奖励仅通过能区分目标与近邻的陈述获得，从而抵抗奖励黑客；描述器被迫同时追踪趋势并命名关键点数值。实验表明，该方法在多个基准上超越SFT与RL基线，且3B模型以1/24参数量超过72B教师模型。

### Q4: 论文做了哪些实验？

论文在10,000个来自TSFragment-600K的片段上训练，图表仅保留少量坐标刻度，不含标题、图例、单位或逐点数值标签，迫使策略描述形状而非读取数值。识别任务统一使用K=4候选。评估覆盖三类指标：准则1（蕴含）在BEDTime和CaTS-Bench上评测，CaTS-Bench参考由Claude Opus 5改写以去除日期、地点、领域和精确值；准则2（识别）同样在两个基准上，由GLM-4-9B和Phi-4-14B两个冻结LLM打分取均值；准则3（预测与重建）在ETTh2、ETTm2、Saugeen河流流量和澳大利亚电力需求四个语料上评测。所有模型均从Qwen2.5-VL-3B-Instruct初始化并使用相同指令。对比方法包括：未调优初始化、从Qwen2.5-VL-72B-Instruct字幕蒸馏的SFT、CapRL式可回答性奖励RL、LLM-as-judge奖励RL，三种RL共享策略优化超参和冻结的Qwen2.5-14B-Instruct验证器。主要结果：LineupRL在两个字幕基准及预测、重建任务上全面超越SFT和RL基线；其训练的3B VLM以1/24参数量超过72B教师模型。案例研究表明LineupRL能抵抗奖励黑客，生成的字幕既追踪趋势又标注关键点数值。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三：其一，奖励依赖冻结 LLM 做 caption-to-series 匹配，K=4 的候选设置较简单，未来可研究候选数量、干扰项难度与奖励信号强度的关系，甚至引入自适应难例挖掘以提升判别粒度。其二，训练数据仅 1 万片段且来自 TSFragment-600K，图表去除了标题、图例与数值标签，这虽防止作弊，却也可能限制模型学习领域语义与单位信息，未来可探索在可控泄漏条件下引入部分结构化元数据。其三，评估集中在 BEDTime、CaTS-Bench 与四个预测语料，跨域、多变量、长序列与不规则采样场景尚未验证。此外，验证器与被训练策略同源（Qwen 系列）可能带来偏好偏差，可尝试异构验证器集成或可学习验证器。最后，识别奖励只保证“可区分”，不保证“充分描述”，如何设计更细粒度的可验证奖励（如关键点、趋势方向、周期性的分项校验）值得进一步探索。

### Q6: 总结一下论文的主要内容

论文针对时间序列描述生成（time series captioning）中的"无根据描述"问题展开研究。作者指出，监督微调依赖大模型合成的参考描述，导致模型只学到参考文本的风格而非真正读懂时间序列，泛化能力差且易产生貌似合理却错误的陈述；而现有的图像描述强化学习奖励（如LLM-as-judge、可回答性奖励）迁移到时间序列领域时容易被奖励黑客攻击或要求过强的时间序列理解能力。为此，论文提出LineupRL，一种基于可验证奖励的强化学习流程，其奖励为"描述到序列识别"：冻结的LLM验证器仅接收生成的描述和K个以原始数值呈现的候选序列（含统计量匹配的干扰项），需从中选出被描述的那条序列，以多次换位后的正确率作为奖励。该方法无需参考描述，能抵抗奖励黑客，并促使描述聚焦于区分性细节。实验表明，在蕴含、识别以及预测与重建充分性等指标上，LineupRL均优于SFT和现有RL基线，且其训练的3B模型以1/24参数量超越了SFT所蒸馏的72B教师模型。
