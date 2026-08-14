---
title: "AQuA: Recursively Self-Improving Quantitative Trading Research Agents"
authors:
  - "Jiacheng Guo"
  - "Suozhi Huang"
  - "Yunlong Gao"
  - "Zihao Li"
  - "Jian Ge"
  - "Xu Kuang"
  - "Mengdi Wang"
date: "2026-08-13"
arxiv_id: "2608.12841"
arxiv_url: "https://arxiv.org/abs/2608.12841"
pdf_url: "https://arxiv.org/pdf/2608.12841v1"
categories:
  - "cs.CL"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Self-Improving Agents"
  - "Quantitative Trading"
  - "Multi-Agent Pipeline"
  - "Time Series Forecasting"
  - "Evidence Retention"
  - "Sandbox Evaluation"
  - "Factor Discovery"
relevance_score: 8.5
---

# AQuA: Recursively Self-Improving Quantitative Trading Research Agents

## 原始摘要

We study recursive self-improvement at the level of quantitative-investment research: whether an autonomous system can use evidence from earlier experiments to improve the hypotheses and candidates proposed in later iterations. We present AQuA, which comprises two separate language-model-driven research systems: one for symbolic factor discovery and one for trainable model development. The two systems do not share agents, memories, candidate spaces, or research state. Instead, each independently closes its own research loop by retaining validated evidence and using it to guide subsequent proposals. In this bounded sense, both systems implement recursive self-improvement at the level of the research process. Each system also uses its own sealed sandbox, which fixes the data splits, feature and label definitions, and evaluator while allowing the model to act only through constrained factor expressions or configuration diffs. The factor system, a manager-mediated multi-agent pipeline, discovers and combines factors into a signal that reaches a combined information coefficient of about $0.190$ on a crypto universe. The model system, a config-driven loop over a hybrid time-series architecture, reaches a per-stock information coefficient of $+0.0843$ on US equities and converts it into a threshold long/short strategy with a held-out Sharpe of up to $+2.50$ at a two-leg cost. The strategy is positive in every year from 2021 to 2025.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

量化投资研究需要在庞大的因子与模型空间中搜索，但方法上的微小错误（如特征读取未来信息、在测试集上选策略、结果局限于特定市场状态）可能产生看似可靠却无法复现的回测。现有量化智能体通常只聚焦于因子发现或模型开发中的单一环节，且更关键的是，不受约束的智能体会污染其后续迭代所依赖的证据：代码生成智能体可能无意引入时间对齐或预处理错误，审阅智能体因代码语义看似合理而漏检，最终导致数据泄漏产生的高分被当作成功先例，递归改进因此会放大错误而非真实发现。仅靠提示级指令和模型审查无法提供可靠的完整性边界，重复访问固定留出集还会引发自适应过拟合。

本文提出的AQuA系统旨在解决这一核心问题：通过密封沙箱设计，在自主迭代开始前固定数据管线、划分、标签和评估器，并限制智能体只能使用受限领域特定语言（DSL）操作，从机制上杜绝泄漏诱导行为。AQuA包含因子发现与模型开发两个独立系统，各自闭环改进研究过程而非成功定义，从而在保证证据完整性的前提下实现递归自我改进。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**LLM驱动的alpha挖掘**是本文Part I的直接基础，该方向从遗传规划、强化学习的算子搜索演进到进化式与智能体式搜索、程序级合成、图结构进化、带经验记忆的自进化智能体，以及融合新闻流的因子生成。AQuA继承了其“先提议、后记忆驱动”的设计，但将因子发现系统与模型开发系统完全隔离，不共享智能体、记忆或搜索状态，各自独立利用实验证据改进后续提议。**自主科研智能体**方面，已有工作将语言模型智能体用于端到端科学流程和交易决策，AQuA采纳了自主研究循环的愿景，但聚焦于量化研究中的递归自改进，并针对数据泄漏这一量化特有风险，将数据路径和评估器设为智能体不可达的密封沙箱。**金融时间序列深度模型**为Part II提供组件基础，包括卷积、状态空间、注意力及混合架构，但本文的贡献并非新模型原语，而是让智能体自主组合这些原语并跨变体积累证据的独立循环。与Part I的关系是概念性的——两者都从先前实验中学习——而非架构性的。

### Q3: 论文如何解决这个问题？

AQuA通过两个相互独立的语言模型驱动研究系统，分别处理符号因子发现和可训练模型开发，实现研究过程层面的递归自我改进。两个系统不共享任何组件，各自独立闭环：每次迭代经历五个阶段——提出假设（因子表达式或模型配置）、构建具体产物、在留出数据上评估、验证无前瞻偏差和制度依赖性，最后将有效证据写入持久化研究状态，供下一轮迭代参考。

