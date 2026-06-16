---
title: "Towards Verifiable Agentic Data Science: Solving Irregular TSQA Via Tool-Grounded Reasoning"
authors:
  - "Sanhorn Chen"
  - "Xiaoyang Chen"
  - "Boyu Liu"
  - "Roy Zhao"
date: "2026-06-13"
arxiv_id: "2606.15107"
arxiv_url: "https://arxiv.org/abs/2606.15107"
pdf_url: "https://arxiv.org/pdf/2606.15107v1"
github_url: "https://github.com/SanhornC/IRTS-ToolBench"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Time Series Question Answering"
  - "Tool-Grounded Reasoning"
  - "Irregular Time Series"
  - "LLM/Agent"
  - "Benchmark"
  - "Verifiability"
  - "Time Series Analysis"
  - "AI Agent"
  - "Tool Calling"
relevance_score: 9.5
---

# Towards Verifiable Agentic Data Science: Solving Irregular TSQA Via Tool-Grounded Reasoning

## 原始摘要

Time series data in real-world deployments is overwhelmingly irregular. Observations are asynchronous, missing values are informative rather than random, and sampling frequencies vary across sensors and operational windows. However, existing Time Series Question Answering (TSQA) benchmarks mostly assume regularly sampled inputs, leaving a fundamental gap in understanding how large language models (LLMs) and AI agents perform under irregular conditions. To bridge this gap, we introduce IRTS-ToolBench, a benchmark of 1,700 questions spanning 10 task types across 13 domains. IRTS-ToolBench is designed to be used independently by any researcher working on LLM-based irregular time series analysis, providing standardized inputs and a reproducible evaluation protocol. Code can be found in https://github.com/SanhornC/IRTS-ToolBench.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决现有时间序列问答（TSQA）基准无法有效评估大语言模型（LLM）和AI智能体在不规则时间序列数据上推理能力的问题。研究背景方面，现实世界中的时间序列数据普遍存在不规则性，如观测异步、缺失值具有信息性而非随机性、采样频率因传感器和操作窗口而异。然而，现有的TSQA基准大多假设输入是规则采样的，这导致对LLM和AI智能体在不规则条件下表现的评估存在根本性缺口。现有方法的不足在于：一方面，现有基准仅处理规则时间序列；另一方面，已有的合成不规则化方法（如MCAR随机丢弃和稀疏掩码重采样）缺乏领域语义理解，生成的数据虽统计上不规则但语义上不可信。TIME-IMM虽识别出真实不规则性有九种因果驱动类型，但尚无工作提出语义驱动的规则到不规则时间序列转换流水线。因此，本文的核心问题是构建一个能够基于工具推理、语义可解释的不规则TSQA基准，以系统评估LLM和AI智能体在真实世界不规则时间序列分析中的表现。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及三大类别。首先，在**TSQA评测基准**方面，TSAQA通过多LLM共识机制生成了六类任务的层次化分类，Time-MQA扩展至多任务上下文增强，ITFormer则专注于航空发动机的跨模态对齐。这些工作直接启发了本文的评测设计，但它们的共同局限是假设输入为规则采样的干净数据，而本文的IRTS-ToolBench专门针对不规则时间序列（如异步观测、非随机缺失）构建了1700个问题，填补了这一空白。

其次，在**不规则时间序列分类与变换方法**上，TIME-IMM提出了九类不规则性分类法（触发式、约束式、伪影式），本文的变换流水线直接采用该分类作为决策空间；Physiome-ODE提供了基于生物ODE的不规则多变量预测基准。然而，这些工作均未利用LLM指导不规则化过程，而本文通过工具增强的Agent工作流实现了可验证的推理。

最后，在**Agent时间序列框架**方面，TimeART建立了工具增强的ReAct风格Agent模板，TS-Agent专注于统计洞察，TimeSeriesScientist则优化了预测工作流。本文在此基础上，将Agent评估扩展至不规则领域，并强调通过工具调用实现可验证的推理过程，而非依赖LLM的隐式知识。

### Q3: 论文如何解决这个问题？

