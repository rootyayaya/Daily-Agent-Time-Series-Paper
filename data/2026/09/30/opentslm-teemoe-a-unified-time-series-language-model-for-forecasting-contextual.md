---
title: "OpenTSLM TeeMoE: A Unified Time-Series Language Model for Forecasting, Contextual Prediction, and Reasoning"
authors:
  - "Tony Chen"
  - "Timo Stoffregen"
  - "Maxwell Xu"
  - "Thomas Kaar"
  - "Martin Maritsch"
  - "Geremia Pompei"
  - "Nicolas Zumarraga"
  - "Robert Jakob"
  - "Paul Schmiedmayer"
  - "Patrick Langer"
  - "Juncheng Liu"
date: "2026-09-30"
arxiv_id: "2609.40265"
arxiv_url: "https://arxiv.org/abs/2609.40265"
pdf_url: "https://arxiv.org/pdf/2609.40265v1"
github_url: "https://github.com/OpenTSLM/OpenTSLM-TeeMoE"
categories:
  - "cs.LG"
tags:
  - "Time-Series Language Model"
  - "Mixture-of-Experts"
  - "LoRA"
  - "Forecasting"
  - "Context-Conditioned Prediction"
  - "Temporal Reasoning"
  - "TimeSeriesExam"
  - "GIFT-Eval"
  - "Context is Key"
  - "Skill-MoE"
  - "External Numerical Specialists"
  - "Forecast Aggregation"
relevance_score: 8.5
---

# OpenTSLM TeeMoE: A Unified Time-Series Language Model for Forecasting, Contextual Prediction, and Reasoning

## 原始摘要

Real-world time-series applications increasingly require models that can handle time series forecasting, context-conditioned prediction, and language-based temporal reasoning. Yet current time-series foundation models remain fragmented across these capabilities: numerical specialists often provide the strongest forecasts, while language-based models offer broader contextual understanding and analysis. A central challenge is to unify these heterogeneous capabilities without reducing their individual performance. We introduce OpenTSLM TeeMoE, a generalist time-series language model that can forecast directly from observed time series, reason over textual context and temporal patterns, and synthesize and refine predictions from external numerical forecasting specialists. We independently train three low-rank experts for forecast aggregation, native forecasting, and temporal analysis over a shared backbone. A learned LoRA mixture-of-experts controller then weights their frozen parameter updates for each request. Our proposed model achieves strong performance on widely used benchmarks for time series forecasting, context-conditioned prediction, and language-based temporal reasoning, ranking among the top three on GIFT-Eval by mean MASE rank, Context is Key by RCRPS, and TimeSeriesExam by accuracy.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

现实世界的时间序列应用日益需要模型同时具备三类能力：对未来数值进行预测、结合文本上下文进行条件化预测，以及对时间模式进行语言化推理。然而当前的时间序列基础模型在这三类能力上呈现割裂状态：数值预测专家（TSFM）通常能给出最准确的预测，但缺乏对上下文的理解与分析能力；基于语言的时间序列模型（TSLM）虽能处理指令、上下文和分析性问题，却在纯数值预测精度上不及专门模型。已有的通用时序模型虽试图覆盖多任务，但更广的任务覆盖往往以牺牲单项任务的专家级性能为代价。因此本文的核心问题是：能否构建一个通用模型，在不稀释各专家能力的前提下，统一数值预测、上下文条件预测与时间推理？为此，作者提出 OpenTSLM TeeMoE，在共享的 Qwen3.6-27B 主干上独立训练三个低秩能力适配器（预测聚合、原生预测、时间分析），冻结后训练一个 LoRA 混合专家控制器为每个请求分配权重并选择输出路径，从而在保留专家性能的同时实现能力整合。

### Q2: 有哪些相关研究？

相关研究主要分为四类。方法类方面，TimesFM、Chronos、Moirai、Timer、Toto、Lag-Llama等时间序列基础模型通过大规模预训练实现跨域数值预测；GPT4TS、Time-LLM、PromptCast、LLMTime将语言模型适配到时间序列任务；OpenTSLM、ChatTS、TS-Reasoner则侧重语言化时序理解。应用类方面，Context is Key明确考察上下文条件下的预测，LLM as Forecasting Planner用语言模型规划引导数值预测器。评测类方面，GIFT-Eval、TimeSeriesExam等基准用于评估预测与推理能力。通用时序模型类方面，UniTS、MOMENT、TsLLM、TimeOmni-1、TimeOmni-VL在单一模型中处理多任务。专家组合类方面，FFORMA、Chroma、Synapse、CastStar研究预测集成与专家选择；LoRA、TEMPO、AdapterFusion、Arrow、MoLE、X-LoRA探索低秩适配与模块化组合。本文的区别在于：通过独立训练预测聚合、原生预测和时序分析三个低秩专家，并用请求级LoRA混合控制器组合冻结参数更新，从而在统一模型中同时保留数值预测、上下文预测与语言推理能力。

