---
title: "Can LLM Coding Agents Reason About Time Series?"
authors:
  - "Filip Rechtorík"
  - "Ondřej Dušek"
  - "Zdeněk Kasner"
date: "2026-06-15"
arxiv_id: "2606.16545"
arxiv_url: "https://arxiv.org/abs/2606.16545"
pdf_url: "https://arxiv.org/pdf/2606.16545v1"
categories:
  - "cs.CL"
tags:
  - "LLM Agent"
  - "time series reasoning"
  - "coding agent"
  - "benchmark"
  - "statistical analysis"
  - "automated decision-making"
relevance_score: 8.5
---

# Can LLM Coding Agents Reason About Time Series?

## 原始摘要

Large language models (LLMs) are increasingly being used for automated decision-making systems in finance, healthcare, or environmental monitoring. Time series data are ubiquitous in these fields, yet hard to process automatically. Can time series be analyzed by LLM agents? We examine three approaches: providing the agent with raw numerical data, using the LLM as a coding agent, or a combination of both. In the coding agent setup, the model iteratively queries the data using Python code. Using two time series understanding benchmarks, we show that agents with code access can outperform models processing raw data by up to 10%. However, even the best performing agent still answers about 22-34% of the questions incorrectly. To get insights into models' strategies and reasoning gaps, we analyze the model outputs with a strong LLM judge. Our analysis reveals that coding agents can select appropriate statistical tests, but often miss important nuances. Meanwhile, models with access to raw data can reach the right conclusions using back-of-the-envelope calculations.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列分析在金融、医疗和环境监测等领域至关重要，但传统方法依赖人类专家结合领域知识，难以自动化。现有LLM直接处理原始数值数据的方法表现不可靠，常被领域特定基线模型超越，且系统性失败于某些任务。本文旨在探索LLM编码智能体能否通过生成Python代码来推理时间序列，以提升自动化分析能力。核心问题是：相比直接处理原始数据，编码智能体是否能更准确地理解时间序列？现有方法不足在于：直接模型缺乏有效策略，而编码智能体虽能选择合适统计检验，却常忽略关键细微差别，且即使最佳智能体仍有22-34%的问题回答错误。因此，本文通过三种设置（原始数据、编码工具、两者结合）进行基准测试，并构建行为分类法，利用LLM裁判自动分析模型输出，以揭示推理差距和错误模式。

### Q2: 有哪些相关研究？

本文的相关研究主要分为三类：

1. **自动化时间序列分析的LLM方法**：这类工作探索将LLM直接应用于时间序列任务，如构建时间序列基础模型（通过大规模预训练）或利用LLM的零样本能力。本文指出，这些方法在需要多步推理或处理特定范围约束时表现不佳，而本文通过对比实验发现，编码智能体（coding agent）在时间序列理解基准上比直接处理原始数据的模型高出10%，但仍有22-34%的错误率。

2. **编码智能体与程序辅助推理**：相关工作包括PAL（通过生成Python代码进行中间推理）、BINDER和RePanda（将自然语言转换为SQL或pandas表达式），以及TS-Reasoner（基于ReAct范式将复杂推理任务分解为专用算子管道）。本文与这些工作的区别在于：本文不仅评估了编码智能体在时间序列任务上的表现，还将其与直接处理原始数据的方法进行了系统比较，并深入分析了智能体的决策过程，而先前工作（如）未进行此类对比。

3. **推理轨迹分析**：这类工作利用LLM作为评判者（LLM-as-a-judge）自动评估模型的推理过程，包括事实性、有效性、连贯性和实用性。本文采用了类似方法，通过强LLM评判者分析模型输出，揭示了编码智能体虽能选择适当的统计检验，但常忽略重要细节；而直接处理原始数据的模型则能通过粗略计算得出正确结论。

### Q3: 论文如何解决这个问题？

该论文通过对比三种LLM Agent架构来解决时间序列推理问题，核心方法是将时间序列理解任务转化为多项选择题，并评估不同数据呈现方式和工具使用对模型性能的影响。

