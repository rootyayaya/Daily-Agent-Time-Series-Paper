---
title: "GRASP: GRanularity-Aware Search Policy for Agentic RAG"
authors:
  - "Varun Gandhi"
  - "Jaewook Lee"
  - "Shantanu Todmal"
  - "Franck Dernoncourt"
  - "Ryan Rossi"
  - "Zichao Wang"
  - "Andrew Lan"
date: "2026-07-11"
arxiv_id: "2607.10463"
arxiv_url: "https://arxiv.org/abs/2607.10463"
pdf_url: "https://arxiv.org/pdf/2607.10463v1"
categories:
  - "cs.AI"
  - "cs.IR"
tags:
  - "Agentic RAG"
  - "Tool Use"
  - "Multi-step Reasoning"
  - "Reinforcement Learning"
  - "Evidence Retrieval"
  - "Context Granularity"
  - "Search Policy"
relevance_score: 6.5
---

# GRASP: GRanularity-Aware Search Policy for Agentic RAG

## 原始摘要

Agentic retrieval-augmented generation (RAG) extends static RAG by allowing language models to iteratively reason, generate search queries, retrieve evidence, and predict answers. However, it remains challenging for models to decide when to retrieve, whether to use lexical matching or semantic similarity, and how to control context granularity to prevent irrelevant tokens from interfering with agent reasoning. In this paper, we introduce GRASP, a reinforcement learning (RL) framework for training agents to adaptively coordinate complementary retrieval tools during multi-step reasoning. GRASP provides the agent with semantic search, keyword search, and paragraph-reading actions, enabling it to retrieve sentence-level evidence and expand further context only when needed. We train the policy with a reward that jointly accounts for answer accuracy, grounded reading, complementary search, and turn efficiency. Experiments on multi-hop reasoning benchmarks show that GRASP improves both retrieval recall and downstream question answering performance compared with single-step retrieval, prompting-based agentic RAG, and RL-based retrieval baselines. Qualitative and ablation analyses show that the learned policy develops interpretable skimming and scanning behavior: it uses semantic search for broad exploration, paragraph reading for local verification, and keyword search for entity-specific evidence. These results suggest that learning to coordinate retrieval signals and context granularity is critical for agent's correct reasoning.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决现有检索增强生成（RAG）系统在复杂多跳推理任务中存在的关键问题。研究背景是，虽然静态RAG通过单次检索外部知识缓解了大模型的知识局限，但面对需要多步推理的复杂问题时，其固定、单步的检索流程无法根据中间推理状态动态调整。现有方法存在三大不足：第一，静态RAG即使检索到正确文档，粗粒度或含噪声的上下文块（chunk）也会引入干扰信息，导致模型推理时产生幻觉；第二，现有智能体RAG虽能迭代检索，但仍面临同样问题，且错误的检索决策会沿推理链传播放大错误；第三，现有方法通常使用单一检索器或固定粒度，无法在多步推理的不同阶段灵活协调词法匹配（如BM25）与语义相似性（如稠密检索）这两种互补的检索信号。因此，本文要解决的核心问题是：如何训练智能体RAG系统，使其在迭代推理过程中，能自适应地决定何时检索、使用哪种检索信号（词法或语义），以及控制返回证据的上下文粒度（如句子级或段落级），从而避免无关信息干扰推理，提升多跳问答的准确性与鲁棒性。

### Q2: 有哪些相关研究？

相关研究主要分为三类：**方法类**、**应用类**和**评测类**。

**方法类**方面，相关工作包括静态RAG（如BM25、密集检索和重排序器）和Agentic RAG。静态RAG采用单步检索，无法根据推理状态调整检索行为，且粗粒度块易引入噪声。Agentic RAG允许模型迭代检索，但现有方法通常使用单一检索器或固定块粒度，限制了多步推理中的适应性。本文GRASP通过强化学习训练策略，动态协调语义搜索、关键词搜索和段落阅读三种工具，并控制上下文粒度，与这些工作不同，它实现了检索信号和粒度的自适应选择。

**应用类**方面，相关工作聚焦于多跳推理问答。现有方法在检索到正确文档后仍可能因上下文噪声而幻觉，或无法利用互补检索信号。GRASP通过奖励设计（联合考虑答案准确率、接地阅读、互补搜索和轮次效率）提升了多跳推理性能，优于基于提示的Agentic RAG和基于RL的检索基线。

**评测类**方面，相关工作包括多跳推理基准测试。GRASP在这些基准上评估，并通过定性和消融分析展示了策略涌现的“略读”和“扫描”行为，类似于人类信息觅食，这与现有仅关注最终性能的评测不同，强调了检索策略的可解释性。

### Q3: 论文如何解决这个问题？

