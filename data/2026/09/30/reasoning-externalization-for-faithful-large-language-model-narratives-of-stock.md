---
title: "Reasoning Externalization for Faithful Large Language Model Narratives of Stock Return Predictions"
authors:
  - "Sujung Kim"
  - "Seung Hwan Cho"
  - "Sangjin Park"
  - "Young-Min Kim"
date: "2026-09-30"
arxiv_id: "2609.38869"
arxiv_url: "https://arxiv.org/abs/2609.38869"
pdf_url: "https://arxiv.org/pdf/2609.38869v1"
categories:
  - "cs.AI"
  - "cs.CE"
tags:
  - "LLM叙事生成"
  - "可解释性"
  - "SHAP"
  - "证据溯源"
  - "推理外化"
  - "金融时间序列"
  - "忠实性验证"
  - "历史类比"
  - "XGBoost"
  - "自然语言报告"
relevance_score: 7.5
---

# Reasoning Externalization for Faithful Large Language Model Narratives of Stock Return Predictions

## 原始摘要

In finance, interpreting machine learning predictions is essential, yet the numerical outputs of explainable AI can be difficult for non-experts to understand. While large language models (LLMs) can translate these outputs into natural language, they may produce errors when inferring numerical changes and feature relations. We propose an LLM narrative framework for cross-sectional stock return prediction that combines temporal Shapley additive explanations (SHAP) evidence with historical regime analogs. Temporal evidence tracks changes in the normalized global SHAP importance of an XGBoost model over six months. Historical analogs are past periods with similar changes in SHAP importance, their model performance and subsequent market returns are provided as comparative context. Using this framework, we conduct a controlled study of progressive reasoning externalization, sequentially providing raw SHAP sequences, deterministic temporal descriptors, and feature relations. Each generated claim is verified against provenance-linked evidence. Across Qwen3, externalizing numerical and relational reasoning improved evidence faithfulness as well as temporal and relational accuracy. Evidence faithfulness increased from 0.696 to 0.996 for Qwen3-32B-Instruct. While historical analogs did not improve structured automatic faithfulness, they received higher human-rated usefulness scores. These results suggest that externalizing verifiable reasoning enhances narrative faithfulness and that historical context adds interpretive value.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在金融领域，机器学习预测模型的黑箱特性使其难以被理解和信任，而SHAP等可解释AI方法虽能量化特征贡献，其输出的数值结果对非专家而言仍晦涩难懂。现有研究尝试用大语言模型将SHAP输出转化为自然语言解释以提升可理解性，但存在两方面不足：其一，金融市场收益生成过程随时间因商业周期、政策变化和危机等结构性转变而演变，基于单一时间点的SHAP解释无法完整反映模型对当前市场状况的解读；其二，历史信息——即模型在类似市场条件下的表现及市场后续演变——尚未被系统性地纳入LLM解释框架，而LLM本身在时间序列推理上能力薄弱，容易在推断数值变化和特征关系时产生错误。因此，本文要解决的核心问题是：如何为LLM提供时间序列XAI证据与历史类比情境，并通过逐步外化数值与关系推理，生成忠实于证据的股票收益预测叙述。具体而言，本文构建了一个框架，将时间SHAP证据与历史相似制度类比相结合，并开展受控研究，逐步外化原始SHAP序列、确定性时间描述符和特征关系，对每条生成声明进行溯源验证，以提升叙述的证据忠实度、时间与关系准确性。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，Lundberg等用SHAP追踪特征贡献随时间的变化以诊断模型性能退化；Mougan等提出Explanation Shift，通过比较历史与当前SHAP分布检测模型特征利用方式的变化；Jenett等将XGBoost与SHAP用于REITs收益预测，发现关键变量重要性随市场状态变化。这些工作侧重监控与检测，未利用SHAP时序模式检索历史相似市场状态。应用类方面，Zeng与Zhu将SHAP输出结构化后经提示工程生成自然语言解释；Zytek等提出Explingo，含Narrator与Grader；Martens等提出XAIstories，将SHAP与反事实解释转为LLM叙事；Geng等发现向LLM提供SHAP特征排名优于让其自行推断；Wang将时序图卷积网络的解释转为股票趋势报告。评测类方面，Lukassen等指出既有研究多评估文本质量而少验证决策实用性；Pratama与Tseng发现LLM信用风险报告存在符号反转、遗漏主特征等保真度问题。此外，Khanna等用宏观指标与文本嵌入检索相似历史时期作为LLM上下文，但相似度基于宏观变量，未使用模型特征归因的时序模式。本文区别在于：将SHAP重要性的时序变化用于检索历史相似状态，并系统研究渐进式推理外化对叙事保真度的影响。

