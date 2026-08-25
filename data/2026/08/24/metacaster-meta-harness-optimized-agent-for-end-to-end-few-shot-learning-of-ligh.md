---
title: "MetaCaster: Meta-Harness-Optimized Agent for End-to-End Few-Shot Learning of Lightweight Time Series Forecasters"
authors:
  - "ChengAo Shen"
  - "Wenchao Yu"
  - "Fangyu Wu"
  - "Dongjin Song"
  - "Hanghang Tong"
  - "Dongsheng Luo"
  - "Wei Cheng"
  - "Haifeng Chen"
  - "Jingchao Ni"
date: "2026-08-24"
arxiv_id: "2608.23473"
arxiv_url: "https://arxiv.org/abs/2608.23473"
pdf_url: "https://arxiv.org/pdf/2608.23473v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "多智能体框架"
  - "少样本学习"
  - "轻量级时序预测器"
  - "数据生成"
  - "元优化"
  - "时序预测"
  - "资源受限场景"
  - "文本上下文"
relevance_score: 8.5
---

# MetaCaster: Meta-Harness-Optimized Agent for End-to-End Few-Shot Learning of Lightweight Time Series Forecasters

## 原始摘要

Time series forecasting (TSF) is evolving toward multimodal and agentic settings, yet using foundation models remains uneconomical in resource-constrained scenarios, where compact, specialized forecasters are more desirable. However, lightweight forecasters typically require substantial training data, limiting their use in domains with scarce, slowly accumulated, or privacy-sensitive time series. To address this dilemma, we investigate the challenging problem of few-shot learning for lightweight forecasters. We propose MetaCaster, a meta-harness-optimized multi-agent framework that uses agentic data generation to automatically train specialized lightweight forecasters from only a few examples and textual contexts. Our work highlights a new TSF paradigm in which agents act not as forecasters but as intermediary engineers that prepare efficient, task-specific forecasters for deployment. Experiments on 18 datasets, 23 state-of-the-art lightweight forecasters, and 14 baselines demonstrate that MetaCaster achieves both data efficiency and computational efficiency while maintaining high-quality TSF performance.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列预测正朝着多模态与智能体方向发展，但现有基于LLM的预测方法存在两大局限：一是LLM作为预测器面临离散语言与连续数值的模态鸿沟，性能常不及专用数值模型；二是大型模型（如LLM或时间序列基础模型）在资源受限场景下部署成本高、碳排放大。相比之下，轻量级预测器虽在单任务上可媲美大模型，却依赖大量下游训练数据，在数据稀缺、积累缓慢或隐私敏感领域（如医疗、金融）难以应用。本文核心问题是：能否仅凭少量样本高效训练轻量级预测器？为此提出MetaCaster框架，采用元驾驭优化的多智能体机制，通过智能体生成增强数据并自动训练专用轻量预测器，而非让智能体直接预测。该框架首次将数据生成与预测器质量对齐，实现了数据效率与计算效率的双重提升，为资源受限场景下的时间序列预测提供了新范式。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**LLM-based TSF**：现有工作多采用“LLM-As-Forecaster”或“Agent-As-Forecaster”范式，直接让大模型或智能体进行预测，部分多任务时序QA智能体也能通过推理完成预测。少数“Agent-As-Engineer”方法虽使用Harness生成预测器，但既不生成时间序列（需大量训练数据），也不自动优化Harness，与本文的端到端元优化框架形成本质区别。**时间序列生成**：包括数据增强、生成式分布建模及语言条件生成等方法，但这些独立生成器仅模拟数据属性，不直接优化下游预测性能，而MetaCaster以预测精度为最终目标，通过智能体生成数据并训练轻量模型，填补了生成与预测之间的鸿沟。**Agent Harness优化**：近期研究证明改进智能体的基础设施层（即Harness）比单纯提升模型更有效，催生了文本与Harness自动优化技术。但现有时序智能体多依赖监督微调或强化学习，本文首次将自动Harness优化引入时间序列智能体，属于该方向的开创性工作。整体而言，MetaCaster创新性地将智能体定位为“工程师”而非“预测者”，通过元级Harness优化实现数据与计算双高效。

### Q3: 论文如何解决这个问题？

MetaCaster提出了一种元驾驭优化的多智能体框架，用于从极少样本和文本上下文中自动训练轻量级时间序列预测器。其核心思想是让智能体充当“中间工程师”，而非直接预测者，通过生成数据来训练任务特定的预测器。

