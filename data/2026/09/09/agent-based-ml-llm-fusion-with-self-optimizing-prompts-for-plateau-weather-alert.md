---
title: "Agent-Based ML-LLM Fusion with Self-Optimizing Prompts for Plateau Weather Alerts"
authors:
  - "Shuai Yan"
  - "Yang Xu"
  - "Shan He"
date: "2026-09-09"
arxiv_id: "2609.10135"
arxiv_url: "https://arxiv.org/abs/2609.10135"
pdf_url: "https://arxiv.org/pdf/2609.10135v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "LLM Agent"
  - "Self-Optimizing Prompts"
  - "Weather Alert Generation"
  - "Natural Language Report Generation"
  - "Explainable Decision-Making"
  - "Industrial Sensor Interpretation"
  - "Multi-Stage Architecture"
  - "Intent Recognition"
  - "Hazard Prediction"
  - "Reasoning-Enhanced Generation"
  - "LightGBM"
  - "Uncertainty Statements"
  - "Causal Mechanisms"
  - "Proactive Perception"
relevance_score: 7.5
---

# Agent-Based ML-LLM Fusion with Self-Optimizing Prompts for Plateau Weather Alerts

## 原始摘要

To address insufficient contextualization, weak generalization, and poor scenario adaptation in tourism meteorological services, we propose SmartWeatherAgent--a unified three-stage architecture integrating intent recognition, hazard prediction, and reasoning-enhanced generation. The system fuses rule-based methods with large language models to parse queries at multiple granularities and employs a LightGBM model enriched with highland-specific features (e.g., wind speed abruptness rate), achieving an F1-Macro score of 0.605 with 1.60 ms latency on high-wind, precipitation, and low-temperature events. A 12-round micro-step prompt self-optimization loop boosts the composite warning quality score S_final from 4.2 (B01) to 8.9 (B12, +112%). Key improvements include a sharp rise in B08 from data source citation (6.5 -> 8.5), sustained high performance in B10 via physical mechanism explanation, and a peak scientific rigor score of 9.2 in B12 through explicit uncertainty statements. The system autonomously generates structured warnings that integrate causal mechanisms, spatiotemporal evolution, quantitative evidence, regulatory references, and confidence statements--enhancing professional depth, logical rigor, and scientific soundness, and advancing meteorological services toward proactive perception, explainable decision-making, and intelligent agency.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

高原旅游气象服务具有高度动态性、强空间异质性和场景依赖性，现有静态规则系统或通用大语言模型普遍存在响应延迟高、场景适应差、上下文感知弱以及缺乏自我进化机制等问题，难以满足游客个性化决策需求。为此，本文提出SmartWeatherAgent，首次将提示自优化机制嵌入智能气象代理核心，构建意图识别、灾害预测与推理增强生成三阶段统一架构。其核心要解决的是：如何通过规则方法与LLM融合实现多粒度查询解析，利用融入高原特有特征（如风速突变率）的LightGBM模型对大风、降水、低温事件进行高效临近预报，并通过12轮微步提示自优化闭环，动态生成融合因果机制、时空演变、定量证据、法规引用与置信度声明的结构化预警，从而提升专业深度、逻辑严谨性与科学合理性，推动气象服务向主动感知、可解释决策与智能代理演进。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，传统气象预警多依赖静态规则系统，如基于阈值的专家规则，虽可解释但泛化差、场景适应性弱；另一类是通用大语言模型直接生成预警，具备一定语言组织能力，但缺乏领域知识约束、易产生幻觉且无自进化机制。此外，LightGBM等梯度提升树模型被广泛用于气象短临预测，但通常仅输出分类结果，缺乏面向用户的解释与推理。应用类方面，已有旅游气象服务研究多聚焦于信息推送与可视化，较少实现意图识别、风险预测与可解释生成的一体化闭环。评测类方面，现有工作多采用准确率、F1等单一指标，鲜有对预警文本质量（如因果机制、时空演化、不确定性表述）进行多轮次、多维度的综合评分。本文与上述工作的核心区别在于：首次将提示自优化机制嵌入气象智能体核心，融合规则与LLM进行多粒度意图解析，并以高原专属特征增强LightGBM实现1.60 ms低延迟预测，同时通过12轮微步提示自优化循环，将综合预警质量分从4.2提升至8.9，实现主动感知、可解释决策与智能代理的一体化。

### Q3: 论文如何解决这个问题？

该论文提出SmartWeatherAgent，一个面向高原旅游气象预警的三阶段统一架构，核心思路是将规则方法、机器学习与大语言模型深度融合，并通过提示自优化实现闭环进化。

