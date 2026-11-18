---
title: "OAK-Mind: Zero-Training Mental Health Change Inference from Passive Sensing via Knowledge-Grounded Multi-Agent LLMs"
authors:
  - "Yishu Ji"
  - "Zhihan Jiang"
  - "Will Ke Wang"
  - "Yuang Fan"
  - "Anind K. Dey"
  - "Xuhai \"Orson\" Xu"
date: "2026-11-17"
arxiv_id: "2611.22248"
arxiv_url: "https://arxiv.org/abs/2611.22248"
pdf_url: "https://arxiv.org/pdf/2611.22248v1"
categories:
  - "cs.MA"
  - "cs.AI"
  - "cs.HC"
  - "cs.LG"
tags:
  - "多智能体LLM"
  - "被动传感"
  - "行为时间序列"
  - "零训练推理"
  - "知识驱动"
  - "可解释推理"
  - "心理健康监测"
  - "领域知识注入"
  - "无监督异常检测"
relevance_score: 7.5
---

# OAK-Mind: Zero-Training Mental Health Change Inference from Passive Sensing via Knowledge-Grounded Multi-Agent LLMs

## 原始摘要

Wearable and smartphone sensors capture behavioral signals associated with mental health, yet inferring mental health outcomes from these signals has traditionally relied on supervised models requiring labeled data and offering limited insight into their predictions. Large language models (LLMs) offer new opportunities to reason over behavioral evidence, but existing LLM-based approaches to passive sensing have largely continued to rely on task-specific fine-tuning or sensor-specific pretraining. In this paper, we introduce \textbf{OAK-Mind}, a zer\textbf{O}-training, multi-\textbf{A}gent, \textbf{K}nowledge-grounded LLM pipeline for inferring mental health changes from passive sensing data. The pipeline organizes sensing data into behavioral dimensions including sleep, physical activity, location mobility, and smartphone use, and orchestrates specialized agents grounded in mental health literature to interpret longitudinal behavioral changes. It synthesizes their assessments and applies questionnaire-based symptom rating to infer changes relative to an individual's baseline assessment with human-readable rationale grounded in observed behavioral patterns and domain knowledge. Across datasets and prediction tasks, while without task-specific training, OAK-Mind achieves comparable or better performance than the most predictive supervised baselines trained on additional labeled samples. It also demonstrate consistent improvement upon direct prompting across four tested LLM backbones. Ablation analyses support the benefits of combining behavioral interpretation with symptom rating, distributing analysis across domain-specific agents, and incorporating domain knowledge. Our findings highlight the potential of knowledge-grounded, multi-agent LLMs for training-free inference of mental health changes from passive sensing data.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决如何在不依赖任务特定训练和标注数据的前提下，从被动感知数据中推断个体心理健康状况变化的问题。研究背景方面，智能手机和可穿戴设备能够持续采集睡眠、体力活动、社交互动和手机使用等行为信号，已有研究表明这些模式与抑郁、焦虑和压力等心理健康结果相关。现有方法主要将该问题建模为监督学习任务，但这类方法依赖规模足够大、质量足够高的带标注被动感知数据集，而此类数据难以获取；同时，监督模型对预测依据的解释能力有限。近年来，大语言模型为解释感知数据提供了新机会，但通用大语言模型并不天然适合处理以时间序列、数值和多模态为主的感知数据，现有基于大语言模型的方法往往仍需任务特定微调或传感器特定预训练，而这些模型适配过程需要充足训练数据、计算资源以及数据准备与优化方面的专业知识，在数据和资源受限的感知研究中难以实际应用。因此，本文的核心问题是：如何设计一种零训练、知识驱动、可解释的多智能体大语言模型流程，将纵向被动感知数据组织为睡眠、体力活动、位置移动性和手机使用等行为维度，由领域知识引导的专门智能体分别分析行为变化，再经跨域综合与问卷症状评级，推断个体心理健康症状严重程度相对于基线的变化（改善、稳定或恶化），并给出基于可观察行为模式和领域知识的可读解释，从而在无需任务特定训练的情况下达到与监督基线相当或更优的性能。

### Q2: 有哪些相关研究？

本文的相关研究可分为四类。

**行为健康与被动感知类**：StudentLife、GLOBEM、College Experience Study、RADAR-MDD等纵向数据集将手机与可穿戴传感数据同重复心理健康评估配对，并发现睡眠规律性、体力活动、位置移动性与抑郁焦虑症状的关联；但Müller等指出GPS抑郁预测在异质人群中泛化显著下降，GLOBEM也显示跨数据集性能差距明显。此类工作为本文提供行为维度依据，但多依赖监督学习。

**传统机器学习类**：Chikersal等用特征提取与选择预测学期末抑郁症状及恶化，另有工作采用群体个性化回归、协同过滤及关联规则挖掘构建行为代理特征。这些方法需标注数据且可解释性有限，本文则以零训练方式替代。

**LLM心理健康推断类**：Mental-LLM、MentaLLaMA基于文本做零样本/少样本提示与指令微调；Health-LLM评估可穿戴健康预测的提示与微调；Yuan等比较数字表型数据的上下文学习与QLoRA微调；PH-LLM、SensorLLM、SensorLM则依赖微调或传感器-语言预训练。本文区别在于无需任务特定训练。

