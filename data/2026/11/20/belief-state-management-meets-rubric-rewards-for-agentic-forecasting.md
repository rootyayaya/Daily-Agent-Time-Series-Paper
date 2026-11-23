---
title: "Belief-State Management Meets Rubric Rewards for Agentic Forecasting"
authors:
  - "Jingyi Chai"
  - "Yun Liao"
  - "Hao Lu"
  - "Kemeng Zhang"
  - "Bingyang Zheng"
  - "Yujie Ge"
  - "Xiangrui Liu"
  - "Linfeng Zhang"
  - "Siheng Chen"
date: "2026-11-20"
arxiv_id: "2611.27286"
arxiv_url: "https://arxiv.org/abs/2611.27286"
pdf_url: "https://arxiv.org/pdf/2611.27286v1"
categories:
  - "cs.AI"
  - "cs.CL"
tags:
  - "LLM Agent"
  - "Belief-State Management"
  - "Rubric Rewards"
  - "Forecasting"
  - "ReAct"
  - "PPO"
  - "GRPO"
  - "Process Reward"
  - "Context Compression"
  - "Agentic Forecasting"
relevance_score: 7.5
---

# Belief-State Management Meets Rubric Rewards for Agentic Forecasting

## 原始摘要

Current large language model (LLM) agents still struggle to forecast real-world events. This stems from two primary limitations: i) standard ReAct harness accumulates reasoning and evidence within one growing context, and ii) outcome-based rewards in forecasting lead to a slow and noisy signal that cannot distinguish sound reasoning from lucky guesses. To address these, we introduce a forecasting training framework including harness design and post-training. For the harness side, we propose Proactive Belief-State Management (PBM), equipping agents with a fold tool to compress lengthy context into compact belief states and reset the context for subsequent exploration. For the training side, we develop SEIPH, a five-dimensional, outcome-blind rubric, providing process-quality rewards. Using the rubric-based reward, we post-train a 35B model with PPO and GRPO, yielding DeepForecaster-PPO and DeepForecaster-GRPO. Theoretically, we prove that idealized fold-based stopping converges and calibrated local rewards reduce segment-level gradient variance. Empirically, DeepForecaster-PPO (35B) achieves the best Brier score on both ForecastBench and Polymarket-Sim, outperforming frontier agents based on DeepSeek-V4-Pro (1.6T), Kimi-K2.6 (1T), and GPT-5.5. DeepForecaster-GRPO ranks second on both FutureX metrics. Ablations reveal that PBM also improves the untrained base model without any training. Calibration analysis shows that DeepForecaster-PPO makes more accurate high-confidence predictions than Qwen3.6 and GPT-5.5. Trajectory analysis further shows that forecasts generally improve from the first to the final belief state as agents gather evidence and revise their judgments.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是大语言模型智能体在真实世界事件预测任务上的表现不足问题。研究背景在于，预测任务要求智能体从多源检索及时证据、在不确定性下推理竞争情景，并在事件揭晓前给出校准概率，且由于实时问题在预测时没有标签，它构成了一个无污染、高要求的智能体测试平台。然而实验发现，当前先进智能体在预测上仍表现糟糕，常夸大证据、把预测当作检索任务、逻辑不合理、缺乏支撑就更新概率。

现有方法存在两方面不足：其一，标准 ReAct 式框架把所有工具观察和推理累积在单一不断增长的上下文中，轨迹变长后陈旧证据和冗余检索结果挤占上下文窗口，难以整合成连贯预测；其二，基于结果的强化学习奖励存在奖励稀疏缓慢（事件揭晓常需数周甚至数月）和噪声大（错误逻辑也可能猜对结果）的问题，仅优化结果正确性会奖励虚假相关而非稳健推理。

