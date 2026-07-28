---
title: "DeepFaith: Evidence-Grounded LLMs for Faithful Incident Reporting in Multi-Stage APT Defense"
authors:
  - "Trung V. Phan"
  - "Tri Gia Nguyen"
  - "Thomas Bauschert"
date: "2026-07-27"
arxiv_id: "2607.24348"
arxiv_url: "https://arxiv.org/abs/2607.24348"
pdf_url: "https://arxiv.org/pdf/2607.24348v1"
categories:
  - "cs.CR"
  - "cs.AI"
tags:
  - "LLM/Agent"
  - "可解释报告生成"
  - "证据路由"
  - "多阶段攻击诊断"
  - "时序语义报告"
  - "事后验证"
  - "工业安全"
  - "自然语言报告生成"
relevance_score: 8.5
---

# DeepFaith: Evidence-Grounded LLMs for Faithful Incident Reporting in Multi-Stage APT Defense

## 原始摘要

Advanced Persistent Threats (APTs) are difficult to detect and interpret due to their multi-stage and stealthy nature. While recent autonomous defense systems leverage provenance graphs and learning-based models for detection and mitigation, their outputs remain largely machine-oriented and difficult for analysts to interpret. Large language models (LLMs) offer a promising interface for report generation, but often produce hallucinated or weakly grounded content. In this paper, we propose DeepFaith, an evidence-grounded framework for faithful incident reporting in multi-stage APT defense. DeepFaith transforms structured outputs from autonomous defense and explainability modules into natural-language reports that are explicitly aligned with underlying system evidence. The framework integrates a unified evidence representation, evidence-grounded prompting, faithfulness-aware generation, and post-generation verification to ensure that all generated statements are supported. Experiments in a realistic enterprise testbed demonstrate that DeepFaith improves faithfulness from 0.68 to 0.92, reduces unsupported claims from 0.32 to 0.08, and increases temporal consistency from 0.6 to 0.88, while maintaining concise reports and lower error rates than existing template-based and LLM-based solutions. These results show that evidence-grounded generation enables reliable, interpretable, and actionable reporting for security operations centers.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

高级持续性威胁（APT）因其多阶段、隐蔽性强的特点，在检测与解释上极具挑战。现有基于溯源图和学习的自主防御系统虽能实现检测与缓解，但其输出（如潜在嵌入、概率分布）高度机器化，安全运营中心（SOC）的分析师难以直接理解。大语言模型（LLM）为生成可读报告提供了可能，但直接使用会产生幻觉或内容缺乏证据支持，尤其在安全关键领域可能导致错误结论。因此，核心问题在于：如何将自主防御与可解释性模块的结构化输出，转化为既信息丰富又能被系统证据严格支撑的、分析师友好的自然语言报告。现有方案要么是缺乏灵活性的模板法，要么是缺乏可靠性的LLM法。本文提出DeepFaith框架，旨在通过将报告生成视为受结构化证据约束的条件生成问题，并引入忠实度感知的生成与验证机制，弥合机器输出与人类可理解、可验证报告之间的鸿沟，实现可靠、可解释且可操作的APT事件报告。

### Q2: 有哪些相关研究？

相关研究可分为三类。**方法类**：一是基于溯源图的APT检测方法（如FLASH），利用图表示学习提升检测性能，但输出机器导向；二是强化学习自适应防御（如DeepStage），通过攻击阶段估计指导分层策略，但缺乏可解释性；三是可解释强化学习（XRL）与图神经网络可解释性（如GNNExplainer、DeepXplain），虽能提供结构/时间证据，但输出仍以机器为中心。**应用类**：LLM在安全运营中心（SOC）任务中的应用（如告警分类、日志分析、事件报告），但Kramer等发现完全自主的LLM摘要易产生幻觉和事实错误，人机协作更可靠。**评测类**：结构化文本生成研究强调忠实性、模式遵循和执行正确性，但领域通用，未考虑网络防御输出的阶段分布、溯源子图等特性。

本文与上述工作的核心区别在于：DeepFaith位于三者交叉点——利用DeepStage的防御输出和DeepXplain的证据对齐，通过统一证据表示、证据引导提示、忠实性感知生成和后验证，将机器输出转化为自然语言报告，将忠实性从0.68提升至0.92，显著减少无依据声明。

### Q3: 论文如何解决这个问题？

DeepFaith通过一个四阶段证据驱动框架解决LLM在APT事件报告中产生幻觉和弱证据支持的问题。核心方法是将自主防御系统输出的结构化证据（包括图结构、概率分布、时间索引和动作解释）转化为忠实于系统状态的自然语言报告。

