---
title: "MotionDecipher: LLM-Assisted Clinical Interpretation of Human Motion Signals for Efficient Gait Analysis"
authors:
  - "Mingrui Ma"
  - "Tian Tan"
  - "Jinsi Guo"
  - "Jessica Rose"
  - "Yiwen Dong"
date: "2026-11-05"
arxiv_id: "2611.08795"
arxiv_url: "https://arxiv.org/abs/2611.08795"
pdf_url: "https://arxiv.org/pdf/2611.08795v1"
categories:
  - "cs.HC"
  - "cs.AI"
tags:
  - "LLM-Assisted Clinical Interpretation"
  - "Human Motion Tokenizer"
  - "Structured Representation"
  - "In-Context Learning"
  - "Gait Analysis"
  - "Time Series to Report"
  - "Semantic Gap Bridging"
  - "Clinical Diagnosis"
  - "Motion Signals"
relevance_score: 8.5
---

# MotionDecipher: LLM-Assisted Clinical Interpretation of Human Motion Signals for Efficient Gait Analysis

## 原始摘要

Clinical gait and motion analysis is widely used to guide targeted interventions for patients with neurological disorders, the outcome of which is typically a report with descriptions of joint movements and forces. Current practices rely on experts' manual effort, which is labor-intensive and time-consuming. Recent advancements in Large Language Models (LLMs) provide opportunities to address this problem, but translating human motion into clinical gait descriptions remains challenging because the quality of the context directly affects LLMs' reasoning capability over continuous motion signals. To tackle this, we introduce MotionDecipher, a novel framework bridging the semantic gap between motion data and clinical interpretations. Specifically, we made 3 key advancements: 1) a Human Motion Tokenizer that converts motion signals into domain-specific tokens for time- and frequency-informed gait interpretation; 2) a Meta Feature Selector that transforms tokens into Structured Representations; and 3) a Hybrid Context Constructor to determine the optimal demonstration-based prompt for In-Context Learning. We evaluated MotionDecipher on data collected at an accredited gait lab from 122 patients and 46 controls. Results show that MotionDecipher achieves 0.91 BERTScore (13% over GPT-5), while expert evaluation ranks MotionDecipher highest in Correctness, Completeness, and Conciseness compared to baselines, highlighting its promise for efficient gait analysis.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于临床步态与运动分析报告的自动化生成问题。在临床实践中，步态分析报告需要专家人工解读关节运动与受力等连续波形数据，并将其转写为标准化临床描述，这一过程劳动密集、耗时巨大（约4-6小时/患者），难以规模化。现有AI方法多局限于疾病分类、异常检测或结果预测等离散输出，而近期将LLM与生物力学数据结合的系统也仅支持临床问答或交互式可视化，无法产出具有临床意义的步态描述。直接将原始运动信号输入LLM同样不可靠：模型未经运动信号预训练，难以处理复杂噪声波形，容易生成难以解释、前后不一致甚至错误的输出，在高风险临床场景中不可接受。因此，本文要解决的核心问题是：如何弥合原始连续运动信号与临床步态语言之间的语义鸿沟，使LLM能够稳定生成准确、可解释、符合专家规范的步态描述。为此作者提出MotionDecipher三阶段框架，分别通过人体运动分词器将信号转化为领域特定token、元特征选择器提取关键步态特征并组织为结构化表示、混合上下文构造器检索最优示范构建上下文学习提示，从而在无需额外训练的情况下实现高效、可解释的临床步态解读。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，已有工作将LLM与生物力学数据结合用于临床问答和交互式分析，但输出局限于离散标签、标量估计或交互可视化，而非临床有意义的步态描述；此外，针对步态分析的AI模型多聚焦于疾病分类、异常检测和结果预测等特定任务。应用类方面，LLM已被应用于多模态传感、增强现实和数字健康等场景，但现有模型未经训练处理复杂噪声运动信号，缺乏生成标准化领域步态解读所需的深层推理能力。评测类方面，现有研究多采用BLEU、ROUGE等通用文本指标，缺乏面向步态临床描述的领域专用评测。与上述工作不同，MotionDecipher是首个在真实临床环境中桥接噪声运动信号与可解释步态报告生成的框架，通过Human Motion Tokenizer、Meta Feature Selector和Hybrid Context Constructor三阶段设计，实现从原始时序信号到专家级临床描述的端到端转换，并引入MEDCON-Gait、GaitTripleF1等领域指标及专家评估进行验证。

### Q3: 论文如何解决这个问题？

MotionDecipher 的核心思路是在连续运动信号与 LLM 临床推理之间搭建语义桥梁，整体框架由三个关键组件串联而成。

