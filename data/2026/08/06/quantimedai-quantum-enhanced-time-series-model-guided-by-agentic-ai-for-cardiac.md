---
title: "QuanTiMedAI: Quantum-Enhanced Time-Series Model guided by Agentic AI for Cardiac Arrest Mortality Prediction"
authors:
  - "Mutasim Fuad Sarker"
  - "Adiba Rahman Namira"
  - "Wafa Binte Alam"
  - "Md Adnan Arefeen"
  - "Mahzabeen Emu"
  - "Sumaiya Tabassum Nimi"
date: "2026-08-06"
arxiv_id: "2608.06294"
arxiv_url: "https://arxiv.org/abs/2608.06294"
pdf_url: "https://arxiv.org/pdf/2608.06294v1"
categories:
  - "cs.AI"
  - "cs.ET"
tags:
  - "Agentic AI"
  - "LLM-guided feature selection"
  - "Time-series mortality prediction"
  - "Quantum recurrent network"
  - "Clinical decision support"
  - "ICU monitoring"
  - "MIMIC-IV"
  - "Temporal modeling"
  - "Feature discovery"
  - "Low-parameter model"
relevance_score: 7.5
---

# QuanTiMedAI: Quantum-Enhanced Time-Series Model guided by Agentic AI for Cardiac Arrest Mortality Prediction

## 原始摘要

Cardiac arrest remains one of the most lethal conditions encountered in intensive care units. Despite the growing availability of electronic health record data, existing mortality prediction studies in this population largely depend on static summaries derived from early admission. Such approaches ignore the temporal progression of physiological deterioration and recovery that unfolds throughout a patient's ICU stay. To address this limitation, we introduce QuanTiMedAI, a quantum-agentic framework developed for cardiac arrest mortality prediction using agentic AI guided quantum enhancement time series model. The proposed system combines an agentic large language model (LLM) for clinically informed feature discovery with a compact quantum recurrent network for temporality aware mortality prediction. Our findings demonstrate that agentic LLM-guided feature selection consistently outperforms conventional feature selection approaches, and the proposed quantum architecture achieves competitive predictive performance through nonlinear feature enhancement while keeping the number of parameters very low. Through extensive experimentation on a MIMIC-IV cohort of cardiac arrest patients, QuanTiMedAI's quantum-enhanced architecture attains an AUROC of 0.852 using only 605 parameters, an improvement of approximately 2.9\% over a current state-of-the-art baseline for this task. A structured ablation study systematically validates the contribution of each architectural design choice. These results show that quantum-enhanced sequential modeling can exceed classical recurrent networks while using substantially fewer parameters.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

心脏骤停是ICU中致死率极高的危重症，尽管电子健康记录数据日益丰富，现有基于MIMIC-IV的死亡预测研究大多依赖入院早期的静态摘要，将患者视为固定快照，无法捕捉ICU住院期间生理恶化与恢复的时间动态变化。这种静态建模方式忽略了时序信息中蕴含的关键预后价值，而序列模型虽在通用ICU人群中表现更优，却尚未被应用于心脏骤停死亡预测。

现有方法还存在两方面不足：一是经典LSTM等序列模型参数规模大，且难以建模长序列中复杂的非线性时间依赖；二是传统特征选择方法如LASSO和相关性过滤纯粹依赖数据统计关联，缺乏临床知识指导，所选特征虽在统计上有效但缺乏临床合理性。

本文提出QuanTiMedAI框架，核心解决三个问题：利用Agentic LLM进行临床知识引导的迭代式特征发现，替代纯数据驱动的特征选择；设计紧凑的量子循环网络（改进五VQC QLSTM架构）以极低参数实现高效时序建模；将两者整合为统一的临床决策支持流水线，在心脏骤停死亡预测任务上超越经典基线，仅用605个参数即达0.852的AUROC，验证了量子增强时序建模与Agentic AI结合的有效性。

### Q2: 有哪些相关研究？

相关研究主要分为以下几类：

**1. 心脏骤停患者死亡预测的经典机器学习研究**  
Sun等、Liu等、Li等和Jia等均基于MIMIC-IV数据库，使用LASSO、XGBoost或集成模型，从入院首日静态特征（人口学、合并症、生命体征等）预测院内或28天死亡率。这些研究均将数据聚合为静态向量，完全忽略时间维度。本文与其区别在于引入三维时序建模，保留患者ICU全程的生理变化动态。

**2. 通用ICU时序预测的深度学习方法**  
Deng等和Wang等分别对MIMIC-IV和MIMIC-III的通用ICU人群应用LSTM、GRU等循环网络，验证了时序模型优于静态分类器。但这些研究未聚焦心脏骤停亚组，且未采用量子架构。本文首次将时序深度学习应用于心脏骤停患者的院内死亡预测。

**3. 量子机器学习与QLSTM研究**  
QLSTM由混合量子-经典架构提出，已在金融预测、混沌时间序列等任务中超越经典LSTM。在医疗领域，Ullah等和npj Digit. Med.的系统综述均指出量子模型在临床EHR时序数据上的应用极为稀缺。唯一生物医学应用是药物发现（静态分子指纹），不涉及时序或临床结局。本文是首个将QLSTM应用于患者EHR时序数据并进行结局预测的工作。

