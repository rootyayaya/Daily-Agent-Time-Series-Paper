---
title: "CLOUDADV: Decision-Aligned Instance Sizing with Zero-Shot Foundation Models under Drift"
authors:
  - "Jack Bell"
  - "Giacomo Carfi"
  - "Gerlando Gramaglia"
  - "Andrea Simioni"
  - "Daniele Fontani"
  - "Vincenzo Lomonaco"
date: "2026-06-30"
arxiv_id: "2606.31470"
arxiv_url: "https://arxiv.org/abs/2606.31470"
pdf_url: "https://arxiv.org/pdf/2606.31470v1"
categories:
  - "cs.AI"
tags:
  - "时间序列预测"
  - "零样本基础模型"
  - "云资源优化"
  - "LLM推荐生成"
  - "漂移适应"
  - "决策对齐"
  - "成本节约评估"
relevance_score: 6.5
---

# CLOUDADV: Decision-Aligned Instance Sizing with Zero-Shot Foundation Models under Drift

## 原始摘要

Cloud virtual machines are often overprovisioned, creating avoidable cost and operational inefficiency. We present CLOUDADV, an interactive engineer-facing advisory system for cloud instance sizing under workload drift. The system combines zero-shot time-series forecasting with bounded recommendation generation across day-, week-, and month-scale planning horizons. For each query, CLOUDADV constructs a structured decision context from historical utilization, forecast summaries, current VM metadata, candidate instance options, pricing, and explicit sizing heuristics. A higher-capacity LLM is used offline to generate reference recommendations, while a smaller production model is evaluated on the same prompts to assess deployment-time alignment under latency and cost constraints. Evaluation prioritizes downstream recommendation quality using simulated Azure cost savings and ex-post exceedance, with rolling-origin forecast accuracy reported as a secondary diagnostic against classical and supervised baselines. In a case study of seven production VMs, the reference recommendations reduce simulated monthly cost from about \$1,503 to \$708, yielding \$795/month in savings (52.9%) under conservative heuristic constraints, while the highest observed exceedance rate among downgraded cases is 1.5%. Although Chronos-2 does not minimize every forecasting metric, it often induces recommendation patterns similar to those of a supervised per-VM baseline. These results suggest that zero-shot foundation models can support decision-aligned provisioning in non-stationary cloud environments while reducing the operational burden of repeated per-tenant retraining, revalidation, and redeployment.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

云计算虚拟机常因过度配置导致成本浪费和运营低效。现有方法依赖为每个虚拟机单独训练的监督式预测模型，但工作负载漂移会使模型过时，需频繁重训练、验证和部署，运维负担重。同时，传统评估仅关注预测误差，忽略了决策对齐——即预测虽数值有偏差，却可能仍支持正确扩缩容决策，而低误差预测若误判决策边界反而有害。本文核心问题是：在非平稳云环境下，零样本时序基础模型能否在避免重复训练的前提下，实现决策对齐的实例规格推荐？为此，论文提出CLOUDADV系统，结合零样本预测、结构化上下文构建与LLM约束推荐，并引入参考模型与生产模型的分离评估框架，以模拟成本节省和超限率为核心指标，检验零样本模型在漂移场景下维持推荐质量的能力。

### Q2: 有哪些相关研究？

该论文的相关研究主要分为以下几类：

1. **预测驱动的资源配置研究**：如Cortez等人的Resource Central工作，证明了VM工作负载行为的一致性可用于预测驱动的调度。本文在此基础上，进一步考虑了工作负载漂移，并采用零样本基础模型避免重复训练。

2. **现有商业工具与局限性**：如Azure Advisor和AWS Compute Optimizer，它们依赖基于百分位数的启发式方法，仅提供点状建议，缺乏前瞻性预测和工程师反馈机制。本文提出的CLOUDADV通过概率性长期预测和人在回路验证工作流解决了这些局限。

3. **时间序列预测方法**：包括经典统计方法（ARIMA、指数平滑、Prophet）和深度学习方法（LSTM、TCN、TSMixer）。本文指出这些方法在非平稳云环境下长时预测性能下降，而零样本基础模型（如TimesFM、Chronos）无需针对每个VM重新训练，能更好地应对漂移。

4. **基础模型在时间序列中的应用**：TimesFM和Chronos等模型展示了强大的零样本预测能力。本文评估了Chronos-2在零样本配置下的表现，发现其虽未最小化所有预测指标，但能产生与监督基线相似的推荐模式，验证了决策对齐的评估视角。

