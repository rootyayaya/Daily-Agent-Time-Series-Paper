---
title: "INTERVenE: Temporal-Abstraction-Interval Based Transformers for Short-Horizon Medical Event Prediction"
authors:
  - "Shahar Oded"
  - "Yuval Shahar"
date: "2026-08-30"
arxiv_id: "2608.29901"
arxiv_url: "https://arxiv.org/abs/2608.29901"
pdf_url: "https://arxiv.org/pdf/2608.29901v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "时间序列预测"
  - "电子健康记录"
  - "时间抽象"
  - "可解释性"
  - "Transformer"
  - "医疗事件预测"
  - "知识驱动"
  - "区间表示"
relevance_score: 6.5
---

# INTERVenE: Temporal-Abstraction-Interval Based Transformers for Short-Horizon Medical Event Prediction

## 原始摘要

Electronic Health Record (EHR) prediction models in the intensive care unit must learn from sparse and irregular measurements while preserving the clinical meaning of time and supporting transparent decision-making. We present INTERVenE, a family of Transformer architectures whose input is an interval-based, knowledge-based temporal abstraction (KBTA), a token stream of named clinical concepts (states, trends, events, contexts) drawn from a curated medical ontology, rather than an unnamed bin index or a raw measurement triplet. This naming layer is what we ask KBTA to do: it makes the model's per-token attributions resolve to clinical concepts by construction. INTERVenE offers two complementary variants: an auto-regressive decoder that generates future abstraction trajectories with a per-step risk readout (localizing \emph{when} and \emph{after which events} risk rises), and a bidirectional encoder for single-pass joint risk and time-to-event prediction. Evaluated on 57,078 MIMIC-IV admissions against GRU-D, STraTS, and KarmaLego, INTERVenE-Enc reaches a support-weighted AUPRC$_w$ of 0.672, improving by 0.041 over the strongest neural baseline with non-overlapping 95\% bootstrap CIs, while also taking the best AUROC$_w$ (0.901) and length-of-stay MAE (44.4\,h). INTERVenE-Ar (AUROC$_w$ $0.854$, AUPRC$_w$ $0.587$ under the same evaluation contract - a strictly harder generative readout) provides a complementary token-level risk trajectory. An input-representation ablation confirms the lift transfers across structured discretizations, positioning KBTA-based intervals as the interpretable substrate that makes per-token attributions resolve to meaningful clinical concepts within the deployed model.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

该论文聚焦于重症监护病房（ICU）中的短期并发症预测问题，其核心挑战在于电子健康记录（EHR）数据具有稀疏性、不规则性和异质性，原始观测值（如实验室检测、用药记录）的临床意义往往依赖于持续时间、趋势和缺失模式。现有方法存在两方面不足：一是高容量神经网络（如GRU-D、STraTS）虽能处理复杂时序数据，但“黑箱”特性限制了临床信任；二是传统符号方法（如KarmaLego）虽可解释但预测性能有限。因此，本文旨在解决“如何在保持预测性能的同时，使模型中间表示具有临床可解释性”这一核心矛盾。具体而言，论文提出将原始观测转换为基于知识的时间抽象（KBTA）区间，形成命名临床概念（状态、趋势、事件、情境）的token流，并构建两种Transformer变体：INTERVenE-Enc用于单次风险与事件时间预测，INTERVenE-Ar用于自回归轨迹生成与逐步骤风险读出。通过这一设计，模型能够将每个token的归因解析为具体临床概念，从而在预测性能（AUPRC达0.672）与可解释性之间取得平衡，验证了KBTA作为可解释基板的有效性。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，KBTA（基于知识的时序抽象）将原始观测转化为带语义的区间状态、趋势和事件，本文直接采用其作为输入表示；KarmaLego挖掘频繁时间区间关系模式，TPF将模式分布压缩为定长向量，本文将其作为传统临床时序挖掘基线。**深度模型类**中，GRU-D通过学习衰减建模缺失值和观测间隔，STraTS用集合注意力处理值-时间-变量三元组，而现有Transformer多依赖就诊级摘要或诊断编码。本文区别于这些方法的关键在于：不处理原始点值或聚合编码，而是将KBTA语义区间作为token，结合Time2Vec连续时间嵌入，实现深度序列模型与临床先验知识的融合。**可解释性类**中，SHAP/LIME等事后方法在原始测量流上难以定位“何时、何种情境”的影响，而本文通过构造性设计——每个token本身即命名临床概念（如“三天血糖下降趋势”），使注意力归因天然对应可理解的医学实体，无需事后解释。整体上，本文填补了KBTA与深度Transformer之间的空白，既保留临床语义又获得神经网络的表示能力。

### Q3: 论文如何解决这个问题？

INTERVenE通过将临床时间序列转化为基于知识的时间抽象（KBTA）区间序列，从根本上重塑了Transformer的输入表示。其核心架构包含三个关键设计：