论文通过构建一个名为IRTS-ToolBench的基准测试框架，系统性地解决了非规则时间序列问答（TSQA）中LLM和AI Agent的可验证推理问题。核心方法围绕一个三阶段流水线展开：首先，对来自13个领域的规则时间序列样本进行非规则化转换，通过上下文增强（LLM生成领域和统计特征描述）、分类学选择（LLM选择非规则类型并输出转换计划）和参数生成（LLM生成验证后的数值参数）三个步骤，生成具有真实缺失模式和非均匀采样间隔的非规则序列。其次，采用多LLM共识机制生成问答对，由三个独立LLM（GPT-5.1、Claude Sonnet 4.5、Gemini 2.5 Flash）评估问题的清晰度和可回答性，确保数据质量。最后，通过独立提案与多数投票结合的方式构建黄金工具集，指定回答每个问题必须调用的最小工具序列。

在架构设计上，基准测试包含1700个问题，涵盖10种任务类型，分为三个递进推理层次：标准推理（异常检测、分类等）、非规则特定推理（时序特征表征、因果关系归因等）和规则-非规则接口推理（缺失推理、严重性估计等）。关键技术包括一个30个工具的库，分为非规则操作符（7个）和高级分析工具（23个，如统计摘要、趋势检测），支持LLM通过工具增强提示或Agent框架进行可验证推理。创新点在于：1）首次系统评估LLM在非规则时间序列上的推理能力；2）通过可复现的标准化协议和黄金工具集实现结果的可验证性；3）构建了从基础采样理解到跨表示推理的渐进式评估体系。

### Q4: 论文做了哪些实验？

论文构建了IRTS-ToolBench基准测试，包含1700个问题，覆盖10种任务类型和13个领域。实验设置包括：通过多LLM评估器（GPT-5.1、Claude Sonnet 4.5、Gemini 2.5 Flash）进行任务质量验证，并随机抽取2%子集进行人工评审（两名本科生独立作答，准确率分别为80%和78%）。对比方法包括商业模型Claude-Opus-4.7（无思考、有思考、有工具调用）和开源模型Qwen3.5-4B、Qwen3.6-27B、DeepSeek-V4-Flash（有无工具调用）。主要结果：Qwen3.6-27B以78.59%总体准确率领先，Claude-Opus-4.7稳定在74-77%。工具调用显著提升特定任务：Qwen3.6-27B在异常检测上从96.80%升至99.60%，分类任务达100%；DeepSeek-V4-Flash在不规则性严重程度估计上从31.33%跃升至98.67%，规律性恢复从64.67%升至89.33%。但时间关系推理和规则vs不规则判别等任务仍具挑战性，表明工具调用对显式数值分析有效，而高层时间推理仍困难。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是三层LLM生成管道对提示敏感，可能引入偏差；二是当前仅支持单变量时间序列，且任务类型以单跳推理为主；三是工具使用依赖预定义的金标准工具集，缺乏动态工具选择能力。未来可探索以下方向：首先，引入多变量和多模态数据（如图表、文本），提升基准的真实性；其次，设计多跳推理任务，测试模型在复杂因果链条下的时序理解能力；此外，可研究自适应工具选择机制，让Agent根据问题动态组合工具而非依赖固定集合；最后，结合可解释性分析，探索模型在工具调用过程中的推理路径可视化，以增强结果的可验证性。

### Q6: 总结一下论文的主要内容

这篇论文针对现实世界中时间序列数据普遍存在的不规则性（如异步观测、信息性缺失、采样频率变化）问题，提出了一个评估大语言模型（LLM）和AI智能体在不规则时间序列问答（TSQA）中表现的标准基准——IRTS-ToolBench。该基准包含1700个问题，覆盖10种任务类型和13个领域。核心贡献在于：通过语义驱动的不规则时间序列构建、任务级诊断以及包含30个工具的工具库，实现了对答案正确性和基于工具推理行为的标准化评估。主要结论是：当前LLM在不规则时间序列上已展现出一定的推理能力，尤其在提供上下文和工具时表现更好，但在高层时序推理和可靠工具使用方面仍存在困难。该工作填补了现有TSQA基准主要假设规则采样数据的空白，为可验证的智能体数据科学研究提供了重要平台。
