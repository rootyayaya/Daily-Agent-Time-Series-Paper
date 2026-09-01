---
title: "A Human-in-the-Loop Autonomous Agent for Industry Time Series Forecasting"
authors:
  - "Xiaoyu Tao"
  - "Mingyue Cheng"
  - "Ze Guo"
  - "Bokai Pan"
  - "Qi Liu"
  - "Shijin Wang"
  - "Enhong Chen"
date: "2026-08-31"
arxiv_id: "2608.30976"
arxiv_url: "https://arxiv.org/abs/2608.30976"
pdf_url: "https://arxiv.org/pdf/2608.30976v1"
categories:
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "Human-in-the-Loop"
  - "Time Series Forecasting"
  - "LLM Agent"
  - "Execution Report"
  - "Evidence Routing"
  - "Tool Use"
  - "Constraint Checking"
  - "Electricity Price Forecasting"
  - "Interpretability"
relevance_score: 9.5
---

# A Human-in-the-Loop Autonomous Agent for Industry Time Series Forecasting

## 原始摘要

Real-world time-series forecasting is rarely a one-shot model invocation: practitioners must formulate tasks, connect data and models, incorporate domain expertise, assess prediction plausibility, and communicate uncertainty. Specialized forecasting models provide strong numerical predictions but usually operate in fixed pipelines, while general-purpose large language model (LLM) agents often lack forecasting-specific checks, constraints, and stopping rules. We present CastClaw, a human-in-the-loop autonomous forecasting system built through forecasting-oriented harness engineering. CastClaw connects data, specialized models, analytical tools, user input, and a versioned execution record in one runtime. Users specify the target, horizon, constraints, and hypotheses in natural language. Starting from a supplied or model-generated forecast, CastClaw checks temporal patterns and user constraints; when evidence is missing, it retrieves context, runs an analysis or another model, or asks the user. It then keeps, revises, or escalates the result under explicit stopping conditions. The output contains the final forecast and an execution report recording inputs, evidence, actions, and revisions. In this five-dataset electricity-price setting, CastClaw reports the lowest point-estimate MSE and MAE among 16 baselines. A Nord Pool case demonstrates the inspectable workflow. CastClaw was also validated offline on provincial electricity-load data from North China covering January--June 2026.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

真实世界的时间序列预测并非一次性模型调用，而是一个系统级任务：实践者需定义任务、连接数据与模型、融入领域知识、评估预测合理性并沟通不确定性。然而，现有方法仅覆盖该流程的片段：专用预测模型虽数值精度高，但固守固定输入输出管道，缺乏任务自主性与动态调整能力；通用大语言模型智能体虽具备推理与工具调用能力，却缺少面向预测的专项检查、约束校验和明确停止规则，易产生不可靠输出。为此，本文提出CastClaw——一个人类参与回路（human-in-the-loop）的自主预测系统，通过预测导向的“工程化框架”（harness engineering）将数据、专用模型、分析工具、用户输入及版本化执行记录整合于统一运行时。其核心目标是实现任务自主性与人类监督的平衡：系统自主选择检查项、调用工具、记录证据与修订，但每次预测变更均须通过验证与约束门控，用户可随时纠正、约束或终止运行。最终输出不仅包含预测结果，还提供可审计的执行报告，从而解决现有方法在系统级预测流程中缺乏可检查性、可控性与证据追溯能力的核心不足。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，传统时序预测模型（如ARIMA、Transformer系列）依赖固定输入输出流程，缺乏任务自主性；LLM预测器（如TimeGPT）将数值预测与推理结合，但缺少领域约束检查。**智能体类**是本文重点对比对象：Agentic Forecasting强调自主工具调用，AlphaCast侧重人机协同推理，TimeSeriesScientist作为通用分析智能体覆盖数据探索到建模，但三者均未系统设计“验证-修订-停止”的闭环机制。**应用与评测类**包括基于公共电力价格数据集的基准测试（如M4、M5竞赛）及工业场景案例（如Nord Pool电价预测），这些工作通常只评估单模型精度，不涉及执行过程可审计性。

CastClaw的独特贡献在于：1）将人类反馈作为一等公民嵌入循环，而非仅作为事后纠错；2）通过版本化执行记录实现全流程可追溯，区别于黑箱智能体；3）所有修订必须通过验证与约束检查，避免盲目迭代。相比TimeSeriesScientist的通用性，CastClaw聚焦预测场景的专用检查（如时序模式、业务约束），比AlphaCast的协同模式更强调系统自主决策，同时保留人工干预接口。

