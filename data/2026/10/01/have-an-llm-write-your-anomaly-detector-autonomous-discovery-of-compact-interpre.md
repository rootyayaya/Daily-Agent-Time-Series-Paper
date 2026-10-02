---
title: "Have an LLM Write Your Anomaly Detector: Autonomous Discovery of Compact, Interpretable Detectors for Time Series"
authors:
  - "David Berghaus"
date: "2026-10-01"
arxiv_id: "2610.01223"
arxiv_url: "https://arxiv.org/abs/2610.01223"
pdf_url: "https://arxiv.org/pdf/2610.01223v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "LLM-driven program search"
  - "autonomous research loop"
  - "time series anomaly detection"
  - "interpretable detector"
  - "compact detector"
  - "TSB-AD benchmark"
  - "univariate anomaly detection"
  - "multivariate anomaly detection"
  - "spectral features"
  - "covariance-aware distance"
  - "no GPU training"
  - "efficient inference"
  - "transparent model"
  - "LLM as author"
  - "program synthesis"
relevance_score: 8.5
---

# Have an LLM Write Your Anomaly Detector: Autonomous Discovery of Compact, Interpretable Detectors for Time Series

## 原始摘要

Time-series anomaly detection trades off predictive accuracy, computational efficiency, and interpretability. We use a large language model not as the detector but as the author of one: an autonomous research loop in which the model repeatedly edits a single short NumPy program under a leakage-free objective, keeping the best-scoring detector it finds. The loop discovers two compact detectors, one for univariate and one for multivariate series, that describe short windows by their local spectral features and compare them with the training-region distribution through a covariance-aware distance. On the TSB-AD benchmark these detectors lead the field across metrics, ahead of the strongest classical, deep, and foundation-model baselines including Time-RCD, yet they train no network and use no GPU, and the multivariate detector is faster than every similarly performing baseline. LLM-driven program search is thus a practical route to accurate, efficient, and transparent detectors.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列异常检测长期面临预测精度、计算效率与可解释性之间的权衡，至今没有一种方法能在各类数据集、异常类型和算力预算下全面占优。经典方法（如KMeans、KNN）成本低、易理解，但往往需要针对数据集做预处理和阈值调参；深度模型与基础模型虽减少了人工调参，却带来训练开销、GPU依赖和黑箱不可解释的问题。本文的核心问题不是手工设计或训练一个检测器，而是探索：能否用大语言模型作为“作者”而非“检测器”，通过自主研究循环自动发现一个既准确又高效、可解释的异常检测器。具体而言，作者让LLM在无泄漏的评估协议下反复编辑一段简短的NumPy程序，以注入合成异常的训练切片作为验证信号，逐步搜索出单变量和多变量两个紧凑检测器。其目标是验证这种LLM驱动的程序搜索能否在TSB-AD基准上超越经典、深度及基础模型基线，同时保持无GPU、无网络训练、单CPU可读可审计的特性。

### Q2: 有哪些相关研究？

相关研究主要分为三类。第一类是时间序列异常检测的基准与模型。评测方面，本文以TSB-AD为主基准，采用Time-RCD发布的16族协议，并在附录中补充TAB基准。对比方法涵盖预训练、深度和经典三类：预训练基础模型Time-RCD；深度重构与预测模型TranAD、USAD、OmniAnomaly、DCdetector及TFMAE；经典方法LOF、Isolation Forest和子序列PCA。与这些依赖网络训练或GPU的方法不同，本文的检测器仅由几行NumPy构成，无需训练网络，却在TSB-AD上领先，且多变量检测器比同性能基线更快。

第二类是自主研究智能体与LLM驱动的程序发现。FunSearch证明LLM提出的程序搜索可在数学中取得新结果；AlphaEvolve将其扩展为通用编码智能体；ShinkaEvolve研究如何提高此类搜索的样本效率；已有工作提出CLI中的自主研究循环，让LLM反复编辑单一产物并按固定指标迭代；EVIL最接近本文应用，为事件序列和时间序列演化紧凑可解释的零样本算法。本文沿用这一“LLM作为作者”的范式，但聚焦于时间序列异常检测，并发现基于局部谱特征与协方差感知距离的紧凑检测器。

第三类是用于基础模型的合成数据。合成模拟被广泛用于预训练时间序列与事件序列基础模型，如Time-RCD使用合成异常与相对上下文，CauKer使用因果一致的核生成序列，SymTime将合成序列与符号表达式配对。与这些工作不同，本文的LLM在推理时不接触数据，只负责编写检测器程序，评分对象是极简NumPy代码。

### Q3: 论文如何解决这个问题？

