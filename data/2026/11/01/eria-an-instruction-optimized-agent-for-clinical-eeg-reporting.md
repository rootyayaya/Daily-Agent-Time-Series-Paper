---
title: "ERIA: An Instruction-Optimized Agent for Clinical EEG Reporting"
authors:
  - "Ahmed Sameh"
  - "Gayal Kuruppu"
  - "Neeraj Wagh"
  - "Bridger Brundy"
  - "Yogatheesan Varatharajah"
date: "2026-11-01"
arxiv_id: "2611.01394"
arxiv_url: "https://arxiv.org/abs/2611.01394"
pdf_url: "https://arxiv.org/pdf/2611.01394v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "LLM Agent"
  - "工具调用"
  - "时序报告生成"
  - "临床EEG分析"
  - "指令优化"
  - "可追溯诊断"
  - "信号处理工具"
  - "自然语言策略优化"
relevance_score: 8.5
---

# ERIA: An Instruction-Optimized Agent for Clinical EEG Reporting

## 原始摘要

Clinical EEG interpretation requires integrating technical quality, background and behavioral states, interictal and ictal abnormalities, and overall clinical context across long recordings. We introduce ERIA (EEG Reporting and Instruction-Optimized Agent), a locally deployable framework in which a single 27B language-model controller analyzes whole-recording EEGs by orchestrating specialized parametric and signal-processing tools. ERIA combines learned tools for background abnormality, sleep-wake state, seizure-like activity, and interictal epileptiform discharges with deterministic spectral, amplitude, symmetry, montage, and signal-quality analyses. Rather than fine-tuning the controller or using multi-agent orchestration, ERIA keeps the controller weights, specialist tools, and safety constraints fixed and optimizes only its natural-language analysis policy with GEPA (Genetic-Pareto), using feedback from expert-written EEG reports. GEPA improves physician-aligned whole-recording report quality over the raw policy, and the optimized policy transfers to external EEG benchmarks. On CerebraGloss-Bench and BrainBench Foundational Analysis, ERIA remains competitive with the models evaluated in the original benchmarks. These results show that specialist tools and language-level policy optimization can extend the clinical and general EEG capabilities of a single locally executable model while preserving local inference and traceable tool use.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决临床脑电图（EEG）解读自动化中的核心矛盾：如何在不依赖超大模型或复杂部署架构的前提下，实现符合临床报告规范、可本地部署且证据可追溯的全记录EEG分析。

研究背景方面，EEG是癫痫等神经系统疾病的基础检查手段，但专家对长时多通道记录的视觉审阅耗时费力且易出错。ACNS指南要求临床EEG报告不仅检测事件，还需系统整合技术质量、行为状态、背景活动、发作间期与发作期异常，并综合为临床解释，因此本质上是“全记录报告”问题。

现有方法存在两类不足：一是EEG-语言系统（如EEGtoText、CELM、CerebraGloss）虽能生成临床描述，但能力被固化在固定学习模型或推理流程中，控制器无法主动选择、组合和回溯互补的专家分析；二是智能体方法（如EEGAgent、BrainAgent、NS-Copilot）虽提升了证据获取的灵活性，却通常依赖超大控制器、托管前沿模型、多智能体协作或较重的闭环执行，且其全记录临床报告质量尚未与医师撰写的配对参考进行严格评估。

因此，本文提出ERIA，用单一27B控制器编排专业参数化与信号处理工具，在保持控制器权重、专家工具和安全约束固定的条件下，仅通过GEPA优化自然语言分析策略，以医师报告为反馈信号，直接以全记录临床解读质量为优化目标，兼顾本地推理与可追溯的工具使用。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类。方法类上，EEG-to-language 方向中，EEGtoText 通过预测预定义 EEG 表型生成结构化报告，并用注意力定位支持信号区域；CELM 将长时程 EEG 编码为与本地语言模型对齐的潜在表示，再解码为结构化临床报告；CerebraGloss 则在渲染的 EEG 波形与临床指令-响应对上微调视觉语言模型，实现短片段细粒度解读。与这些工作不同，ERIA 不依赖固定的学习式 EEG-to-language 通路，而是由控制器在推理时动态调用可独立解释的专家工具。应用类上，EEGAgent 是最接近的前身，但使用 235B 大控制器且仅作可行性研究，分析策略未经临床报告反馈优化；BrainAgent 采用分层多智能体架构，NS-Copilot 协调多个 GPT-5.2 智能体完成模型选择与重规划。ERIA 则以单个本地可执行的 27B 控制器，通过改进工具使用策略而非增加智能体或规模来提升能力。评测类上，BrainBench 提供指令条件下的多域 EEG 分析基准，CerebraGloss-Bench 亦用于评测；ERIA 在这些基准上与原始评测模型保持竞争力。优化类上，Reflexion、Self-Refine 与 GEPA 通过语言反馈改进模型行为而不改权重，ERIA 将 GEPA 用于优化临床 EEG 的证据获取、验证与综合策略，并以专家报告作为反馈信号。