整体框架包含四个主要模块：**证据序列化**、**证据驱动提示构建**、**忠实感知语言生成**和**验证与重生成**。首先，证据序列化模块将异构的结构化证据\(\mathcal{E}_t\)通过确定性函数\(\mathcal{S}(\cdot)\)转换为标准化的中间表示\(\tilde{\mathcal{E}}_t\)，包含阶段、时间、结构和动作四个语义字段，为LLM提供稳定的输入接口。其次，证据驱动提示构建模块将序列化证据组织成结构化提示\(\mathcal{P}_t\)，包含任务指令、证据字段和约束条件，强制模型输出必须基于证据。

在语言生成阶段，DeepFaith集成了三种关键技术：**忠实性损失**\(\mathcal{L}_{faith}=1-F(y_t,\mathcal{E}_t)\)惩罚无证据支持的声明；**阶段置信度分数**\(c_t\)被纳入提示，使模型能根据不确定性调整措辞（高置信度用肯定语气，低置信度用谨慎描述）；**紧凑性损失**惩罚超长输出，确保报告简洁。最后，验证与重生成模块计算忠实性分数\(F(y_t,\mathcal{E}_t)\)，若低于阈值\(\tau_F\)则触发重生成循环，形成防止幻觉的安全机制。

创新点在于：1）统一证据表示解决了异构数据与LLM的接口问题；2）证据驱动提示设计将结构化约束直接嵌入生成过程；3）后验证机制确保输出可靠性。实验表明，该方法将忠实性从0.68提升至0.92，无证据支持声明从0.32降至0.08，时间一致性从0.6提升至0.88。

### Q4: 论文做了哪些实验？

论文在模拟真实企业环境的测试平台上进行实验，该平台分为LAN、DMZ、服务器和管理四个区域，使用Auditd和Zeek收集主机和网络遥测数据，并通过CALDERA驱动的对抗性剧本模拟多阶段APT攻击。实验将DeepFaith与三种基线方法对比：基于模板的规则报告、普通LLM（LLaMA-2-13B）和思维链（CoT）提示。主要评估指标包括忠实度（F）、无依据声明率（UCR）、时间一致性（C_time）和报告长度。结果显示，DeepFaith在忠实度上达到0.92，显著优于模板（0.72）、普通LLM（0.68）和CoT（0.75）；UCR降至0.08，远低于其他方法（0.28-0.32）；时间一致性为0.88，高于普通LLM（0.60）和CoT（0.68）；报告长度仅130 tokens，与模板（120 tokens）相当，远短于普通LLM（180 tokens）和CoT（200 tokens）。消融实验表明，所有组件（如序列化、提示、忠实度约束、验证等）均对性能有贡献，移除任一组件都会导致指标下降。此外，使用不同大小的开源LLM（如Llama-3.2-3B、Qwen2.5-3B等）作为骨干网络时，DeepFaith仍能保持较高忠实度（0.84-0.90），验证了其可移植性。

### Q5: 有什么可以进一步探索的点？

DeepFaith在证据锚定生成方面取得了显著进展，但仍存在若干可探索的局限与方向。首先，当前框架依赖预定义的结构化证据表示，可能无法灵活适应未知或变异的APT攻击模式，未来可引入动态证据图谱构建机制，使系统能自动识别并整合新型攻击线索。其次，验证机制虽降低了幻觉率，但仅基于事后检查，缺乏生成过程中的实时纠偏，可探索在线约束解码或强化学习策略，在生成每一步即确保与证据对齐。此外，报告生成目前为单向输出，未来可构建交互式人机协同系统，允许分析师通过自然语言提问或修正，LLM据此动态调整报告内容并更新证据链。最后，当前实验环境为模拟企业网络，真实场景下的噪声数据与不完整日志会挑战证据质量，需研究鲁棒性更强的证据筛选与置信度评估方法。

### Q6: 总结一下论文的主要内容

DeepFaith提出了一种基于证据的框架，用于在多阶段APT防御中生成忠实且可解释的事件报告。该框架解决了现有自主防御系统输出机器导向、难以被分析师理解，以及大语言模型生成内容易产生幻觉或缺乏证据支撑的问题。DeepFaith通过集成统一证据表示、证据引导提示、忠实感知生成和后生成验证，确保所有报告陈述均与底层系统证据对齐。在真实企业测试床上的实验表明，DeepFaith将忠实度从0.68提升至0.92，无根据声明率从0.32降至0.08，时间一致性从0.6提升至0.88，同时保持报告简洁且错误率低于基于模板和LLM的基线方法。核心贡献在于证明了结构化证据集成而非模型规模是实现可靠、可解释且可操作安全报告的关键，为安全运营中心提供了更高效、更可信的自动化报告生成方案。
