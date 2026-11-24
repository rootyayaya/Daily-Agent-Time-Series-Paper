---
title: "MedTimeQ: Query-guided fusion of time-series foundation models and LLMs for multi-lead ECG classification"
authors:
  - "Kiana Taktehrani"
  - "Maryam Hosseini"
  - "Arash Mohammadi"
date: "2026-11-22"
arxiv_id: "2611.29690"
arxiv_url: "https://arxiv.org/abs/2611.29690"
pdf_url: "https://arxiv.org/pdf/2611.29690v1"
github_url: "https://github.com/kkianamm/MedTimeQ"
categories:
  - "eess.SP"
tags:
  - "时序基础模型"
  - "LLM融合"
  - "ECG分类"
  - "多导联时序"
  - "查询引导融合"
  - "语义原型学习"
  - "参数高效微调"
  - "医疗时间序列"
  - "临床语义"
  - "门控残差融合"
relevance_score: 7.5
---

# MedTimeQ: Query-guided fusion of time-series foundation models and LLMs for multi-lead ECG classification

## 原始摘要

Accurate classification of medical time series, such as electrocardiograms (ECGs), requires capturing waveform morphology, long-range temporal structure, inter-lead dependencies, and clinical semantics. Existing large language model (LLM)-based approaches often map signal patches directly into the language embedding space, potentially underusing pretrained time-series knowledge and transferring redundant or irrelevant information. We propose MedTimeQ, a parameter-efficient framework that integrates a lead-aware temporal foundation encoder with an LLM-reprogrammed ECG pathway through gated residual fusion. A Query Former uses learned diagnostic queries to select and compress fused representations into informative soft tokens for a frozen LLM. Semantic prototype learning further guides classification through multiple clinical descriptions per category, statistics-based prompt selection, and knowledge distillation. Both foundation backbones remain frozen, limiting training to lightweight interface and classification components. We evaluate MedTimeQ on PTB-XL, Chapman-Shaoxing, and MIT-BIH for recording-level diagnosis, rhythm classification, and heartbeat classification, respectively. MedTimeQ achieves the best performance in 11 of 12 dataset-metric comparisons, with consistent class-balanced gains across all three tasks. On PTB-XL, it achieves 76.93% accuracy and 58.14% macro-F1, exceeding MedTsLLM by 10.08 and 7.07 percentage points, respectively. These results demonstrate the benefits of selectively integrating pretrained temporal representations with clinical language semantics. Code: https://github.com/kkianamm/MedTimeQ

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于医学时间序列（尤其是心电图）分类任务。准确的ECG分类需要同时捕捉波形形态、长程时间依赖、多导联关系以及临床语义，但现有方法难以将这些信息统一利用。近年来，基于大语言模型（LLM）的方法通过将信号片段直接映射到语言嵌入空间进行分类，代表性工作包括MedTsLLM、Time2Lang、OpenTSLM等。然而，这类方法存在明显不足：直接将信号patch投射进语言嵌入空间，可能未能充分利用预训练时间序列模型所蕴含的生理知识，同时会引入冗余或无关信息，导致诊断相关证据被稀释。此外，现有方法尚未在统一框架内同时整合导联感知的时间表示、时序特征与LLM兼容特征的自适应融合、基于可学习查询的信号到语言迁移，以及语义接地的原型学习。针对这些局限，本文提出MedTimeQ，其核心问题是：如何在保持两个基础骨干网络冻结、仅训练轻量接口的前提下，选择性地将预训练时间序列表示与临床语言语义相结合，把诊断相关证据压缩为软token输入冻结LLM，并通过临床语义原型定义决策空间，从而在记录级诊断、节律分类和心搏分类等多任务上实现参数高效且类别均衡的性能提升。

### Q2: 有哪些相关研究？

相关研究主要分为三类。方法类方面，MedTsLLM、Time2Lang、OpenTSLM、MEIT、GEM、ECG-LLM、K-MERL、SuPreME 和 FG-CLEP 等语言对齐方法将生理信号映射到临床文本或 LLM 嵌入空间，用于分类、表示学习和推理；其中 MedTsLLM 是本文最直接的对比基线，本文在 PTB-XL 上较其准确率和宏 F1 分别提升 10.08 和 7.07 个百分点。与这些方法不同，MedTimeQ 不直接把信号 patch 映射进语言嵌入空间，而是先以导联感知的时间序列基础模型编码，再通过门控残差融合与 LLM 重编程通路结合，避免冗余信息传递。应用类方面，已有工作将 LLM 用于 ECG 分类与临床语义适配，并采用临床依据的提示集成提升生物医学语义适应性；本文进一步引入多临床描述、统计筛选提示和知识蒸馏构建语义原型决策空间。评测类方面，PTB-XL、Chapman-Shaoxing 和 MIT-BIH 是常用基准，分别对应记录级诊断、节律分类和心搏分类；本文在三者上验证参数高效的多任务一致性收益。总体而言，现有研究尚未在统一框架中联合导联感知时间表示、时序与 LLM 兼容特征的自适应融合、学习查询的信号到语言迁移以及语义原型学习，这正是本文的切入点。

### Q3: 论文如何解决这个问题？