论文的核心思路是把大语言模型从“检测器”转变为“检测器的作者”，通过一个自主研究循环让 LLM 反复编辑一段简短的 NumPy 程序，从而自动发现紧凑、可解释的时序异常检测器。整体框架由三部分组成：固定的评测 harness、候选检测器程序、以及 LLM 驱动的迭代循环。harness 定义数据接口、验证目标与评分代码，LLM 只能修改检测器程序本身。每轮迭代中，模型先查看当前程序与近期得分，再提出具体修改（从超参数调整到新增评分组件甚至结构重写），随后在验证集上运行并读取分数。与爬山搜索不同，该循环不自动接受或拒绝修改，所有尝试轨迹（包括得分下降的编辑）都保留在上下文中作为后续灵感，最终返回整个会话中得分最高的程序。为避免过拟合，搜索不使用真实异常标签，而是仅在训练区间的留出切片上注入合成异常，异常类型取自 GutenTAG 分类体系，覆盖幅度类与范围内形状/上下文类，单变量侧重范围内家族，多变量还加入跨通道联合扰动，从而防止候选检测器只擅长某一类异常。搜索被引导向短小、单一原理的程序，以保持可读性。最强循环由 Opus 4.8 驱动，在单变量和多变量两种设定下独立运行，均发现基于“局部频谱特征 + 协方差感知高斯新颖度”的检测器：滑动短窗口，用 Hann 窗去均值后计算功率谱，单变量提取熵、峰值集中度、质心、对数能量、谱平坦度、低/高频带比、谱斜率与复杂度坍缩项等八维签名并拼接 11 个对数频带功率，构成 19 维描述子，再用收缩全协方差 Mahalanobis 距离对正常窗口高斯建模，并在二进尺度空间上做尾部加权融合；多变量则对每通道分频带能量联合建模，用单一高斯模型捕捉跨通道关系破裂。创新点在于：LLM 作为程序搜索器而非检测器、无泄漏合成验证目标、以及发现无需训练网络、无需 GPU、运行时间随序列长度近似线性且高度可解释的检测器。

### Q4: 论文做了哪些实验？

论文在TSB-AD和TAB两个基准上评估。TSB-AD采用Time-RCD的16家族协议，含11个单变量家族（IOPS、MGAB、NAB、NEK、Power、SED、Stock、TODS、UCR、WSD、Yahoo）和5个多变量家族（MSL、PSM、SMAP、SMD、SWaT），报告affiliation F-measure、F1-T、标准F1和VUS-PR。对比方法包括Time-RCD基础模型、TranAD、USAD、OmniAnomaly、DCdetector、TFMAE等深度模型，以及LOF、Isolation Forest、Sub-PCA等经典基线。TAB则覆盖更大规模数据（单变量14家族816条序列，多变量25家族214条序列），对比HBOS、EIF、KMeans、TimesNet、PatchTST、iTransformer、Anomaly Transformer及Time-RCD、TSPulse、Chronos等。主要结果：Opus 4.8循环发现的检测器在TSB-AD四项指标上均取得最多第一名，标准F1和VUS-PR优势最大，仅多变量侧略逊于GPT 5.6 Terra。在TAB多变量上四项range-aware指标全部第一，单变量上ROC类指标领先。消融实验比较了不同LLM驱动与ShinkaEvolve搜索，并对比FFT、Spectral Residual、C22MP及catch22+Mahalanobis，发现检测器VUS-PR达53.9，远超后者最高35.0，证明其描述子组合具有独特优势。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：其一，搜索过程依赖特定LLM（Opus 4.8）与特定目标函数，未验证跨模型、跨任务的稳定性与可复现性；其二，发现的检测器在TAB的region-based affiliation F-measure上仅居中游，因其输出尖锐新颖性峰值而非宽泛异常区间，说明目标函数与评估指标间存在错配；其三，搜索空间限于短NumPy程序，未触及多变量通道间依赖建模、在线/流式场景与概念漂移适应。

未来可探索：一是将搜索目标从单一标量分数改为多目标（精度、延迟、可解释性、区间覆盖）的帕累托搜索，缓解指标错配；二是引入课程式或分阶段编辑，让LLM先搜索特征描述子再搜索距离度量，提升搜索效率与可解释性；三是把该自主循环扩展到变化点检测、因果异常归因与在线自适应场景，并系统研究不同LLM、提示策略与预算下的发现质量，形成可复用的“LLM即算法设计师”方法论。

### Q6: 总结一下论文的主要内容

本论文提出一种由大语言模型驱动的自主研究循环，让LLM充当“异常检测器作者”而非检测器本身：模型在无泄漏协议下反复编辑一段简短的NumPy程序，依据注入合成异常的训练切片进行评分，保留最优程序。搜索分别为单变量和多变量序列发现两个紧凑检测器，二者均以短窗口的局部谱特征描述序列，并通过协方差感知距离与正常训练窗口分布比较。在TSB-AD基准上，这两个检测器在全部四项指标上取得最多第一名，超越Time-RCD等经典、深度和基础模型基线，且无需训练网络、无需GPU，多变量检测器速度更快。消融实验表明其优势来自LLM组合出的特定谱组织描述子，而非既有框架，证明LLM程序搜索是获得准确、高效、可解释检测器的实用路径。
