---
title: "Traceable LLM Reasoning for Fake-Order Fraud Detection"
authors:
  - "Siqi You"
  - "Bingsong Xu"
  - "Zhixian Zheng"
  - "Xinjian Peng"
  - "Yang Xie"
  - "Ying Wang"
  - "Jiarong Xu"
date: "2026-07-25"
arxiv_id: "2607.23075"
arxiv_url: "https://arxiv.org/abs/2607.23075"
pdf_url: "https://arxiv.org/pdf/2607.23075v1"
categories:
  - "cs.CR"
  - "cs.AI"
  - "cs.LG"
tags:
  - "LLM/Agent用于异常检测"
  - "可解释时序诊断"
  - "语义统一模块"
  - "反思机制"
  - "强化学习"
  - "工业传感器解释"
  - "traceable reasoning"
  - "专家反馈"
  - "欺诈检测"
relevance_score: 7.5
---

# Traceable LLM Reasoning for Fake-Order Fraud Detection

## 原始摘要

Detecting fake-order fraud at scale remains a critical challenge for large online-to-offline (O2O) service platforms, as existing approaches often rely on expert-designed features, produce black-box decisions, and provide limited interpretability. To address these limitations, we propose DeepScrub, a reinforcement learning framework built upon large language models (LLMs) for fake-order fraud detection with traceable reasoning. DeepScrub introduces three innovations. First, a semantic unification module converts heterogeneous risk signals into textual descriptions that LLMs can understand. Second, continued pre-training on risk-control corpora injects domain knowledge, and task rewards jointly evaluate prediction correctness and reasoning quality. Third, the SUggest-REflect (SURE) mechanism incorporates expert feedback and model self-checking to iteratively refine reasoning paths. On a real-world fake-order fraud detection dataset, DeepScrub achieves a macro-F1 score of 85.3%, outperforming the best baseline by 2.7 percentage points. Our task-optimized 8B model further surpasses a 32B model, showing that domain adaptation can matter more than model scale in this setting. In a four-week live pilot, DeepScrub achieved 91.8% precision and 88.5% recall, improving over first-stage human reviewers by 16.6 and 38.8 percentage points. It reduced first-stage manual review workload by 94% and saved nearly one million RMB annually. These results show that DeepScrub improves fraud review accuracy, reduces first-stage review workload, and provides traceable evidence for production risk-review workflows.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在大型O2O服务平台上，虚假订单（刷单）欺诈检测面临严峻挑战。现有方法主要分为两类：一是依赖专家手工设计特征和规则，虽在特定场景有效，但维护成本高且难以适应欺诈策略的快速演变；二是基于深度学习的黑盒模型，虽提升了检测精度，但其决策过程不透明，无法为执法和申诉流程提供可解释的证据。尤其是在本地生活O2O场景中，线上订单与线下履约紧密耦合，错误的判定可能误伤合法商家，损害平台公信力。因此，核心问题在于如何构建一个既能准确识别欺诈，又能生成可追溯、可审计推理路径的检测系统。本文提出的DeepScrub框架旨在解决这一矛盾，通过将大语言模型（LLM）与强化学习结合，实现可溯源的推理，从而在提升检测性能的同时，为风险审查工作流提供清晰的决策依据。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及三大类别。首先是**欺诈检测**领域，早期工作依赖专家规则和手工特征，后续机器学习方法从历史数据中学习行为模式，图方法则关注关联账户和社区。这些方法虽有效，但缺乏可解释的自然语言推理过程，而本文的DeepScrub通过LLM生成可追溯的推理路径，弥补了这一不足。其次是**LLM中的强化学习**，如RLHF、PPO、DPO、GRPO等方法主要用于通用偏好对齐或最终答案正确性，而本文针对虚假订单欺诈审查这一具体任务，设计了结合领域适应、任务特定奖励和SURE机制的训练框架，优化了推理轨迹的质量。最后是**可解释AI与工业应用**，现有可解释方法多为事后解释或特征重要性分析，本文则实现了决策与推理过程的同步生成，并在实际部署中验证了其减少人工审核工作量和提升效率的效果。总体而言，本文在方法上融合了LLM的语义理解、强化学习的优化能力以及领域知识的注入，在应用上聚焦于O2O平台的欺诈审查场景，与现有工作形成了明确区分。

### Q3: 论文如何解决这个问题？

