---
title: "FactoryLLM: A Safe and Open-Source AI Playground for Evaluating LLMs in Smart Factories"
authors:
  - "Yash Pulse"
  - "Yong-Bin Kang"
  - "Abhik Banerjee"
  - "Abdur Forkan"
  - "Prem Prakash Jayaraman"
date: "2026-06-12"
arxiv_id: "2606.14119"
arxiv_url: "https://arxiv.org/abs/2606.14119"
pdf_url: "https://arxiv.org/pdf/2606.14119v1"
categories:
  - "cs.AI"
tags:
  - "LLM/Agent"
  - "RAG"
  - "工业故障诊断"
  - "智能工厂"
  - "多文档推理"
  - "文档分析"
  - "开源平台"
  - "评估框架"
relevance_score: 8.5
---

# FactoryLLM: A Safe and Open-Source AI Playground for Evaluating LLMs in Smart Factories

## 原始摘要

Fault diagnostics and recovery in smart factories is challenging because critical information is dispersed across manuals of multiple machines which are interconnected through the manufacturing process. Large Language Models (LLMs) can provide a promising approach. In this paper, we propose FactoryLLM, a safe and open-source AI playground designed for evaluating different LLM-based retrieval-augmented generation (RAG) models by analysing documents from multiple machines across the manufacturing process. FactoryLLM enables the user to configure the LLM, and assess performance when reasoning over multiple documents, through a dual evaluation setup using both RAGAS and NVIDIA's LLM-as-a-Judge metrics. FactoryLLM is safe because it allows users to run local or open-source LLMs without sharing sensitive industrial data, providing a controlled environment for experimentation. We demonstrate the efficacy of FactoryLLM through a case study which involves an Autonomous Intelligent Vehicle and its Mobile Planner software, evaluating three LLMs across 30 maintenance queries derived from approximately 600 pages of cross-machine documentation. The results suggest that FactoryLLM is effective in cross-machine document reasoning: every model achieved a groundedness score above 0.88. The full code and documentation for community to test FactoryLLM with their manufacturing specific scenarios are publicly available.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在现代智能工厂中，设备高度互联，故障往往跨机器、跨系统传播，导致诊断极为困难。尽管每台机器都配有详尽的技术手册，但关键信息分散在不同机器、不同术语体系的文档中，操作员需要查阅数百页资料才能定位跨系统故障根源。现有方法存在明显不足：基于关键词的搜索无法处理语义差异；基于规则的专家系统需要大量人工知识工程且难以维护；知识图谱虽能结构化表示机器关系，但构建和更新成本高昂。同时，资深技术人员的退休加剧了专业知识断层。本文提出FactoryLLM，一个安全、开源的AI实验平台，旨在系统评估基于检索增强生成（RAG）的大语言模型（LLM）在跨机器文档推理中的表现。其核心目标是解决LLM在智能工厂中跨异构文档进行故障推理的评估难题，通过提供可控的本地/开源模型运行环境（保障数据安全）以及RAGAS和NVIDIA LLM-as-a-Judge双重评估指标，填补现有研究缺乏对跨机器文档推理能力系统评估的空白。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及三大类工作。第一类是**LLM在制造业中的应用**，如Li等人对LLM在生产规划、质量保证和维修中的综述，Raza等人对工业LLM应用的行业调研，以及Getz和Tong从航空维修日志中提取信息的研究。这些工作展示了LLM在单一制造任务中的潜力，但均未解决跨机器、跨文档的推理问题——这正是FactoryLLM的核心贡献。第二类是**面向工业文档的RAG系统**，包括Kernan Freire等人为洗涤剂工厂开发的RAG知识共享工具、Zhang等人在博世构建的图RAG增强维修聊天机器人，以及Liu等人提出的混合RAG技术。这些系统均针对单一机器或单一生产场景设计，缺乏跨机器检索与推理能力。第三类是**RAG系统的评估方法**，如RAGAS框架（使用忠实度、答案相关性等指标）、ARES（利用合成数据微调轻量级评判器）以及Roychowdhury等人在电信领域对RAGAS指标的评估。现有评估工具很少用于制造业维修场景，且多依赖临时问题集和人工检查。FactoryLLM填补了上述空白：它是一个开源的多文档RAG平台，支持跨机器文档推理，允许并排比较多种LLM和提示策略，并使用RAGAS进行标准化评估，为跨机器维修推理研究提供了可重复的基线。

### Q3: 论文如何解决这个问题？