核心架构包含三个关键设计。第一，密封沙箱机制：数据划分、特征/标签定义和评估器全部由人工预先固定并密封，模型只能通过受限的因子表达式或配置差异（config diff）行动，无法修改任何密封组件，从结构上杜绝数据泄漏。第二，双指标分离策略：搜索过程中仅向智能体返回验证集上的分数用于排序和早停，最终测试窗口在配置冻结后只评分一次，绝不反馈给智能体，防止选择偏差。第三，因果封闭性保证：因子系统使用公式化alpha算子注册表，所有时序算子仅读取回溯窗口、横截面算子仅读取当前时间戳，任何组合表达式天然因果；模型系统通过冻结数据划分和注册表约束，确保每个配置都无泄漏。

创新点在于：将递归自我改进限定在研究过程而非模型参数层面，通过持久化研究状态实现证据积累；因子系统采用管理者中介的多智能体流水线，结合可证伪假设提案机制；模型系统使用混合时间序列架构的配置驱动循环，在加密资产上达到约0.190的IC，美股上实现+0.0843的每股IC和最高+2.50的夏普比率，2021至2025年每年均为正收益。

### Q4: 论文做了哪些实验？

论文构建了AQuA系统，包含两个独立的自改进研究循环，分别进行因子发现和模型开发实验。

**Part I（因子发现）**：在加密货币五分钟数据集上运行。系统采用六智能体流水线（数据管理员→可视化分析师→想法挖掘器→因子评估器→回测工程师→研究图书管理员），由AI经理协调。实验通过三个嵌套反馈循环迭代改进，累积记忆和信念。结果显示，组合验证信息系数（IC）随迭代从约0.026-0.037的单因子水平提升至约0.190的组合信号IC，且与价格、成交量、未平仓合约和资金流等简单基线对比，确认因子非基线重复。

**Part II（模型开发）**：在美国股票日内数据上预测未来30分钟收益。按时间划分：2010-2019训练，2020为隔离缺口，2021-2025为测试窗口。对比了线性岭回归（IC=+0.0251）、LGB（+0.0397）、xLSTM（+0.0434）、LSTM（+0.0535）、GRU（+0.0613）和混合模型（+0.0843），混合模型最优。策略层面，阈值多空组合在2bps双边成本下，行业中性化后Sharpe为+2.15，叠加因果波动率目标后达+2.50，完全因果walk-forward为+2.0，且2021-2025每年均为正收益（Sharpe分别为+1.7、+3.5、+1.9、+1.8、+2.7）。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索空间主要体现在三方面。首先，系统仅在单一市场（加密货币5分钟、美股30分钟）验证，跨市场、跨频率的泛化能力未知，未来可探索多市场联合训练或自适应频率调整机制，并引入动态再校准策略以应对市场状态切换。其次，测试集隔离依赖操作员纪律而非技术保障，存在治理风险，可设计基于密码学承诺或可信执行环境的硬隔离方案，将“审计属性”升级为“可验证保证”。第三，因子发现与模型训练目前完全解耦，而耦合是自然演进方向——但需警惕共享数据导致的间接选择泄漏。建议在耦合时采用“冻结因子库”协议，即因子系统产出的信号先经独立验证集固化，再作为模型系统的固定输入，同时引入差分隐私或因果干预技术切断隐性信息流。此外，当前循环仅优化验证指标，未来可加入风险调整后的多目标奖励（如换手率、最大回撤），并探索元学习机制让系统自动调整研究策略本身，而非仅调整候选方案。

### Q6: 总结一下论文的主要内容

AQuA提出了一个由两个独立LLM驱动的研究系统组成的框架，分别用于符号因子发现和可训练模型开发，二者不共享智能体、记忆或候选空间，各自独立闭环，通过保留已验证证据指导后续假设与候选生成，实现研究流程层面的递归自我改进。每个系统配备密封沙箱，固定数据划分、特征与标签定义及评估器，模型仅能通过受限因子表达式或配置差异进行交互。因子系统在加密货币领域达到约0.190的综合信息系数；模型系统在美国股票上实现每股+0.0843的IC，并转化为阈值多空策略，样本外夏普比率最高达+2.50，且2021至2025年间每年均为正收益。该工作证明了自主研究系统在量化投资中递归改进的可行性，未来方向是将两系统耦合，使发现因子反哺模型循环。
