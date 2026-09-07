---
title: "WearableQA: A Benchmark for Health Reasoning over Real-World Wearable Data"
authors:
  - "Ji Soo Lee"
  - "Xilun Chen"
  - "Pierce Chuang"
  - "Ashish Shenoy"
  - "Jason Wei"
  - "Dohwan Ko"
  - "Hyunwoo J. Kim"
  - "Benoit Corda"
date: "2026-09-04"
arxiv_id: "2609.05405"
arxiv_url: "https://arxiv.org/abs/2609.05405"
pdf_url: "https://arxiv.org/pdf/2609.05405v1"
categories:
  - "cs.CL"
tags:
  - "time series reasoning"
  - "wearable health data"
  - "LLM benchmark"
  - "multi-signal integration"
  - "health reasoning"
  - "longitudinal data"
  - "physiological interpretation"
relevance_score: 7.5
---

# WearableQA: A Benchmark for Health Reasoning over Real-World Wearable Data

## 原始摘要

Recent advances in wearable sensing enable continuous monitoring of physiological and behavioral signals, yet existing benchmarks rarely evaluate whether AI systems can reason over a real user's longitudinal wearable record. We introduce WearableQA, a benchmark comprising 4,084 10-option multiple-choice questions constructed from the wearable time series, blood biomarkers, and demographics of 200 real users, each with up to 500 days of daily measurements. WearableQA preserves authentic wearable distributions that include device noise and inter-individual variability. To evaluate distinct reasoning capabilities, we introduce 16 question types organized along two complementary axes: data versus health reasoning, which distinguishes computation over longitudinal measurements from physiological interpretation; and single- versus cross-signal reasoning, which separates reasoning about individual signals from the integration of multiple signals. To construct reliable questions at scale, we adopt a dual-grounding framework that combines literature-grounded physiological findings with statistically validated population-grounded physiological patterns. This enables the capture of meaningful relationships observed in real-world wearable data. Evaluation of 14 proprietary and open-source LLMs demonstrates that WearableQA effectively differentiates model capabilities, with performance ranging from 19.6% to 72.9% against a 10% chance baseline. Moreover, WearableQA remains far from solved: most models achieve accuracies below 60%. Overall, WearableQA provides a realistic and diagnostic benchmark for evaluating LLM reasoning over real-world wearable data.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着可穿戴传感技术的进步，人体生理与行为信号（如心率、睡眠、活动量）可被长期连续监测，大语言模型（LLM）也被越来越多地用于个性化健康理解与监测。然而，现有AI系统在真实用户纵向可穿戴数据上的推理能力远未被充分评估。当前基准测试大多依赖合成或模拟信号，而非真实世界测量数据，因此无法反映设备噪声、个体间差异及用户特定基线等真实分布特征。此外，现有评测很少区分“从原始数据中计算信息”与“结合生理知识进行健康解释”这两种本质不同的推理能力，也难以诊断模型在整合多源信号时的不足。为此，本文提出WearableQA基准，包含基于200名真实用户、每人长达500天日常测量数据（含可穿戴时间序列、血液生物标志物与人口统计学信息）构建的4,084道选择题。其核心目标是系统评估LLM能否对真实用户的长期纵向可穿戴记录进行可靠推理，并精细诊断模型在数据推理与健康推理、单信号与跨信号推理等维度上的具体短板，从而填补现有基准缺乏真实性、诊断性与规模化构建方法的空白。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**医学与健康推理评测类**：如MedQA、MedMCQA、PubMedQA和HealthBench，主要基于文本和静态病例评估医学知识，但缺乏对个体纵向生理历史的推理能力。本文与之区别在于，WearableQA基于真实用户的长期可穿戴数据，要求模型整合时间序列与多源信号。**生理信号问答类**：如ECG-QA将心电图波形引入问答，但波形推理与纵向可穿戴数据聚合不同，后者需跨时间整合多模态行为与生理信号。PHIA虽涉及可穿戴数据，但基于模拟轨迹且侧重检索聚合，未结合血液生物标志物。本文则使用真实用户数据并联合人口统计信息与生物标志物。**时间序列推理评测类**：如TimeSeriesExam等，多依赖合成或模拟信号，侧重通用数值推理、模式识别等，缺乏真实世界噪声与个体差异，也未评估生理学解释。WearableQA填补了这一空白，通过16种问题类型区分数据推理与健康推理，并基于文献和统计验证的群体模式构建确定性答案，实现诊断性评测。

### Q3: 论文如何解决这个问题？

WearableQA通过“双 grounding”框架系统性地解决真实世界可穿戴数据健康推理的评测难题。整体框架包含三个核心模块：数据构建、问题生成和质量控制。

在数据构建上，基准整合了200名真实用户的纵向可穿戴时间序列（16项日常指标，覆盖心适能、活动能量、睡眠和压力四大生理域）、17项血液生物标志物及人口统计学信息，并保留设备噪声和个体差异，确保数据真实性。

