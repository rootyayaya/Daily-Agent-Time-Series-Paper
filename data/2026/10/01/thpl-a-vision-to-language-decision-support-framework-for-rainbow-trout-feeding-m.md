---
title: "THPL: A Vision-to-Language Decision Support Framework for Rainbow Trout Feeding Management in RAS"
authors:
  - "Meng Liang"
  - "Guanbo Feng"
  - "Haozhuang Chi"
  - "Shilong Zhao"
  - "Zhixin Xiong"
  - "Yuhang He"
  - "Wenfeng Han"
  - "Tianhao Zhao"
  - "Zhihong Ma"
  - "Ying Liu"
date: "2026-10-01"
arxiv_id: "2610.02378"
arxiv_url: "https://arxiv.org/abs/2610.02378"
pdf_url: "https://arxiv.org/pdf/2610.02378v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Vision-to-Language"
  - "LLM Decision Support"
  - "Precision Aquaculture"
  - "Multimodal DPO"
  - "Hierarchical Behavior Encoder"
  - "Industrial Fault Diagnosis"
relevance_score: 8.5
---

# THPL: A Vision-to-Language Decision Support Framework for Rainbow Trout Feeding Management in RAS

## 原始摘要

In Recirculating Aquaculture Systems (RAS), precision feeding is critical for minimizing costs and improving fish welfare. However, existing methods lack cognitive alignment between fish behaviors and management knowledge, impeding translation into executable, interpretable feeding decisions. To address this, we propose THPL, a generative feeding decision framework tailored for rainbow trout (Oncorhynchus mykiss) in RAS. First, Fishsort extracts trajectories to establish an Activity Coefficient (AC) quantifying feeding intensity. Second, a Hierarchical Behavior Encoder (HBE) models individual temporal progression and collective dynamics using Temporal and Set Transformers, transforming trajectory tensors into dual-evidence representations of explicit physical and implicit soft tokens. Finally, these tokens are integrated with environmental parameters, metadata, and expert rules to fine-tune an LLM via LoRA, followed by counterfactual multimodal Direct Preference Optimization (mDPO) to reinforce causal reasoning. Results show that AC exhibits a statistically significant monotonic positive correlation with expert-annotated feeding intensity (Spearman $ρ= 0.925$, $p < 0.001$). Ablations indicate that decision accuracy improves from 33.33% (text-only baseline) to 93.33% with dual-evidence tokens, confirming that continuous spatiotemporal tokens provide necessary physical grounding for LLMs. Compared with standard LoRA, counterfactual mDPO elevates decision accuracy from 93.33% to 96.67%, advances METEOR from 58.10% to 85.30%, reduces Self-BLEU-2 from 58.79% to 52.88%, and increases Distinct-3 from 6.68% to 7.81%, suppressing templating and actuation biases while reinforcing causal consistency and operational safety. Overall, by integrating continuous kinematics with LLM reasoning, this study provides a novel decision support paradigm for precision aquaculture.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文聚焦于循环水养殖系统（RAS）中虹鳟精准投喂管理的核心难题：现有方法缺乏鱼类行为表征与养殖管理知识之间的认知对齐，导致难以将感知输出转化为可执行、可解释的投喂决策。具体而言，传统投喂决策依赖人工观察或预设时间表，缺乏对鱼群摄食状态的标准化定量描述，容易造成投喂不足或过量，进而升高饲料转化率、恶化水质并损害鱼类福利。尽管计算机视觉已被广泛用于鱼类摄食强度评估，但间接方法（如水面波纹、残饵）与真实摄食行为存在偏差，直接方法（如轨迹运动特征）又受高密度遮挡、目标数量波动和身份切换导致的轨迹碎片化与噪声困扰。更重要的是，现有任务特定模型大多局限于行为量化与状态识别，无法将数值感知输出转化为实际管理决策；而通用大语言模型虽具备推理能力，却无法直接解读连续视频流和鱼群轨迹，且缺乏物理 grounding 易产生幻觉。因此，论文旨在构建一个知识驱动的视觉到语言决策支持框架，统一行为丰富性、物理可解释性与操作安全性，实现精准、安全、可解释的投喂管理。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是鱼类摄食强度评估（FFIA）方法：间接量化通过水面扰动、光反射、溅射波纹和残饵分布等次级表现推断摄食状态，如 Wu 等（2024）基于溅射特征的分类准确率超过 98.22%，但实验室条件下高精度识别与真实摄食行为之间常存在偏差；直接量化则通过任务特定模型提取突然加速、急转弯等运动特征来评估摄食动机（Fuchs & Caudill, 2019; Wei et al., 2021; Gyllingberg et al., 2023），但在高密度 RAS 环境中受遮挡、目标数量波动和身份切换影响，轨迹驱动模型稳定性受限。第二类是跨模态对齐研究：先前工作通过 Querying Transformers（Li et al., 2023）或时间原型重编程（Jin et al., 2024）探索视觉/时序序列与语言模型的对齐，但这些方法主要针对静态视觉特征或规则一维时间序列，难以表征高密度养殖中由目标数量波动、遮挡和身份切换引起的复杂集体动力学。第三类是 LLM 在决策支持中的应用：LLM 具备上下文逻辑推理和多源信息综合能力，但在真实养殖控制中面临物理 grounding、生物约束和操作安全的严格要求，无约束的通用 LLM 易产生事实幻觉或与生产条件不一致的输出。本文在此基础上提出 THPL 框架，通过显式物理证据与隐式软令牌的统一行为到语言接口，结合反事实 mDPO 对齐与专家规则约束，弥补了现有方法在行为丰富性、物理可解释性和操作安全性之间的鸿沟。