### Q3: 论文如何解决这个问题？

OpenTSLM TeeMoE 的核心思路是通过模块化 LoRA 专家混合，在冻结的共享语言骨干上统一三类异构能力，避免能力相互干扰。整体框架采用两遍前向：第一遍禁用所有适配器，仅用骨干生成请求表示，供控制器分配权重；第二遍按该权重组合适配器，并选择数值解码器或语言模型头输出结果。

三个专家独立训练：聚合专家先用 XGBoost 对八个预训练预测器按 CRPS 预测相对排名并池化为参考分位数，再与 Toto-FnF 十模型集成按标量权重融合，得到十三候选的参考预测；数值编码器将预测水平、不确定性和候选分歧编码为连续 token，解码器学习有界残差修正，并用分歧门控 g_t 在候选分歧大时收缩修正，同时保持分位数单调性。原生预测专家直接从历史与文本上下文生成时间戳-值对，采样多次形成经验预测分布。分析专家则通过语言头完成模式识别、异常检测、序列比较和统计关系解释等问答任务。

关键创新在于冻结骨干、三个适配器和聚合组件，仅训练一个线性控制器，将请求表示映射为三个 softmax 权重 π，按 W'=W+Σπ_e ΔW_e 在每层组合低秩更新，且整个响应共享同一混合权重。控制器训练同时使用各能力预测损失和输出格式损失，后者以 -log π_agg 监督数值与文本路径的选择，使聚合权重超过 0.5 时走数值解码器，否则走语言生成。这种设计既保留了各专家的专长，又实现了统一调度。

### Q4: 论文做了哪些实验？

论文在三个基准上评估了TeeMoE：GIFT-Eval（97个评估单元、371,330个预测窗口，指标为mean MASE rank）、Context is Key（CiK，355个实例、71类任务，指标RCRPS）和TimeSeriesExam（TSE，746道题，指标准确率）。主要结果：GIFT-Eval平均MASE排名19.990，CiK RCRPS为0.115，TSE准确率78.552%，三项均进入前三。模型总参数约40B（含27B语言骨干及外部预测模型与适配器），却在CiK上超过405B的Llama-3.1-405B-Instruct，在TSE上超过约117B的GPT-oss-120B，并优于GPT-5.2的预测修正。消融实验包括：单独激活三个专家（原生预测、分析、聚合）与组合对比，组合后CiK RCRPS较原生专家再降6.6%，TSE较分析专家提升0.134个百分点；组合控制实验（top-1路由、等权1/3、全强度1）显示学习权重平衡最佳；联合训练基线在三项任务上均逊于TeeMoE。训练成本方面，独立专家训练为30.756 H100 GPU小时，联合训练为58.657。数值集成实验比较了等权8/13模型池、XGBoost加权、Toto-FnF及其混合，学习加权显著优于均匀池化，且精修进一步提升混合结果。

### Q5: 有什么可以进一步探索的点？

论文的局限主要在于评估方式：三个基准分别独立考察预测、上下文预测与推理能力，未能检验真实场景中预测与推理交替进行的复合工作流，例如先给出预测、再用新上下文解释并修正预测的闭环过程。此外，实验仅基于单一骨干模型家族，结论能否迁移到其他架构与训练配方尚不明确。未来可探索的方向包括：构建交替式多轮评测协议，衡量模型在“预测—解释—修正”链条中的稳定性与一致性；将专家扩展到异常检测、因果归因等更多能力，并研究控制器在能力冲突时的动态权衡机制；引入不确定性感知的路由，让模型在数值专家与语言推理分歧时主动校准；以及探索专家与控制器联合微调、跨骨干迁移等更高效的训练策略。

### Q6: 总结一下论文的主要内容

论文针对现有时间序列基础模型能力割裂的问题——数值模型擅长预测，语言模型擅长上下文理解与推理——提出统一通用模型 OpenTSLM TeeMoE。其核心思路是在共享骨干网络上独立训练三个低秩专家，分别负责预测聚合、原生预测和时间序列分析，再由可学习的 LoRA 混合专家控制器为每个请求加权组合冻结的专家参数更新。实验表明，该模型在 GIFT-Eval、Context is Key 和 TimeSeriesExam 三个基准上均进入前三，分别以 MASE 排名、RCRPS 和准确率衡量。结论指出，模块化组合能有效保留各专家优势，训练成本更低，且支持单独重训某一能力，为构建通用时间序列模型提供了兼顾性能与灵活性的实用路径。
