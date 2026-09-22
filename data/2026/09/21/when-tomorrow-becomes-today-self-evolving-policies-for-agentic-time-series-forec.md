---
title: "When Tomorrow Becomes Today: Self-Evolving Policies for Agentic Time-Series Forecasting"
authors:
  - "Yifan Hu"
  - "Xilin Dai"
  - "Zhiyuan Qu"
  - "Yiding Liu"
  - "Zewei Dong"
  - "Jiang-ming Yang"
  - "Qiang Xu"
date: "2026-09-21"
arxiv_id: "2609.24862"
arxiv_url: "https://arxiv.org/abs/2609.24862"
pdf_url: "https://arxiv.org/pdf/2609.24862v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Self-Evolving Policies"
  - "Time Series Forecasting"
  - "Delayed Feedback"
  - "Orchestration Policy"
  - "Expert Trust"
  - "Agent Path Selection"
  - "Intervention Strength"
  - "Frozen Backbone"
  - "Time-MMD"
  - "LLM Agent"
  - "Tool Use"
  - "Multi-Agent Reasoning"
relevance_score: 8.5
---

# When Tomorrow Becomes Today: Self-Evolving Policies for Agentic Time-Series Forecasting

## 原始摘要

Agentic time series forecasting concerns systems whose underlying mechanisms evolve, making the relative effectiveness of numerical models, reasoning strategies, and intervention rules inherently time-varying. Consequently, a time series agent must adapt the forecasts it produces and the orchestration policy that determines which components to trust and how to coordinate them. The deployment process naturally provides supervision for this adaptation as forecast horizons elapse and realized targets reveal the effectiveness of earlier decisions. Committing all numerical expert forecasts and candidate agent paths before target observation allows each realized outcome to evaluate the entire alternative set, providing delayed feedback without additional annotation. However, existing time series agents primarily incorporate prior experience through forecast refinement, reflection, or retrieval, without systematically converting realized outcomes into persistent updates to the joint orchestration policy governing later origins. To exploit this delayed feedback systematically, we introduce TimEvolve, a frozen-backbone time series agent that converts each realized outcome into persistent joint updates of expert trust, agent path selection, and intervention strength. A temporally ordered predict, reveal, and update protocol applies this feedback to subsequent forecasts. Experiments across eight Time-MMD domains show that TimEvolve achieves the best average MSE and MAE ranks among fifteen methods and the lowest errors on both metrics in seven domains. These results demonstrate the value of learning forecasting policies from the futures encountered during deployment.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是“智能体化时间序列预测”中一个被忽视的核心矛盾：当系统机制随时间漂移、趋势突变或外部事件改变动态时，数值模型、推理策略与干预规则的相对有效性本身是时变的，但现有时间序列智能体却主要依赖预测精炼、反思或检索来利用历史经验，并未系统性地把部署过程中真实揭晓的结果转化为对“联合编排策略”的持久更新。换言之，它们能改进当前这一次预测，却无法持续校准“该信任哪些数值专家、该选择哪条证据驱动的智能体路径、该以多强力度修正数值先验”这些后续预测所依赖的决策规则。本文要解决的核心问题，正是如何利用预测目标揭晓后自然产生的延迟反馈，在语言模型、数值预测器、分析工具和提示均保持冻结的前提下，将已实现结果转化为对专家信任、路径选择与干预强度的协同、持久更新，从而让智能体在部署中不断演化其预测策略，而非仅做一次性的预测修正。

### Q2: 有哪些相关研究？

现有相关研究主要可分为三类。**方法类**：Cast-R1 通过监督与强化学习训练工具增强的序列决策策略；KairosAgent 将工具驱动的语义推理与时间序列基础模型结合，并用预测目标优化推理器；Last-mile agents 利用弱结构化上下文证据修正数值预测并保留事后反思。这些工作将预测从数值映射扩展为选择工具、解释证据、调用专家与精炼候选的智能体流程，但主要聚焦预测构建与经验使用，未系统地将已实现结果转化为持久策略更新。**在线学习与专家集成类**：在线专家建议学习利用观测损失更新专家权重，OneNet 通过在线集成应对概念漂移，MoE-F 为语言模型专家混合开发在线门控。它们用结果反馈调整专家分配，但未联合适配智能体路径与干预强度。**记忆反馈类**：Reflexion 将环境反馈转为文本经验，MemCast 构建分层经验记忆并在推理时调整记忆条目置信度。本文 TimEvolve 的区别在于，将专家信任、智能体路径选择与干预强度统一为联合编排策略，并利用部署中自然揭示的延迟结果进行持久更新。

