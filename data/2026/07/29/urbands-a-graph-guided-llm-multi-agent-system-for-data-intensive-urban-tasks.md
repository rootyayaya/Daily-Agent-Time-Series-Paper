---
title: "UrbanDS: A Graph-Guided LLM Multi-Agent System for Data-Intensive Urban Tasks"
authors:
  - "Zhilun Zhou"
  - "Jianghao Yu"
  - "Yuming Lin"
  - "yongjun yang"
  - "Sun Yongquan"
  - "Depeng Jin"
  - "Yong Li"
date: "2026-07-29"
arxiv_id: "2607.26724"
arxiv_url: "https://arxiv.org/abs/2607.26724"
pdf_url: "https://arxiv.org/pdf/2607.26724v1"
categories:
  - "cs.AI"
tags:
  - "LLM Agent"
  - "Multi-Agent System"
  - "Graph-Guided"
  - "Data Science Agent"
  - "Report Generation"
  - "Urban Data"
  - "Planner Agent"
  - "Execution Agent"
  - "Memory"
  - "User Feedback"
relevance_score: 7.5
---

# UrbanDS: A Graph-Guided LLM Multi-Agent System for Data-Intensive Urban Tasks

## 原始摘要

Large language model (LLM) agents have been widely applied in automating data science tasks. However, existing methods typically rely on a limited set of provided datasets, and they face challenges in data-intensive scenarios that require discovering and leveraging relevant information from large-scale and heterogeneous data repositories. Urban tasks are representative examples of such scenarios, as urban data are not only large-scale and multi-sourced, but also exhibit complex spatial, temporal, and semantic relationships. To address these challenges, we propose UrbanDS, a graph-guided LLM multi-agent system for data-intensive urban tasks. We first construct a unified dataset graph to organize reusable dataset skills and the relationships among datasets. Specifically, we develop a Data Profiling Agent that constructs a skill for each dataset. Moreover, a Relation Agent identifies relationships among datasets and integrates these relationships into the dataset graph. At runtime, a Planner Agent retrieves task-relevant datasets from the graph and generates execution plans. Multiple Execution Agents then perform data processing and analysis, while their execution progress and intermediate results are shared through a common memory. Finally, a Report Agent synthesizes the experimental logs into a report, which can be further refined based on user feedback. To systematically evaluate the capability of agents in handling data-intensive urban scenarios, we further construct UrbanDS-Bench, an urban data science benchmark covering representative data analysis and modeling tasks. Experiments on both general and urban benchmarks demonstrate that UrbanDS consistently outperforms existing data science agents on data-intensive tasks. Furthermore, UrbanDS has been deployed on the urban operations platform of Dongxihu District, Wuhan, demonstrating its effectiveness in real-world urban applications.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决数据密集型城市任务中，现有大语言模型（LLM）智能体系统难以从大规模、多源、异构的城市数据仓库中自主发现并利用相关数据集的问题。研究背景是，LLM智能体已被广泛应用于自动化数据科学流程，但现有方法通常依赖任务直接提供的少量数据集，缺乏在真实场景中从大型数据仓库中检索和整合信息的能力。现有方法的不足主要体现在：城市数据规模大、来源多（如交通、人口、经济等），且具有复杂的空间、时间和语义关系，导致智能体难以识别相关数据源并正确集成用于下游分析。本文要解决的核心问题是：如何设计一个LLM多智能体系统，使其能够自动组织大规模城市数据集、发现任务相关数据、生成执行计划、协同处理分析，并最终生成可迭代优化的报告，从而高效完成数据密集型城市分析任务。

### Q2: 有哪些相关研究？

相关研究可分为三类。第一类是数据科学智能体系统，包括DS-Agent（基于案例推理）、Data Interpreter（层次化图工作流）、AutoML-Agent（全流程自动化）、LAMBDA（自然语言交互）和DeepAnalyze（端到端分析模型）。这些系统依赖预提供数据集，缺乏从大规模异构数据仓库中自主发现和整合数据的能力。UrbanDS通过构建统一数据集图、可复用技能和显式关系来弥补这一不足。第二类是数据科学评测基准，如DS-1000、LLM4DS、DSBench、DABstep和DataSciBench，它们通常直接提供所需数据集，不评估数据发现能力。CoDA-Bench虽引入含数百数据集的噪声文件系统，但智能体仍难以兼顾数据发现与代码执行。UrbanDS-Bench则专门评测数据密集型城市场景下的数据集发现与多源数据整合能力。第三类是城市智能体基准，如CityBench和USTBench，它们评估城市推理与决策，但已预设任务环境与所需观测。UrbanDS-Bench要求智能体自主从大型数据池中发现相关数据集并执行分析，重点评测数据密集型仓库中的城市数据科学能力，而非单纯的城市知识或推理能力。