### Q3: 论文如何解决这个问题？

ERIA 的核心思路是“冻结模型、只优化语言策略”。整体框架为单控制器 Agent：本地部署的 Qwen3-27B 控制器采用 ReAct 式推理-行动循环，不直接读取波形，而是接收用户请求、选择工具、观察结构化输出并迭代收集证据，直至合成结构化 EEG 报告。系统提示被拆为固定部分与可变分析策略：固定部分规定系统范围、安全约束与证据接地规则（学习模型输出只作支持性证据而非诊断），可变策略则决定如何探索记录、选择与回看分析、调和互补证据并组织最终回答。

工具层按 ACNS 指南的证据类别组织，包含确定性工具（记录摘要、信号质量、预处理检查、导联组合推导、幅度统计、Welch 频谱、半球对称性）、学习型临床工具（背景异常、粗粒度活动筛查、细粒度事件分类、睡眠-觉醒分期、IED 候选筛查）以及本地知识检索。工具覆盖 1 s 至 30 s 多时间尺度，采用由粗到细策略：10 s 粗筛定位可疑区间，再用 2.5 s 分类器细查；相邻阳性窗合并为候选区间。每个工具返回质量提示，使控制器能感知技术不确定性。

关键创新在于用 GEPA（Genetic-Pareto）仅优化自然语言分析策略：冻结控制器权重、专家工具与安全约束，由独立 LLM 临床评估器按七个临床域（背景、发作期、发作间期、总体分类、状态/睡眠、局灶异常、印象）对照医师报告打分并提供文本反馈，反射器据此提出策略修订，候选策略先在采样优化案例上测试、提升后在验证集上选择，测试集全程隔离。由此在保持本地推理与可追溯工具使用的同时，提升报告与医师的一致性并可迁移至外部基准。

### Q4: 论文做了哪些实验？

论文围绕ERIA框架开展了内部临床评估与外部基准迁移两类实验。内部评估使用200例由认证癫痫专家按ACNS指南撰写的私人临床EEG报告数据集，按记录级划分为50例优化、50例验证和100例受保护测试；控制器为本地部署的Qwen3.8-27B，温度0、上下文65,536 token、最多60次ReAct迭代，采用GPT-OSS-120b作为医师对齐评估器，GEPA反思使用Qwen3.5-122B-A10B-NVFP4，预算750次指标调用，在单台DGX Spark上约4–5天完成。结果显示，验证集临床总分从0.5099升至0.6277（相对提升23.1%），受保护测试集从0.5052升至0.6024（绝对提升0.0972，相对提升19.2%）；同时工具调用从33.72增至46.78次/例，控制器迭代从10.58降至9.34，睡眠/清醒证据覆盖早中晚三段的比例从40%升至98%。外部评估在CerebraGloss-Bench和BrainBench Foundational Analysis上进行，均未参与优化。CerebraGloss-Bench上MCQ准确率保持71.11%，对话QA从3.60升至3.87，描述ROUGE-1从30.70略降至30.17；BrainBench FA加权分从85.86升至86.89，超过原基准最强CodeAct的84.97。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三：其一，GEPA 优化出的策略会引入与现有工具集不匹配的指令（如要求检查睡眠纺锤波、K-复合波，却无对应检测器），未来可在策略生成阶段引入机器可读的工具契约校验，或让控制器在工具缺失时自动降级为显式声明不确定性，而非强行描述。其二，评估依赖与单份参考报告的概念级一致性，缺乏波形级金标准，且仅来自单一机构 200 例回顾数据；可开展多中心、前瞻性评估，并引入多名专家标注与一致性建模，区分“措辞差异”与“临床错误”。其三，控制器权重与工具均冻结，仅优化语言策略，能力上限受工具覆盖限制；可探索轻量工具扩展（纺锤波、K-复合波检测器）与策略-工具联合优化，并研究策略在更异构采集条件与报告风格下的迁移稳定性。此外，工具调用增至 46.78 次/例，推理成本与时延值得系统评估。

### Q6: 总结一下论文的主要内容

论文针对临床脑电图（EEG）长时程记录解读需综合技术质量、背景与行为状态、发作间期与发作期异常及整体临床语境的问题，提出ERIA框架。ERIA是一个可本地部署的单一27B语言模型控制器，通过编排专用参数化工具与信号处理工具分析整段EEG，涵盖背景异常、睡眠-觉醒状态、类癫痫活动、发作间期癫痫样放电等学习型工具，以及频谱、幅度、对称性、导联与信号质量的确定性分析。方法上不微调控制器、不采用多智能体编排，而是固定控制器权重、专家工具与安全约束，仅用GEPA（遗传-帕累托）基于专家撰写的EEG报告反馈优化其自然语言分析策略。结论表明，GEPA提升了与医师对齐的整段报告质量，优化策略可迁移至外部EEG基准，在CerebraGloss-Bench与BrainBench基础分析上保持竞争力，说明专用工具与语言级策略优化可在保持本地推理与可追溯工具使用的同时扩展单一模型的临床与通用EEG能力。