整体框架包含三种设置：**直接代理**（Direct Agent）仅提供原始数值文本；**代码代理**（Code Agent）将数据加载为pandas DataFrame，允许模型通过编写Python代码迭代查询；**混合代理**（Hybrid Agent）则同时提供原始数据和DataFrame访问权限。后两者构成编码代理（Coding Agent），支持多轮代码执行与反馈循环。

关键技术包括：1）数据表示层：原始数据以纯文本形式呈现，DataFrame则支持通过代码进行统计计算和可视化；2）推理循环机制：编码代理可生成代码、执行并获取输出，直至模型决定给出最终答案；3）输出解析：通过编辑距离匹配提取<answer>标签中的答案。

主要创新点在于：1）系统性对比了三种信息获取方式对时间序列推理的影响，发现混合代理在TimeSeriesExam和TSFU基准上分别达到78.0%和65.6%的最高准确率，比直接代理提升约10%；2）揭示了编码代理的优势与局限——能正确选择统计检验方法但常忽略细微特征，而直接代理可通过心算推理得出正确结论；3）分析了不同问题类型的最佳策略差异，如代码代理更擅长相关性分析，直接代理更适合结构突变检测。实验使用gpt-oss-120b和qwen3-next-80b两个模型，验证了混合设置对高性能模型的有效性。

### Q4: 论文做了哪些实验？

论文在时间序列理解基准上进行了实验。实验设置包括三种LLM代理方式：直接代理（仅访问原始文本数据）、代码代理（通过Python代码查询DataFrame）和混合代理（同时访问原始数据和代码）。数据集采用TimeSeriesExam（746道多选题，涵盖5大类别）和TSFU（2000道题，覆盖10个特征类别）。对比方法包括随机基线（TimeSeriesExam上40.1%，TSFU上29.3%）以及gpt-oss-120b和qwen3-next-80b两个模型。

主要结果：混合代理表现最佳，在TimeSeriesExam上gpt-oss-120b达到78.0%准确率（代码代理70.4%，直接代理65.3%），在TSFU上达到65.6%（代码代理63.0%，直接代理55.6%）。代码代理比直接代理提升高达10%，但最佳代理仍有22-34%的错误率。分析显示，代码代理能选择合适统计检验但常忽略细微差别，直接代理则通过简单估算也能得出正确结论。代码代理在93.6-94.6%情况下依赖代码，但未用代码时准确率骤降至42.0%（接近随机基线）。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是当前仅使用多选题基准测试，无法全面评估代理在真实场景中编写完整分析流程、处理噪声数据等开放式任务的能力；二是实验仅针对开源模型，商业模型虽能力更强但推理链不可见，限制了深度分析；三是未与专门的时间序列预训练模型对比。未来可探索的方向包括：构建更贴近实际需求的基准，如要求代理自主完成数据清洗、特征工程和自由文本报告生成；引入多模态融合策略，将原始数值与代码执行结果结合，弥补纯数值推理的细节缺失；设计可解释性增强模块，通过显式约束代理在代码中嵌入统计假设检验的上下文注释，减少对细微差别的忽略；此外，可尝试将时间序列预训练模型作为LLM的工具调用接口，利用其专业特征提取能力辅助推理。

### Q6: 总结一下论文的主要内容

这篇论文研究了大型语言模型（LLM）智能体在时间序列分析中的推理能力。核心问题是：LLM能否通过编码智能体形式有效分析时间序列数据？论文比较了三种方法：直接提供原始数值数据、将LLM作为编码智能体（通过Python代码迭代查询数据）、以及两者结合。在时间序列理解基准测试上，编码智能体比处理原始数据的模型准确率提升高达10%，但最佳智能体仍有22-34%的问题回答错误。通过LLM裁判分析模型输出发现，编码智能体能选择恰当的统计检验，但常忽略关键细节；而访问原始数据的模型虽方法简单（如估算），却有时能得出正确结论。论文贡献在于系统评估了不同智能体设置，揭示了编码智能体在时间序列任务中的潜力与局限，强调了需要谨慎管理以避免过度信任数值结果和遗漏细微信息。
