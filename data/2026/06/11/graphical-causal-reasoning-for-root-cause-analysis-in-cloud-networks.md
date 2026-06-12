---
title: "Graphical Causal Reasoning for Root Cause Analysis in Cloud Networks"
authors:
  - "Fabien Chraim"
  - "Dominik Janzing"
  - "John Evans"
date: "2026-06-11"
arxiv_id: "2606.13532"
arxiv_url: "https://arxiv.org/abs/2606.13532"
pdf_url: "https://arxiv.org/pdf/2606.13532v1"
categories:
  - "cs.NI"
  - "cs.LG"
tags:
  - "因果发现"
  - "根因分析"
  - "云网络"
  - "图模型"
  - "格兰杰因果"
  - "时间序列"
  - "可解释性"
relevance_score: 6.5
---

# Graphical Causal Reasoning for Root Cause Analysis in Cloud Networks

## 原始摘要

Cloud-computing relies on large-scale networks which are inherently complex systems. In this paper, we present a novel approach to root cause analysis (RCA) of cloud network incidents, leveraging graph-based causal discovery techniques. Our method addresses the limitations of rule-based automation by introducing a spatiotemporal grouping strategy and an automation ontology to reduce the dimensionality of the problem. We construct a causal graph from binary time series data using bivariate Granger causality and conditional independence tests. For inference, we introduce a probabilistic method that assigns edge-specific conditional probabilities as a function of time lag, allowing for interpretable, time-aware root cause scoring via causal graph traversal.
  We evaluated the system using a labeled dataset of 35 production incidents from a major cloud provider. The model successfully recalled the correct root cause in 85.7% of incidents and produced an exact match in 74.3%. In production, the deployed system has been used in over 800 real-world incidents, with positive qualitative feedback from network engineers. These results highlight the practicality of a data-driven, causal approach to RCA in dynamic and large-scale operational environments.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

云计算依赖的大规模网络本质上是复杂系统，故障发生时会产生大量因果和症状信号，导致根因分析极具挑战。现有方法主要依赖基于规则的自动化，但这类方法难以扩展，无法捕捉动态的、拓扑感知的交互，且规则脆弱，需要运维人员持续维护，导致问题升级延迟和运营负担加重。本文旨在解决云网络中根因分析的可扩展性和准确性问题，核心是提出一种基于图因果发现的新方法。该方法通过引入时空分组策略和自动化本体来降低问题维度，利用二元格兰杰因果和条件独立性检验从二元时间序列数据构建因果图，并开发了一种概率推理方法，为每条边分配随时间延迟变化的条件概率，从而通过因果图遍历实现可解释的、时间感知的根因评分。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是传统RCA方法，如基于分布偏移比较的方法和RCD、CIRCA等因果推断方法，它们依赖清晰的事故前后分割和连续数据，缺乏时间感知建模。本文与之不同，仅使用二元异常指标，无需正常数据基线，直接在异常区间内学习因果图。第二类是微服务领域的RCA方法，如CausalRCA和BARO，它们使用深度生成模型和贝叶斯变化点检测，但面临可扩展性挑战且未建模滞后效应。本文通过引入时空分组策略和自动化本体降低维度，并采用格兰杰因果性和条件独立性检验构建因果图，更适合超大规模网络环境。第三类是知识图谱推理方法，如基于故障排查文档的概率推理，但缺乏时间传播建模和直接因果结构发现。本文创新性地将图因果发现与时空分组、自动化本体结合，提出边缘特定条件概率作为时间滞后函数的概率推理方法，实现了可解释、时间感知的根因评分。在评测上，本文使用35个生产事故标注数据集和800+实际事故验证，展示了数据驱动因果方法在动态大规模运维环境中的实用性。

### Q3: 论文如何解决这个问题？

