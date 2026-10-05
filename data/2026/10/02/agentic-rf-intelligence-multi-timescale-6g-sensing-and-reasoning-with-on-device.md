---
title: "Agentic RF Intelligence: Multi-Timescale 6G Sensing and Reasoning with On-Device Foundation Models"
authors:
  - "Jaron Fontaine"
  - "Jelle De Moerloose"
  - "Xander Vanparys"
  - "Anton Lambrecht"
  - "Eli De Poorter"
  - "Adnan Shahid"
date: "2026-10-02"
arxiv_id: "2610.03139"
arxiv_url: "https://arxiv.org/abs/2610.03139"
pdf_url: "https://arxiv.org/pdf/2610.03139v1"
categories:
  - "eess.SP"
tags:
  - "Agentic Time Series"
  - "多时间尺度智能"
  - "无线感知与推理"
  - "设备端基础模型"
  - "LLM工具调用"
  - "双环架构"
  - "6G网络"
  - "物理层基础模型"
  - "边缘计算"
  - "异步推理"
relevance_score: 7.5
---

# Agentic RF Intelligence: Multi-Timescale 6G Sensing and Reasoning with On-Device Foundation Models

## 原始摘要

Future 6G systems share a central challenge with Physical AI: combining sensing, reasoning, and action on network-edge infrastructure in rapidly changing physical environments under strict latency, compute, and energy constraints. Addressing this challenge requires multi-timescale intelligence, combining fast perception that tracks wireless phenomena within milliseconds with slower reasoning that directs sensing and adapts network policies and resources over seconds. In this paper, we present a vision for Agentic RF Intelligence based on a dual-loop architecture that decouples fast, locally autonomous wireless sensing (e.g., detecting spectrum dynamics, interference, and signal sources) from slower agentic reasoning and orchestration. We provide an on-device prototype in which the full stack runs on a single NVIDIA Jetson Thor connected to a B200 Mini USRP. The fast loop processes IQ samples using signal-processing tools and wireless physical-layer foundation models (WPFM), while a local Large Language Model (LLM) asynchronously interprets RF events, invokes tools and steers sensing. Our experiments confirm the separation in timescales, as WPFMs operate at millisecond latency, while LLM interactions take seconds to minutes. The fast loop remains operational during agentic reasoning, providing initial evidence for the feasibility of this decoupled architecture. We conclude by outlining extensions toward memory-driven self-improvement, world models, network control, and multi-agent operation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

未来6G系统与物理AI面临一个共同挑战：如何在严格时延、算力和能耗约束下，于网络边缘基础设施上融合感知、推理与行动。无线物理层事件持续时间极短，如跳频每625微秒发生一次、Wi-Fi突发在毫秒内结束，若感知速度慢于事件本身，就不是延迟观测而是直接错过。然而语言模型响应需数百毫秒至数秒，原始IQ、CSI、CIR等信号速率过高难以在设备端缓存，又过于底层无法被LLM直接理解，直接上传会淹没推理层。现有工作因此只向推理层暴露KPI、估计值或语义状态等高层信息，虽便于智能体处理，却限制了可感知的内容。与此同时，无线物理层基础模型（WPFM）能直接处理底层异构无线数据，轻量变体在边缘硬件上推理可低于毫秒，但WPFM与智能体无线系统大多被分开研究，已有结合也仅让智能体消费WPFM的性能指标，而非将其作为可调用工具。因此本文要解决的核心问题是：如何在单设备系统上，将智能感知层与智能体决策及RF感知工具连接起来，使智能体能够在目标硬件的算力、内存、功耗和时序约束下，按需选择、配置并组合感知能力，实现快慢双环解耦的Agentic RF智能。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，现有无线智能体系统（如基于日志、KPI、语义状态或CSI/AoA/Doppler等估计量的方案）将推理层建立在固定感知流水线的预定义输出上，智能体只能消费高层抽象信息，无法按需调用或重配置底层感知；另一类是无线物理层基础模型（WPFM），可直接处理原始IQ、CIR等低层数据，支持调制识别、干扰检测、人体活动识别等任务，轻量变体在边缘硬件上推理延迟低于毫秒，但缺乏智能体推理能力，仅作为固定流水线使用。应用类方面，已有工作将智能体用于无线网络控制，实现目标分解、工具调用与闭环自适应，但作用于已抽象的网络状态而非物理层信号。评测类方面，已有研究在边缘设备上评测WPFM推理时延与LLM响应时延，但未将二者集成于同一系统。本文与上述工作的核心区别在于：首次提出双环架构，将快速WPFM感知与慢速LLM智能体推理解耦，智能体可主动调用并重配置WPFM作为工具，且全栈在单台Jetson Thor加USRP上端侧运行，弥补了WPFM与智能体系统长期分离的空白。

### Q3: 论文如何解决这个问题？

