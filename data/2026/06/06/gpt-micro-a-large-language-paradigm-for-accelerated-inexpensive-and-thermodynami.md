---
title: "GPT-Micro: A large language paradigm for accelerated, inexpensive, and thermodynamics-consistent discovery of constitutive models in manufacturing"
authors:
  - "Soumik Dutta"
  - "Kiarash Naghavi Khanghah"
  - "Sania Shree"
  - "Logan McNeil"
  - "Thomas Feldhausen"
  - "Hongyi Xu"
  - "Rajiv Malhotra"
date: "2026-06-06"
arxiv_id: "2606.08238"
arxiv_url: "https://arxiv.org/abs/2606.08238"
pdf_url: "https://arxiv.org/pdf/2606.08238v1"
categories:
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "LLM/Agent Workflow"
  - "可解释时间序列分析"
  - "工业故障诊断"
  - "时序报告生成"
  - "RAG"
  - "Symbolic Regression"
  - "物理一致性"
relevance_score: 8.5
---

# GPT-Micro: A large language paradigm for accelerated, inexpensive, and thermodynamics-consistent discovery of constitutive models in manufacturing

## 原始摘要

Constitutive modeling of the relationship between process-imposed material states and fundamental material properties is critical to control of material microstructure in manufacturing processes. The limited accuracy resulting from the typical reliance on fallible human expertise and intuition for postulation and revision of the models functional form results in incremental and time consuming model discovery. Conventional Machine Learning (ML) incurs significant cost and time of data generation. Model discovery using Large Language Models (LLMs) suffers from the above issues and/or ignores the inviolability of fundamental thermodynamics laws. This work creates a novel GPT-Micro paradigm for autonomous, data sparse, and thermodynamics-compliant discovery of de-novo constitutive models. This framework seamlessly integrates semantic knowledge extraction from literature, enforcement of thermodynamics-based conservation laws, and sparse datasets, with LLM-driven generation and refinement of model hypotheses. Validation is performed for a long-intractable constitutive modeling problem in a printed electronics process testbed. This reveals significant and simultaneous advantages over the state-of-the-art including: (a) More than 70 percent reduction in data burden relative to ML-based modeling without loss in accuracy; (b) 400X reduction in discovery time after data generation, from months to hours, relative to human-driven modeling; (c) Discovery of models with novel functional forms without subjective human choice of a starting hypothesis; (d) Enhanced physics-rooted trustworthiness, human interpretability, and mechanistic insight via synthesis of compact, conservation-compliant, and physically complete analytical models. The potential of GPT-Micro to realize rapid, low-cost, physically trustworthy, and interpretable microstructure modeling across the manufacturing landscape is discussed.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文旨在解决制造业中本构模型（constitutive model）发现的核心难题：传统方法在模型可扩展性与数据负担之间存在严重权衡。具体而言，传统的人类驱动建模依赖专家直觉来提出模型函数形式，导致发现过程缓慢（数月甚至数年）且精度有限；而纯数据驱动的机器学习方法虽然无需人工假设函数形式，但需要大量高保真数据（实验或模拟），成本高昂。此外，现有基于大语言模型（LLM）的模型发现方法要么忽略了热力学守恒定律的约束，要么无法自主发现全新的函数形式，仅能进行系数校准。论文提出的GPT-Micro范式旨在实现自主、数据稀疏且热力学一致的本构模型发现，通过整合文献语义知识提取、热力学守恒定律约束、稀疏高保真数据集以及LLM驱动的假设生成与迭代优化，同时降低数据需求、加速发现过程并保证物理可解释性。

### Q2: 有哪些相关研究？

相关研究可分为三类：第一类是传统人类驱动建模，依赖专家经验提出模型形式，如增量板料成形中的断裂模型开发耗时十余年，但精度有限且速度慢。第二类是数据驱动机器学习，如神经网络直接关联材料状态与微观结构，但需要大量高保真数据；物理信息神经网络（PINNs）和DeepONets虽引入物理约束，但仍需人类预设模型形式。第三类是LLM驱动的模型发现，包括预训练LLM识别本构关系（无法引入守恒定律）、LLM迭代优化系数（仍需人类定义函数形式）、RAG知识检索结合参数-微观结构建模（无法考虑守恒定律且缺乏假设优化）。GPT-Micro的独特之处在于首次无缝集成了LLM文献知识提取、热力学守恒定律强制约束、稀疏数据反馈和LLM驱动的假设生成与优化，克服了上述方法的局限性。

