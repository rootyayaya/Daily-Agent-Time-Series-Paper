---
title: "ReForest: Interpretability Meets Reasoning in Isolation Forest"
authors:
  - "Juyoung Seo"
  - "Geonwoo Bang"
  - "Dongho Kim"
  - "Moohong Min"
date: "2026-10-27"
arxiv_id: "2610.37316"
arxiv_url: "https://arxiv.org/abs/2610.37316"
pdf_url: "https://arxiv.org/pdf/2610.37316v1"
categories:
  - "cs.AI"
tags:
  - "时间序列异常检测"
  - "可解释性"
  - "LLM推理"
  - "语义解释生成"
  - "统计与语义融合"
  - "不确定性感知集成"
  - "工业故障诊断"
  - "决策路径自然语言化"
relevance_score: 8.5
---

# ReForest: Interpretability Meets Reasoning in Isolation Forest

## 原始摘要

Statistical anomaly detection methods like Isolation Forest are efficient but suffer from a critical semantic gap. They identify numerical rarities but fail to understand the contextual meaning of data, often missing subtle, context-dependent anomalies. Conversely, Large Language Models possess strong semantic reasoning capabilities but are prohibitively expensive and slow for large-scale deployment. To bridge this gap, we propose ReForest, a novel framework that synergizes the statistical efficiency of Isolation Forest with the reasoning power of LLMs. ReForest transforms the latent decision paths of Isolation Forest into natural-language explanations, enabling an LLM to refine anomaly detection through an uncertainty-aware dynamic ensemble. This approach allows the model to adaptively weigh statistical and semantic signals based on uncertainty-driven instance-level confidence. Extensive experiments on four real-world datasets (Healthcare, Finance) demonstrate that ReForest significantly outperforms baselines, achieving an average 21% improvement in Recall and a 10% gain in F1-score. Our framework not only improves detection performance but also enhances model transparency by grounding semantic narratives in statistical evidence, providing interpretable rationales essential for high-stakes decision-making.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决统计异常检测方法（尤其是孤立森林）与真实数据语义理解之间的“语义鸿沟”问题。研究背景在于，孤立森林等传统方法凭借线性可扩展性和对数值离群点的高效识别，被广泛用于金融欺诈检测、网络安全入侵检测和医疗诊断等关键场景，其基本假设是异常“少而不同”，能在更少步骤内被隔离。然而，现有统计方法存在根本不足：它们把特征当作抽象数字，忽略数据背后的语义上下文，因而容易漏掉依赖语境的细微异常（假阴性），或把语义上合理的稀有案例误判为异常（假阳性）。例如，高薪的年轻员工在统计上可能稀有，但若其岗位是高成本地区的高级开发者，则语义上完全合理；反之，数值正常的“30岁实习生”却可能在语境上异常。另一方面，大语言模型具备语义推理与世界知识，可弥补这一缺陷，但直接用于大规模异常检测成本高、速度慢，且缺乏统计依据时可能生成看似合理却错误的解释。因此，本文的核心问题是：如何在保持统计方法效率的同时引入语义推理能力，弥合数值稀有性与语境异常之间的鸿沟，并实现可解释、可扩展的异常检测。为此，作者提出ReForest框架，将孤立森林的隔离路径转化为自然语言叙述，并借助不确定性感知的动态集成，按实例级置信度自适应权衡统计信号与语义信号。

### Q2: 有哪些相关研究？

相关研究主要分为三类。方法类方面，统计与距离方法长期主导异常检测：Isolation Forest 利用随机树隔离异常点，LOF 通过局部密度偏差检测局部异常，One-Class SVM 在高维空间学习正常数据边界，HBOS、KNN 基于距离度量，ECOD 利用经验累积分布函数实现免调参检测；深度学习方法包括自编码器、变分自编码器和 Deep SVDD，学习正常数据的紧凑表示。这些方法计算高效，但缺乏语义理解，难以捕捉属性级关系与领域约束。应用类方面，LLM 被用于时序异常检测（如 GPT-4 解读时间模式）、日志分析（LogGPT）和视觉异常检测（AnomalyGPT）。混合类方面，AnomalyLLM 通过知识蒸馏将 LLM 能力迁移到小模型，另一些工作将 LLM 用作数据增强或合成异常生成工具。本文与上述工作的区别在于：现有混合方法要么对全部数据点调用 LLM 导致成本高昂，要么将 LLM 当作黑盒分类器而缺乏统计依据、易产生幻觉，且多采用固定组合策略；ReForest 则提取 Isolation Forest 的隔离路径作为可解释特征为 LLM 提供统计依据，并引入基于不确定性的实例级动态加权机制，实现统计筛选与语义验证的互补协同。

### Q3: 论文如何解决这个问题？

ReForest 的核心思路是用“统计筛选—语义推理—不确定性融合”的三段式架构，弥合孤立森林数值异常与语义异常之间的鸿沟，同时把 LLM 的调用成本控制在可接受范围。

