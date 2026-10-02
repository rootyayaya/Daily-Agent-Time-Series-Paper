---
title: "Generalist Representation, Specialist Detection: TS-Router for Time-Series Anomaly Detection"
authors:
  - "Tian Lan"
  - "Yifei Gao"
  - "Yimeng Lu"
  - "Xuming An"
  - "Meng Wang"
  - "Yue Pan"
  - "Wenjun He"
  - "Chenghao Liu"
  - "Chen Zhang"
date: "2026-10-01"
arxiv_id: "2610.00978"
arxiv_url: "https://arxiv.org/abs/2610.00978"
pdf_url: "https://arxiv.org/pdf/2610.00978v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Time Series Anomaly Detection"
  - "Time-Series Foundation Model"
  - "Router"
  - "Specialist Selection"
  - "Representation Learning"
  - "Unsupervised Detection"
  - "Model Selection"
  - "Industrial Sensor"
relevance_score: 6.5
---

# Generalist Representation, Specialist Detection: TS-Router for Time-Series Anomaly Detection

## 原始摘要

Time-series anomaly detection (TSAD) is difficult to generalize across datasets because heterogeneous temporal dynamics imply different notions of normality and favor different detection criteria. While time-series foundation models provide transferable representations, coupling them with a fixed anomaly-scoring mechanism can overlook this variation. This motivates a different perspective on foundation-model-based TSAD: using foundation models to coordinate specialized anomaly criteria rather than directly imposing a universal one. Based on this view, we propose \textbf{TS-Router}, a generalist-representation, specialist-detection framework that estimates the relative competence of heterogeneous anomaly detectors from pretrained temporal representations and selects suitable specialists for each target series. To avoid relying on specialist-performance labels from real tasks, we derive soft competence supervision from specialists' relative performance on labeled simulated tasks. At deployment, routing requires no target anomaly labels, and only the selected specialists are fitted unsupervisedly on the target series. We bound Top-\(k\) set-competence regret under representation coverage and conditional competence stability. Across 16 real-world benchmarks and four complementary evaluation metrics, TS-Router achieves the best overall average rank. Controlled ablations with multiple frozen TSFM encoders further support the use of pretrained representations for competence estimation and adaptive specialist selection. The code is available at https://anonymous.4open.science/r/TS-Router-D8FF.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决时间序列异常检测（TSAD）中跨数据集泛化困难的核心问题。研究背景在于：不同时间序列的异质动态特性意味着“正常”的定义和适用的异常判据各不相同，传统方法遵循“一数据集一模型”范式，需要针对每个目标序列单独选择、调参和拟合检测器，而检测器的适用性高度依赖目标序列，自动化选择方法又依赖手工特征或有限的历史性能记录，难以在未见序列上推断适用性。时间序列基础模型虽提供了可迁移的表示，但现有基于TSFM的方法通常将可迁移表示与固定的异常评分机制（如预测或重建误差）绑定，近期系统评估表明这种直接适配未必优于简单的局部统计基线。这说明解决表示问题并不等于解决异常决策问题。因此，本文的核心问题是：基础模型在TSAD中除直接定义异常判据外还能扮演什么角色？论文提出“通才表示、专家检测”的视角，将可迁移的时间表示与依赖目标的异常决策分离，让基础模型充当异质异常判据的协调者，通过能力路由为每个目标序列自适应地选择并组合合适的专家检测器，且部署时无需目标异常标签。

### Q2: 有哪些相关研究？

现有相关研究大致可分为三类。方法类方面，USAD、OmniAnomaly、TranAD、TFMAE等基于重构的深度方法，以及统计、距离、密度、子空间、孤立森林和单类分类等经典检测器，均针对单一目标序列拟合，依赖不同归纳偏置来定义正常性与异常分数，但跨异构序列部署时仍需逐目标选择与适配。基础模型类方面，MOMENT、UniTS等通用时序基础模型提供可迁移表示，TimesFM、Chronos、Time-MoE侧重预测迁移，DADA、TSPulse将预训练模型适配到异常检测，TimeRCD则用带标签合成数据预训练异常专用基础模型；然而这些工作通常将可迁移表示与统一的检测器或固定异常评分机制绑定，未针对不同目标自适应选择异常判据。评测与选择类方面，MetaOD通过元学习和手工描述符迁移历史检测器性能，Unsupervised Model Selection与Choose Wisely利用代理准则或序列特征评估候选检测器，AutoTSAD进一步自动化检测器配置、选择与集成，伪异常与异常注入方法则用合成样本直接训练检测器。与上述工作不同，TS-Router不直接施加统一异常判据，而是利用预训练时序表示估计异构检测器的相对胜任度，并从模拟任务中导出软胜任度监督，在部署时无需目标异常标签即可为每条序列选择合适专家，从而实现可扩展的跨序列泛化。

