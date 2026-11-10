---
title: "Agent4Crypto: A Dual-Reflective and Market-Feedback-Aligned LLM-Based Multi-Agent System for Cryptocurrency Trading"
authors:
  - "Guangyan Gan"
  - "Jiahao Li"
  - "Jiashun Wang"
  - "Lin William Cong"
date: "2026-11-09"
arxiv_id: "2611.12269"
arxiv_url: "https://arxiv.org/abs/2611.12269"
pdf_url: "https://arxiv.org/pdf/2611.12269v1"
categories:
  - "cs.MA"
  - "cs.CL"
tags:
  - "LLM-based Multi-Agent System"
  - "Reflection"
  - "Feedback Optimization"
  - "Financial ReasoningBank"
  - "Retrieval-Augmented Generation"
  - "Counterfactual Contribution"
  - "PPO Gating Policy"
  - "Interpretable Decision Pipeline"
  - "Cryptocurrency Trading"
  - "Time Series Analysis"
relevance_score: 6.5
---

# Agent4Crypto: A Dual-Reflective and Market-Feedback-Aligned LLM-Based Multi-Agent System for Cryptocurrency Trading

## 原始摘要

Cryptocurrency markets provide a natural testbed for autonomous AI agents because they are digital-native, high-frequency, and machine-speed environments, yet existing methods often struggle with non-stationary market regimes, opaque decisions, and fixed aggregation rules. In this paper, we propose Agent4Crypto, a dual-reflective and market-feedback-aligned multi-agent system. The framework coordinates specialized agents for data collection, analysis, risk assessment, reflection, and trading, synthesizing heterogeneous signals from prices, indicators, news, and charts in an interpretable decision pipeline. Our central design is a trader-centric decision mechanism: three style-specific trader agents, Aggressive, Neutral, and Conservative, generate candidate actions and natural-language rationales from the same market context, while their influence is learned rather than manually fixed. A PPO-based gating policy dynamically allocates trader weights through a dual-reflective feedback process. One reflection stream evaluates post-trade decision quality from realized portfolio outcomes and distills reusable lessons into a Financial ReasoningBank for retrieval in subsequent trader prompts, while the other estimates trader-level counterfactual contribution, indicating which style has recently aligned better with market movements. The PPO state combines Counterfactual Contribution Memory with market features, previous trader weights, and current trader actions, so trader influence adapts across bull, sideways, and bear regimes. Experiments on BTC, ETH, and XRP show that Agent4Crypto improves total return and Sharpe ratio over traditional strategies, machine learning and reinforcement learning baselines, and existing LLM-based trading systems, demonstrating the value of interpretable trader competition and market-feedback-driven adaptation in volatile cryptocurrency markets.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决加密货币市场中自动化交易策略难以适应非平稳市场环境、决策不透明以及多智能体聚合方式僵化的问题。研究背景方面，加密货币市场具有7×24小时运行、高频波动、频繁且剧烈的市场状态切换等特征，是检验自主AI智能体的理想试验场，但策略在某一时期表现良好后往往迅速失效，如何适应市场状态变化是核心挑战。现有方法存在明显不足：传统机器学习和深度学习模型多为黑箱，可解释性差，难以支撑信任与风险控制；单智能体LLM系统受限于金融决策复杂性和领域知识稀缺，交易收益提升有限；现有多智能体LLM交易系统（如CryptoTrade）依赖静态角色和固定交互规则，缺乏显式风险管理与记忆机制，未考虑异质交易风格，也未将智能体行为与真实市场反馈对齐；而RLHF等方法在高度随机市场中难以可靠评估决策质量，且多智能体场景下训练对象与训练资源分配本身就很困难。因此，本文要解决的核心问题是：如何构建一个可解释的多智能体加密货币交易框架，通过双反思机制（交易后决策质量反思与交易者级反事实贡献估计）和市场反馈驱动的强化学习门控策略，动态学习激进、中性、保守三类交易者的影响力权重，使其在牛市、震荡和熊市等不同市场状态下自适应调整，同时保持决策过程透明可解释。

### Q2: 有哪些相关研究？

本文的相关研究主要分为两类。

**方法类：LLM交易系统。** 早期工作采用单智能体范式，让LLM作为独立交易者，依据新闻、财报、价格等外部信号生成决策，如新闻驱动的情绪分析智能体，以及引入推理与记忆机制以提升决策一致性的FinMem。这类方法依赖固定推理模式、缺乏多元视角，鲁棒性与泛化能力有限。随后出现多智能体LLM交易框架，设置新闻分析师、技术分析师、风险控制者等异质角色，通过辩论、协作或信息共享提升事实准确性与决策稳定性。但现有研究很少考虑激进、中性、保守等交易风格差异，且多数框架的角色、交互协议与贡献权重均为人工设定并在推理时固定，智能体既未微调也未与真实市场结果对齐，无法从实际盈亏中学习贡献权重。本文的区别在于显式建模异质交易风格，并用强化学习依据市场反馈动态调整各智能体贡献。