整体框架包含四个阶段。第一阶段是自适应统计筛选：先用孤立森林为每个样本打分，再依据训练集估计的异常比例 r̂_anom 乘以安全边际 α（取 1.5，借鉴 Tukey 1.5 IQR 规则），并裁剪到 [0.05, 0.50] 区间，得到筛选率 C_est，只把得分最高的这部分样本送入 LLM。实验中实际筛选率约 15–20%，使 LLM 只处理最模糊的少量样本，避免全量推理的开销。

第二阶段是路径感知的语义提取。孤立森林每棵树产生一条决策路径，全部送入 LLM 会造成信息过载。ReForest 基于“短路径即强异常信号”的奥卡姆剃刀原则，按路径深度升序排序，选取 top-K 最短路径，再结合训练集统计量（四分位位置、极端程度等）翻译成自然语言叙述，为 LLM 提供可解释的结构性证据。

第三阶段由 LLM 依据上下文提示对候选样本做语义验证，输出语义异常分 S_LLM。

第四阶段是不确定性感知的动态集成，也是关键创新点。先将孤立森林得分经 Z-score 与 sigmoid 归一化为 P_IF，再定义动态权重 α(x)=Clip(α_base+Δ(P_IF), α_min, α_max)：当 P_IF 远离 0.5（高置信）时上调统计权重，靠近 0.5（高不确定）时下调，让语义推理接管。最终概率为 P_final=α(x)·P_IF+(1−α(x))·S_LLM/10。

该设计的创新在于：以统计模型作高效预过滤降低 LLM 成本；用最短路径提取实现可解释的结构化提示；以实例级不确定性自适应调配两种信号，兼顾统计严谨性与语义上下文感知，并在高风险决策场景中提供可审计的推理依据。

### Q4: 论文做了哪些实验？

论文围绕三个研究问题展开实验。实验设置上，采用四个真实数据集：医疗领域的HCV（615样本、12特征、异常率13.3%）和Stroke（4909样本、10特征、异常率4.3%），金融领域的HMEQ（3364样本、12特征、异常率8.9%）和Loan Default（9578样本、13特征、异常率16.0%）。对比方法包括统计基线IForest、LOF、ECOD以及深度学习模型AutoEncoder，均基于PyOD实现；以F1为主指标，同时报告Precision和Recall。主要结果显示：在Stroke上ReForest的Recall从IForest的0.19提升至0.27，F1达0.22；HCV上F1最高为0.68；Loan Default上P/R/F1均最优（0.31/0.37/0.34）；HMEQ上AutoEncoder最优（F1=0.37），ReForest与IForest相当。整体平均Recall提升21%、F1提升10%。此外，在HCV上进行K∈{1,…,5}的路径数敏感性实验，发现K=3–4时F1最高（约0.714和0.732），K=5时降至约0.686，故默认取K=4；并通过四个定性案例展示ReForest纠正IForest的假阳性与假阴性并给出可理解解释。

### Q5: 有什么可以进一步探索的点？

论文的局限主要有三点：一是语义路径信息的收益依赖数据集，当异常由明显统计模式驱动时提升有限；二是LLM调用虽经自适应筛选降至15–20%，但成本与延迟仍制约大规模部署；三是不确定性校准较粗糙，难以精准判断何时需要语义推理。未来可探索：改进不确定性校准机制，用更细粒度的置信度估计或学习式路由替代阈值筛选；在提示中注入结构化领域知识（如医疗规则、金融合规约束），提升语义判断的可靠性；扩展到多模态与流式场景，设计成本感知的语义路由策略。此外，可考虑用小规模蒸馏模型替代大LLM承担部分推理，或引入人机协同反馈闭环，让专家修正结果反哺路径解释与集成权重，从而在保持可解释性的同时进一步降低成本并提升跨数据集鲁棒性。

### Q6: 总结一下论文的主要内容

论文针对传统统计异常检测方法（如Isolation Forest）存在语义鸿沟的问题——它们只能识别数值稀有性，却无法理解数据的上下文含义，容易漏检依赖语境的细微异常；而大语言模型虽具备语义推理能力，但大规模部署成本高、速度慢。为此，作者提出ReForest混合框架，将Isolation Forest的统计效率与LLM的推理能力相结合。方法上，ReForest首先通过自适应统计筛选，仅将异常得分最高的约15%–20%样本送入LLM；随后提取Isolation Forest决策路径中最短的Top-K条路径并转化为自然语言叙述，为LLM提供统计依据；最后采用不确定性感知的动态集成机制，根据实例级置信度自适应调整统计模型与LLM的权重。在医疗与金融四个真实数据集上的实验表明，ReForest平均提升召回率21%、F1分数10%，并能提供统计与语义双视角的可解释理由，使异常检测从纯数值稀有性迈向上下文感知的可信决策。
