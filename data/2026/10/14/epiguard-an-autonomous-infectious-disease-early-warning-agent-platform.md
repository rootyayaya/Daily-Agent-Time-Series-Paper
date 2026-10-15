---
title: "EpiGuard: An Autonomous Infectious-Disease Early Warning Agent Platform"
authors:
  - "Tonglong Wei"
  - "Zheng Yuan"
  - "Lingshuai Lin"
  - "Yuhui Yao"
  - "Xing Xie"
  - "Na Zou"
date: "2026-10-14"
arxiv_id: "2610.19396"
arxiv_url: "https://arxiv.org/abs/2610.19396"
pdf_url: "https://arxiv.org/pdf/2610.19396v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Autonomous Early Warning"
  - "Epidemic Forecasting"
  - "Evidence Routing"
  - "Self-Improving Agent"
  - "Reusable SOP"
  - "Multi-Source Surveillance"
  - "Data Availability Regimes"
  - "LLM/Agent Workflow"
  - "Time Series Forecasting"
relevance_score: 6.5
---

# EpiGuard: An Autonomous Infectious-Disease Early Warning Agent Platform

## 原始摘要

Infectious disease outbreaks often spread rapidly before signs of widespread transmission become apparent, leaving a big challenge for rapid response and effective intervention. However, current infectious-disease early-warning systems face three major challenges: fragmented epidemiological evidence across diverse surveillance sources, highly uneven data availability across diseases and geographic regions, and delayed warning procedure caused by manual data collection, analysis, and reporting. To address these challenges, we present EpiGuard, an autonomous, continually self-improving agentic platform for timely and reliable early warning of more than 50 infectious diseases across different regions. EpiGuard proactively monitors and captures newly released official surveillance records, using the latest available evidence for risk assessments. It dynamically adjusts its analytical strategy across three evidence availability regimes, enabling reliable risk assessment under diverse data conditions, ranging from the absence of historical observations to sparse and abundant evidence. Moreover, EpiGuard learns from the successful execution process by preserving effective data-acquisition and analytical procedures as reusable standard operating procedures, enabling it to progressively generalize to previously unseen diseases and regions. We use officially released infectious-disease surveillance data from the China CDC and the United States CDC to evaluate EpiGuard's effectiveness. Experimental results demonstrate that EpiGuard outperforms state-of-the-art forecasting systems, improving forecasting performance by 9.68% and 14.04% on the China CDC and U.S. CDC datasets, respectively.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

传染病暴发往往在广泛传播迹象显现之前就已迅速扩散，给快速响应和有效干预带来巨大挑战。然而，现有传染病早期预警系统面临三大瓶颈：其一，流行病学证据分散于各类监测来源，病例记录、实验室数据、官方通报与开源信息各自独立维护、更新时间不一，难以在预警窗口内汇聚完整且最新的证据；其二，不同疾病和地区的证据可得性极不均衡，常规监测病种拥有多年历史数据，而新发病种或监测薄弱地区可能仅有零星报告甚至无历史观测，单一预测方法难以普适；其三，数据采集、清洗、分析与报告高度依赖人工，导致从疫情信号出现到预警发布的流程严重滞后。针对上述问题，本文提出 EpiGuard——一个自主且持续自我改进的智能体平台，旨在为跨地区 50 余种传染病提供及时可靠的早期预警。其核心在于：主动监测并捕获最新官方监测记录以维护动态证据库；结合 LLM 推理与预测模型池，在证据缺失、稀疏、充足三种机制下自适应配置分析流程；并将成功任务中的有效数据获取与分析流程固化为可复用标准操作程序，实现对新病种和新地区的渐进式泛化。

### Q2: 有哪些相关研究？

本文的相关研究主要可分为三类。方法类方面，传统传染病早期预警系统经历了从法定病例报告、症状监测、统计阈值检测到互联网事件监测和多源流行病学建模的演进。代表性工作包括中国传染病自动预警响应系统，它基于固定阈值和时间序列模型从法定病例报告中生成预警信号；以及HealthMap、GPHIN和ProMED-mail等数字流行病情报系统，通过监测新闻报道、官方公告等开源信息识别新发传染病信号。应用类方面，上述系统已广泛部署于公共卫生监测实践，支持早期 detection 和更可靠的预警。评测类方面，本文使用中国CDC和美国CDC官方发布的监测数据进行评估。与这些工作的关系在于，EpiGuard同样致力于传染病早期预警，并继承了多源证据融合和互联网监测的思路。区别在于：现有系统面临证据碎片化、数据可得性不均和人工流程延迟三大挑战，而EpiGuard通过自主监测、证据自适应规划机制和自改进SOP机制，实现了跨50余种疾病和区域的动态分析，并在中美CDC数据上分别超越最强基线9.68%和14.04%。

### Q3: 论文如何解决这个问题？

