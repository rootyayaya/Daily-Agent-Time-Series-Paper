---
title: "LEMMO: A Large Electromagnetic Model leveraging Pretrained LLMs for Million-Sample Signal Understanding"
authors:
  - "Mingkai Li"
  - "Jiajun Wu"
  - "Yihan Mao"
  - "Zilin Sang"
  - "Taosong Yu"
  - "Yuan Ma"
  - "Minghe Liu"
  - "Qianqian Yang"
  - "Zhiguo Shi"
date: "2026-11-06"
arxiv_id: "2611.09476"
arxiv_url: "https://arxiv.org/abs/2611.09476"
pdf_url: "https://arxiv.org/pdf/2611.09476v1"
github_url: "https://github.com/N1rv4n4/LEMMO"
categories:
  - "cs.AI"
  - "cs.SD"
tags:
  - "电磁信号理解"
  - "LLM多模态扩展"
  - "长信号描述生成"
  - "指令驱动识别"
  - "信号到文本"
  - "百万级样本处理"
  - "线性注意力编码器"
  - "时序重采样"
  - "信号证据检索"
  - "结构化查询"
  - "事实监督"
  - "大规模信号数据集"
relevance_score: 7.5
---

# LEMMO: A Large Electromagnetic Model leveraging Pretrained LLMs for Million-Sample Signal Understanding

## 原始摘要

Large language models have expanded beyond text to vision, audio, and other modalities, but understanding raw electromagnetic (EM) signals remains challenging. Wideband recordings can contain millions of samples, whereas existing waveform-based EM models are primarily evaluated on short in-phase and quadrature (IQ) segments, leaving long-recording understanding and detailed description insufficiently explored. We introduce LEMMO, a large EM model for instruction-driven recognition and description of long raw IQ recordings. LEMMO combines a linear-attention EM encoder with anti-aliased temporal resampling to process up to eight million complex samples. Its EM-text interaction module conditions learnable queries on instructions before retrieving signal evidence. Compact queries support recognition, while structured queries with auxiliary factual supervision organize scene-level properties, signal attributes, and cross-signal relationships for detailed description. We also construct and release a unified 1.38-TB corpus of real-world and synthetic EM signals, including LEMMO-ShortQA and LEMMO-LongDesc. Compared with MERLIN-LoRA, LEMMO improves mean EM-Bench perception accuracy by 15.77 %, mean strategy-generation ROUGE-L F1 by 4.38 points, and mean LEMMO-ShortQA accuracy by 14.31 %. It also improves categorical and numerical fact F1 on both LEMMO-LongDesc tasks while preserving its language backbone's MMLU performance. Our code and datasets are available at https://github.com/N1rv4n4/LEMMO and https://huggingface.co/datasets/DaftJun/RFLAS, respectively.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决如何让大语言模型直接理解长段原始电磁信号（IQ 记录）并生成自然语言描述的问题。研究背景是：电磁信号承载无线活动信息，对通信、感知、自主系统和安全等应用至关重要；LLM 已从文本扩展到视觉等模态，但理解原始电磁信号仍具挑战。现有方法的不足主要有三点：一是任务特定的深度学习和电磁基础模型多在仅含数百到数千个 IQ 样本的短片段上训练和评估，无法证明其理解百万级样本长记录的能力；二是 RF-GPT 等基于频谱图的方法不显式保留相位信息，时频细节受图像分辨率限制；三是 MERLIN、PReD 等虽连接信号表示与 LLM，但缺乏对长原始 IQ 的详细描述能力。本文要解决的核心问题是：在未知信号时频位置、不能依赖目标裁剪或滤波的条件下，如何高效编码高达八百万复数样本的连续宽带 IQ 记录，并构建指令驱动的信号到语言接口，使模型能根据指令选择相关证据，既完成识别任务，又对信号成分、属性及其关系进行详细描述。为此作者提出 LEMMO，结合线性注意力编码器、抗混叠时间重采样和指令条件化的 EM-文本交互模块，并构建统一语料与 LEMMO-ShortQA、LEMMO-LongDesc 基准。

### Q2: 有哪些相关研究？

相关研究主要分为两类。第一类是电磁基础模型，侧重自监督可迁移表征学习：RIS-MAE对原始IQ信号做掩码重建，IQFM采用对比学习，SpectrumFM、6G WavesFM和WiFo面向频谱管理、通信、感知、定位与信道预测；Patch化分词和EMind的长度自适应多信号打包则提升了编码效率与异构输入适应性。这类工作仅提供表征，缺乏指令驱动交互与自然语言描述，且多在数千采样点的短输入上评测，难以覆盖长时突发、频率变化与跨事件关系。第二类是电磁-语言模型，将信号与LLM结合：RadioLLM用提示与token重编程，WirelessLLM微调LLM处理无线任务，MERLIN联合学习信号表征并适配预训练LLM；Seeing Radio、RF-GPT将信号转为图像表征，PReD融合波形、频谱、时频图与星座图等多视图，DiSC-AMC将数值特征离散为符号token并结合检索做调制分类。这些方法虽支持语言化处理，但视觉表征保真度受变换与渲染分辨率限制，幅度谱图不显式保留相位。LEMMO的区别在于直接以原始IQ为输入，通过线性注意力编码与抗混叠重采样处理多达八百万复数采样，并以指令条件化的结构化查询和辅助事实监督生成场景级、属性级与跨信号关系的详细描述。

