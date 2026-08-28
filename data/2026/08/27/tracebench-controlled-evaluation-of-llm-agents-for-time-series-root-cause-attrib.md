---
title: "TraceBench: Controlled Evaluation of LLM Agents for Time-Series Root-Cause Attribution"
authors:
  - "Tommaso Bendinelli"
  - "Artur Dox"
  - "Christian Holz"
date: "2026-08-27"
arxiv_id: "2608.27182"
arxiv_url: "https://arxiv.org/abs/2608.27182"
pdf_url: "https://arxiv.org/pdf/2608.27182v1"
categories:
  - "cs.LG"
tags:
  - "LLM Agent"
  - "Time-Series Root-Cause Attribution"
  - "Controlled Evaluation"
  - "Anomaly Detection"
  - "Dynamical Systems"
  - "Simulation-Based Benchmark"
  - "Agent Trajectories"
  - "Domain Context"
  - "Numerical vs Visual Exploration"
  - "Prediction Format Impact"
relevance_score: 9.5
---

# TraceBench: Controlled Evaluation of LLM Agents for Time-Series Root-Cause Attribution

## 原始摘要

LLM agents are increasingly applied to anomaly detection and root-cause analysis in time-series observations collected from real-world systems; however, their performance on these tasks has not been systematically evaluated under controlled conditions. We introduce TraceBench, a simulation-based framework for generating controlled root-cause attribution tasks. In each generated task, an agent receives time-series observations produced by simulating a physical dynamical system and must determine whether a system parameter was altered during the simulation and, if so, which one. Using TraceBench, we generate tasks from three interpretable mechanical systems and systematically evaluate four LLM agents across controlled experimental conditions, yielding new insights into how these agents analyze time-series observations from dynamical systems. Our results show that agents benefit substantially from domain context and explore data primarily through numerical console output rather than visualizations. We also find that agents generally perform worse when required to produce a Python script that maps each time-series sample to a predicted root-cause label than when they submit predictions directly. We release our datasets, agent trajectories, experimental results, and a leaderboard on our website, tracebench.github.io.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文旨在解决LLM智能体在多变量时间序列根因归因任务中缺乏系统性、受控评估的问题。研究背景是，LLM智能体已被广泛应用于真实系统的异常检测与根因分析，但现有基准（如软件遥测、云故障注入）虽能评估端到端诊断能力，却无法隔离智能体结合时序物理推理与领域知识的能力。同时，现有语言-时间序列数据集多聚焦于模式描述或问答，未提供生成观测数据的机制性系统描述，难以测试智能体通过多步工具辅助分析形成并修正诊断假设的过程。

为此，本文提出TraceBench，一个基于物理仿真的可控框架，通过模拟机械系统生成根因归因任务，要求智能体判断系统参数是否被修改及具体哪个参数。该框架沿四个可控轴（领域上下文、观测噪声、标注样本、提交模式）设计，以系统隔离智能体在时间序列推理与领域知识整合上的表现。核心问题是：在受控条件下，LLM智能体能否有效利用系统描述进行假设推理，以及不同提交方式（直接答案 vs. 程序化脚本）如何影响其诊断性能。

### Q2: 有哪些相关研究？

相关研究主要分为两条主线。**第一类是智能体系统与基准**，如TimeSeriesGym评估智能体在时间序列上的机器学习工程任务，TS-Reasoner研究程序辅助的分解式推理，TSAIA构建科学工程分析工作流，TemporalBench评估历史理解与事件预测。在工业诊断方向，OpenRCA聚焦软件遥测的根因定位，AIOpsLab在故障注入的云环境中评估智能体，AssetOpsBench扩展至工业监控维护。这些工作与本文共享多步、上下文感知的诊断理念，但区别在于：它们覆盖更广泛的分析任务或异构数据，而TraceBench通过受控物理仿真隔离了根因归因任务，每个样本明确对应“无干预”或“单一参数变化”，从而能独立控制领域上下文、观测噪声、标注样本和提交模式四个维度。

**第二类是单轮、无工具使用的时间序列理解基准**，包括评估病因推理与事实问答的工作、TimeSeriesExam（模式识别与因果推理）、TIME-RA（异常诊断）、SciTS（科学时间序列理解）、Time-MQA与TRQA（多任务问答）、ITFormer与ChatTS（多模态理解）、Time-MMD（数值与文本对齐）、TimeText语料库及BEDTime（时间序列描述）。这些基准的文本通常与观测样本绑定（如问题、时间戳标注或模式描述），而TraceBench提供的是与样本无关的机制性系统描述——测量什么、哪些参数可变、物理动力学如何——要求智能体利用该先验描述提出假设并针对轨迹验证，这是其核心区别。

