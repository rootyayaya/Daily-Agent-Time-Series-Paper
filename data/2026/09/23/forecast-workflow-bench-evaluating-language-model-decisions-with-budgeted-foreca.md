---
title: "Forecast Workflow Bench: Evaluating Language-Model Decisions with Budgeted Forecast Tools"
authors:
  - "Shunya Nagashima"
date: "2026-09-23"
arxiv_id: "2609.27385"
arxiv_url: "https://arxiv.org/abs/2609.27385"
pdf_url: "https://arxiv.org/pdf/2609.27385v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "LLM决策"
  - "时间序列基础模型"
  - "工具调用"
  - "预算约束"
  - "预测工作流"
  - "成本感知"
  - "基准测试"
  - "电力负荷预测"
  - "决策质量评估"
relevance_score: 8.5
---

# Forecast Workflow Bench: Evaluating Language-Model Decisions with Budgeted Forecast Tools

## 原始摘要

Time-series foundation models (TSFMs) provide forecasts for operational decisions, but accuracy alone does not determine their value. Evaluating agents that use these models requires measuring decision quality and forecast cost. FWBench evaluates this capability on 1,251 electricity and cycle-hire cases using fixed forecast tools and simulated capacity contracts. Agents select models, histories and horizons, then submit capacities to minimize a stated loss-cost objective. We evaluated two hosted and eight local configurations, including small language models, and tested local models with and without TSFMs. GPT-6 Astra bought inexpensive short-horizon forecasts selectively, using 2.5% of the budget, and outperformed fixed policies when the saved decisions were scored with three loss-cost weightings. FWBench enables reproducible evaluation of how language models select and use time-series forecasts to make decisions under cost constraints.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列基础模型虽能提供跨领域预测，但预测精度本身并不等同于决策价值。现有评估主要关注预测精度或预测器选择，却未衡量预测带来的容量决策改善是否足以抵消其成本。同时，近期开源的小规模时间序列基础模型（不足十亿参数）结合小型语言模型，已具备在无云端通信条件下支持本地决策的潜力，但现有基准尚未建立这类本地系统在成本约束下的决策能力评估，也未与专有 LLM 进行对比。本文提出 Forecast Workflow Bench（FWBench），旨在解决“语言模型如何在预算约束下选择并使用时间序列预测工具以做出高质量容量决策”这一核心问题。该基准基于 1,251 个电力与共享单车案例，使用固定预测工具和模拟容量合同，要求智能体选择模型、历史长度与预测视野，并提交容量以最小化给定的损失-成本目标，从而可复现地评估预测选择、预测成本与最终决策质量之间的权衡。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，时间序列基础模型（TSFM）研究关注跨任务预训练知识迁移，使模型能为运营决策提供预测。评测类方面，已有基准主要评估预测精度、预测器选择及更广泛的时间序列任务；TimeSeriesGym 评估时间序列工程能力，TemporalBench 评估上下文预测与事件推理。智能体类方面，近期语言模型智能体结合规划、记忆与外部工具，相关基准测试其工具使用、API 规划与调用、策略合规、有状态工具使用及工业运营能力；CostBench 衡量规划成本差距，EcoAgent-Bench 评估预算约束下的经济决策。与这些工作不同，FWBench 聚焦于预测选择如何影响容量决策与成本：它让托管与本地模型在相同固定预测工具、容量约束和预测预算下运行，要求智能体选择模型、历史与预测视野并提交容量，以最小化给定的损失-成本目标，从而可复现地评估语言模型在成本约束下如何选择和使用时间序列预测进行决策。

### Q3: 论文如何解决这个问题？

FWBench 的核心思路是把“预测精度”转化为“决策质量”，通过固定工具集与模拟容量合同来评测语言模型在预算约束下的预测工具选择与使用能力。

整体框架上，基准构建了 1,251 个电力与共享单车案例，数据来自 EIA-930 与 TfL。智能体在目标日前 1 天或 7 天观察小时级历史，选择预测模型、历史长度与预测视野，然后提交分块容量计划。评测不直接看预测误差，而是用决策损失衡量：对每个目标小时，损失由容量过剩惩罚与需求未满足惩罚加权组成，并施加容量可行域与相邻块爬坡约束。