### Q3: 论文如何解决这个问题？

LEMMO 的核心思路是把原始 IQ 波形通过“指令条件化的信号接口”映射到语言模型嵌入空间，从而让 LLM 直接完成长记录识别与描述。整体框架由 EM tokenizer、EM encoder、时间重采样器、EM-text 交互模块和 Qwen3.5-4B 语言骨干组成。

首先，EM tokenizer 对 I/Q 两路使用统一峰值幅度归一化，将不同无线技术的记录放到同一尺度，再切成 16 个 IQ 样本的非重叠 patch，并加入正弦位置编码、采样率 token 和可学习 CLS token。EM encoder 采用 12 层因果线性注意力，计算量随 token 长度近似线性，并通过掩码波形重建进行预训练，使编码器先学习波形结构。

针对百万级长记录，时间重采样器对超过一百万样本的序列按每百万样本切分子序列，每个子序列经六阶段下采样压缩 64 倍，再拼接后由两层双向线性注意力整合跨子序列上下文；短记录则直接跳过重采样。

关键创新在 EM-text 交互模块：可学习查询先对任务指令做交叉注意力，再检索信号特征，使同一记录能按任务提取不同证据。识别任务使用 16 个查询（Q16），并接四个任务特定残差适配器与分类头做辅助监督；描述任务使用 128 个结构化查询（Q128），分为全局、对象和关系查询，并引入位置编码和事实预测头，监督场景属性、对象计数、信号属性及跨信号关系。最终查询表示投影到 LLM 嵌入空间，与指令一起输入冻结的 Qwen3.5-4B，仅用 rank-16 LoRA 微调，实现指令驱动的识别与详细描述。

### Q4: 论文做了哪些实验？

论文在四个数据集上开展实验：自建的LEMMO-ShortQA（45类、输入128至500万IQ样本，含AMC、JPR、UAV识别、WTC四任务）、LEMMO-LongDesc（4G LTE、5G NR、基础调制、ISM、UAV信号，输入约40万至800万样本）、公开的EM-134K（13.4万信号-语言对，用于指令微调）与EM-Bench（14任务、每任务300例，仅评测）。对比方法为MERLIN-LoRA（冻结Qwen3-4B-Instruct-2507并加rank-16 LoRA）及GPT-6 Luna、DeepSeek-V4.1-Flash、Gemini-3.5-Flash-Lite、Qwen3.8-Flash四个通用LLM，并额外用MMLU评估通用知识保持情况。

主要结果：EM-Bench上LEMMO在14项任务中11项最优，感知平均准确率59.30%（较MERLIN-LoRA提升15.77个百分点），策略生成平均ROUGE-L F1为47.64（+4.38）；LEMMO-ShortQA平均准确率70.05%（+14.31%），其中UAV识别从41.88%升至73.75%（+31.87%）；LEMMO-LongDesc场景概览七项指标全领先，Category F1与Value F1分别提升5.07和8.73，单信号描述Category F1提升6.99；MMLU保持64.98%，略高于骨干64.34%，而MERLIN全量微调后降至30.00%。输入长度消融显示4K→4M时Category F1提升26.32、Value F1提升22.21。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点：其一，LEMMO 依赖大规模标注语料（1.38 TB）与辅助事实监督，数据构建成本高，未来可探索自监督预训练、少样本/零样本迁移，降低对人工标注的依赖。其二，模型上限为八百万采样点，对更长的连续宽带记录仍受显存与序列建模限制，可研究分段记忆、流式推理或稀疏注意力以支持超长信号。其三，评测集中于识别与描述，缺乏对时序定位、异常检测、因果推理等任务的验证，可扩展至故障诊断等下游场景。其四，电磁信号与文本对齐的可解释性不足，结构化查询虽提供事实监督，但证据溯源与置信度校准仍待加强。此外，可引入跨模态（频谱图、协议元数据）融合，并探索模型在低信噪比、未知调制方式下的鲁棒性与泛化能力。

### Q6: 总结一下论文的主要内容

论文针对现有电磁信号模型主要在短IQ片段上训练评估、难以理解百万级原始IQ长记录的问题，提出LEMMO——一个面向指令驱动识别与描述的大型电磁模型。方法上，LEMMO结合线性注意力电磁编码器与抗混叠时间重采样，可处理多达八百万个复数样本；其电磁-文本交互模块先以指令条件化可学习查询，再检索信号证据，并设计紧凑识别查询（Q16）与结构化描述查询（Q128，含全局、对象特征和关系分组及辅助事实监督）两种配置。作者还构建并发布了1.38TB真实与合成电磁信号语料，包括LEMMO-ShortQA和LEMMO-LongDesc。实验表明，相比MERLIN-LoRA，LEMMO在EM-Bench平均感知准确率提升15.77%，策略生成ROUGE-L F1提升4.38点，ShortQA准确率提升14.31%，并在长描述任务上改善类别与数值事实F1，同时保持语言主干MMLU性能。
