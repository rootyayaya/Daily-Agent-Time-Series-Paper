---
title: "TIMERSI: Towards Self-Improved Agentic Deployment for Time-Series Foundation Models"
authors:
  - "Haoxin Liu"
  - "Deqing Fu"
  - "Lucheng Fu"
  - "Yiqiao Jin"
  - "Rushi Qiang"
  - "Harshavardhan Kamarthi"
  - "B. Aditya Prakash"
date: "2026-10-14"
arxiv_id: "2610.19725"
arxiv_url: "https://arxiv.org/abs/2610.19725"
pdf_url: "https://arxiv.org/pdf/2610.19725v1"
categories:
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "Time-Series Foundation Models"
  - "Self-Improving Agent"
  - "Coding Agent"
  - "Forecasting Pipeline Optimization"
  - "Feedback-Guided Revision"
  - "Adaptive Pipeline Selection"
  - "Automated Deployment"
  - "Time Series Forecasting"
relevance_score: 8.5
---

# TIMERSI: Towards Self-Improved Agentic Deployment for Time-Series Foundation Models

## 原始摘要

Time-series foundation models provide strong zero-shot forecast, but deployment for real- world applications still requires task-specific designs for model inputs and outputs. Direct inference can leave domain knowledge and re- curring forecast errors unaddressed, while tai- lored pipelines require substantial human ex- pertise and effort. We introduce TIMERSI, a self-improving agentic deployment system around frozen forecasting models. A cod- ing agent translates task descriptions into ex- ecutable pipeline changes. It tests each re- vision on historical forecasting windows and uses observed errors to guide subsequent re- visions. During deployment, an adaptive se- lector chooses among the resulting pipelines using completed forecasts under similar con- ditions. Across 198 tasks on TIME and FEV- bench, TIMERSI outperforms all submissions on six point and probabilistic forecasting met- rics. Controlled comparisons support the value of feedback-guided revision over non-iterative pipeline search. Further experiments verify the generalization with different coding agents and forecasting models.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列基础模型虽具备强大的零样本预测能力，但在真实场景部署时，仍需针对具体任务设计输入与输出流程。例如节假日闭店信息可辅助需求预测，潮汐周期可指导洋流预测，但将这些领域知识转化为可执行的部署管线，往往依赖大量人工专业知识与精力。直接推理无法利用领域知识，也难以纠正反复出现的预测误差；而定制化管线开发成本高昂。现有基于大语言模型的代码智能体虽可自动生成与评估程序，但在预测任务中面临两大挑战：一是看似合理的修改未必提升精度，例如日历信息可通过模型输入或独立预测器引入，效果差异显著，需借助历史预测误差来评估与修正；二是平均表现良好的管线在预测条件变化时可能不再适用。因此，本文提出 TIMERSI，一个围绕冻结预测模型的自改进智能体部署系统，核心是用任务知识指导尝试方向、用预测反馈指导修正与选择，通过迭代管线改进与自适应管线选择两阶段，自动构建并动态选用部署管线，从而在无需微调基础模型的前提下提升多任务预测性能。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，TSFM（时间序列基础模型）如Chronos、TimesFM、Moirai等提供零样本预测能力，但直接推理无法利用任务知识。LLM代码智能体（如Codex、GPT系列驱动的编程代理）已被用于自动化程序生成与评估，本文将其扩展至预测流水线构建。递归自我改进（RSI）在LLM领域已有探索，本文首次将其应用于冻结TSFM的部署流水线。应用类方面，传统TSF部署依赖人工特征工程与后处理校正，如节假日效应建模、潮汐周期注入等，本文用智能体自动完成这些任务知识到代码的转化。评测类方面，TIME和FEV-bench是近期提出的时间序列预测基准，涵盖多领域任务，本文在其198个任务上全面评测。与上述工作的区别在于：本文不微调模型权重，而是围绕冻结TSFM构建可迭代改进的部署流水线，并通过自适应选择器应对条件变化，实现了反馈引导的递归自我改进，而非一次性流水线搜索。

### Q3: 论文如何解决这个问题？

TIMERSI 将时序基础模型（TSFM）的部署过程自动化，核心思路是在冻结模型权重的前提下，让编码智能体通过“执行—评估—修订”的闭环迭代改进任务流水线，并在部署时自适应地选择最合适的流水线。

