---
title: "PersonaAgent: Retrieval-Augmented Transaction Anomaly Scoring with Refreshable Multi-Entity Persona Memory"
authors:
  - "Zhengyu Fang"
  - "Liang Wang"
  - "Yingtong Dou"
  - "Yuzhong Chen"
  - "Shubham Jain"
  - "Junpeng Wang"
  - "Xiran Fan"
  - "Menghai Pan"
  - "Jiarui Sun"
  - "Yan Zheng"
  - "Yiwei Cai"
date: "2026-11-05"
arxiv_id: "2611.08094"
arxiv_url: "https://arxiv.org/abs/2611.08094"
pdf_url: "https://arxiv.org/pdf/2611.08094v1"
categories:
  - "cs.LG"
tags:
  - "Agentic Anomaly Detection"
  - "Transaction Anomaly Detection"
  - "Refreshable Memory"
  - "Retrieval-Augmented Scoring"
  - "Persona Memory"
  - "Industrial Deployment"
  - "Payment Networks"
  - "Entity Behavior Signals"
relevance_score: 7.5
---

# PersonaAgent: Retrieval-Augmented Transaction Anomaly Scoring with Refreshable Multi-Entity Persona Memory

## 原始摘要

In large-scale payment networks, entities (card, merchant, etc.) and their interactions play a key role in transaction anomaly detection. However, transaction patterns between different entities usually change more frequently than the production model refresh schedule. Meanwhile, entity embedding tables suffer from high-cardinality and sparse interaction issues. To resolve the above challenges, we present PersonaAgent, an agentic transaction anomaly detection framework which represents the latest entity behavior signals as personas and saves them in a refreshable memory. Offline, a weekly scheduled batch job is used to extract the latest behavior signals and update them in the memory. At inference time, a lightweight adapter retrieves the corresponding entity behavior signals of each transaction from memory and uses them to augment the base anomaly classifier's scoring. Through comprehensive benchmarking with different anomaly detection models at Visa, PersonaAgent is able to score transactions efficiently (a 1,000-transaction CPU batch in 1-2 ms), lifting the PR-AUC by 0.65-6.58% and the production business metric by 8.93-14.24% relatively in deployment.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于大规模支付网络中的交易异常检测问题。研究背景是：在Visa这类覆盖数十亿凭证、上亿商户、年交易量达数千亿笔的系统中，异常检测模型（detector）需要在高延迟约束下对每笔授权交易打分，而异常样本稀少、概念漂移频繁、标签延迟严重。现有方法存在明显不足：工业级检测器体量大，每次发布需集成与验证，更新周期通常长达数月；但实体（卡、商户等）的交易行为漂移却快得多，可每周重新估计，导致部署模型参数中编码的知识滞后，形成"知识延迟差"。此外，实体嵌入表面临高基数与交互稀疏问题，对稀有实体、MCC–Location等实体组合乃至未见ID提供的证据有限；语义初始化虽能丰富嵌入，但仍属于模型权重，更新仍需重新发布。特征存储只提供单实体聚合，未回答"哪些行为信号能描述实体"以及"行为相似的实体如何分组以让长尾实体借用群体证据"；手写规则难以覆盖数百万商户、800+ MCC与230+ Location码，纯数值聚类则按数值相似而非行为语义分组。LLM智能体虽可离线完成这些设计，但在线逐笔调用LLM会把文本生成放到延迟关键路径上。因此，本文要解决的核心问题是：如何在不改变已冻结检测器权重、不在线调用LLM的前提下，将可独立刷新的多实体行为证据注入检测流程，弥合知识延迟差，提升异常打分效果。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类。方法类方面，交易表示学习包括交易基础模型与序列表格Transformer从事件历史学习时序表示，图模型与实体/同类群嵌入表编码关系，支付网络研究引入商户历史，LLM句嵌入可初始化实体嵌入；异常检测研究关注极端类别不平衡下的金融数据与通用时间序列异常、标签延迟及缺失/漂移观测下的预测与插补。PersonaAgent与高基数类别属性的层次平滑相关，但通过行为主题聚合低交易量商户证据、最小支持度分组及MCC-主题父级回退来处理冷启动商户。检索增强评分方面，RAG将输出锚定于外部文档，表格检索用近邻行作为上下文，BRIGHT将实体嵌入批计算与实时预测分离，后验校准仅用模型输出对齐结果率；PersonaAgent则从共享可刷新多实体记忆检索数值行为上下文，经轻量适配器与冻结检测器分数结合，采用确定性键查找与预定义回退，无需相似度搜索或生成，且记忆与适配器作为版本化包独立于检测器权重更新。Agentic设计方面，LLM优化器改进指令与结构化流水线，CAAFE仅保留提升验证性能的特征，FeatLLM离线构造特征，LLM可诱导可解释主题或分配检索标签，LLM智能体用于时间序列预测，TimeEvo将诊断失败转化为新工具并需配对验证；PersonaAgent在设计时迭代精炼persona协议，由提议角色与Protocol Critic诊断候选，采用有界协议自演化并以预设开发规则（开发集BM1提升且检查通过）决定接受，从而决定共享版本化多实体记忆的构建与多检测器使用方式。