### Q3: 论文如何解决这个问题？

TS-Router 的核心思路是将“通用表示”与“专家检测”解耦：不再用固定评分机制直接判定异常，而是用预训练时序基础模型（TSFM）的表示来动态协调一组异构专家检测器。

整体框架分两阶段训练与一次部署路由。第一阶段，TSFM 按其原生目标预训练，获得可迁移的时序表示；第二阶段冻结编码器，仅训练一个轻量 MLP 路由器。由于真实 TSAD 标签稀缺，作者借鉴 RCD 的标注模拟设定，构造覆盖多样时序结构与异常机制的模拟任务集，每个任务作为“能力探针”。对固定专家池中每个轻量检测器，在无标签拟合协议下生成异常分数，再用模拟标签以 VUS-PR 评估其能力，得到能力向量。该向量不压缩为单一最优专家标签，而是通过带温度 τ 的 Softmax 转为软能力目标，保留专家间的排序与成对能力差距。路由器以 KL 散度拟合该软目标，从冻结表示的均值池化向量预测完整能力分布。

部署时，路由器对完整无标签观测序列前向推理，取 Top-k 专家；仅这些被选专家在目标序列前缀上无监督拟合，在评估后缀上打分，经标准化、平均与 min-max 重缩放融合为最终异常分数。多变量情形逐变量独立执行后聚合。

创新点在于：用基础模型表示估计专家相对胜任度而非直接打分；用模拟任务导出软能力监督，避免依赖真实任务性能标签；理论上在表示覆盖与条件能力稳定假设下给出 Top-k 集合胜任度遗憾界，将表示信息、软目标预测与能力迁移分离，并证明路由相对固定专家的增益下界。

### Q4: 论文做了哪些实验？

论文在16个真实世界TSAD基准上评估TS-Router，包括11个单变量数据集（IOPS、MGAB、NAB、NEK、Power、SED、Stock、TODS、UCR、WSD、YAHOO）和5个多变量数据集（MSL、PSM、SMAP、SMD、SWaT），采用VUS-PR、Affiliation-F1、F1_T和Standard-F1四个互补指标。对比方法涵盖直接零样本模型（TimeRCD、DADA、Chronos、MOMENT、TimesFM、Time-MoE）和目标拟合无监督方法（OmniAnomaly、USAD、TranAD、TFMAE、DCdetector）。主要结果：TS-Router在四个指标上均取得最高平均分和最佳平均排名（Overall Rank 2.66），在64个数据集-指标组合中26次排名第一、39次进入前二；VUS-PR得分49.59，显著高于次优TimeRCD的37.00。在11个单变量基准上进行了路由有效性和表示消融实验，对比Best Fixed、Best Top-3、Oracle及全池集成，并使用NDCG@k和Hit@k评估路由质量；表示消融将默认TimeRCD编码器替换为传统特征及冻结的Chronos、MOMENT编码器。附录还包含预算、池大小、路由头敏感性及合成到真实和留一数据集迁移测试。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有四点。其一，路由监督完全依赖合成任务分布，模拟器虽覆盖多样时序结构与异常机制，但与真实任务的分布偏移仅靠有界密度比假设约束，未来可研究更贴近真实数据的仿真策略，或引入少量真实无标签任务进行自监督校准。其二，专家池固定且刻意轻量，路由只反映归纳偏置差异；若引入更强或可微专家，需重新界定“能力”与“容量”的分离，并探索端到端联合优化。其三，表示由冻结TSFM均值池化得到，序列级单一向量可能丢失局部异常定位信息，可尝试多尺度或token级路由。其四，当前按变量独立路由再聚合，跨变量异常模式未被利用，未来可设计多变量联合路由与专家组合，并研究Top-k中k的自适应选择。

### Q6: 总结一下论文的主要内容

论文针对时间序列异常检测（TSAD）难以跨数据集泛化的问题，指出异构时间动态意味着不同的“正常”定义和检测准则，而现有时间序列基础模型（TSFM）通常将可迁移表示与固定异常评分机制耦合，忽视了这种差异。为此，作者提出TS-Router，一种“通才表示、专家检测”框架：利用预训练时间表示估计多个异构异常检测器的相对能力，并为每个目标序列自适应选择合适专家。为避免依赖真实任务的专家性能标签，方法从专家在带标签模拟任务上的相对表现中导出软能力监督；部署时路由无需目标异常标签，仅对选中的专家在目标序列上无监督拟合。理论上，作者在表示覆盖与条件能力稳定性假设下给出了Top-k集合能力遗憾界。在16个真实基准和四种互补指标上，TS-Router取得最佳平均排名，消融实验进一步验证了预训练表示用于能力估计和自适应专家选择的有效性。