### Q3: 论文如何解决这个问题？

CastClaw通过“人在回路”的自主预测系统解决工业时序预测中固定流程与专家知识脱节的问题。其核心是一个版本化执行记录（Versioned Execution Record），统一管理请求、数据版本、约束、证据、候选预测和操作日志，确保用户硬约束不可被静默覆盖。

系统架构分为五个阶段：意图理解、证据检索、候选生成、验证修订和结果交付。用户以自然语言指定目标、预测时长、粒度、约束和假设，系统对缺失关键信息主动提问而非默认填充。在预测前，CastClaw会检索历史规则和相似运行记录，但仅作为待验证建议，与当前数据冲突的项会被拒绝。

关键技术在于验证-修订循环：系统加载用户预测或运行注册模型后，对候选结果检查时序模式、领域约束、上下文变化、模型分歧和用户假设。若证据不足，可检索上下文、分析相似时段、运行其他模型或询问用户，但仅在证据变化时重复动作。修订结果必须通过验证指标和硬约束才替换当前预测，否则保留在记录中。

创新点包括：显式区分硬约束与待验证假设；每个证据项标注来源和适用范围；停止条件明确（预测受支持、行动价值低、预算耗尽或需专家判断）；输出包含完整执行报告，记录输入、证据、工具输出和修订决策。在五个电力价格数据集上，CastClaw取得最低MSE和MAE，并通过华北省份电力负荷数据验证了离线工作流执行能力。

### Q4: 论文做了哪些实验？

论文在五个公开电力价格数据集（BE、DE、FR、NP、PJM）上进行了实验，按7:1:2比例划分训练、验证和测试集。对比方法包括16种基线，涵盖统计方法、专用神经模型、基础模型、基于LLM的预测器及预测智能体。主要指标为测试集MSE和MAE。

结果显示，CastClaw在全部十个数据集-指标组合中取得最低误差。相对最优基线，MSE降低幅度为：BE 5.5%、DE 30.1%、FR 11.4%、NP 17.7%、PJM 9.7%；MAE降低幅度分别为13.9%、20.9%、23.5%、23.5%、11.3%。五数据集平均降幅为MSE 14.9%、MAE 18.6%。最强基线因数据集而异，但CastClaw在两个指标下均保持第一，最大增益出现在DE，BE和PJM的较小增益表明结果非单一数据集驱动。

此外，论文通过Nord Pool案例展示了可检查的工作流，记录请求、残差检查、上下文检索、调整测试及验证比较。还利用中国北方2026年1-6月省级电力负荷数据进行了离线工作流验证，确认了任务规范、模型与工具接口、用户输入机制及执行报告的有效性，但该验证仅证明离线执行能力，不涉及精度对比或部署效果。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下几方面展开：首先，当前验证仅局限于电力价格与负荷数据，未来应在更多领域（如交通、金融、气象）和更大规模数据集上检验泛化能力，并补充消融实验以量化各模块（如检查机制、检索策略、人工介入频率）的独立贡献。其次，用户研究缺失，需设计系统性实验评估人机协作效率、用户信任度及认知负荷，探索更自然的多轮交互方式。第三，可引入主动学习机制，让Agent在不确定性高时自动请求标注或补充数据，减少人工干预。第四，当前系统依赖预设规则和LLM推理，可探索将领域知识图谱或因果模型嵌入检查流程，增强对异常模式的解释能力。最后，执行报告目前仅作记录，未来可将其转化为可迁移的提示模板或策略库，实现跨任务经验复用，并研究多Agent协作或联邦学习框架下的分布式部署可能性。

### Q6: 总结一下论文的主要内容

CastClaw是一个面向工业时间序列预测的人机协同自主智能体系统。针对现实预测中任务定义、数据连接、领域知识融入和不确定性沟通等复杂流程，该方法通过预测导向的工程化框架，将专用预测模型、分析工具、用户输入和版本化执行记录整合于统一运行时。用户以自然语言指定目标、预测范围、约束和假设，系统自动检查时间模式与约束条件，在证据缺失时检索上下文、运行分析或询问用户，并在明确停止条件下保留、修订或升级预测结果。在五个电力价格数据集上，CastClaw取得了16个基线中最低的点估计MSE和MAE，Nord Pool案例展示了可检查的工作流程，华北省级电力负荷数据验证了其离线有效性。该工作强调了预测智能体应具备领域感知的检查机制和用户参与机制，而非单纯依赖模型能力。
