---
title: "Agentic Root Cause Analysis through Evidence-Grounded Reasoning"
authors:
  - "Amaury Wei"
  - "Olga Fink"
date: "2026-07-24"
arxiv_id: "2607.22385"
arxiv_url: "https://arxiv.org/abs/2607.22385"
pdf_url: "https://arxiv.org/pdf/2607.22385v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "可解释故障诊断"
  - "根因分析"
  - "证据路由"
  - "数字孪生"
  - "工具增强LLM"
  - "零样本推理"
  - "工业传感器"
  - "推理时反思"
  - "假设驱动推理"
relevance_score: 9.5
---

# Agentic Root Cause Analysis through Evidence-Grounded Reasoning

## 原始摘要

Diagnosing the root cause of anomalies is essential for safe industrial operation. Despite extensive sensor instrumentation, formulating hypotheses and gathering evidence remains a manual process, creating a major operational bottleneck. While existing data-driven approaches aim to automate this, two critical limitations restrict their deployment: their operate as black boxes unable to justify their diagnosis, and they require scarce labeled examples of faulty operation. To address this gap, we introduce AgentRCA, a zero-shot agentic framework for evidence-grounded root cause analysis. Rather than learning fault-specific mappings, AgentRCA performs inference-time reasoning by combining a data-driven digital twin (modeling normal system dynamics) with a tool-augmented large language model. The agent iteratively gathers statistical evidence, evaluates competing hypotheses, and identifies the physical fault that best explains the observed behavior. Evaluated on a real-world multiphase-flow facility and a large-scale chemical plant, AgentRCA achieves diagnostic performance competitive with fully supervised baselines without relying on fault-specific training. Crucially, it produces transparent reasoning traces that explicitly link observed symptoms to their underlying physical causes. These results establish autonomous hypothesis-driven reasoning as a practical foundation for scalable industrial root cause analysis.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业系统的安全运行依赖于对异常根因的准确诊断。尽管现代工业设施配备了密集的传感器网络，但传统的根因分析（RCA）仍高度依赖工程师手动提出假设、收集证据并验证，这构成了严重的运维瓶颈。现有数据驱动方法试图自动化这一过程，但存在两个关键局限：一是它们作为“黑箱”模型，无法提供可解释的诊断依据；二是它们严重依赖标注的故障数据，而工业环境中此类数据极其稀缺且获取成本高昂。此外，无监督方法虽能检测异常，却仅止于统计归因，无法对物理故障机制进行因果推理。为解决这一矛盾，本文提出AgentRCA，一个零样本的智能体框架。其核心创新在于，不学习故障特定的映射，而是将RCA转化为一个基于证据的推理工作流。通过结合仅用正常数据训练的数据驱动数字孪生与工具增强的大语言模型，智能体在推理时迭代地收集统计证据、评估竞争性假设，并最终识别出最能解释观测行为的物理故障。该方法旨在实现无需故障样本、具备透明推理链的自动化根因诊断，弥合因果逻辑与动态过程数据之间的鸿沟。

### Q2: 有哪些相关研究？

相关研究可分为三类：**模型/知识驱动方法**、**数据驱动方法**和**LLM/Agent方法**。模型/知识驱动方法（如基于物理模型、故障树、贝叶斯网络）虽支持可解释推理，但依赖精确物理模型和静态因果架构，难以适应动态工业过程。数据驱动方法（如监督式深度学习）将RCA视为分类问题，需要大量标注故障样本，且黑箱特性缺乏可解释性；无监督方法（如异常检测、因果归因）仅定位异常变量，无法进行物理故障推理。LLM/Agent方法（如用于软件系统故障诊断的Agent框架）主要处理离散日志，不适用于连续传感器数据。AgentRCA的关键区别在于：它结合了数据驱动数字孪生（仅需正常数据训练）与工具增强LLM，通过推理时迭代收集统计证据、评估假设，实现零样本、证据驱动的RCA，既避免了监督学习对故障样本的依赖，又克服了无监督方法仅做统计归因的局限，同时生成透明推理链。

### Q3: 论文如何解决这个问题？

AgentRCA将根因分析构建为一个基于证据的交互式推理任务，而非静态分类问题。其核心方法是将数据驱动的数字孪生与工具增强的大语言模型（LLM）智能体相结合，在推理时进行假设驱动诊断。

