---
title: "An integrated diffusion-weighted imaging processing and interpretation platform for MR-guided radiotherapy"
authors:
  - "Yunxiang Li"
  - "Yan Dai"
  - "Yen-Peng Liao"
  - "Jie Deng"
  - "Jill B De Vis"
  - "You Zhang"
date: "2026-08-20"
arxiv_id: "2608.20519"
arxiv_url: "https://arxiv.org/abs/2608.20519"
pdf_url: "https://arxiv.org/pdf/2608.20519v1"
categories:
  - "physics.med-ph"
  - "cs.AI"
tags:
  - "RAG"
  - "LLM agent"
  - "time series report"
  - "traceable diagnosis"
  - "clinical interpretation"
  - "tool use"
  - "knowledge base"
  - "evidence routing"
  - "MR-guided radiotherapy"
  - "diffusion-weighted imaging"
relevance_score: 7.5
---

# An integrated diffusion-weighted imaging processing and interpretation platform for MR-guided radiotherapy

## 原始摘要

Background: Magnetic resonance imaging-guided linear accelerators (MR-Linacs) allow diffusion-weighted imaging (DWI) to be acquired at every treatment fraction, but converting these low-signal-to-noise-ratio acquisitions into clinical decisions requires both reliable quantitative processing and an interpretation that reconciles a scattered and often contradictory literature.
  Purpose: To describe and evaluate an integrated, web-based platform that carries raw MR-Linac DWI to a structured, literature-grounded clinical interpretation, and to assess its retrieval-augmented generation (RAG) interpretation module by independent expert rating.
  Methods: The platform couples a deep-learning processing pipeline, comprising distortion correction, denoising, and intravoxel incoherent motion (IVIM)/apparent diffusion coefficient (ADC) fitting, with longitudinal region-of-interest analysis and a RAG interpretation agent. The agent reasons over a two-layer knowledge base of curated publications (a structured catalog index plus line-indexed full text), delegates arithmetic to deterministic tools, and is designed to trace each statement to a source document, section, and line range. One medical physicist and one physician independently rated the agent's reports for nine longitudinal glioblastoma cases on a 1-5 scale across three metrics: clinical-reasoning soundness, literature-citation quality, and overall clinical utility.
  Results: Across 54 ratings, the pooled mean was 4.65 +/- 0.80, with 93% of ratings >= 4; metric means were 4.6 (reasoning), 4.5 (citation), and 4.8 (utility), and raters agreed within one point on 85% of paired ratings.
  Conclusions: A single platform can integrate MR-Linac DWI post-processing with traceable, expert-evaluated clinical interpretation, while highlighting the safeguards needed to verify LLM-generated reasoning in radiation oncology.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

磁共振引导放疗（MR-Linac）能在每次治疗时采集弥散加权成像（DWI），为肿瘤反应监测提供了前所未有的纵向采样密度。然而，其临床转化面临两大障碍：一是技术层面，MR-Linac DWI信噪比低且存在几何畸变，导致IVIM参数（尤其灌注相关参数）拟合不稳定；二是解释层面，即使获得可靠参数，将Dp、Dt、fp轨迹转化为临床判断需综合大量分散且常相互矛盾的文献，且多参数可能朝相反方向变化，缺乏统一框架解决这种不一致性。现有软件仅覆盖部分流程，缺乏从原始DWI到可审计临床解释的完整路径。本文旨在开发并评估一个集成化网络平台，将深度学习处理管线（畸变校正、去噪、IVIM/ADC拟合）与基于检索增强生成（RAG）的临床解释智能体相结合，使每条结论都锚定于具体文献来源，从而弥合技术处理与临床决策之间的鸿沟，实现可追溯、可审计的MR-Linac DWI全流程应用。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**技术方法类**：本文建立在作者前期开发的基于隐式神经表示（INR）的低信噪比处理链上，包括地标匹配B样条畸变校正、带限INR去噪及IVIM参数估计，区别于传统诊断DWI处理，专门针对MR-Linac的物理约束。**临床应用类**：已有24项研究（900例患者）的荟萃分析表明DWI可区分胶质母细胞瘤真性进展与假性进展（敏感性0.88、特异性0.85），但ADC单一参数混淆扩散与灌注；IVIM模型在胶质瘤分级和疗效评估中显示价值，但文献中阈值和参数-结局关系因场强、b值方案等因素相互矛盾。**智能解读类**：检索增强生成（RAG）技术已在其他医学领域展现潜力，如DeepRare系统在罕见病诊断中Recall@1达57.18%，推理链有效性获专家95.4%认可。本文的独特贡献在于首次将上述三方面整合为单一可审计平台，从原始DICOM到结构化临床报告全流程贯通，并以RAG代理实现每条陈述可追溯至文献具体行段，填补了MR-Linac DWI从处理到临床决策之间的空白。

