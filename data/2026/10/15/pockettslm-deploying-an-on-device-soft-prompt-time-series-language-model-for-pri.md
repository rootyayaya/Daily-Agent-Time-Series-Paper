---
title: "PocketTSLM: Deploying an On-Device Soft-Prompt Time-Series Language Model for Privacy-Preserving Smartphone Reasoning"
authors:
  - "Max Rosenblattl"
  - "Nikhil Krishnaswamy"
  - "Leon Nissen"
  - "Manuel Milling"
  - "Nicolas Zumarraga"
  - "Ning Wang"
  - "Thomas Kaar"
  - "Robert Jakob"
  - "Björn W. Schuller"
  - "Elgar Fleisch"
  - "Patrick Langer"
  - "Paul Schmiedmayer"
date: "2026-10-15"
arxiv_id: "2610.21308"
arxiv_url: "https://arxiv.org/abs/2610.21308"
pdf_url: "https://arxiv.org/pdf/2610.21308v1"
github_url: "https://github.com/SchmiedmayerLab/PocketTSLM"
categories:
  - "cs.LG"
  - "cs.CL"
tags:
  - "Agentic Time Series"
  - "On-Device LLM"
  - "Soft-Prompt"
  - "Time-Series Language Model"
  - "Privacy-Preserving"
  - "Mobile Deployment"
  - "ECG-QA"
  - "Sleep Staging"
relevance_score: 8.5
---

# PocketTSLM: Deploying an On-Device Soft-Prompt Time-Series Language Model for Privacy-Preserving Smartphone Reasoning

## 原始摘要

Consumer phones and wearables increasingly collect physiological time-series data, yet most mobile systems treat these streams as summaries or text rather than as temporal evidence. This representation is poorly matched to personal health systems that need to retrieve, route, or summarize sensor evidence while preserving temporal structure. Cloud-hosted time-series language models avoid smartphone limits, but they repeatedly move sensitive physiology off the device and add latency and per-query compute cost. Mobile model alternatives that aggregate time-series data into statistical features or serialize raw samples as text either compress temporal structure or exhaust the context and memory budgets of small on-device models. We present PocketTSLM, a mobile-native deployment of OpenTSLM SoftPrompt, the soft-prompt variant of the OpenTSLM time-series language model. PocketTSLM runs fully on a consumer smartphone by injecting encoded time-series windows as embeddings instead of tokenizing time series as text. A numerical parity protocol verifies identical greedy-decoded token sequences between the Swift port and a Python reference using Apple's MLX machine-learning framework. Answers also match the PyTorch reference, although rationale wording can differ. An on-device context-economics benchmark compares the soft-prompt path with a text-serialized baseline on the same backbone. In our benchmark format, soft-prompting uses approximately 12 times fewer time-series tokens and reduces prompt-prefill cost. PocketTSLM processes 30-second Sleep-EDF electroencephalography clips for sleep staging and a 1,000-sample (10 s) 12-lead electrocardiogram clip from ECG-QA. In comparison, text-serialized baselines exceed the phone's context or memory budget at longer time-series windows. All inference runs entirely on the device, with no health data transmitted during inference.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文旨在解决在消费级智能手机上部署时间序列语言模型（TSLM）时面临的核心矛盾：一方面，手机和可穿戴设备持续采集生理时间序列数据，但现有移动系统通常将其压缩为统计摘要或文本，丢失了时间结构，难以支持需要检索、路由或总结传感器证据的个人健康应用；另一方面，云端托管的TSLM虽然能避免手机端限制，却需要将敏感生理数据反复传出设备，带来隐私风险、延迟和按查询计算成本。而现有的移动端替代方案要么将时间序列聚合为统计特征，要么将原始样本序列化为文本，前者压缩了时间结构，后者则耗尽小型端侧模型的上下文和内存预算。因此，论文提出PocketTSLM，目标是在完全不离设备的前提下，实现时间序列语言模型在智能手机上的原生部署，同时保持时间序列的时序结构，并支持睡眠分期和心电图问答等推理任务。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是云端时间序列语言模型，如OpenTSLM及其软提示变体，它们通过将时间序列编码为嵌入而非文本令牌来保留时序结构，但依赖云端计算。第二类是移动端健康推理系统，如LLaSA和SensorLLM，它们尝试在设备上处理传感器数据，但通常将时间序列聚合为统计特征或序列化为文本，导致时序信息损失或上下文超限。第三类是隐私保护机器学习，强调在设备上完成推理以避免数据传输，但少有工作专门针对时间序列语言模型进行端侧部署。本文与OpenTSLM软提示变体直接相关，将其从云端移植到手机端，并引入数值一致性协议验证移植正确性。与LLaSA和SensorLLM相比，本文的核心区别在于使用软提示注入时间序列嵌入，而非文本序列化，从而在相同骨干模型下显著减少令牌数量，并避免上下文和内存溢出。