该论文提出了一种基于图因果推理的云网络根因分析方法，核心方法包括因果图构建与概率推理。整体框架分为三部分：首先，通过时空分组策略和自动化本体论降低问题维度。自动化本体论将网络信号归纳为观察、故障、风险、动作四类节点，并定义其因果关系；时空分组则基于拓扑跳数和时间窗口收集事件，将变量空间从全网络缩减至单个事件内。其次，采用二元Granger因果检验和条件独立性测试构建因果图：对每对变量使用逻辑回归模型比较受限与非受限模型的似然比，若p值低于阈值则添加因果边；再通过三元组条件独立性测试（如C→B→A链）剔除间接边，得到有向图。最后，提出概率根因推理方法：为每条边计算时间延迟条件概率P(A=1|B=1, Δt)，基于历史事件按分钟分箱估计；推理时，对每个候选根因r，遍历图中所有到影响变量y的路径，计算路径似然（边概率乘积），取最大似然作为该候选得分，返回超过阈值θ的前三名。创新点包括：将因果发现适配于二进制事件序列、引入自动化本体论实现变量抽象、以及通过时间感知的条件概率实现可解释的根因评分。

### Q4: 论文做了哪些实验？

论文在真实云网络生产环境中部署了基于因果图的根因分析系统，并进行了系统性评估。实验采用来自某主要云提供商的35个高影响、低频生产事件作为标注数据集，这些事件均绕过了现有基于规则的自动化系统。对比方法包括专家设计的规则方法、选择事件中第一个信号、最后一个信号（紧邻影响前）以及离影响位置网络跳数最近的信号。主要结果如下：因果推理方法在35个事件中正确召回根因（recall@3）30次（85.7%），精确匹配26次（74.3%）；规则方法精确匹配17次（48.6%），正确召回22次（62.8%）；选择第一个信号精确匹配12次（34.3%）；选择最后一个信号精确匹配21次（60%）；选择最近信号精确匹配9次（25.7%），正确召回18次（51.4%）。此外，系统在七个月内处理了800多个真实事件，其中48个事件获得工程师星级评分：19个5星（完全正确），25个至少3星（部分正确）。实验表明，基于概率因果图的方法在精确度和召回率上显著优于纯时间或空间启发式基线，但低评分事件分析也揭示了空间建模压缩过度导致区分度不足的局限。

### Q5: 有什么可以进一步探索的点？

论文的主要局限性在于空间建模的抽象化导致信息损失，难以区分局部故障与邻近故障，也无法有效处理网络路径和端点相关的指标。未来可探索的方向包括：1) 引入更精细的空间粒度建模，例如将网络拓扑中的路径、节点和端点信息显式编码到因果图中，以提升对局部异常的区分能力；2) 在因果发现阶段加入显式的时间约束，如时间窗口或延迟分布先验，以增强Granger因果检验的准确性；3) 采用图神经网络（GNN）模型替代当前的路径遍历评分方法，利用其端到端学习能力自动捕捉时空依赖结构，同时保持可解释性。此外，可考虑融合多模态数据（如日志、指标、告警）构建异构因果图，并引入主动学习或在线更新机制，以应对动态网络环境中的概念漂移。这些改进有望在保持可扩展性的前提下，进一步提升根因定位的精度和鲁棒性。

### Q6: 总结一下论文的主要内容

这篇论文提出了一种基于图因果推理的云网络故障根因分析方法。针对传统规则自动化难以处理大规模动态网络的问题，作者通过时空分组策略和自动化本体来降低问题维度，利用二元格兰杰因果性和条件独立性检验从二进制时间序列数据中构建因果图。在推理阶段，提出了一种概率方法，为每条边分配与时间延迟相关的条件概率，通过遍历因果图实现可解释的、时间感知的根因评分。使用某云服务商35个生产事件数据集进行评估，模型在85.7%的案例中成功召回正确根因，74.3%实现精确匹配。该系统已部署于800多个真实事件中，获得工程师积极反馈。该研究证明了数据驱动的因果方法在大规模动态运营环境中进行根因分析的实用性和有效性。
