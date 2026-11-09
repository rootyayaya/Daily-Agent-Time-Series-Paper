---
title: "Personalized health coaching via coachable health age and counterfactual wearable trajectories"
authors:
  - "Simon A. Lee"
  - "Zeinab Esmaeilpour"
  - "Menglian Zhou"
  - "Marius Guerard"
  - "Sohrab Sidhu"
  - "Alexandru Solot"
  - "Hamid Palangi"
  - "Pramod Rudrapatna"
  - "Ming-Zher Poh"
  - "Max A. Xu"
  - "Daniel McDuff"
  - "Dimitrios Antos"
  - "Yuzhe Yang"
  - "Jeffrey N. Chiang"
  - "Anthony Z. Faranesh"
  - "Lindsey Sunden"
  - "Mark Malhotra"
  - "Shwetak Patel"
  - "A. Ali Heydari"
  - "Ahmed A. Metwally"
date: "2026-11-05"
arxiv_id: "2611.08568"
arxiv_url: "https://arxiv.org/abs/2611.08568"
pdf_url: "https://arxiv.org/pdf/2611.08568v1"
categories:
  - "q-bio.QM"
  - "cs.LG"
tags:
  - "可穿戴传感器"
  - "健康时序"
  - "反事实轨迹预测"
  - "世界模型"
  - "智能体工作流"
  - "个性化健康指导"
  - "可解释健康年龄"
  - "多变量时序预测"
  - "临床安全验证"
relevance_score: 7.5
---

# Personalized health coaching via coachable health age and counterfactual wearable trajectories

## 原始摘要

Personalized health coaching requires moving beyond retrospective wearable summaries toward quantitative, actionable behavioral prescriptions. We introduce Coachable Health Age (CHA), an interpretable health-age metric built from modifiable physiological and behavioral signals passively captured by consumer wearables. Across the WEAR-ME (N=2,780), All of Us (N=22,748), and longitudinal Fitbit (N=1,464) cohorts, CHA aligns with established cardiometabolic health constructs and improves prognostic discrimination for incident cardiovascular and metabolic disease beyond age, sex, and body mass index. To enable prospective behavioral optimization, we developed Sensor World Model (SensorWM), an action-conditioned wearable world model pretrained on over 2.2 million person-weeks of longitudinal sensor data from approximately 100,000 participants. SensorWM accurately forecasts multi-week physiological responses to candidate lifestyle changes ($R^2=0.664$), outperforming generic time-series foundation models while preserving downstream clinical signal for diabetes, hypertension, and other health outcomes. Finally, we integrate CHA and SensorWM into an agentic counterfactual coaching system to synthesize personalized 12-week coaching plans. In blinded paired reviews, certified lifestyle coaches preferred counterfactual-grounded plans over plans grounded in wearable history alone for overall quality (71.4%, P < 0.001) and anticipated adherence (71.0%, P < 0.001), and board-certified clinicians judged 99.2% of counterfactual-grounded plans to meet clinical safety criteria (vs. 97.6% of comparison plans). Automated evaluations across the full cohort (N=2,780) also favored counterfactual-grounded plans. By closing the loop between longitudinal tracking, trajectory prediction, and counterfactual coaching, our framework provides a scalable path to systematically improve cardiometabolic health.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决个性化健康指导中“可行动性”不足的核心问题。研究背景是：全球大量慢性病（尤其心血管代谢疾病）负担可归因于缺乏运动、睡眠不佳、饮食不健康等可改变行为，因此具有可预防性；而消费者可穿戴设备能持续、被动地采集生理与行为信号，为量化健康状态和追踪行为改变提供了数据基础。现有方法存在三方面不足：其一，传统“健康年龄”多通过机器学习从临床生物标志物或可穿戴数据预测实际年龄，或训练于死亡/表型结局，其优化目标是预测年龄或风险，而非“可改变性”，可能依赖固定、难以干预的生理特征，且模型不透明，事后归因只能说明哪些输入影响估计，无法回答“改变行为后健康年龄会如何变化”。其二，现有纵向建模与可穿戴基础模型多为观察性预测，估计的是既有行为模式下的未来，而非在不同行为情景下的反事实轨迹；数字孪生范式也缺乏针对连续行为（活动、睡眠、运动）的动作条件化建模。其三，当前基于大语言模型的健康教练多基于回顾性数据摘要，依赖定性人群经验而非个体化、校准的剂量-反应估计，且缺乏生活方式教练与临床专家的严格评估。因此，本文要解决的核心问题是：构建一个由可解释、可反复测量且可修改信号构成的“可指导健康年龄”（CHA），并耦合动作条件化的可穿戴传感器世界模型（SensorWM）与智能体反事实教练系统，从而在纵向追踪、轨迹预测与反事实指导之间闭环，生成可量化、个性化且临床安全的12周行为指导方案。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类。方法类：一是生物年龄/健康年龄估计，现有方法多用机器学习从临床生物标志物或可穿戴连续数据预测实际年龄，或以死亡率和表型结局训练“第二代时钟”，如“心脏年龄”“体能年龄”；这些方法优化的是风险预测而非可改变性，且多为黑箱，事后归因无法回答“改变行为后指标如何变化”，本文的CHA则基于可解释、可重复测量的可修改信号构建。二是纵向生理建模，包括循环/Transformer模型、大规模可穿戴基础模型及数字孪生范式，但它们多为观察性预测，或针对离散临床治疗序列；本文的SensorWM是动作条件化的可穿戴世界模型，面向活动、睡眠、运动等连续行为场景生成反事实轨迹。应用类：LLM健康教练已能解读可穿戴数据并对话式指导，但通常基于回顾性数据摘要和人群启发式，缺乏个体化剂量反应估计，且易产生无依据建议；本文将LLM教练与显式生理响应模型和可解释结局指标耦合，使建议可追溯至预测健康收益。评测类：近期出现可穿戴教练基准，但少有系统同时经生活方式教练与临床专家严格盲评；本文开展了教练配对盲评与临床安全性评估，并辅以全队列自动评测。