整体框架分为三层：意图识别、灾害预测与推理增强生成。第一层采用正则表达式匹配与Qwen3大模型协同分类，正则负责初步过滤，LLM解决上下文歧义，将用户意图划分为简单查询、灾害预警、家庭出行等六类，提升系统鲁棒性。第二层针对高原强风、降水、低温三类高影响天气，构建基于LightGBM的短临预报模型，并引入高原专属特征：风速突变率、降水爆发指示、阵风比以及正余弦时间编码，辅以滚动统计、阈值二值化和分位数极端性标记，形成多维输入表示，实现1.60 ms延迟、F1-Macro 0.605的实时预测，同时为生成模块提供结构化依据。第三层建立“生成→评估→优化”闭环流水线，通过12轮微步迭代驱动LLM进行提示自适应优化。输出质量由复合评分S_final衡量，融合语义、逻辑与科学性三部分：语义分考察从现象描述到多因子耦合机制再到区域风险分化的递进；逻辑分评估“天气系统触发→时间演化→影响传播→针对性建议”推理链的完整性；科学分由量化指标清晰度、数据可追溯性、法规引用准确性、不确定性陈述完整性和术语严谨性五维加总。

创新点在于：将高原物理特征工程与轻量梯度提升模型结合，兼顾精度与实时性；设计12轮微步提示自优化机制，使S_final从4.2提升至8.9（+112%），科学严谨性峰值达9.2；系统可自主生成融合因果机制、时空演化、量化证据、法规引用与置信度声明的结构化预警，推动气象服务向主动感知、可解释决策与智能代理演进。

### Q4: 论文做了哪些实验？

论文围绕高原气象预警开展了两组实验。第一组是灾害预测模型对比实验，使用VisualCrossing提供的拉萨2024年1月1日至2025年5月21日逐小时气象数据，共12168条记录，含温度、降水、风速、阵风、UV指数和能见度等变量，缺失值低于2.1%并用线性插值填补，按7:3时序划分训练测试集。构建38维特征，包括3/6小时滚动统计、风速一阶差分、阵风比、昼夜温差指示、正余弦周期编码和极端事件指示变量。对比LightGBM、随机森林、梯度提升、XGBoost和CatBoost，采用贝叶斯优化和5折TimeSeriesSplit调参。结果显示LightGBM综合得分S=0.55最高，F1-Macro为0.61，低温F1达0.77，降水F1为0.50，强风F1为0.17，准确率97%，推理延迟仅1.60ms，显著优于随机森林的63.72ms。第二组是提示词自优化实验，采用12轮微步闭环框架，基于Qwen-Max生成预警，从语义深度、逻辑连贯和科学严谨三维评分。复合得分S_final从B01的4.2提升至B12的8.9，提升112%，其中B08因数据来源引用从6.5升至8.5，B12科学严谨性达9.2，各指标标准差均小于0.5。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三方面：数据仅限拉萨，地理泛化能力不足；提示词自优化受限于预设评价维度与分阶段框架，缺乏对新兴预警需求的开放感知和结构自重构能力；系统未接入实时业务数据流，在通信中断、传感器噪声或极端稀有事件下的鲁棒性有待检验。未来可从以下方向探索：一是引入跨区域迁移学习或元学习，提升对不同高原城市的适应能力；二是将提示优化从封闭维度扩展为开放式需求发现机制，结合强化学习实现评价维度的动态演化；三是构建实时数据同化与在线学习闭环，增强对数据异常和概念漂移的鲁棒性。此外，可探索多模态融合（如卫星云图、雷达回波）与不确定性量化，并引入人机协同反馈机制，让领域专家参与预警生成与纠偏，从而在保持可解释性的同时提升系统的持续适应性与业务可信度。

### Q6: 总结一下论文的主要内容

论文针对旅游气象服务中上下文不足、泛化能力弱和场景适应性差的问题，提出了SmartWeatherAgent——一个融合意图识别、灾害预测与推理增强生成的三阶段统一架构。系统将规则方法与大型语言模型相结合，实现多粒度查询解析，并采用融入高原特有特征（如风速突变率）的LightGBM模型，对大风、降水和低温事件进行预测，F1-Macro达0.605，延迟仅1.60毫秒。通过12轮微步提示自优化循环，综合预警质量得分S_final从4.2提升至8.9，增幅达112%，其中数据源引用、物理机制解释和不确定性声明等维度均有显著改善。系统能够自主生成融合因果机制、时空演变、定量证据、法规引用和置信度声明的结构化预警，显著提升了专业深度、逻辑严谨性和科学合理性，推动气象服务向主动感知、可解释决策和智能代理方向发展。
