---
title: "Governed Self-Evolution for Autonomous Investing: A Multi-Agent LLM System with an Invariant Core"
authors:
  - "Yebo Feng"
  - "Jingyang Dai"
  - "Liangrui Pan"
  - "Nelson Lau"
  - "Jiahua Xu"
  - "Yang Liu"
date: "2026-10-22"
arxiv_id: "2610.30557"
arxiv_url: "https://arxiv.org/abs/2610.30557"
pdf_url: "https://arxiv.org/pdf/2610.30557v1"
github_url: "https://github.com/yebof/quant-agent"
categories:
  - "cs.AI"
  - "cs.CL"
  - "cs.MA"
  - "q-fin.PM"
tags:
  - "Multi-Agent LLM"
  - "Self-Evolution"
  - "Memory"
  - "Reflection"
  - "Feedback Optimization"
  - "Typed Reports"
  - "Financial Time Series"
  - "Risk Management"
  - "Live Deployment"
  - "Replay Verification"
relevance_score: 7.5
---

# Governed Self-Evolution for Autonomous Investing: A Multi-Agent LLM System with an Invariant Core

## 原始摘要

LLM agents that act on live Web data must combine heterogeneous evidence, remember what they have done and improve from outcomes without weakening their own safeguards. We study this problem in autonomous investing, where every action is irreversible and based on untrusted Web content. We present Steward, a multi-agent LLM system that draws the boundary of self-evolution in its type system. First, nine role-specialised agents decide jointly: four analysts read news feeds, SEC filings, macroeconomic series and market data and emit typed reports, from which a Portfolio Manager sets target positions that a protected Risk Manager audits. Second, a seven-layer shared memory, assembled by code from the system's own record, gives each decision its position context, the market narrative, calibration and the agent's past decisions. Third, the system improves itself by review: code grades every trade and forecast nightly and writes the grades into memory, and each quarter a reflector proposes prompt learnings that a deterministic gate applies reversibly and replay of recorded inputs verifies. All three operate around an invariant core of order arithmetic, risk rules and discipline-agent prompts that no self-edit can reach. In a five-month live deployment (102 trading days, 1,632 LLM calls), the system contained a 24.6% sector drawdown to a 0.3% loss; in replay of its recorded inputs, a single model given the same raw data traded more and lost 1.35 points against the market over five days where the joint design showed no significant loss, and no injected instruction was followed; and a 2015-2026 backtest shows the core alone lowering the maximum drawdown under all 50 random entry policies. The reflector traced the dominant failure to its root cause, and the gate applied a learning that the agent adopted on trigger evenings and on no control evening. Code: https://github.com/yebof/quant-agent

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决的核心问题是：如何让一个直接基于实时、不可信 Web 数据行动的多智能体 LLM 系统，在从自身决策结果中持续自我改进的同时，不削弱其安全约束。研究背景是自主投资这一高风险场景：每个动作不可逆、按日以真金白银计分，输入全部来自公开 Web 内容（新闻、SEC 文件、FRED 数据、行情），核心威胁正是不可信内容触达有行动权限的智能体。现有 LLM 交易智能体虽已组合分析师角色、记忆与反思，但多在历史数据上评估，难以排除预训练泄漏；其学习回路依赖模型自我反思或回测，且没有任何机制区分"可以改变的部分"与"必须不变的部分"。论文据此指出四类未被观测的失效模式：自我评分偏乐观（F1）、纪律侵蚀（F2）、变更不可审计（F3）、变更无效却报告进步（F4）。本文要解决的核心问题即：把自我进化的边界画在类型系统而非提示词中，使提案类型无法命名由订单算术、阻断性风控规则和纪律智能体提示构成的不变内核，从而让系统能改写自己却无法削弱自身保障，并在数月实盘运行中验证这一设计。

### Q2: 有哪些相关研究？

相关研究可分为四类。自我改进与自进化智能体方面，Reflexion、Self-Refine让模型自我批评与修正，Voyager积累技能库，Promptbreeder与OPRO以模型为提议者优化提示，Generative Agents加入记忆与周期反思；但已有研究指出LLM自我纠错不可靠、口头置信度过度自信。本文据此以代码计算的结果驱动进化，并用类型级白名单与确定性门控加以约束，且首次报告在真实市场长期运行并记录提议与拒绝的自进化智能体。金融文本与LLM方面，已有研究证实媒体悲观情绪、文件情感词典误判、新闻情绪当日吸收，以及GPT-4标题标签预测短期漂移、LLM需检索与工具接地以防幻觉；这些工作多在回测中评估信号，本文贡献在于对多源行动智能体的治理而非单一信号。交易智能体方面，FinMem提出分层记忆，FinCon构建经理—分析师层级与言语强化，QuantAgent构建自改进知识库，FinAgent与TradingAgents引入工具使用与交易公司角色，StockAgent模拟市场；其评估多为历史回测（存在预训练泄漏）或模拟环境，本文则进行前向实盘评估，由代码对实盘结果评分并围绕不可触及的核心进化。安全方面，提示注入及其间接形式已被刻画，近期防御转向执行隔离、能力与信息流控制等架构手段；本文的不变核心属此类架构防御，并新增“自身记录反馈给反思器改写指令”这一通道。框架与评测方面，AutoGen、MetaGPT、CAMEL协调角色智能体，结构化输出使模式化JSON廉价，本文把模式用作推理规范、审计产物与进化边界；Mind2Web、WebArena评估Web智能体，Kapoor等要求报告成本与可复现性，本文均予遵循。

