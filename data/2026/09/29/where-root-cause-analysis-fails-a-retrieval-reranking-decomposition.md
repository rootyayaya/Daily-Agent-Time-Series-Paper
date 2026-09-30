---
title: "Where Root Cause Analysis Fails: A Retrieval-Reranking Decomposition"
authors:
  - "Hada Melino Muhammad"
  - "Luan Pham"
  - "Laure Barrière"
  - "Sachin Shetty"
  - "Leonardo Pulga"
  - "Flora D. Salim"
date: "2026-09-29"
arxiv_id: "2609.36686"
arxiv_url: "https://arxiv.org/abs/2609.36686"
pdf_url: "https://arxiv.org/pdf/2609.36686v1"
github_url: "https://github.com/cruiseresearchgroup/DecompRCA"
categories:
  - "cs.LG"
tags:
  - "Root Cause Analysis"
  - "Retrieval-Reranking Decomposition"
  - "LLM Reranker"
  - "Multi-Signal Retrieval"
  - "Industrial Sensor Diagnosis"
  - "Benchmark Audit"
  - "Top@k Accuracy"
  - "Causal Graph"
  - "System Description Document"
  - "Anomaly Detection"
relevance_score: 8.5
---

# Where Root Cause Analysis Fails: A Retrieval-Reranking Decomposition

## 原始摘要

Identifying the root cause of an anomaly among hundreds of sensors is critical for preventing safety incidents and costly downtime in complex monitored systems. Existing studies evaluate root cause analysis (RCA) methods using top@k accuracy. We show that this metric has a fundamental blind spot: it conflates two failure modes, retrieval failure, where the true cause is never considered, and reranking failure, where it is considered but ranked too low. In this work, we introduce a retrieval-reranking decomposition and audit four well-known benchmarks to expose this blind spot. Our experiments show that, on benchmarks with complex faults, statistical baselines mis-rank the true cause 79-100% of the time, and graph-based methods never clearly beat the best statistical baseline, whether their causal graphs are learned on short fault windows, on retrieved candidate pools guaranteed to contain the cause, or on multi-day normal-operation data. Meanwhile, on simple benchmarks where faults manifest significantly at their origin, retrieval is nearly solved (98-100%). Guided by the decomposition, we build a two-stage pipeline combining a multi-signal retriever with an LLM reranker that, as one fixed configuration, matches or exceeds the best baseline's top@1 accuracy on all six benchmark suites (by up to +12 points), with no causal graph or labeled data required. When all methods rank the same retrieved candidates with the true cause guaranteed present, adding a short system-description document lets the reranker lead the best baseline by +7 to +18 points on every benchmark. Code is available at https://github.com/cruiseresearchgroup/DecompRCA.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注复杂监控系统（如工业水处理、楼宇管理、云服务系统）中的根因分析（RCA）问题：当系统出现异常时，运维人员需要从成百上千个传感器中快速定位真正的故障源，以避免安全事故和高额损失。现有研究普遍采用 top@k 准确率来评估 RCA 方法，但本文指出该指标存在根本性盲点：它把两种本质不同的失败模式混为一谈——检索失败（真实根因从未进入候选集）与重排序失败（根因在候选集中但排名过低）。这一混淆导致文献中“从未检索到根因”的方法与“检索到但排错序”的方法在指标上表现相同，却需要完全不同的修复策略。此外，现有基准（如 WADI、SWaT）多基于微服务类直接故障，根因本身就是窗口中最显著的信号，而信息物理系统中故障会沿物理组件传播放大，真实根因被下游效应掩盖，使得仅在这些基准上评估的方法产生虚假的检索覆盖感。因此，本文的核心问题是：通过提出检索-重排序分解框架，系统审计现有基准与方法，揭示被单一排名指标掩盖的两类失败模式，并验证二者可被独立修复。

### Q2: 有哪些相关研究？

相关研究可分为四类。方法类中，单信号打分器如BARO、ε-Diagnosis、FaaSRCA、KPIRoot+、MicroHECL、TORAI、PRISM直接对每个时间序列打偏差分并排序，不显式构造候选集，因此top@k混淆了检索与重排两阶段，本文首次将其拆开度量。因果图类如CIRCA、CausalRCA、RUN、CHASE、REASON、RCD、MicroCERCL、Cloud Atlas把根因视为图中特权节点，但图学习本身即检索器，传播放大和短故障窗使图质量主导检索失败，本文在每场景设置下分离其两类失败。LLM类中，D-Bot、RCLAgent、AMER-RCL以多智能体探索隐式定义候选集却从不度量检索覆盖；KAT、RC-LLM、SpecRCA用LLM对已检测候选集做后验推理，SpecRCA的草稿-验证架构最接近本文两阶段流水线，但仅报告端到端精度。列表式重排类如RankGPT、Rank-without-GPT、FIRST、Rank-R1、Rank-K、AcuRank为本文LLM重排器提供范式。评测类中，RCAEval、PetShop、LEMMA-RCA提供基准，后者观察到OT数据性能下降却归因于数据复杂度而非检索-重排结构，本文则给出结构性解释。

