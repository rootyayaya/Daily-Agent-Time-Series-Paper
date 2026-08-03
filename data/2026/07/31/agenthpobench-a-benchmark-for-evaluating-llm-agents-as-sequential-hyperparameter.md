---
title: "AgentHPOBench: A Benchmark For Evaluating LLM Agents as Sequential Hyperparameter Optimizers"
authors:
  - "Tianyu Huai"
  - "Tingshuo Fan"
  - "Xinchi Chen"
  - "Yining Zheng"
  - "Yuxin Wang"
  - "Shuang Chen"
  - "Jie Zhou"
  - "Xuanjing Huang"
date: "2026-07-31"
arxiv_id: "2607.29626"
arxiv_url: "https://arxiv.org/abs/2607.29626"
pdf_url: "https://arxiv.org/pdf/2607.29626v1"
categories:
  - "cs.AI"
tags:
  - "LLM Agent"
  - "超参数优化"
  - "顺序决策"
  - "实验证据解释"
  - "基准测试"
  - "机器学习任务"
relevance_score: 7.5
---

# AgentHPOBench: A Benchmark For Evaluating LLM Agents as Sequential Hyperparameter Optimizers

## 原始摘要

As LLMs evolve from code completion systems into autonomous scientific agents, evaluating their ability to conduct experiments has become increasingly important. Existing benchmarks typically focus on static code generation, paper replication, or final answer correctness, but do not directly assess whether agents can interpret experimental evidence and use it to guide subsequent hyperparameter decisions. To address this gap, we introduce AgentHPOBench, a sequential benchmark comprising 30 executable machine learning tasks across seven research categories. Each task begins with a validated baseline run, after which an agent performs several sequential interventions. At each step, the agent observes the accumulated configurations, metrics, and logs before proposing the next valid configuration. We evaluate 12 widely used agents and conventional HPO baselines under a unified protocol. The results show that current agents exhibit measurable experimental optimization ability across domains, but still face clear limitations in sustained iterative refinement, complex log diagnosis, and consistent progress toward reported reference performance.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着大语言模型从代码补全工具演化为自主科学智能体，评估其开展实验的能力变得日益重要。现有基准测试大多聚焦于静态代码生成、论文复现或最终答案正确性，无法直接检验智能体是否能够解读实验证据并据此指导后续超参数决策。传统HPO基准虽然提供受控的表格或代理目标用于比较优化算法，但通常抽象掉了研究仓库中的日志、配置和程序上下文，导致一个关键能力未被充分考察：智能体能否从已完成的仓库实验中提取证据，并将其转化为下一个有效的超参数配置。

为填补这一空白，本文提出AgentHPOBench，一个包含30个可执行机器学习任务、覆盖七个研究类别的顺序基准。每个任务从验证过的基线运行开始，智能体需在多次干预中观察累积的配置、指标和日志，并提议下一个有效配置。核心问题在于：自主智能体能否仅凭实证反馈，通过一系列超参数干预真正改进现实机器学习实验？该基准旨在隔离并评估智能体将实验反馈转化为有效配置决策的能力。

### Q2: 有哪些相关研究？

相关研究可分为三类。**基准评测类**：MLAgentBench、ML-Bench、MLE-bench评估智能体在代码库使用、模型训练和ML工程中的表现；CORE-Bench、RE-Bench、PaperBench关注可复现性、研究工程和论文复现；MLGym、MLE-Dojo、MLR-Bench和AIRS-Bench则覆盖更完整的ML研究工作流。这些基准侧重通用研究执行或复现能力，而AgentHPOBench专门隔离出“从仓库指标和日志生成下一组有效超参数配置”这一核心能力进行评测。

**HPO方法与基准类**：OpenML和HPOBench提供标准化任务比较优化算法，NAS-Bench-101提供架构搜索目标函数。传统方法如随机搜索、代理模型、Hyperband/BOHB和PBT通常假设预定义搜索空间、结构化目标接口和相对干净的数值反馈，而AgentHPOBench要求智能体处理真实仓库中的非结构化日志和累积轨迹。

**LLM优化类**：OptFormer从调优轨迹学习优化器，LLAMBO将LLM融入贝叶斯优化，其他工作探索LLM引导的HPO决策和基于智能体的优化框架。与这些提出新优化方法的工作不同，AgentHPOBench不提出新方法，而是系统评估智能体能否将可执行研究仓库的累积反馈可靠转化为有效配置并实现经验性改进，填补了现有基准未直接评估智能体解释实验证据并指导后续超参数决策能力的空白。

### Q3: 论文如何解决这个问题？

论文通过构建一个名为AgentHPOBench的基准测试框架来解决评估LLM智能体在顺序超参数优化中实验能力的问题。其核心方法是将真实可执行的机器学习研究仓库转化为30个标准化任务单元，覆盖NLP、CV、时间序列等七个研究领域。

