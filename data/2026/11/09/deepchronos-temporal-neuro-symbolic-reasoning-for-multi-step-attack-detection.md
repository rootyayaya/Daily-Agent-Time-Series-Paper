---
title: "DeepChronos: Temporal Neuro-Symbolic Reasoning for Multi-Step Attack Detection"
authors:
  - "Sofia Burkow"
  - "Andrea Agiollo"
  - "Enkeleda Bardhi"
  - "Fernando Kuipers"
  - "Kaitai Liang"
  - "Georgios Smaragdakis"
date: "2026-11-09"
arxiv_id: "2611.12760"
arxiv_url: "https://arxiv.org/abs/2611.12760"
pdf_url: "https://arxiv.org/pdf/2611.12760v1"
categories:
  - "cs.CR"
  - "cs.AI"
  - "cs.NI"
tags:
  - "神经符号推理"
  - "多步攻击检测"
  - "时序因果约束"
  - "入侵检测"
  - "逻辑进展检测"
  - "时序规则推理"
  - "可解释诊断链"
  - "工业安全"
relevance_score: 6.5
---

# DeepChronos: Temporal Neuro-Symbolic Reasoning for Multi-Step Attack Detection

## 原始摘要

Modern cyber threats commonly unfold as multi-step attacks comprising temporally and causally related phases. Current defenses commonly follow a detect first and correlate later paradigm. Intrusion detection systems classify events independently, while downstream systems reconstruct attack progression from the resulting alerts or audit records. In this context, learning-based detectors learn attack-step dependencies implicitly as statistical regularities in the data and cannot guarantee that their predictions follow the real attack progression. Conversely, correlation systems represent attack relationships explicitly, but apply this knowledge only after the underlying attack observations have been detected. We present DEEPCHRONOS, a neuro-symbolic network intrusion detection system that shifts the paradigm from detect first and correlate later to detection through logical progression. DEEPCHRONOS combines learned flow-level evidence with explicit attack-phase rules, temporal prerequisites, and previously inferred phases, allowing the evolving attack history to inform and constrain each detection decision. Evaluations on DARPA 2000 and AIT-LDS V2 show that DEEPCHRONOS improves macro F1 over purely neural baselines by up to 11.3%, eliminates causal violations under strict temporal constraints, and maintains millisecond-scale inference latency. These results demonstrate that integrating explicit attack progression knowledge into detection produces more accurate and temporally coherent multi-step attack predictions.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决多步攻击（MSA）检测中“先检测、后关联”范式带来的根本性割裂问题。研究背景是：现代网络威胁通常由侦察、初始访问、提权、横向移动、数据外泄等多个在时间和因果上相互关联的阶段组成，单独看每个事件往往并不足够可疑，只有结合攻击进展才能识别。现有方法存在两类不足：基于规则或机器学习的入侵检测系统对事件独立分类，攻击步骤依赖只能作为统计规律被隐式学习，可能预测出前提尚未出现的阶段，产生不符合真实攻击进程的无效预测；而告警关联系统虽显式表示攻击关系，却只能在检测决策完成之后才进行推理，攻击进展知识无法反过来约束每个事件的分类，误报还可能生成虚假攻击路径。因此，本文的核心问题是：如何将显式的攻击阶段规则和时间前提直接嵌入检测过程本身，使已推断出的攻击历史能够指导和约束每一次新的检测决策，从而在攻击目标达成前实现更准确、时间上因果一致的多步攻击检测。

### Q2: 有哪些相关研究？

本文的相关工作主要分为三类。方法类方面，传统网络入侵检测系统分为基于签名的NIDS（匹配专家定义的攻击描述）和数据驱动的NIDS（学习恶意或异常流量模式），后者通常估计 p_θ(Y=y|x)，但独立分类事件、隐式学习攻击步骤依赖，无法保证预测符合真实攻击进程；关联系统则显式表示攻击关系，但仅在攻击观测被检测后应用知识，属于“先检测后关联”范式。神经符号AI方向，DeepProbLog扩展了概率逻辑语言ProbLog，引入神经谓词，将神经网络输出的概率分布嵌入逻辑规则，支持端到端训练与概率推理，是本文的符号推理基础。应用类方面，多步攻击（MSA）检测研究关注侦察、初始访问、持久化、横向移动、收集与外泄等阶段的识别，并需处理阶段跳过、重复与交错，以及因果违规和回归违规问题。评测类方面，常用DARPA 2000和AIT-LDS V2等数据集评估多步攻击检测性能。与上述工作相比，DeepChronos的区别在于将“先检测后关联”转变为“通过逻辑进程检测”，把学习到的流级证据与显式攻击阶段规则、时间前置条件及已推断阶段结合，使攻击历史约束每次检测决策，从而提升宏F1、消除严格时间约束下的因果违规并保持毫秒级推理延迟。

### Q3: 论文如何解决这个问题？