### Q3: 论文如何解决这个问题？

TimEvolve 的核心思路是把部署过程中自然产生的“延迟反馈”系统性地转化为对编排策略的持久更新，而所有预测组件保持冻结。整体框架遵循“预测—揭示—更新”的时间有序协议：在时刻 t 先提交所有专家预测与候选路径，待 t+H 目标揭示后，用真实结果同时评估整个备选集，无需额外标注。

架构上包含三个联动决策模块。EvolveTrust 维护专家信任权重，融合四个视角：训练/验证预热、在线已完成窗口、当前证据可信度、以及历史证据模式下的表现，通过 ρ_t 随标注窗口累积逐步提升在线与模式视角的贡献，形成数值先验。EvolveReason 由冻结语言模型提出结构化路径，每条路径指定证据解释、专家子集与可选修正，再用共享滚动岭回归基于连续性、范围、平滑度、结构分数五个预揭示特征预测对数 MSE 并选路。EvolveIntervene 用门控系数 α_t 在先验与选中路径间插值，其监督目标 α_t* 由最小化 MSE 的二次型解析导出，并以权重 w_t 做能量加权岭回归拟合。

创新点在于：将专家信任、路径选择、干预强度三者的联合策略统一由揭示结果监督更新，并发布为单一检查点；用损失几何推导出可识别的混合标签，使延迟反馈被系统化利用而非仅做反思或检索。

### Q4: 论文做了哪些实验？

论文在Time-MMD的八个领域（农业、气候、经济、能源、环境、安全、社会公益、交通）上评估TimEvolve，采用时间顺序70/10/20划分，报告标准化目标空间的MSE和MAE，每个预测时域单独评估并等权汇总，测试步长为1，策略更新仅使用完整时域已结束的预测。对比方法共十五种，分四组：代理基线（KairosAgent、MemCast、CastFlow）、零样本基础模型（Aurora、TimesFM-3、Chronos-2、Toto-2.0、Sundial、Moirai-Large）、全样本多模态模型（T3Time、TimeCMA、CALF）和全样本单模态模型（PatchTST、DLinear）。主要结果：TimEvolve取得最佳平均MSE/MAE排名1.250/1.375，在八个领域中的七个领先两项指标；在全部十六个领域-指标对比中优于CastFlow，对MemCast和KairosAgent各胜十四项。消融显示，相比完全冻结策略的变体，完整策略平均降低MSE 6.3%、MAE 7.6%，经济领域MSE最大降幅17.7%（0.220降至0.181），社会公益领域MAE最大降幅25.0%（0.508降至0.381）；冻结EvolveTrust退化最大，其次为EvolveReason和EvolveIntervene。

### Q5: 有什么可以进一步探索的点？

论文的局限与可拓展方向主要有三点。其一，反馈依赖“完整预测视界揭示”，在长视界或高频场景下延迟显著，未来可引入部分视界下的信用分配或时序折扣机制，加速策略收敛。其二，策略更新仅覆盖专家信任、路径选择与干预强度三类变量，未触及提示模板、工具调用顺序等更细粒度编排，可探索结构化策略空间或分层强化学习。其三，实验集中于八个领域，跨域迁移与冷启动场景下策略能否快速适配仍待验证，可研究元学习初始化或领域自适应正则。此外，当前以MSE/MAE为优化目标，未来可纳入校准性、方向准确率或决策效用等指标，并检验策略在分布突变与对抗扰动下的鲁棒性。

### Q6: 总结一下论文的主要内容

论文针对智能体时间序列预测中组件有效性随时间变化的问题，提出将部署过程中自然产生的延迟反馈转化为对编排策略的持续更新。作者将预测过程形式化为“预测—揭示—更新”协议：在目标揭示前，智能体预先提交所有数值专家预测、候选路径及最终预测；当预测窗口结束后，真实目标为已选与未选方案同时提供监督信号。基于此，论文提出 TimEvolve，一个冻结骨干的时间序列智能体，通过 EvolveTrust、EvolveReason 和 EvolveIntervene 三个模块，分别联合更新专家信任、智能体路径选择与干预强度，而语言模型、数值预测器和工具均保持冻结。在八个 Time-MMD 领域上的实验表明，TimEvolve 在十五种方法中取得最佳平均 MSE 和 MAE 排名，并在七个领域上同时取得最低误差，验证了从部署中遇到的未来结果学习预测策略的价值。
