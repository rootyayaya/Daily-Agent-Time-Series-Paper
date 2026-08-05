---
title: "CastFSR: A Fast--Slow--Reflect Agentic Reasoning Framework for Context-Aware Time Series Forecasting"
authors:
  - "Xiaoyu Tao"
  - "Mingyue Cheng"
  - "Bokai Pan"
  - "Chuang Jiang"
  - "Huanjian Zhang"
  - "Tian Gao"
  - "Yaguo Liu"
  - "Qi Liu"
  - "Enhong Chen"
date: "2026-08-04"
arxiv_id: "2608.03031"
arxiv_url: "https://arxiv.org/abs/2608.03031"
pdf_url: "https://arxiv.org/pdf/2608.03031v1"
github_url: "https://github.com/Xiaoyu-Tao/CastFSR"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Time Series Forecasting"
  - "LLM Agent"
  - "Fast-Slow-Reflect"
  - "Context-Aware Reasoning"
  - "Reflection"
  - "Reinforcement Learning"
  - "Tool Use"
  - "Evidence Retrieval"
  - "Forecast Validation"
relevance_score: 8.5
---

# CastFSR: A Fast--Slow--Reflect Agentic Reasoning Framework for Context-Aware Time Series Forecasting

## 原始摘要

Time series forecasting is fundamental to decision-making in complex systems, where future dynamics are influenced not only by historical observations but also by evolving contextual features. Recent advances in large language models (LLMs) have extended forecasting beyond numerical extrapolation toward context-aware reasoning. However, existing approaches often lack explicit mechanisms to identify relevant contexts, reason about their impacts, and validate forecasts against temporal and domain constraints. In this work, we propose CastFSR, an agentic framework that formulates context-aware forecasting as a Fast--Slow--Reflect workflow. In fast thinking, CastFSR profiles observations and selects lightweight forecasters to construct a data-driven forecast prior. In slow deliberation, it retrieves contextual evidence, adaptively determines informative look-back windows, and reasons about how contexts reshape future dynamics. In reflection, it iteratively refines forecasts to ensure temporal, contextual, and domain consistency. CastFSR supports both training-free inference with off-the-shelf LLMs and efficient deployment through a two-stage SFT and reinforcement learning strategy that transfers its orchestration capability to compact LLMs. Extensive experiments on public datasets demonstrate that CastFSR consistently outperforms representative baselines. Our code is available at https://github.com/Xiaoyu-Tao/CastFSR.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列预测（TSF）在能源、金融、交通等复杂系统中至关重要，其未来动态不仅受历史观测影响，还受不断演变的上下文特征（如政策、事件、环境变化）驱动。现有方法主要分为两类：传统统计/深度模型虽擅长时序建模，但过度依赖历史数据，难以整合外部上下文；而基于大语言模型（LLM）的预测方法虽引入语义推理，却缺乏显式机制来识别相关上下文、推理其影响，并验证预测结果是否符合时间与领域约束。因此，核心问题是如何将数值预测、上下文证据与反思性验证有机协同，实现真正的上下文感知预测。

本文提出CastFSR框架，将上下文感知TSF重构为“快-慢-反思”的智能体决策流程：快速阶段通过剖析观测并选择轻量预测器构建数据驱动先验；慢速阶段检索上下文证据、自适应确定回看窗口并推理上下文如何重塑未来动态；反思阶段迭代校验时间、上下文与领域一致性。该框架旨在解决现有方法在上下文识别、影响推理和约束验证上的缺失，同时支持免训练推理与两阶段蒸馏部署，兼顾灵活性与性能。

### Q2: 有哪些相关研究？

时间序列预测的相关研究主要分为两条主线。**方法类**上，早期工作以统计模型（自回归、状态空间）和深度学习（RNN、TCN、Transformer）为主，近年则涌现出基于大规模预训练的基础模型，通过跨语料学习提升泛化能力。但这些方法本质上仍依赖数值模式外推，缺乏对上下文信息的主动检索与推理。**应用类**上，多变量方法建模序列间依赖，上下文感知方法引入外部特征，但通常以固定输入形式在单次前向传播中被动使用，无法动态评估历史模式是否仍适用。**智能体与决策类**研究则涵盖经典强化学习（状态-动作映射）和基于LLM的工具增强型智能体（多步推理、外部工具调用），后者在问答、代码生成等任务中表现优异，但主要面向状态、动作和评估信号定义明确的场景。

本文与上述工作的核心区别在于：CastFSR将上下文感知预测显式构建为“快-慢-反思”智能体工作流，快思考负责数据驱动的预测先验，慢思考主动检索上下文证据并自适应确定回看窗口，反思阶段则迭代校验时序与领域一致性。相比固定单次推理的预测模型，它具备主动识别相关上下文、推理影响并验证约束的能力；相比通用智能体系统，它针对时间序列预测的时序特性设计了专门的编排与优化策略（两阶段SFT+强化学习），实现了向轻量级LLM的高效迁移。

