---
title: "EEG-Captioner: Grounding EEG-to-Language Generation in Fundamental Signal Properties"
authors:
  - "Leyuan Jin"
  - "Jiahao Mei"
  - "Yixuan Yuan"
  - "Shimeng Li"
  - "Mengyue Wu"
  - "Yue Ding"
date: "2026-10-22"
arxiv_id: "2610.30995"
arxiv_url: "https://arxiv.org/abs/2610.30995"
pdf_url: "https://arxiv.org/pdf/2610.30995v1"
categories:
  - "cs.LG"
tags:
  - "EEG-to-language"
  - "signal captioning"
  - "signal-level QA"
  - "multimodal encoder"
  - "time series semantics"
  - "factual consistency"
relevance_score: 6.5
---

# EEG-Captioner: Grounding EEG-to-Language Generation in Fundamental Signal Properties

## 原始摘要

Electroencephalography (EEG)-to-language models offer a promising approach for translating complex neural signals into human-readable descriptions. However, generating plausible language does not necessarily demonstrate that a model has learned to interpret the underlying EEG signal. A direct way to assess such interpretation is to probe objectively measurable properties of the signal itself. We therefore construct an EEG-language dataset of 160,781 segments annotated with signal-level question answering (QA) pairs, where each question targets one of five property families and requires a quantitative comparison involving spectral, spatial, temporal, or lateral signal properties. Each segment is also paired with a feature-grounded EEG caption. We further propose a Dual-Domain EEG Encoder that jointly models temporal waveforms and spectral-spatial representations, and introduce EEG-Captioner, a unified EEG-to-language framework trained with both signal-level QA and EEG caption supervision. Experiments show that the proposed encoder achieves the highest overall macro-averaged balanced accuracy (Macro-BA) among the compared EEG encoders, while EEG-Captioner achieves a Macro-BA of 88.81% on signal-level QA and improves caption factual consistency from 82.06% to 83.46% over caption-only language adaptation, demonstrating the complementary benefits of signal-level QA and caption supervision.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注脑电图（EEG）到自然语言生成任务中的“接地”（grounding）问题。研究背景是：EEG 能无创、高时间精度地测量神经活动，而大语言模型为把复杂神经信号转写为人类可读描述提供了新途径。然而，现有 EEG-to-language 模型（如 E²-LLM、CerebraGloss、NeuroNarrator）虽能生成看似合理的文本，却缺乏对信号本身可测量属性的显式监督与直接评估，因此难以判断生成描述是否真正基于时间、频谱、空间和半球偏侧等基本信号特征；同时，现有 EEG 表征模型（EEGNet、BIOT、LaBraM 等）主要面向下游任务，并非为保留这些属性而设计。针对上述不足，本文的核心问题是：如何构建带显式信号级监督与评估的 EEG-语言数据与统一框架，使 EEG 到语言的生成真正扎根于基本信号属性。为此，作者构建了含 160,781 个片段、覆盖五类信号属性问答与特征接地描述的数据集，提出联合建模时域波形与频谱-空间表示的双域 EEG 编码器，并引入统一框架 EEG-Captioner，通过信号级问答与描述监督联合训练，以同时提升基础 EEG 理解与事实一致的描述生成。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，EEG表示学习经历了从紧凑卷积与Transformer架构（如EEGNet、SleepTransformer）到大规模预训练模型（如BIOT、EEGPT、LaBraM、CBraMod）的发展，这些模型在下游任务上表现优异，但并非为保留语言生成所需的EEG信号属性而设计；本文提出的Dual-Domain EEG Encoder则联合建模时域波形与频谱-空间结构，并以学习到的紧凑token替代文本化特征。EEG到语言生成方面，E²-LLM将预训练EEG表示与LLM结合用于情感推理，但未显式监督信号属性；CerebraGloss对视觉-语言模型进行指令微调以做临床EEG解读，侧重临床特征；NeuroNarrator结合频谱-空间与时序建模，并用LLM评分评估生成描述中的信号属性。与上述工作相比，本文的区别在于构建了带信号级QA与特征锚定描述的数据集，对时域、频谱、空间和偏侧属性提供显式监督与直接评测，并通过QA与描述联合训练提升事实一致性。评测类方面，现有工作多依赖LLM评分或下游任务指标，缺乏对基础信号属性的系统化客观评估，本文以信号级QA的Macro-BA填补这一空白。

### Q3: 论文如何解决这个问题？

