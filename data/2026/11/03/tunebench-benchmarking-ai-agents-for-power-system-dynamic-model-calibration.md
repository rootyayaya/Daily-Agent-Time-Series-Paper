---
title: "TuneBench: Benchmarking AI Agents for Power System Dynamic Model Calibration"
authors:
  - "Andrea Pomarico"
  - "Salvatore Tessitore"
  - "Giorgio Giannuzzi"
  - "Alberto Berizzi"
date: "2026-11-03"
arxiv_id: "2611.04640"
arxiv_url: "https://arxiv.org/abs/2611.04640"
pdf_url: "https://arxiv.org/pdf/2611.04640v1"
github_url: "https://github.com/Power-Agent/PowerAgentBench"
categories:
  - "eess.SY"
tags:
  - "LLM Agent"
  - "工具调用"
  - "迭代反馈优化"
  - "工业系统校准"
  - "电力系统动态模型"
  - "参数调优"
  - "基准测试"
  - "可解释子问题分解"
  - "物理指标提取"
  - "Agentic AI"
relevance_score: 7.5
---

# TuneBench: Benchmarking AI Agents for Power System Dynamic Model Calibration

## 原始摘要

Large Language Model (LLM)-based agents can automate complex engineering workflows by interacting with tools, interpreting feedback, and making iterative decisions. This paper introduces TuneBench, a benchmark for evaluating Agentic AI in power system dynamic model calibration, where controller parameters are adjusted to reproduce target dynamic responses. The benchmark reflects a common Transmission System Operator (TSO) practice, in which equivalent models used for Dynamic Security Assessment (DSA) are calibrated against measurements from grid-code compliance tests when proprietary models are unavailable. Two cases of increasing complexity are considered: the governor and Automatic Voltage Regulator (AVR) of a synchronous generator and the control system of a Battery Energy Storage System (BESS), both tuned against active-power and voltage step tests within a budget of 15 simulations. LLM-based agents are compared with random search and Genetic Algorithm (GA) baselines over 10 independent runs. Only the most advanced models, Opus 5.5 and GPT-6, accurately reproduce all target trajectories, with median R2 above 0.995 in every test and tracking errors up to two orders of magnitude lower than the baselines. The agent logs show that these agents autonomously extract dynamic performance indices, such as settling time and damping, and relate them to specific control parameters, decomposing the tuning problem into physically interpretable sub-problems. The benchmark is publicly available at https://github.com/Power-Agent/PowerAgentBench/tree/main/benchmarks/dynamic/level3.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决电力系统动态模型校准过度依赖人工经验、缺乏对AI Agent能力系统评估的问题。研究背景是：输电系统运营商在动态安全评估中广泛使用相量域仿真，其可靠性高度依赖动态模型的准确性；但由于专有模型和控制参数往往不对外披露，运营商需基于并网合规测试（有功功率、电压阶跃等）的实测数据构建等效模型并反复调参，使仿真轨迹逼近实测响应。现有方法虽包括遗传算法、卡尔曼滤波等优化手段，但整个过程仍严重依赖经验丰富的工程师来识别关键参数、解读参数影响并迭代修正模型，效率低且难以规模化。与此同时，基于大语言模型的Agent已具备调用工具、执行代码、依据反馈迭代决策的能力，在电力系统多个环节展现潜力，但已有工作多聚焦单一任务，缺少面向完整动态模型校准工作流的标准化评测。为此，本文提出TuneBench基准，构建反映真实TSO实践的调参任务（同步发电机调速器与AVR、电池储能系统控制系统），在15次仿真预算内要求Agent自主选择并调整控制参数以复现目标动态响应，并将LLM Agent与随机搜索、遗传算法基线在准确性和计算开销上进行比较，从而系统回答Agent能否胜任此类需工程知识与动态响应解读的多步校准任务。

### Q2: 有哪些相关研究？

相关研究可分为三类。方法类：传统动态模型校准依赖人工试错或遗传算法、卡尔曼滤波等优化方法，通过最小化仿真与实测轨迹偏差调整参数，但需经验工程师识别关键参数并解释其影响。应用类：已有研究将LLM用于电力市场竞价、机组组合与调度、最优潮流及电网控制，但多针对单一任务而非完整工程工作流；近期出现面向配电网分析和复杂电力系统问题的智能体框架。评测类：PowerAgent社区提出PowerAgentBench-SS与PowerAgentBench-Dyn，分别面向稳态与动态研究；RestoreBench关注潮流不收敛恢复。本文与上述工作的关系与区别在于：TuneBench聚焦动态模型校准这一TSO实际工作流，要求智能体自主提取调节时间、阻尼等动态性能指标，将其映射到具体控制参数，并在15次仿真预算内迭代调整，而非单步任务；同时首次将LLM智能体与随机搜索、遗传算法基线在同步机调速器/AVR及BESS控制两个案例上系统对比，强调可解释的子问题分解能力。

### Q3: 论文如何解决这个问题？

