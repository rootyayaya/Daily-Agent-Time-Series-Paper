---
title: "Detect, Explain, Interpret: An End-to-End Benchmark for Time Series Anomaly Detection, Explainability and Interpretability"
authors:
  - "Roberto Stanzione"
  - "Jules Barbe"
  - "Magali Parrino"
  - "Jérémie Fourmann"
  - "Paul Boniol"
date: "2026-10-01"
arxiv_id: "2610.01168"
arxiv_url: "https://arxiv.org/abs/2610.01168"
pdf_url: "https://arxiv.org/pdf/2610.01168v1"
categories:
  - "cs.LG"
  - "cs.AI"
  - "cs.DB"
tags:
  - "Time Series Anomaly Detection"
  - "Explainability"
  - "Interpretability"
  - "Benchmark"
  - "Multivariate Time Series"
  - "High-dimensional Time Series"
  - "LLM for Time Series"
  - "Industrial Sensor Data"
  - "Cloud Storage Systems"
  - "Anomaly Attribution"
  - "Semantic Annotation"
  - "Frozen LLM Baselines"
  - "Real-world Dataset"
  - "Detection-Explainability-Interpretability Pipeline"
relevance_score: 8.5
---

# Detect, Explain, Interpret: An End-to-End Benchmark for Time Series Anomaly Detection, Explainability and Interpretability

## 原始摘要

Time Series Anomaly Detection has received increasing attention, driven by the growing availability of complex time series data. This surge has led to the development of numerous detection methods, as well as a variety of benchmarks aimed at thoroughly evaluating their performance. However, most existing detectors remain largely agnostic to domain context, overlooking explainability and interpretability. One of the main reasons for this gap is that current benchmarks primarily focus on detection accuracy, and only few of them evaluate spatial explainability. Moreover, no benchmark currently provides sufficiently rich semantic annotations to support the generation of human-understandable interpretations of anomalies. To address these limitations, we introduce SHAD (Scality High-dimensional Anomaly Detection benchmark), a fully annotated benchmark composed of 215 multivariate, high-dimensional time series collected from real-world distributed cloud storage systems operated by Scality. The proposed dataset includes rich contextual information, covering three families of anomalies with varying degrees of severity. As further contribution, we provide a foundation for future work by evaluating baseline methods for Detection, Explainability, and Interpretability, covering all stages of a TSAD pipeline. For Detection, we benchmark a wide range of existing anomaly detectors, testing their effectiveness on the proposed real-world dataset. Then, we consider explainability by evaluating whether measuring the contribution of each dimension in the generated anomaly score can provide accurate anomaly attributions. Finally, for interpretability, we investigate the effectiveness of frozen LLM baselines in localizing and interpreting anomalies.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决时间序列异常检测领域评测基准“重检测精度、轻可解释性”的问题。随着复杂时间序列数据不断增多，异常检测方法层出不穷，相关基准也大量涌现，但多数检测器对领域上下文不敏感，忽略可解释性（explainability）与可解读性（interpretability）。其根源在于现有基准主要评估检测准确率，仅少数涉及空间层面的可解释性，且没有任何基准提供足够丰富的语义标注来支撑生成人类可理解的异常解释。例如 Exathlon 虽提供根因与影响区间，但异常类型粗粒度、未显式映射到系统组件，也缺乏细粒度、语义丰富的逐维度标注。同时，LLM 虽推动可解释方案发展，但高质量、带文本上下文的时间序列数据稀缺，研究者被迫依赖合成数据，难以进行真实场景评估。为此，本文提出 SHAD 基准，包含 215 条来自 Scality RING 分布式云存储系统的高维多元时间序列，覆盖正常与三类不同严重程度的异常，并提供逐维度标签、组件映射及详细文档。其核心目标是首次支持对完整 TSAD 流水线（检测、解释、解读）进行端到端评测，并给出 18 种检测器、空间归因及零样本 LLM 定位与解释的基线评估。

### Q2: 有哪些相关研究？

相关研究可分为三类。方法类方面，距离、密度和预测（预测/重构）三类检测器是主流，但大多与领域上下文无关；可解释方法分内在可解释模型（如决策树）与模型无关方法（LIME、Anchors、SHAP及其时序扩展、DuoGAT等），后者通过扰动或特征归因给出空间归因；可解释性研究则相对有限，如MacroBase、Boubekki等的ECG内部表示聚类，以及ChatTS等支持多变量时序推理的多模态LLM。应用类方面，LLM已被用于异常检测、结合文本上下文提升预测与决策，以及基于Agent和工具增强的根因分析。评测类方面，NAB、TODS、TimeEval、TimeSeAD、TSB-UAD、Exathlon、TSB-AD、TAB等基准主要评测检测精度，仅Exathlon涉及空间可解释性，均缺少细粒度维度标签与语义描述。本文的SHAD与上述工作的区别在于：基于Scality真实分布式云存储系统构建215条多变量高维序列，提供逐维度标签与描述，并首次端到端覆盖检测、可解释性与可解释性（含冻结LLM基线）三个阶段的评测。

