---
title: "Automated Testing of LLM-Based Post Hoc Explainers Using Model Checking as an Oracle"
authors:
  - "Dennis Gross"
  - "Helge Spieker"
date: "2026-08-31"
arxiv_id: "2608.30581"
arxiv_url: "https://arxiv.org/abs/2608.30581"
pdf_url: "https://arxiv.org/pdf/2608.30581v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "LLM解释器"
  - "模型检测"
  - "自动化测试"
  - "自然语言解释"
  - "顺序决策"
  - "忠实性评估"
  - "测试用例生成"
  - "MDP环境"
relevance_score: 6.5
---

# Automated Testing of LLM-Based Post Hoc Explainers Using Model Checking as an Oracle

## 原始摘要

Large language models (LLMs) are used as post hoc explainers of sequential decision-making policies, producing natural-language explanations of why an action was chosen. However, LLMs often generate plausible but incorrect statements, and no existing approach systematically tests whether such explanations are faithful to the underlying environment. Two classic software testing challenges stand in the way: there is no oracle for the correctness of an explanation, and the test inputs, natural language queries about a policy's behavior, lack the structure needed for systematic test case generation. We address both. Probabilistic model checking provides the test oracle, computing exact reference results against which LLM answers are graded automatically. A taxonomy of post hoc query categories structures the input space around the environment-level facts from which policy explanations are composed; test cases generated from it are prioritized by question-specific diagnostic difficulty scores. Across seven MDP environments, the testing separates three open-weight LLMs: a reasoning model passes 85% of test cases, a mid-size model 70%, and a 1B model falls below the random baseline, while prioritization surfaces significantly harder cases than random selection. Our results indicate how trustworthy LLM-generated explanations are in model-free settings, where the same LLMs are used but no oracle exists to verify them.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

大型语言模型（LLM）被用作序列决策策略的事后解释器，生成自然语言解释以说明为何选择某个动作。然而，LLM经常产生看似合理但错误的陈述，且现有方法缺乏系统性测试机制来验证这些解释是否忠实于底层环境。这带来两大软件测试挑战：一是缺乏测试预言机，判断解释正确性需知道环境和策略的真实属性；二是输入空间非结构化，难以确定哪些解释查询类型值得测试。因此，尽管已有工作评估LLM解释甚至用于提升策略性能，但尚无方法系统测试LLM是否真正理解环境并生成忠实解释。

本文提出自动化测试方法，通过概率模型检查提供精确参考结果作为测试预言机，自动评判LLM回答；并引入事后查询分类法结构化输入空间，基于环境级事实生成测试用例，按问题特定诊断难度分数排序。该方法在七个MDP环境中区分了三个开源LLM，验证了LLM生成解释的可信度，并推断其在无模型设置中的可靠性。

### Q2: 有哪些相关研究？

本文的相关研究主要分为四类：

**1. 顺序决策的可解释性（XRL）**：包括策略摘要、显著性图、奖励分解等传统方法，以及近期利用LLM生成事后解释的工作。这些方法聚焦于“生成”解释，而本文关注“测试”解释是否忠实于环境，这是本质区别。

**2. LLM作为事后解释器**：已有工作用LLM为策略生成自然语言解释，但评估仅依赖人类研究或LLM-as-a-judge等近似参考。本文首次引入概率模型检查的精确结果作为ground truth，并按查询类别分类评估，避免了主观偏差。

**3. LLM测试与评估**：涵盖行为测试套件、幻觉基准及PlanBench等可验证基准。这些工作测试的是LLM自身的任务能力，而本文测试的是LLM对“另一个系统”（策略）决策解释的忠实性，对象不同。

**4. AI系统的模型检查**：已有工作用概率模型检查验证策略的PCTL性质，或结合LLM生成反事实、验证策略本身。但本文的独特之处在于，模型检查不直接验证策略，而是作为测试预言机，为LLM生成的解释提供精确的评分基准。

综上，本文的核心创新在于将模型检查从“验证策略”转向“验证解释”，填补了LLM解释忠实性系统化测试的空白。

### Q3: 论文如何解决这个问题？

该论文提出了一种系统化测试LLM作为事后解释器的方法，核心创新在于用概率模型检验构建测试预言机，解决了解释正确性无参照和测试输入缺乏结构两大挑战。