### Q3: 论文如何解决这个问题？

论文提出 PersonaAgent 框架，将实体行为信号抽象为“persona”并存入可刷新的语义记忆，从而在不改动生产检测器的前提下提升异常评分。整体分为设计、周更、打分三阶段。

设计阶段采用 agentic persona-protocol 自演化：由 LLM 扮演信号定义、叙事模式、主题规则、协议批评者四个角色，迭代提出候选协议，每个候选协议重建记忆并训练临时适配器，在独立开发集上按固定规则择优，最终冻结协议与执行配置。协议包含五部分：行为信号、叙事模式、主题构建、检索规则与发布检查。主题构建结合叙事嵌入与行为特征聚类，形成 56 个商户主题、19 个 MCC 主题、9 个地理位置主题及最多 171 个 MCC–Location 交互主题，显著压缩了高基数稀疏键空间。

周更阶段由批处理作业按冻结协议，从截止时点前的合规历史重算五类数值视图（卡消费摘要、商户主题、MCC 主题、位置主题、交互视图），生成带版本号的记忆快照，经兼容性校验后与适配器打包发布；该阶段不调用 LLM，打分完全确定性。

打分阶段，轻量适配器按精确键检索每条交易对应的五条数值记录（含支持度、回退层级等可靠性指标），与基础分数和元数据输入拼接成定长 persona 特征向量，经树模型和小型神经网络输出最终分数；商户无映射或历史不足时按预定义规则回退到更大主题记录。创新点在于可刷新多实体 persona 记忆、LLM 仅用于设计期的自演化协议，以及检测器无关的轻量适配器，实现 1000 笔 CPU 批量 1–2 ms 的高效打分。

### Q4: 论文做了哪些实验？

论文在Visa真实支付数据上开展了全面实验。设置上分为两个评估期：Period 1为离线留出测试集，Period 2为部署期实时打分（结果事后回填），记忆快照与四个适配器在两期之间保持冻结，以检验记忆老化下的增益持续性。基准为四个已冻结的现有异常检测器（Detector 1–4），对比对象是各检测器自身的冻结基础分数，指标包括业务指标BM1、PR-AUC和AUC，并采用配对bootstrap给出95%置信区间。主要结果：全部24个检测器–时期–指标比较均显示提升，且置信区间均高于零；部署期BM1相对提升8.93%–14.24%，PR-AUC提升0.65%–6.58%，AUC提升0.23%–0.66%，其中Detector 2在BM1上增益最大（+20.08%/+14.24%）。效率上，1000笔交易的CPU批处理仅需1–2 ms。消融实验表明：仅用基础分数时适配器无增益；加入五个persona视图后PR-AUC与AUC平均再提升3.20和0.44个百分点，八个检测器–时期组合全部上升。单视图预测中消费行为摘要最强，语义主题在三个分组视图上优于传统聚类（MCC +0.26、Merchant +0.19、交互视图 +0.14）。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于：persona 记忆依赖每周离线批更新，实体行为在周内发生突变（如盗卡集中攻击、商户突发异常）时存在滞后；persona 以行为信号摘要形式存储，缺乏对时序演化与跨实体关系（如卡—商户团伙）的显式建模；轻量 adapter 仅做检索增强打分，未形成闭环反馈来验证记忆质量。未来可探索：1）事件驱动的增量记忆刷新，结合流式检测触发局部 persona 重算，缩短更新延迟；2）引入时序图或记忆网络刻画实体间交互演化，而非孤立 persona；3）设计记忆可信度与遗忘机制，对漂移或噪声 persona 降权；4）让 agent 具备主动查询与反事实推理能力，在低置信交易上触发二次检索；5）研究 persona 的可解释输出与人工反馈闭环，并评估在概念漂移与对抗攻击下的鲁棒性。

### Q6: 总结一下论文的主要内容

论文针对大规模支付网络中实体行为漂移快于检测模型更新周期所产生的“知识延迟差”问题，提出 PersonaAgent 框架。其核心思路是将卡片、商户、MCC、位置及交互等多实体行为信号表示为可审计的“人格”记录，存入可刷新的语义人格记忆，从而在不改动冻结检测器参数的前提下注入最新行为证据。方法上，LLM 智能体仅在离线设计阶段通过多角色自演化搜索人格协议，确定行为信号、叙事模式与语义主题划分；每周批处理按冻结协议刷新数值记忆，在线评分时轻量适配器通过精确键检索五类人格视图，并与检测器基础分数融合输出最终分数，全程不调用 LLM。在 Visa 四个冻结检测器上的离线测试与上线部署表明，该方法每千笔交易 CPU 批处理仅需 1–2 ms，PR-AUC 相对提升 0.65–6.58%，生产业务指标相对提升 8.93–14.24%，且语义主题优于传统聚类，验证了可刷新多实体记忆对缓解知识延迟的有效性。