### Q3: 论文如何解决这个问题？

论文提出Steward——一个多智能体LLM自主投资系统，其核心思路是把"自我进化"的边界写进类型系统，用"不变内核+可进化外围"的结构解决LLM代理在不可信Web数据上行动、记忆与自我改进而不削弱安全护栏的问题。

整体框架上，系统由九个角色化智能体与一个确定性内核组成，每个交易日运行六个会话：晨会中四位分析师（新闻、财报、宏观、技术）并行读取RSS、SEC文件、FRED序列与行情数据，输出带类型的报告；组合经理综合报告与共享记忆设定目标仓位；确定性订单构造器、阻断式风控引擎与LLM风控经理依次把关后才执行。午间与收盘会话只允许卖出，熔断器每30分钟无LLM运行，晚间对当日交易打分，季度会话进行反思。

主要组件包括：一是七层共享记忆，由代码从系统自身记录中组装（当日信号、持仓上下文、市场叙事、45天校准表、风控裁决、自身历史决策、预计账簿），保证智能体引用的每个数字都来自代码而非其他智能体的文字；二是模式强制的思维链，每个输出类型内嵌逐步CoT字段，跨字段校验器编码领域不变量，验证后的对象连同输入原样存储，使记录本身可被评分、反思与回放；三是判断与算术分离，LLM只输出目标仓位意图，止损、仓位规模、风险预算、盈亏比等全部由确定性代码计算，硬规则先于LLM审核运行，风控经理失败即关闭。

创新点在于：不可信Web文本被限制在上游，原始标题只进入新闻与财报智能体，组合经理永远看不到原文；不变内核π₀（订单算术、风控规则、纪律智能体提示词）任何自编辑都无法触及；进化只发生在记忆与六个可编辑智能体的Learnings区，季度反思器提出至多三条学习，经确定性门控（追加式、词边界绊线、Jaccard去重、FIFO上限、单次提交可git回滚）可逆应用，并通过回放录制输入验证效果。

### Q4: 论文做了哪些实验？

论文围绕Steward系统开展了三类评估：实盘部署、轨迹重打分与回放实验。实盘方面，系统于2024年某五个月窗口（102个交易日、1,632次LLM调用）在10万美元纸面账户中基于实时Web数据交易，共产生746笔成交，API成本约每日4.4美元，期间将24.6%的板块回撤控制在0.3%亏损。轨迹重打分对7,843条技术分析师评级、1,885个符号日新闻情绪、97条晚间预测、556个目标权重、90条风险裁决及全部往返交易按后续价格打分：技术分析师5/10/20日IC仅为-0.004、0.019、0.031，新闻情绪与后续走势不相关，晚间分析师次日方向准确率37%，低于54%基准；但组合经理综合目标权重收益达+15.4%（无退出）、+12.2%（含风控编辑），夏普2.33对1.80，显著优于跟随分析师买入评级的+1.3%。回放实验用20个早晨的原始输入对比三种架构：单模型代理在5日和10日市场调整后收益为负，5日内跑输市场1.35个点，而联合设计无显著亏损，且无注入指令被遵循。此外2015–2026回测显示，仅不变量核心即可在全部50种随机入场策略下降低最大回撤。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索点主要有三。其一，实盘仅五个月、单一美股组合、纸面账户，样本与市场状态有限，且纸面成交不含市场冲击，未来需跨市场、跨资产与更长周期的验证，并引入真实滑点建模。其二，自进化仅在季度尺度由反射器提出、门控应用，学习粒度和频率偏低，可探索更细粒度的在线校准与多层级学习率，同时研究门控误拒/误受的统计保证。其三，不变核虽由类型系统保护，但"核心"边界本身由人设定，可探索让系统在受限元层提出核的调整建议、由人审批的半自动治理。此外，分析师信号单独很弱、执行缺口显著（意图+12.2%对实盘+5.0%），可改进订单执行与退出机制；也可引入不确定性估计与多模型投票，缓解单模型回放中过度交易的问题。

### Q6: 总结一下论文的主要内容

论文针对“能读取实时网页数据并自主行动的LLM智能体”这一场景，提出核心难题：如何在整合异构弱证据、记忆历史决策并从结果中学习的同时，不削弱自身的安全约束。作者以自主投资为具体场景（每笔操作不可逆、输入均为不可信网页内容），提出Steward多智能体LLM系统。方法上，九个角色化智能体协同决策：四名分析师分别处理新闻、SEC文件、宏观序列与行情数据并输出类型化报告，由组合经理设定目标仓位，受保护的风险经理审核；代码从系统自身记录中组装七层共享记忆；系统通过“治理式自演化”改进——代码每晚对每笔交易与预测打分，每季度由反思器提出类型化提示学习，经确定性、可逆的门控应用并由回放验证。关键在于将自演化边界画在类型系统中：提案类型无法命名由订单算术、风险规则与纪律智能体提示构成的不变核心，因此系统可改写自身却无法削弱安全护栏。主要结论：五个月实盘（102个交易日、1632次LLM调用）中，系统将24.6%的板块回撤控制为0.3%亏损；回放显示单一模型在相同数据上交易更多且跑输市场1.35个百分点，且未执行任何注入指令；2015–2026回测表明仅不变核心即可在全部50种随机入场策略下降低最大回撤。意义在于首次对自演化LLM智能体进行数月实盘评估并完整记录演化循环的每次提案与拒绝，证明“类型系统治理”可在保持可演化性的同时守住安全底线。