### Q3: 论文如何解决这个问题？

GPT-Micro采用四阶段自主工作流：第一阶段，用户提供工艺、材料、微观结构等关键词，通过API自动下载相关文献语料，利用RAG（检索增强生成）提取材料状态与微观结构属性之间的定性关系（如正相关、负相关、指数趋势等）。第二阶段，LLM基于提取的定性信息生成50个初始状态-微观结构模型假设（解析方程形式），在少量高保真训练数据上校准系数并评估验证误差；若验证R²未达阈值（如0.98），LLM根据前一轮假设及其误差反馈生成20个优化假设，迭代直至满足精度。第三阶段，将最终状态-微观结构模型与已知的热力学守恒定律（如Allen-Cahn方程）结合，生成大量合成数据（无需额外高保真数据），计算材料属性（如有效扩散系数）与材料状态的关系。第四阶段，利用符号回归（PySR）从合成数据中发现本构模型的解析表达式及其系数。该方法的关键创新在于：通过LLM从部分相关的文献中拼接信息，减少高保真数据需求；通过热力学守恒定律确保物理一致性；通过迭代假设优化填补文献信息空白，实现自主发现全新函数形式。

### Q4: 论文做了哪些实验？

论文以金属纳米线烧结印刷电子工艺为测试平台，验证GPT-Micro的有效性。实验设置：材料状态包括纳米线半径（7.5-12.5 nm）、烧结温度（400-800 K）和初始取向角（0°-60°），微观结构属性为收缩率δ̇和旋转角速度θ̇。高保真数据来自分子动力学（MD）模拟，共125个样本，其中27训练、27验证、71测试。GPT-Micro仅用54个训练+验证样本即完成模型发现。对比实验：与四种传统ML方法（前馈神经网络、支持向量回归、高斯过程回归、随机森林）比较，在相同数据量下GPT-Micro的测试精度显著更高；将ML的数据量增至128和250个样本后，GPT-Micro仍实现70%以上的数据负担降低。发现时间对比：GPT-Micro在数据生成后数小时内完成模型发现，而人类驱动建模耗时约12年（从2009年工艺首次报道到2021年模型完成）。模型分析：GPT-Micro发现的模型形式紧凑且可解释，例如有效扩散系数Deff的表达式包含√θ0和指数项，而人类模型需更复杂形式。此外，通过跟踪假设优化过程发现，对于文献信息充分的δ̇模型无需优化，而对于文献缺失的θ̇模型需3轮优化，验证了GPT-Micro填补信息空白的能力。

### Q5: 有什么可以进一步探索的点？

未来方向包括：第一，将GPT-Micro扩展到更复杂的制造工艺（如增材制造中的多尺度微观结构演化），验证其泛化能力。第二，改进LLM假设生成的质量，例如通过引入领域特定预训练或更精细的提示工程，减少对迭代优化的依赖。第三，探索更高效的符号回归方法，以处理高维材料状态空间。第四，将GPT-Micro与主动学习结合，在模型发现过程中自适应选择最具信息量的高保真实验，进一步降低数据需求。第五，研究模型不确定性量化，为工业决策提供置信度评估。第六，开发多Agent协作框架，让不同LLM分别负责文献分析、假设生成和物理约束验证，提升系统鲁棒性。第七，将本框架迁移至工业故障诊断领域，例如从传感器时序数据中自主发现故障演化模型。

### Q6: 总结一下论文的主要内容

GPT-Micro是一种自主、数据高效且热力学一致的本构模型发现范式，针对制造业中材料微观结构建模的瓶颈问题。该方法创新性地整合了LLM驱动的文献知识提取、RAG检索、热力学守恒定律约束、稀疏数据反馈和迭代假设优化，实现了从部分相关文献中拼接信息并自主发现全新解析本构模型。在纳米线烧结工艺测试中，GPT-Micro相比传统ML减少70%以上高保真数据需求，相比人类驱动建模加速400倍（从数月降至数小时），且发现的模型具有紧凑、可解释和物理一致的特点。该工作为加速新材料和新工艺的工业应用提供了有力工具，并展示了LLM在科学发现中的巨大潜力。