### Q3: 论文如何解决这个问题？

论文的核心思路是把根因分析从单一的排序问题拆解为“检索”与“重排序”两个可独立优化的失败模式。作者首先指出，传统 top@k 指标混淆了两种失败：一是检索失败，即真实根因从未进入候选集；二是重排序失败，即根因在候选集中但排名过低。基于这一分解，论文构建了一个两阶段流水线作为验证工具。

第一阶段是多信号检索器。它不依赖因果图，而是融合三种互补信号来生成候选集：偏差幅度，用于捕捉直接故障中幅度最大的传感器；最早起始时间，用于恢复 HVAC 类渐变漂移中的先兆信号；离散状态变化，用于捕捉 SWaT 类执行器或模式切换故障。三种信号各自排序后按预算 K 均匀分配并去重合并，形成候选集 C，保证真实根因尽可能被包含。

第二阶段是 LLM 重排序器。对候选集中的每个传感器，构建证据记录，包括偏差幅度、首次起始时间、基线窗口与故障窗口的均值及绝对/相对偏移，将所有记录放入单个提示词中，由 LLM 返回排序。可选地，将描述系统架构与传播路径的自然语言文档注入系统提示，无需形式化为因果图。

该流水线完全无监督，不使用标注故障数据，且在所有数据集上使用同一配置。实验表明，该固定配置在六个基准套件上匹配或超过最佳基线的 top@1 准确率，最高提升 12 个百分点；当候选集保证包含真实根因时，加入简短系统描述文档可使重排序器领先最佳基线 7 至 18 个百分点。创新点在于将 RCA 失败模式显式分解，并用检索与 LLM 重排序分别对应解决，同时以自然语言领域知识替代形式化因果图。

### Q4: 论文做了哪些实验？

论文在四个运行基准上评估，覆盖两个领域：RCAEval 微服务基准含 Online Boutique、Sock Shop、Train Ticket 三个套件（各 n=125，服务级），以及工业控制基准 WADI（n=14）、SWaT（n=36）、HVAC（n=48，指标级）。对比两类基线：统计类 BARO、RCD、ε-Diagnosis；图类基于 PC/FCI 学习因果图后用 PageRank、随机游走或 CIRCA 排序。LLM 重排器为 gpt-oss-120b，T=1.0 运行 n=3，K=15，分无/有领域知识文档两种配置，报告 top@1/3/5 与 Avg@5，并定义 Retrieval@K 与 Rerank@k 分解。

主要结果：微服务基准上检索近乎解决（Retrieval@15 达 0.98–1.00），瓶颈在重排；工业 CPS 上统计基线重排错误率高达 79–100%，图方法从未明显超过最佳统计基线。两阶段流水线在全部六个基准套件上 top@1 匹配或超过最佳基线，最高提升 +12 个百分点；在检索受控池中加领域文档后领先最佳同池基线 +6.7 至 +18.1 个百分点。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来方向可从四方面展开。其一，评测基准规模小且仅覆盖水务与楼宇系统，传播型故障样本有限，未来需扩展到电力、化工、航空等更多工业场景，验证分解框架的普适性。其二，检索器配置在同一批基准上固定调参，存在过拟合风险，可探索跨域自适应检索与无监督候选池构建。其三，域知识文档目前为静态注入，未来可研究按故障类型动态检索与自适应摄入知识，甚至让 LLM 自主生成并校验系统描述。其四，LLM 重排器具有非确定性，且对分布外故障的置信度可能失准，可引入校准机制、集成多次采样或与因果图方法互补融合。此外，检测器决定检索基底，异常检测与 RCA 的联合协同设计是值得深入的方向，例如端到端可微的检测—检索—重排框架，以及人在回路中如何缓解自动化偏见，也是落地部署亟需探索的问题。

### Q6: 总结一下论文的主要内容

本论文针对复杂系统中根因分析（RCA）的评估方法展开研究，指出现有基于top@k准确率的评估存在根本性盲点：它混淆了检索失败（真实根因未被纳入候选集）与重排序失败（根因被纳入但排名过低）两种本质不同的失败模式。为此，作者提出检索-重排序分解框架，并审计了四个知名基准。实验表明，在复杂故障基准上，统计基线有79%-100%的概率将真实根因错误排序，而基于图的方法无论因果图如何学习，均未明显优于最佳统计基线；在简单故障基准上，检索几乎已解决（98%-100%）。基于该分解，作者构建了一个两阶段流水线，将多信号检索器与LLM重排序器结合，在无需因果图或标注数据的情况下，于六个基准套件上匹配或超越最佳基线的top@1准确率（最高提升12个百分点）。论文还发现，在保证真实根因存在于候选池时，加入简短系统描述文档可使重排序器领先基线7至18个百分点。该研究揭示了RCA评估的关键缺陷，并提出了实用且有效的解决方案。
