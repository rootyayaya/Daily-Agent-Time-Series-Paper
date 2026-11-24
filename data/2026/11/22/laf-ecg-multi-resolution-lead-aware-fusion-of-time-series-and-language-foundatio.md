---
title: "LAF-ECG: Multi-Resolution Lead-Aware Fusion of Time-Series and Language Foundation Models for ECG Classification"
authors:
  - "Kiana Taktehrani"
  - "Maryam Hosseini"
  - "Amir Keynia"
  - "Aram Montazami"
  - "Arash Mohammadi"
date: "2026-11-22"
arxiv_id: "2611.29721"
arxiv_url: "https://arxiv.org/abs/2611.29721"
pdf_url: "https://arxiv.org/pdf/2611.29721v1"
github_url: "https://github.com/kkianamm/LAF-ECG"
categories:
  - "cs.LG"
tags:
  - "时间序列基础模型"
  - "语言基础模型融合"
  - "ECG分类"
  - "多分辨率时序"
  - "导联感知"
  - "双基础模型"
  - "时序-语言对齐"
  - "医疗时间序列"
relevance_score: 6.5
---

# LAF-ECG: Multi-Resolution Lead-Aware Fusion of Time-Series and Language Foundation Models for ECG Classification

## 原始摘要

Automated electrocardiogram (ECG) interpretation has advanced substantially with deep learning, yet many methods remain task-specific and label-dependent. Large language models (LLMs) and time-series foundation models (TSFMs) offer complementary pretrained representations, but integrating them is challenging because of mismatched feature spaces and the lead- and scale-dependent structure of ECG signals. We propose LAF-ECG (Lead-Aware Foundation Fusion for ECG), a dual-foundation framework that extends MedTsLLM with a lead-aware interface to a frozen TSFM backbone while retaining its reprogramming pathway. The proposed framework captures multi-resolution temporal context, fuses temporal and language-aligned ECG representations through adaptive residual integration, and employs branch-specific supervision with cross-branch alignment. LAF-ECG achieves 71.10% accuracy and 62.43% macro-F1 on PTB-XL, and 89.73% accuracy and 65.94% macro-F1 on Chapman-Shaoxing, outperforming MedTsLLM on both datasets. These results highlight the value of preserving lead-specific temporal structure when combining temporal and language foundation representations for ECG classification. The code is publicly available at https://github.com/kkianamm/LAF-ECG.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决心电图（ECG）自动分类中基础模型融合的关键难题。研究背景方面，ECG诊断信息分布在多个导联和时间模式中，深度学习虽已取得较好分类性能，但多数方法仍是任务特定且依赖标注，学到的表示难以迁移；与此同时，大语言模型（LLM）和时间序列基础模型（TSFM）分别提供了语言对齐与纯时序的预训练表示，二者具有互补潜力。现有方法的不足在于：MedTsLLM等基于LLM重编程的方法虽将数值时序映射到语言模型空间，却未充分利用TSFM的时序表示；而Time2Lang等尝试结合TSFM与LLM的工作，面临特征空间不匹配的问题，且未能保留ECG固有的导联相关性和多尺度结构，导致融合效果受限。本文的核心问题是：如何在冻结的时序与语言基础模型骨干下，有效整合两类互补表示，同时保留导联特异的时序结构和多分辨率信息。为此作者提出LAF-ECG双基础模型框架，通过导联感知时序基础模块建模导联间重要性、多分辨率时序上下文捕获全局信息、自适应残差融合整合两路表示，并配合分支特定监督与跨分支对齐，最终在PTB-XL和Chapman-Shaoxing上均优于MedTsLLM。

### Q2: 有哪些相关研究？

相关研究可按以下三类组织。

**语言模型重编程类**：Time-LLM 最早提出将数值时间序列重编程到预训练语言模型空间的范式，实现跨模态对齐；MedTsLLM 将其扩展到生理信号，是本文的直接基础。LAF-ECG 保留了 MedTsLLM 的重编程通路，但额外引入时间序列基础模型分支，弥补其缺乏原生时序表征的不足。

**时间序列基础模型类**：MOMENT 等 TSFM 提供强预训练时序表征；Time2Lang 探索了 TSFM 与 LLM 结合用于健康感知。与 Time2Lang 不同，本文针对 ECG 的导联与尺度依赖结构，设计了导联感知接口与多分辨率上下文模块，并以冻结骨干方式融合两类基础模型。

**ECG 专用预训练与深度分类类**：ECG-FM 通过大规模 ECG 预训练获得可复用生理表征；传统深度学习 ECG 分类方法虽性能较强，但多为任务特定、依赖标注，迁移性受限。本文以双基础模型融合提升跨数据集泛化，并在 PTB-XL 与 Chapman-Shaoxing 上验证优于 MedTsLLM。

### Q3: 论文如何解决这个问题？

LAF-ECG 采用双基础模型融合框架，在冻结的时序基础模型 MOMENT 与冻结的语言模型 Llama-2-7B 之间建立“导联感知”接口，同时保留 MedTsLLM 的重编程通路，从而解决特征空间不匹配与 ECG 导联/尺度依赖结构难以融合的问题。

