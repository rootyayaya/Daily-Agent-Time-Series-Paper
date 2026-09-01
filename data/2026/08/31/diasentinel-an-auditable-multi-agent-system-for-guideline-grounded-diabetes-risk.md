---
title: "DIASENTINEL: An Auditable Multi-Agent System for Guideline-Grounded Diabetes Risk Screening"
authors:
  - "Yung Wei Shueh"
  - "Zhi-Jie Chen"
  - "Chia-Hsuan Hsu"
  - "Hsin-Ling Hsu"
  - "Donghua Zhang"
  - "Chenwei Wu"
  - "Jun-En Ding"
  - "Tongze Zhang"
  - "Shihao Yang"
  - "Pengfei Hu"
  - "Fang-Ming Hung"
  - "Feng Liu"
date: "2026-08-31"
arxiv_id: "2608.31128"
arxiv_url: "https://arxiv.org/abs/2608.31128"
pdf_url: "https://arxiv.org/pdf/2608.31128v1"
categories:
  - "cs.CL"
tags:
  - "multi-agent system"
  - "guideline-grounded report generation"
  - "verification layer"
  - "clinical decision support"
  - "EHR"
  - "risk screening"
  - "LLM entailment"
  - "auditable system"
  - "RAG"
  - "citation"
relevance_score: 6.5
---

# DIASENTINEL: An Auditable Multi-Agent System for Guideline-Grounded Diabetes Risk Screening

## 原始摘要

Large language models (LLMs) offer promising clinical decision support but remain vulnerable to hallucinated facts, unsupported recommendations, and citation errors. We present DIASENTINEL, a fully on-premise multi-agent system for one-year type 2 diabetes mellitus (T2DM) risk screening and guideline-grounded report generation from electronic health records (EHRs). The system integrates calibrated risk prediction, deterministic clinical signal extraction, Reciprocal Rank Fusion over American Diabetes Association (ADA) guidelines, and a hybrid verification layer combining rule-based checks with LLM entailment. The demonstration provides a real-time batch-screening dashboard and an interactive patient report interface with cited recommendations, verification results, and raw EHR comparison. DIASENTINEL demonstrates a practical framework for reliable, auditable, and privacy-preserving LLM-based clinical decision support.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

糖尿病（T2DM）是全球高发慢性病，早期识别高风险人群对预防疾病至关重要。现有基于电子健康档案（EHR）的LLM临床决策支持系统虽取得进展，但存在三大核心缺陷：一是模型预测概率校准不良，无法真实反映疾病发病率；二是LLM可能产生幻觉，编造无依据的实验室数值或临床建议；三是检索增强生成（RAG）存在引用漂移，将有效建议错误关联到不相关来源。这些问题严重削弱了系统的可解释性、可验证性和临床可靠性。

为此，本文提出DIASENTINEL——一个完全本地部署的多智能体系统，用于一年期T2DM风险筛查和基于指南的报告生成。系统通过校准的LLM风险预测器、确定性临床信号提取、基于ADA指南的倒数排名融合检索，以及结合规则检查与LLM蕴含判断的混合验证层，将诊断流程分解为可审计、有证据依据的子任务。其核心目标是构建一个可靠、可审计且保护隐私的临床决策支持框架，确保每条建议都有据可查、可追溯，从而解决LLM在医疗应用中幻觉与引用错误的关键问题。

### Q2: 有哪些相关研究？

DIASENTINEL的相关研究主要可分为以下几类：

**方法类**：一是基于LLM的临床风险预测，如利用LoRA微调Qwen等模型进行疾病风险分层，本文与其区别在于显式进行了概率校准，使预测概率与真实发病率对齐；二是RAG在医学中的应用，现有工作多采用单一检索或重排序，本文提出两阶段检索（稠密检索+交叉编码器重排序）并通过RRF融合，解决了重排序器单独使用时的长度偏差问题。

**应用类**：包括基于EHR的糖尿病风险筛查系统，如利用传统机器学习或深度学习模型预测T2DM发病风险，本文的差异在于构建了端到端的多智能体系统，将风险预测、指南检索、报告生成和验证分解为可审计的子任务；此外还有临床决策支持系统，但多数缺乏可验证性和引用溯源机制。

**评测类**：针对LLM幻觉和引用漂移的检测方法，如基于规则或NLI的验证技术，本文创新性地将四种确定性检查与LLM蕴含检查结合，形成混合验证层，对报告中的事实一致性、无依据内容和引用错误进行系统审计。

与这些工作相比，DIASENTINEL的核心贡献在于将校准预测、确定性信号提取、混合验证和完全本地化部署整合为一个实用的临床工作流，强调可审计性和隐私保护，而不仅是算法性能提升。

