---
title: "HighwayVerse: A Chain-of-Inspection Benchmark for Highway Infrastructure Anomaly Understanding"
authors:
  - "Junyi Yang"
  - "Zheng Si"
  - "Yilin Zhai"
  - "Pengpeng Ouyang"
  - "Hongxi Wang"
  - "Kangze Li"
  - "Mo Chen"
  - "Sicong Zhang"
  - "Hua Wang"
  - "Dongyuan Wu"
  - "Dong Chen"
  - "Mingliang Xu"
date: "2026-11-21"
arxiv_id: "2611.28800"
arxiv_url: "https://arxiv.org/abs/2611.28800"
pdf_url: "https://arxiv.org/pdf/2611.28800v1"
categories:
  - "cs.CV"
  - "cs.AI"
  - "cs.CL"
tags:
  - "多模态大语言模型"
  - "视觉异常检测"
  - "诊断推理链"
  - "检索增强生成"
  - "基础设施巡检"
  - "基准数据集"
  - "可解释诊断"
  - "维护决策"
relevance_score: 7.5
---

# HighwayVerse: A Chain-of-Inspection Benchmark for Highway Infrastructure Anomaly Understanding

## 原始摘要

Practical highway infrastructure inspection entails progressive diagnostic reasoning from visual perception to maintenance decisions, yet existing benchmarks remain confined to isolated tasks, leaving Multimodal Large Language Models (MLLMs) insufficiently evaluated across sequential inspection stages. Meanwhile, current datasets focus primarily on highway pavement defects, falling short of real-world inspection across diverse infrastructure components such as highway pavements, guardrails, glare screens, and drainage systems. To address these gaps, we formulate the Highway Infrastructure Inspection Progression Chain (HIIP-Chain), spanning Anomaly Detection, Anomaly Recognition, Condition Analysis, and Maintenance Resolution, and introduce HighwayVerse. HighwayVerse comprises 14,143 real-world Ground and Unmanned Aerial Vehicle (UAV) inspection records spanning 100 and 17 anomaly categories, respectively, with 84,858 expert-reviewed question-answer pairs. We evaluate 12 open-source and closed-source MLLMs using the chained metric Final, which credits a correct maintenance decision only when all preceding diagnostic stages are completed correctly. Results show that although models achieve relatively high accuracy when initially judging whether an anomaly is present, their markedly lower Final scores expose struggles across downstream recognition, analysis, and decision-making. This discrepancy indicates that current MLLMs do not fully comprehend specific highway anomaly patterns beyond superficial initial judgments. Furthermore, we propose LaneRAG, a training-free retrieval-augmented framework that provides hierarchical reference guidance achieving consistent performance improvements across diverse MLLMs. Our dataset, evaluation benchmark, and source code will be publicly released.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决现有公路基础设施巡检基准无法评估多模态大模型完整诊断推理能力的问题。研究背景方面，实际巡检是一个从视觉感知到养护决策的渐进诊断过程，需要依次完成异常确认、识别定位、状态刻画、风险评估与养护处置，而多模态大模型具备整合视觉感知与领域推理的潜力。现有方法的不足体现在两方面：一是现有基准局限于孤立任务，如RoadBench仅覆盖路面损伤分类与描述，DriveLM、RoadSocial等聚焦目标感知、交通事件分析与驾驶动作规划，均未在诊断前置条件下评估养护决策的正确性；二是数据覆盖的基础设施实体与异常类别有限，地面数据集多集中于路面裂缝与道路障碍物，无人机数据集如RDD2022仅含四类路面病害，远不能满足真实巡检中护栏、防眩屏、排水系统等多样实体的需求。因此，本文的核心问题是：如何构建一个覆盖完整巡检链条、涵盖多视角多类别基础设施异常、并能以链式依赖方式严格评估模型真实理解能力的基准，同时探索无需训练即可提升模型巡检表现的方法。为此作者提出HIIP-Chain评估协议与HighwayVerse基准，并设计LaneRAG检索增强框架。

### Q2: 有哪些相关研究？

现有相关研究可分为三类。方法类方面，传统视觉检测方法及数据集多聚焦裂缝、坑洞、护栏、桥梁或道路障碍物的局部感知；通用MLLM通过视觉编码器与语言模型耦合实现指令跟随，但细粒度判别能力不足，现有补救手段如语言引导视觉精炼、专家定位模块需任务特定训练，大小模型协作、KKA、VISPROG、ViperGPT、MMAD、MuRAG等则分别借助轻量路由、知识生成异常样本、外部工具组合或检索增强来提升能力；上下文示例选择上，Flamingo用视觉相似度，MMICES增加文本重排序。应用与评测类方面，通用多模态基准评估广泛视觉推理，工业基准如MMAD从无监督缺陷检测推进到独立多任务问答；道路场景中RoadBench提供合成道路损伤图文对，DriveLM以图结构QA连接感知、预测与规划，RoadSocial和RoadSceneBench关注交通事件分析与关系语义。区别在于，这些基准对地面与无人机视角下高速公路基础设施覆盖有限，且未在HIIP-Chain诊断前置条件下评估维护决策正确性；HighwayVerse以检测、识别、状态分析、维护决策的渐进链填补该空白，LaneRAG则以离线层次化参考库结合DINOv2与CLIP表征进行路由引导检索，无需更新MLLM参数，区别于扁平相似度匹配。