**对齐类：金融LLM对齐。** 常见策略包括检索增强生成、领域数据微调、金融语料预训练（如BloombergGPT、BBT-Fin）、参数高效微调（LoRA、QLoRA）及指令微调模型（PIXIU、FinGPT、Instruct-FinGPT）。此外，自我精炼与基于人类反馈的强化学习提供反馈式改进，金融领域也已将市场反馈强化学习用于情绪预测。但据作者所知，尚无工作将市场反馈整合进多智能体LLM交易框架，本文正是填补这一空白。

### Q3: 论文如何解决这个问题？

Agent4Crypto 采用三阶段闭环架构来解决加密货币交易中的非平稳市场、决策不透明和聚合规则固定等问题。整体框架包括：多模态市场理解、双反思交易员决策、市场执行与反馈对齐。

第一阶段，数据团队中的资产、技术、新闻和视觉四个智能体分别处理链上基本面、技术指标、新闻事件和K线图，由分析师智能体综合为高层洞察，风险经理进行定性风险评估，金融推理库检索历史经验注入后续提示。

第二阶段是核心创新：三个风格特定的交易员智能体（激进、中性、保守）在同一市场情境下各自生成连续动作及自然语言理由，其影响力不手工固定，而由基于PPO的门控策略动态分配权重。门控状态融合了市场特征、上一步权重、当前交易员动作以及反事实贡献记忆（CCM）——后者通过计算每个交易员单独动作在真实市场收益下的假设贡献，估计其近期独立可靠性。

第三阶段，执行聚合动作后，双反思反馈机制运行：一条反思流根据实际组合收益评估决策质量，将可复用经验蒸馏进金融推理库供后续检索；另一条估计交易员级反事实贡献，更新CCM。PPO以净组合收益为奖励更新门控策略，使交易员影响力在牛市、震荡市和熊市中自适应调整。创新点在于可解释的交易员竞争机制与市场反馈驱动的权重学习闭环。

### Q4: 论文做了哪些实验？

论文围绕四个研究问题展开实验。实验设置上，选取BTC、ETH、XRP三种资产，按时间顺序划分验证窗口与测试窗口，覆盖牛市、震荡与熊市行情；所有提示输入严格按时间点构造以避免前视泄漏，交易按次日开盘价结算并收取0.1%手续费，初始资金100万美元，每种方法用5个随机种子（42–46）重复运行取平均，LLM方法额外重复5次生成。对比方法包括：规则策略（Buy-and-Hold、SMA、SLMA、MACD、布林带）、机器学习与深度学习基线（LSTM、Informer、AutoFormer、TimesNet、PatchTST）、强化学习基线（DQN、PPO、SAC）以及LLM交易系统CryptoTrade。主要结果显示，Agent4Crypto在BTC上总收益达6.66%、日收益均值0.09%、夏普比率0.10，均优于所有基线；ETH总收益-4.77%、XRP为-2.36%，同样优于对比方法，而Buy-and-Hold在三种资产上分别亏损15.24%、31.81%和22.37%。消融实验表明，移除数据团队专业化、团队间协作或交易员竞争后性能均下降，验证了各模块的贡献。此外还进行了权重精炼策略对比（等权、直接精炼与PPO学习）及与CryptoTrade的风险规避案例研究。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在：其一，实验仅在BTC、ETH、XRP三种主流币种上验证，样本覆盖有限，且部分币种（如ETH、XRP）绝对收益为负，说明系统在熊市或震荡市中的稳健性仍不足；其二，PPO门控策略与反事实贡献估计依赖历史反馈，在极端行情或流动性骤变时可能存在滞后；其三，Financial ReasoningBank的检索质量与提示词设计对LLM依赖较强，缺乏对推理链可靠性的量化评估。未来可探索：引入更多币种与高频数据验证泛化性；将门控机制扩展为多时间尺度自适应；结合因果推断提升反事实贡献估计的鲁棒性；并加入风险约束或仓位管理模块，以改善下行风险控制。

### Q6: 总结一下论文的主要内容

论文针对加密货币市场高波动、非平稳且现有LLM交易系统决策不透明、聚合规则固定的问题，提出Agent4Crypto——一个双反思、市场反馈对齐的多智能体交易框架。方法上，系统由数据团队、分析师、风险经理、反思器与交易团队协作，整合价格、技术指标、新闻与图表等多模态信号；核心是以激进、中性、保守三类交易者智能体对同一市场情境生成候选动作与自然语言理由，并通过PPO门控策略动态学习其权重。双反思机制包括：基于已实现收益提炼经验教训存入Financial ReasoningBank供后续检索，以及估计各交易者的反事实贡献以判断其近期与市场走势的匹配度。在BTC、ETH、XRP上的实验表明，该方法在总收益与夏普比率上优于传统策略、机器学习与强化学习基线及现有LLM交易系统，验证了可解释交易者竞争与市场反馈驱动自适应的价值。