### Q3: 论文如何解决这个问题？

UrbanDS通过构建一个图引导的LLM多智能体系统来解决数据密集型城市任务中的挑战。其核心方法分为两个阶段：数据集图构建和任务执行。

在数据集图构建阶段，系统首先通过**数据画像智能体**对每个数据集进行一次性探索，生成包含内容、字段含义、时空范围、加载方法等信息的**数据集技能**，避免重复检查原始文件。接着，**关系智能体**识别数据集之间的三种关系：空间关系（空间覆盖重叠）、时间关系（时间范围重叠）和语义关系（字段指向同一实体）。对于语义关系，系统采用增量式**语义码本**方法，先为每个可能关联的字段分配代码，再由关系智能体验证并生成连接描述，从而高效地构建包含节点（数据集技能）和边（关系）的统一数据集图。

在任务执行阶段，**规划智能体**从图中逐步检索相关数据集：先查看所有数据集的名称和简短描述，再读取候选数据集的完整技能，并利用图邻居的紧凑摘要发现潜在有用数据，最终生成包含选定数据集和可执行步骤的分析计划。随后，多个**执行智能体**并行处理每个步骤，通过共享的**进度内存**记录观察结果、发现和生成文件，实现中间结果的复用。最后，**报告智能体**综合生成分析报告，**修订智能体**根据用户反馈进行迭代优化。

该系统的创新点在于：1）通过一次性探索和技能存储避免重复计算；2）利用图结构高效组织数据集关系并支持渐进式检索；3）多智能体协作与共享内存机制降低了代码生成复杂度并提升了执行效率。

### Q4: 论文做了哪些实验？

论文在两类基准上评估了UrbanDS。实验设置包括：UrbanDS-Bench（450个数据分析任务和8个数据建模任务）和CoDA-Bench的hard子集（119个任务，每个任务平均需从约1422个文件中定位资源）。对比方法包括DS-Agent、Data Interpreter、DeepAnalyze、AutoGen和Claude Code，除DeepAnalyze外均使用DeepSeek-V4-Pro。主要结果：UrbanDS在UrbanDS-Bench上总体准确率达70.0%（空间65.7%、时间83.6%、时空73.9%），优于最强基线Claude Code（62.9%），相对提升11.2%；在CoDA-Bench上准确率46.2%，比Claude Code提升10.0%。在数据建模任务中，UrbanDS在所有指标上均取得最佳，如POI签到预测R²达0.464（所有基线为负值）。消融实验显示，移除数据集关系使UrbanDS-Bench准确率降至66.7%，移除数据集技能降至58.9%。实际部署于武汉东西湖区，用户反馈分析时间从4.08小时降至0.73小时，加速5.6倍。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于当前系统主要面向用户指定的分析任务，缺乏在开放场景下的自主探索能力，如无预设问题时的数据挖掘、异常模式发现和新研究问题提出。未来可探索的方向包括：1) 增强Agent的主动探索机制，使其能基于数据集图谱自动识别数据间的潜在关联和异常信号，生成假设并验证；2) 引入因果推断和可解释性模块，帮助Agent理解数据生成过程，从而发现更深层的城市运行规律；3) 优化多Agent协作中的记忆共享策略，结合图结构信息实现更高效的推理路径规划；4) 扩展数据集图谱的动态更新能力，使系统能在线学习新数据源和任务经验。此外，可考虑将LLM与专用时序模型结合，提升对时空序列数据的处理精度。

### Q6: 总结一下论文的主要内容

UrbanDS提出了一种图引导的LLM多智能体系统，用于解决数据密集型城市任务中大规模异构数据发现与利用的挑战。核心贡献包括：1）构建统一的数据集图，通过数据画像智能体为每个数据集创建可复用技能，并由关系智能体识别数据集间的空间、时间和语义关系；2）运行时规划智能体从图中检索相关数据集并生成执行计划，多个执行智能体通过共享内存协作完成数据处理与分析，最终由报告智能体生成可迭代优化的报告。实验表明，UrbanDS在通用和城市基准测试中均优于现有数据科学智能体，并在武汉东西湖区城市运营平台成功部署，验证了其实际应用价值。该工作为城市数据科学中的自动化分析提供了新范式，但未来需扩展至无预设问题的开放探索场景。