### Q3: 论文如何解决这个问题？

该论文通过构建一个集成的Web平台，将MR-Linac DWI的原始数据处理与基于文献的临床解读无缝衔接。平台采用单页应用架构，后端基于Flask和Flask-SocketIO实现实时通信，前端为HTML/JavaScript客户端，所有图像处理均在本地GPU加速硬件上完成，确保数据不出院。

核心处理流程包含三个深度学习模块：首先是基于B样条隐式神经表示（LMBS-INR）的畸变校正，通过跨模态地标匹配与变形场正则化实现DWI与解剖图像的精确配准；其次是带限隐式神经表示（BL-INR）去噪模块，利用自监督学习限制网络频率内容并施加物理约束，将噪声标准差降至原来的40%；最后是IVIM-INR参数拟合模块，采用SIREN周期激活网络将参数图建模为空间连续函数，显著提升纵向可重复性（如fp的ICC从0.29提升至0.56）。

平台的创新核心是检索增强生成（RAG）解读智能体，其设计包含三个关键机制：一是两层知识库结构，第一层为结构化目录（含元数据、肿瘤类型、参数范围及章节级内容锚点），第二层为行索引全文，支持逐字检索；二是两阶段检索策略，先通过目录筛选匹配出版物，再仅获取锚定段落，避免无关信息干扰；三是工具辅助计算与可追溯引用，所有数值计算委托给确定性Python工具，每个陈述均关联到源文档、章节和行号范围，确保可审计性。该智能体在9例胶质母细胞瘤的纵向评估中获得4.65/5的平均评分，93%评分≥4，验证了其临床实用性与文献引用质量。

### Q4: 论文做了哪些实验？

论文构建并评估了一个面向MR引导放疗的集成化DWI处理与解读平台，实验聚焦于平台端到端处理能力及RAG解读模块的临床质量。实验设置上，平台在本地环境完成从原始DICOM到纵向IVIM/ADC参数图及临床报告的自动处理，无需人工脚本。数据集为9例纵向胶质母细胞瘤（GBM）病例，每例包含多次MR-Linac采集的DWI数据。对比方法为两名专家（一名医学物理师、一名医师）独立对平台生成的报告进行1-5分制评分，评估三个维度：临床推理合理性、文献引用质量、整体临床实用性。主要结果：共54项评分（9例×3指标×2评分者），合并均值为4.65±0.80，93%评分≥4分。各维度合并均值为：临床推理4.61±0.92，文献引用4.50±0.99，临床实用性4.83±0.38。物理师评分整体高于医师（4.78 vs 4.52），且物理师在推理维度给出全5分，而医师在少数非典型病例中给出较低评分（推理最低2分，引用最低1分）。两名评分者在85%的配对评分中差异不超过1分。代表性案例中，平台正确识别了ADC和Dt的早期升高与晚期下降趋势，并区分了治疗反应与可能的肿瘤复发模式，该案例获得双评分的满分评价。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下方向展开：首先，当前评估仅基于9例胶质母细胞瘤和两位专家，缺乏多中心、大样本及跨病种验证，未来需纳入头颈、前列腺等已建语料库的癌种，并对比不同LLM配置和提示策略的稳健性。其次，研究未验证IVIM参数区分真性进展与假性进展的临床效能，建议结合病理或≥6个月影像随访作为金标准，开展前瞻性队列研究，并与ADC-only基线进行头对头比较。第三，RAG检索的“证据匹配”仍存在病例不匹配问题，可引入结构化病例表型编码（如分子分型、治疗线数）实现更精细的检索过滤，并开发自动化的引用完整性校验器。第四，当前报告对非典型病例的置信度校准不足，可设计基于不确定性估计的动态置信度输出机制。最后，平台虽为器官无关架构，但跨癌种泛化需验证知识库扩展后的检索精度和推理一致性，并探索多模态融合（如结合T2-FLAIR影像特征）以增强解释的临床可操作性。

### Q6: 总结一下论文的主要内容

该论文介绍了一个集成式网络平台，用于处理MR-Linac采集的弥散加权成像（DWI）数据并生成基于文献的临床解读。平台结合了深度学习处理流程（包括畸变校正、去噪和IVIM/ADC拟合）与纵向感兴趣区分析，并配备检索增强生成（RAG）解读智能体。该智能体基于双层知识库推理，将算术任务委托给确定性工具，并确保每项陈述可追溯至源文献的章节和行号。在九例纵向胶质母细胞瘤病例的独立评估中，医学物理师和医师对报告进行1-5分评分，综合均分为4.65±0.80，93%评分≥4分，其中临床实用性得分最高（4.8）。该平台证明了将定量处理与可审计的文献解读整合于单一系统的可行性，同时揭示了验证LLM推理在放射肿瘤学中应用所需的保障措施，为多参数IVIM在治疗反应监测中的推广奠定了基础。
