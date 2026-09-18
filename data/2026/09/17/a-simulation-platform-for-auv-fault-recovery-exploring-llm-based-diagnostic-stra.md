---
title: "A Simulation Platform for AUV Fault Recovery: Exploring LLM-Based Diagnostic Strategies"
authors:
  - "Khalid Halba"
  - "Kylie Cooper"
  - "James G. Bellingham"
date: "2026-09-17"
arxiv_id: "2609.20620"
arxiv_url: "https://arxiv.org/abs/2609.20620"
pdf_url: "https://arxiv.org/pdf/2609.20620v1"
categories:
  - "cs.RO"
  - "cs.AI"
tags:
  - "LLM-based diagnosis"
  - "fault recovery"
  - "AUV"
  - "simulation platform"
  - "ensemble evaluation"
  - "anomaly detection"
  - "structured prompting"
  - "LLM-judge"
  - "autonomous systems"
  - "predictive maintenance"
relevance_score: 8.5
---

# A Simulation Platform for AUV Fault Recovery: Exploring LLM-Based Diagnostic Strategies

## 原始摘要

Autonomous underwater vehicles (AUVs) operating beyond reliable communications must recover from failures without human intervention. We investigate an architecture in which conventional deterministic layered control autonomy manages normal operations, while an invokable large language model (LLM) serves as a diagnostic and recovery planner when onboard anomaly detection identifies performance outside expected limits. Because language models are stochastic, rigorous evaluation requires ensemble testing rather than individual demonstrations. We present a closed-loop simulation architecture that couples real-time C vehicle software with a higher-level orchestration layer for physics-based fault injection, structured prompting, language-model interaction, mission file generation, validation, execution, and LLM-judge scoring. The framework, which we call SPAR (Simulation Platform for AUV Recovery), supports evaluation across fault realizations, prompt structures, reasoning models, and mission conditions. We vary these for a mass-shift fault over 480 SPAR trials, evaluating a frontier model and three off-the-shelf locally deployable LLMs. Model choice dominates diagnosis: the frontier model places the CG-shift mechanism in its top three hypotheses in 85-90% of trials, versus 60-78% for the best local model. Reasoning analysis indicates that local-model success is associated with following the complete diagnostic procedure, whereas weaker models often commit prematurely to elevator failure even though the actuator tracks its command. Diagnosis and operational decision performance do not appear to be coupled in this dataset. The contributions are an architecture extending unanticipated-fault recovery from detection to mitigation and an ensemble methodology for evaluating LLM-assisted mission management on low-power AUVs.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

长航时AUV任务通常依赖确定性分层控制自主系统来管理制导、控制、行为和任务序列，该架构适用于正常操作以及有预定义响应的预期故障。然而，当发生未预期故障时，飞行器虽能观测到性能超出预期范围，但现有分层控制自主系统中并未编码故障原因及相应的操作决策，这一“任务管理”环节仍属空白。现有经典AUV故障诊断方法主要针对预定义的执行器、传感器和部件故障，依赖模型残差、阈值、观测器或训练分类器，对未知或衍生故障的覆盖有限；已有任务级监测方法虽能检测到偏离正常行为的异常，但无法确定底层物理原因或生成任务级操作决策。此外，LLM虽已被用于将自然语言目标转化为地面和空中机器人的可执行计划，但其在AUV故障恢复中的应用仍很有限，且现有规划研究通常假设无故障执行。因此，本文的核心问题是：在通信受限、功率和计算资源紧张的AUV平台上，如何利用可调用的LLM作为诊断与恢复规划器，在异常检测触发后，基于结构化遥测数据推断未预期故障的物理原因并生成可执行的任务级恢复方案，同时通过闭环仿真平台SPAR和集成测试方法，系统评估不同模型、提示结构和故障条件下的诊断准确性与操作决策性能。

### Q2: 有哪些相关研究？

相关研究可分为三类。方法类方面，经典AUV故障诊断主要针对预定义的执行器、传感器和部件故障，采用基于模型的残差、阈值、观测器或训练分类器，但对未知或衍生故障覆盖有限；Raanan等人用在线主题模型和实时垂直面异常检测器识别偏离标称行为的异常，但只能确认“行为异常”，无法确定物理原因或生成任务级决策，本文正是接续其后的诊断与缓解步骤。应用类方面，LLM已被用于将自然语言目标转化为地面与空中机器人的可执行计划，但用于AUV故障恢复的研究仍有限，最接近的同期工作面向操作员异常诊断，早期规划研究则多假设无故障执行；本文把LLM作为基于文本的诊断与恢复规划器，解释结构化异常遥测、提出新任务文件，并经确定性验证器后闭环执行。评测类方面，水下机器人仿真生态包括HoloOcean、UUV Simulator、Stonefish、DAVE和AUV Workbench等，SPAR沿用类似结构，但专门面向故障建模、可重复故障注入和基于成熟车辆代码的闭环运行决策评估，并以480次试验的集成方法统计评估LLM辅助任务管理。

