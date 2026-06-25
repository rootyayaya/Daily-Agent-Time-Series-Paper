---
title: "Explainable Control Framework (XCF) based on Fuzzy Model-Agnostic Explanation and LLM Agent-Supported Interface"
authors:
  - "Faliang Yin"
  - "Hak-Keung Lam"
  - "David Watson"
date: "2026-06-24"
arxiv_id: "2606.25941"
arxiv_url: "https://arxiv.org/abs/2606.25941"
pdf_url: "https://arxiv.org/pdf/2606.25941v1"
categories:
  - "cs.HC"
  - "cs.AI"
  - "eess.SY"
tags:
  - "可解释控制"
  - "LLM Agent"
  - "自然语言报告生成"
  - "模糊模型无关解释"
  - "用户交互界面"
  - "控制决策解释"
  - "闭环系统"
  - "倒立摆"
  - "Turtlebot避障"
relevance_score: 8.5
---

# Explainable Control Framework (XCF) based on Fuzzy Model-Agnostic Explanation and LLM Agent-Supported Interface

## 原始摘要

Increasing demand for precise and reliable control in complex scenarios has led to the development of increasingly sophisticated controllers, including data-driven approaches employing closed box models and mathematically rigorous yet complex designs. This complexity highlights the needs for explainable control that can provide human-understandable insights into controller behavior. In this paper, an explainable control framework (XCF) along with supporting algorithms and user interface are proposed to explain how controllers determine their control actions and their underlying working mechanism. The novel contributions of this work are threefold: First, the XCF is designed to provide model-agnostic explanations for controllers in closed-loop systems and can optionally refine local explanations by system response dynamics. Second, a novel explanation method, hierarchical fuzzy model-agnostic explanation for control systems (HFMAE-C), is proposed based on the designed framework. The HFMAE-C employs a fuzzy logic system to approximate the controller's behavior and system dynamics, providing sample, local, domain and universe level explanations via IF-THEN rules revealing the controller's decision logic and salience values quantifying the contribution of system states to control actions. Third, a large language model agent-supported user interface is developed to automatically analyze user requirements, select appropriate algorithms, interpret the generated explanations to a natural language report, and provide interactive consultation. Case studies on inverted pendulum system and Turtlebot obstacle avoidance demonstrate the effectiveness of the proposed method through simulated user experiments and quantitative comparisons with mainstream explainable control approaches.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着工业系统日益复杂，数据驱动的“黑箱”控制器（如深度强化学习模型）虽性能强大，但其决策过程不透明，难以被人类理解和信任。现有可解释控制方法存在两大不足：一是多为模型特定（model-specific），难以泛化到不同控制器；二是解释粒度单一，无法满足从全局逻辑到局部实例的多层次理解需求。此外，缺乏智能交互界面，用户难以将技术性解释转化为可操作的洞察。本文旨在解决上述问题，提出一个模型无关的可解释控制框架（XCF）。核心目标是：1）设计一个通用的、可提供分层解释（样本级、局部级、域级、全局级）的框架，以揭示任意控制器的决策逻辑和状态贡献度；2）提出基于模糊逻辑系统的层次化解释方法（HFMAE-C），通过IF-THEN规则和显著性值提供语义化解释；3）开发基于大语言模型（LLM）Agent的交互界面，自动解析用户需求、生成自然语言报告，实现人机交互式咨询，从而将黑箱控制器转化为可理解、可信任的系统。

### Q2: 有哪些相关研究？

本文的相关研究主要分为三类：**可解释人工智能（XAI）方法**、**可解释控制框架**以及**LLM Agent 在工程中的应用**。

在XAI方法方面，本文与LIME、SHAP等模型无关解释方法密切相关。这些方法通过局部近似解释黑箱模型，但主要针对静态分类/回归任务。本文提出的HFMAE-C方法继承其模型无关性，但创新性地引入模糊逻辑系统，专为闭环控制系统设计，能够提供从样本到宇宙的多层级解释，并利用系统响应动态优化局部解释，弥补了现有方法忽略控制时序依赖性的不足。

在可解释控制领域，相关工作包括基于符号回归的控制器解释（如遗传编程）和基于规则提取的方法（如决策树近似PID）。本文区别于这些方法：首先，HFMAE-C不依赖控制器结构假设（模型无关）；其次，它通过模糊IF-THEN规则同时揭示决策逻辑和状态贡献度（显著性值），而传统规则提取仅输出离散逻辑；最后，XCF框架支持通过系统动态反馈修正解释，这在静态解释方法中未见。

在LLM Agent应用方面，本文借鉴了近期将LLM作为交互接口的研究（如GPT-4用于代码生成或数据分析）。但本文的独特贡献在于：开发了一个专用Agent，能自动解析用户需求、选择解释算法，并将模糊规则和显著性值转化为自然语言报告，同时提供交互式咨询。这与仅生成代码或简单问答的通用LLM应用不同，实现了从技术解释到用户友好沟通的端到端自动化。

