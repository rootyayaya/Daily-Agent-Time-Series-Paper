---
title: "EvoTS-Agent: A Self-Evolving LLM Agent for Financial Time Series Change Point Detection"
authors:
  - "Lei Jiang"
  - "Ye Wei"
  - "Xinyu Xi"
  - "Jordan Langham-Lopez"
  - "Yifan Bao"
  - "Raad Khraishi"
  - "Yihao Ang"
  - "Anthony K. H. Tung"
  - "Lukasz Szpruch"
  - "Hao Ni"
date: "2026-08-18"
arxiv_id: "2608.17933"
arxiv_url: "https://arxiv.org/abs/2608.17933"
pdf_url: "https://arxiv.org/pdf/2608.17933v1"
categories:
  - "cs.AI"
  - "cs.CE"
tags:
  - "LLM Agent"
  - "Time Series Change Point Detection"
  - "Self-Evolving"
  - "Validation-Guided"
  - "Tool Use"
  - "Financial Time Series"
  - "Autonomous Model Selection"
  - "Experiment Trajectory Evolution"
  - "Revision/Alternative/Recombination"
  - "Agentic Time Series"
relevance_score: 8.5
---

# EvoTS-Agent: A Self-Evolving LLM Agent for Financial Time Series Change Point Detection

## 原始摘要

Financial time series exhibit non-stationary and heterogeneous statistical properties, making change-point detection challenging because no single unsupervised algorithm performs consistently across assets and market regimes. Conventional workflows consequently depend heavily on expert-driven model selection, feature design, and hyperparameter tuning, limiting their scalability and adaptability. We propose EvoTS-Agent, a validation-guided self-evolving LLM agent for autonomous financial time-series change-point detection. EvoTS-Agent first performs curated exploratory data analysis to characterize dataset properties and initialize candidate detection models. It then evolves executable experiment trajectories through three complementary operators: \textit{Revision} exploits the current best solution, \textit{Alternative Strategy} explores fundamentally different modeling directions when progress stagnates, and \textit{Recombination} synthesizes complementary evidence from high-performing trajectories. Validation feedback guides trajectory evolution throughout the search, enabling the agent to adapt its detection pipeline to the statistical characteristics of each dataset while preserving reliable optimization. Experiments across four benchmark datasets demonstrate that EvoTS-Agent consistently outperforms existing LLM-based agents while maintaining a 100\% execution success rate across all evaluated backbone LLMs.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

金融时间序列具有非平稳、异质性的统计特征，其变点检测面临核心挑战：没有任何单一无监督算法能在不同资产和市场状态下持续表现优异。传统工作流高度依赖专家进行模型选择、特征设计和超参数调优，这不仅难以规模化，且当市场统计特性变化时适应效率低下。

现有LLM智能体方法存在明显局限：预定义工作流限制了搜索策略的灵活性；检索式系统复用的历史经验难以迁移到统计特性不同的数据集；简单迭代优化缺乏显式机制来决定何时利用当前方案、何时探索根本性替代方案，且无法综合多个成功实验的互补证据，容易陷入次优建模方向。

本文提出EvoTS-Agent，一个验证引导的自进化LLM智能体，旨在解决自主金融时间序列变点检测问题。其核心创新在于通过修订、替代策略和重组三种互补算子，在闭环框架内进化可执行的实验轨迹，使检测流程能自适应每个数据集的统计特性，同时保持可靠的优化过程。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，经典统计方法（如最优分割、贝叶斯推断）假设段内分布参数恒定；非参数方法（如最大均值差异）放宽为整分布不变；深度学习方法（如KL-CPD）在隐表征空间检测变化；谱方法则关注频域特征。**智能体类**工作包括ReAct（通用推理-行动范式）、DS-Agent（案例推理）、ResearchAgent（文献检索迭代）、TS-Agent（金融时序建模流程化）及MOSAIC（蓝图模块编排），这些方法虽实现自动化，但多遵循预设流程或仅反复修正当前方案。**最相关工作**是SE-Agent，其通过修订、重组、精炼演化轨迹，但主要面向软件工程推理优化。

本文与上述工作的核心区别在于：EvoTS-Agent维护可执行的实验轨迹（记录计划、模型、变换、反馈、验证性能及谱系），并以验证结果动态控制演化策略——默认修订当前最优解，停滞时激活替代策略，最终基于证据重组。这使得经验反馈不仅决定保留哪个方案，更决定后续搜索方向，实现了搜索策略本身的自适应调整，而非单纯自动化或固定流程优化。

### Q3: 论文如何解决这个问题？

EvoTS-Agent通过“验证引导的自进化”框架解决金融时间序列变点检测中无监督算法难以跨资产和市场状态泛化的问题。其核心设计分为两个阶段：