### Q3: 论文如何解决这个问题？

SPAR采用闭环仿真架构，将实时C语言载具软件与高层编排层耦合，形成从故障注入到评分决策的完整回路。整体框架由四个软件组件构成：Python/Qt编排层、C载具仿真器、被测语言模型规划器和语言模型评判器，组件间通过少量文件与数据结构交换信息。

核心流程为：编排层写入故障描述符，仿真器读取后以50Hz积分六自由度水动力学，在运行中注入指定故障，并将感知变量记录为传感器表；错误捕获模块通过死区、持续性和验证三级滤波监视四个通道，越限时触发异常标志。编排层据此组装提示词，规划器返回诊断、可执行任务文件及推理轨迹；任务经语法与安全校验后执行，评判器对诊断打分，继续/中止决策则由确定性代码依据故障物理单独核验。

关键技术包括：一是分层自主架构，常规控制由确定性分层控制器承担，仅在异常检测触发时调用LLM作为诊断与恢复规划器，适配低功耗AUV；二是结构化提示设计，静态部分包含八个物理领域的工程参考、行为目录和任务文件格式，不点名任何子系统，动态部分仅给出检测到的症状而非注入故障本身，迫使模型从效应反推原因；三是可替换规划器接口，支持前沿模型与本地部署模型；四是独立评判器由第四家厂商模型担任，避免自评。

创新点在于将LLM辅助恢复从检测扩展到缓解的架构，以及面向随机语言模型的集成评测方法，通过480次试验跨故障实现、提示结构、推理模型和任务条件进行严格评估。

### Q4: 论文做了哪些实验？

论文基于SPAR闭环仿真平台开展实验，将实时C语言车载软件与物理故障注入、结构化提示、LLM交互、任务文件生成与验证、LLM评判评分相耦合。实验注入前向重心（CG）偏移故障，设置两种幅值（0.005 m和0.05 m）和两个注入阶段（下潜t=300 s、巡航t=800 s），并设计三个提示层级（Tier 1提供完整方程与子系统上下文，Tier 2去除方程，Tier 3仅保留基本工程参考）。评估四个LLM：前沿模型gpt-5.5及三个本地模型gemma4:12b、gpt-oss:20b、nemotron-nano-12b-v2。每个模型×层级×幅值×阶段重复10次，共480次试验，每个模型-层级对n=40。任务为从5 m下潜至200 m并巡航约1 km。诊断正确性以真实CG偏移进入前三假设为准，操作决策按可管理故障应继续、严重故障应中止评分。主要结果：gpt-5.5前三诊断率85%/90%/85%，本地最佳nemotron为78%/68%/60%，gemma4为42%/30%/38%，gpt-oss仅10%/28%/25%；排名第一率gpt-5.5为75%/70%/43%。决策方面，0.005 m时gpt-5.5巡航正确继续93%、下潜90%，gpt-oss为53%/27%，nemotron仅3%/7%，gemma4全部中止；0.05 m时gemma4全部正确中止，nemotron达97%/83%，gpt-oss为93%/80%，gpt-5.5巡航100%但下潜仅33%。结果表明模型选择主导诊断，且诊断与操作决策性能不耦合。

### Q5: 有什么可以进一步探索的点？

当前工作的局限主要体现在三方面：一是仅验证了质量偏移这一种故障，诊断与决策在其他故障类型（如推进器退化、传感器漂移）上的泛化性未知；二是提示工程变量（长度、顺序、程序约束）与模型能力相互纠缠，无法分离各自贡献；三是诊断正确性与操作决策明显解耦，说明单一指标不足以刻画系统可靠性。未来可从以下方向深入：其一，构建多故障、多任务阶段的组合测试集，考察模型在分布外故障上的鲁棒性；其二，引入受控消融实验与分阶段短提示、检索增强，明确工程上下文注入的最优粒度；其三，让分层控制自主性暴露命令-响应一致性、剩余控制权限等派生指标，并对关键决策施加确定性校验，形成“LLM规划+确定性守门”的集成架构；其四，探索面向诊断流程的轻量微调与工具调用式智能体，使本地小模型在低功耗约束下也能维持结构化推理。

### Q6: 总结一下论文的主要内容

论文针对自主水下航行器在通信受限条件下无法依赖人工干预恢复故障的问题，提出SPAR闭环仿真平台。其架构将确定性分层控制用于常规运行，并在异常检测触发时调用大语言模型作为诊断与恢复规划器，支持物理故障注入、结构化提示、任务文件生成、验证执行及LLM评判评分。作者以质量偏移故障开展480次试验，评估一个前沿模型和三个本地可部署模型。结果表明，模型选择对诊断影响显著：前沿模型在85%至90%试验中将重心偏移机制列入前三假设，最佳本地模型为60%至78%；本地模型成功多与遵循完整诊断流程相关，较弱模型常过早归因于升降舵故障。诊断准确性与操作决策表现并不耦合。该工作贡献了从检测到缓解的故障恢复架构及面向低功耗AUV的LLM集成评估方法。
