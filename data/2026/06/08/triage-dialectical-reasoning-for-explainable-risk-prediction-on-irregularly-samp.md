---
title: "TRIAGE: Dialectical Reasoning for Explainable Risk Prediction on Irregularly Sampled Medical Time Series with LLMs"
authors:
  - "Hyeongwon Jang"
  - "Gyouk Chu"
  - "Changhun Kim"
  - "Joonhyung Park"
  - "Hangyul Yoon"
  - "Eunho Yang"
date: "2026-06-08"
arxiv_id: "2606.09030"
arxiv_url: "https://arxiv.org/abs/2606.09030"
pdf_url: "https://arxiv.org/pdf/2606.09030v1"
github_url: "https://github.com/HyeongWon-Jang/TRIAGE"
categories:
  - "cs.LG"
  - "cs.AI"
  - "cs.CL"
tags:
  - "时间序列报告"
  - "可解释故障诊断"
  - "LLM/Agent"
  - "时序异常检测"
  - "自然语言报告生成"
  - "临床时间序列"
  - "证据路由"
  - "反思"
  - "可追溯诊断链"
relevance_score: 8.5
---

# TRIAGE: Dialectical Reasoning for Explainable Risk Prediction on Irregularly Sampled Medical Time Series with LLMs

## 原始摘要

Clinical early warning systems built on electronic health records, in which clinical observations are recorded as irregularly sampled medical time series (ISMTS), must deliver both calibrated risk scores for patient triage and interpretable rationales that clinicians can verify. Large Language Models (LLMs) have been explored for this task, yet they collapse graded clinical risk into overconfident binary predictions. This risk polarization undermines both calibration and cross-patient comparability. To address this, we propose TRIAGE, a framework that trains an LLM to generate dialectical reasoning over competing clinical outcomes by eliciting outcome-specific rationales. This dialectical formulation mitigates risk polarization, enabling a single LLM to yield continuous risk scores grounded in explicit clinical reasoning. Evaluated on three ISMTS benchmarks, TRIAGE achieves an average AUPRC improvement of 3.3% and reduces calibration error by 81% compared to the competitive baselines. An LLM-as-a-judge assessment further shows that our rationales surpass post-hoc explanations from the baseline by 20% in clinical reasoning quality. The source code is available at https://github.com/HyeongWon-Jang/TRIAGE .

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决在电子健康记录（EHR）中，基于不规则采样医疗时间序列（ISMTS）进行临床早期预警时，现有方法无法同时提供校准良好的连续风险评分和可解释的临床推理的问题。研究背景是，临床预警系统需要两个关键特性：一是用于患者分诊和资源分配的、跨患者可比的校准风险评分；二是基于临床知识推理的自然语言解释，以便医生验证。然而，现有方法要么是使用专门的深度学习模型（如RNN、Transformer）获得高性能但无法提供解释，要么是使用后验可解释性方法提供非语言的特征归因，但缺乏高层次临床推理。特别是，基于大语言模型（LLM）的方法也面临困境：一类方法（如HeLM）仅从隐式token概率提取连续风险评分，但无自然语言推理；另一类方法（如KARE）虽生成推理，但仅优化离散答案，导致风险评分极端化（风险极化问题），即推理过程预先承诺单一结果且只呈现支持性证据，使得预测概率偏向极端，无法实现跨患者可比。因此，本文要解决的核心问题是：如何让LLM在ISMTS风险预测中，既能生成基于辩证推理（同时考虑多种临床结局）的自然语言解释，又能输出校准良好、连续且可比较的风险评分，从而克服风险极化问题。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是**不规则采样时间序列建模方法**，包括基于RNN、ODE、集合编码器、插值、注意力、Transformer和图网络等专用架构。这些方法专注于提升预测精度和表示学习，但无法生成自然语言解释。本文与之不同，利用LLM进行临床风险预测，并将风险评估与文本推理耦合。第二类是**LLM在临床时间序列中的应用**，主要分为两种范式：一是通过答案令牌概率进行风险评分（将LLM视为分类器），二是通过硬标签预测生成推理。部分工作将预测任务交给神经网络，仅用LLM生成辅助解释。本文的创新在于将推理和风险评分统一在单个LLM中，通过辩证推理生成连续风险评分和可解释的临床推理，避免了风险极化问题。第三类是**可解释性评估**，本文采用LLM-as-a-judge评估临床推理质量，超越了传统事后解释方法。整体上，本文在方法上融合了辩证推理与LLM，在应用上聚焦于不规则采样医疗时间序列的风险预测，在评测上引入了更符合临床需求的推理质量评估。