**1. 探索性数据分析（EDA）与模型初始化**  
代理首先对时间序列进行轻量级EDA，提取时序、频谱和变点敏感特征（如滞后1自相关、趋势强度、非平稳性、频谱集中度、周期性和局部均值/方差差异）。这些元特征与原始可视化、任务元数据一起输入LLM选择器，从模型库中挑选K个主模型和至多2个备选模型。每个模型经初始实现和一次修订，生成2K条可执行实验轨迹存入记忆库，验证得分最高的轨迹成为当前最优解（incumbent）。

**2. 轨迹级进化优化**  
在优化阶段，代理通过三个互补算子迭代改进最优轨迹：  
- **Revision（修订）**：常规操作，基于当前最优脚本和近期成功轨迹生成单一可执行修改，调整表示、检测器配置、超参数或后处理。  
- **Alternative Strategy（替代策略）**：当修订改进低于阈值或无效时触发，利用停滞轨迹作为负证据，探索根本不同的建模方向或未尝试的EDA推荐模型。  
- **Recombination（重组）**：在最终迭代中，从多个高性能轨迹中合成互补组件，整合搜索过程中发现的有效思想。  

每个实验执行后均在验证集上评估，仅当得分严格优于当前最优时才更新incumbent。接受与停滞状态独立判定，允许小幅改进成为新最优但同步触发替代策略。所有轨迹（含实现、验证结果、代码修改和理由摘要）存入记忆库，支持后续决策。该设计确保100%执行成功率，并在四个基准数据集上超越现有LLM代理。

### Q4: 论文做了哪些实验？

论文在四个基准数据集上评估了EvoTS-Agent的变点检测性能：合成OU过程数据集（模拟均值回归金融过程）、均值-方差联合漂移数据集（模拟市场状态转换）、ADIA Lab结构突变挑战数据集（拼接为多断点序列）、以及真实世界的Bee Dance蜜蜂摆动行为数据集。每个数据集按时间顺序划分为训练集（60%）、验证集（20%）和测试集（20%）。

实验对比了三个LLM智能体基线（TS-Agent、DS-Agent、ResearchAgent），并使用四种骨干LLM（GPT-4o、GPT-5.4、Claude Sonnet-4.6和Sonnet-5）进行测试。模型库集成了八种检测方法，包括PELT、Bottom-up、Window、ChangeForest-RF/KNN、贝叶斯离线检测、KL-CPD及频谱差异基线。评估指标包括F1（主指标，±10样本容差）、精确率、召回率、Hausdorff距离（定位精度）和成功率。

主要结果显示：EvoTS-Agent在多数数据集和骨干模型上取得最优或次优F1分数，且在所有骨干模型下均保持100%执行成功率。例如，在均值-方差漂移数据集上，GPT-5.4的F1从基线0.568/0.562提升至0.833；在ADIA数据集上，GPT-4o的Hausdorff距离从212.0/130.6降至14.8，F1从0.235/0.461提升至0.500。相比之下，ResearchAgent虽偶获高分但成功率低至33.3%，而EvoTS-Agent始终稳定运行。

### Q5: 有什么可以进一步探索的点？

EvoTS-Agent在金融时间序列变点检测上展现了自进化能力，但仍存在若干可探索方向。首先，当前EDA特征（如局部均值/方差差异）主要捕捉一阶和二阶统计突变，对高阶矩变化或频谱结构突变（如周期性切换）不敏感，可引入小波散射或谱熵特征增强表征。其次，三个进化算子依赖验证集反馈，但金融数据非平稳性强，验证集分布可能漂移，可引入在线分布偏移检测或滚动窗口验证，提升鲁棒性。第三，轨迹记忆仅存储成功轨迹，失败轨迹仅作负面信号，可挖掘失败模式构建“反模式库”，加速搜索收敛。第四，模型库覆盖有限，可扩展至深度学习检测器（如基于Transformer的变点网络），并让LLM动态生成新模型结构。最后，当前仅用验证分数引导进化，未考虑计算成本或可解释性，可引入多目标优化，平衡检测精度与模型复杂度。此外，跨资产迁移学习值得探索，即利用历史任务经验初始化新任务的搜索起点。

### Q6: 总结一下论文的主要内容

EvoTS-Agent提出了一种自进化的LLM智能体框架，用于解决金融时间序列变点检测中因数据非平稳性和异质性导致的算法选择困难问题。该方法首先通过探索性数据分析（EDA）刻画数据集特性，初始化候选检测模型；随后通过三个互补算子演化实验轨迹：Revision利用当前最优解进行局部优化，Alternative Strategy在停滞时探索全新建模方向，Recombination综合多条高性能轨迹的互补证据。整个搜索过程由验证反馈引导，并采用保留最优解的机制确保性能不退化。在四个基准数据集上的实验表明，该框架在所有评估的后端LLM上均保持100%执行成功率，且一致优于现有基于LLM的智能体方法。其核心贡献在于将变点检测重构为可执行的科学实验搜索过程，实现了检测流程对数据特性的自适应，为可扩展、透明的金融变点检测提供了新范式。