本文与上述工作的核心区别在于：强调**决策对齐**而非原始误差最小化，并首次将零样本基础模型与交互式工程师建议系统结合，在非平稳云环境中实现无需重复训练的资源优化。

### Q3: 论文如何解决这个问题？

CLOUDADV通过一个“预测到决策”的流水线来解决云虚拟机实例大小调整问题。其核心方法是将零样本时间序列预测与有界推荐生成相结合，并构建结构化决策上下文来指导大型语言模型（LLM）生成最终建议。

整体框架是一个面向工程师的交互式咨询系统。主要模块包括：1）**遥测数据处理模块**，负责对CPU和内存利用率时间序列进行重采样和插值；2）**零样本预测模块**，使用Chronos-2等基础模型生成概率性预测，并提取95百分位数作为保守需求估计；3）**有界决策上下文构建模块**，将当前SKU、历史摘要、预测摘要、候选SKU集、定价信息和显式调整启发式规则（如头部空间参数τ_cpu=0.85、τ_mem=0.80，以及候选SKU限制因子δ=2.0）组装成结构化上下文；4）**推荐生成模块**，使用LLM（如Claude Opus作为参考模型，Qwen3.5-35B作为生产模型）从该上下文中生成包含动作、目标SKU和理由的结构化推荐记录。

关键技术包括：使用有效95百分位数（历史与预测的最大值）来避免瞬态低估；通过启发式规则约束可行决策空间，确保安全性和成本效益；以及输出验证机制，确保生成的标识符和数值与检索证据一致。创新点在于将预测作为中间信号而非最终目标，通过结构化上下文将LLM的生成限制在有界决策空间内，从而在零样本设置下实现安全、可防御的实例大小调整，同时避免了对每个租户进行重复训练和部署的运维负担。

### Q4: 论文做了哪些实验？

论文在7台真实生产虚拟机的遥测数据上进行了实验。数据经过预处理（去重、线性插值、裁剪至0.1以上、Min-Max归一化），按时间顺序划分为60%训练、20%验证和20%测试。实验设置了三种规划周期：日尺度（30分钟间隔，预测48步）、周尺度（6小时间隔，预测4步）和月尺度（12小时间隔，预测2步）。对比方法包括经典统计模型（Naive Seasonal、ARIMA、Prophet）、神经网络（TSMixer）以及预训练基础模型（Chronos-2、TimesFM 2.5）。此外，还评估了两种零样本LLM配置（高容量参考模型和低容量生产模型）的推荐质量。主要结果：在7台VM的案例研究中，参考模型将模拟月成本从约1503美元降至708美元，节省795美元/月（52.9%），降级案例的最高超限率为1.5%。Chronos-2虽未在所有预测指标上最优，但其推荐模式与监督基线相似。实验表明，零样本基础模型能在非平稳云环境中支持决策对齐的实例配置，同时减少重复训练和部署的运维负担。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：仅基于7个生产VM的案例研究，规模较小；仅评估了CPU和内存指标，未涉及网络I/O、磁盘等关键资源；未考虑多VM协同调度的复杂场景；且仅使用Chronos-2单一基础模型。未来可探索：1）在更大规模、更多样化的VM集群上验证，并引入多模态资源预测（如网络、存储）；2）设计自适应漂移检测机制，动态调整推荐频率和约束边界；3）将LLM Agent与强化学习结合，实现推荐策略的在线自优化；4）探索多模型集成策略，利用不同基础模型在特定资源或时间尺度上的互补优势；5）增加可解释性模块，向工程师解释“为何推荐此规格”的因果推理过程，提升信任度。

### Q6: 总结一下论文的主要内容

CLOUDADV提出了一种面向工程师的云实例大小调整咨询系统，旨在解决工作负载漂移下的虚拟机过度配置问题。该方法结合零样本时间序列预测与有界推荐生成，覆盖日、周、月三个规划周期。系统从历史利用率、预测摘要、当前VM元数据、候选实例选项、定价和显式调整启发式规则中构建结构化决策上下文，利用高容量LLM离线生成参考推荐，并在延迟和成本约束下评估小模型的对齐效果。评估以模拟Azure成本节约和事后超标率为首要指标，滚动预测准确性为次要诊断指标。在七个生产VM案例中，参考推荐将模拟月成本从约1503美元降至708美元，节省52.9%，最高超标率仅1.5%。研究表明，零样本基础模型（如Chronos-2）虽未最小化所有预测指标，但能产生与监督基线相似的推荐模式，支持非平稳云环境中的决策对齐配置，同时减少重复训练、验证和部署的运维负担。