### Q3: 论文如何解决这个问题？

论文针对现有基准任务割裂、覆盖部件单一的问题，提出以“链式检查”重构评测与增强范式。整体框架上，作者首先形式化高速公路基础设施检查渐进链（HIIP-Chain），将检查拆为异常检测、异常识别、状态分析（定位、描述、风险三问并行）与养护决策四个阶段六个问题，并构建HighwayVerse数据集：14,143条真实地面与无人机巡检记录、100与17个异常类别、84,858条专家审核问答对，覆盖路面、护栏、防眩屏与排水系统。评测上提出链式指标Final，只有上游检测、识别及至少一项状态分析均正确时，养护决策才计分，从而过滤偶然猜对、暴露模型在细粒度识别与决策上的真实短板。方法上提出免训练检索增强框架LaneRAG：离线构建分层参考库，用LLM将细粒度标签聚合为粗粒度部件族，形成两级索引；推理时用冻结的DINOv2与CLIP双编码器拼接归一化视觉嵌入，由轻量MLP路由器预测前二粗类，再按主范围、扩展范围、全局范围检索三张互补参考图（锚定、易混边界、对比负例），与问题一起构成参考条件提示，引导冻结MLLM完成细粒度判别。创新点在于链式评测协议、多部件真实基准与即插即用的分层检索引导。

### Q4: 论文做了哪些实验？

论文在自建的HighwayVerse基准上开展实验，该基准包含14,143条真实公路巡检记录（Ground 971条测试、UAV 963条测试），覆盖100与17类异常，共84,858个专家审核问答对，并按HIIP-Chain协议评估异常检测、识别、状态分析与养护决策四个阶段。实验评测了12个MLLM，包括8个开源模型（Qwen2.5-VL-3B/7B、InternVL3.5-8B、Qwen3-VL-8B/32B、MiniCPM-V4.5、Qwen3.5-9B/27B）和4个闭源模型（GPT-4o、GPT-6.1-Terra、Gemini 2.5 Flash、Grok 4.20 Non-Reasoning），每个模型分别作为基线及搭配免训练检索增强框架LaneRAG进行测试，指标为各阶段链式准确率、Mean与Final。主要结果显示：所有模型在阶段1异常检测准确率较高（如Qwen2.5-VL-3B在UAV达55.87%、Ground达50.26%），但阶段2识别骤降，Overall Final仅19.96%；InternVL3.5-8B从阶段1的逾71%降至Overall Final的33.45%。GPT-6.1-Terra在识别与状态分析阶段显著领先，Overall Final达58.48%。LaneRAG在全部12个模型上均带来提升，Overall Mean平均提升2.15%、Overall Final平均提升2.33%，开源模型提升更大（Final +2.60%，UAV阶段2识别最高+12.35%）。消融实验表明完整LaneRAG在16个设置中均最优或并列最优，UAV阶段2识别较无RAG提升6.99%、Ground提升1.49%。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有以下几点：其一，HIIP-Chain 仅覆盖检测、识别、状态分析、养护决策四阶段，尚未纳入时序演化与多期巡检对比，未来可引入跨时间巡检记录，考察缺陷劣化趋势推理与预测性养护决策。其二，LaneRAG 为免训练检索增强，增益在闭源强模型上有限（Final 平均仅 +1.78%），可探索可训练的检索器或领域微调，让模型内化细粒度异常先验而非依赖外部参考。其三，Ground 视角增益明显弱于 UAV，说明检索库与视角匹配、跨视角知识迁移仍有改进空间，可研究视角对齐的参考库构建与多视角融合。其四，评估以单选项精确匹配为主，缺乏对推理链过程质量与错误传播的细粒度诊断，可引入阶段级错误归因与链式一致性分析。此外，可扩展到更多基础设施部件与真实长尾异常，并探索主动巡检中的不确定性拒答机制。

### Q6: 总结一下论文的主要内容

论文针对现有公路基础设施巡检基准任务割裂、覆盖实体单一的问题，提出HighwayVerse多视角基准。作者首先将真实巡检流程形式化为公路基础设施巡检递进链（HIIP-Chain），涵盖异常检测、异常识别、状态分析（定位、描述、风险评估）与养护决策四个递进阶段，并构建包含14,143条地面与无人机巡检记录、84,858个专家审核问答对的数据集，覆盖100类地面异常与17类无人机异常，且保留真实长尾分布。评测采用链式指标Final，仅当前序诊断全部正确时才计入养护决策得分。对12个开源与闭源多模态大模型的实验表明，模型在异常检测阶段准确率较高，但Final分数显著下降，说明其并未真正理解细粒度异常模式。为此作者提出免训练检索增强框架LaneRAG，通过分层参考库与主、扩展、全局三范围检索提供上下文视觉引导，在全部模型上取得一致提升。