DeepChronos 的核心思路是将多步攻击检测从“先检测后关联”转变为“通过逻辑推演直接检测”。整体框架由四部分组成：数据准备、神经符号推理、攻击记忆与告警决策。

在数据准备阶段，原始流量被转换为网络流，并提取两类特征：一是流级统计特征，仅使用包头字段以适配加密流量；二是源/目的中心的滑动窗口统计特征，用于捕捉扫描等跨流的全局交互模式。随后构造 DeepProbLog 推理查询，查询输入包括攻击上下文（历史已观测攻击阶段的二值标志）、流上下文（协议、方向、端口等符号特征）以及流特征（仅统计特征，不含 IP、端口、时间戳，以避免过拟合到特定环境）。

关键技术在于神经符号推理规则：某攻击阶段成立需同时满足三个条件——时间前提允许（plausible_attack_phase，依据历史阶段标志约束阶段顺序，如外泄必须发生在入侵之后）、流上下文符合攻击阶段规则（attack_phase_rule，如 sadmind 蠕虫须针对 111 端口）、神经网络给出可疑证据（neural_evidence）。良性流则定义为所有攻击阶段证据均不成立，采用 negation-as-failure 语义计算概率。这种设计将时间约束、符号规则与神经预测统一到同一推理过程中。

创新点包括：将显式攻击进展知识直接嵌入流级推理，使历史阶段约束当前预测；神经组件专注学习可泛化的行为模式，符号组件负责 IP、端口等结构化知识，提升可解释性；引入轻量级攻击记忆，按攻击者-目标 IP 对维护独立历史状态，支持多攻击活动并行跟踪与状态化检测；最终告警基于同一历史中多个相关阶段的累积而非孤立预测，从而过滤侦察阶段的大量误报。

### Q4: 论文做了哪些实验？

论文在DARPA 2000和AIT-LDS V2两个公开多步攻击数据集上评估DeepChronos，采用分层70/30划分训练/测试集，将PCAP转为Zeek流并对齐攻击标注。评价指标包括准确率、宏/加权F1、误报率FAR、检测率DR及逐阶段F1，并自定义因果违反率CVR和回归违反率RVR衡量时序一致性。对比方法包括多类LSTM、集成LSTM两个神经基线，去除神经组件的纯符号逻辑基线，以及最先进系统Kitsune；DeepChronos评估端到端训练与神经预训练两个变体，最多训练50轮。主要结果：在AIT-LDS V2上，引入时序约束与攻击阶段规则（T+R）的预训练模型将宏F1从0.878提升至0.944，RVR从0.152降至0.002；在DARPA上，端到端T+R模型取得最佳宏F1 0.940，并实现CVR=RVR=0的完美时序一致性，而神经基线出现大量进展违反。Kitsune在DARPA上宏F1最高（0.984），但FAR达0.03719，远高于端到端T+R模型的0.00015，且不提供攻击进展一致性指标。整体上DeepChronos较纯神经基线宏F1最高提升11.3%，在严格时序约束下消除因果违反，并保持毫秒级推理延迟。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：其一，威胁模型假设攻击者非自适应，未考虑延迟、重排或省略攻击阶段等规避策略，而实际对抗环境中攻击者可模仿正常流量或打乱阶段顺序，符号规则的刚性可能被利用；其二，仅依赖网络流头部与连接级元数据，无法覆盖加密载荷内的语义信息及主机侧无网络痕迹的活动，检测范围受限；其三，攻击阶段划分与多步判定阈值依赖先验知识，跨场景迁移时规则需人工重构。未来可探索：引入自适应对抗训练与阶段顺序扰动增强，提升神经-符号耦合的鲁棒性；将符号规则参数化或学习化，使阶段先验可从数据中弱监督获取；结合溯源图或主机日志做跨模态证据融合，弥补网络可见性缺口；并研究在线增量更新机制，在保持毫秒级延迟下动态修正规则与历史证据权重。

### Q6: 总结一下论文的主要内容

论文针对多步攻击检测中现有防御遵循“先检测后关联”范式的问题，即入侵检测系统独立分类事件、关联系统仅在告警产生后才重建攻击进程，导致攻击步骤依赖只能被隐式学习、预测可能违背真实攻击逻辑，提出将显式攻击进程知识嵌入检测环节的新范式“通过逻辑进程进行检测”。方法上，作者设计DeepChronos神经符号入侵检测系统，结合神经网络从噪声网络流数据中提取恶意行为证据，与显式攻击阶段规则、时间前置条件及已推断阶段进行概率化联合推理，并用轻量记忆为活跃攻击上下文维护独立历史，使早期弱证据可参与检测。在DARPA 2000和AIT-LDS V2上的实验表明，DeepChronos相比纯神经基线宏F1最高提升11.3%，在严格时间约束下消除因果违规，并保持毫秒级推理延迟，证明显式攻击进程知识能产生更准确、时间一致的多步攻击预测。