### Q3: 论文如何解决这个问题？

论文提出 THPL 框架，包含四个功能层。第一层是任务特定行为感知层（TSM）：利用 Fishsort 对俯视投喂视频进行多目标跟踪，提取连续轨迹并构建时空轨迹张量 X∈ℝ^{B×T×N×F}（T=10 个 0.5 秒时间窗，F=5 个运动通道：归一化质心坐标、平面速度分量和瞬时加速度）。同时计算无量纲活动系数（AC），融合个体位移、游泳速度和加速度的 z-score 标准化均值，并通过训练集全局极值归一化到 [0,1] 区间，再经网格搜索优化阈值将摄食强度分为弱、中、强三档。第二层是分层行为编码器（HBE）：采用 Temporal-then-Set 级联结构，先由个体级 Temporal Transformer 通过多头自注意力捕获游泳动力学和爆发转向运动学，提取实体级表示 H_temp；再由 Set Transformer 通过集合注意力块处理实体维度，生成保持排列等变性的交互令牌 H_set。显式证据头用 M 个可学习查询对 H_set 进行交叉注意力池化，生成显式物理令牌 Z_exp；隐式行为头通过时序-集合双向交叉注意力融合 H_temp 和 H_set，再用 K 个可学习查询池化生成隐式软令牌 Z_soft。两者拼接为双行为前缀嵌入 Z_out∈ℝ^{B×(M+K)×4096}。第三层是提示工程层（PET）：规则引擎根据离线 AC 阈值索引专家控制规则（投喂器状态、投喂间隔、投喂量），提示组合器将水质数值、养殖背景元数据和候选规则格式化为结构化文本提示。第四层是策略决策层：以 Llama-3.1-8B 为基座，通过 LoRA（r=8, α=16）微调，再经反事实多模态直接偏好优化（mDPO）对齐。mDPO 损失包含响应偏好项、行为证据条件偏好项和锚定偏好项，强制模型依赖轨迹证据而非语言先验。训练分三阶段：HBE 行为令牌对齐预训练（复合多任务损失，含分类、属性回归、序数分类、对比对齐、令牌多样性和结构敏感性损失）、多模态监督微调（加权 SFT 损失，弱强度样本权重 2.0）、反事实 mDPO 对齐。推理时确定性输出验证器解析生成文本并校验投喂器状态、间隔和投喂量。

### Q4: 论文做了哪些实验？