### Q3: 论文如何解决这个问题？

DIASENTINEL通过一个完全本地部署的多智能体系统来解决LLM在临床决策支持中的幻觉、无依据推荐和引用错误问题。整体架构基于LangGraph编排，将人口级批量筛查与患者级报告生成分离，核心设计原则是仅将预测、报告合成和语义验证交给LLM，而EHR检索、事实提取、数值比较和证据检索保持确定性。

系统包含五个关键模块：**风险函数**使用LoRA微调的Qwen2.5-14B模型，通过softmax将token级对数概率转换为原始风险估计，并经Platt缩放校准，生成一致的一年T2DM风险评分；**解释代理**通过六条确定性阈值规则（覆盖HbA1c、空腹血糖、BMI、血压、LDL和代谢综合征脂质模式）提取临床可解释的风险信号；**趋势代理**在365天窗口内比较变量最早与最新值，使用变量特异性噪声容限带生成趋势标签，并输出结构化事实和自然语言摘要供合成器逐字复用；**证据代理**从ADA糖尿病诊疗标准构建本地检索语料库，将指南分割为382个区块，用bge-m3嵌入、bge-reranker-v2-m3重排序，再通过RRF融合两种排序结果；**合成器**生成五部分临床报告，每条推荐显式绑定来源、章节和页码元数据，无依据陈述则渲染为通用非引用指导。

创新点在于混合验证层：四个确定性检查确保报告与风险评分、EHR数值、纵向发现和指南引用的一致性，外加一个LLM蕴含检查验证推荐是否被检索到的指南段落语义支持。验证代理严格只读注释，将所有结果记录到追加式JSONL审计日志中，不修改生成报告，保障了透明性和临床医生最终权威。

### Q4: 论文做了哪些实验？

论文围绕DIASENTINEL系统开展了三方面实验。**风险预测与分层**方面，采用严格验证/测试划分（测试集N=2,491），使用Platt缩放校准（a=1.0049, b=-1.5693），报告AUROC、AUPRC、Brier分数及阈值指标。结果显示AUROC为0.737（95%CI: 0.694-0.773），Brier分数0.054；默认阈值（p=0.5）下准确率0.8212、敏感性0.4733、特异性0.8434、NPV 0.9615。高风险阈值（p≥0.056）实现72%敏感性和62%特异性，分层校准显示各层预测概率与观测发病率高度一致（如高风险层0.115 vs 0.117）。与基线对比中，DIASENTINEL的AUROC（0.737）优于逻辑回归（0.697）且与XGBoost（0.731）相当，但AUPRC（0.146）低于XGBoost（0.211）。

**指南检索**方面，构建50题评估集（5类查询，Cohen's κ=0.76），对比三种检索策略。RRF融合策略在Recall@5（0.745）、MRR（0.672）和Chapter@5（0.939）上均最优。

**验证可靠性**方面，对4种确定性检查各构造3个注入错误和3个干净案例，共24例实现100%敏感性和100%特异性；LLM蕴含检查在40对证据对上达到80%敏感性和100%特异性，且温度=0时三次运行结果完全一致。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在验证深度和泛化能力上。当前系统仅展示了技术框架，缺乏大规模临床前瞻性验证，且风险预测模型可能受限于特定人群的EHR数据质量与偏倚。未来可探索多中心外部验证，并引入时间序列动态特征（如血糖波动轨迹）以提升预测精度。在可解释性方面，虽然采用混合验证层，但LLM的蕴含判断仍可能产生逻辑漏洞，可考虑引入因果推理图或结构化医学知识图谱来增强规则与语义的交叉校验。此外，多智能体间的协作机制目前较为固定，可探索自适应任务分配与动态路由策略，例如根据患者风险分层动态调用不同专家模块。最后，隐私保护虽采用本地部署，但联邦学习框架可进一步实现跨机构协同训练而不共享原始数据，同时需评估系统在真实临床工作流中的医生接受度与决策时效性。

### Q6: 总结一下论文的主要内容

DIASENTINEL是一个完全本地部署的多智能体系统，用于从电子健康记录中进行一年期2型糖尿病风险筛查和基于指南的报告生成。该系统整合了校准的风险预测、确定性临床信号提取、基于美国糖尿病协会指南的倒数排名融合检索，以及结合规则检查与LLM蕴含判断的混合验证层。其核心贡献在于解决LLM在临床决策支持中的幻觉、无依据建议和引用错误问题，通过实时批量筛查仪表板和交互式患者报告界面，提供带引用的建议、验证结果和原始EHR对比。该系统展示了在保护患者隐私的前提下，构建可靠、可审计的LLM临床决策支持框架的实用方法，显著提升了透明度和可信度。
