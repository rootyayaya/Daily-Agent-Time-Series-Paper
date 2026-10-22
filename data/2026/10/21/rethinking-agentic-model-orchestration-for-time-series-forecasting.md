---
title: "Rethinking Agentic Model Orchestration for Time Series Forecasting"
authors:
  - "Tong Guan"
  - "Tianxiang Zhan"
  - "Shirui Pan"
  - "Ming Jin"
date: "2026-10-21"
arxiv_id: "2610.29504"
arxiv_url: "https://arxiv.org/abs/2610.29504"
pdf_url: "https://arxiv.org/pdf/2610.29504v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Agentic Model Orchestration"
  - "Time Series Forecasting"
  - "Foundation Models"
  - "Model Selection"
  - "Controlled Evaluation"
  - "GIFT-Eval"
  - "Complementarity"
  - "Historical Evidence Saturation"
relevance_score: 7.5
---

# Rethinking Agentic Model Orchestration for Time Series Forecasting

## 原始摘要

Time series foundation models (TSFMs) perform unevenly across forecasting tasks. Recent work uses agentic model orchestration (AMO) to select or combine TSFMs, often outperforming individual forecasters. Yet these gains may reflect stronger or more complementary candidates rather than better orchestration. To disentangle these effects, we introduce FairAMO, a controlled evaluation protocol with frozen candidate forecasts. Experiments on GIFT-Eval show that AMO improves accuracy, but its gains are bounded by the candidate TSFMs. The best orchestrators reduce MASE by less than 6% relative to the best single TSFM across all tasks. These gains depend on complementarity (different candidates excel on different tasks) rather than the number of candidates. Adding members yields diminishing returns, and a redundant member can erase these gains. The value of historical evidence also saturates quickly. A few recent windows capture all gains, and further history adds none. These findings separate system-level forecasting gains from the contribution of orchestration itself.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是时间序列预测中的智能体模型编排（AMO）问题。研究背景是：时间序列基础模型（TSFM）在不同任务上表现差异明显，没有单一模型能在所有数据集和预测设置下都最优，例如 TimesFM 擅长长时程预测、Moirai 擅长多变量与协变量、Chronos 擅长短单变量季节性建模。因此，近期工作提出用智能体编排来动态选择或组合多个 TSFM，并在 GIFT-Eval 等榜单上取得领先成绩。

现有方法的不足在于：这些 AMO 系统使用不同的候选模型池进行评估，缺乏受控对比，导致观测到的系统性能同时混杂了三个因素——候选模型强度、候选模型互补性以及编排能力本身。因此，榜单上的提升未必来自编排机制，而可能只是候选模型更强或更互补。

本文要解决的核心问题是：如何将系统级预测收益与编排本身的贡献区分开来。为此作者提出 FairAMO 受控评估协议，基于冻结的预测库，让所有编排器在相同候选预测、相同历史证据和相同评测指标下比较，并独立变化候选池组成、规模和证据预算，从而系统分析编排的真实增益及其边界。

### Q2: 有哪些相关研究？

本文的相关研究可按编排机制分为三类。第一类是LLM介导的编排，代表工作有MoiraiAgent、TSOrchestra的agent以及TimeCopilot的agent框架，它们借助大语言模型解读预测证据并指导模型选择或组合。第二类是特征条件化编排，包括TimeRouter、Toto-2.0 FnF和FFORMA，通过学习从时间序列描述符到编排决策的映射来实现自适应。第三类是基于历史误差驱动的编排，如RAES-Conductance-V和TSOrchestra SLSQP，直接依据过去的预测误差做出决策。

与上述工作不同，本文并不提出新的编排器，而是提出FairAMO这一受控评测协议，在冻结候选预测的条件下重新审视AMO的收益来源。已有工作多报告AMO优于单一TSFM，但本文指出这些增益可能来自更强或更互补的候选模型，而非编排本身。实验表明，最佳编排器相对最佳单一TSFM仅将MASE降低不到6%，且增益取决于候选间的互补性而非数量，增加成员收益递减，冗余成员甚至会抵消增益；历史证据的价值也很快饱和。此外，本文还考察了可复现性，发现MoiraiAgent、TimeRouter和Toto FnF仅提供推理产物而缺少完整训练代码，RAES-Conductance-V与TSOrchestra SLSQP则公开了决策推导与应用代码，因此本文通过复用或改造现有仓库组件来复现这些AMO方法。

### Q3: 论文如何解决这个问题？

