---
title: "ConceptTS: LLM-Guided Concept Bottlenecks for Interpretable Multivariate Time-Series Forecasting"
authors:
  - "Yichen Jiang"
  - "Yueqiao Chen"
  - "Dongyu Liu"
date: "2026-08-21"
arxiv_id: "2608.21277"
arxiv_url: "https://arxiv.org/abs/2608.21277"
pdf_url: "https://arxiv.org/pdf/2608.21277v1"
categories:
  - "cs.LG"
tags:
  - "time series report"
  - "semantic description"
  - "LLM-guided concept bottleneck"
  - "interpretable forecasting"
  - "multivariate time series"
  - "natural language generation"
  - "concept activation"
  - "domain knowledge injection"
  - "intervention"
relevance_score: 8.5
---

# ConceptTS: LLM-Guided Concept Bottlenecks for Interpretable Multivariate Time-Series Forecasting

## 原始摘要

State-of-the-art multivariate time-series forecasters can model complex temporal and cross-variable dependencies, yet their opaque representations provide limited insight into why a particular forecast is produced. This lack of transparency restricts their use in settings where practitioners must understand and assess the factors underlying a prediction. We introduce ConceptTS, an interpretable forecasting framework that organizes its predictions around named, human-readable concepts. ConceptTS uses a large language model to propose task-relevant concepts and generate executable labeling rules, translating the language model's domain knowledge into direct supervision without costly manual concept annotation. The proposed concepts are organized into three complementary bottlenecks that describe the historical context, local forecast intervals, and the full forecast horizon. A shared decoder combines representations derived from their predicted activations to construct the forecast, making the model's decision process explicit and supporting direct concept-level interventions. Experiments on the Beijing Multi-Site Air Quality dataset show that ConceptTS achieves accuracy competitive with strong black-box baselines while producing semantically meaningful concept activations.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

多变量时间序列预测在医疗、环境监测、能源和工业等领域至关重要，但现有高性能模型（如Transformer、图网络等）虽能捕捉复杂时序与变量依赖，其内部表示却高度不透明，无法解释预测背后的具体证据。这种“黑箱”特性在风险敏感场景中严重阻碍了用户对预测结果的信任与故障排查。

现有可解释方法存在明显不足：基于归因或显著性的方法仅提供低层重要性分数，难以表达语义层面的条件；传统概念瓶颈模型（CBM）依赖专家定义概念和逐样本标注，成本高昂；ProtoTS虽引入原型推理，但原型含义需事后推断；TimeX++则仅解释已有预测器，并未让预测过程真正经过命名语义证据。因此，当前缺乏一种既能保持高精度、又能使内部证据语义明确、受监督且直接关联预测路径的预测框架。

本文提出ConceptTS，旨在解决上述核心矛盾。它利用大语言模型自动生成任务相关概念及可执行标注规则，免去人工标注；将概念组织为历史、局部区间和全局预测三个互补瓶颈，通过共享解码器构建预测，使决策过程显式化并支持概念级干预，从而在保持与强黑箱基线竞争精度的同时，提供语义清晰、可干预的预测解释。

### Q2: 有哪些相关研究？

时间序列预测的可解释性研究可分为三类。**第一类是事后归因方法**，如Series Saliency联合学习预测与多变量输入区域的显著性，Temporal Fusion Transformer提供变量选择权重和时序注意力，TimeX++通过信息瓶颈学习分布内、保标签的解释性实例。这些方法主要输出变量和时间戳的重要性或输入实例，但用户仍需自行推断其语义，且解释并非模型实际计算路径的中间表示。**第二类是概念瓶颈模型**，最初用于图像分类，如概念嵌入模型通过嵌入表示概念激活状态。本文将其扩展到多变量时间序列，但需应对趋势、持续时间、跨变量关系等多尺度时序概念，且避免昂贵的人工标注。**第三类是语言引导的概念发现**，如LaBo利用语言模型提出候选概念并通过视觉-语言模型落地，概念瓶颈LLM组织决策于可读概念。这些方法多面向图像或文本，而连续时序需要可执行规则定义概念激活条件。**与本文最接近的是ProtoTS**，它学习与典型预测曲线关联的层次化潜原型，但原型无名称且预测可能依赖原型匹配之外的信息。相比之下，ConceptTS用离线LLM提出命名时序概念和可执行标注规则，将概念组织为历史上下文、局部预测区间和完整预测范围三个瓶颈，通过共享解码器组合激活表示，实现直接检查和干预，无需人工分段标注。

### Q3: 论文如何解决这个问题？

