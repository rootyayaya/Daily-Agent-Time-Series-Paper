---
title: "Anlu: Enabling In-Context Time Series Anomaly Detection in Foundation Models via Counterfactual Supervision"
authors:
  - "Tian Lan"
  - "Yifei Gao"
  - "Yimeng Lu"
  - "Xuming An"
  - "Meng Wang"
  - "Yue Pan"
  - "Wenjun He"
  - "Chen Zhang"
date: "2026-10-05"
arxiv_id: "2610.06180"
arxiv_url: "https://arxiv.org/abs/2610.06180"
pdf_url: "https://arxiv.org/pdf/2610.06180v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "时间序列异常检测"
  - "上下文学习"
  - "基础模型"
  - "反事实监督"
  - "参考记忆"
  - "门控适配器"
  - "TSB-AD-U"
relevance_score: 7.5
---

# Anlu: Enabling In-Context Time Series Anomaly Detection in Foundation Models via Counterfactual Supervision

## 原始摘要

Whether a time-series pattern is anomalous often depends on the operating regime of the monitored process. A missing event can signal a fault in one regime and be routine in another, and the query alone may not reveal which regime applies. We study in-context learning (ICL) for time series anomaly detection (TSAD) through reference-conditioned detection, where a reference record provides evidence about expected behavior and model parameters remain fixed at inference. Supplying the reference is not enough: when training anomalies are recognizable from the query alone, the detector can fit its targets while ignoring the reference. We therefore introduce counterfactual supervision, which pairs one query with two references that support different normal rules and labels the query under each. At positions where the two labels disagree, no detector that ignores the reference can fit both targets. Anlu learns from this supervision by adding a reference memory and zero-initialized gated adapters to a frozen time-series foundation model (TSFM) pretrained for anomaly detection. On the 350 TSB-AD-U evaluation sequences, Anlu raises the mean VUS-PR of the frozen TSFM from 0.542 to 0.607. Replacing the reference with zeros lowers Anlu's score to 0.499.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业监控中，传感器流是否异常取决于被监控过程所处的运行工况：同一模式在一种工况下是故障，在另一种工况下可能是常规行为，而仅凭查询序列本身往往无法判断适用哪种规则。现有方法存在两类局限：基于预训练时间序列基础模型的零样本检测器只能依据查询自身数值和上下文打分，无法被告知当前适用何种工况；半监督检测器则需针对目标序列的正常数据重新训练参数，每遇到新工况就要再训练一轮。虽然正常运行的记录容易采集，但代表性故障样本稀少，因此本文研究“参考条件化检测”：将一段独立的正常记录作为输入，在推理时指定工况，从而在未观测到任何故障前就能演示正常行为。然而，仅提供参考并不保证检测器真正使用它——当合成异常仅凭查询即可识别时，训练会忽略参考而仍达到低损失。为此，本文提出反事实监督：将同一查询与两条支持不同正常规则的参考配对，并分别标注，使得在标签不一致的位置上，任何忽略参考的检测器都无法同时拟合两个目标，从而被迫读取参考信息。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，TimesFM、Chronos、Moirai、Toto 等时序基础模型（TSFM）面向零样本预测，MOMENT 统一支持预测、分类、插补与异常检测；DADA 与 TimeRCD 属于零样本异常检测器，仅从查询窗口自身推断正常行为，不接受独立的正常记录。应用类方面，InCTRL 以少量正常样本提示对图像打分，LLMAD 检索相似正常/异常片段作为大语言模型演示，iAmTime 在含异常掩码的演示片段上训练 TSFM 并逐片段选择异常类型。评测类方面，本文使用 TSB-AD-U 的 350 条序列评估，并报告 VUS-PR 指标。

与上述工作的关系与区别在于：TSFM 的上下文微调虽引入相关序列示例，但预测目标仍是目标序列的未来，示例只提升预测质量而不改变预测对象；InCTRL 与 LLMAD 中查询标签由其自身内容决定，上下文有帮助但非必需；iAmTime 变化的是哪些异常类型算异常。Anlu 则保持查询不变，让参考记录决定正常规则，并通过反事实监督在两条参考支持不同规则处赋予不同标签，使忽略参考的检测器无法同时拟合两个目标，从而真正实现参考条件化的上下文异常检测。

### Q3: 论文如何解决这个问题？

