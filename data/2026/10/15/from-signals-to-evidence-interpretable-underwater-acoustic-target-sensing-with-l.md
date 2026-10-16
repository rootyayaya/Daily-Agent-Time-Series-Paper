---
title: "From Signals to Evidence: Interpretable Underwater Acoustic Target Sensing with Large Language Models - Part I: Framework and Recognition"
authors:
  - "Yuge Zhang"
  - "Jie Chen"
  - "Zhengqiao Zhao"
  - "Xiling Yao"
  - "Lingji Xu"
  - "Jingdong Chen"
  - "Yixin Yang"
date: "2026-10-15"
arxiv_id: "2610.22064"
arxiv_url: "https://arxiv.org/abs/2610.22064"
pdf_url: "https://arxiv.org/pdf/2610.22064v1"
categories:
  - "cs.SD"
  - "eess.SP"
tags:
  - "LLM for time series"
  - "interpretable time series"
  - "underwater acoustic sensing"
  - "physics-aware encoding"
  - "evidence-grounded reasoning"
  - "multimodal time series"
  - "attribute-level evaluation"
  - "industrial fault diagnosis"
  - "semantic report generation"
  - "signal-to-evidence chain"
relevance_score: 7.5
---

# From Signals to Evidence: Interpretable Underwater Acoustic Target Sensing with Large Language Models - Part I: Framework and Recognition

## 原始摘要

Underwater acoustic target detection and recognition are essential to marine surveillance and intelligent ocean sensing. Despite substantial advances in deep learning, existing systems typically produce binary detection decisions, categorical labels, or scalar confidence scores, offering limited insight into the physical evidence underlying their outputs. Large language models (LLMs) offer an opportunity to move underwater acoustic sensing toward interpretable, evidence-grounded understanding; however, generic audio encoders struggle to capture the distinctive physical characteristics of underwater acoustics, and physically annotated data are scarce. In this paper, the first of a two-part series, we propose a from-signals-to-evidence framework that integrates physics-aware acoustic encoding with a pretrained LLM, organized around a unified feature-evidence-decision chain with a shared reasoning core. An open input layer accommodates heterogeneous information-raw waveforms, time-frequency representations, environmental and geographic data, and textual physical priors-unifying detection and recognition within a common formulation. In Part I, we instantiate this framework for target recognition through an Underwater Acoustic Physics-aware Transformer (UPT), which tokenizes complementary acoustic representations and learns task-disentangled physical representations through four physics-oriented learning tasks. We develop a physics-parameterized data engine that provides traceable supervision at two levels of granularity and introduce an attribute-level evaluation protocol to assess the physical fidelity of generated descriptions. Experiments on simulated recordings of four vessels demonstrate accurate vessel recognition and reliable estimation of shaft frequency, blade-passing frequency, and machinery-related attributes.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决水下声学目标检测与识别中“决策不可解释、缺乏物理证据支撑”的核心问题。研究背景方面，被动水下声学感知是海洋监视与智能海洋观测的基石，其处理链包括检测与识别两个阶段，但舰船辐射噪声在传播中严重衰减和畸变，不同船型又可能呈现相似的频谱与调制模式，使得可靠检测与稳健识别长期面临挑战。现有方法存在明显不足：早期基于LOFAR、DEMON、MFCC等手工特征的方法虽有一定物理可解释性，却在复杂声学环境中性能受限；深度神经网络虽提升了识别精度，但其决策范式仍不透明，通常只输出二值检测、类别标签或标量置信度，置信度还可能校准不良，无法揭示哪些声学线索支撑了结论。本文要解决的核心问题是：如何将水下声学感知从“硬标签+置信度”推进到“以证据为基础的可解释决策”。为此，作者提出从信号到证据的UPD框架，将物理感知声学编码器与预训练LLM通过跨模态对齐耦合，构建“特征—证据—决策”链；Part I针对识别任务实例化该框架，设计UPT对互补声学表示进行令牌化，并通过四个物理导向任务学习任务解耦表示，同时构建物理参数化数据引擎提供双粒度监督，引入属性级评估协议，以验证生成描述在物理属性上的保真度。

### Q2: 有哪些相关研究？

相关研究可分为三类。方法类方面，经典声学分析依赖LOFAR、DEMON和MFCC等手工特征，提取轴频线、叶频谐波等物理线索，但特征在噪声遮蔽和时变条件下不稳定，且依赖专家设计。数据驱动方法则用CNN、RNN、注意力残差网络和Transformer在ShipsEar、DeepShip等数据集上提升分类精度，MHT-UATR-Transformer还引入层次化分词与掩码重建自监督学习，并结合数据增强、迁移学习和少样本适应。应用与语义类方面，DEMONet利用DEMON特征路由专家网络，UART实现音频、频谱图与模板描述的三模态对比对齐，MF-UATR融合预训练语言-音频表示，ASE-CLAP用LLM构建声学语义描述并丰富类原型。评测类方面，UA-Bench对九个开放LALM在合成水声信号上评测，最高叶级准确率仅13.1%，显示通用模型迁移能力有限。本文与上述工作的区别在于：不再停留于类别标签或置信度，而是将物理感知编码器与预训练LLM耦合，通过UPT和物理参数化数据引擎生成可验证、带证据的细粒度物理描述，并引入属性级评测协议。