FactoryLLM通过一个六层流水线架构解决跨机器文档推理的难题。其核心设计是**配置驱动、模块化**的，确保实验可复现与透明。

**整体框架**从底层到用户接口依次为：配置层、知识摄取层、交互层、检索层、推理层和存储层。

**主要模块与关键技术**：
1.  **配置层**：允许用户灵活选择LLM提供商（包括本地模型）、推理策略（IO、CoT、ToT、GoT）和RAG策略（向量或图检索），所有配置持久化存储，保证实验可复现。
2.  **知识摄取层**：将上传的多份技术文档（PDF等）切块，并根据配置构建会话隔离的向量索引（ChromaDB）或图索引（NebulaGraph），实现跨机器文档的联合索引。
3.  **检索层**：根据配置选择RAG策略，从统一索引中检索与查询最相关的`top-k`文档片段，支持跨系统信息检索。
4.  **推理层**：结合查询与检索到的上下文，执行选定的推理策略生成有据可依的回答。支持多路径探索与投票机制，若无相关上下文则返回回退响应，并记录所有推理步骤。
5.  **存储层**：使用关系数据库记录所有交互、推理状态和文档元数据，支持完整的审计追踪和RAGAS评估。

**核心创新点**在于：1) 提供了一个**安全、开源的沙盒环境**，允许在本地运行模型，避免敏感工业数据泄露；2) 采用**双评估机制**（RAGAS + LLM-as-a-Judge）系统评估RAG模型；3) 通过**会话级索引和配置驱动**的设计，实现了对跨机器文档的可控、可复现的联合推理。

### Q4: 论文做了哪些实验？

论文在FactoryLLM平台上进行了跨机器文档推理实验。实验设置固定：块大小1000 tokens、重叠200 tokens、每查询检索top-10块。数据集包含30个跨机器维护查询，来自自主智能车辆（AIV）和Mobile Planner软件约600页的技术文档，所有问题均需结合两个文档才能回答。对比了三种LLM：Qwen3-235B-A22B-Instruct-2507、Llama 4 Maverick和Gemma-3-27B。评估采用RAGAS（上下文精度、上下文召回、响应相关性、忠实度）和NVIDIA LLM-as-Judge（上下文相关性、响应基础性）双框架，所有指标在[0,1]尺度上计算。

主要结果：所有模型平均得分在0.73-0.76之间。检索侧指标较弱：上下文精度0.46-0.51，上下文召回0.76-0.89。生成侧指标较高：响应基础性0.88-0.95，忠实度0.62-0.72，响应相关性0.72-0.75。NVIDIA上下文相关性0.86-0.90。关键发现：跨机器RAG可行但受限于检索（基础性>0.88，精度平均0.48）；双框架提供互补信号（召回与忠实度相关系数r=0.61；基础性平均0.91 vs 忠实度0.66）。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：当前仅依赖自动评估指标（RAGAS和NVIDIA LLM-as-a-Judge），缺乏人类专家对诊断结果正确性和实用性的验证；实验规模较小（仅30个查询、3个模型），未涉及多模态文档（如图表、时序数据）和实时传感器数据；且未深入分析检索精度低但高接地性的矛盾原因。

未来可从以下方向探索：1）引入工业领域专家进行人工标注和评估，构建更可靠的基准；2）扩展至多模态RAG，融合设备日志、振动信号等时序数据与文本手册；3）设计自适应检索策略，结合知识图谱优化跨文档关联；4）开发主动学习机制，让LLM在诊断过程中主动向操作员提问以澄清歧义；5）探索轻量化模型部署方案，满足边缘计算的实时性要求。此外，可研究如何利用LLM生成可解释的故障推理链，提升诊断结果的可信度。

### Q6: 总结一下论文的主要内容

FactoryLLM针对智能工厂中故障诊断与恢复时多机器手册信息分散的挑战，提出一个安全、开源的AI评估平台。该平台通过检索增强生成（RAG）技术，使LLM能跨机器文档进行推理。核心贡献包括：支持用户配置不同LLM，并采用RAGAS和NVIDIA的LLM-as-a-Judge双重评估指标；通过仅运行本地或开源模型保障工业数据安全。案例研究基于自主智能车辆及其移动规划器软件，利用约600页跨机器文档构建30个维护查询，评估三个LLM。结果显示所有模型在文档推理中均取得高于0.88的groundedness分数，验证了平台有效性。该工作为工业场景下LLM的安全评估提供了标准化工具，促进了跨机器知识整合与故障诊断的自动化。