**4. 与现有工作的核心差异**  
所有既往心脏骤停研究均无时序表示、无量子架构、无Agentic LLM特征选择。本文是唯一同时整合三维时序建模、LSTM/QLSTM混合架构、Agentic LLM特征发现与可解释性推理的框架，填补了量子时序模型在重症临床预测中的空白。

### Q3: 论文如何解决这个问题？

QuanTiMedAI通过一个端到端的量子-智能体混合框架来解决心脏骤停死亡率预测问题，其核心设计围绕两大创新模块展开。

整体框架包含四个关键组件：**智能体特征选择模块**、**工程化严重度评分通道**、**量子增强循环网络（QLSTM）**以及**分类头**。在特征选择阶段，论文采用基于Gemma 4的智能体LLM，通过两阶段流程（初始选择与迭代精炼）从MIMIC-IV数据中筛选临床相关特征。智能体接收死亡率分层的统计摘要（包括特征相关性、均值±标准差、时间趋势和缺失率），输出K个特征及其权重向量和偏置，并经过最多R轮基于交叉验证性能反馈的迭代优化，强制每轮替换至少α·K个特征以探索特征空间。

严重度评分通道是连接智能体与预测模型的关键桥梁：利用LLM导出的权重对标准化特征进行加权求和，经sigmoid激活后生成每个时间步的临床恶化摘要，嵌入领域知识。该通道作为额外输入通道与原始特征拼接，形成形状为(T, K+1)的张量。

核心创新在于**5-VQC QLSTM架构**：将经典LSTM的每个门替换为混合量子-经典模块，包含经典线性投影和变分量子电路（VQC）。每个VQC采用三阶段设计——Hadamard门初始化叠加态、基于arctan的角度编码、循环CNOT纠缠和可训练旋转门的变分层，最后测量Pauli-Z期望值。特别地，论文通过残差跳跃连接将原始输入直接注入隐藏状态精炼VQC，缓解量子瓶颈导致的信息丢失。整个模型仅需605个参数，通过量子非线性特征增强实现AUROC 0.852，比经典LSTM提升约2.9%，同时保持极低的参数复杂度。

### Q4: 论文做了哪些实验？

论文在MIMIC-IV数据库中构建了心脏骤停ICU患者队列（ICD-9 427.5/ICD-10 I46），以入院后24小时内的临床数据预测院内死亡。实验设置包括三个受控条件：特征选择策略（agentic LLM引导 vs 随机选择）和循环单元架构（QLSTM vs 经典LSTM），其余流程完全一致。共提取56个临床特征，涵盖生命体征、严重程度评分、血液学、凝血、肾功能、代谢/电解质、血气、心脏/肝脏标志物、液体平衡、血管活性药物、通气状态、人口统计学和合并症。

对比方法包括：经典双层LSTM（随机特征选择）、LSTM（LLM引导特征选择）和QuanTiMedAI（QLSTM+LLM引导）。评估指标为AUROC、AUPRC和Brier分数，采用V折交叉验证报告均值±标准差和95%置信区间。主要结果显示，QuanTiMedAI以仅605个参数达到AUROC 0.852，较当前最优基线提升约2.9%。热力图展示了不同特征数K和时间窗口T下的性能变化。消融研究系统验证了各设计选择（LLM特征选择、5-VQC结构、残差连接、严重程度评分通道）的贡献，证实量子增强序列建模能以显著更少的参数超越经典循环网络。

### Q5: 有什么可以进一步探索的点？

该研究在量子-智能体融合框架上展现了创新性，但仍存在若干可探索方向。首先，模型仅在MIMIC-IV单一数据集上验证，缺乏外部多中心数据集的泛化测试，未来可引入eICU或本地医院数据验证跨机构稳定性。其次，QLSTM的量子电路模拟器受限于比特数和噪声模型，实际量子硬件部署时需考虑退相干影响，可探索混合量子-经典架构或噪声自适应训练策略。第三，智能体特征选择依赖Gemma 4的医学知识边界，可引入检索增强生成（RAG）机制动态接入最新临床指南，或设计多智能体辩论机制提升特征选择的可解释性。第四，当前仅预测死亡率，可扩展至多任务学习框架（如同时预测住院时长、并发症风险），并利用SHAP值或注意力权重可视化时序特征贡献，增强临床信任度。最后，605参数的超轻量模型虽高效，但可尝试神经架构搜索（NAS）自动优化量子电路结构，或引入脉冲神经网络（SNN）替代LSTM门控机制，进一步探索时间依赖性建模的极限。

### Q6: 总结一下论文的主要内容

QuanTiMedAI提出了一种量子增强的智能体时间序列框架，用于ICU心脏骤停患者死亡预测。现有研究多依赖入院早期的静态摘要，忽略了患者生理状态的时序演变。该方法创新性地结合了智能体大语言模型（LLM）进行临床知识驱动的特征选择，以及紧凑的量子循环网络（QLSTM）进行时序建模。在MIMIC-IV队列上的实验表明，该框架仅用605个参数即达到0.852的AUROC，比参数匹配的经典LSTM提升约2.9%。消融实验验证了各设计组件的贡献，其中输入重注入跳跃连接带来约1.5%的AUROC提升。该研究首次将智能体AI特征发现与量子时序建模整合于临床决策支持流程，证明了量子增强序列模型能以极低参数超越经典循环网络，为可解释的临床时间序列预测提供了新范式。
