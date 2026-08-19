---
title: "Can Large Language Models Explain Flight Safety Events? A Prior-Guided Semantic LLM-based Approach"
authors:
  - "Lu Xu"
  - "Xu Li"
  - "Linjiang Zheng"
  - "Fan Li"
  - "Riquan Zhang"
  - "Jiaxing Shang"
date: "2026-08-18"
arxiv_id: "2608.18017"
arxiv_url: "https://arxiv.org/abs/2608.18017"
pdf_url: "https://arxiv.org/pdf/2608.18017v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "可解释时序诊断"
  - "LLM时间序列分析"
  - "自然语言报告生成"
  - "统计专家与LLM结合"
  - "提示工程"
  - "少样本学习"
  - "航空安全"
  - "飞行数据分析"
  - "故障解释"
relevance_score: 9.5
---

# Can Large Language Models Explain Flight Safety Events? A Prior-Guided Semantic LLM-based Approach

## 原始摘要

Improving flight safety with flight data requires not only accurate detection of risk events, but more importantly, clear interpretation of their underlying causes at the level of pilot control behavior. Existing explainable AI techniques, such as feature importance maps, often require considerable domain knowledge to translate them into operationally meaningful explanations. Large Language Models (LLMs), which excel at language reasoning, bring a promising solution to this issue. However, applying LLMs in this domain presents key challenges such as modal inconsistency, limited classification ability, scarcity of task-specific data for fine-tuning, and lack of domain knowledge. To overcome these challenges, we propose FlightLLM, a prior-guided semantic LLM-based approach for interpretable flight safety analysis. Specifically, we first perform feature engineering to address modal inconsistency, combining statistical descriptors with physically meaningful flight indicators. This representation is further processed by a Semantic Discretization module, which converts abstract numerical patterns into qualitative descriptions that are more compatible with language reasoning. In addition, since LLMs are not inherently strong classifiers, CatBoost is incorporated as a statistical expert, and its prediction results are injected into the prompt as prior guidance. A contrastive few-shot learning strategy is further adopted to compensate for limited data. Finally, we design structured prompts to embed aviation-specific knowledge into the inference process. Using hard landing, a representative risk event with complex causal mechanisms, as an anchor point, we evaluate FlightLLM on a dataset of 704 real-world A320 flight samples. Experimental results show that the proposed approach achieves competitive classification performance while generating direct and reasonable explanations for event causes.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

飞行安全事件分析正从单纯的事件监测转向对深层因果机制的挖掘，尤其是飞行员操控行为层面的归因。现有基于QAR多变量时间序列的研究存在明显不足：传统机器学习方法（如SVM、聚类）和深度模型（如LSTM、Transformer）虽能实现高精度分类，但本质上是“黑箱”，其输出（如注意力权重）仍需领域专家二次解读，难以直接转化为可操作的因果解释，导致模型输出与人类可理解的叙事之间存在鸿沟。

本文要解决的核心问题是：如何利用大语言模型（LLM）实现飞行安全事件的端到端可解释分析，即不仅准确检测风险事件，更能直接生成符合航空领域知识的因果文本解释。具体面临四大挑战：一是QAR高维时间序列与LLM文本处理间的跨模态不一致；二是LLM本身不擅长时间序列分类；三是飞行安全事件发生概率极低，缺乏大规模微调数据；四是通用LLM缺乏航空领域知识，易产生幻觉。

为此，论文提出FlightLLM框架，通过特征工程与语义离散化解决模态差异，引入CatBoost作为统计专家提供先验指导以弥补分类短板，采用对比少样本学习应对数据稀缺，并设计结构化提示注入领域知识，最终在真实A320数据集上实现竞争性分类性能与直接合理的因果解释。

### Q2: 有哪些相关研究？

在飞行安全事件解释领域，已有研究主要分为三类。**传统可解释性方法**：LIME和SHAP被广泛用于识别关键特征（如Khattak、Midtfjord等），但多聚焦于环境因素，忽略飞行员操作行为；CAM和注意力机制（如Li的IMTCN、Shang的双阶段注意力）虽能突出关键时间区域或参数，仍需领域专家事后解读，缺乏直接因果叙述。**LLM时间序列分析**：Yu等首次将LLM用于金融预测，Sun等总结了两类策略（改造LLM架构或转换数据表示）。后续工作如DSCA-GNN、向量量化映射、文本化描述提示等，多面向通用时序或异常检测（如AXIS、AnoCoT），但未结合飞行领域知识，且数据复杂度远低于QAR数据。**飞行安全预测模型**：Yang、Qi等结合特征选择与SHAP解释硬着陆，但解释仍停留在特征重要性层面。