### Q3: 论文如何解决这个问题？

CastFSR将上下文感知的时间序列预测建模为一个“快思考-慢推理-反思”的序列决策过程，核心创新在于将预测逻辑与协调策略解耦，让LLM负责编排而非直接生成数值。

整体框架包含三个主要模块。**快思考阶段**通过模块化工具集（特征提取工具+预测模型库）对历史序列进行趋势分析、季节性检测、统计画像和数据质量检查，然后自适应选择统计模型、深度模型或基础模型生成数据驱动的数值先验，利用成熟预测器的归纳偏置保证数值稳定性。**慢推理阶段**首先进行上下文认知，自适应搜索长程上下文历史并选择与预测视界对齐的窗口（不同因素具有不同时间尺度），检索结构化证据；随后评估上下文影响的方向、幅度和时间范围，若证据微弱或与历史模式冗余则保留原先验，否则对相关时间戳或片段施加上下文校准的调整，生成候选预测。**反思阶段**执行三类一致性检查：时间一致性（趋势、季节、转折点、连续性）、上下文一致性（修订是否被证据支持）和领域一致性（单位、非负性、容量限制等），对局部不一致进行定向修正而非整体重新生成，最终输出预测窗口和可解释轨迹报告。

创新点包括：将预测器作为可调用的工具而非固定组件，实现输入到模型的动态路由；自适应回看窗口替代固定窗口；以及通过两阶段训练（SFT学习可执行行为+GRPO强化学习优化完整决策轨迹）将工作流能力内化到紧凑模型中，支持免训练推理和高效部署两种模式。

### Q4: 论文做了哪些实验？

论文在多个真实世界数据集上进行了全面实验。实验设置包括长短期预测任务：长期任务使用96的look-back/horizon，短期任务使用168/24，评估指标为MSE和MAE。数据集涵盖ETT基准（ETTh1、ETTh2、ETTm1、ETTm2）、Wind、以及EPF基准的电力价格数据集（BE、DE、FR、NP、PJM）。

对比方法包括统计方法（ARIMA、Prophet）、深度学习方法（DLinear、ConvTimeNet、PatchTST、iTransformer、TimeXer）、基础模型（TimesFM、Sundial）、LLM方法（OFA、Time-LLM、TokenCast等）以及智能体系统（TimeSeriesScientist、AlphaCast）。主要结果中，CastFSR-Zero和CastFSR-R1在大多数指标上取得最优或次优性能，其中CastFSR-R1在ETTh1上达到MSE 0.077、MAE 0.210。

消融实验验证了三个模块的互补性，移除Fast-thinking导致最大性能下降。此外还评估了不同LLM协调器（GPT-5.6-sol、DeepSeek V4 Flash等）的泛化性，以及SFT和RL训练策略的贡献，两者均能提升性能。案例分析展示了模型在风功率预测中自适应平衡历史模式与上下文特征的能力。

### Q5: 有什么可以进一步探索的点？

CastFSR在框架设计上已较为完整，但仍有若干可探索的深化方向。首先，其Fast与Slow模块的耦合依赖LLM对上下文证据的检索质量，当外部知识库稀疏或噪声较大时，推理可能退化；可引入检索结果的置信度评分，并让Reflect阶段据此动态调整修正强度。其次，当前验证主要基于数值误差，缺乏对预测结果可解释性的量化评估，未来可设计面向“上下文-预测偏差”归因的指标，以检验模型是否真正捕捉了因果驱动因素。第三，两阶段训练策略中，SFT与RL的奖励函数仅关注精度，未纳入时间一致性或领域约束的软惩罚，可探索多目标RL以平衡精度与约束满足。此外，框架对多变量间复杂交互的建模仍偏隐式，可尝试在Slow阶段显式构建变量关系图，并利用图神经网络增强上下文推理。最后，跨域泛化能力尚未充分验证，可设计元学习机制，使框架在少量样本下快速适应新领域。

### Q6: 总结一下论文的主要内容

CastFSR提出了一种面向上下文感知时间序列预测的智能体推理框架，将预测任务重构为“快-慢-反思”三阶段决策流程。在快思考阶段，框架通过分析观测数据并选择轻量级预测器，构建数据驱动的预测先验；慢思考阶段则检索上下文证据、自适应确定有效回看窗口，并推理上下文如何重塑未来动态；反思阶段通过迭代优化，确保预测满足时间、上下文和领域一致性约束。该方法支持两种部署模式：直接使用现成大语言模型的无训练推理，以及通过两阶段监督微调和强化学习将编排能力迁移至紧凑模型的高效部署。在多个公开数据集上的实验表明，CastFSR显著优于代表性基线，验证了数据驱动先验构建、上下文感知时序推理与约束感知预测验证三者互补的有效性，为复杂系统决策提供了更可靠的预测基础。
