---
title: "Do Time-Series Foundation Models Pay Off for Industrial Monitoring? A Cost-Aware Empirical Study"
authors:
  - "Guan-Hua Wen"
  - "Kuan-Yu Chen"
date: "2026-08-24"
arxiv_id: "2608.22968"
arxiv_url: "https://arxiv.org/abs/2608.22968"
pdf_url: "https://arxiv.org/pdf/2608.22968v1"
categories:
  - "cs.LG"
tags:
  - "Time-Series Foundation Models"
  - "Industrial Monitoring"
  - "Anomaly Detection"
  - "Empirical Study"
  - "Cost-Aware Evaluation"
  - "C-MAPSS"
  - "MIMII"
  - "BDG2"
  - "Zero-Shot Forecasting"
  - "Lightweight Baselines"
relevance_score: 7.5
---

# Do Time-Series Foundation Models Pay Off for Industrial Monitoring? A Cost-Aware Empirical Study

## 原始摘要

Industrial monitoring models must detect operationally relevant deviations while satisfying target-specific data, calibration, and resource constraints. Time-series foundation models (TSFMs) promise reusable representations and zero-shot forecasts, yet evidence for their deployment value remains mixed when task definitions are heterogeneous and lightweight baselines are competitive. This work presents a protocol-aware empirical assessment across three settings: a C-MAPSS degradation-risk proxy, normal-only training for anomalous-sound detection on MIMII, and BDG2 forecasting-residual diagnostics with synthetic target perturbations. We assess classical one-class methods, compact neural autoencoders, residual forecasters, MOMENT-small, Chronos-T5, and TimesFM 2.5 in terms of anomaly-ranking performance, risk-horizon sensitivity, residual forecasting and perturbation sensitivity, and local implementation cost. Across 100 C-MAPSS engines evaluated out of fold, TCN-AE reaches fold-weighted AUROC/AUPRC 0.9570/0.8960, compared with 0.7310/0.3080 for MOMENT reconstruction; paired engine-cluster bootstrap confidence intervals exclude zero for both differences. Across five matched MIMII pump evaluations, OCSVM also exceeds MOMENT reconstruction in AUROC and AUPRC. On a fixed 12-meter BDG2 panel, TimesFM 2.5 has the lowest aligned forecast error and the highest synthetic AUROC point estimate, although synthetic AUPRC is similar across TSFM and fitted residual models. Same-device measurements show that MOMENT incurs higher latency, peak allocated VRAM, and serialized state-dictionary size than TCN-AE. Under the evaluated frozen and zero-shot settings, TSFMs are task-dependent deployment options rather than default replacements for fitted lightweight models.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业监控模型需要在满足目标数据、校准和资源约束的前提下，检测与运行相关的偏差。时间序列基础模型（TSFM）宣称具备可复用的表征和零样本预测能力，但其实际部署价值尚不明确，尤其是在任务定义异构且轻量级基线模型表现强劲的场景下。现有研究缺乏在统一协议下、针对不同工业监控任务（如退化风险、异常声音检测、预测残差诊断）的系统性评估，也未充分考虑本地部署的延迟、内存和模型大小等成本因素。因此，本文的核心问题是：在冻结和零样本设置下，TSFM 是否能在异常排序、风险敏感性、预测残差和扰动敏感性上显著优于传统单分类方法、紧凑神经自编码器等轻量级模型，同时权衡其高昂的本地实现成本。研究旨在提供协议感知的经验比较，而非提出新检测器或建立通用排名，以回答TSFM在工业监控中是否值得替代轻量级模型这一关键部署问题。

### Q2: 有哪些相关研究？

相关研究主要分为四类。**方法类**中，时间序列异常检测研究涵盖重建、预测、密度估计、对比学习及图/注意力架构；工业迁移学习强调源-目标域失配需显式处理。**应用类**包括：MIMII数据集支持真实工厂噪声下的机器声音异常检测，DCASE 2020 Task 2 规范了仅用正常声音训练的无监督检测协议；BDG2建筑能耗数据源于ASHRAE预测竞赛，本文因缺乏故障标签而采用注入扰动探测残差敏感性。**模型类**中，MOMENT提供多任务预训练时间序列模型，Chronos将数值量化为token适配语言模型架构，TimesFM采用解码器-only架构实现零样本预测，ChronosAD则专门探索基础模型表示用于异常检测。**评测类**方面，有研究在电力系统预测中评估TSFM的零样本精度、微调效率、视界敏感性等，但本文不同之处在于：聚焦工业监测的冻结/零样本部署模式，强调任务异构性和本地实现成本（延迟、显存、模型大小），并采用匹配协议对比轻量级基线（TCN-AE、OCSVM）与TSFM，揭示TSFM并非默认替代方案，而是任务相关的部署选项。

### Q3: 论文如何解决这个问题？

