---
title: "NeoResearch: Literature- and Experience-Guided Autonomous Time Series Model Discovery"
authors:
  - "Ze Guo"
  - "Mingyue Cheng"
  - "Xiaoyu Tao"
  - "Shuo Yu"
  - "Shangtong Ye"
date: "2026-11-13"
arxiv_id: "2611.18235"
arxiv_url: "https://arxiv.org/abs/2611.18235"
pdf_url: "https://arxiv.org/pdf/2611.18235v1"
categories:
  - "cs.LG"
tags:
  - "LLM Agent"
  - "时间序列预测"
  - "自主模型发现"
  - "文献挖掘"
  - "经验记忆"
  - "双循环工作流"
  - "超参数优化"
  - "实验反馈"
  - "知识引导"
relevance_score: 7.5
---

# NeoResearch: Literature- and Experience-Guided Autonomous Time Series Model Discovery

## 原始摘要

Developing effective forecasting models for diverse time-series domains requires substantial expert knowledge, evidence from scientific literature on the web, and iterative experimentation. However, translating this knowledge and research experience into model designs requires preserving source context and testing applicability under task-specific assumptions. In this paper, we propose NeoResearch, a literature- and experience-guided autonomous research framework that leverages large language models (LLMs) as researchers to discover lightweight, domain-specific forecasting models. Specifically, NeoResearch establishes an expert-inspired dual-loop research workflow, coupling hypothesis-driven architecture exploration with iterative training and hyperparameter optimization through experimental feedback. To enable knowledge-grounded discovery, the agent autonomously mines scientific literature from the Web, extracting modeling mechanisms, empirical evidence, and applicability conditions to formulate task-grounded, testable architecture hypotheses. Furthermore, a hierarchical experience memory links literature findings to experimental outcomes and consolidates conditional lessons, guiding architecture discovery and training optimization while supporting reuse across forecasting tasks. Experiments on ten datasets show competitive performance and support dual loops, literature extraction, and memory reuse. Our code is available.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决如何利用网络科学文献与研究经验，自主发现轻量级、领域特定的时间序列预测模型这一问题。研究背景是：构建有效的预测模型需要专家知识、来自网络科学文献的证据以及迭代实验，但将这些知识与研究经验转化为模型设计，需要保留来源语境并在任务特定假设下检验其适用性。现有方法的不足体现在三方面：其一，架构探索与训练优化缺乏协调，性能不佳时难以判断是建模假设不当还是训练不足；其二，在线文献中的机制与实证结论产生于不同语境，直接使用难以保留来源证据与适用条件，且已有LLM智能体方法多依赖数值序列化或经验积累，未系统地将文献知识转化为可检验的设计决策；其三，实验历史难以提炼为可复用经验，无法说明“在何种条件下何种改动带来何种结果”。因此，本文的核心问题是：如何将网络科学证据转化为可检验的建模假设，并将实验结果整合为可复用经验，同时保留来源溯源、评估任务特定适用性，从而在无需LLM参与推理的情况下自主发现领域特定的轻量预测模型。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类。方法类：深度预测模型基于不同时间结构假设，包括循环网络、图网络、状态空间模型、分解方法（DLinear、TimeMixer）、卷积设计（TimesNet、ConvTimeNet）及Transformer变体（PatchTST、iTransformer、TimeXer），其适用性取决于任务特性；自动化方法则搜索预测架构与配置。LLM智能体类：TimeSeriesScientist结合诊断、模型选择与验证引导配置；MONAQ利用LLM估计生成资源受限架构；MetaCaster结合领域感知合成数据与轻量模型训练及工具优化。LLM驱动研究类：SciMON检索灵感并评估新颖性；ResearchAgent利用学术图谱与评审智能体细化问题与方法；CodeScientist、AI-Researcher连接文献与代码实现；NADER以搜索树组织论文启发的架构修改并保留成败经验；The AI Scientist与AIDE覆盖想法、实验与报告；R&D-Agent分离假设探索与方案开发，R&D-Agent-Quant与EvoScientist维护经验记忆以供复用。区别在于，NeoResearch聚焦文献与经验引导的领域特定预测架构发现，以双循环工作流协调架构假设与迭代训练优化，产出可脱离LLM独立预测的轻量模型，并通过分层经验记忆跨任务复用条件性经验。

### Q3: 论文如何解决这个问题？