主要模块包括：一是固定预测工具服务，如 Chronos-Bolt Tiny、Chronos-2、TimesFM 2.5，按模型、历史长度和视野收取信用；二是共享优化器，用动态规划在给定经典或 TSFM 预测下最小化期望合同损失；三是回放机制，允许智能体在历史起点上测试预测精度并支付费用；四是评分函数，将归一化超额损失与信用消耗等权组合，并设无效提交惩罚。

关键创新在于：第一，将 TSFM 评测从精度指标转向端到端决策价值；第二，引入预算约束，迫使智能体在预测成本与决策收益间权衡；第三，提供可复现的固定工具与模拟合同，使不同语言模型配置可在同一损失-成本目标下比较。实验显示 GPT-6 Astra 仅用 2.5% 预算选择性购买廉价短期预测，即在多种损失权重下优于固定策略，说明该框架能有效区分“会用预测做决策”的智能体。

### Q4: 论文做了哪些实验？

论文在FWBench基准上开展了系统实验。实验设置：T=24、d=3（八种动作）、α=0.3、r=0.30，每案例预算B=113,726预测积分、限12次工具调用；电力短缺权重按六小时分段（1,1,2,1.5），σ分别为0.0542（电力）和0.0434（共享单车）。数据集包含1,091个电力案例（50家机构，2026年2、7、8月）和160个共享单车案例（20个站点，2026年5月），共1,251例、22,518次对话。对比方法包括两个托管模型（GPT-6 Astra等，高推理强度）和八个本地配置（四个量化本地模型，思考开/关；含<10B的SLM与≥10B的较大模型），并与固定策略（Chronos-2、小时经验分布）及三种选择器对比。主要结果：Astra仅购买短时程Bolt Tiny预测，使用约2.5%–2.6%预算，S排名第一，在全部八个队列-提前期子集中点估计最优，且相对最佳免费策略和三种选择器的配对95%聚类自助区间排除零。本地配置均劣于小时经验分布；Gemma 4 E4B思考开启可完成全部案例但S高出一倍以上。TSFM访问未给任何本地配置带来显著收益，反而使Gemma 4 12B（无思考）和Qwen3.6（思考）的S显著上升。目标函数含成本后，Astra积分消耗降低98.5%，决策损失仅增1.6%。重打分显示Astra在0.25/0.75和0.75/0.25权重下仍居首。

### Q5: 有什么可以进一步探索的点？

论文的局限主要在覆盖范围与实验设计：仅两个领域、16个日期、模拟合同，周期租赁数据未计入未满足需求，天气因素可能造成站点间相关性，置信区间未做多重检验校正，固定电价与单一校准周也限制了经济解释力；托管模型对比缺少移除TSFM的消融与全量重复运行，通用测试框架无法区分完整智能体系统间的差异。未来可探索的方向包括：引入任务专用决策模型，扩展时间与领域覆盖，比较各自框架下的完整智能体系统，并在不同校准期重复TSFM可及性对比；同时测量边缘设备上的端到端延迟、内存与能耗，并保持工具与评分一致。此外，工具目录更新后需重建oracle参考，可考虑动态预算分配、多目标损失权重自适应以及真实合同与需求缺失场景下的鲁棒性评估。

### Q6: 总结一下论文的主要内容

FWBench 关注一个核心问题：时间序列基础模型（TSFM）的预测精度并不等同于其决策价值，评估使用这些模型的智能体需要同时衡量决策质量与预测成本。为此，论文提出了 FWBench 基准，在 1,251 个电力与共享单车案例上，使用固定预测工具和模拟容量合同，要求智能体选择模型、历史长度与预测视野，并提交容量以最小化给定的损失-成本目标。研究评估了两个托管配置和八个本地配置，包括小型语言模型，并测试了本地模型在有/无 TSFM 情况下的表现。结果显示，GPT-6 Astra 选择性地购买廉价短视野预测，仅用 2.5% 预算，在三种损失-成本权重下均优于固定策略；而完全有效的 SLM 方案仍落后于免费策略。该基准支持在统一工具与成本约束下可复现地评估语言模型如何选择和使用时间序列预测进行决策。