首先，原始临床记录经Mediator引擎映射为具有临床语义的KBTA区间（如“高血糖状态”“上升趋势”），每个区间被拆分为START和END两个边界token，并通过四层分层嵌入（原始概念→TAK抽象→带值概念→位置角色）编码，例如“GLUCOSE_STATE_HIGH_START”这样的命名概念链。这种设计使语义相似的token天然共享底层嵌入，同时将Time2Vec时间编码与概念嵌入拼接后线性投影，避免了标准Transformer中加法混合导致的信息纠缠。

其次，模型采用共享骨干网络，通过注意力掩码区分两种变体：INTERVenE-Ar使用因果掩码进行自回归轨迹生成，在每个生成步骤输出风险读数；INTERVenE-Enc使用双向注意力进行单次前向的风险与时间联合预测。骨干网络集成时间RoPE位置编码和AdaLN-Zero自适应层归一化，将静态患者上下文注入每个Transformer块。

训练采用三阶段策略：阶段1用时间下一token预测（多热BCE+时间差回归）预训练嵌入器；阶段2分别采用合法性掩码的软核时间目标（自回归）或原子区间掩码的MLM（双向），并辅以时间差回归、成对排序损失等辅助任务；阶段3进行风险头对齐微调，通过教师强制到自由运行的分布偏移补偿。

创新点体现在：软核时间目标解决了终端事件稀疏问题，原子区间掩码防止了边界token间的信息泄漏，梯度解耦的稀疏转码器钩子实现了不改变模型行为的可解释性归因，使每个token的贡献直接对应到命名的临床概念。

### Q4: 论文做了哪些实验？

实验基于MIMIC-IV糖尿病队列共57,078次入院记录，预测六种临床结局（肾脏损伤、高血糖、严重高血糖、低血糖、严重低血糖、死亡）。所有方法共享相同的训练/验证/测试划分和评估协议，采用2,000次患者级bootstrap重抽样计算95%置信区间。对比方法包括KarmaLego+TPF、GRU-D、STraTS（预训练+微调）和ss-STraTS，以及INTERVenE的两种变体：自回归解码器（INTERVenE-Ar）和双向编码器（INTERVenE-Enc）。主要指标为支持加权AUPRC（AUPRC_w）。

结果显示INTERVenE-Enc达到最优AUPRC_w 0.672，比最强神经基线ss-STraTS提高0.041，比KarmaLego提高0.085，且95%置信区间不重叠；同时取得最佳AUROC_w（0.901）、F1_w（0.628）和住院时长MAE（44.4小时）。逐结局分析中，INTERVenE-Enc在六个结局中的五个取得最高AUPRC，肾脏损伤（0.790 vs 0.726）和死亡（0.605 vs 0.563）提升最大。INTERVenE-Ar在更困难的自回归生成评估协议下达到AUROC_w 0.854、AUPRC_w 0.587。校准方面，INTERVenE-Enc支持加权ECE为0.016，温度缩放后降至0.013。可解释性分析显示，死亡风险归因主要由严重低白蛋白血症等临床概念主导，负向归因则对应恢复相关概念。

### Q5: 有什么可以进一步探索的点？

INTERVenE的进一步探索可从以下几个方向展开。首先，其核心局限在于KBTA层依赖专家构建的TAK知识库，扩展至新疾病或人群需重新定义抽象规则，成本高昂。未来可探索利用大语言模型自动生成或扩充抽象规则，或设计可学习的离散化层，在保留可解释性的同时减少人工干预。其次，当前粒度将临床等价数值折叠为同一概念，可能丢失细粒度信息，可尝试分层或多尺度时间抽象以捕捉更细微的生理变化。第三，模型仅在MIMIC-IV单一队列验证，需外部多中心验证及跨人群公平性分析。此外，训练成本高昂限制了多随机种子评估，可探索模型剪枝、知识蒸馏或更高效的训练策略以降低计算开销。最后，INTERVenE-Ar的自回归生成虽能定位风险上升时机，但其推理速度慢，可研究非自回归生成或引入检索增强机制来平衡效率与可解释性。

### Q6: 总结一下论文的主要内容

INTERVenE提出了一种基于知识型时间抽象（KBTA）的Transformer家族，用于重症监护室电子健康记录中的短期医疗事件预测。其核心创新在于将输入表示为来自医学本体论的命名临床概念（状态、趋势、事件、情境）的令牌流，而非原始测量值或未命名的时间桶，从而在构造上确保模型每个令牌的归因可解析为临床概念。方法包含两种变体：自回归解码器INTERVenE-Ar生成未来抽象轨迹并逐步输出风险读数，定位风险升高的时间点与触发事件；双向编码器INTERVenE-Enc则进行单次联合风险与事件时间预测。在57,078例MIMIC-IV入院数据上，INTERVenE-Enc的加权AUPRC达0.672，较最强神经基线提升0.041，AUROC达0.901，住院时长MAE为44.4小时；INTERVenE-Ar在更严格的生成式评估下也表现良好。消融实验证实性能提升可跨离散化方案迁移，表明KBTA区间作为可解释基底，使模型内归因指向有意义的临床概念，实现了预测性能与临床可解释性的统一。