### Q3: 论文如何解决这个问题？

论文提出了一套端到端框架，将可解释健康年龄、动作条件世界模型与智能体反事实教练三者闭环整合。

核心方法分三层。第一，构建 Coachable Health Age（CHA）：选取静息心率、每日步数、睡眠时长、每周活跃区间分钟等可重复测量、可改变的可穿戴信号，利用经共线性校正的流行病学风险比，在对数风险空间中以加法方式映射到 Gompertz 心血管代谢风险曲线，得到年龄等价的健康年龄。其模块化加法结构保证可解释、可扩展，新增 VO₂max、睡眠规律性等信号无需重训练。第二，开发 Sensor World Model（SensorWM）：在约 10 万名参与者、228 万人周的纵向可穿戴数据上预训练的动作条件潜空间世界模型，将生理状态编码到潜空间，并以近期轨迹与行为动作为条件自回归预测未来多周生理响应（R²=0.664），优于通用时间序列基础模型且保留下游临床信号。第三，智能体反事实教练系统：以参与者近期可穿戴历史初始化 SensorWM，模拟不同步数、睡眠、有氧运动方案下的 12 周生理轨迹，映射为 CHA 变化，并用可行性约束优化目标在预期 CHA 下降、个体行为努力惩罚与临床安全边界之间权衡排序，再由 LLM 智能体生成个性化 12 周计划。

创新点在于：以可改变行为锚定心血管代谢结局而非全因死亡，使健康年龄“可教练”；用动作条件世界模型实现前瞻性反事实推演；并将追踪、预测与反事实处方闭环，经盲法专家评审验证计划质量与临床安全性均优于仅基于历史的可穿戴方案。

### Q4: 论文做了哪些实验？

论文围绕CHA与反事实教练框架开展三项关联实验。实验设置与数据集：在WEAR-ME（N=2,780）中评估CHA与改良Life's Essential 8（mod-LE8）、代谢综合征严重度（MSSS）及自报健康的一致性；在纵向Fitbit队列（N=1,464）考察两年内每3个月窗口的个体内可改变性；在All of Us（N=22,748，无病基线18,423，Cox队列14,663）进行前瞻性临床验证。SensorWM在约96,957名参与者、228万人周数据（182,797个12周窗口）上预训练，并在WEAR-ME留出集评估。对比方法包括按时间年龄训练的穿戴设备时钟、LLM直接估计健康年龄、血液PhenoAge及通用时间序列基础模型。主要结果：CHA与mod-LE8相关|r|=0.512、与MSSS相关|r|=0.355，优于PhenoAge（0.406/0.319）和穿戴时钟（0.141/≤0.048）；CHA在年龄、性别、BMI之外提升对高血压、2型糖尿病和心血管疾病的预后判别。SensorWM多周生理响应预测R²=0.664，优于通用基础模型并保留下游临床信号。在盲法配对评审中，认证生活方式教练对反事实方案总体质量偏好71.4%（P<0.001）、预期依从性偏好71.0%（P<0.001）；临床医生判定99.2%反事实方案符合临床安全标准（对照97.6%）；全队列自动化评估亦支持反事实方案。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有四点。其一，CHA仅基于静息心率、步数、睡眠时长和AZM四个可穿戴信号，虽模块化可扩展，但尚未纳入VO₂max、睡眠规律性、胰岛素抵抗等可选信号，未来可系统评估这些扩展对预后判别与"可教练性"的增量贡献。其二，SensorWM的验证以短期（12周）回顾性数据为主，随访跨度有限，长期（数月至数年）反事实轨迹的外推可靠性、以及分布漂移下的稳健性仍待前瞻性验证。其三，专家评估样本较小（5名教练、5名医生），且全队列自动评估依赖LLM评分器，存在与人类判断偏差的风险，需更大规模、多中心的随机对照试验检验真实行为改变与临床终点。其四，框架聚焦心脏代谢健康，对心理健康、肌骨健康等维度覆盖不足。我的改进思路是：引入因果推断与不确定性量化，为反事实建议给出置信区间与安全边界；结合强化学习或闭环自适应策略，根据用户实际依从性动态调整12周计划；并探索多模态（饮食日志、血糖CGM）融合以提升可教练性。

### Q6: 总结一下论文的主要内容

论文针对现有健康年龄指标多为不可改变、黑箱式预测、难以指导行为干预的问题，提出可教练健康年龄（CHA）——一种基于消费级可穿戴设备被动采集的可修改生理与行为信号（静息心率、睡眠时长、步数、活动分钟）构建的可解释健康年龄指标，并按心血管代谢结局的流行病学风险比映射到年龄尺度。在WEAR-ME、All of Us和纵向Fitbit三个队列中，CHA与既有心血管代谢健康评分高度一致，并在年龄、性别、BMI之外提升了对新发高血压、2型糖尿病和心血管疾病的预后判别力，且个体内可在数月尺度上改变。为支持前瞻性行为优化，作者开发了动作条件化的可穿戴传感器世界模型SensorWM，在约10万人、228万人周的纵向数据上预训练，能准确预测多周生理对生活方式改变的反应（R²=0.664）。最后将二者集成为智能体反事实教练系统，生成个性化12周计划；盲评中生活方式教练更偏好反事实计划（71.4%，P<0.001），临床医生判定99.2%符合安全标准。该框架打通了长期追踪、轨迹预测与反事实教练的闭环，为规模化改善心血管代谢健康提供了路径。