### Q3: 论文如何解决这个问题？

论文的核心贡献在于构建了SHAD这一端到端基准，从检测、可解释性和可解读性三个层面系统性地解决现有基准的不足。整体框架基于Scality Ring分布式对象存储系统搭建实验环境，每个集群由一台管理服务器和三台存储服务器组成，每台存储服务器配备四块数据盘、两块元数据盘和一块系统盘，运行六个软件存储节点及一个S3连接器，共采集171个指标，形成215条多变量高维时间序列，每条约1021个数据点，采样间隔为1分钟。

在异常设计上，论文定义了服务器故障、磁盘故障和存储节点故障三类异常，并支持单点、同时和异步三种模式，异步模式进一步细分为级联、滚动和独立三种子模式，同时引入严重程度参数，覆盖从最小影响到高影响的多种场景。标注体系分为两层：顶层标注为每个时间点赋予二值标签表示异常是否发生；维度级标注则仅标记与根因组件直接相关的维度，从而实现精确的异常归因。

在评估方法上，论文为TSAD流水线的各阶段提供了基线：检测阶段测试多种现有异常检测器在真实数据集上的效果；可解释性阶段评估通过度量各维度对异常分数的贡献能否提供准确的异常归因；可解读性阶段则探索冻结LLM基线在定位和解释异常方面的有效性。其创新点在于首次提供了具有丰富语义标注的高维真实世界基准，支持从检测到归因再到自然语言解释的全流程评估，填补了现有基准在可解释性和可解读性方面的空白。

### Q4: 论文做了哪些实验？

论文围绕三个研究问题在SHAD基准上展开实验。检测方面，评估了18种最先进检测方法（含半监督与无监督），使用TSB-AD优化超参数，以VUS-PR（25点缓冲）为指标。结果显示半监督方法整体优于无监督方法，但无监督的KMAD与OA、USAD、AE、CNN等顶级半监督方法在α=0.05下无显著差异；半监督方法擅长检测微弱异常（如Single Snode、Single Disk），而KMAD对系统级事件（如异步服务器故障）更鲁棒。可解释性方面，选取OA、CNN、KMAD，用NDCG评估维度归因，发现其表现接近随机基线，说明检测精度无法直接转化为诊断能力；污染维度少的异常（Single Disk仅4维）最难定位。可解释性（LLM）方面，用Catch22特征、多面板图像和自然语言描述三种表示，对5个LLM进行单次调用问卷测试，覆盖存在性、类型、严重度（F1）及维度、时间定位（准确率），重复5次。结果整体偏低：存在性约0.43-0.48，类型最高21%（图像），严重度最高16%，维度定位仅1-4%，时间定位最高12%（Claude）。加入level₁监督后维度与时间定位平均提升7.2%和7.9%，level₂后时间定位再提升14.4%。同族Mistral模型对比显示规模影响性能。

### Q5: 有什么可以进一步探索的点？

当前工作的局限主要有三点：一是现有检测器在SHAD上仍非完美，尤其对高维、低幅度异常易漏检；二是可解释性无法直接复用检测器的归因分数，维度级贡献评估尚缺专用方法；三是冻结LLM难以正确解读异常，说明仅靠文本提示不足以弥合数值与语义的鸿沟。未来可从以下方向探索：其一，研究在移除直接受影响指标后的鲁棒检测，检验模型是否依赖捷径特征；其二，基于SHAD的逐维标签训练专用可解释性模型，替代原生归因，并引入因果或反事实分析提升归因可信度；其三，将可靠的维度级解释结构化为语义增强上下文，结合检索增强或轻量微调，使LLM生成有数据与语义双重依据的解释。此外，可探索检测、解释、解读三阶段的联合优化与端到端评估协议，并关注跨系统、跨严重程度的泛化能力。

### Q6: 总结一下论文的主要内容

论文针对时间序列异常检测中现有基准普遍只关注检测精度、忽视可解释性与可解读性的问题，提出了SHAD——一个端到端基准数据集。SHAD包含215条来自Scality真实分布式云存储系统的高维多变量时间序列，涵盖三类不同严重程度的异常，并提供逐维度标签及丰富的文本语义标注。论文在检测、可解释性和可解读性三个阶段评估了基线方法：检测方面测试了多种现有异常检测器；可解释性方面考察异常分数中各维度贡献能否提供准确归因；可解读性方面探索冻结LLM定位与解释异常的效果。结论表明，现有SOTA检测方法虽准确但并非完美，现有方法无法原生解决可解释性问题，冻结LLM也无法给出正确解释。SHAD为后续研究提供了新方向。
