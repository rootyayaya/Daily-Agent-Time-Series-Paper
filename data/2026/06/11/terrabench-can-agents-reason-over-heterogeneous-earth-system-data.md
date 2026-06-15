---
title: "TerraBench: Can Agents Reason Over Heterogeneous Earth-System Data?"
authors:
  - "Dat Tien Nguyen"
  - "Thao Nguyen"
  - "Fadillah Adamsyah Maani"
  - "Huy M. Le"
  - "Muhammad Umer Sheikh"
  - "Numan Saeed"
  - "Muhammad Haris Khan"
  - "Salman Khan"
date: "2026-06-11"
arxiv_id: "2606.13148"
arxiv_url: "https://arxiv.org/abs/2606.13148"
pdf_url: "https://arxiv.org/pdf/2606.13148v1"
categories:
  - "cs.AI"
tags:
  - "LLM/Agent for Time Series"
  - "Tool Use/Calling"
  - "Multi-Agent Reasoning"
  - "Planning"
  - "Benchmark"
  - "Earth Science"
  - "Heterogeneous Data"
  - "ReAct"
  - "Scientific Workflow"
relevance_score: 7.5
---

# TerraBench: Can Agents Reason Over Heterogeneous Earth-System Data?

## 原始摘要

Climate and environmental decision-making increasingly requires reasoning across heterogeneous inputs, including gridded physical data, satellite imagery, geospatial context, and simulator outputs. Weather and climate foundation models can forecast well, but do not reason interactively in language, while large language models (LLMs) reason in language but cannot operate directly on high-dimensional Earth-system data. As a result, real scientific workflows in Earth-science remain underserved. We introduce TerraBench, a benchmark for grounded Earth-science reasoning, built on TerraAgent, a ReAct-style executable framework that interleaves reasoning, tool calls, and observations to couple LLM planning with scientific tools for environmental retrieval, geospatial processing, simulation, and artifact-backed computation. TerraBench unifies analysis of Earth observation imagery, gridded data, GIS reasoning and simulation in a single executable interface, whereas prior benchmarks isolate these capabilities into narrow individual tasks. It is also the first in this space to pair process-level tool-use metrics with tolerance-aware numeric scoring. The benchmark comprises 403 extensive agentic tasks across three tracks (Fundamentals, Simulator-Grounded, and Document-Grounded Verification) and eight application domains with 24,500 verified execution steps. These results indicate that reliable Earth-science agents must go beyond tool access to coordinate heterogeneous workflows, parameterize tools precisely, and preserve artifact provenance.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决当前地球科学领域中，缺乏能够统一处理异构数据源并进行交互式推理的智能体评估基准的问题。研究背景是，气候与环境决策日益需要综合推理网格化物理数据、卫星图像、地理空间信息和模拟器输出等多种异构输入。现有方法存在明显不足：天气和气候基础模型虽能进行预测，但无法以语言形式进行交互式推理；而大语言模型（LLM）虽能进行语言推理，却无法直接操作高维地球系统数据。此外，现有基准如OpenEarthAgent和ThinkGeo等，通常将卫星图像、环境数据、GIS推理和模拟等能力隔离为独立的窄任务，缺乏统一、可审计的工作流评估，且主要衡量工具调用轨迹的对齐度，忽略了数值容错性。本文的核心问题是：如何构建一个统一的、可执行的基准，来评估智能体在真实地球科学工作流中，能否通过协调异构工具、精确参数化工具并保留中间产物，完成需要融合多种数据源和模拟器的复杂推理任务。为此，论文提出了TerraBench基准和TerraAgent框架。

### Q2: 有哪些相关研究？

相关研究主要分为两类。第一类是**多模态智能体基准**，如ReAct、HuggingGPT、Visual ChatGPT、MM-ReAct等，它们扩展了工具增强推理，相关基准如ToolBench、API-Bank、VisualWebArena、GAIA等聚焦于工具调用、长时执行和过程诊断。TerraBench与这些工作在评估哲学上一致，但不同之处在于其专门针对地球科学领域，整合了地球观测（EO）图像、网格化环境数据、GIS推理、模拟和文档验证，填补了气候特定工作流的空白。

第二类是**地球科学智能体基准**，包括Terra、ClimateIQA、WeatherQA、UnivEARTH、GeoHOP等数据集和系统，以及AutoClimDS、Zephyrus、ThinkGeo、GeoBenchX、Earth-Agent等工具驱动系统。这些工作通常专精于EO感知、天气推理或地理空间工具使用等单一任务。TerraBench的创新在于将上述多种能力统一到一个基准中，并首次引入过程级工具使用指标与容差数值评分相结合，而非仅依赖工具轨迹评估或LLM作为评判者的最终答案评估，这对处理地球科学中异构数值输出至关重要。

### Q3: 论文如何解决这个问题？