整体框架包含四个阶段：**预言机构造**、**测试用例生成与优先级排序**、**测试执行**和**判定**。首先，对MDP和PCTL属性进行模型检验，为每个可达状态计算出属性结果V(s)、动作值Q(s,a)和危险度D(s)，从而推导出最优动作集、瓶颈状态等期望答案。其次，基于查询分类法（对象/范围/模式）生成测试用例，并通过诊断难度分数δ进行优先级排序——δ设计了三种机制：模糊性（候选值接近难以区分）、选择性（正确答案少而干扰多）和显著性（存在模仿真实结构的诱饵）。例如，最佳动作查询的δ=1-|A*(s)|/|Act(s)|，最优动作越少难度越高；瓶颈查询则用瓶颈中心度C_B(s)衡量。

测试执行阶段，每个测试用例通过提示模板渲染为自然语言查询，发送给被测LLM并重复多次以应对随机性。判定阶段自动将LLM回答与预言机精确比较：概率答案比对V(s)，动作排名比对真实排序（允许并列），瓶颈判断比对精确瓶颈集合。该方法在七个MDP环境中成功区分了三个开源LLM的能力差异，证明其能有效评估无模型场景下LLM解释的可靠性。

### Q4: 论文做了哪些实验？

论文围绕三个研究问题展开实验：诊断优先级排序是否有效（RQ1）、更强LLM是否通过更多测试（RQ2）、查询类别难度是否有差异（RQ3）。实验设置采用7个MDP环境（Frozen Lake、Wolf–Goat–Cabbage、Water Jug、Transporter、Stock Market、Job Shop、Dam），每个环境配对一个可达性属性，用Storm模型检查器计算精确参考结果作为测试预言。测试了三个开源权重模型：Gemma 3 1B、Qwen3.5（推理模式）和Gemma 4 31B，以均匀随机回答为基线，最优策略为上限。协议为温度0贪心解码，每类别20个状态，答案限制为结构化JSON，分数为通过测试比例。

主要结果：诊断优先级排序在220个可比单元中，75个（34.1%）产生更难案例，Wilcoxon符号秩检验p=0.035，确认优先级排序有效（RQ1）。平均性能上，Qwen3.5最强（0.85），Gemma 4 31B次之（0.70），均高于随机基线（0.51），而Gemma 3 1B在优先级排序下仅0.43，低于随机，但在随机选择下升至0.55，表明其缺陷仅在诊断性查询下暴露（RQ2）。类别难度上，最难的为dead ends in subset（0.59）和worst action（0.60），最易的为二元bottleneck查询（0.72），证实类别间难度存在显著差异（RQ3）。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下方向展开：首先，当前测试环境均为有限状态MDP和记忆less策略，可扩展至部分可观测环境（POMDP）或连续状态空间，以检验LLM在更复杂动态下的解释忠实性。其次，测试查询仅覆盖最优性、安全性等基础类别，可引入因果归因、反事实推理等更深层解释类型，并设计联合查询（如同时询问多步决策链）以暴露LLM的推理断裂。第三，诊断难度分数目前依赖人工设计的启发式规则，可尝试用元学习或对抗生成方式自动发现“陷阱”状态，提升测试效率。此外，当前仅评估单轮回答，可引入多轮对话式追问机制，检测LLM在交互中修正错误解释的能力。最后，将测试框架与可解释性方法（如SHAP值）结合，构建更细粒度的归因基准，并探索用测试结果微调LLM，使其在无模型场景下主动标注不确定性，从而提升实际部署中的可信度。

### Q6: 总结一下论文的主要内容

本文提出了一种自动化测试LLM作为事后解释器的方法，针对顺序决策策略生成的自然语言解释缺乏忠实性验证的问题。核心挑战在于缺乏测试预言机（判断解释正确性的标准）和输入空间非结构化。作者采用概率模型检查作为预言机，通过PCTL时序逻辑精确计算环境属性（如最优动作、安全性），自动评判LLM回答；同时提出事后查询分类法，按环境事实结构化输入空间，并依据问题特异性诊断难度（如非最优动作比例）对测试用例排序。在七个MDP环境中评估三个开源LLM：推理模型通过85%测试，中型模型70%，1B模型低于随机基线，且优先级排序显著提升难度。该工作意义在于，通过受控环境下的精确验证，揭示了LLM解释在无模型场景中的可信度边界，为可解释AI的可靠性测试提供了系统化框架。
