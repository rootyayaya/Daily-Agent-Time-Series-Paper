---
title: "Predicting Only from Selected Evidence: A Tempered Product-of-Experts Bottleneck for Auditable EEG Diagnosis"
authors:
  - "Yinghao Wang"
  - "Shujian Yu"
  - "Duc Han Le"
  - "Zhikai Yu"
  - "Changming Wang"
  - "Van-Tam Nguyen"
date: "2026-08-25"
arxiv_id: "2608.24377"
arxiv_url: "https://arxiv.org/abs/2608.24377"
pdf_url: "https://arxiv.org/pdf/2608.24377v1"
categories:
  - "eess.SP"
tags:
  - "Agentic Time Series"
  - "可解释时序诊断"
  - "证据瓶颈"
  - "产品-of-专家融合"
  - "脑电异常检测"
  - "基础模型适配"
  - "可审计诊断"
  - "信息率限制"
  - "后验KL惩罚"
  - "选择忠实度审计"
relevance_score: 8.5
---

# Predicting Only from Selected Evidence: A Tempered Product-of-Experts Bottleneck for Auditable EEG Diagnosis

## 原始摘要

Pretrained EEG backbones improve transfer performance, but downstream diagnosis heads remain hard to audit: predictions are made from unrestricted hidden states, whereas explanations are usually produced only after the decision. We introduce tPoE-EIB, an evidence-information bottleneck head for adapting EEG backbones under an evidence-only prediction constraint. tPoE-EIB selects temporal and channel evidence, maps the selected summaries to Gaussian experts over a shared latent variable, and fuses them with a tempered product-of-experts posterior. The classifier observes only this latent, so the decision path is explicit and rate-limited by the expected posterior KL. This gives a tractable supervised objective with an information-rate penalty, while the closed-form tempered posterior mitigates overconfident fusion from correlated evidence axes. We evaluate tPoE-EIB on pretrained EEG foundation-model backbones across six diagnosis settings: event-type classification, abnormality detection, seizure detection, cognitive-decline staging, depression screening, and cerebrovascular-disease classification. The evaluation spans public benchmarks and in-house clinical cohorts, binary screening and fine-grained staging, and sparse and dense montages. tPoE-EIB preserves competitive balanced accuracy and improves over representative post-hoc explanations on selection-faithfulness audits, including insertion-deletion and gate-causality tests. Its structured posterior further enables integration-faithfulness audits, including expert-drop, posterior-reliance, and expert-disagreement tests. Overall, these results suggest that evidence-only, rate-limited fusion is a practical route to auditable diagnosis on top of frozen EEG foundation backbones.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

脑电（EEG）诊断正从专用小模型转向预训练基础模型，但下游诊断头的可审计性成为主要瓶颈。现有方法中，冻结骨干网络后接池化与任务头虽性能良好，分类器却可利用隐藏状态中的任意预测规律（如噪声结构、个体特征或伪影线索），且解释仅在预测完成后由事后方法（如积分梯度、Dynamask）生成，未约束实际用于决策的信息，导致解释与真实计算路径脱节，存在忠实性问题。在EEG临床场景中，医生需沿时间与通道两个自然轴审查证据，而现有模型常将支持分散于全时段或集中于解剖学上不合理的通道，难以干预和度量。

为此，本文提出tPoE-EIB，一种将证据置于前向决策路径的下游适应头。其核心是“仅证据预测约束”：分类器只能访问经时间/通道门控、证据摘要及温度化专家乘积后验融合后的潜在变量，无法接触未受限的池化特征，并通过KL项对信息率进行限制。这使决策路径显式化、可审计，同时闭式后验缓解相关证据轴的过度自信融合，为高风险的EEG诊断提供了一条实用的可审计路径。

### Q2: 有哪些相关研究？

相关研究可归为三类。**方法类**中，EEG专用骨干网络（如EEGNet、EEG Conformer）及基础模型（LaBraM、CBraMod、CodeBrain）聚焦于可复用表征学习，但下游头仍直接使用无约束隐状态；本文针对这一最后环节，提出仅基于证据的预测约束。**可解释性类**中，事后归因方法（Integrated Gradients、Dynamask、TIMING）在预测后生成解释，但分类器可能使用了未展示信息；内在约束方法（如Concept Bottleneck Models、Right for the Right Reasons）将预测路径本身受限，但依赖人工标注概念。本文更接近后者，但中间变量是模型自动选择的时域和通道证据摘要，而非人类概念，且同时审计门控和后验融合。**信息瓶颈与融合类**中，Deep VIB通过变分KL率实现信息压缩，多视图方法（如Product-of-Experts）处理相关源融合，但标准PoE假设条件独立。本文针对同一EEG表征的时域与通道投影存在相关性，通过温度化PoE折扣重复支持，避免过度自信融合。与现有工作相比，本文的核心区别在于将证据选择、信息率惩罚和温度化后验融合统一为可审计的诊断头，并在冻结基础模型上实现显式决策路径。

### Q3: 论文如何解决这个问题？

