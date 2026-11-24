---
title: "Pain Reassessment from Pulse Waveforms with Language Model Explanations"
authors:
  - "Cheng Ding"
  - "Jiaming Liu"
  - "Daoqiang Zhang"
date: "2026-11-22"
arxiv_id: "2611.29128"
arxiv_url: "https://arxiv.org/abs/2611.29128"
pdf_url: "https://arxiv.org/pdf/2611.29128v1"
categories:
  - "cs.LG"
tags:
  - "LLM解释生成"
  - "生理信号分析"
  - "证据链接"
  - "临床决策支持"
  - "纵向时序建模"
  - "可解释性"
  - "医疗健康"
relevance_score: 7.5
---

# Pain Reassessment from Pulse Waveforms with Language Model Explanations

## 原始摘要

Routine photoplethysmography (PPG) offers a continuous physiological signal for pain reassessment between self-reports. Whether prior recordings provide an individualized physiological reference beyond care-process timing remains unresolved. Across 52,082 report-linked assessments from 21,514 patients in MIMIC-III critical care and MC-MED emergency care, we evaluate a workflow that pairs longitudinal PPG representations with local evidence-linked language interpretation. Among 27 methods, source-selected full-history models achieved average precision of 0.824 from critical to emergency care and 0.822 in reverse. Removing historical pulse-run representations while retaining reassessment availability and elapsed time lowered critical-to-emergency four-hour within-patient concordance from 0.718 to 0.534. This comparison supports the contribution of prior pulse-run representations to within-patient ordering beyond timing cues. Across 2,905 test patients, a local Qwen model interpreting frozen predictions achieved a 94.7% patient-equal pass rate on automated evidence checks after at most one revision. Longitudinal pulse context and evidence-linked language interpretation support a patient-centred workflow for pain reassessment.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决疼痛再评估中的核心难题：如何利用常规监护产生的纵向光电容积脉搏波（PPG）信号，在患者两次自我报告之间判断其疼痛状态是否发生变化，并为这一判断提供可解释的临床证据。

研究背景方面，疼痛包含感觉与情绪成分，患者自报是评估核心，但自报是间歇性的；而常规监护仪持续记录PPG，该信号反映外周血容量变化并受呼吸、交感活动和体温调节影响，具备用于纵向评估的潜力。现有方法的不足体现在两点：其一，跨患者的生理情感识别只能评估“识别”能力，无法满足临床再评估所需的“个体内排序”比较；其二，临床病史中同时记录了观察过程本身，参考记录是否可得、间隔时间长短等护理流程线索本身就可能携带预测信息，因此以往研究难以厘清先前的脉搏内容是否在时间线索之外提供了额外信息。此外，生理评分还需要与个体评估相绑定的解释，而分数变化可能与决策不变并存，参考缺失时也无法进行时间比较。

因此，本文要解决的核心问题是：在控制再评估可得性与间隔时间等流程线索的条件下，检验既往脉搏波形表征是否能为患者内疼痛与无痛观察的排序提供超越时间线索的增量信息，并进一步构建一个将固定预测与证据关联的语言解释相结合、以患者为中心的可解释再评估工作流。

### Q2: 有哪些相关研究？

本文的相关工作可分为四类。方法类：pyPPG通过脉搏关键点提取可解释的时序与形态特征；Pulse-PPG从连续记录中学习波形表示；Cross Reconstruction Transformer以自监督重建学习时序—频谱结构；CHEER实现从丰富通道到精简通道的信息迁移；GRU-D利用掩码与时间间隔建模临床记录中的信息性缺失；Sun等采用排序损失进行早期时序分类。应用类：SenseEmotion、PainFormer在实验诱发疼痛下融合生理与行为信号；Lim等比较术前无痛与术后中重度疼痛记录；Fang等基于MIMIC-III生理测量建模疼痛；Ryu等用PPG形态结合XGBoost评估围术期疼痛；Seok等融合EEG、PPG、ECG与面部温度区分慢性疼痛患者。评测类：FActScore评估单条事实主张的支持度，SourceCheckup分别评估医学来源有效性与陈述支持度；Zech等考察影像模型跨院迁移；Amidei等用GPT-4解读纤维肌痛叙述，Almanac检索临床参考资料；MedCPT与BioLinkBERT作为非生成式问题路由对照。区别在于：本文聚焦常规再评估中同一患者相邻报告的排序，保留报告时序与各库定义，并在相同评估上对比完整与精简历史，以隔离既往脉搏内容相对“参考可得性与时间”的独立贡献，同时用本地语言模型对冻结预测生成证据关联解释。