论文的核心思路是：不把“生成通顺语言”当作模型理解EEG的证据，而是用信号本身可客观测量的属性来约束和检验生成过程。为此，作者从TUEG v2.0.2构建了一个包含160,781个片段的EEG-语言数据集，每个片段配有信号级问答对和特征驱动的EEG描述。问答不回归绝对特征值，而是设计为关系比较，覆盖五个属性族：主导频带、最强脑区、峰值时段、时间模式和偏侧优势；每族含五种特征条件，共25个候选问答，答案由全精度数值特征直接计算，并通过有效性与歧义准则过滤不可靠标注。描述则由数值特征摘要引导大模型生成，仅描述时、频、空、偏侧特性，避免临床或认知推断。

架构上提出双域EEG编码器，包含两条并行分支：时间分支把各通道波形切分为短patch并投影为时间token，直接建模局部波形动态；频谱-空间分支将片段划分为Early/Middle/Last三个区间，用Welch法计算通道级PSD，再以通道自注意力建模电极间依赖。两分支表示经对齐融合后，通过通道注意力池化和全局Transformer聚合，输出EEG token。EEG-Captioner再用可学习投影器把这些token映射到LLM嵌入空间，作为多模态上下文。训练时共享同一编码器、投影器和LLM，用任务指令区分信号级问答与描述生成，联合优化两类监督。创新点在于以关系型信号问答作为可验证的中间监督，并与描述监督互补，使信号级问答Macro-BA达88.81%，描述事实一致性从82.06%提升到83.46%。

### Q4: 论文做了哪些实验？

实验基于作者构建的EEG-language数据集开展，共160,781个EEG片段，按文件名不相交方式划分为128,625/16,078/16,078的训练、验证与测试集，所有实验共用同一划分。评估指标包括：信号理解任务报告各属性族平衡准确率（BA）及其宏平均Macro-BA；描述生成任务报告BLEU-4、ROUGE-L，并用GPT-5.6 Sol从主导频谱模式、时间趋势、频谱特征、空间分布四方面评估事实一致性（0–100%）。

编码器对比实验将提出的Dual-Domain EEG Encoder与LaBraM、CBraMod在表示层（五类信号级QA）和语言层（接入Qwen2.5-Omni-7B）比较。分类器阶段Dual-Domain取得89.87% Macro-BA，优于LaBraM（76.06%）和CBraMod（50.45%）；迁移到Qwen后仍保持优势（86.06% vs 73.47%、47.96%）。扰动实验（跨样本打乱EEG或置零）导致性能显著下降，说明模型依赖EEG输入而非语言捷径。

EEG-Captioner评估在相同冻结编码器下比较三个变体：仅描述适配、仅信号级QA、联合训练。仅描述适配Macro-BA为47.82%，仅QA为86.06%，EEG-Captioner提升至88.81%；描述事实一致性由82.06%提升至83.46%，ROUGE-L由0.4722升至0.4865，BLEU-4由0.3124升至0.3302。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点。其一，信号级QA仅覆盖频谱、空间、时间、偏侧五类属性，且以定量比较为主，未来可扩展到更细粒度属性（如相位耦合、事件相关电位成分、跨频段耦合）及开放式描述，检验模型是否真正理解而非模式匹配。其二，数据集仅16万余段且来自有限采集范式，跨被试、跨设备、跨任务的泛化性未验证，可构建多中心基准并引入被试无关评估协议。其三，Dual-Domain编码器虽融合时域波形与频谱-空间表示，但两域交互仍较浅，可探索跨域注意力或对比对齐，使频谱-空间特征反哺时域建模。其四，QA与caption联合训练仅带来约1.4%的事实一致性提升，说明监督信号互补性未被充分挖掘，可尝试课程学习、属性可控生成或基于可解释性反馈的强化学习，将信号属性作为生成约束。此外，可引入不确定性估计与错误归因机制，区分模型是"语言流畅"还是"信号理解"，从而更严格地评估接地性。

### Q6: 总结一下论文的主要内容

论文针对脑电图到语言生成中“语言流畅不等于真正理解信号”的问题，提出以可客观测量的信号属性来检验和约束模型。作者构建了包含160,781个片段的EEG-语言数据集，每个片段配有信号级问答对，覆盖频谱、空间、时间与偏侧性五类属性，并附有基于特征的EEG描述。方法上，提出双域EEG编码器，联合建模时域波形与频谱-空间表示，并构建统一框架EEG-Captioner，同时用信号级问答和EEG描述监督训练。实验表明，该编码器在对比编码器中取得最高宏平均平衡准确率，EEG-Captioner在信号级问答上达到88.81%，并将描述事实一致性从82.06%提升至83.46%，说明信号级问答与描述监督具有互补收益，有助于将EEG到语言生成锚定在可测量信号属性上。