tPoE-EIB通过引入“证据信息瓶颈”头来解决预训练EEG骨干网络下游诊断头难以审计的问题。其核心设计是强制分类器只能从显式选择的证据中获取信息，而非直接使用无约束的隐藏状态。

整体框架遵循“冻结骨干网络→证据选择→后验融合→分类”的流水线。首先，冻结的EEG骨干网络将输入映射为patch-grid表示H。随后，两个轻量MLP分别从时间维和通道维生成连续sigmoid门控g_t和g_c，通过加权平均形成边缘证据摘要e_t和e_c。这两个摘要被送入两个高斯专家网络，各自生成对共享潜变量z的信念分布。

关键技术在于使用“温度化产品-of-专家”（tempered PoE）后验融合两个证据流：q_α(z|e_t,e_c) ∝ p(z)·q_t^α_t·q_c^α_c。温度参数α_t, α_c∈[0,1]可校正相关证据轴导致的过度自信问题——理论证明标准PoE在专家相关时精度过高，而温度化可匹配真实后验精度。该后验具有闭式高斯解，便于训练和推理。

训练目标为证据信息瓶颈目标J_EIB = I(Y;Z) - β·I(E;Z)，其变分下界包含交叉熵损失和KL散度率项。此外还加入两个选择阶段正则化器：稀疏惩罚L_sparse限制门控质量，一致性正则L_cons通过轻增强分支稳定门控。分类器f_ψ仅接收采样的潜变量z，从构造上保证决策路径完全显式且受信息率限制。

创新点包括：证据唯一预测约束（前向图限制）、温度化PoE融合机制、以及可操作的KL率解释——训练后的KL上界约束了输入信息对预测的影响量。这使得模型不仅保持竞争性准确率，还支持多种基于干预的忠实度审计（如专家丢弃、后验依赖测试）。

### Q4: 论文做了哪些实验？

实验围绕四个问题展开：Q1验证仅证据约束的预测可行性，Q2消融头部设计，Q3审计可解释性，Q4检验通道选择的临床对齐性。实验覆盖六个EEG诊断任务（事件分类、异常检测、癫痫检测、认知衰退分期、抑郁症、脑血管疾病），使用TUH公共基准（TUEV/TUAB/TUSZ）和院内临床队列（58-129通道），以CodeBrain为主要冻结骨干，CBraMod为跨骨干验证。对比方法包括EEGNet、ContraWR、BENDR、BIOT、LaBraM及线性探针等。

主要结果：CodeBrain-tPoE-EIB在公共基准上取得最佳平衡准确率（TUAB 80.7%、TUEV 48.8%、TUSZ 76.4%），较线性探针提升+1.7至+2.7个百分点。头部消融显示tPoE-EIB在七个任务中五项排名第一，可学习温度α收敛至约0.5。审计实验表明门控忠实性在时间轴上表现良好（TUAB gap_t=0.169），专家丢弃测试显示通道轴主导（Δc=30.1），后验依赖ρ0≈0.52-0.62。临床对齐验证中，TUAB异常类在枕顶区门控强度翻倍（d=1.75），抑郁症显示顶叶/中央区激活增强，脑血管疾病呈现显著偏侧化。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是tPoE-EIB的因子化接口（时间与通道专家独立建模）无法表达“通道j仅在时段s内重要”这类联合时空依赖模式，限制了证据表达的丰富性；二是当门控值接近均匀分布或高度患者特异时，群体层面的审计存在盲区，难以捕捉个体化诊断路径；三是固定潜在维度d_z缺乏任务自适应性，可能在不同分类粒度（如二分类与细粒度分期）下造成信息瓶颈过紧或过松。

未来探索可从以下方向展开：其一，设计率自适应瓶颈，根据类别或任务动态分配d_z，平衡信息压缩与诊断精度；其二，引入层次化专家结构，将多类决策分解为嵌套判断，提升细粒度分期的可解释性；其三，开发联合时间-通道掩码并施加结构化先验，使模型能表达边际门控无法覆盖的交互模式，同时保持证据可审计性。此外，可探索将tPoE-EIB与在线学习结合，适应非平稳EEG分布，并扩展至跨中心多模态数据验证其泛化能力。

### Q6: 总结一下论文的主要内容

本文提出tPoE-EIB，一种面向可审计EEG诊断的证据信息瓶颈头。其核心约束是“仅凭证据预测”：模型只能从选定的时间与通道证据中提取摘要，映射为共享低维潜变量上的高斯专家，并通过温度化产品-of-专家后验融合；分类器仅接触该潜变量，决策路径显式且受信息率限制。该方法在冻结的EEG基础模型骨干上，通过变分下界优化带信息率惩罚的监督目标，同时缓解相关证据轴导致的过自信融合。在六种诊断任务（事件分类、异常检测、癫痫检测、认知衰退分期、抑郁筛查、脑血管病分类）中，tPoE-EIB保持竞争性平衡准确率，并在选择忠实度审计（插入-删除、门因果测试）上优于事后解释方法；其结构化后验还支持集成忠实度审计（专家丢弃、后验依赖、专家分歧测试）。结论表明，仅证据、限速融合是冻结EEG基础模型上实现可审计诊断的实用路径。