MedTimeQ 的核心思路是：不把 ECG 信号直接硬映射进语言空间，而是让“时间序列基础模型”和“LLM”各自贡献互补信息，再通过查询机制只把诊断相关证据送入 LLM。整体框架包含四个关键组件。

第一，双分支编码。一条分支沿用 MedTsLLM 的 LLM 重编程信号编码器，将归一化、分块后的 ECG patch 投影为 LLM 兼容的 token 流，充当语义桥梁；另一条分支引入冻结的 MOMENT-1-base 时间序列基础编码器，并通过可学习的导联嵌入和注意力加权池化聚合多导联信息，保留波形形态与跨导联结构——这正是纯语言重编程容易丢失的归纳偏置。

第二，查询引导的门控融合。两路 token 对齐后拼接，经特征级门控生成残差增量，以“保留 LLM 兼容表示为主、按需注入时间证据”的方式融合，避免冗余信息污染。

第三，MQ-Former 压缩。它维护一组可学习的诊断查询，通过自注意力加对融合记忆的交叉注意力，将变长融合序列压缩为固定长度的软 token，使不同查询分别专注于形态、时序或跨导联证据，再与提示嵌入一起送入冻结 LLM。

第四，语义原型预测。为每个类别准备多条临床描述，经统计筛选后取平均归一化形成类原型，用余弦相似度加可学习温度分类，并将原型作为教师对可训练预测头做知识蒸馏。

训练时两个基础骨干均冻结，只更新适配层、投影、融合、MQ-Former、辅助头等轻量组件；损失由交叉熵、各分支辅助损失、跨分支对齐、查询多样性正则和语义蒸馏组成。创新点在于导联感知的时间基础模型融合、门控残差与查询压缩的选择性证据传递，以及临床语义原型监督。

### Q4: 论文做了哪些实验？

论文在三个公开心电图基准上评估MedTimeQ：PTB-XL（21,799条10秒12导联记录，按1–8/9/10折划分训练/验证/测试，五类诊断超类）、Chapman-Shaoxing（45,152条10秒12导联记录，筛选九类节律的单标签记录并重采样至512点，分层80/10/10划分）和MIT-BIH（44条非起搏记录，采用DS1/DS2跨患者协议，记录114、119、208、223作验证，按AAMI五类进行心搏分类）。实验设置上，两路表征共享512维空间，MQ-Former为4层、32个学习查询、8个注意力头，输出投影到冻结的Llama-2-7B嵌入空间；训练20轮，Adam优化器，批大小16，学习率1e-4，dropout 0.1，bfloat16精度，使用NVIDIA H100 80GB。对比方法包括MedTsLLM、GEM等代表性方法，指标为准确率及宏平均F1、精确率、召回率，以宏F1为主。结果显示MedTimeQ在12项数据集-指标比较中11项最优：PTB-XL上准确率76.93%、宏F1 58.14%，较MedTsLLM分别提升10.08和7.07个百分点；Chapman-Shaoxing上较MedTsLLM准确率提升4.94、宏F1提升6.53、宏精确率提升12.98、宏召回率提升8.28个百分点；MIT-BIH上取得最高准确率、宏F1和宏精确率，但宏召回率低于GEM。消融实验表明，加入导联感知时序编码器与融合使宏F1从51.07%升至57.47%、召回率从49.85%升至56.64%，语义原型学习进一步提升类平衡指标。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有以下几点。其一，框架仅在三个公开 ECG 数据集上验证，且两个基础骨干均被冻结，跨模态（EEG、PPG、影像）与跨任务（预后、事件预测）的泛化性尚不明确，未来可在更多临床场景中检验该查询式融合范式的可迁移性。其二，Query Former 的软 token 数量与诊断查询设计目前依赖人工设定，缺乏对"选择多少、选择什么"的可解释性分析，可探索自适应查询数量与注意力可视化，以增强临床可信度。其三，语义原型依赖人工撰写的类别描述，存在描述偏差与覆盖不足风险，未来可引入 LLM 自动生成并筛选原型，或构建可学习的原型库。其四，门控融合为静态权重，可考虑引入不确定性估计与样本级动态路由，在信号质量差时更多依赖语言先验。此外，当前仅做分类，未来可扩展到定位、分段与报告生成等更细粒度任务，并结合医生反馈进行人机协同的持续学习。

### Q6: 总结一下论文的主要内容

论文针对多导联心电图分类中现有LLM方法将信号片段直接映射到语言嵌入空间、未能充分利用预训练时序知识且易引入冗余信息的问题，提出MedTimeQ参数高效框架。方法上，它通过门控残差融合将导联感知的时序基础编码器与经LLM重编程的ECG通路结合，利用Query Former以可学习诊断查询选择并压缩融合表示，生成信息丰富的软令牌输入冻结LLM；同时引入语义原型学习，借助每类多个临床描述、基于统计的提示选择与知识蒸馏引导分类，两个基础骨干均保持冻结。在PTB-XL、Chapman-Shaoxing和MIT-BIH上分别进行记录级诊断、节律分类与心搏分类，MedTimeQ在12项数据集-指标比较中11项最优，PTB-XL上准确率达76.93%、宏F1为58.14%，较MedTsLLM分别提升10.08和7.07个百分点。结论表明，选择性融合预训练时序表示与临床语言语义具有互补优势，紧凑查询接口可有效学习二者交互。