### Q3: 论文如何解决这个问题？

TRIAGE通过引入辩证推理机制解决LLM在医疗时间序列风险预测中的风险极化问题。核心方法包含两个创新组件：一是推理过程设计，二是两阶段训练流程。

在推理架构上，TRIAGE采用三部分设计。输入表示层将不规则采样的医疗时间序列以变量为中心的格式序列化，拼接任务定义、静态属性和时序观测。结果检查模块针对每个候选结局（如恶化/稳定）分别生成独立的推理链，要求模型在做出最终决策前同时考虑正反两方面证据，避免单边推理。风险估计模块则创新性地在推理链末尾直接输出结局token，而非先给出结论，通过提取该固定位置的logits计算连续风险分数，从而保留梯度化的风险信号而非二值化输出。

训练流程分为两个阶段。第一阶段通过辩证推理监督，使用强LLM为每个候选结局生成条件化推理链（仅包含支持该结局的证据，不提及对立结局），并用这些合成数据微调小模型。第二阶段采用自我精炼，利用GRPO算法对模型自身生成的推理链进行强化学习，其中奖励函数设计为批次级别的对比损失，通过拉大正负样本风险分数的间隔来增强跨患者可比性。最终损失函数结合了决策token的交叉熵损失和推理token的GRPO损失。

### Q4: 论文做了哪些实验？

论文在三个不规律采样的医学时间序列基准数据集（P12、P19和MIMIC-III）上进行了实验。P19任务是预测6小时内脓毒症发作，P12和MIMIC-III任务是院内死亡率预测。对比方法包括GRU-D、mTAND、SeFT、Raindrop、STraTS、ViTST、KEDGN、Hi-Patch等ISMTS基线，以及GPT-5.1和gpt-oss-120b等零样本LLM。主要评估指标包括区分度（AUROC和AUPRC，以AUPRC为主）和校准度（期望校准误差ECE和Brier分数BS）。

主要结果：TRIAGE在强化学习阶段后（TRIAGE_{SFT+RL}）表现最佳，平均排名1.58，在每项指标上均位列第一或第二。与最强基线GRU-D相比，平均AUROC提升0.8%，平均AUPRC提升3.3%。校准方面，TRIAGE_{SFT+RL}将平均ECE降低80%（从约0.19降至0.04以下），平均Brier分数降低49%（从约0.14降至0.08以下）。在变量缺失的鲁棒性测试中（随机遮蔽10%-50%变量），TRIAGE在MIMIC-III上所有遮蔽比例下AUPRC均领先，在P12上与最强基线持平。LLM-as-a-judge评估显示，TRIAGE的推理质量比基线的事后解释高出20%。

### Q5: 有什么可以进一步探索的点？

论文的局限性首先在于仅针对二分类任务，未来可扩展至多分类或多标签临床场景，例如同时预测多种并发症。其次，LLM推理链的高计算成本限制了低延迟场景的应用，可探索轻量级推理蒸馏或混合架构，将LLM作为“慢思考”模块仅在关键时间步激活。第三，LLM-as-a-judge评估存在模型偏差，需引入临床专家标注的黄金标准数据集，或开发结合医学知识图谱的自动化评估指标。最后，生成推理的准确性存疑，可设计对抗性验证机制，通过对比真实临床决策路径来检测逻辑漏洞。此外，当前框架未充分利用时间序列的时序结构，可引入时间注意力机制或神经微分方程来显式建模不规则采样模式，使LLM的推理更贴合生理动态变化。

### Q6: 总结一下论文的主要内容

TRIAGE提出了一种基于辩证推理的框架，用于对不规则采样的医学时间序列进行可解释风险预测。核心问题在于现有LLM在临床早期预警中会将分级风险退化为过度自信的二元预测，导致校准失效和跨患者可比性下降。该方法通过训练LLM对竞争性临床结局生成特定理由的辩证推理，从而缓解风险极化，使单个LLM能输出基于明确临床推理的连续风险分数。在三个ISMTS基准上，TRIAGE平均AUPRC提升3.3%，校准误差降低81%，且临床推理质量比事后解释方法提升20%。主要结论表明，通过辩证推理监督和自精炼，小型开源LLM能同时实现高性能预测和可解释性，为LLM临床决策支持提供了预测性能与可解释性协同发展的新路径。