论文提出FairAMO这一受控评估协议，将每个编排器统一视为候选TSFM的集成函数，通过三阶段框架把“编排本身的贡献”与“候选模型变强或互补”的影响分离开来。整体流程为：首先构建冻结预测库，所有M个候选TSFM只在GIFT-Eval上运行一次，不重训不微调，其分位数预测按（数据集、期限、序列、窗口、候选、分位数）缓存，库分为带真值的训练回测、可选验证回测以及隐藏真值的测试预测三个区域，所有编排器都从同一库中抽取K≤M个成员。其次是编排器拟合，在测试标签揭示前，编排器只接收允许的证据（最近N个训练回测及可选验证回测），据此产出模型选择或组合权重策略，随后提交并冻结，禁止重跑、重加权或窥视测试分数。最后是测试评估，冻结策略作用于缓存测试预测，仅在此阶段揭示标签，由官方GIFT-Eval评分器返回MASE和CRPS。主要组件包括五类参考编排器（随机、开发集选择最优、等权、Argmin路由、仅作上界的Oracle）、五个外部编排器（TimeRouter、Toto-2.0 FnF、RAES、TSOrchestra SLSQP、TimeCopilot Median）以及两个复现编排器（LLM介导的MoiraiAgent-Retrained及其数值对应Small Patch Router，后者对历史与候选预测打补丁、用共享时序Transformer编码并按注意力跨候选打分）。创新点在于以冻结候选预测实现公平对照，从而量化AMO增益的上界、揭示其依赖互补性而非成员数量、并发现历史证据价值快速饱和。

### Q4: 论文做了哪些实验？

论文在GIFT-Eval基准上采用FairAMO受控评估协议（冻结候选预测）开展实验，围绕三个研究问题展开。实验设置包括5个候选TSFM的候选池、不同池规模（2至5个成员）以及不同回测证据预算（仅验证集到100次回测）。对比方法涵盖11种可部署编排器，包括TSOrchestra SLSQP、Argmin Router、TimeRouter，以及最佳单一TSFM（TiRex2）和窗口级oracle上界。主要结果：RQ1中，最强可部署编排器TSOrchestra SLSQP达到0.658 MASE，相对最佳单一模型TiRex2的0.697仅降低5.6%（0.039），而窗口级oracle为0.580，仍留有约三分之二差距；Argmin Router为0.662，TimeRouter为0.665，且增益超过0.01的方法均依赖回测证据。RQ2中，池从2增至5时最佳单一模型几乎不变（0.699→0.697），oracle从0.647降至0.580，Argmin Router从0.689改善至0.662，实现率从18.4%升至29.8%，但增量递减；证据方面，Argmin Router在加入3次训练回测后从0.672降至0.661，随后回升至0.664，SLSQP在10次回测时达到峰值0.658后退化。RQ3中，同一Argmin Router在10个三元子集上MASE跨度为0.670–0.690（0.020），实现率从9.8%到32.3%相差三倍；含TiRex2的子集平均实现28.5%的headroom，不含者仅13.4%；最弱模型Toto2-313m加入6个二元子集中的5个后最多改善0.013 MASE，说明增益取决于误差互补性而非候选数量或强度。

### Q5: 有什么可以进一步探索的点？

论文的局限主要有三点：一是最强方法仍是简单的选择与加权规则，LLM 介导的编排贡献尚不明确，说明复杂 agent 机制未必优于轻量规则；二是每个配置仅做一次决策，无法兑现窗口级（window-level）的潜在提升空间，决策粒度太粗；三是历史证据价值快速饱和，仅少数近期窗口即捕获全部收益，长历史建模意义有限。未来可探索的方向包括：更细粒度的决策承诺，如按窗口或按预测步动态切换与加权；利用回测之外的上下文（如数据特征、任务元信息、领域知识）驱动 agent 推理，而非仅依赖历史误差；以及围绕互补误差剖面而非模型排名构建候选池，主动筛选错误模式互补的 TSFM。我的补充思路是：可将编排目标从最小化平均误差转向风险感知或分位数校准，并引入在线学习与元学习实现跨任务自适应编排；同时设计可解释的编排决策日志，以厘清 LLM 推理与简单规则各自的增益边界。

### Q6: 总结一下论文的主要内容

论文关注智能体模型编排（AMO）在时间序列预测中的真实价值。针对现有工作常将性能提升归因于编排本身的问题，作者提出 FairAMO 受控评估协议，冻结候选预测结果，从而将系统级收益与编排贡献分离。基于 GIFT-Eval 的实验表明：AMO 确实能提升精度，但增益受候选 TSFM 池限制，最优编排器相对最佳单一模型仅降低不到 6% 的 MASE；增益主要来自候选模型间的互补性而非数量，增加冗余成员甚至可能抵消收益；历史证据的价值也快速饱和，仅少数近期窗口即可捕获全部增益。结论指出，最强方法仍是简单的选择与加权规则，LLM 介导编排的作用尚不明确，未来可探索更细粒度决策与基于互补误差轮廓构建候选池。
