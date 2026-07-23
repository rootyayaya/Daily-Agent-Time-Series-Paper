---
title: "MOF-Sleuth: Tool-Grounded Reward Alignment for Explainable Fine-Grained MOF CIF Auditing"
authors:
  - "Yu Liu"
  - "Zhiwei Yang"
  - "Diandian Guo"
  - "Kun Peng"
  - "Fangfang Yuan"
  - "Cong Cao"
  - "Chaozhuo Li"
  - "Zhiyuan Ma"
  - "Yanbing Liu"
  - "Guobin Zhao"
date: "2026-07-22"
arxiv_id: "2607.19935"
arxiv_url: "https://arxiv.org/abs/2607.19935"
pdf_url: "https://arxiv.org/pdf/2607.19935v1"
categories:
  - "cs.AI"
tags:
  - "LLM/Agent for 时序诊断"
  - "工具调用与证据路由"
  - "可解释故障诊断"
  - "强化学习对齐"
  - "化学/材料领域诊断"
  - "证据驱动解释"
  - "细粒度归因"
relevance_score: 7.5
---

# MOF-Sleuth: Tool-Grounded Reward Alignment for Explainable Fine-Grained MOF CIF Auditing

## 原始摘要

Large metal-organic framework (MOF) databases support simulation, screening, and machine learning through crystallographic information files (CIFs). Subtle chemical and structural errors in these inputs can compromise downstream results and hinder manual inspection. LLM advances in computational chemistry offer paths beyond predictive screening toward fine-grained diagnosis with evidence-grounded explanations. However, two challenges remain: (i) limited fine-grained attribution: MOF-specific validators and machine-learning models scale detection but provide fixed checks, readiness scores, or coarse labels rather than evidence-grounded explanations; and (ii) unreliable CIF reasoning: direct LLM auditing is costly and unreliable because chemical evidence is implicit across atom-site records and requires geometric, connectivity, occupancy, and charge calculations. Both stem from weak coupling between chemical evidence and language-model explanation. We introduce MOF-Sleuth, a reinforcement-guided CIF auditing agent with two modules: a deterministic Forensic Lab and a Sleuth reasoning engine. The Lab derives composition, geometry, connectivity, occupancy, coordination, and charge evidence, and Sleuth uses this evidence to produce an evidence-grounded explanation, error types, and a binary decision. Reward-guided reinforcement learning (RL) turns tool measurements into chemical explanation-level supervision, rewarding not only the final answer but also cited chemical evidence and evidence-supported diagnoses. We introduce Chemically Grounded Diagnosis (Chem-GD), a metric that assesses whether a correct diagnosis is explained by factual, relevant CIF-derived evidence. Across four benchmarks, MOF-Sleuth establishes state-of-the-art performance among LLM-based approaches and MOF-specific machine-learning methods, demonstrating gains in detection, attribution, and grounded explanation quality.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决金属有机框架（MOF）晶体学信息文件（CIF）在自动化审计中缺乏细粒度归因与可解释性的核心问题。研究背景在于，大型MOF数据库依赖CIF进行高通量模拟与机器学习，但CIF中常存在原子缺失、电荷不平衡、配位不合理等细微错误，这些错误会无声地影响下游结果。现有方法存在明显不足：一方面，MOFChecker等规则验证器和机器学习模型虽能规模化检测，但仅提供固定检查、就绪评分或粗粒度错误类别，无法给出基于证据的细粒度解释；另一方面，直接使用大语言模型（LLM）进行审计成本高昂且不可靠，因为化学证据隐含在原子位点记录中，需要几何、连接性、占据率和电荷计算等客观推导，而LLM缺乏计算基础，易产生幻觉或无关解释。因此，本文要解决的核心问题是：如何实现MOF CIF审计的细粒度错误分类与归因，同时生成基于证据的化学解释，从而弥合化学证据与语言模型解释之间的弱耦合。

### Q2: 有哪些相关研究？

相关研究主要分为三类：**AI for MOFs与CIF可靠性**、**LLM与智能体科学推理**、以及**强化学习结构化推理**。

在**AI for MOFs**领域，现有工作如MOFChecker（几何/电荷检查）、MOSAEC（金属氧化态不一致性）、MOFClassifier（可读性分数）、SETC（质子/电荷/无序分类）和LitMOF（多源LLM智能体修复），均侧重于固定规则检查、标量分数或粗粒度分类，缺乏细粒度归因和基于证据的解释。MOF-Sleuth则通过确定性取证实验室和强化学习，实现了证据支撑的细粒度诊断。

在**LLM与智能体科学推理**方面，CoT、ReAct、Reflexion、AutoGen、MetaGPT等提升了推理和工具使用能力，但直接用于CIF审计时，因化学证据隐式分布在长表格中，易产生无依据的生成。MOF-Sleuth通过工具-证据对齐和奖励引导，确保了诊断的化学事实基础。

在**强化学习结构化推理**中，PPO、GRPO、DeepSeek-R1等优化了数学推理的最终答案，但未涉及化学审计所需的错误归因、模式一致性和事实支撑。MOF-Sleuth引入Chem-GD指标，奖励化学证据引用和诊断支持，填补了这一空白。

### Q3: 论文如何解决这个问题？

论文通过构建MOF-Sleuth智能审计代理来解决MOF CIF文件中的细粒度化学错误诊断与可解释性问题。核心方法分为两大模块：**Forensic Lab（法医实验室）** 和 **Sleuth（侦探推理引擎）**。