ConceptTS通过一种“LLM引导的概念瓶颈”框架来解决多变量时间序列预测的可解释性问题。其核心思想是让大语言模型（LLM）自动生成人类可读的概念及对应的可执行标注规则，从而替代昂贵的人工概念标注，并将这些概念组织成三个互补的瓶颈模块来驱动预测。

整体框架包含四个主要部分：**LLM概念生成器**、**ModernTCN风格编码器**、**三个并行概念瓶颈**和**共享残差解码器**。

在LLM概念生成器中，系统先对训练数据提取统计摘要（包括回看窗口统计、预测窗口统计、子窗口统计、通道间相关性等），并利用K-means聚类生成数据分布画像。LLM基于这些信息一次性生成三类概念：回看窗口概念（描述历史模式）、预测子窗口概念（描述局部细节）和全局预测概念（描述整体趋势），每个概念都附带一个可执行的Python谓词，用于自动为所有训练片段打上二元标签，避免了逐段调用LLM的高昂成本。

编码器采用ModernTCN的变量独立嵌入和大核深度卷积，分别编码回看窗口和预测窗口，并通过注意力池化将嵌入转换为三个上下文向量。三个概念瓶颈（回看、子窗口、全局）采用CEM结构，每个概念有输入无关的正负嵌入，通过sigmoid激活概率加权混合形成概念上下文向量。子窗口概念还通过双向GRU捕捉跨子窗口的时序依赖。

解码器将概念上下文、BiGRU输出和残差通道拼接，通过堆叠残差解码器以从粗到细的方式生成预测。整个模型端到端训练，使用混合损失（预测损失+概念监督损失），既保证预测精度，又确保概念激活的语义有效性。

### Q4: 论文做了哪些实验？

论文在Beijing Multi-Site Air Quality数据集上进行了实验，以PM2.5为预测目标，包含6种污染物和5种气象特征，覆盖3个监测站点（Aotizhongxin、Dingling、Tiantan），采用MAE和RMSE作为评估指标。实验设置了两种数据可用性场景：未来感知模式（外生特征已知）和仅回看模式（仅用历史数据），分别与不同基线对比。

在未来感知模式下，模型在Aotizhongxin站点取得12.71 µg/m³的MAE，优于Informer（28.62）、随机森林（26.73）、DeepAR（13.97）和NHiT（16.94），与XGBoost（12.34）、TFT（12.44）和LightGBM（12.46）相当。在仅回看模式下，模型MAE为55.59，优于TimeXer（57.43）、iTransformer（59.16）、DLinear（56.27）和LSTM（55.91），略逊于Informer和Crossformer（差距小于0.81）。

消融实验表明：增加预测子窗口概念数量可单调降低MAE；残差通道权重α_residual从1.0降至0.01时，全模型MAE从15.35改善至12.71，但概念瓶颈的贡献度下降（概念仅模型与全模型差距从0.5%扩大至161%），表明该参数可权衡精度与可解释性。案例研究展示了模型在三个概念瓶颈中产生语义明确的概念激活，支持概念级干预。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三方面：一是极端污染尖峰的预测精度不足（RMSE差距较大），说明概念瓶颈对异常事件的建模能力有限；二是概念集完全依赖LLM先验知识，缺乏数据驱动校准，可能遗漏重要领域概念；三是实验仅基于单一空气质量数据集，泛化性未验证。未来可探索：1）引入概念-残差动态路由机制，让模型根据输入自适应调整概念与残差通道的权重，而非固定超参数；2）设计概念验证与修正模块，利用数据分布或反事实推理自动筛选、合并或补充LLM提出的概念；3）将概念瓶颈扩展到多任务场景（如同时预测多种污染物），验证概念共享与迁移能力；4）探索概念激活的时间动态性，建模概念间的时序依赖关系，而非当前独立激活假设。此外，可尝试用概念级对比学习增强概念的可区分性和鲁棒性，或引入不确定性估计提升极端事件预测可靠性。

### Q6: 总结一下论文的主要内容

ConceptTS提出了一种基于大语言模型引导的概念瓶颈框架，用于可解释的多变量时间序列预测。其核心贡献在于利用LLM自动生成任务相关概念及其可执行标注规则，避免了昂贵的人工概念标注。方法上，模型将概念组织为三个互补瓶颈，分别描述历史上下文、局部预测区间和完整预测范围，并通过共享解码器基于概念激活构建预测，使决策过程透明且支持概念级干预。在北京市多站点空气质量数据集上的实验表明，ConceptTS在预测精度上与强黑盒基线相当，同时产生语义上有意义的概念激活。消融实验和干预测试进一步验证了解码器对概念激活通道的依赖，展示了模型在准确性与可解释性之间的有效权衡。该工作为高 stakes 场景下的可信时间序列预测提供了新思路。