### Q3: 论文如何解决这个问题？

论文提出“从信号到证据”的统一框架，将水下声学感知组织为特征—证据—决策链：F=φ(X)、E=g(F,P)、D=h(E)。核心是让决策D条件依赖于显式证据E，而非直接依赖特征F，从而区别于事后解释方案。框架以LLM为共享推理核心，将声学信号、时频表示、环境地理信息与文本物理先验统一映射到同一语义空间，输入层开放可扩展，新信息源只需增加编码器或扩展文本上下文。

在识别实例化中，论文设计了水下声学物理感知Transformer（UPT）。它从接收信号中提取三种互补表示：Log-Mel谱图、时变线谱和DEMON谱，分别独立分块嵌入，并附加位置嵌入与特征类型嵌入，使每个声学token锚定到特定物理结构。UPT围绕四个物理分析任务训练：轴频估计、轴频趋势估计、叶频估计和机械线谱检测，通过任务特定注意力自适应加权三种表示，并利用四个任务分支与共享Transformer编码器实现任务解耦，避免物理语义相互干扰。其损失为四项任务的加权组合。

训练采用两阶段协议：先优化UPT，再以仅答案目标微调完整框架。UPT输出与文本查询一起投影到预训练LLM（Qwen3-4B-Instruct）的嵌入空间，通过LoRA适配，冻结其余预训练参数，将学习负担限制在声学到语义的映射上。输出为结构化描述D=⟨d;e1,…,eM⟩，每个证据项对应可验证的声学特征子集，并强制“先证据后决策”的字段顺序。

此外，论文构建物理参数化数据引擎，从显式采样的物理参数合成可追溯样本，提供两级粒度监督，并引入属性级评估协议检验生成描述的物理保真度。创新点在于：物理接地的可验证证据链、任务解耦的物理感知编码、共享LLM推理核心以及可追溯的数据生成机制。

### Q4: 论文做了哪些实验？

论文在仿真录音上开展了实验，覆盖四类舰船目标。实验设置上，采用物理参数化数据引擎生成带物理标注的8秒信号，包含稳态低速、稳态高速、加速和减速四种工况，身份参数在类间刻意重叠以避免平凡判别。数据集为四类舰船的仿真录音，提供轴频、叶频及机械属性等两级粒度的可追溯监督。对比与评估方面，论文引入属性级评估协议，用于衡量生成描述在物理属性上的保真度，而非仅看分类标签。主要结果包括：系统能准确完成舰船识别，并可靠估计轴频、叶片通过频率（BPF）及机械相关属性；四个物理分析任务（SFE、STE、BPFE、MLD）中，线谱对SFE和MLD更关键，DEMON谱对STE和BPFE不可或缺，任务特定注意力系数提供了可解释的贡献度量。此外，UPT与Qwen3-4B-Instruct通过LoRA对齐，采用仅答案目标训练，验证了从信号到证据链的可行性。

### Q5: 有什么可以进一步探索的点？

当前工作主要验证于仿真数据，四类船只规模有限，物理参数化引擎虽提供可追溯监督，但与真实海洋环境的信道复杂性、噪声非平稳性仍有差距，域偏移下的泛化能力尚未充分检验。其次，属性级评估聚焦轴频、叶频等显式物理量，对推理链条本身的逻辑一致性与证据—决策因果性缺乏量化指标，LLM 仍可能生成貌似合理却与声学特征不符的描述。未来可探索：一是引入真实海试数据或半监督/域自适应方法，缩小仿真—实测鸿沟；二是将框架扩展至多目标、多传感器与阵列场景，并与 Part II 的低信噪比检测形成闭环；三是设计证据可验证性度量与不确定性校准机制，使每条证据可回溯至具体时频结构；四是结合声传播模型做物理约束的提示学习或检索增强，提升环境先验的利用效率。

### Q6: 总结一下论文的主要内容

本文提出一种“从信号到证据”的可解释水声目标感知框架，将物理感知声学编码器与预训练大语言模型耦合，围绕统一的“特征—证据—决策”链组织检测与识别任务。作为两部分系列的第一篇，论文聚焦识别场景，设计了水下声学物理感知Transformer（UPT），对Log-Mel谱、时变线谱和DEMON谱进行独立token化，并通过轴频估计、轴频趋势、叶频估计和机械线谱检测四项物理任务学习任务解耦的物理表征。为解决数据稀缺，作者构建了物理参数化仿真数据引擎，提供离散物理属性标签与结构化文本描述的双粒度监督，并提出属性级评估协议。四类舰船仿真实验表明，该方法能准确识别目标，并可靠估计轴频、叶频及机械相关属性，验证了证据驱动水声识别的可行性。