**整体框架**：首先，Forensic Lab将原始CIF文件转化为结构化的化学证据报告，包含客观事实、硬标志、诊断信号、上下文和引用别名。然后，Sleuth引擎基于该报告进行语义推理，输出证据驱动的解释、15种细粒度错误类型集合以及二元判定（有误/无误）。

**主要模块与关键技术**：
1.  **Forensic Lab**：包含8个确定性化学工具（如周期性几何计算、连接性分析、电荷账本检查等），负责提取组成、几何、连接性、占据率、配位和电荷等证据。其输出是纯结构化的、可验证的事实库，不直接给出最终判定，从而将计算密集型操作从语言模型中剥离。
2.  **Sleuth推理引擎**：接收Forensic Lab的报告，进行语义推理。其输出受模式约束，确保解释和归因必须基于报告中的证据。
3.  **奖励引导的强化学习（GRPO）**：这是关键创新。论文设计了六项确定性验证奖励，分为任务、模式和诊断三大类。其中，**R_grd（证据基础奖励）** 验证解释中引用的化学事实是否真实存在于报告中；**R_evid（诊断证据奖励）** 验证预测的错误类型是否被工具导出的结构信号支持。这直接将工具测量转化为化学解释级别的监督，惩罚虚构证据或缺乏支持的诊断。
4.  **Chem-GD指标**：提出了化学基础诊断指标，严格评估正确诊断是否由相关且可验证的CIF证据解释，实现了无需模型评判的客观可解释性度量。

**创新点**：核心在于将确定性化学工具与LLM的语义推理通过奖励对齐紧密结合，解决了LLM直接审计时化学证据隐式、不可靠的问题，实现了细粒度归因和证据驱动的可解释诊断。

### Q4: 论文做了哪些实验？

论文在四个基准测试（CoRE-MOF 2019、CoRE-MOF 2026、ToBaCCo、QMOF）上评估了MOF-Sleuth，涵盖分布内、平衡OOD和不平衡场景。对比方法包括四组：开源原始CIF LLM（Qwen3 4B/8B/30B-A3B、Gemma-4-31B）、前沿API模型（DeepSeek-v4-Pro、GPT-5.5、Claude-Sonnet-4.6）、13种通用Agent框架（如Self-Consistency、Reflexion、AutoGen等）以及MOF专用验证器（MOFChecker 2.0、MOFClassifier、SETC-GAT）。主要指标包括二元检测的准确率（Acc）和平均召回率（Avg. Rec）、四父类归因的Type-Hit Acc，以及联合衡量诊断正确性与解释质量的Chem-GD。

主要结果：MOF-Sleuth在三个指标上达到最优：平均准确率0.781、Type-Hit Acc 0.712、Chem-GD 0.713。相比之下，最强API模型GPT-5.5直接读取CIF仅达0.698准确率，通用Agent框架平均准确率仅0.410-0.487。消融实验显示，使用Forensic Lab报告替代原始CIF将平均准确率从0.441提升至0.568，Chem-GD从0.055提升至0.229；奖励引导对齐进一步将准确率提升至0.781，Chem-GD提升至0.713。与MOF专用验证器相比，MOF-Sleuth的准确率（0.943）显著优于MOFChecker等（0.710-0.785），且能生成可解释归因。专家验证显示，MOF-Sleuth的判决一致性达0.930（κ=0.860），归因准确率0.700。

### Q5: 有什么可以进一步探索的点？

MOF-Sleuth在证据归因和解释质量上取得了显著进展，但仍有几个可探索的方向：首先，当前Forensic Lab依赖确定性规则，对非常规配位模式或无序结构可能产生错误证据，未来可引入图神经网络或密度泛函理论辅助验证，增强证据的鲁棒性。其次，奖励设计仅关注化学证据引用和诊断正确性，未考虑解释的简洁性或可读性，可加入语言质量奖励项，避免冗长或歧义输出。第三，模型在跨数据库泛化上未充分验证，不同MOF数据库的CIF格式差异可能导致证据提取失败，需设计自适应解析器。最后，当前仅处理单个CIF审计，未来可扩展为批量对比审计，例如检测同一MOF不同版本间的差异，或结合主动学习优先审计高不确定性样本，提升工业场景实用性。

### Q6: 总结一下论文的主要内容

MOF-Sleuth提出了一种基于强化学习奖励对齐的LLM Agent框架，用于对金属有机框架（MOF）的晶体信息文件（CIF）进行细粒度、可解释的审计。现有方法要么依赖固定规则或粗粒度标签，无法提供证据支撑的解释；要么直接使用LLM审计，因化学证据隐含于原子位点记录中而不可靠。该框架包含两个模块：确定性取证实验室（Forensic Lab）从CIF中提取组成、几何、连接性、占有率、配位和电荷等化学证据；Sleuth推理引擎利用这些证据生成证据支撑的解释、错误类型和二元决策。通过奖励引导的强化学习，将工具测量结果转化为化学解释级别的监督信号，不仅奖励最终答案，还奖励引用的化学证据及其支撑的诊断。论文还提出了化学基础诊断（Chem-GD）指标，用于评估正确诊断是否基于事实相关的CIF证据。在四个基准测试中，MOF-Sleuth在检测、归因和可解释性方面均优于现有LLM方法和MOF专用机器学习方法，实现了从二元有效性筛查到细粒度、可解释诊断的跨越。
