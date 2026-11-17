---
title: "TRACK: Tool-Augmented Reasoning over Time Series for Fault Diagnosis in Power Management System"
authors:
  - "Erkan Bayram"
  - "Debanjan Ghosh"
  - "Li Zhu"
  - "Sambarta Dasgupta"
date: "2026-11-16"
arxiv_id: "2611.21178"
arxiv_url: "https://arxiv.org/abs/2611.21178"
pdf_url: "https://arxiv.org/pdf/2611.21178v1"
categories:
  - "cs.LG"
  - "cs.AI"
  - "cs.CL"
  - "eess.SY"
tags:
  - "Agentic Time Series"
  - "Tool-Augmented Reasoning"
  - "Fault Diagnosis"
  - "Power Management System"
  - "Time Series Report Generation"
  - "Small Language Model"
  - "On-Device LLM"
  - "Physics-Grounded Diagnosis"
  - "Structured Diagnostic Report"
  - "Rubric-Based Evaluation"
  - "Multi-Load Benchmark"
  - "Out-of-Distribution Generalization"
relevance_score: 9.5
---

# TRACK: Tool-Augmented Reasoning over Time Series for Fault Diagnosis in Power Management System

## 原始摘要

Fault diagnosis in power management systems running multiple loads relies on experts manually inspecting current and voltage waveforms, which fails to scale across deployed units. We present TRACK, which pairs a time series encoder with a Small Language Model to produce structured, physics-grounded diagnostic reports, calling tools for exact, verifiable calculations. It operates on-device, keeping proprietary sensor data local and avoiding expensive API calls. We introduce a rubric-based framework that evaluates these reports by scoring structure, signal fidelity, physics reasoning, diagnosis, and actionability through per-criterion verdicts. On a 15-class multi-load simulated benchmark, TRACK achieves over 95% fault-category accuracy and generalizes to out-of-distribution faults, whereas the best encoder-probing baseline reaches only 58% accuracy.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于多负载电力管理系统中的故障诊断问题。此类系统通过集中或分区电源管理单元持续采集各通道的电压与电流波形，一旦发生LED失效、连接器退化或风扇堵转等故障，波形中会浮现诊断特征，需结合欧姆定律、功率耗散等电路级物理知识并跨通道推理才能定位根因。然而，现有实践依赖领域专家人工判读波形，耗时昂贵且难以在大量部署单元上扩展。另一方面，大语言模型虽能对信号进行推理并泛化到未见故障，但需要云端级资源、延迟高，且机电系统产生的专有数据带宽有限，不适合上传云端，而设备本身具备板载算力，因此故障诊断应在边缘侧完成。本文要解决的核心问题是：能否用一个多模态小型语言模型在设备端跟踪 sensed 负载电压与电流中的诊断特征，生成既有物理依据又可执行的推理链？其挑战包括：模型需在内存与算力受限下处理基线值各异的多元时间序列；推理中需包含一系列正确的数值计算，而小型语言模型数值表示脆弱；需对偏差模式进行推理并解释分布外故障；以及传统基于文本重叠的NLP指标无法评估物理推理质量。为此，作者提出工具增强架构TRACK与基于评分标准的评估框架来应对上述问题。

### Q2: 有哪些相关研究？

**方法类：时间序列推理与多模态对齐。** SensorLM 在大规模数据上对齐传感器与语言，但只生成统计性描述，缺乏物理依据；OpenTSLM 将时间序列分块作为软提示注入 LLM 嵌入空间，与本文最接近。TRACK 的区别在于引入工具调用以保证数值稳定、物理正确与可验证性，并用评分量表评估推理质量而非仅看准确率。此外，Chronos、TimesFM 等时间序列基础模型及 GPT4TS、TEMPO 等 LLM 方法聚焦预测任务，而 TRACK 聚焦物理感知推理；其他工作还涉及异常检测、RL 知识注入、人在回路反馈与符号程序等。

**工具增强推理类。** 受 Toolformer 在生成中插入 token 的启发，TRACK 使用物理专用工具调用；ToolRL 表明分解奖励的 RL 优于 SFT，但本文试点 RL 无额外收益，故采用带观察掩码和命名变量链的 SFT。TimeClaw 采用智能体运行时，TRACK 执行器更简单（10 个无状态函数）但保证领域正确性；KairosAgent 用工具调用生成文本形态描述供预训练预测模型使用，而 TRACK 在生成过程中调用物理工具并据此得出故障结论。

**评测类：LLM-as-Judge。** 标准数值评分 LLM 评判常校准不佳且不可复现；AutoRubric 通过分解为二元标准实现稳定可解释评估，TRACK 将其适配到物理推理，检查物理定律应用、自洽性与因果链完整性。

### Q3: 论文如何解决这个问题？

TRACK 的核心思路是将时间序列编码器与小型语言模型（SLM）耦合，通过工具调用实现可验证的精确计算，从而在边缘设备上生成物理 grounded 的结构化诊断报告。