实验在余杭智慧水产养殖研究中心进行，78 尾平均体重 65g 的虹鳟置于 1.60m×1.60m RAS 水箱，水温 12°C，pH 8.0，溶解氧>8mg/L。相机距水面 1m 俯拍，20FPS，1280×720 分辨率。共采集 299 个 5 秒视频片段，按时间划分训练集 239 段（第 1-8 天）、验证集 30 段（第 9 天）、测试集 30 段（第 10 天）。对训练集应用物理一致运动学增强（PCKA），生成 2868 个变换视图，构建 3107 个训练实例。实验包括：1）运动学建模与阈值优化：AC_mean 的 ANOVA F=176.88（p<0.001），效应量 η²=0.9291，优于方差和能量公式；AC 与专家标注摄食强度呈显著单调正相关（Spearman ρ=0.925, p<0.001；Kendall τ=0.804），Jonckheere-Terpstra 趋势检验 z=17.79（p<0.001）；最优阈值 [0.00,0.181] 弱、(0.181,0.462] 中、(0.462,1.00] 强，分类准确率 95.32%（macro-F1=95.43%），五折交叉验证泛化准确率 94.31%。2）HBE 架构消融：Temporal-then-Set 结构准确率 97.0%、F1=0.967；Set-Only 和 Set-then-Temporal 仅 33.5% 和 33.4%；Temporal-Only 90.2%。3）扰动鲁棒性：轻微扰动保持 100% 决策一致性，最大空间高斯抖动降至 66.7%，70% 帧丢失保持 90.0%，轨迹输入置零后一致性崩溃至 33.3%（与纯文本基线持平）。4）决策性能：纯文本基线准确率 33.33%，加入双证据行为令牌后提升至 93.33%；反事实 mDPO 进一步将准确率提升至 96.67%，METEOR 从 58.10% 提升至 85.30%，Self-BLEU-2 从 58.79% 降至 52.88%，Distinct-3 从 6.68% 升至 7.81%。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：1）实验仅基于单一虹鳟队列的 10 天数据，30 个测试片段来自第 10 天两次投喂事件，评估的是队列内时间泛化而非跨种群生物重复，未来需在多种鱼类、多养殖系统和更长周期上验证泛化性。2）物理一致运动学增强仅依赖刚性空间旋转和反射，虽保持标量速度幅值，但不意味着完全流体动力学等价，可能引入分布漂移。3）AC 公式采用等权融合位移、速度和加速度的 z-score 均值，虽经消融验证优于方差和能量公式，但权重配置和聚合方式仍有优化空间。4）反事实偏好对仅覆盖水温、溶解氧、养殖密度、投喂历史和跨物种生理基线五个维度，可扩展至更多环境胁迫因素和操作场景。5）mDPO 对齐依赖专家策展的偏好对，标注成本高，未来可探索自动偏好生成或基于规则的合成方法。6）当前框架的决策输出为结构化文本，可进一步与自动化投喂设备深度集成，实现闭环控制。7）HBE 的隐式软令牌虽编码丰富动态模式，但缺乏直接可验证的物理 grounding，可探索软令牌的可解释性增强方法。8）可迁移至其他工业故障诊断场景，将时序信号转换为诊断报告并支持可追溯决策。

### Q6: 总结一下论文的主要内容

本文提出 THPL，一个面向 RAS 虹鳟精准投喂管理的知识驱动视觉到语言决策支持框架。框架包含四个功能层：任务特定行为感知层通过 Fishsort 提取鱼群轨迹并计算无量纲活动系数（AC），量化摄食强度并索引专家规则；分层行为编码器（HBE）采用 Temporal-then-Set 级联结构，通过时序 Transformer 和集合 Transformer 分别建模个体运动学和集体动力学，生成显式物理令牌和隐式软令牌组成的双证据行为表示；提示工程层将环境参数、养殖背景和专家规则编译为结构化文本提示；策略决策层以 Llama-3.1-8B 为基座，经 LoRA 微调和反事实 mDPO 对齐，生成包含投喂量、投喂间隔、投喂器状态和专家理由的结构化决策文本，并由确定性验证器校验后执行。实验表明，AC 与专家标注摄食强度呈显著单调正相关（Spearman ρ=0.925），分类准确率 95.32%；双证据行为令牌将决策准确率从纯文本基线的 33.33% 提升至 93.33%；反事实 mDPO 进一步将准确率提升至 96.67%，METEOR 从 58.10% 提升至 85.30%，Self-BLEU-2 从 58.79% 降至 52.88%，Distinct-3 从 6.68% 升至 7.81%，有效抑制模板化并增强因果一致性和操作安全性。该研究为精准水产养殖提供了新的决策支持范式，其将连续时空运动学与 LLM 因果推理结合的方法对工业故障诊断和可解释时间序列分析具有借鉴意义。