NeoResearch 的核心思路是把大语言模型当作“自主研究员”，用专家式的双层循环工作流把文献知识与实验经验转化为轻量级领域专用预测模型。整体框架包含两个嵌套循环：外层“架构发现循环”负责从 Web 挖掘科学文献，提取建模机制、实证证据与适用条件，并结合数据诊断（缺失值、分布、时序动态、变量关系）和检索到的历史经验，形成任务相关、可检验的架构假设；每个假设需记录预期效果、可反驳的观测以及适用条件，再翻译为包含预处理与架构（建模范式、时间主干、变量交互、模块组合）的候选设计。内层“训练优化循环”在固定架构下迭代调整学习率、批大小、正则化、调度策略和训练损失，输出验证指标、收敛曲线与误差诊断，供外层反思假设、修正或替换架构。关键技术包括：以结构化“配方”记录设计、训练损失与训练配置，把假设与可执行实验绑定；通过受控对比隔离单一改动以做机制归因；维护持久化研究状态，链接假设、配方、运行、模型产物与评估；以及分层经验记忆，将文献发现、实验结局与适用条件关联并整合为条件性经验，支持跨任务复用，同时保留原始文献记录与 LLM 参数不变。创新点在于文献证据与实验反馈的双环耦合、带适用条件的假设管理、以及可迁移的分层经验记忆，最终发现的模型独立于 LLM 进行数值预测。

### Q4: 论文做了哪些实验？

论文在10个多变量输入、单目标预测任务上评估NeoResearch，覆盖电价、能源系统与水文领域：EPF基准的BE、DE、FR、NP、PJM，以及ETTh1、GEFCom2014-L、Windy、Sunny和MOPEX。EPF任务用168步历史预测24步电价，其余任务用96步预测96步，且仅使用观测到的过去协变量。对比方法包括16个预测基线（ARIMA、Prophet、GNN、MTGNN、RNN、LSTM、DeepAR、Mamba、S-Mamba、DLinear、TimeMixer、ConvTimeNet、TimesNet、PatchTST、iTransformer、TimeXer），以及AIDE和Optuna-TPE（预算25次迭代），指标为MSE和MAE。主要结果：NeoResearch在多数对比中取得最优，例如ETTh1 MSE 0.1004/MAE 0.2434，MOPEX 0.9812/0.5443，NP 0.3546/0.3618，PJM 0.1849/0.3093；Windy上MAE最低但MSE不及DLinear和DeepAR。消融显示完整双循环在所有10个任务上均优于w/o Outer Loop和w/o Inner Loop；移除架构级、优化级或全部记忆均使误差上升；去除文献抽取或知识也变差。研究模式对比中Alpha优于HMC和Zero；预算敏感性显示PJM随预算提升最稳定，NP和MOPEX在25次迭代最优、30次变差。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点。其一，实验仅覆盖十个中小规模单目标多变量预测任务，且候选模型限制在千万参数、单卡4090预算内，未来可扩展到长序列、概率预测、多变量联合预测及更高维工业场景，检验框架的可扩展性。其二，文献知识依赖网页检索与LLM抽取，存在来源偏差与幻觉风险，MOPEX上直接原文反而劣于无文献，说明抽取质量与适用条件判断仍是瓶颈，可探索检索增强验证、引用溯源与知识置信度加权。其三，经验记忆目前以任务为粒度冷启动复用，跨任务迁移的负迁移与顺序依赖尚未充分研究，可引入元学习式记忆检索或因果筛选。其四，搜索预算敏感性呈非单调，说明停止准则与假设多样性不足，可结合贝叶斯优化或进化策略提升候选产出率。此外，可解释性方面尚未分析LLM提出假设的推理链质量，未来可加入假设可证伪性评估与人机协同审计。

### Q6: 总结一下论文的主要内容

论文针对领域特定时间序列预测中科学知识与实验经验难以转化为可测试模型设计的问题，提出 NeoResearch 框架。其问题定义为：在固定研究预算下，利用网络文献与历史经验自主发现轻量级预测模型，并仅依据验证集选择最优模型。方法上，以通用 LLM 作为自主研究者，构建专家式双层循环工作流：外层循环挖掘文献中的建模机制、实证证据与适用条件，结合任务数据诊断和分层经验记忆提出可检验的架构假设；内层循环迭代优化训练配置与超参数，并将验证结果和收敛诊断反馈给外层以决定继续调优或重构架构。主要结论：在电力市场、能源系统和水文等十个数据集上，NeoResearch 在多数任务上优于代表性统计与神经预测方法及自动化模型开发基线；消融实验支持双层循环、结构化文献抽取和分层经验记忆的有效性，跨任务复用知识、经验与模型设计可提升目标任务表现，且所发现模型可脱离 LLM 独立预测。