EpiGuard 的核心是一个以 Agent 规划与决策中心（APDC）为中枢的闭环自主预警框架，通过 LLM 驱动的规划编排将用户请求、证据获取、自适应分析、风险评估、报告生成与经验积累串联起来。

整体架构包含五个功能组件。用户交互层（UIL）从开放式请求中提取目标疾病与地理区域，形成疾病—区域对，并据此检索对应的标准操作程序（SOP）；系统维护一个按疾病—区域对索引的 SOP 集合，无匹配时则路由至零样本工作流。APDC 作为基于 LLM 的规划与编排组件，接收请求与 SOP 检索结果，将任务分解为可执行动作并组织成自适应分析计划，协调数据获取与处理（DAP）、模型分析与风险判定（MARD）、报告生成（RG）三大组件的调用顺序与中间结果路由。

关键技术有三点。其一，DAP 主动监控多源官方监测数据（如中国 CDC、美国 CDC、WHO FluNet 等），按报告周期主动抓取新发布记录，通过比较与合并操作持续更新流行病学证据库，并以统一表示封装结构化观测、补充信息与元数据，实现证据维护与单次请求解耦。其二，MARD 依据证据可用性动态切换三种机制：无证据时由 LLM 综合权威流行病学信息进行评估，稀疏证据时引入有限观测作为上下文但避免数值预测，证据充足时则从包含 30 多个统计、机器学习、深度学习及预训练时序基础模型的模型池中，基于最近完整观测区间的回顾性误差选择最优模型进行预测，并将结果映射为 OK、WATCH、WARNING、CRITICAL 四级风险。其三，自我改进机制将成功预警任务中有效的数据获取与分析流程保存为可复用 SOP，使系统能逐步泛化到未见过的疾病与区域。

创新点在于：证据自适应分析策略、回顾性模型选择、主动式证据库维护，以及从成功执行中持续积累 SOP 的自改进闭环。

### Q4: 论文做了哪些实验？

论文使用中国CDC和美国CDC官方监测数据构建了两个数据集：China-Infectious Disease（5条呼吸道病原体阳性率序列）和US-Infectious Disease（10种法定传染病病例数序列），均按1周间隔报告，并按6:2:2划分训练、验证和测试集，任务是预测未来4周数值，评价指标为MASE和RMSE。对比方法包括五类端到端预测系统：AutoGluon-TimeSeries、流行病预训练模型CAPE、TimeSeriesScientist智能体、epi4cast加权集成、微调LLM系统Predict NIDs，以及基于DeepSeek V4 Flash和GPT-4o mini的通用LLM基线。主要结果显示，EpiGuard在两个数据集上所有指标均最优，MASE分别为1.38和0.90，RMSE分别为1.42和30.45，较次优模型分别提升9.68%和14.04%；相比直接使用DeepSeek-V4，在美国数据集上提升23.03%。此外，单一时序基础模型对比表明Toto 2.0在中国数据最优、Moirai 2.0在美国数据最优，验证了模型池的必要性；多源信号实验显示加入全国疾病活动和州际航班连通性分别带来16.22%和24.8%的提升。

### Q5: 有什么可以进一步探索的点？

当前工作的局限主要体现在三方面：其一，评估仅依赖中美CDC的官方监测数据，对低资源地区、非正式渠道（如新闻、社交媒体）及动物宿主信号的融合尚未验证；其二，模型池虽能自适应选择，但缺乏对预测不确定性的显式量化与校准，预警阈值决策仍偏启发式；其三，SOP的复用与泛化机制在真正未见病原体上的长期累积效果缺乏纵向验证。未来可探索：引入因果推断与反事实分析，区分相关性信号与真实驱动因素；将流行病学机理模型（如SIR类）与数据驱动智能体结合，形成混合建模范式；构建多模态证据图，纳入基因组测序、气候、人口流动等异构数据；设计人机协同的主动学习回路，让领域专家反馈直接修正SOP；并建立跨区域、跨病原体的标准化评测基准，检验预警的时效性与公平性。

### Q6: 总结一下论文的主要内容

EpiGuard是一个面向传染病早期预警的自主、持续自我改进的智能体平台，旨在解决现有预警系统面临的三重挑战：流行病学证据分散于多源监测系统、不同疾病与地区间数据可用性极不均衡、以及人工采集分析导致的预警延迟。平台以智能体规划与决策中心为核心，协调用户交互、数据获取与处理、模型分析与风险判定、报告生成及自我改进五大模块，形成闭环预警框架。其关键创新在于证据自适应规划机制，结合大语言模型推理与包含30余种模型的预测模型池，在无证据、稀疏证据和充足证据三种情形下动态调整分析流程；同时通过自我改进机制将成功任务中的有效流程固化为可复用标准操作程序，逐步泛化至新疾病与地区。基于中国CDC和美国CDC官方监测数据的实验表明，EpiGuard在两个数据集上分别比最强基线提升9.68%和14.04%，验证了其在多疾病、多地区场景下的有效性与泛化能力。
