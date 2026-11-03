---
title: "ClickSight: An LLM Framework for Interpreting Student Clickstreams Through Learning Strategies"
authors:
  - "Bahar Radmehr"
  - "Lan Tran"
  - "Ekaterina Shved"
  - "Fatma Bet{ü}l G{ü}reş"
  - "Adish Singla"
  - "Tanja K{ä}ser"
date: "2026-11-01"
arxiv_id: "2611.02021"
arxiv_url: "https://arxiv.org/abs/2611.02021"
pdf_url: "https://arxiv.org/pdf/2611.02021v1"
github_url: "https://github.com/epfl-ml4ed/ClickSight-CEAI"
categories:
  - "cs.AI"
  - "cs.CL"
  - "cs.CY"
tags:
  - "LLM"
  - "clickstream"
  - "时序语义报告"
  - "证据路由"
  - "可解释诊断"
  - "教育数据挖掘"
  - "分阶段管道"
  - "LLM评估"
relevance_score: 7.5
---

# ClickSight: An LLM Framework for Interpreting Student Clickstreams Through Learning Strategies

## 原始摘要

Digital learning environments produce rich clickstream data that can reveal how students approach learning tasks, yet interpreting these fine-grained traces often requires substantial expert effort. We introduce ClickSight, a framework for interpreting student clickstreams through learning strategies defined in the literature. Given a student clickstream and a predefined set of learning strategies, ClickSight uses a staged LLM-based pipeline to identify strategy-relevant evidence, assess adherence to each strategy, and generate an evidence-grounded interpretation of the student's behavior. We evaluate ClickSight across two learning environments, 365 students, and 12 model backbones using an expert-grounded quality rubric and an LLM judge calibrated with human-expert ratings. Our results show that ClickSight can generate high-quality strategy-based interpretations across different models and environments, with reasoning models performing more consistently than instruction-tuned counterparts. We further find that providing external clickstream-extracted guidance can improve interpretation quality for strategies that require precise quantitative information from the trace. By connecting fine-grained clickstreams with theoretically defined learning strategies and preserving the evidence underlying each judgment, ClickSight provides a flexible approach for studying student behavior in digital learning environments.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

数字学习环境产生的点击流数据虽蕴含丰富的学生学习行为信息，但将原始、细粒度的交互日志转化为有意义的学习行为解读仍十分困难。现有方法主要依赖机器学习技术，如设计领域特定特征、聚类学生行为、序列模式挖掘、专家标注训练监督模型或知识追踪等，虽能提取有意义的模式，但通常需要大量专家投入来定义特征、构建标签、指定模式或解释结果表示，这种对专家驱动、领域特定流程的依赖使其难以跨学习环境迁移，限制了可扩展性。大语言模型虽具备模式识别、抽象与推理能力，有望减轻专家负担，但在教育AI中主要应用于语义丰富的文本数据（如自动评分、反馈生成、质性编码），将其直接用于行为性、非文本教育数据的研究仍不充分，且多通过微调、预计算指标或工程化表示实现。因此，本文要解决的核心问题是：LLM能否直接解读点击流数据，并基于文献中理论定义的学习策略推导出高层次行为洞察。为此，作者提出ClickSight框架，采用分阶段的LLM流水线，先检索策略相关证据，再评估学生对各策略的遵循程度并给出有证据支撑的判断，最终整合为连贯的行为解读，从而在减少专家投入的同时实现可扩展、可迁移的点击流解读。

### Q2: 有哪些相关研究？

本文的相关研究主要分为两条主线。

**学习策略与点击流分析类**：一类工作基于专家定义的特征或规则，将细粒度学生行为映射到自我调节学习过程或学习策略上，如用理论驱动的轨迹解析器识别SRL过程并提供自适应支架；另一类通过人工标注轨迹片段训练监督模型，检测计划、假设检验、控制变量实验等策略行为。此外，序列模式挖掘、时序分析和聚类等方法从数据中自动发现行为结构与学习画像，减少预先设定行为类别的需求。这些方法使理论构念可从交互数据中测量，但均依赖专家确定映射、特征或解释发现模式，难以跨策略和学习环境迁移。

**LLM教育数据分析类**：现有LLM应用多处理语义丰富的文本输入，如评分与反馈、作文与编程作业评价；在定性编码中，LLM依据预定义类别或编码手册识别SRL阶段、编码课堂话语等，效果优于归纳生成类别。更近的工作将LLM扩展到行为与多模态数据，但通常先转换为量化指标、结构化表示或时间可视化再输入模型。最接近本研究的是将游戏日志转为文本回放的GPT-4o困境检测，其在数值推理信号上表现不佳，需结合传统检测器，且仅针对单一行为构念和单一环境。

