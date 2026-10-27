---
title: "OneEEG: A Unified Signal-Visual Multimodal Language Model with Task-Aware Mixture of Projectors for Multi-Task EEG Understanding"
authors:
  - "Jiacheng Zhang"
  - "Xueyi Zhang"
  - "Xin Lu"
  - "Siqi Cai"
  - "Haizhou Li"
date: "2026-10-26"
arxiv_id: "2610.35355"
arxiv_url: "https://arxiv.org/abs/2610.35355"
pdf_url: "https://arxiv.org/pdf/2610.35355v1"
categories:
  - "cs.LG"
tags:
  - "EEG"
  - "多模态大语言模型"
  - "任务感知混合投影器"
  - "信号-视觉对齐"
  - "指令微调"
  - "多任务理解"
  - "基准测试"
relevance_score: 6.5
---

# OneEEG: A Unified Signal-Visual Multimodal Language Model with Task-Aware Mixture of Projectors for Multi-Task EEG Understanding

## 原始摘要

Electroencephalography (EEG) is widely used in clinical assessment, brain-computer interfaces, and cognitive-state analysis, yet EEG modeling remains fragmented across task paradigms. Recent multimodal large language models (MLLMs) provide a promising interface for flexible multimodal reasoning, but their ability to understand EEG inputs remains limited. In this work, we propose OneEEG, a unified EEG-MLLM framework for multi-task EEG understanding. By training on our curated OneEEG-Instruct, a multi-task EEG instruction-tuning dataset, OneEEG jointly models numerical EEG representations and visual EEG representations, and introduces a task-aware Mixture of Projectors (MoP) to align heterogeneous EEG features across different task families with the LLM embedding space. We further establish OneEEG-Bench, a benchmark for evaluating current MLLMs and our method on multi-task EEG understanding. Experiments show that existing MLLMs have limited ability to interpret EEG inputs, while OneEEG achieves stronger performance by integrating numerical and visual EEG representations with task-aware EEG-to-LLM projection. Extensive ablations and analyses further reveal the effects of visual EEG renderings, MoP variants, router behavior, and feature dispersion across EEG tasks.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决脑电图（EEG）建模长期碎片化、难以在统一框架下支持多任务理解的问题。研究背景方面，EEG 广泛用于神经评估、癫痫分析、睡眠监测、脑机接口和认知状态估计等场景，但不同任务往往对应不同的实验范式、通道配置、受试群体和标注体系，且判别性模式高度依赖任务，涵盖时间动态、频谱特征和空间分布，因此现有 EEG 模型多基于任务特定假设，配有专门预处理和架构，限制了统一表示与交互框架的发展。

现有方法主要有两条路线：一是标准多模态大模型范式，用 EEG 编码器提取数值信号特征，再经共享投影器映射到 LLM 嵌入空间；二是将 EEG 渲染为波形图、频谱或地形图，交由视觉语言模型理解。二者存在两个不足：其一，单一共享投影器难以对齐异质 EEG 特征，EEG 信噪比低、内在语义弱，特征在不同任务间高度分散，单一映射易引入跨任务干扰；其二，仅支持单一输入形式，数值表示保留细粒度时间信息但编码器兼容性差，视觉表示提供灵活接口却损失细节。

因此，本文核心问题是：构建统一的 EEG-多模态大模型框架 OneEEG，同时建模数值与视觉两种 EEG 表示，并引入任务感知的投影器混合（MoP）机制，缓解单投影器瓶颈，实现跨异质 EEG 任务的任务感知对齐，配合 OneEEG-Instruct 指令微调数据集与 OneEEG-Bench 基准，系统评估多任务 EEG 理解能力。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类。方法类方面，EEG表征学习与基础模型是重要基础，LaBraM、EEGPT、Brant、CBraMod、BrainOmni、BIOT、Neuro-GPT、NeuroLM等采用自监督或大规模预训练学习可迁移EEG表征，但它们主要是表征编码器，缺乏自然语言交互与指令跟随能力；本文在此基础上将EEG表征与多模态语言模型结合，实现指令驱动的统一理解。多模态大模型方面，GPT-5.5、Gemini-3 Pro、Qwen VL、LLaVA等通用MLLM及Lingshu、MedGemma等医学MLLM具备强视觉理解能力，但EEG波形、频谱、地形图与自然图像差异显著，其EEG理解能力尚未被充分研究。EEG专用LLM/MLLM方面，CerebraGloss基于波形图像构建临床EEG视觉语言模型，WaveMind对齐EEG与文本、视觉模态，EEG-VLM研究基于EEG图像的睡眠分期视觉语言建模；这些工作多侧重信号到语言或视觉EEG解读之一，对数值与视觉EEG表征的统一支持不足，且缺乏跨任务统一评测，本文的OneEEG与OneEEG-Bench正是针对这些空白。混合专家方面，EEGMamba引入任务感知MoE，BrainMoE采用通道级专家路由，EEGMoE探索领域解耦专家；它们主要面向EEG特征提取，而本文提出任务感知的投影器混合（MoP），在EEG到LLM的投影阶段实现任务特化，以缓解跨任务对齐冲突。