整体框架包含三个组件：一是 Transformer-CNN 编码器（6 层、8 头、d=128、patch size 4），用于处理每个负载的 12 路传感器通道；二是线性投影器，将 128 维编码映射到 LLM 的 2048 维空间；三是冻结的 Qwen 2.5-3B 模型，配合 LoRA（r=16, α=32）生成推理轨迹。每个通道前插入文本预提示（如“Load channel: DC fan, measured mean: 142.3 mA, baseline: 140.0 mA”），提供通道身份与健康基线先验，软提示 token 与文本 token 交错输入上下文窗口。

关键创新在于工具执行器：它拦截生成文本中的 [CALL:] 模式，调用预定义工具函数完成精确算术（如电流、电压、功率计算），并将结果以命名变量注入后续推理，保证推理链中的数值计算可验证，类似符号推理。这解决了 SLM 数值表示脆弱的问题。

训练采用四阶段课程学习：继承 OpenTSLM 的 MCQ 与 Captioning 阶段后，新增第三阶段——基于 1000 个 SPICE 网表瞬态仿真的电路时间序列（CTS）语料，并引入简单工具调用，使模型接触电气信号行为；第四阶段在 Power Management Bench 上微调，覆盖 5 个负载通道、15 类（含 10 类故障），使用类加权损失处理健康/故障样本不平衡。

此外，论文提出基于评分标准的评估框架，从结构、信号保真、物理推理、诊断和可操作性五个维度以 MET/UNMET 二元判定打分，弥补传统 NLP 指标无法捕捉物理推理质量的缺陷。整个流水线在边缘设备本地运行，保护专有数据并避免云端 API 开销。

### Q4: 论文做了哪些实验？

论文实验围绕故障分类与推理质量两条主线展开。数据集为自建的 Power Management Bench：用 LTSpice 仿真中央电源管理单元驱动五类负载（电阻、热垫、PWM 电阻、风扇、LED 灯带），共 15 类（5 健康+10 故障）、12 通道 116 点时序，故障样本约占 25%；训练/验证/测试各约 22K/2.75K/2.75K，另有 1,050 条分布外（OOD）样本。对比方法包括：在 Trans-CNN 与 Chronos-T5-tiny 编码器嵌入上训练的 MLP 分类器（逐步加入健康基线标量与负载 one-hot），以及三种推理轨迹变体（直接生成、公式标签、工具调用）和不同课程阶段/编码器冻结配置。主要结果：最佳 MLP 探针在合并测试集仅约 58%（ID 最高 72.22%，OOD 最高 29.33%），而 TRACK 推理模型达 95.42% 准确率；工具调用变体综合评分 94.15%，高于公式标签 85.85% 与直接生成 77.98%；Stage 3 使冻结 Chronos 编码器从 92.70% 提升至 95.42%，一致性 97.97%；零样本 Stage 3 模型准确率仅 2.82%。此外，0.5B/1.5B/3B 解码器缩放实验中 1.5B 与 3B 准确率约 93%，0.5B 降至 83.5%、一致性降至 59.3%，生成延迟 42–65 秒；并在 Jetson Orin NX 上完成实机部署验证。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三：其一，评估依赖LLM-as-a-judge，虽采用二元评分标准更有效，但判定仍存在脆弱性和不可复现性，未来可引入人工标注校准、构建可复现的确定性评分器，或训练专用小模型作为评判者。其二，SLM生成的推理链具有非确定性，可能产生物理上不合理的中间步骤，可探索用工具调用轨迹做过程级监督、以物理约束校验推理链，并结合工具特定奖励的强化学习提升可靠性。其三，当前仅在仿真15类多负载基准上验证，真实部署中的噪声、传感器漂移与未见故障模式仍是空白，需构建实机数据集并研究在线自适应与分布外检测。此外，作者提到的降低Jetson端延迟、rubric驱动的提示优化也值得深入；我补充一点：可让编码器与工具调用共享不确定性估计，在置信度低时主动请求专家复核，形成人机协同闭环。

### Q6: 总结一下论文的主要内容

论文针对多负载电源管理系统故障诊断依赖专家人工判读电流电压波形、难以规模化部署的问题，提出TRACK架构：将时间序列编码器与小型语言模型结合，通过调用工具完成精确可验证的计算，把物理推理与数值计算分离，从而在设备端本地生成结构化、物理可解释的诊断报告，既保护专有传感器数据又避免昂贵API调用。作者还提出基于评分细则的评估框架，从结构、信号保真、物理推理、诊断与可执行性五个维度逐项打分。在15类多负载仿真基准上，TRACK故障类别准确率超过95%，并能泛化到分布外故障，而最佳编码器探测基线仅58%。结论指出，3B参数模型即可实现跨五路负载通道的可靠诊断，现成编码器如Chronos适合实际部署，未来将探索工具奖励强化学习与实时延迟优化。