GRASP将Agentic RAG建模为有限步马尔可夫决策过程，通过强化学习训练策略模型自适应协调三种互补检索工具。核心框架包含三个主要模块：策略LLM、检索环境和奖励模型。策略LLM在每个推理步骤先生成推理片段，然后从动作空间选择动作，动作空间包括语义搜索(τ_s)、关键词搜索(τ_k)、段落阅读(τ_r)和终止回答(τ_a)。语义搜索使用稠密表征捕捉语义相似性，关键词搜索通过词汇匹配获取精确匹配证据，两者均返回句子级证据及其父段落标识符。段落阅读动作允许代理在需要时展开句子所属的完整段落，从而控制上下文粒度。

关键技术在于奖励函数设计，包含四个组成部分：答案准确性(R_A)使用预测答案与参考答案的token级F1分数；有依据阅读(R_R)评估代理是否从黄金文档而非干扰文档中读取段落；互补搜索(R_S)鼓励两种搜索工具都检索到黄金证据；轮次效率(R_E)在答案正确的前提下奖励较少的推理步数。总奖励R = R_A + 0.7R_R + 0.15R_S + 0.15R_E，确保答案准确性是主要驱动因素。

学习算法采用组相对策略优化(GRPO)，对每个查询采样G条轨迹，通过组内相对比较而非绝对奖励尺度更新策略。训练时屏蔽检索返回的观察token，仅对模型自生成token计算损失。实验表明该策略学会了可解释的略读和扫描行为：语义搜索用于广泛探索，段落阅读用于局部验证，关键词搜索用于实体特定证据。

### Q4: 论文做了哪些实验？

论文在三个多跳问答基准（HotpotQA、2WikiMultiHopQA、MuSiQue）上进行了实验，使用验证集作为测试集，从每个数据集中均匀采样500个问题。对比方法包括单步检索（词法、语义、混合检索）、基于提示的Agentic RAG（IRCoT，使用gpt5-mini生成CoT）和基于RL的检索基线（Search-R1，使用PPO和GRPO）。主要模型基于Qwen 2.5 3B Instruct，使用GRPO训练，检索深度为top-k=5。

检索召回率方面，GRASP在三个数据集上均表现最佳（HotpotQA: 0.90, 2Wiki: 0.90, MuSiQue: 0.70），显著优于单步混合检索（0.86, 0.60, 0.59）和Search-R1（最高0.77）。QA性能上，GRASP在EM、F1和LLM评判（JD）指标上全面领先，例如HotpotQA上EM=0.53、F1=0.66、JD=0.71，远超IRCoT（EM=0.24）和Search-R1（EM最高0.45）。消融实验表明，去除语义搜索（τ_s）导致EM下降0.072，去除段落阅读（τ_r）导致EM下降0.122，验证了互补搜索工具和上下文粒度的重要性。定性分析显示，学习到的策略形成了“语义搜索→段落阅读→关键词搜索”的类人浏览行为。

### Q5: 有什么可以进一步探索的点？

首先，论文在奖励设计上严重依赖金标准支持事实标注，这限制了其在缺乏此类标注数据集上的应用。未来可探索弱监督或自监督替代方案，例如利用答案归因或轨迹自一致性生成代理证据信号，从而将多工具强化学习扩展到更广泛的语料库。

其次，学习到的策略仍存在过早终止和检索不完整的问题。尽管工具调用次数趋于稳定，但策略偶尔会在必要证据未出现前就提交答案。未来应研究奖励塑形，对未检索到金标准证据集时的过早承诺进行惩罚，并引入辅助自我评估信号，允许模型在不确定时选择弃权而非猜测。

最后，实验仅基于单个3B参数模型，未探究模型规模对工具使用涌现行为的影响。未来应在1B、3B、7B和14B等不同规模下进行系统比较，以刻画规模与工具使用涌现之间的关系，并观察更大模型是否会学习到更激进的策略而跳过证据阅读。

### Q6: 总结一下论文的主要内容

GRASP提出了一种基于强化学习的粒度感知搜索策略，用于解决智能体RAG中检索时机、匹配方式与上下文粒度控制的核心问题。该方法将语义搜索、关键词搜索和段落阅读定义为可协调的检索动作，通过奖励函数联合优化答案准确性、证据溯源、互补检索和轮次效率。在多跳推理基准上的实验表明，GRASP在检索召回率和下游问答性能上均优于单步检索、提示驱动型智能体RAG及基于强化学习的基线方法。定性分析与消融实验揭示，学习到的策略形成了可解释的扫读与精读行为：语义搜索用于广泛探索，段落阅读用于局部验证，关键词搜索用于实体证据定位。该研究证明了协调检索信号与上下文粒度对智能体正确推理的关键作用，为构建更可靠的智能体RAG系统提供了新范式。