**智能体与传感解读类**：PHIA、SensorChat、GLOSS及个人健康智能体将推理、检索、代码生成分配给专门角色。本文借鉴多智能体分工，但引入心理健康文献知识 grounding 与问卷式症状评分，实现可解释的纵向变化推断。

### Q3: 论文如何解决这个问题？

OAK-Mind 的核心思路是将被动感知数据的心理健康变化推断重构为一个零训练的多智能体“意义建构”过程，用领域知识驱动的 LLM 智能体替代传统的监督学习模型。整体框架分为三层智能体，全部由同一个现成 LLM 通过提示词专门化，不更新任何参数，也不使用他人标注数据或上下文示例，唯一的标签输入是参与者自身的基线得分。

第一层是四个行为变化智能体，分别负责睡眠、身体活动、位置移动性和手机使用四个行为域。每个智能体接收参与者在基线 T1 和随访 T2 两个窗口内该域的感知特征序列，特征名被转为可读描述并按日排列成时间序列。智能体被注入从心理健康知识图谱中抽取的领域知识——该图谱由 LLM 从文献和临床资料中提取实体关系，再按域关键词与结局关键词筛选直接关联并转写为自然语言陈述。智能体据此比较两窗口的行为模式变化，输出带方向判断的行为变化叙述。

第二层是跨域综合智能体，它整合四个域叙述与基线得分，评估症状相关信号是缓解、持续还是加重，并权衡各域证据的一致性或冲突性；基线得分还使智能体考虑“变化空间”，例如接近量表下限者改善余地很小。

第三层是症状评分智能体，它按照 PHQ-4 子量表的条目结构与评分程序，基于综合叙述和基线条目分估计随访时各条目得分，求和后与基线比较，输出改善/稳定/加重的预测标签及可读理由。

创新点在于：完全免训练、以知识图谱接地气的多智能体分工、行为解释与症状评分的两阶段结合，以及全过程自然语言叙述带来的可解释性。消融实验也验证了行为解释与症状评分结合、按域分配智能体以及引入领域知识的各自收益。

### Q4: 论文做了哪些实验？

论文围绕OAK-Mind开展了三组实验。实验设置上，以GLOBEM和College Experience两个被动感知数据集为基准，任务为抑郁与焦虑症状变化的三分类预测（改善、稳定、恶化），评价指标包括准确率、平衡准确率、宏F1和加权F1。对比方法包括五类监督机器学习基线（Xu等协同过滤、Saeb等弹性网逻辑回归、Chikersal等嵌套特征选择加AdaBoost、Borelli等LightGBM、Ahmed等XGBoost）、四种零样本LLM提示方法（Kim等、Yu等零样本、Yu等Tree-of-Thought、Yuan等）以及多数类基线。主实验中所有LLM方法使用GPT-5.4，温度1.2，各方法重复五次取均值。结果表明，OAK-Mind在无需任务特定训练的情况下，性能与使用额外标注样本训练的最强监督基线相当或更优。在GPT-5.2、Qwen-plus、Gemini-2.5-flash、DeepSeek-chat四个骨干模型上，OAK-Mind相对直接提示均有稳定提升。消融实验显示，去除领域知识、将四个领域智能体合并为单一智能体、仅保留行为分析与综合、仅保留问卷症状评分，均导致性能下降，验证了知识 grounding、多智能体分工及行为解读与症状评分结合的有效性。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点。其一，评估依赖问卷式症状评分作为中间桥梁，而被动传感信号与临床量表之间的映射本身存在噪声，未来可引入纵向临床访谈或生态瞬时评估（EMA）作为更可靠的监督锚点，并检验推理链与真实症状轨迹的一致性。其二，方法在四个 LLM 骨干上验证，但对模型规模、上下文长度与推理成本的权衡缺乏系统分析，零训练管线在长周期、高频传感数据下的可扩展性与延迟仍是开放问题。其三，多智能体分工（睡眠、活动、位置、手机使用）目前由人工先验设定，维度间交互（如睡眠紊乱与社交退缩的耦合）可能被割裂，可探索自适应智能体路由或跨维度联合推理。其四，知识 grounding 依赖文献检索，存在覆盖偏差与时效性问题，可构建可更新的领域知识库并引入检索质量评估。其五，缺乏对个体差异与分布漂移的鲁棒性检验，未来可结合个性化基线校准与不确定性量化，输出置信度而非单一推断，从而提升临床可用性。

### Q6: 总结一下论文的主要内容

论文针对从被动感知数据推断心理健康变化这一任务，指出现有监督模型依赖大量标注数据且缺乏可解释性，而现有 LLM 方法仍需任务微调或传感器预训练。为此提出 OAK-Mind：一个零训练、多智能体、知识 grounded 的 LLM 流水线。方法上将感知数据组织为睡眠、身体活动、位置移动和手机使用四个行为维度，由四个行为变化智能体分别结合心理健康领域知识解读纵向行为变化，再由跨域综合智能体整合证据，最后由症状评分智能体依据 PHQ-4 问卷条目和基线评分推断症状是改善、稳定还是恶化，并给出自然语言理由。主要结论：在多个数据集和预测任务上，OAK-Mind 无需任务特定训练即可达到与最强监督基线相当或更优的性能，并在四种 LLM 骨干上稳定优于直接提示；消融实验验证了行为解读与症状评分结合、领域专用智能体分工及领域知识引入的收益，凸显了知识驱动多智能体 LLM 在无训练、可解释心理健康推断中的潜力。