此外，本文在倒立摆和Turtlebot避障案例中与主流可解释控制方法（如LIME-C、决策树近似）进行了定量对比，验证了HFMAE-C在解释保真度和用户理解效率上的优势。

### Q3: 论文如何解决这个问题？

论文提出了一种基于模糊模型无关解释和LLM Agent支持界面的可解释控制框架（XCF），以解决复杂控制器行为难以理解的问题。核心方法包括三个创新点：首先，XCF设计为模型无关的解释框架，可对闭环系统中的控制器提供解释，并可选地通过系统响应动态优化局部解释。其次，提出层次化模糊模型无关解释方法（HFMAE-C），采用模糊逻辑系统（FLS）近似控制器行为和系统动态。FLS使用TSK模糊规则，每条规则包含IF部分（系统状态与模糊集的隶属度）和THEN部分（线性模型），通过全组合规则库和加权平均输出生成解释。HFMAE-C提供样本、局部、领域和全域四个层次的解释，通过IF-THEN规则揭示决策逻辑，并通过显著性值量化系统状态对控制动作的贡献。解释层次通过层次化学习实现：先训练全域解释器，再基于重要性分组构建领域解释器（采用权重聚合或规则聚合），最后针对局部实例进行细化训练，并可结合全局知识或系统响应动态优化。第三，开发了LLM Agent支持的用户界面，自动分析用户需求、选择合适算法、将解释结果转化为自然语言报告，并提供交互式咨询。该界面通过轻量级LLM（如Qwen3 4b）实现规划器功能，准确识别用户意图（全域、领域或局部解释），并生成结构化报告。实验在倒立摆和Turtlebot避障案例中验证了有效性，与SHAP、LIME等方法相比，XCF在保真度、单调性和R²分数上表现更优。

### Q4: 论文做了哪些实验？

论文在倒立摆系统和Turtlebot避障两个案例上进行了实验。实验设置上，倒立摆系统采集5000个样本，按4:1划分训练/测试集，模糊逻辑系统每个状态设3个模糊集，学习率0.2。Turtlebot避障案例中，XCF使用2000个样本，与SHAP、LIME、MAPLE进行对比，各方法计算成本相近。

主要结果包括：在倒立摆系统中，宇宙级解释器预测R²分数接近1.0，但RMSE较大（训练161.90，测试157.95）；域级解释器中，规则聚合的RMSE（1.61/1.68）低于权重聚合（12.52/12.80）；局部解释器经三步优化后，预测RMSE降至2.53/2.54，响应误差也最低（x1:0.0012, x2:0.0010）。在Turtlebot避障中，XCF通过特征显著性和IF-THEN规则揭示了控制器行为：避障阶段主要依赖角度变量（θ_obs和θ_target显著值约0.07），而距离变量影响很小；重定向阶段则转向目标导向。定量评估采用忠实度、单调性和R²分数三个指标，XCF在所有指标上均优于对比方法。

### Q5: 有什么可以进一步探索的点？

论文在可解释控制方面取得了显著进展，但仍存在若干可探索的方向。首先，XCF的模糊解释器依赖预定义的模糊集和规则数量，其泛化能力可能受限于复杂非线性控制器。未来可引入自适应模糊系统或神经符号方法，动态调整规则粒度以提升解释精度。其次，LLM Agent接口虽能生成自然语言报告，但其对模糊规则的理解可能产生语义偏差，尤其在多模态或时序依赖场景下。可探索结合因果推理与LLM的交互式追问机制，增强解释的鲁棒性。此外，当前评估指标（如忠实度、单调性）仅关注特征归因一致性，未衡量解释对控制策略改进的实际效用。建议设计任务导向的评估框架，例如通过解释引导控制器参数调优或故障诊断。最后，XCF在工业级高维系统（如多机器人协同）中的计算效率与实时性尚未验证，可考虑模型蒸馏或稀疏化技术降低推理开销。

### Q6: 总结一下论文的主要内容

该论文提出了一种面向控制系统的可解释框架（XCF），旨在解决复杂控制器（如黑箱模型）缺乏可解释性的问题。核心贡献包括：1）设计了一个模型无关的解释框架，可对闭环系统中的控制器行为提供分层解释，并可选地利用系统响应动态优化局部解释；2）提出了一种新颖的层次化模糊模型无关解释方法（HFMAE-C），通过模糊逻辑系统近似控制器行为，以IF-THEN规则和显著性值揭示决策逻辑，提供样本、局部、域和全局四个层次的解释；3）开发了基于大语言模型（LLM）的智能用户界面，可自动分析用户需求、选择算法并将解释结果转化为自然语言报告。在倒立摆和Turtlebot避障案例中，实验表明该方法在预测精度和响应动态上优于SHAP、LIME等主流方法，且轻量级LLM（如Qwen3-4b）能高效完成意图识别，验证了框架的实用性和可部署性。该工作为工业故障诊断等复杂场景提供了透明、可交互的控制系统分析工具。