第一，Human Motion Tokenizer 负责把多变量运动时间序列转成离散、可解释的领域 token。它为每个身体部位（Trunk、Pelvis、Hip、Knee、Ankle 等）生成四类互补编码：Tendency Encoding 用 Savitzky-Golay 平滑一阶导数（窗长 5、二阶多项式）刻画运动趋势并抑制噪声；Comparative Encoding 将每个时刻信号值与 46 名正常对照的 mean±1SD 规范边界比较，经步长 θ=0.5 的区间量化映射为“低于/处于/高于正常范围”的离散 token；Statistical Encoding 先由转折点检测算法识别足跟着地/离地事件并划分支撑、摆动等步态阶段，再提取各阶段与事件的 MAX/MIN/AVG 并填充对齐；Frequency Encoding 用 db4 小波、3 层 DWT 保留低频近似系数重构去噪信号。四类编码沿步态周期拼接，再按身体部位堆叠成 T×C×B 三维张量，兼顾时间、特征与解剖空间三个维度。

第二，Meta Feature Selector 将 token 重组为多个 Meta Feature Vector（MFV），每个 MFV 聚合趋势、步态事件/阶段、身体部位等完整描述所需信息，再用一组由临床专家选择准则形式化的关键词规则集进行直接匹配过滤，剔除对诊断无贡献的冗余细节，最终按解剖区域组织成 Structured Representations。

第三，Hybrid Context Constructor 从步态报告模板数据库（GRTDC）中检索最优示范，构建基于示范的 In-Context Learning 提示，引导 LLM 生成覆盖多身体部位的分层步态分析报告。

创新点在于：以时间—频率—统计—对比四类编码弥合信号与临床语言的语义鸿沟；用规则化元特征选择替代噪声过滤，实现面向临床决策的信息压缩；并以检索式 ICL 提示替代微调，使 LLM 能高效、可解释地输出结构化步态报告。

### Q4: 论文做了哪些实验？

论文在经认证的步态实验室开展真实临床评估，数据采集自2024年1月至2025年7月的122名患者和46名对照者，使用10摄像头光学3D运动捕捉系统（100Hz，Helen Hayes标记集，18+4个反光标记）和测力台（50Hz）采集运动学与动力学数据，每位患者完成10–20次7米步行试验，经Cortex软件与MATLAB脚本预处理、分割步态周期并归一化至0–100%。评估采用定量指标与专家评分相结合：定量上以BERTScore衡量生成临床步态描述的质量，MotionDecipher取得0.91 BERTScore，较GPT-5提升13%；同时在患者年龄与BMI分组上表现出稳健性。专家评估中，由医学专家从Correctness（正确性）、Completeness（完整性）和Conciseness（简洁性）三个维度对生成报告打分，MotionDecipher在所有维度上均排名最高，优于多个基线LLM。实验整体验证了该框架在真实临床场景下的有效性、鲁棒性与临床相关性。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：其一，MotionDecipher 目前仅生成步态报告的第一部分（定量与临床步态描述），尚未覆盖损伤机制关联与循证治疗建议，临床闭环不完整；其二，评估依赖 122 名患者与 46 名对照的单中心数据，跨机构、跨设备（如 IMU、视频）泛化性未验证；其三，Tokenizer 与 Hybrid Index 依赖人工设计的 token 类别与相似度权重，对罕见病理模式可能欠敏感；其四，ICL 演示语料规模有限，检索质量受 GRTDC 覆盖度制约。未来可探索：将框架扩展至完整报告生成并引入机制推理链；结合轻量微调或强化学习替代纯 ICL，提升对长尾异常的鲁棒性；引入不确定性估计与专家回环校验以保障临床安全；并开展多中心、多模态前瞻性验证与读者研究，量化其对治疗决策与患者结局的实际影响。

### Q6: 总结一下论文的主要内容

论文针对临床步态分析报告生成高度依赖专家人工、耗时费力的问题，提出 MotionDecipher 框架，旨在弥合原始运动信号与临床可解释步态描述之间的语义鸿沟。其核心方法包含三部分：一是 Human Motion Tokenizer，将连续运动信号转化为趋势、对比、统计、频率四类领域特定 token，无需额外训练；二是 Meta Feature Selector，依据临床规则筛选关键步态特征并重组为结构化表示；三是 Hybrid Context Constructor，通过联合文本与数值相似度的 Hybrid Index 算法检索最优示例，构建上下文学习提示。研究在 122 名患者和 46 名对照的真实步态实验室数据上评估，MotionDecipher 取得 0.91 BERTScore，较 GPT-5 提升约 13%，并在正确性、完整性和简洁性上获专家最高评价，同时将单患者分析与报告撰写时间从约 4–6 小时缩短至平均 2 分钟，展示了其在高效临床步态分析中的应用潜力。
