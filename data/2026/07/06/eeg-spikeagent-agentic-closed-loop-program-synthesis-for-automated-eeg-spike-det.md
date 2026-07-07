---
title: "EEG-SpikeAgent: Agentic Closed-Loop Program Synthesis for Automated EEG Spike Detection"
authors:
  - "Sonali Santhosh"
  - "Kelly Shuhong Yu"
  - "Eugene Chang"
  - "Jonathan Kim"
  - "Kie Shidara"
  - "Danilo Bernardo"
date: "2026-07-06"
arxiv_id: "2607.04558"
arxiv_url: "https://arxiv.org/abs/2607.04558"
pdf_url: "https://arxiv.org/pdf/2607.04558v1"
categories:
  - "cs.CL"
  - "cs.AI"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "LLM/Agent for Time Series"
  - "Closed-Loop Program Synthesis"
  - "EEG Spike Detection"
  - "Signal Processing Feature Engineering"
  - "Tabular Classifier"
  - "Interpretability"
  - "Code-Driven Feature Generation"
  - "Clinical Time Series"
  - "Automated Feature Engineering"
relevance_score: 8.5
---

# EEG-SpikeAgent: Agentic Closed-Loop Program Synthesis for Automated EEG Spike Detection

## 原始摘要

Automated detection of interictal epileptiform discharges in scalp electroencephalography (EEG) is clinically important, but recent high-performing deep-learning models often trade interpretability for accuracy. We introduce EEG-SpikeAgent, a closed-loop program-synthesis framework that uses a large language model (LLM) agentic system to generate signal-processing features for spike detection in scalp EEG. The system iteratively proposes one deterministic EEG feature module at a time, executes the resulting code on EEG to generate tabular features, evaluates performance via a tabular classifier, summarizes run-level metrics, and feeds structured diagnostics back to the model for refinement. Across iterations, EEG-SpikeAgent proposes and refines candidate signal features and decision rules informed by model performance. We evaluated EEG-SpikeAgent on VEPISET, a public 29-channel dataset of 4-second epochs containing 2,516 discharge-containing and 22,933 non-discharge epochs. Across five-fold cross-validation with a gradient-boosted tree classifier, agent-generated features achieved an area under the receiver operating characteristic curve of 0.935, balanced accuracy of 0.699, F1 score of 0.557, sensitivity of 0.401, and specificity of 0.996 at the default operating point. At an operating point with sensitivity 0.80, mean precision was 0.470 and mean specificity was 0.900. Artifact-aware feature generation improved balanced accuracy and F1 score over spike-only feature search. These results indicate that LLM-based program synthesis can automate EEG feature engineering in auditable and inspectable code-driven manner for clinical and methodological review.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

脑电图（EEG）中发作间期癫痫样放电（IEDs）的自动检测具有重要临床价值。现有方法面临两难：高性能深度学习模型虽准确度高，但牺牲了可解释性，且依赖大量标注数据，易学习到脆弱的捷径，在不同数据集或记录条件下泛化性存疑；而基于物理模型的可解释管线虽数据高效，却依赖专家手动设计特征集，迭代优化过程缓慢且耗时。因此，亟需一种既能自主探索EEG特征空间、又能保持特征定义和决策规则可审计、可解释的系统。本文提出的EEG-SpikeAgent旨在解决这一核心矛盾：通过大语言模型（LLM）智能体在闭环中迭代生成信号处理特征代码，自动构建可审计、可检查的EEG尖峰检测管线，从而在保持高检测性能的同时，确保每个生成的特征均可被审查、消融或追溯至模型行为，克服现有方法在可解释性与自动化之间的权衡。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及三大类工作。**方法类**：首先是基于深度学习的EEG尖峰检测系统，如多种达到专家级准确率的模型，但本文指出这些系统牺牲了可解释性且泛化性受限于数据集差异；其次是传统物理特征工程管道，它们依赖手动定义信号形态、频谱等特征，但迭代优化缓慢且依赖专家经验。本文的EEG-SpikeAgent通过LLM代理自动生成可审计的特征代码，克服了这两类方法的局限。**应用类**：包括临床EEG中发作间期癫痫样放电（IED）的自动检测，人类专家依赖空间相位反转和时域尖峰形态等线索，而本文首次将LLM驱动的程序合成应用于该任务，实现了闭环特征搜索。**评测类**：本文在VEPISET公开数据集上进行了五折交叉验证，与纯数据驱动方法相比，其生成的梯度提升树分类器在AUC（0.935）和特异性（0.996）上表现优异，且通过引入伪迹感知特征搜索提升了平衡准确率和F1分数。本文的核心区别在于：不同于黑箱深度模型，它保留了每个特征的代码级可审计性；不同于手动管道，它实现了自动化迭代优化。

### Q3: 论文如何解决这个问题？