区别在于：ClickSight直接在原始点击流上跨多种理论定义的学习策略和两个学习环境生成证据支撑的解释，并系统评测多模型骨干，填补了多策略、多环境下LLM解释能力的空白。

### Q3: 论文如何解决这个问题？

论文提出的ClickSight框架将原始点击流转化为LLM可读的符号化表示，再通过分阶段提示流水线生成有证据支撑的策略解读。整体流程为：首先把每个事件转换为函数式代码风格的动作表示（动作类型、参数、时间戳及系统反馈），并引入环境描述、文献定义的学习策略集合以及评估维度（aspect），形成策略—维度对。核心方法包含四个阶段：证据过滤阶段仅接收完整格式化点击流，针对每个策略筛选出与各维度相关的动作证据；证据分析阶段对筛选出的动作逐一分析其对该策略的含义；依从性评估阶段为每个维度给出依从等级及基于证据的理由；最后解读生成阶段汇总所有策略级评估，生成符合完整性、正确性、论证性和可读性四项质量标准的自然语言解读。前三阶段对每个策略独立运行，各阶段采用固定输出模式以便级联传递，从而逐步收窄证据并保留判断依据。创新点包括：将细粒度点击流与理论定义的学习策略显式连接；采用分阶段、证据可追溯的提示设计而非端到端黑箱解读；支持可选的专家撰写指导与点击流提取指导（索引、计数），后者对需要精确量化信息的策略尤为有效；并配套基于评分量表和经人类专家校准的LLM评判器进行评估。

### Q4: 论文做了哪些实验？

论文在两个数字学习环境中开展实验：PharmaSim（205名学生，诊断推理策略）和Beer's Law Lab（160名学生，探究策略），共涉及365名学生。评估了12个LLM骨干模型，涵盖Qwen3、GPT-OSS和GPT三个家族，包括指令微调版与推理版。对比方法为ClickSight的分阶段流水线（COP）与两种提示基线：零样本（ZS）和思维链（CT）。评价采用专家锚定的四维质量评分标准（完整性、正确性、论证充分性、可理解性）及经人类专家评分校准的LLM评判器（GPT-5-mini），专家间一致性κ≥0.85，评判器与专家一致性κ≥0.70。主要结果：完整性、可理解性在所有条件下均达1.00；PharmaSim中三种方法差异不显著；Beer's Law Lab中COP总体得分0.735，显著优于ZS（0.704）和CT（0.702），正确性0.815显著高于ZS。推理模型比指令微调模型表现更稳定，如Qwen3-4B-Thinking在PharmaSim的正确性和论证充分性分别为0.84和0.92，而指令版仅0.51和0.48。外部点击流提取指导可提升需精确定量信息策略的解释质量。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：其一，评估仅覆盖两个学习环境、365名学生，策略集合由文献预定义，跨领域泛化性尚未验证；其二，解释质量依赖LLM裁判且仅用人类评分校准，缺乏对下游教学干预效果的实证检验；其三，结果表明显式外部引导对需要精确量化信息的策略有增益，但引导的生成方式与误差传播尚未系统研究。未来可探索：将ClickSight与真实教学反馈闭环结合，检验解释能否改善学习结果；引入多模态与时间序列建模增强对细粒度行为模式的捕捉；研究策略定义本身的自动发现与自适应扩展，减少对专家先验的依赖；并针对推理模型与非推理模型的差异，设计轻量化的证据抽取模块以降低对强推理能力的依赖。

### Q6: 总结一下论文的主要内容

论文针对数字学习环境中点击流数据细粒度强、解释依赖专家且难以跨环境迁移的问题，提出ClickSight框架。其问题定义是：如何利用文献中定义的学习策略，将原始点击流自动转化为可解释、有证据支撑的学生行为解读。方法上，ClickSight先将点击流转换为LLM可读的符号化表示，再采用分阶段提示流水线，依次完成证据过滤、证据分析、策略依从性评估和整体解释生成，并可选择加入专家指导或点击流提取的量化信息。研究在PharmaSim和Beer's Law Lab两个环境、365名学生和12个模型上评估，结果表明ClickSight能生成高质量的策略解释，推理型模型表现更稳定，精确的点击流摘要可提升复杂策略的解释质量。其意义在于降低专家负担，连接低层交互与理论化学习策略，为规模化研究学生行为提供灵活方法。