论文通过提出TerraBench基准和TerraAgent框架来解决地球系统数据异构推理问题。核心方法是将大语言模型（LLM）的语言推理能力与领域专用工具的科学执行能力解耦，构建一个可执行的、工具驱动的科学工作流框架。

**整体框架**：TerraAgent采用ReAct风格设计，核心流程为：用户问题→规划工作流→调用工具→记录中间观测→生成结构化答案与证据追踪。框架包含一个领域组织的工具注册表，涵盖环境数据检索、卫星图像处理、GIS分析、确定性模拟、可视化等77个子工具。

**主要模块**：
1. **工具层**：包括再分析数据检索（如ERA5）、预报模型（Pangu-Weather、Aurora）、模拟器（AquaCrop作物模型、DSSAT、CLIMADA灾害评估、EnergyPlus建筑能耗、SUMO交通模拟）等11类工具组。
2. **规划与执行层**：LLM负责工作流协调，但所有定量输出必须来自工具执行，而非模型生成。
3. **评估模块**：提出双指标评估体系——ToolUseScore（过程级指标，包括工具选择准确率、参数正确性、工作流顺序一致性等6个维度）和NumScore（容忍度感知的数值评分，采用指数衰减函数对接近正确但未完全匹配的答案给予部分分数）。

**创新点**：
1. 首次将地球观测图像、网格化数据、GIS推理和模拟统一到单一可执行接口，而非孤立任务。
2. 引入过程级工具使用指标与容忍度感知数值评分相结合的双重评估机制。
3. 构建包含403个复杂任务、24500个验证步骤的基准，覆盖因果推理层次（Level 0-3），强调观测基础能力（Level 0）对当前智能体的挑战。

### Q4: 论文做了哪些实验？

论文在TerraBench上进行了全面的实验评估。实验设置基于TerraAgent框架，包含403个agentic任务，横跨三个轨道（基础、模拟器验证、文档验证）和八个应用领域，共24,500个验证步骤。评估指标包括工具使用指标（ToolAcc、CategoryF1、ArgAcc、OrderScore、ToolUseScore）和答案正确性指标（NumScore、Hit@tol）。对比方法包括前沿模型（GPT-5.4/5.5、Gemini 3.1 Pro/2.5 Flash、Claude Haiku 4.5/Sonnet 4.6）、基线Agent（Qwen3.5-9B）和开源模型（Qwen3系列、Gemma 4、Mistral 7B、Llama 3.1 8B、InternVL3-8B等）。主要结果：最强模型Claude Sonnet 4.6仅达到ToolUseScore 59.22、NumScore 28.44、Hit@tol 22.88，表明任务极具挑战性。前沿模型在流程和结果间存在差距（如Claude Haiku 4.5流程质量高但结果中等），开源模型表现更弱（Qwen3.5-9B ToolUseScore 31.18但NumScore仅1.30）。关键发现：工具使用质量普遍高于答案质量，数值误差是主要失败模式（84.6%-99.3%），模型对模拟和可视化工具使用不足（<1.31%）。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是当前基准构建依赖严格的后执行验证和确定性工作流，虽然保证了科学严谨性，但自由形式轨迹的标注者间一致性评估不足；二是深度优先的标注策略导致每个任务构建成本高昂，限制了规模扩展；三是所有模型在工具使用熟练度与最终答案正确性之间存在显著差距，表明现有Agent缺乏对异构工作流的全局协调能力。

未来可从以下方向探索：首先，开发半自动化标注流水线，利用LLM生成候选轨迹并辅以专家校验，在保持科学严谨性的同时降低构建成本；其次，引入分层专家审计机制，对数值容差验证等关键决策进行独立审核，提升基准可靠性；最后，针对工具协调瓶颈，可设计元学习框架让Agent自主发现工具调用模式，或引入因果推理模块显式建模数据流依赖关系，从而缩小过程指标与结果正确性之间的鸿沟。

### Q6: 总结一下论文的主要内容

TerraBench论文提出了一个面向地球系统科学推理的基准测试和可执行框架TerraAgent，旨在解决现有气候基础模型无法进行语言交互推理、而大语言模型无法直接处理高维地球系统数据的矛盾。该框架采用ReAct风格，将LLM的规划能力与环境检索、地理空间处理、模拟和计算工具相结合，实现多模态数据（网格化物理数据、卫星图像、地理空间上下文和模拟器输出）的协同推理。基准包含403个复杂任务，涵盖三个轨道（基础、模拟器驱动和文档驱动验证）和八个应用领域，共24,500个验证执行步骤。核心贡献在于：首次在统一可执行接口中整合地球观测、网格数据分析、GIS推理和模拟，并引入过程级工具使用指标与容错数值评分。主要结论是，当前最先进模型在工具使用熟练度与最终答案正确性之间存在显著差距，表明可靠的地球科学智能体不仅需要工具访问能力，还需协调异构工作流、精确参数化工具并维护工件来源。该工作为开发科学可靠的地球科学LLM智能体提供了可复现的测试平台。