EEG-SpikeAgent通过一种闭环程序合成框架将EEG尖峰检测转化为可解释的自动化特征工程问题。其核心方法基于大语言模型（LLM）驱动的智能体系统，在迭代过程中逐步生成确定性信号处理特征，并利用下游分类器反馈优化特征组合。

整体框架是一个六阶段闭环搜索循环：1）**上下文构建**：向LLM提供当前代码摘要、数据集假设、特征性能历史及特征清单；2）**特征提案**：LLM每次仅提出一个互补的可解释特征变更方案；3）**代码编辑**：代码编辑模型将提案实现为最小化Python模块（限定修改~/features/feature_*.py文件）；4）**宿主执行**：主机注册新特征，在固定EEG数据分割上运行特征提取，生成表格化特征矩阵；5）**组合评估**：使用XGBoost分类器在训练集上进行分层交叉验证，计算平衡准确率、F1分数、AUROC等指标；6）**诊断反馈**：生成包含指标、混淆矩阵和失败案例的结构化诊断摘要，反馈至下一轮上下文。

关键技术包括：**确定性特征执行器**（每个特征模块定义Pydantic配置模型、注册条目和确定性执行函数，将单条EEG片段映射为固定数值诊断）、**增量特征管理**（通过特征清单维护活跃特征组合，新特征评估时不重复计算未变更特征块）、**约束性特征搜索**（强制使用短窗口多实例摘要、鲁棒归一化和紧凑跨通道聚合，避免全周期平均或高维表示）、**人工制品感知调度**（在第5/10/15次迭代强制生成伪迹相关特征以提升分类性能）。创新点在于将LLM的程序合成能力与可审计的确定性信号处理相结合，通过闭环反馈实现特征空间的自动探索与优化，最终在VEPISET数据集上达到0.935的AUROC和0.699的平衡准确率。

### Q4: 论文做了哪些实验？

实验使用VEPISET公共数据集，包含84名患者的29通道头皮EEG数据，共2,516个癫痫样放电（IED）epoch和22,933个非IED epoch（每个4秒）。采用5折交叉验证，每折由LLM驱动的EEG-SpikeAgent自主生成400-500个定量EEG特征（共20次迭代），并训练XGBoost分类器。对比方法为仅使用尖峰检测特征的消融实验。主要结果：在默认操作点，模型AUROC达0.935±0.008（95% CI: 0.925-0.946），平衡准确率0.699±0.016，F1分数0.557±0.034，灵敏度0.401±0.032，特异度0.996±0.001。在灵敏度0.80的操作点，平均精确度0.470，平均特异度0.900。消融实验表明，引入伪迹检测特征使平衡准确率提升约1.4个百分点，F1分数提升2.3个百分点。特征重要性分析显示，形态学和空间尖峰特征贡献最大，但伪迹特征（仅占18%）也出现在前30重要特征中，验证了伪迹建模的有效性。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：灵敏度较低（默认阈值仅0.401），仅在单一公共数据集上验证，未测试连续记录筛查、事件定位或站点分布偏移，且特征可检查性不等于临床可解释性。未来可探索的方向包括：1）引入校准机制和操作点自适应选择，根据临床场景（高特异性筛查或高灵敏度检测）动态调整阈值；2）扩展至连续EEG记录和多种IED亚型（如棘波、尖慢波）的细粒度检测，并评估拓扑和形态学特征的影响；3）结合多中心数据验证特征稳定性，并引入对抗性测试评估对噪声和伪影的鲁棒性；4）将框架迁移至其他EEG任务（如癫痫发作检测、睡眠分期），并探索LLM与可微分特征提取器的混合架构，在保持可审计性的同时提升性能。此外，可设计交互式工具让临床专家对生成特征进行标注反馈，形成人机协同的闭环优化。

### Q6: 总结一下论文的主要内容

EEG-SpikeAgent提出了一种基于大语言模型（LLM）的闭环程序合成框架，用于自动检测头皮脑电图（EEG）中的发作间期癫痫样放电（IED）。该方法通过LLM智能体系统迭代生成确定性信号处理特征代码，执行后生成表格特征，并由分类器评估性能，再将结构化诊断反馈给模型进行优化。在VEPISET公共数据集上（29通道，4秒片段），使用梯度提升树分类器进行五折交叉验证，代理生成的特征实现了0.935的AUC、0.699的平衡准确率和0.557的F1分数。主要贡献在于提供了一种可审计、可检查的特征搜索过程，每个特征都是可执行的确定性代码，比纯深度学习系统的潜在表示更易解释和追踪。结果表明，LLM引导的程序合成能自动化EEG特征工程，且显式伪迹建模有助于提升性能。尽管在灵敏度上不如深度学习方法，但该系统的高特异性（0.996）使其适用于假阳性负担重要的场景，如大规模EEG回顾性审查。