DeepScrub 通过一个三阶段强化学习框架解决虚假订单欺诈检测中的可解释性问题。首先，**多模态语义统一模块**将异构风险信号（图结构、序列、表格）通过标准化模板转化为LLM可理解的文本描述，弥合模态鸿沟。其次，**领域知识注入**通过持续预训练在风险控制语料（含公开资料、治理材料和脱敏案例）上进行，以1:15的风险-通用数据比例平衡领域适应与通用能力保持，得到领域增强基座模型。核心创新在于**SUggest-REflect (SURE) 机制**：在训练中，策略模型首先生成候选响应（含推理过程和答案），然后通过双分支（内在或外在）建议模块——利用预训练的交易专家模型和风险控制专家模型提供反馈，驱动模型进行自我反思和迭代优化，生成修正后的响应。最终通过加权平均混合初始和最终响应的优势信号来指导策略更新。奖励设计上，除了格式奖励和准确率奖励（结合答案正确性、置信度权重和推理过程与专家推理的语义相似度），还引入**推理奖励**，通过计算条件概率和困惑度衡量推理过程对正确答案的贡献，并用关键词覆盖率防止奖励黑客行为。整体上，DeepScrub 实现了可追溯的推理路径，在真实数据集上macro-F1达85.3%，并在线上试点中将人工审核工作量降低94%。

### Q4: 论文做了哪些实验？

论文在真实O2O平台伪造订单欺诈检测数据集上进行了实验。实验设置包括：将训练集20%用于监督微调（SFT），80%用于强化学习（RL），学习率1e-5，预热比0.05，组大小6，在4个计算节点（32块高性能GPU）上训练约108小时。对比方法包括：未微调的Qwen3-32B通用大模型，以及InternLM3-8B-Instruct、Llama3-8B、GLM4-9B等开源模型（在相同数据上微调）。主要结果：DeepScrub的宏平均F1达85.3%，超过最佳基线2.7个百分点；在“商家刷单”最难子任务上F1为77.4%，比最佳微调基线（73.9%）高3.5个百分点；优化的8B模型性能超过32B模型。消融实验表明：去除RL后宏F1降至83.0%；去除SURE机制后宏F1降至83.7%（商家刷单F1降至75.5%）；去除准确率奖励导致最大下降（宏F1降至79.3%）；去除推理奖励使复杂场景性能下降。在四周线上试点中，DeepScrub达到91.8%精确率和88.5%召回率，比人工审核员分别提升16.6和38.8个百分点，减少94%人工审核工作量，每年节省近100万元人民币。

### Q5: 有什么可以进一步探索的点？

DeepScrub在O2O虚假订单检测中取得了显著成效，但仍存在若干可探索的方向。首先，其语义统一模块将异构信号转为文本描述，可能丢失数值型特征的细粒度信息，未来可引入多模态融合机制，如保留原始数值特征与文本表征的联合学习。其次，SURE机制依赖专家反馈和模型自检，但专家标注成本高且可能引入偏差，可探索基于主动学习的专家干预策略，或利用对比学习自动生成反事实推理路径。此外，当前仅针对单一欺诈场景，跨领域泛化性未验证，可尝试在物流、金融等不同风控任务中测试迁移能力。最后，推理路径的可追溯性虽增强可解释性，但未量化每条证据的贡献度，可引入Shapley值或注意力权重来评估各推理步骤的重要性，进一步提升审计透明度。

### Q6: 总结一下论文的主要内容

DeepScrub提出了一种基于大语言模型（LLM）的强化学习框架，用于解决O2O平台虚假订单欺诈检测中的可解释性不足问题。该方法首先通过语义统一模块将异构风险信号（如图、序列、结构化记录）转化为文本描述，使LLM能够理解；其次，利用风险控制语料进行持续预训练注入领域知识，并设计任务奖励联合优化预测正确性和推理质量；最后，引入SUggest-REflect（SURE）机制，结合专家反馈和模型自检迭代优化推理路径。在真实数据集上，DeepScrub的宏F1达到85.3%，优于基线2.7个百分点，且8B模型超越32B模型，表明领域适应比模型规模更重要。在四周线上试点中，精确率和召回率分别达91.8%和88.5%，较人工审核提升16.6和38.8个百分点，减少94%的一审工作量，年节省近100万元。该工作证明了LLM推理在工业风控中的可落地价值。