因此，本文要解决的核心问题是：如何设计更合适的智能体框架与训练信号，使预测智能体既能避免上下文溢出、开展聚焦的多线索探索，又能获得可区分推理质量的过程级奖励，从而训练出校准良好、推理稳健的预测智能体。为此作者提出主动信念状态管理（PBM）框架与 SEIPH 五维、结果无关的评分量表奖励，并结合 PPO/GRPO 进行后训练。

### Q2: 有哪些相关研究？

本文的相关工作可分为四类。**通用智能体框架类**：已有研究通过组织工具调用、记忆与交互历史来提升长程LLM智能体，并发展出上下文工程、结构化轨迹折叠、上下文压缩训练等方法；但这些通用记忆与压缩手段并未显式追踪预测所需的不确定性、竞争假设与概率更新。**预测专用框架类**：现有预测框架分为多智能体与单智能体两种设计，前者为搜索、证据综合、预测分配独立角色以并行探索，后者保持统一研究循环，如Bayesian Linguistic Forecaster在每次工具调用时维护概率估计与证据摘要，Milkyway则回访未决问题并更新预测状态；它们虽强调持续状态追踪，却忽略了单条预测轨迹中累积的搜索结果，本文的PBM正是以折叠工具压缩长上下文并重置上下文来弥补这一缺口。**结果型奖励类**：近期工作用真实事件、市场结果或延迟标签训练预测智能体，奖励与最终正确性直接挂钩，但信号延迟且噪声大，幸运猜测与有据预测难以区分，导致信用分配稀疏并可能强化捷径。**评分量表奖励类**：Echo为预测选取领域特定行为量表，FinanceHarness用专家设计量表评估金融研究过程，另有研究探索自适应或可复用量表；这些工作表明量表能提供及时可解释的反馈，但如何设计预测专用标准并在长研究轨迹上可靠分配信用仍待解决，本文的SEIPH五维结果盲量表即针对此问题提出。

### Q3: 论文如何解决这个问题？

论文提出“预测训练框架”，从执行框架与后训练两方面协同解决上下文膨胀与奖励信号稀疏问题。框架侧的核心是主动信念状态管理（PBM）：在标准搜索与访问工具之外增加 fold 工具，由智能体自主决定何时折叠。每次折叠时，智能体以结构化参数写入四类信念状态——Foresight（当前概率分布、关键结论及证据到概率的推理链）、Evidence（累积事实、数字与来源）、Search history（各段搜索与发现摘要）、Todo（剩余高产出研究方向）；其中 Foresight 与 Todo 每次覆盖更新，Evidence 与 Search history 追加保留。折叠后，执行框架丢弃当前段全部原始搜索与访问消息，将上下文重置为原始问题加渲染后的信念状态，使智能体在紧凑起点上继续探索多条独立证据线，避免上下文溢出；当判断进一步研究难以改变预测时直接输出最终预测。该机制同时天然形成训练所需的段边界，每段可独立评估过程质量。训练侧提出 SEIPH 五维评分量表（Search、Evidence、Inference、Probability、History），每维含三条准则并按 0/1/2 离散打分、归一化后取五维均值得到 U_k；再与硬有效性门控 G_k 结合形成段级奖励 r_k=G_kU_k-(1-G_k)，对编造事实、信念状态幻觉或扭曲、目标时间漂移、结果泄漏、非法概率等致命错误施以 -1 惩罚，普通工具错误等轻微缺陷则由 U_k 自然体现。利用该段级过程奖励，作者以 PPO 与 GRPO 对 35B 模型后训练，得到 DeepForecaster-PPO 与 DeepForecaster-GRPO。理论上证明基于折叠的停止策略在镜像下降下收敛到最优截断点，且校准的局部奖励在保持期望策略梯度不变的同时降低段级梯度方差。

### Q4: 论文做了哪些实验？