### Q3: 论文如何解决这个问题？

论文提出了一套“推理外化”的LLM叙事生成框架，用于横截面股票收益预测的可解释叙述。整体流程是：先用XGBoost对30个股票特征进行月度收益预测，并用TreeSHAP计算每个股票、特征、月份的SHAP值；再对SHAP值做横截面绝对均值与归一化，得到月度全局归因向量P_t，并构造最近六个月的时序证据S_t。随后，框架检索历史上SHAP重要性变化轨迹相似的市场状态作为“历史类比”，附带当时的RankIC和后续市场收益，作为比较性背景而非因果证据。所有预测、局部SHAP、全局归因、时序描述、特征关系和历史类比都存入统一的结构化证据注册表，每个证据单元带有唯一溯源ID。

核心创新在于“渐进式推理外化”的实验设计：C0仅提供预测与当前归因；C1加入原始六个月归因序列，让LLM自行推断趋势；C2额外提供确定性的数值统计量，如六个月变化Δ6P、OLS斜率和趋势方向；C3进一步提供“OVERTAKES”特征超越关系；C3-Analog再加入历史类比证据。这样把数值计算和关系推断从LLM转移到外部确定性模块，LLM只负责基于证据生成自然语言和结构化声明。每个声明都必须引用证据ID，并可选择弃权。实验在Qwen3-32B/14B/8B及多个模型家族上进行，结果显示外化数值与关系推理显著提升了证据忠实度，例如Qwen3-32B-Instruct从0.696提升到0.996，历史类比虽未提升自动忠实度，但人类评分的有用性更高。

### Q4: 论文做了哪些实验？

论文围绕LLM叙事生成开展了三类实验。首先，在股票收益预测任务上对比线性回归、Ridge、随机森林和XGBoost，使用RankIC、RankICIR、RMSE、MAE评估。XGBoost取得最高RankIC 0.0361和RankICIR 0.5380，较随机森林分别提升1.4%和9.8%，但RMSE和MAE略高，最终被固定用于后续SHAP分析。其次，在Qwen3、Ministral、Llama等模型上进行C0至C3的推理外化对照实验，逐步提供原始SHAP序列、确定性时序描述和特征关系。Qwen3-32B-Instruct的证据忠实度EF从C1的0.6960提升至C3的0.9964，时序准确率从0.3396升至0.9896，关系准确率从0.5250升至1.0000；C0弃权准确率为0.8386。C3-Analog的EF略降至0.9891。最后，用Claude Opus 5对400个样本做LLM-as-a-Judge评估，两条件下文本时序迁移准确率均为0.9975，C3-Relational在证据范围遵循和叙事综合上略优。另有10名评估者参与人工评价，历史类比在有用性上得分更高。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：其一，实验仅基于XGBoost与SHAP这一组合，未验证对其他模型（如深度时序模型、图神经网络）或其他归因方法（如Integrated Gradients、LIME）的适用性；其二，历史相似期（historical analogs）虽在人工评分中更有用，却未提升自动忠实度指标，说明其价值机制尚不清晰，可能与当前评估指标无法捕捉叙事解释力有关；其三，研究聚焦横截面股票收益预测，未涉及交易决策、组合优化等下游任务，也未考虑市场分布漂移对证据时效性的影响。未来可探索：将推理外化框架扩展到多模态金融数据与多模型集成场景；设计能同时衡量事实忠实度与解释有用性的混合评估体系；引入因果推断替代纯相关性SHAP证据，以增强叙事在反事实情境下的稳健性；并研究人机协作中用户反馈如何反向优化证据结构化粒度。

### Q6: 总结一下论文的主要内容

论文针对金融机器学习预测中SHAP等可解释性输出难以被非专家理解、而LLM直接基于原始数值证据生成叙述时易在数值变化与特征关系推断上出错的问题，提出一种证据锚定的LLM叙述框架。方法上，基于CRSP月度数据训练XGBoost进行横截面股票收益预测，构建30个特征的六个月全局SHAP重要性时间轨迹，并检索SHAP重要性变化相似的历史市场状态作为对比语境；随后通过渐进式推理外化，依次提供原始SHAP序列、确定性时序描述符和特征关系，并将每条生成声明与带溯源标识的证据注册表进行确定性核验。实验表明，外化数值与关系推理显著提升证据忠实度、时序准确率和关系准确率，Qwen3-32B-Instruct的证据忠实度从0.696提升至0.996；历史类比虽未提升结构化自动忠实度，但在人工评估中获得更高的有用性评分。研究说明，将易错推理步骤外化为可验证证据可提升金融XAI叙述的可靠性，历史语境则提供补充性解释价值。