论文提出的核心解决方案是面向6G边缘设备的双环Agentic RF智能架构，将快速感知与慢速推理在时间尺度上解耦。整体框架分为两个执行环：快速环贴近物理接口，以毫秒级速率持续处理IQ样本、CSI、CIR、Doppler或频谱测量等异构观测，由信号处理工具提取测量量，并由无线物理层基础模型（WPFM）生成紧凑表征，支撑时延敏感的下游任务；这些能力通过MCP等接口以“工具”形式暴露给智能体。快速环还负责监控触发条件，一旦检测到信号、调制方式或异常变化，便异步上报事件。慢速环则运行本地LLM智能体，结合记忆、外部知识及潜在RF世界模型进行长时程推理与编排，通过工具接口调用测量、信号分析、WPFM推理、感知配置以及记忆检索和仿真等专家工具，从而在不进入实时路径的前提下引导快速环观测。

原型Agentic-USRP部署于NVIDIA Jetson Thor与B200 Mini USRP上。快速环作为后台worker控制无线电，支持Triggers、Jobs、Monitors三类操作，事件经线程安全的序列化事件总线异步发布，快速环从不等待LLM。慢速环采用Ollama量化的本地LLM，配合跨会话记忆，通过FastMCP统一接口访问感知、分析、记忆和控制能力。WPFM嵌入保留在记忆中而不直接暴露给LLM，以缓解表征与上下文失配。

创新点包括：快慢环时间尺度解耦、事件总线异步通信、工具化感知接口、LLM不直接访问无线电且仅提交有界工具调用与验证策略，以及面向资源竞争的动作安全设计。

### Q4: 论文做了哪些实验？

实验在单块 NVIDIA Jetson Thor 连接 B200 Mini USRP 的端侧原型上开展，验证双环架构中快慢环的时间尺度分离。快环基准测试对比了紧凑 CNN（0.82M 参数）与 Transformer 无线物理层基础模型（WPFM，2.91M 参数）：CNN 单窗（2048 IQ 样本）推理延迟 0.42 ms，WPFM 为 1.36 ms；FP32 下吞吐分别为 59,349 和 29,441 窗/秒，FP16 加批处理（BS=256）提升至 89,987 和 47,266 窗/秒，完整 USRP-to-WPFM 流水线在隔离运行时达 56 Msps。慢环评估了 Gemma 4 12B/31B、Qwen 3.5 9B、Qwen 3.8 27B、Nemotron 3.5 30B-A3B 五种本地 LLM，在三个逐步增强的智能体场景（频谱观测、信号调查、异步事件调查）中，各做一次运行并对比开启/关闭推理。结果显示：开启推理时 Nemotron 3.5 30B-A3B 平均延迟最低（37.0 s）、吞吐最高（37.8 tokens/s）；关闭推理时 Qwen 3.5 9B 最快（18.9 s）；Gemma 4 12B 开启推理仅完成 1/3 场景。快慢环延迟相差约 4–6 个数量级，表明该架构适合操作员级调查而非实时控制。

### Q5: 有什么可以进一步探索的点？

论文的局限主要在于：双环架构虽验证了时间尺度解耦的可行性，但慢环LLM推理仍需秒到分钟级，难以支撑真正闭环的网络控制；WPFM与LLM之间的语义接口、事件抽象方式尚未系统评估；原型仅单设备、单USRP，缺乏多节点协同与真实6G负载验证；记忆机制与工具调用的可靠性也未量化。未来可探索的方向包括：一是构建分层记忆与检索增强的智能体，使RF事件经验可跨会话积累并驱动自改进；二是引入RF世界模型，让LLM在潜在空间中预测频谱演化，减少对真实探测的依赖；三是将慢环输出形式化为可验证的控制策略，与O-RAN等标准接口对接；四是研究多智能体协作下的频谱共享与干扰协调，并探索WPFM与LLM的联合蒸馏以降低端侧开销。此外，如何定义RF领域的可解释性与安全边界，也是值得深入的问题。

### Q6: 总结一下论文的主要内容

论文针对未来6G系统与Physical AI共同面临的核心挑战——在严格的时延、算力和能耗约束下，于网络边缘基础设施上融合感知、推理与行动——提出了“Agentic RF Intelligence”愿景。其核心是双环架构：快环负责毫秒级的本地自主无线感知，利用信号处理工具与无线物理层基础模型（WPFM）处理IQ样本，检测频谱动态、干扰和信号源；慢环由本地大语言模型（LLM）异步驱动，负责解释RF事件、调用工具并引导感知与网络策略调整。作者在单台NVIDIA Jetson Thor连接B200 Mini USRP上实现了端到端原型。实验证实了时间尺度的分离：WPFM以毫秒级延迟运行，LLM交互则需数秒至数分钟，且快环在推理期间持续运行。该工作为解耦式边缘智能架构提供了初步可行性证据，并展望了记忆驱动自改进、世界模型、网络控制与多智能体协作等方向。