论文在三个实时预测基准上评估智能体：FutureX（覆盖政治、经济、科技、体育等195个网站的问题，用L1精确准确率和L2集合级F1衡量）、ForecastBench（每两周发布预测市场与真实时间序列问题，用Brier分数衡量，截至2026年9月16日共229道已解决问题）、Polymarket-Sim（Polymarket问题，覆盖2026年8月31日至9月5日的126道已解决问题，报告Brier、Alpha和准确率）。对比方法包括五个前沿模型（GPT-5.5、GLM-5.2、Kimi-K2.6、DeepSeek-V4-Pro、DeepSeek-V4-Flash）、基座Qwen3.6-35B-A3B、未训练的Qwen3.6-PBM，以及经SFT和PPO/GRPO训练的DeepForecaster-PPO与DeepForecaster-GRPO。主要结果：DeepForecaster-PPO在ForecastBench（Brier 0.151，优于Kimi-K2.6的0.175和GPT-5.5的0.184）和Polymarket-Sim（Brier 0.147、Alpha -0.012）上均取得最佳，35B模型超越参数量高达45倍的前沿智能体；DeepForecaster-GRPO在FutureX的L1（82.89）和L2（73.54）上排名第二。消融实验显示，仅使用PBM框架即可将Polymarket-Sim的Brier从0.221降至0.193、Alpha从-0.087提升至-0.059；在ReAct框架下，PPO反而劣于基座模型，说明PBM分段为基于评分标准的强化学习提供了更密集有效的反馈。校准分析表明，DeepForecaster-PPO在置信度不低于0.9的26次预测全部正确，而Qwen3.6和GPT-5.5在高置信区间存在过度自信。轨迹分析显示，强化学习后折叠次数增加（PPO 3.95、GRPO 4.22），响应长度分别增长13.9%和24.3%，且预测通常随信念状态更新而改善。人类基线Brier为0.134、准确率81.75%，仍优于所有LLM智能体。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于：PBM 的 fold 压缩与信念状态更新依赖启发式触发，压缩比和重置时机缺乏自适应机制，长程任务中可能丢失关键证据；SEIPH 五维评分虽为过程奖励，但维度权重与评分标准由人工设定，存在与真实预测质量错配的风险，且 rubric 奖励可能被策略“刷分”而偏离校准；实验集中在 ForecastBench 与 Polymarket-Sim 两类基准，事件类型与时间跨度有限，跨领域泛化未验证；与人类基线仍有差距，尤其在高不确定性事件上。

未来可探索：一是让 fold 的触发与压缩粒度由模型学习，而非固定规则，并引入可回溯的证据记忆库以缓解信息丢失；二是用少量结果信号对 rubric 做在线校准或元学习权重，降低奖励黑客风险；三是将信念状态显式建模为概率分布并加入校准约束，直接优化 Brier 分解项；四是扩展到多模态证据与更长时程事件，并研究 PPO 与 GRPO 在不同不确定性区间的互补性。

### Q6: 总结一下论文的主要内容

论文针对LLM智能体在真实事件预测中的两大瓶颈：标准ReAct框架将推理与证据不断堆积在单一持续增长的上下文中，以及基于结果的奖励信号稀疏、延迟且难以区分合理推理与侥幸猜测。为此提出DeepForecaster训练框架，包含执行框架与后训练两部分。框架侧设计主动信念状态管理（PBM），为智能体配备fold工具，将冗长上下文压缩为紧凑信念状态并重置上下文以继续探索；训练侧提出SEIPH五维、结果盲的评分量表，提供过程质量奖励。基于该奖励，用PPO和GRPO对35B模型进行后训练，得到DeepForecaster-PPO与DeepForecaster-GRPO。理论上证明理想化fold停止收敛，校准的局部奖励降低片段级梯度方差。实验上，DeepForecaster-PPO在ForecastBench和Polymarket-Sim上取得最佳Brier分数，超越基于DeepSeek-V4-Pro、Kimi-K2.6和GPT-5.5的前沿智能体；消融显示PBM无需训练即可提升基座模型，校准分析表明其高置信预测更准确，轨迹分析显示预测随证据积累逐步改善。
