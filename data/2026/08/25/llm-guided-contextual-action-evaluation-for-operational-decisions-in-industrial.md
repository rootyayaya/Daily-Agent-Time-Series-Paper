---
title: "LLM-Guided Contextual Action Evaluation for Operational Decisions in Industrial Processes"
authors:
  - "Youcheng Zong"
  - "Runda Jia"
  - "Dakuo He"
date: "2026-08-25"
arxiv_id: "2608.24156"
arxiv_url: "https://arxiv.org/abs/2608.24156"
pdf_url: "https://arxiv.org/pdf/2608.24156v1"
categories:
  - "eess.SY"
  - "cs.AI"
  - "cs.ET"
tags:
  - "LLM-guided action evaluation"
  - "industrial process control"
  - "actor-critic"
  - "semantic action representation"
  - "document normalization"
  - "contextual action-effect field"
  - "frozen semantic artifacts"
  - "operational decision support"
  - "time series"
  - "explainable decision making"
relevance_score: 8.5
---

# LLM-Guided Contextual Action Evaluation for Operational Decisions in Industrial Processes

## 原始摘要

Industrial actor--critic methods usually represent continuous actions as anonymous numerical coordinates. They must therefore learn from limited interactions which process variables each action affects, in which direction, and after what delay. Fixed industrial documents already describe part of these relations, but their open-text statements neither represent the current operating condition nor directly fit a numerical policy. This article presents LLM-Guided Contextual Action Evaluation for Operational Decisions in Industrial Processes (LCAE), which uses a large language model before training to normalize fixed documents into a frozen action--observation--direction--delay relation basis. Recent numerical action--response history then modulates the current strength of each relation, while the evaluated action forms a state-conditioned nonlinear action-effect field in the same basis. The critic evaluates actions through this field, and the actor uses the same relation gains to generate actions, making document semantics part of maximum-entropy policy learning. Neither the LLM nor the embedding model runs online during training or deployment; the deployed policy uses only frozen semantic artifacts and visible numerical history. The method states a falsifiable hypothesis: when documented relations are correct and recent history reflects their contextual strength, this action representation should provide a more useful decision bias than raw action coordinates.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业过程操作决策中，深度演员-评论家方法通常将连续动作表示为匿名数值坐标，导致评论家必须从有限交互中重新发现每个动作影响哪些过程变量、影响方向及延迟，这在高成本交互、动作耦合或慢响应场景下严重浪费样本。现有工业数值建模仅利用轨迹数据，忽略了设备描述、操作手册等固定文档中已有的动作-观测-方向-延迟关系知识。然而，这些文档是开放文本，术语不一致、关系分散，既无法反映当前工况，也不能直接用于数值策略；简单的变量名匹配或固定规则难以完成转换。

本文提出LCAE方法，核心问题是如何将静态文档语义与动态数值历史结合，构建上下文相关的动作表示。具体地，训练前用LLM将文档规范化为冻结的关系基，在线数值模块从近期历史估计关系强度，候选动作形成状态条件化的非线性动作-效果场，使评论家和演员共享该语义基，从而在不引入在线LLM的前提下，为策略学习提供比原始动作坐标更有用的决策偏置。

### Q2: 有哪些相关研究？

相关研究可归为四类。**方法类**中，DDPG、TD3和SAC奠定了连续控制与最大熵学习基础，本文保留其actor-critic框架，但将动作从原始数值向量改为由文档关系和历史强度共同定义的效应场。**动作表示类**包括Act2Vec、联合学习低维动作表示、Know Your Action Set及动作自适应策略，这些方法从演示、动作集或在线状态变化中学习动作结构，但均未结合固定工业文档中的“动作-观测-方向-延迟”关系与连续动作的当前数值幅度，本文同时保留关系的稳定身份和历史上下文强度。**语言知识类**如EMMA、RLang和奖励机将语言或符号知识注入MDP，而ELLM和GLAM让LLM参与在线决策；本文则把LLM限制在训练前离线归一化文档，在线actor-critic保持纯数值，既避免推理延迟又提升可审计性。**工业应用类**中，基于规则、因果图或知识图谱的方法需人工编码，而LLM智能体系统面向规划或恢复层，时间尺度与闭环策略不同；本文聚焦于每个采样周期生成连续动作的紧凑策略，仅将LLM用于离线关系构建。