### Q3: 论文如何解决这个问题？

OneEEG 的核心思路是将脑电理解统一到多模态大语言模型框架中，同时输入数值信号与波形图像两种表示，并用任务感知的投影器混合机制完成 EEG 特征到 LLM 空间的适配。

整体架构以 Qwen2.5-VL-7B 为语言主干并保留其原生视觉编码器，数值 EEG 信号则由预训练的 EEGPT 编码器处理。信号流将多通道 EEG 沿时间维切分为不重叠 patch，经通道感知嵌入与 Transformer 编码得到 EEG token 序列；视觉流把 EEG 渲染成波形图像，走 MLLM 原生视觉通路；文本流按标准分词嵌入。三路 token 拼接后送入语言模型生成答案。针对通道设置，标准 19 通道数据同时使用数值与视觉两路，非标准通道数据则省略数值信号、仅用波形图像。

关键创新是任务感知的 Mixture of Projectors（MoP）。它维护一个轻量投影器库，每个投影器为同构 MLP，将 EEG 特征映射到 LLM 隐藏维。基础 EEG 属性问题绕过路由，固定使用 basic 投影器；任务导向问题则由路由器结合 EEG token 特征与任务族嵌入计算 token 级打分，序列平均后做硬 top-1 选择，仅激活一个投影器，既保持效率又实现按任务族对齐异构 EEG 特征。

此外，对通道兼容样本采用前缀增强视觉条件：波形图像特征既作为辅助视觉前缀紧邻 EEG token，又保留原生图像占位符走预训练图文通路，从而在保留原有图像-文本接口的同时为 EEG token 提供局部视觉上下文。训练采用两阶段策略：第一阶段冻结编码器与 LLM，仅训练 MoP 完成投影对齐；第二阶段进一步训练 MoP、视觉投影器与 LLM 的 LoRA 参数，编码器保持冻结，以标准自回归语言建模目标优化。

### Q4: 论文做了哪些实验？

论文在自建的OneEEG-Bench基准上进行主实验，该基准包含基础EEG属性QA和任务导向EEG QA，覆盖Basic、Motor、State、Clinical、Event及非标准通道设置下的Sleep、Vigilance共七类任务。对比方法包括闭源MLLM（Gemini-3 Flash/Pro、GPT-5.5）、开源MLLM（Qwen2.5-VL-7B、Qwen3-VL-8B、InternVL3.5-8B/38B、LLaVA-OneVision-2-8B）、医学MLLM（MedGemma-1.5-4B、Lingshu-7B/32B）及EEG专用模型CerebraGloss。主要结果显示OneEEG取得最佳Overall 65.67%和Macro 68.24%，较最强基线GPT-5.5分别提升15.28和15.23个百分点，且无效输出率仅0.05%。消融实验在Phase 1设置下比较共享投影器、MoP自由/固定路由及视觉前缀等变体，完整OneEEG取得Overall 59.30%、Macro 59.57%的最优结果，验证MoP与视觉前缀的关键作用。此外还比较波形图、频谱图及其组合输入，发现波形图整体优于频谱图，组合未带来稳定增益；并通过t-SNE分析投影前后EEG表示的任务族聚类结构。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点。其一，EEG编码器在训练中保持冻结，作者也承认其提供的特征仍不完美且依赖任务，导致Motor、State等细粒度任务提升有限；未来可探索端到端微调或引入任务自适应编码器，甚至用对比学习预训练EEG表征。其二，视觉表征仅采用波形图，消融显示频谱图反而有害，说明视觉渲染方式仍较粗糙，可尝试时频图、拓扑脑图或多视图融合，并研究渲染参数对LLM理解的影响。其三，MoP采用固定路由，Free路由反而更差，说明路由策略尚不理想，可引入软路由、负载均衡或基于任务不确定性的动态路由。其四，基准覆盖任务与数据集有限，跨被试、跨设备泛化及长时EEG、实时推理效率尚未验证。此外，可结合可解释性分析（如投影前后表征对齐、注意力可视化）提升临床可信度，并探索数值与视觉表征的更优融合机制而非简单拼接。

### Q6: 总结一下论文的主要内容

论文针对EEG建模长期分散于各任务范式、现有MLLM难以理解EEG输入的问题，提出统一框架OneEEG，实现多任务EEG理解。方法上，OneEEG采用双流架构，同时建模数值EEG表示与波形图像视觉表示，并引入任务感知的投影器混合（MoP），通过路由器从投影器库中为不同任务族选择投影路径，缓解单一共享投影器带来的跨任务干扰；同时构建多任务指令微调数据集OneEEG-Instruct和评测基准OneEEG-Bench，并采用投影对齐与多模态指令微调两阶段训练。实验表明，现有MLLM解读EEG能力有限，OneEEG在基准上取得最佳总体与宏平均准确率，较最强基线GPT-5.5分别提升约15.28和15.23个百分点，消融验证了MoP与视觉前缀条件化的有效性。