**整体框架**包含三个主要阶段：输入处理、模块化工具诊断和迭代推理循环。首先，多变量测试窗口被映射到最近邻的正常运行工况（基于设定点通过标准化欧氏距离匹配），以获取工况特定的统计基线。

**主要模块/组件**包括：
1. **数字孪生**：由工况划分（Ω）和预计算的统计基线（均值向量、标准差向量、皮尔逊相关矩阵）以及一个仅在正常数据上训练的卷积自编码器组成，用于学习正常系统动力学。
2. **模块化诊断工具**：智能体可查询四种工具获取定量证据：自编码器残差工具（报告偏离正常流形的重建误差，仅返回前10个最异常信号）、统计偏移工具（计算均值和方差的定向偏移分数）、相关性工具（计算当前窗口与基线相关矩阵的差异）以及时间偏差工具。
3. **LLM推理智能体**：实例化为Qwen3-30B-A3B模型，接收测试窗口和自然语言故障描述。它通过迭代查询工具、分析返回的数值证据，动态更新并排序候选假设表，最终输出一个将观测症状与物理原因明确关联的、基于证据的诊断轨迹。

**创新点**在于：无需故障特定训练样本（零样本），通过推理时结合数字孪生的定量证据与LLM的物理上下文理解，实现了与全监督方法相当的诊断性能，同时生成完全透明的推理链，解决了黑箱问题。

### Q4: 论文做了哪些实验？

论文在PRONTO和TEP两个工业基准上评估了AgentRCA。PRONTO是一个17维信号、含4种故障的真实多相流设施；TEP是52变量、21种故障的大型化工过程。实验采用零样本设置：仅用正常数据训练数字孪生，故障窗口全部用于评估。对比方法包括LightGBM、Autoencoder分类器和MiniRocket+Ridge分类等监督基线。主要结果：在PRONTO上，AgentRCA零样本Top-1准确率达87.6%，Top-2达96.8%，接近监督基线（LightGBM 99.0%，Autoencoder 99.6%，MiniRocket 94.5%）。监督基线在少量标注数据下性能急剧下降（每类仅3个窗口时最佳仅65.1%），而AgentRCA无需故障样本。消融实验显示，假设表推理结构优于无结构和ReAct结构；操作条件匹配和方向性统计证据最关键，移除后Top-1分别降至40.6%和43.8%。模型鲁棒性实验表明，GPT-5-mini和Qwen3-30B在结构化推理下表现稳定，而小模型Gemma4-E4B在假设表格式下性能下降。温度敏感性实验显示结构化推理在0.0-1.0温度范围内保持稳定。

### Q5: 有什么可以进一步探索的点？

AgentRCA的局限性为未来研究提供了明确方向。首先，其假设推理时的正常工况已包含在训练数据中，但工业系统常出现未见过的工况或缓慢漂移，因此需要探索在线更新数字孪生或引入自适应机制。其次，诊断工具的错误（如传感器故障）会直接传播，未来可引入不确定性量化或冗余验证机制，例如多工具交叉验证或置信度评分。第三，当前框架仅诊断而不推荐纠正措施，可扩展为闭环系统，结合强化学习或因果模型自动生成控制策略。此外，开放集诊断是一个关键方向，通过异常检测或分布外识别，让代理主动标记未知故障而非强行归入已知类别。针对复杂工厂，可设计分层多智能体架构，让子智能体分别推理子系统，再由全局智能体整合。最后，主动假设测试值得探索，即利用系统模拟器生成故障签名并与实际观测对比，从而提升诊断的鲁棒性和可解释性。这些改进将推动AgentRCA从诊断助手向自主运维决策系统演进。

### Q6: 总结一下论文的主要内容

该论文提出了一种名为AgentRCA的零样本智能体框架，用于解决工业异常的根本原因分析问题。传统方法依赖黑箱模型和稀缺的故障标注数据，难以部署。AgentRCA通过结合数据驱动的数字孪生（建模正常系统动态）与工具增强的大语言模型，在推理时进行证据驱动的因果推理。智能体迭代收集统计证据、评估竞争假设，最终识别最能解释观测行为的物理故障。在真实多相流设施和大型化工厂的评估中，AgentRCA无需故障特定训练，即可达到与全监督基线相当的诊断性能。其核心贡献在于实现了透明的推理轨迹，将观测症状与物理原因显式关联，为可扩展的工业根因分析提供了自主假设驱动推理的实用基础。