### Q3: 论文如何解决这个问题？

论文的核心方法是构建一个“纵向脉搏波形表示 + 本地证据关联语言解释”的疼痛再评估工作流。整体框架分三层：第一层是输入构造，对每次评估取当前脉搏窗口，并从同一患者、同一次就诊、同一数据划分中选取时间间隔在60秒至14400秒内的最近一次合格记录作为个体化生理参照；参照选择不使用先前疼痛值，因此任一报告状态均可作为前序记录。第二层是预测建模，比较了27种方法，包括仅用当前pyPPG生物标志物的逻辑回归、CatBoost、TabM，保留逐搏信息的均值与注意力多实例模型，以及基于Pulse-PPG冻结编码器和PainFormer图像编码器的波形表示模型。最终在源验证上选出的两个模型均采用运行级输入：每个评估槽包含标准化嵌入、可用性向量、相对中点、归一化时长和槽存在标志，拼接三个槽得到当前向量，再与参照向量、参照可用性及对数时间间隔拼接为3098维输入。第三层是解释生成，使用本地Qwen模型对冻结预测进行证据关联的语言解释，并在自动证据检查下允许至多一次修订。创新点在于：用同一患者的历史脉搏运行表示提供超越时间线索的个体化参照，通过去除历史表示的消融实验证明其贡献；采用患者等权加权和源验证冻结规则，避免频繁评估患者主导；将预测与可核验的语言解释配对，形成以患者为中心的再评估工作流。

### Q4: 论文做了哪些实验？

论文在MIMIC-III v1.4重症监护和MC-MED急诊两个数据库上开展实验，共纳入21,514名患者的52,082条与疼痛报告关联的评估（MIMIC 19,147条、MC-MED 32,935条），按患者划分训练/验证/测试集。任务为二分类识别是否存在疼痛自报。对比方法共27种，包括仅用当前pyPPG生物标志物的逻辑回归、CatBoost、TabM及均值/注意力多实例模型、排序变体，使用历史参考特征的专家模型，Pulse-PPG编码器与逻辑探针、PainFormer图像编码器适配等波形模型，以及仅用历史可用性和间隔时间的WorkflowLR，并做固定平均、约束堆叠和专家组消融。主要结果：源验证选出的全历史模型跨库平均精度（AP）为0.824（重症到急诊）和0.822（反向）；去除历史脉搏段表征但保留重评可用性与间隔时间后，重症到急诊四小时内患者内一致性从0.718降至0.534，说明历史脉搏表征在时间线索之外仍有贡献。在2,905名测试患者上，本地Qwen模型解释冻结预测，经至多一次修订后自动证据检查的患者等权通过率达94.7%。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有四点。其一，历史参考仅取最近一次合格记录且限定60秒至4小时窗口，未探索更长病程、多次历史或多模态（生命体征、用药、护理记录）融合，可研究不规则时间序列的注意力聚合与缺失感知建模。其二，研究为回顾性、跨库外部验证，标签依赖自报疼痛这一噪声较大的二值终点，缺乏前瞻性干预试验验证临床效用，未来可设计疼痛再评估触发的前瞻性研究并引入连续疼痛评分。其三，语言解释仅用本地Qwen模型做证据一致性自动检查，未评估临床医生可读性与信任度，也未与预测不确定性联动，可探索解释忠实度、反事实解释及人机协同评估。其四，模型在源域选型后冻结迁移，跨中心分布偏移仅靠z-score与固定阈值处理，可引入域自适应、个体化校准与在线更新，并分析不同肤色、灌注状态下的公平性。

### Q6: 总结一下论文的主要内容

论文针对常规光电容积脉搏波（PPG）能否在两次自报疼痛之间提供个体化生理参照这一问题展开研究。作者基于MIMIC-III重症监护与MC-MED急诊共21,514名患者的52,082次报告关联评估，提出将纵向PPG表征与局部证据关联的语言解释相结合的工作流。方法上，从27种方法中选出全历史模型，在跨场景迁移中平均精度达0.824和0.822；控制实验显示，去除历史脉搏片段表征后，四小时内患者内一致性从0.718降至0.534，说明历史脉搏信息超越时间线索对个体内排序有贡献。解释环节使用本地Qwen模型解读冻结预测，在2,905名测试患者上经至多一次修订即达到94.7%的自动化证据检查通过率。结论表明，纵向脉搏上下文与证据关联的语言解释可支持以患者为中心的疼痛再评估流程。
