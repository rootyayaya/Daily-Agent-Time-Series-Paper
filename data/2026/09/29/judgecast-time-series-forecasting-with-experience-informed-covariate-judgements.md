---
title: "JudgeCast: Time Series Forecasting with Experience-Informed Covariate Judgements"
authors:
  - "Donguk Kwon"
  - "Wooseok Jeong"
  - "Dongha Lee"
date: "2026-09-29"
arxiv_id: "2609.36966"
arxiv_url: "https://arxiv.org/abs/2609.36966"
pdf_url: "https://arxiv.org/pdf/2609.36966v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "时间序列预测"
  - "协变量判断"
  - "LLM智能体"
  - "经验学习"
  - "反馈优化"
  - "时序基础模型"
  - "judgmental adjustment"
  - "残差引导"
  - "自进化"
relevance_score: 7.5
---

# JudgeCast: Time Series Forecasting with Experience-Informed Covariate Judgements

## 原始摘要

Covariate effects vary across contexts and shift over time, requiring forecasters to assess how to use them for each forecasting context. As forecasting proceeds, observations for earlier forecasts become available, providing feedback on past covariate use for subsequent forecasts. However, when multiple covariates act together, the forecast error reveals the numerical discrepancy from the observation but not how the covariates should have been used. We introduce JudgeCast, an experience-based framework for time series forecasting with covariates. Following the judgmental adjustment practice, a frozen TSFM provides the base forecast, while a frozen LLM uses the current context and relevant experience to adjust it. Within the adjustment, assessing covariate effects and determining the numerical adjustment serve distinct roles, so JudgeCast first forms explicit covariate-wise judgments and then determines the adjustment. After observation, JudgeCast uses the observed residual of the base forecast to reconstruct alternative judgments and evaluates the original and alternatives through their resulting adjustments. The best-performing decision is selected and retained as validated experience for subsequent forecasts. Across diverse real-world datasets, JudgeCast outperforms strong baselines. Ablations show that explicit covariate-wise judgment can improve forecast-time adjustment, while residual-guided experience construction yields more reliable forecasting gains than retaining raw decisions as experience.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决在带协变量的时间序列预测中，如何从预测反馈中构建可复用经验以指导未来预测的问题。研究背景是：时间序列基础模型（TSFM）已能提供强零样本预测，但目标未来还可能受协变量影响，且协变量效应随情境变化并随时间漂移，因此预测器需要针对每个预测情境判断如何使用协变量。现有方法要么在生成预测时直接融合上下文信息，要么通过重训练或参数高效微调把预测误差反馈进模型，但反复更新会带来额外计算与延迟，且在模型参数不可更新时不可用。近期一些方法尝试不更新参数，仅从预测误差中提炼反思或指导并保留为经验，但当多个协变量共同作用时，预测误差只揭示与观测值的数值偏差，并不能唯一说明各协变量应如何被评估和使用。例如雨天促销下需求高于预测，可能是促销被低估、降雨抑制效应被高估，或降雨改变了促销响应方式。因此，本文的核心问题是：如何利用观测后得到的基预测残差，重构并验证关于协变量使用的判断，从而形成可复用的经验，用于后续预测时的判断性调整，且无需更新模型参数。

### Q2: 有哪些相关研究？

本文的相关研究主要分为三类。方法类方面，现有协变量感知预测方法将协变量与目标变量一同输入预测函数，近期工作还用统计先验或外部上下文知识引导条件建模，但协变量效应是在预测生成过程中隐式建模的，而非显式表示为逐协变量判断；事后归因方法也只在预测完成后量化协变量贡献，而非作为预测时的决策。应用类方面，基于LLM的时间序列预测方法会检索历史案例、利用预测误差改进上下文推理或生成预测指导，MemCast更是将预测结果、推理轨迹和时间特征组织为分层经验，但这些方法复用的是案例、误差、反思、指导或轨迹，并未利用观测值重构预测时关于上下文使用方式的决策。评测与调整类方面，自动化判断调整保持原预测器固定并在其上叠加调整层，已有工作用智能体结合外部信息修正预测、训练LLM修正预测、用LLM引导残差学习纠正冻结骨干，或检索相似历史序列进行事后修正，检索式共形方法则用历史残差做区间校准。与这些工作不同，JudgeCast显式分离协变量效应评估与数值调整，形成逐协变量判断，并用观测残差重构替代判断、筛选验证经验，用于后续预测。

### Q3: 论文如何解决这个问题？