问题生成采用“先发现后标注”策略。文献grounding从11篇经PubMed/PMC验证的同行评审论文（如Nature Medicine）提取生理关系，要求每个关系至少有两项独立同向研究支持，并记录结构化卡片防止过度声明。群体grounding则直接从大型队列挖掘模式，通过三重统计验证门：效应量（|ρ|≥0.5且窗口前后符号一致）、稳健性（bootstrap 80%复现、留一天验证、死区排除）和真实性（跨用户错配检验FDR≤0.20）。所有问题的答案均由确定性计算程序从用户真实测量中推导，而非预先设定。

架构上，问题沿两个正交轴组织：数据推理vs健康推理（区分计算与生理解释），单信号vs跨信号推理（区分独立与集成分析），形成16种问题类型。每个问题通过可复用计算原语库（如lagged_correlation、threshold_flags）实例化为显式计算图，保证可复现性。干扰项构造区分推理类型：数据推理使用相反趋势、相邻窗口等可验证类别，健康推理则基于临床合理但矛盾的解读。

质量控制包括计算有效性验证、重复项去除、答案平衡、三模型+人工审核，并审计捷径（如高预测性指标对、选项类别泄漏）。创新点在于：双grounding机制结合文献证据与数据驱动模式，2×2分类学提供诊断性能力评估，以及10选项设计将随机基线降至10%，有效区分模型能力（19.6%-72.9%）。

### Q4: 论文做了哪些实验？

论文构建了WearableQA基准，包含4084道10选1多选题，数据来自200名真实用户长达500天的可穿戴时间序列、血液生物标志物和人口统计信息。实验评估了14个专有和开源LLM，包括GPT-4o、GPT-5.4、Gemini-2.5-Pro、Gemini-3.1-Pro、Claude-Sonnet-4、Claude-Opus-4.6，以及Llama系列、Gemma系列和Mistral-Small-3.1等。

实验设置采用默认链式思考（CoT）协议，每道题附带用户最近500天数据、人口统计、血液标志物和队列参考统计。主要结果：准确率从Llama-3.2-3B的19.6%（接近10%随机基线）到Gemini-3.1-Pro的72.9%不等。Gemini-3.1-Pro领先第二名Claude-Opus-4.6（60.2%）12.7个百分点。开源模型中Gemma-4-26B-A4B最佳（42.5%），超过GPT-4o（34.7%）7.8个百分点。

细粒度分析显示：多数模型在健康推理上优于数据推理，如GPT-4o健康53.5%对数据25.3%；跨信号推理普遍更难，GPT-5.4单信号59.1%对跨信号45.7%。消融实验表明CoT显著提升专有模型性能（Claude-Opus-4.6单信号提升27点），但对开源模型增益有限。输入表示测试显示文本格式优于图像格式（行式51.2%对图像网格36.6%）。Agentic评估中，GPT-5.4配备Python工具后准确率提升至71.3%。位置偏差分析发现小模型存在严重选项偏好（Llama-3.2-3B直接回答时51.5%选同一选项），CoT可缓解此偏差。先验依赖测试显示模型在定义性信号对上表现远优于经验性信号对（如Gemini-2.5-Pro差距51.5点），表明模型更擅长利用先验知识而非从数据中推断用户特定关联。

### Q5: 有什么可以进一步探索的点？

WearableQA的局限性与未来探索可从以下方向展开：其一，当前问题基于200名用户的静态历史数据，缺乏对时间动态因果关系的建模，未来可引入干预性问答（如“若用户改变睡眠习惯，静息心率将如何变化”）以测试模型的因果推理能力；其二，双 grounding 框架依赖文献与群体统计模式，对个体化罕见生理状态（如疾病早期信号）覆盖不足，可结合无监督异常检测或个性化基线建模生成更具临床意义的问题；其三，模型在跨信号整合上表现薄弱，可探索多模态融合架构（如将时间序列与文本化健康日志联合编码）或引入检索增强生成（RAG）机制，使模型能主动查询相关生理背景知识；其四，现有评估仅关注答案正确率，未来可增加对推理过程可解释性的度量，如要求模型输出中间计算步骤或置信度，以区分“猜测正确”与“真正理解”；最后，可扩展至非日粒度数据（如分钟级HRV）或加入干预后的反事实数据，以更贴近可穿戴设备在真实健康管理中的动态决策场景。

### Q6: 总结一下论文的主要内容

WearableQA是一个针对真实世界可穿戴数据健康推理的基准测试，包含来自200名真实用户的4,084道选择题，每道题基于长达500天的日常测量数据（包括可穿戴时间序列、血液生物标志物和人口统计信息）构建。该基准通过保留设备噪声和个体差异，真实反映了可穿戴数据的分布特性。论文设计了16种问题类型，沿“数据推理vs健康推理”和“单信号vs跨信号推理”两个维度系统评估模型能力。为大规模构建可靠问题，作者提出双重锚定框架，结合文献支撑的生理学发现与统计验证的人群模式。对14个专有和开源LLM的评估显示，模型准确率在19.6%至72.9%之间（随机基线为10%），多数模型低于60%，表明该任务尚未解决，尤其数据推理和跨信号推理对现有模型构成显著挑战。WearableQA为评估LLM在真实可穿戴数据上的推理能力提供了现实且可诊断的基准。