该论文通过协议感知的实证评估框架，系统比较了时间序列基础模型（TSFMs）与轻量级基线模型在工业监测中的实际部署价值。核心方法是为三个异构工业场景（C-MAPSS退化风险、MIMII异常声音检测、BDG2能耗预测残差诊断）设计统一的监测评分接口，将不同任务映射为标量异常分数，同时保留各领域特定的解释语义。

整体框架包含四个主要模块：**数据协议层**针对每个数据集定制训练/评估流程（如C-MAPSS采用引擎分离五折交叉验证，MIMII使用配对文件清单，BDG2固定12米面板）；**模型集合层**涵盖经典单类方法（Isolation Forest、OCSVM、LOF、PCA重建）、轻量深度模型（TCN-AE、LSTM-AE）、残差预测器（Ridge、LightGBM）及三种TSFM（MOMENT-small、Chronos-T5、TimesFM 2.5）；**评估协议层**统一采用95%训练分数分位数作为阈值，避免测试标签泄漏；**成本审计模块**在同设备上测量延迟、峰值VRAM和序列化状态字典大小。

关键技术包括：C-MAPSS中采用滑窗RUL代理标签（h=30主分析），MIMII使用共享的128×32 log-mel张量缓存，BDG2通过五种注入种子和十种扰动类型生成合成伪标签。创新点在于：1）不跨数据集比较排名，而是按部署场景解释结果；2）采用引擎/文件/仪表作为配对bootstrap重采样单元，确保统计严谨性；3）将计算成本作为一等公民指标纳入评估。最终发现TSFM在冻结零样本设置下是任务依赖的部署选项，而非轻量模型的默认替代品。

### Q4: 论文做了哪些实验？

论文在三个工业监测场景下开展了系统实验。**C-MAPSS**上，以100台发动机的17,731个窗口评估退化风险代理任务，对比TCN-AE、Isolation Forest与MOMENT-small（重建和嵌入两种配置）。TCN-AE取得最优折加权AUROC/AUPRC/F1为0.9570/0.8960/0.7959，Isolation Forest接近（0.9521/0.8866/0.7847），而MOMENT重建仅0.7310/0.3080，配对bootstrap置信区间排除零差异，且该劣势在15-40周期预测范围内稳定存在。**MIMII**上，采用仅正常数据训练检测异常声音，五折匹配协议显示OCSVM的AUROC/AUPRC均值（0.6944/0.7277）显著优于MOMENT重建（0.5501/0.5890），每折置信区间均低于零。**BDG2**上，对12个仪表进行合成扰动诊断，TimesFM 2.5取得最低对齐预测误差（MAE 9.3059, RMSE 15.7695）和最高合成AUROC（0.7239），但AUPRC与LightGBM（0.1639）、Ridge（0.1549）接近，且延迟、尖峰等事件对所有模型均困难。资源审计显示MOMENT延迟（13.37ms vs 0.29ms）、显存（691MB vs 2.6MB）和状态字典（138MB vs 13.8KB）远超TCN-AE。结论：冻结TSFM在零样本下并非轻量拟合模型的默认替代。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从以下维度展开：首先，当前TSFM均采用冻结或零样本模式，未评估微调、适配器或更大规模变体的潜力，未来可系统比较轻量级微调（如LoRA）与全参数微调在工业监测中的成本-性能权衡。其次，C-MAPSS的退化风险代理标签和BDG2的合成扰动本质上是代理指标，需在真实故障数据集上验证结论的稳健性，并探索标签语义与监测目标对齐的协议设计。第三，时序依赖性问题（如C-MAPSS窗口内高相关性和BDG2固定面板）提示需开发更严格的分组验证协议，例如跨设备或跨时间段的泛化测试。此外，当前仅测算了推理阶段成本，未来应纳入预处理、模型加载及端侧部署的完整生命周期开销，并考察CPU/边缘设备上的能效比。最后，可探索混合架构——利用TSFM的零样本先验生成残差或伪标签，再由轻量模型进行在线适配，从而在保持低延迟的同时提升异常排序性能。

### Q6: 总结一下论文的主要内容

本研究针对工业监测场景，系统评估了时间序列基础模型（TSFMs）与传统轻量级模型的部署价值。在C-MAPSS退化风险、MIMII异常声音检测和BDG2预测残差诊断三个任务中，对比了一类方法、紧凑自编码器、残差预测器及MOMENT、Chronos-T5、TimesFM等TSFM。结果显示：在100台C-MAPSS引擎上，TCN-AE的AUROC/AUPRC达0.9570/0.8960，显著优于MOMENT重建的0.7310/0.3080；MIMII任务中OCSVM同样超越MOMENT。TimesFM在BDG2预测误差和合成AUROC上最优，但AUPRC无显著优势。此外，MOMENT的延迟、显存占用和模型体积均高于TCN-AE。核心结论是：在冻结和零样本设置下，TSFM是任务相关的部署选项，而非轻量级拟合模型的默认替代品。研究强调，实际部署需保留目标正常基线，并报告校准边界，合成诊断不能替代真实事件标签的验证。