论文将动态模型校准建模为一个交互式环境 T=(O,A,E,C,G,M)，其中观测空间 O 为仿真波形与诊断信息，动作空间 A 为配置仿真、运行仿真、分析响应与修改模型参数，E 为基于开源仿真器 ANDES 的时域仿真环境，C 为机器可读的工程约束（仿真预算、受保护文件、允许的事件修改与报告要求），G 为隐藏的目标轨迹与评估机制，M 为可选的语义记忆组件。智能体在每一步接收观测 o_t、选择动作 a_t，并通过仿真器或工具反馈获得新观测，循环直至达到满意拟合或耗尽预算（每个实例最多 15 次仿真）。

关键设计包括：参数搜索空间不做预先限定，智能体需依据参数的物理含义及其对有功功率、电压等电气量的影响，自主识别并修改任意可访问的动态模型参数，从而使“参数选择”本身成为被评估的推理环节；评估采用 RMSE 与决定系数 R² 两个互补指标，分别刻画拟合误差与对目标动态变化规律的复现程度；基准包含两个复杂度递增的案例——同步发电机调速器与自动电压调节器（AVR），以及电池储能系统（BESS）控制系统，均针对有功功率与电压阶跃测试进行整定，并与随机搜索、遗传算法基线在 10 次独立运行下对比。

框架遵循四项原则：工具 grounded 的评估、多轮迭代决策、工程约束护栏与结果导向评估。创新点在于：将 TSO 实际工作中基于并网合规测试测量数据校准 DSA 等值模型的流程转化为可复现的智能体基准；允许智能体自主提取调节时间、阻尼等动态性能指标并将其关联到具体控制参数，从而把整定问题分解为物理可解释的子问题；在保留智能体自主性的同时通过机器可读约束确保评估可控可复现。

### Q4: 论文做了哪些实验？

论文在ANDES仿真平台上构建了两个复杂度递增的校准案例：同步发电机（IEEEG1调速器与ESST1A励磁系统）和电池储能系统（REGCA1、REECA1、REPCA1控制器），每个案例均包含有功功率阶跃测试（Test P）和电压阶跃测试（Test V），目标参数被刻意偏离标准值以避免LLM凭记忆作答。LLM智能体（Opus 5.5、GPT-6、Sonnet 5、GPT-5.6、Haiku 4.5）在15次仿真预算内顺序完成两项测试，并与随机搜索和遗传算法（各150次仿真预算）在10次独立运行下对比。结果显示：发电机案例中，Test P较简单，Sonnet 5、GPT-5.6和GA的R²均超过0.998，Opus 5.5与GPT-6误差最低（RMSE为1.8×10⁻³和1.5×10⁻³ pu，R²=0.9999）；Test V更具区分度，仅Opus 5.5和GPT-6近乎精确复现目标（RMSE低于10⁻⁵ pu，R²=1），Haiku 4.5失败（R²=0.03）。BESS案例难度显著更高：Test P中仅Opus 5.5和GPT-6稳定复现目标特征，RMSE约3.6–4.1×10⁻⁴ pu，比随机搜索（4.7×10⁻² pu）和GA（3.4×10⁻² pu）低约两个数量级；Test V中仅二者成功，Opus 5.5最优（RMSE=6.6×10⁻⁵ pu，R²=0.99997），其余方法R²均低于0.8。运行时间方面，Opus 5.5中位耗时分别为22.1和67.5分钟，GPT-6为17.6和21.7分钟，在精度与效率间取得最佳平衡。智能体日志表明其能自主提取调节时间、阻尼等动态性能指标并分解调参子问题。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索空间主要体现在三方面。其一，基准仅覆盖同步机调速器/AVR与BESS控制两类场景、15次仿真预算，且目标参数由标称值人为偏移，尚未验证真实量测噪声、通信延迟与模型结构失配下的鲁棒性，未来可引入含噪声与部分可观测的实测数据，并扩展到多机系统、风电机组及跨设备耦合调参。其二，评估以R²和跟踪误差为主，缺乏对智能体推理链正确性的量化，可设计“参数—指标—物理机理”一致性评分与可解释性审计指标。其三，当前仅最强模型能完成任务，说明对LLM推理能力依赖过强，可探索工具增强（如自动灵敏度分析、频域辨识）、检索物理知识库、多智能体分工与人在环校验，并研究仿真预算自适应分配策略，以降低对模型规模的依赖并提升工程可信度。

### Q6: 总结一下论文的主要内容

论文针对输电网运营商在专有模型缺失时需依据并网合规测试的实测响应校准动态等值模型这一实际需求，提出了 TuneBench 基准，用于评估基于大语言模型的智能体在电力系统动态模型校准中的能力。问题定义为：在 15 次仿真预算内调整控制器参数，使仿真轨迹复现目标动态响应。基准包含两个复杂度递增的案例：同步发电机的调速器与自动电压调节器，以及电池储能系统的控制系统，均需在有功功率与电压阶跃测试下校准。方法上将 LLM 智能体与随机搜索、遗传算法基线在 10 次独立运行中对比。主要结论是：仅 Opus 5.5 和 GPT-6 能在预算内准确复现全部目标轨迹，各测试中 R² 中位数均高于 0.995，跟踪误差最多比基线低两个数量级；智能体日志显示其能自主提取调节时间、阻尼等动态性能指标并关联具体控制参数，将调参问题分解为物理可解释的子问题。该基准已公开，为智能体在电力系统动态校准中的应用提供了可复现的评测平台。