整体架构包含两条互补通路。第一条是 MedTsLLM 重编程分支：将重采样到 512 点的对齐信号经 RevIN 归一化、8 点分块并按导联嵌入，再通过可学习投影把冻结词表嵌入映射为源原型，用交叉注意力完成重编程，得到语言对齐的 ECG token。第二条是基于冻结 MOMENT 的导联感知时序分支（LTFM）：MOMENT 输出未归约的逐导联 token，模型为每个导联加入可学习嵌入，并用导联注意力为同一时间位置的各导联 token 计算权重并加权求和，显式保留导联特异性结构。

在此基础上，多分辨率时序上下文（MRTC）模块用两个重叠的原始分辨率窗口（1–512 与 489–1000）分别经同一冻结 MOMENT 与共享 LTFM 处理，再经 patch 级与窗口级注意力池化得到全局时序上下文，并通过门控机制注入对齐后的时序 token，弥补重采样造成的高频细节损失。

自适应残差 token 融合（ARTF）模块先将 MedTsLLM token 数对齐到 MOMENT token 数，再把时序表示经两层 GELU MLP 投影到 LLM 空间，用特征级门控做残差融合，且以 MedTsLLM 表示为残差锚点，避免时序分支破坏语言对齐表示。融合后的序列与编码数据集、患者和任务信息的提示嵌入拼接，送入冻结 Llama-2-7B，仅对 ECG 位置隐状态做注意力池化后分类。

训练上引入分支特定辅助监督（BAS），对融合前的两条分支分别池化和分类并取平均交叉熵；同时采用监督跨分支对齐（SCA），以同类样本为正样本对做对称对比损失，拉近两个特征空间。总损失为分类损失、辅助损失与对齐损失的加权和。创新点在于导联注意力聚合、多分辨率上下文门控注入、残差式自适应融合以及跨分支对齐监督。

### Q4: 论文做了哪些实验？

论文在PTB-XL和Chapman-Shaoxing两个数据集上评估LAF-ECG。PTB-XL使用100Hz十二导联记录，按标准患者划分（1–8训练、9验证、10测试），将诊断SCP码映射为NORM、MI、STTC、CD、HYP五个超类；Chapman-Shaoxing降采样至100Hz，构建八类单节律子集（SB、SR、AFIB、ST、AF、SA、SVT、AT），共43,021条记录，按70/10/20分层划分（30,114/4,302/8,605），类别数从141（AT）到15,824（SB），存在明显不平衡。模型冻结MOMENT-1-base与Llama-2-7B，仅训练适配层等模块，共约6.77B参数，可训练参数52.3M（0.77%）。训练20轮，AdamW（学习率3e-4、权重衰减0.01），类别加权交叉熵加0.05标签平滑，批大小4配合四步梯度累积（有效批16），并使用导联幅值缩放、导联丢弃与时间掩码增强。对比方法包括GPT4TS、PatchTST、OpenTSLM、MedTsLLM和GEM，评价指标为准确率、macro-F1、精确率和召回率。结果显示LAF-ECG在PTB-XL上达71.10%准确率和62.43% macro-F1，在Chapman-Shaoxing上达89.73%准确率和65.94% macro-F1，均优于MedTsLLM等基线；三个随机种子的PTB-XL均值为70.74±0.33%准确率和61.93±0.43% macro-F1。消融实验表明移除高分辨率上下文导致macro-F1下降4.07点，平均导联池化下降3.10点，去除跨分支对齐下降2.51点。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有以下几点。其一，实验仅在PTB-XL和Chapman-Shaoxing两个数据集上验证，且Chapman上macro-F1仅65.94%，说明类别不平衡与细粒度诊断（如多标签共病）仍是短板，未来可扩展到更多导联配置、更多中心数据及多标签场景。其二，TSFM主干保持冻结、仅训练轻量接口，虽高效但可能限制对ECG域特征的深度适配，可探索部分解冻、LoRA等参数高效微调与接口学习的联合优化。其三，多分辨率与导联感知融合目前较粗粒度，可引入可学习的导联注意力或跨导联图结构，并显式建模导联间拓扑关系。其四，缺乏可解释性分析，未来可结合注意力可视化或概念瓶颈，验证语言分支是否真正提供临床语义对齐。其五，可探索跨模态对齐的对比预训练目标，以及将框架推广到其他生理信号（EEG、PPG）与生成式报告任务。

### Q6: 总结一下论文的主要内容

论文针对现有ECG分类方法任务特定、依赖标注且难以融合异构基础模型表征的问题，提出LAF-ECG双基础模型框架。其核心是在MedTsLLM重编程通路基础上，引入冻结的MOMENT-1-base时序主干，并设计四个组件：导联感知时序基础模块（LTFM）建模token级导联间重要性；多分辨率时序上下文（MRTC）利用重叠窗口捕获全局信息；自适应残差token融合（ARTF）以门控方式整合时序与语言对齐表征；分支特定辅助监督（BAS）与监督式跨分支对齐（SCA）增强特征判别性与类一致性。在PTB-XL和Chapman-Shaoxing上，模型分别取得71.10%/62.43%和89.73%/65.94%的准确率/macro-F1，均优于MedTsLLM等基线；消融实验表明高分辨率上下文贡献最大。该工作证明了在融合时序与语言基础模型时保留导联特异时序结构的重要价值。