### Q3: 论文如何解决这个问题？

论文提出PocketTSLM，将OpenTSLM软提示变体完整部署到消费级智能手机上。核心方法包括：1）软提示注入：将编码后的时间序列窗口作为嵌入向量直接注入语言模型，而非将时间序列令牌化为文本，从而保留时序结构并大幅减少令牌数量。2）Swift移植与数值一致性协议：使用Apple的MLX框架和MLX-Swift接口，将Python参考实现移植到Swift，并设计数值一致性协议，验证Swift移植与Python参考在贪心解码下产生完全相同的令牌序列；答案与PyTorch参考也匹配，尽管理由措辞可能不同。3）端侧上下文经济学基准：在同一骨干模型上比较软提示路径与文本序列化基线，在基准格式下，软提示使用约12倍更少的时间序列令牌，并降低提示预填充成本。4）实际任务验证：处理30秒Sleep-EDF脑电片段进行睡眠分期，以及来自ECG-QA的1000样本（10秒）12导联心电图片段。所有推理完全在设备上运行，推理过程中不传输任何健康数据。

### Q4: 论文做了哪些实验？

实验主要包括三部分：1）数值一致性验证：通过数值一致性协议，比较Swift移植与Python参考在贪心解码下的令牌序列，确认两者完全一致；同时答案与PyTorch参考匹配，但理由措辞可能不同。2）端侧上下文经济学基准：在同一骨干模型上，比较软提示路径与文本序列化基线，在基准格式下，软提示使用约12倍更少的时间序列令牌，并降低提示预填充成本。3）实际任务评估：使用30秒Sleep-EDF脑电片段进行睡眠分期，以及来自ECG-QA的1000样本（10秒）12导联心电图片段进行问答。结果显示，文本序列化基线在较长的时间序列窗口下会超出手机的上下文或内存预算，而PocketTSLM能够成功处理这些任务。所有推理均在设备上完成，未传输健康数据。

### Q5: 有什么可以进一步探索的点？

论文的局限性包括：1）仅在特定任务（睡眠分期和心电图问答）上验证，尚未扩展到更多生理信号和健康应用；2）数值一致性协议主要关注令牌序列一致性，但未深入评估生成理由的语义质量；3）软提示方法依赖预训练的OpenTSLM软提示变体，未探索在设备上微调或适应个性化数据的能力；4）未系统评估能耗、延迟和内存占用的详细权衡。未来方向可包括：扩展至更多时间序列任务（如异常检测、预测性维护），探索端侧持续学习与个性化，研究多模态传感器融合，以及开发更高效的软提示压缩和缓存策略。此外，可将PocketTSLM与Agent工作流结合，实现端侧证据路由和可追溯决策报告。

### Q6: 总结一下论文的主要内容

PocketTSLM是首个在消费级智能手机上完全本地运行的时间序列语言模型部署方案。它基于OpenTSLM软提示变体，通过将时间序列编码为嵌入而非文本令牌，保留了时序结构并大幅减少令牌数量。论文使用Apple MLX框架将模型移植到Swift，并设计数值一致性协议验证移植正确性。在端侧上下文经济学基准中，软提示路径比文本序列化基线使用约12倍更少的令牌，并降低预填充成本。实验在睡眠分期和心电图问答任务上验证了可行性，而文本基线在较长窗口下会超出手机资源限制。所有推理均在设备上完成，不传输健康数据，满足了隐私保护需求。该工作为在移动设备上部署时间序列语言模型提供了实用方案，并展示了软提示在资源受限环境下的优势。