本文FlightLLM的独特之处在于：一是通过语义离散化模块将数值特征转化为定性描述，解决模态不一致；二是引入CatBoost作为统计专家注入先验知识，弥补LLM分类能力不足；三是采用对比少样本学习应对数据稀缺，并通过结构化提示嵌入航空领域知识。相比现有工作，FlightLLM不仅实现竞争性分类性能，更能直接生成面向飞行员操作行为的因果解释，无需专家二次翻译，填补了从预测结果到可操作安全建议的鸿沟。

### Q3: 论文如何解决这个问题？

FlightLLM通过一个五模块协同框架解决飞行安全事件解释难题，核心思路是将统计学习与语言推理深度融合。整体架构包含数据预处理与特征工程、语义离散化、统计专家提示、动态上下文检索和提示构造与LLM调用五个部分。

在特征工程模块，采用双分支提取策略：一方面用TSFresh自动提取统计特征，另一方面基于航空领域知识手工设计物理可解释特征（如下降率、俯仰角变化等），两者拼接形成混合特征向量，兼顾统计鲁棒性与物理语义。针对数值与语言模态不一致问题，语义离散化模块基于分位数将连续值映射为"极低/略低/正常/略高/极高"五个语义等级，并构造包含物理含义、语义标签和原始数值的三元描述符，使LLM在接触数字前先激活先验知识，规避token碎片化导致的数值理解缺陷。

由于LLM分类能力有限，系统引入CatBoost作为统计专家，将其预测标签和概率注入提示词作为先验引导，形成弱到强的协作机制：当两者判断一致时增强解释可信度，不一致时促使LLM重新审视证据。动态上下文检索模块从历史样本中筛选相似案例作为参考。最后通过结构化提示词嵌入航空领域知识，引导LLM生成针对事件原因的合理说明。创新点在于语义离散化桥接数值与语言鸿沟、统计专家提示增强推理稳定性，以及对比少样本学习缓解数据稀缺问题。

### Q4: 论文做了哪些实验？

论文围绕FlightLLM框架，以硬着陆为锚定事件，在704个真实A320航班样本（282次硬着陆、422次正常着陆，比例约2:3）上开展实验。数据来自QAR记录，涵盖32个飞行参数，统一重采样至4Hz，并截取触地前30秒至触地时刻的动态区间以避免数据泄漏。

实验设置包括三个LLM（GPT-3.5、DeepSeek-V1、GLM-4.7-flash）作为语言推理核心，对比基线为LSTM和SVM（SVM采用RFE特征选择）。评估指标为准确率、精确率、召回率和F1分数。

主要结果：FlightLLM在分类性能上与基线相当或更优，同时能生成直接、合理的因果解释。具体而言，CatBoost作为统计专家注入的预测先验显著提升了LLM的分类稳定性，语义离散化模块将数值模式转化为定性描述，增强了可解释性。对比实验表明，纯LLM分类能力有限，而FlightLLM通过先验引导和对比少样本学习，在保持高准确率的同时，提供了比传统特征重要性方法更易理解的飞行员操作层面的归因分析。实验还验证了该方法对尾撬、跑道偏出等类似复杂事件的泛化潜力。

### Q5: 有什么可以进一步探索的点？

基于FlightLLM的研究，未来可从以下方向深入探索：首先，当前方法依赖CatBoost作为统计专家提供先验，可尝试引入多专家集成或自适应先验选择机制，提升对多样化事件的泛化能力。其次，语义离散化模块依赖人工设计的定性描述规则，未来可探索利用LLM自动生成更细粒度、上下文感知的语义表征，减少人工干预。第三，实验仅聚焦重着陆事件，可扩展至尾撬、跑道偏离等事件，验证框架的通用性，并引入跨事件迁移学习。第四，当前对比少样本策略仅利用正常样本，可结合合成数据生成或数据增强技术缓解类别不平衡。最后，解释生成缺乏量化评估指标，可设计面向飞行员认知的评估协议，或利用人类反馈强化学习优化解释的实用性与可操作性，推动实际部署。

### Q6: 总结一下论文的主要内容

该论文提出FlightLLM框架，旨在利用大语言模型（LLM）实现飞行安全事件的分类与可解释性分析。研究以硬着陆事件为锚点，基于704个真实A320航班QAR数据，解决四个关键挑战：跨模态不一致、分类能力有限、数据稀缺和领域知识不足。方法上，首先通过特征工程融合TSFresh统计特征与航空物理指标，再经语义离散化模块将数值转化为定性描述；引入CatBoost作为统计专家提供先验指导，并采用对比少样本学习策略增强分类性能；最后通过结构化提示注入航空领域知识。实验表明，FlightLLM在分类性能上具有竞争力，同时能生成直接合理的事件原因文本解释，弥合了数据驱动分类与可理解解释之间的鸿沟，为飞行安全分析和飞行员培训提供可靠参考。