整体框架包含三个关键组件：**Meta-Generator**（第一智能体）、**Forecaster Trainer**（第二智能体）和**Harness Proposer**（第三智能体）。Meta-Generator以可替换的LLM为核心，不直接生成时间序列，而是利用其规划、推理和编码能力，通过驾驭（Harness）创建TS-Generator程序，该程序整合领域知识、规则和模型来生成数据。它分析支持集数据、生成候选数据并执行质量检查，若未通过则修订生成器。Forecaster Trainer负责将生成的数据按比例划分为训练集和验证集，调度计算资源并行训练23种轻量级预测器（如MixLinear、TSMixer、FITS），并评估其性能。Harness Proposer是元优化器，通过三个阶段（自规划分析、诊断、更新）自动编辑Meta-Generator的驾驭参数（系统提示和技能），以最小化生成数据训练与真实数据训练预测器之间的性能差距，采用基于铰链损失的度量来引导优化。

创新点在于：一是提出“智能体作为工程师”的新范式，而非直接预测；二是采用元驾驭优化策略，冻结LLM而优化其提示和技能，使生成的数据直接针对下游预测性能优化，而非仅追求数据真实性；三是推理阶段仅保留轻量级预测器，丢弃所有智能体，实现高效部署。

### Q4: 论文做了哪些实验？

实验基于GIFT-Eval基准，涵盖18个数据集、9个领域，划分为8个训练集、7个域内测试集和3个域外测试集。时间序列按80%/10%/10%划分，回看窗口设为336，预测步长为192。对比方法包括5种生成模型（TimeVAE、DiffTS、T2S、TimeDP、VerbalTS）、4种增强技术（Repeat、Bootstrap、Jitter、MagWarp）、4种预训练基础模型（Chronos、Moirai、VisionTS、Time-LLM）及Agent流水线TimeScientist。实验在K=10/30/50样本下进行，以MSE和MAE为指标。

主要结果：MetaCaster在多数数据集上优于生成/增强基线，性能随K增大而提升；K≥30时接近甚至超越全量训练效果，表明优化数据可提升训练质量；K=10时仍具竞争力，且能良好泛化至域外数据。与TimeScientist相比，后者因无法生成数据而性能不随K扩展。在Solar数据集K=30时，MetaCaster以243参数的MixLinear模型实现与基础模型相当的性能，延迟降低10³倍、参数量减少10⁵倍。消融实验显示，用MMD/Wasserstein距离替代预测目标优化会降低性能，移除上下文线索显著恶化结果，而不同LLM（GPT-5.4、Gemini-3.1-Pro等）表现相近，说明Harness优化是关键。

### Q5: 有什么可以进一步探索的点？

当前工作主要局限在极端零样本场景的缺失，即无任何参考序列时，代理缺乏目标域的统计锚点，生成数据可靠性不足。未来可探索将预训练TSFM的嵌入知识作为先验注入生成器，或设计自适应检索机制从外部库中匹配相似域样本，以缓解冷启动问题。其次，实验域覆盖有限，可扩展至TSFM完整预训练语料，验证跨域泛化能力，并优化Harness对不同数据分布的适应策略。此外，轻量预测器库的更新滞后于新模型涌现，可引入动态模型注册与自动评估管线，使代理能实时集成最新架构。最后，当前代理主要依赖文本上下文，可尝试融合多模态信号（如传感器统计特征、领域图谱）增强生成多样性，并探索元学习与强化学习结合，使Harness在迭代中自主调整生成策略，进一步提升数据效率与预测精度。

### Q6: 总结一下论文的主要内容

本文提出MetaCaster，一种面向轻量级时间序列预测器的元框架优化多智能体系统，解决资源受限场景下小样本学习难题。其核心贡献在于颠覆传统范式：智能体不作为预测器，而作为“中间工程师”，仅凭少量样本和文本上下文，自动完成数据生成、预测器训练、参数调优和模型选择的全流程。方法上，MetaCaster通过元框架优化协调多智能体协作，实现端到端自动化，兼顾数据效率与计算效率。实验覆盖18个数据集、23种轻量级预测器和14个基线，验证了该方法在保持高质量预测性能的同时，显著降低对训练数据的依赖。该工作为智能体时间序列预测开辟了“智能体即工程师”的新方向，对隐私敏感或数据积累缓慢的工业场景具有重要应用价值。