### Q3: 论文如何解决这个问题？

TraceBench通过一个基于物理仿真的可控任务生成框架，系统性地评估LLM智能体在时间序列根因归因上的表现。其核心设计围绕四个独立可调的任务轴展开：领域上下文（是否提供系统描述与通道含义）、观测噪声（通过标量κ控制干扰强度）、标注样本（是否提供带标签的支持批次）、以及提交模式（直接答案或编写可复用Python脚本）。

框架的任务生成流程如下：首先，从物理模拟器（如弹跳球、滑块系统）中生成无噪声轨迹，通过在随机干预时间点对某个系统参数施加瞬时阶跃变化来构造干预样本，同时生成无干预样本作为对照。为排除模糊样本，框架采用双重过滤机制：一是通过无干预探针和静态变化探针计算效应-噪声比（阈值ρ=2），剔除干预效果不可检测或与静态参数变化不可区分的样本；二是针对每个模拟器手工设定特定拒绝规则，排除因物理耦合（如重力与质量的乘积效应）导致的观测混淆。最终，每个样本被标注为无干预或特定参数干预类别。

在评估环节，智能体接收包含任务指令、测试批次（及可选支持批次）的提示，在直接模式下逐样本输出预测，或在程序化模式下提交一个可独立运行的脚本。这一设计不仅衡量智能体的即时推理能力，还通过脚本在未见数据上的表现检测其泛化能力。创新点在于将根因归因任务从真实系统迁移到可控仿真环境，使得干预类型、噪声水平、上下文信息等变量可独立调节，从而揭示智能体在不同条件下的行为差异——例如对数值输出的偏好、对领域上下文的依赖程度，以及程序化提交带来的性能下降。

### Q4: 论文做了哪些实验？

论文基于TraceBench框架，从三个可解释物理系统（BallDrop、BounceBall、MassSlide）生成根因归因任务，系统评估了四个LLM智能体（gpt-5.5、gemini-3.1-pro、claude-opus-4.6、minimax-m2.7）在受控条件下的表现。实验设置包括两种噪声水平（低噪声和高噪声）和两种提交模式（直接答案和程序化提交），每个条件包含3个标注支持样本和详细系统描述，每个任务含10个测试样本，使用5个重复种子，每个智能体共60个评估片段。

主要结果：gpt-5.5在所有条件下准确率最高（低噪声直接模式达0.933），claude-opus-4.6次之，minimax-m2.7表现最差（平均低46个百分点）。噪声增加导致所有智能体准确率下降（gpt-5.5降11个百分点），程序化提交模式普遍比直接模式表现更差。消融实验显示，移除领域上下文导致准确率大幅下降（gpt-5.5降32个百分点），而移除标注样本影响较小。探索行为分析表明，智能体主要依赖数值控制台输出（占输入上下文77-80%），很少检查可视化图表，gpt-5.5使用更少的Python调用但更精准。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下几个方向展开：首先，当前仅覆盖三个机械系统，物理动力学空间有限，未来可引入更复杂的高维、非线性或混沌系统，以及真实工业场景中的多变量耦合故障，以检验方法的泛化性。其次，程序化提交模式下held-out准确率显著低于episode准确率，说明模型生成的映射函数缺乏稳定的物理因果捕获能力，可探索将物理先验（如守恒量、微分方程结构）注入程序生成过程，或引入可微编程与符号回归来提升可解释性和泛化性。再者，实验发现agent几乎不依赖可视化而偏好数值控制台输出，这提示可设计更高效的交互接口，如结构化摘要、关键统计量自动提取或主动查询机制，减少无效探索。此外，当前评估聚焦于单参数干预，可扩展至多参数同时扰动、时变参数漂移等更贴近实际运维的复杂场景。最后，资源效率与准确性未呈单调关系，可研究自适应推理策略，让agent根据任务难度动态分配计算预算，并探索跨任务元学习以提升样本效率。

### Q6: 总结一下论文的主要内容

TraceBench提出了一个基于仿真的可控框架，用于系统评估LLM智能体在时间序列根因归因任务上的表现。该框架通过物理动力学系统生成多变量时间序列，要求智能体判断系统参数是否被修改及具体哪个参数被修改。作者在三个可解释机械系统上，对四个LLM智能体在噪声水平、领域上下文、标记示例和提交模式四个可控维度下进行了系统评估。主要发现包括：智能体显著受益于领域上下文，主要依赖数值控制台输出而非可视化进行数据探索，且当要求生成Python脚本进行逐样本预测时，性能普遍低于直接提交预测结果。该工作为评估LLM智能体在时间序列物理推理与工具辅助分析方面的能力提供了标准化基准，并揭示了不同智能体在探索策略和资源利用上的显著差异。