论文的核心思路是把时间序列异常检测从“仅凭查询序列判断”转化为“参考条件下的上下文判断”，并通过反事实监督强制模型真正利用参考信息。整体框架基于一个冻结的时间序列基础模型（TSFM），查询编码器与参考编码器共享同一预训练初始化。参考序列先经冻结编码器得到 patch 表示，再由一个可训练的 Perceiver 风格重采样器压缩为每通道 32 个记忆 token，形成参考记忆。

关键技术是零初始化门控适配器：在查询编码器的第 3、5、7、8 层后插入适配器，每个适配器包含归一化交叉注意力与归一化前馈块，二者输出分别乘以初始为零的 tanh 门控后残差回加。因此适配器在初始化时是恒等映射，不破坏预训练特征，只学习如何从参考记忆中读取证据。冻结的投影层与检测头最终输出每个时间点、每个通道的两个 logits，其差经通道平均和 sigmoid 得到异常分数。

创新点在于反事实监督：每个训练单元包含同一查询和两条支持不同正常规则的参考，并分别给出标签。在两条标签不一致的位置上，任何忽略参考的确定性检测器都无法同时拟合两个目标，其交叉熵下界为 log2，从而在理论上排除了“只看查询”的捷径解。训练目标由检测损失与冻结重建头的掩码重建损失组成，仅优化适配器与重采样器参数。该设计使 Anlu 在 TSB-AD-U 上把冻结 TSFM 的平均 VUS-PR 从 0.542 提升到 0.607，而将参考置零后降至 0.499，证明性能确实来自参考条件化。

### Q4: 论文做了哪些实验？

论文在TSB-AD-U评估集的350条序列（来自23个源数据集）上进行实验，指标为VUS-PR（序列级无权重均值）。参考前缀取训练边界b之后的前min(b,10000)个样本，查询用其均值和总体标准差归一化，参考沿用同一统计量；零参考条件将归一化参考值全部置零但保留长度与有效性掩码。长查询按重叠窗口打分并对重叠处异常logit取平均，推理时关闭随机patch掩码。主要结果：Anlu使用原始参考前缀时平均VUS-PR达0.607，较冻结TSFM的0.542提升0.065；将参考置零后降至0.499。相对零参考条件，原始前缀在248条序列上得分更高、82条更低、20条持平。此外，论文在TimeRCD表1的11个单变量数据集中剔除训练前缀含异常标签的168条序列，保留10个数据集的532条序列，用窗口10000、步长1500评估，并在VUS-PR、Standard-F1、F1-T、Affiliation-F四项指标上与TimeRCD、DADA、MOMENT、TimesFM、Chronos、Time-MoE、MovingVar.等零样本模型及TranAD、USAD、OmniAnomaly、LOF、IForest、Sub-PCA、DCdetector、TFMAE等全样本模型对比，Anlu平均排名1.30至2.90，在多数数据集上取得第一。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：其一，评估仅覆盖 TSB-AD-U 的 350 条序列，且依赖数据集提供的参考前缀，真实工业场景中参考记录往往稀缺或需人工挑选，参考质量对性能的影响未被系统研究；其二，反事实监督依赖合成任务构造，两个参考需支持不同正常规则，这种配对在开放域中如何自动生成仍是难题；其三，方法冻结 TSFM 仅训练记忆与门控适配器，跨域、跨采样率的泛化能力尚不明确。未来可探索：一是参考检索与选择机制，让模型自主从历史库中挑选最相关的参考，而非依赖固定前缀；二是将反事实监督扩展到多参考、连续工况空间，处理渐变型异常；三是引入可解释性输出，如指出查询中哪些位置因参考而改变判定，提升工业可审计性；四是结合在线更新，使参考记忆随工况漂移自适应演化。

### Q6: 总结一下论文的主要内容

论文研究参考条件式时间序列异常检测（reference-conditioned TSAD）：同一模式在不同工况下可能正常也可能异常，仅凭查询本身无法判断适用哪种规则。作者将其形式化为上下文学习问题，即额外输入一段正常参考记录来指明当前工况，模型参数在推理时保持不变。为解决检测器可能忽略参考、仅凭查询拟合标签的捷径问题，论文提出反事实监督：将同一查询与两条支持不同正常规则的参考配对并分别标注，在标签冲突位置上，任何忽略参考的检测器交叉熵至少为 log 2，从而强制模型读取参考。方法上，Anlu 在冻结的时序基础模型上加入参考记忆库和零初始化门控适配器，仅训练该通路。在 TSB-AD-U 的 350 条序列上，Anlu 将平均 VUS-PR 从 0.542 提升至 0.607；将参考置零后降至 0.499，验证增益确实来自参考内容。