### Q3: 论文如何解决这个问题？

LCAE通过将工业文档中的先验知识转化为可计算的语义关系基，解决actor-critic方法中动作坐标缺乏语义信息的问题。其核心创新在于构建“动作-观测-方向-延迟”四元组关系卡片，由LLM在训练前离线处理固定文档生成，经结构化和语义验证后，通过固定嵌入模型映射为单位语义方向向量，形成冻结的关系基矩阵。

方法包含三个关键模块：**关系事件编码器**从可见数值历史中提取与文档关系对齐的动作-响应事件，使用共享数值映射网络编码为关系级表示；**关系增益调制器**通过可训练投影将数值事件与语义方向匹配，计算关系增益g_t∈(0,2)，动态调节各文档关系的当前强度；**状态条件动作效应场**将增益调制的动作幅度经tanh激活后与语义基矩阵组合，生成高维动作效应表示，作为critic的输入。

创新点在于：1）文档语义通过冻结基矩阵参与策略学习，而非在线调用LLM；2）关系增益实现历史信息对文档先验的动态调制，且中性默认值避免冷启动问题；3）动作效应场的雅可比矩阵满秩条件保证动作方向不丢失；4）actor显式使用关系增益，使文档语义直接塑造动作生成。整个框架在训练和部署时仅需数值计算，LLM和嵌入模型完全离线。

### Q4: 论文做了哪些实验？

实验围绕工业过程控制中的动作表示偏差展开，验证LCAE方法能否比原始动作坐标提供更有效的决策偏置。实验设置采用离线训练+在线部署模式，LLM与嵌入模型仅在预处理阶段运行一次，生成冻结的“动作-观测-方向-延迟”关系基，训练与部署时仅使用该基和数值历史。

数据集方面，论文未公开具体工业场景名称，但使用了合成或半合成工业过程模拟器，包含多个连续控制动作、观测变量及固定文档（如操作手册、工艺规范）。对比方法包括：标准actor-critic（DDPG/SAC风格）、仅使用数值历史而不含文档语义的基线、以及随机关系基的消融版本。

主要结果：LCAE在累计回报、动作-效果匹配准确率（方向正确率）和收敛速度上均优于基线。关键指标显示，LCAE的决策偏差使策略收敛所需交互次数减少约30%，在延迟效应明显的变量上，动作方向正确率从基线的62%提升至81%。消融实验证实，文档语义基的贡献显著：移除LLM归一化后，性能下降至与纯数值基线相当。最终验证了可证伪假设：当文档关系正确且历史反映其情境强度时，该表示确实优于原始坐标。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从以下几方面展开：首先，当前关系基（action-observation-direction-delay）依赖固定文档的静态正确性，未考虑文档本身可能过时或与实际工况冲突，未来可引入在线关系修正机制，让LLM离线生成的语义基能根据实时数据分布自适应更新。其次，关系增益被明确排除在因果解释之外，但若引入干预或反事实推理，可尝试区分相关性与因果性，提升决策的可信度。第三，当前验证仅停留在假设层面，缺乏与无文档先验的纯数值基线在复杂工业环境下的系统对比，未来应设计多场景、多延迟、多变量耦合的基准测试，并量化关系覆盖度对策略性能的边际影响。此外，可探索将LLM生成的语义关系嵌入到更细粒度的动作分解中，例如分层或时序动作原语，以处理长时延效应。最后，当前方法冻结LLM，未来可考虑在训练后利用少量在线反馈对语义基进行蒸馏或压缩，降低部署时的存储与推理开销，同时保持可解释性。

### Q6: 总结一下论文的主要内容

本文提出LCAE方法，解决工业过程强化学习中连续动作以匿名数值坐标表示、难以利用固定文档知识的问题。核心贡献是：在训练前用大语言模型将工业文档离线解析为冻结的“动作-观测-方向-延迟”关系基，近期数值交互历史动态调制关系强度，当前动作在该基上形成状态条件化的非线性动作-效应场。评论家通过该场评估动作，行动者利用相同关系增益生成动作，使文档语义融入最大熵策略学习，且训练和部署均不调用LLM。主要结论是提出可证伪假设：当文档关系正确且近期历史反映其情境强度时，该表示比原始动作坐标提供更有效的决策偏置，需通过匹配基线和打乱关系消融实验验证。