整体框架采用“任务定义-交互执行-统一评估”的三层架构。每个任务包含一个经过验证的基线配置、一个受限干预空间、评估协议和标量性能指标。智能体在每次干预中观察累积的轨迹历史（包括配置、指标和日志），然后提出下一个有效配置，由统一评估框架验证并执行，返回新的观测结果。

主要模块包括：任务构建模块，从GitHub仓库提取可执行实验并保留原始脚本、依赖和日志；干预空间定义模块，仅保留影响实验结果的超参数；统一评估框架，标准化智能体与异构仓库的交互，同时维护智能体可见轨迹和内部执行记录；审计模块，在评分前验证记录完整性和指标提取正确性。

关键技术在于将超参数优化形式化为顺序决策问题，智能体必须从日志和指标中解读实验证据并转化为有效配置。创新点包括：首次将真实研究仓库作为可执行任务单元进行顺序优化评估；设计了有界归一化分数和基线胜率作为主要评估指标；采用统一的评估协议确保不同后端（开放权重和API智能体）的可比性。实验评估了12种智能体和传统HPO方法，揭示了当前智能体在持续迭代优化和复杂日志诊断方面的局限性。

### Q4: 论文做了哪些实验？

实验在AgentHPOBench基准上进行，涵盖NLP、CV、TS、Graph、RL、LLM和SL七类共30个可执行机器学习任务。采用有限预算协议，即参考基线加五次顺序干预，每次约使用原始训练预算的10%。评估了12种智能体（包括Qwen3-8B/32B、Gemma2-2B、DeepSeek-R1-Qwen-14B、Phi-4-14B、Llama-3.1-8B等开源模型，以及DeepSeek-V4-Pro、GPT-5.5、GLM-4.7/5.1、Kimi-2.6、Claude Sonnet 4.6等API模型）和随机搜索、TPE、BOHB三种传统HPO基线。主要指标为平均有界归一化分数（MBNS）、基线胜率（BWR）和平均锚点达成率（MAA）。

结果显示，Claude Sonnet 4.6表现最佳，有限预算下整体MBNS为0.407、BWR为76.7%、MAA为79.5%；开源模型中Qwen3-32B最优（MBNS 0.148）。传统HPO方法整体落后于强智能体。消融实验表明，去除中间反馈使Qwen3-32B的MBNS从0.148降至0.052；全预算设置提升所有智能体MBNS和MAA，但BWR未一致改善；原生harness相比CLI harness产生更大相对改进。轨迹分析显示多数智能体在前两次干预中获益，但持续优化能力有限。

### Q5: 有什么可以进一步探索的点？

AgentHPOBench揭示了当前LLM智能体在超参数优化中的核心瓶颈，未来可从以下方向深入探索：  
1. **长程记忆与策略固化**：现有智能体在持续迭代中易陷入局部最优或重复无效配置，可引入显式经验回放机制或元学习策略，将历史轨迹编码为可检索的决策先验。  
2. **日志语义理解增强**：复杂日志诊断能力不足，可结合代码结构感知的预训练模型（如针对堆栈轨迹的专用编码器）或让智能体主动生成调试性实验（如消融变量）来定位失败根因。  
3. **跨任务泛化与迁移**：当前性能在不同领域差异显著，可设计任务间共享的“优化策略库”，通过检索相似任务的成功轨迹来初始化新任务的搜索方向。  
4. **资源自适应决策**：不同计算预算下智能体策略应动态调整，可训练一个成本感知的控制器，在探索深度与评估频率间自动权衡。  
5. **与经典HPO融合**：将贝叶斯优化或进化算法的数值建议作为智能体的外部工具，让LLM负责高层策略选择而非低层参数生成，形成混合决策框架。  
此外，基准本身可扩展多轮多目标优化、噪声鲁棒性评估，并加入对智能体“解释自身决策”的元评价维度，以推动更可信的科学发现流程。

### Q6: 总结一下论文的主要内容

AgentHPOBench提出了一个用于评估LLM智能体作为序列化超参数优化器能力的基准。现有基准多聚焦静态代码生成或最终答案正确性，无法直接检验智能体是否理解实验证据并据此调整超参数。该基准包含7个研究领域的30个可执行机器学习任务，每个任务从已验证的基线运行开始，智能体需在观察累积配置、指标和日志后，逐步提出下一个有效配置。研究在统一协议下评估了12种主流智能体与传统HPO基线，结果显示当前智能体展现出跨领域的实验优化能力，但在持续迭代改进、复杂日志诊断以及稳定逼近参考性能方面仍存在明显局限。该工作确立了研究仓库中HPO作为挑战性场景的地位，为开发具备更强实验诊断与序列决策能力的智能体奠定了基础。