整体框架分为两个阶段。第一阶段是迭代式流水线改进。系统以直接推理作为参考流水线，智能体根据任务描述编写 Python 代码，覆盖四个环节：预处理、特征构造、上下文选择和后处理。在输入侧，它可以变换观测值、将任务知识编码为额外变量、选择送入模型的历史窗口与变量组；在输出侧，它可以组合预测、拟合辅助预测器并纠正系统性误差。每次修订都在历史预测窗口上执行，系统返回预测分数、窗口级误差和执行日志，智能体据此决定是细化、组合还是更换策略。早期窗口构成适应集用于迭代，后期窗口构成选择集用于筛选，最终保留排名最高的流水线与参考流水线组成部署集。

第二阶段是自适应流水线选择。由于平均表现好的流水线未必适合每个未来窗口，系统对每个目标变量、每个预测起点单独选择。选择器用近期历史和参考预测的数值特征（水平变化、近期趋势、预测形状等）描述当前条件，检索相似的历史已完成窗口，并按相似度加权比较各流水线相对参考的误差，选择加权历史误差最低者，由其提供完整预测视野和所有分位数。随着新窗口完成，误差反馈持续更新，选择策略动态调整，而流水线代码保持固定。

创新点在于：用执行反馈引导代码修订而非非迭代搜索；将任务语义与数值反馈结合；在冻结 TSFM 上实现自改进部署，并在 TIME 与 FEVbench 的 198 个任务上取得领先。

### Q4: 论文做了哪些实验？

论文在TIME基准的98个任务和FEVbench的100个任务上进行评估，分别覆盖111,177和235,039个预测实例。默认配置将TimesFM 3.0与Claude Code配对。TIME报告归一化MASE和CRPS（越低越好），FEVbench报告MASE、SQL、WQL和WAPE的技能分数（越高越好）。对比基线包括TIME上32个、FEVbench上31个已发表提交，涵盖基础模型、监督预测器和统计方法，主要有TimesFM 3.0、Chronos-2、Toto 2.0、QiYao-M和TiRex-2。主要结果：TIMERSI在全部六项指标上取得最佳，相比直接推理TimesFM 3.0，TIME上MASE降低1.52%、CRPS降低1.61%；FEVbench上MASE技能提升2.79个百分点、SQL技能提升2.26个百分点。消融实验显示非迭代搜索劣于直接推理，而TIMERSI优于直接推理。泛化实验验证了不同编码代理（Antigravity/Gemini 3.8 Flash）和预测模型（Chronos-2、LPTM）下均有效。案例研究显示任务级MASE降低2.86%–6.70%。

### Q5: 有什么可以进一步探索的点？

论文的局限主要有三点：一是依赖清晰的任务与变量描述，若描述模糊或缺失领域语义，编码智能体难以将数值模式与领域知识对齐；二是历史窗口上的改进不保证未来预测提升，分布漂移仍是核心开放问题；三是系统围绕冻结的预测模型构建，未探索与模型微调或持续学习的协同。未来可从以下方向深入：其一，引入自动化的任务描述生成与变量语义推断，降低对人工描述的依赖；其二，设计面向分布漂移的在线验证与回滚机制，例如用漂移检测触发管线重选或再修订；其三，将自适应选择器从“事后选择”升级为“预测性路由”，提前判断哪条管线在何种条件下更可靠；其四，探索多智能体协作，让编码、评估与领域推理智能体分工，提升修订质量与可解释性。这些方向有望推动自改进部署系统在真实工业场景中更稳健地落地。

### Q6: 总结一下论文的主要内容

论文针对时间序列基础模型在实际部署中仍需大量人工设计输入输出流程的问题，提出了自改进智能体部署系统TIMERSI。其核心思路是：在冻结的预测模型外围，由编码智能体将任务描述转化为可执行的流水线修改，并在历史预测窗口上测试每次修改，利用观测到的误差指导后续迭代；部署阶段则由自适应选择器根据相似条件下已完成预测的表现，从生成的多个流水线中择优。在TIME和FEVbench的198个任务上，TIMERSI在六项点预测与概率预测指标上均超越所有提交方案。受控实验表明，反馈引导的迭代修改优于非迭代的流水线搜索，且在不同编码智能体和预测模型上均具泛化性。该工作为时间序列基础模型的自动化、任务自适应部署提供了新范式。