JudgeCast 将协变量预测建模为对基础预测的“判断性调整”，整体框架由冻结的 TSFM、冻结的 LLM 和可累积的经验记忆三部分组成。每个预测窗口内，TSFM 仅依据目标序列历史生成基础预测 ŷ^base；LLM 则结合当前上下文与检索到的相关经验，先形成显式的逐协变量判断 J∈S^{C×H}（标签集为 {--,-,0,+,++}，表示各协变量相对基础预测的方向与强度），再据此确定数值调整量 a，最终预测为 ŷ=ŷ^base+a。这一“先判断、后调整”的两阶段设计是核心创新，因为评估协变量作用与确定数值修正承担不同角色。

在经验利用上，判断阶段按归一化协变量值与基础预测的相似度检索经验 E^jud；调整阶段则按目标上下文与基础预测的相似度、并匹配协变量判断来检索 E^adj，为数值调整提供参照。

观测到真实值后，框架用基础预测的观测残差 r 进行反馈重构：由 g^alt 在不使用原判断与记忆的条件下生成 N 个备选判断，与原判断一起，各自经 g^adj 重新生成调整，再以调整与残差的误差最小者为最优判断 J*。随后进行验证，仅当调整误差优于不调整（L(r,a*)<L(r,0)）时，才将该判断、调整及其理由作为“已验证经验”写入记忆，否则记忆不变。这种残差引导的经验构建与验证机制，确保记忆只保留真正带来预测增益的决策，比直接存储原始决策更可靠。

### Q4: 论文做了哪些实验？

论文在七类真实世界数据集上开展实验：五个短期电价预测基准（NP、PJM、BE、FR、DE，含两个市场协变量）、ENTSO-e Load（小时负荷+天气协变量）和Rossmann（日零售销量+日历与促销协变量），沿用MemCast的数据划分，测试集为最后20%。对比方法包括统计方法ARIMA、Prophet，训练型方法DLinear、PatchTST、iTransformer、TimeXer、ConvTimeNet、Time-LLM，纯推理LLM方法LSTPrompt、LLM-Time、TimeReasoner，以及记忆型方法MemCast。实现上以Chronos-2为冻结TSFM、GPT-5 mini为LLM，生成N=4个替代判断并检索top-5经验，用MSE和MAE评估。主要结果：JudgeCast在全部七个数据集上取得最低MSE和MAE，较最强基线平均降低16.7%和6.5%；例如NP上MSE 19.657、MAE 2.875，ENTSO-e上MSE 2.393、MAE 0.988。消融显示显式协变量判断在短期数据集上降低MSE约3.4%–4.6%，验证经验较无经验平均降低MSE 12.1%、MAE 9.7%。此外还验证了不同TSFM/LLM骨干的稳健性、直接协变量条件化收益有限及协变量时间错位场景下的优势。

### Q5: 有什么可以进一步探索的点？

尽管 JudgeCast 在多个数据集上表现优异，但仍存在可进一步探索的空间。首先，经验记忆在测试阶段固定不变，无法在线更新，未来可研究增量式经验积累与遗忘机制，以适应概念漂移。其次，方法依赖 GPT-5 mini 等闭源 LLM，推理成本较高，可探索蒸馏到小模型或本地化部署的可行性。第三，当前仅处理数值型协变量，未涉及文本、图像等多模态协变量，可扩展至多模态判断。第四，协变量时间错位实验显示方法对偏移仍敏感，可引入显式对齐或不确定性建模。最后，判断与调整两阶段可进一步联合优化，例如用强化学习让 LLM 从残差反馈中直接学习判断策略，而非仅靠检索经验。

### Q6: 总结一下论文的主要内容

论文提出 JudgeCast，一个基于经验的时间序列协变量预测框架。问题在于：协变量效应随情境变化，而预测误差只反映数值偏差，无法说明协变量应如何被使用。方法上，JudgeCast 将协变量预测建模为对基础预测的判断性调整：冻结的 TSFM 仅依据目标历史生成基础预测，冻结的 LLM 结合当前情境与相关经验，先形成显式的逐协变量判断，再确定数值调整。观测到真实值后，利用基础预测残差重构备选判断，通过各自产生的调整进行评估，选出最优决策，且仅当调整后预测优于基础预测时才作为已验证经验存入记忆。在多个真实数据集上，JudgeCast 平均降低 16.7% MSE 和 6.5% MAE；消融表明显式协变量判断提升预测时调整，残差引导的经验构建比原始经验更可靠。
