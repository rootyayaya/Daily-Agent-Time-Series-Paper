---
title: "Do RUL explanations hold up? Faithfulness and stability of attributions on C-MAPSS"
authors:
  - "Manh Hien Nguyen"
  - "Ngoc Thanh Nguyen"
  - "Isabella Mendoza Cortes"
  - "Tam Khuat"
  - "Thanh Pham"
  - "Nhat Quang Tran"
  - "Ushik Shrestha Khwakhali"
  - "Loan Do"
date: "2026-10-03"
arxiv_id: "2610.04278"
arxiv_url: "https://arxiv.org/abs/2610.04278"
pdf_url: "https://arxiv.org/pdf/2610.04278v1"
categories:
  - "cs.LG"
tags:
  - "RUL预测"
  - "可解释性"
  - "归因方法"
  - "C-MAPSS"
  - "预测性维护"
  - "XAI评估"
  - "工业传感器"
  - "忠实性"
  - "稳定性"
relevance_score: 6.5
---

# Do RUL explanations hold up? Faithfulness and stability of attributions on C-MAPSS

## 原始摘要

Deep remaining-useful-life (RUL) models on NASA C-MAPSS are now routine, and so are heatmaps that colour sensors and timesteps. A heatmap that looks mechanical is not the same as an explanation an engineer can act on. We train three standard architectures - a 1D CNN, an LSTM, and a small Transformer encoder - on the official FD001 and FD003 splits with the piecewise RUL cap of 125 cycles and the official PHM08 asymmetric score. We then attach three attribution maps (Integrated Gradients, occlusion, last-layer attention) and evaluate them with the checks the XAI-for-PdM literature still under-reports: deletion/insertion faithfulness, Spearman stability under sensor-scale noise, agreement across training seeds, and cosine consistency inside RUL bins. Prediction error is a prerequisite, not the claim. The headline is which explanation method moves the RUL output when its top cells are removed, and which map survives a 5% input perturbation. Integrated Gradients and occlusion are similarly faithful on the LSTM; Transformer attention is cheap and temporally smooth but weakly faithful. All three maps are almost unchanged under 5% input noise, yet IG/occlusion agree only moderately across two LSTM seeds - stability to sensor jitter is not the same as stability to retraining. A secondary tabular check on the AI4I 2020 failure dataset shows the same deletion pattern for tree importances. We recommend occlusion or IG for any C-MAPSS-style report that will be read by a maintenance engineer, and we treat raw attention weights as a visualisation only.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

深度RUL预测模型在NASA C-MAPSS数据集上已十分常见，随之而来的还有大量对传感器和时间步进行着色的热力图。然而，一张看起来“机械式”合理的热力图，并不等同于工程师可以据以行动的解释。现有XAI-for-PdM文献普遍存在一个关键缺口：它们往往只展示归因图，却很少系统评估这些解释是否忠实、是否稳定。具体而言，删除被高亮的单元是否真的会改变RUL输出？传感器上的微小噪声是否会让归因排序彻底混乱？跨训练种子的归因结果是否一致？这些问题在已有工作中被严重低估。本文的核心问题正是：在C-MAPSS标准基准上，主流归因方法（Integrated Gradients、遮挡、Transformer注意力）所生成的解释，是否经得起忠实性与稳定性的检验？作者刻意保持预测器普通，将实验预算集中在评估套件上，通过删除/插入忠实性、传感器尺度噪声下的Spearman稳定性、跨种子一致性以及RUL分箱内的余弦一致性四项检查，回答“哪种解释方法真正可信”这一问题，并据此给出面向维护工程师的报告建议。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，Lei 等系统综述了从传感器到模型的 RUL 技术栈；Li 等将深度 CNN 引入 C-MAPSS，Zheng 等则推广了 LSTM 的应用，本文正是在这些标准架构（1D CNN、LSTM、Transformer）基础上展开，但重点不在预测精度，而在解释的可信度。评测类方面，本文借用了 XAI 文献中的 deletion/insertion 协议，并参考 Yeh 等对 infidelity 与 sensitivity 的形式化定义，将后者转化为一种按领域缩放的廉价噪声测试；同时本文指出显著性可能与模型无关，这是对既有评测的重要补充。应用类方面，Matzka 发布的 AI4I 2020 是可解释 PdM 分类数据集，本文仅将其作为删除思想在第二领域的验证，而非主实验对象。总体而言，现有工作多关注模型性能或单一归因可视化，本文的差异在于系统评估归因图的忠实性与稳定性，并区分“对传感器抖动的稳定”与“对重训练的稳定”，最终建议在 C-MAPSS 报告中优先使用 occlusion 或 IG，而将原始注意力权重仅视为可视化。

### Q3: 论文如何解决这个问题？

论文的核心方法是把“预测精度”当作前提而非结论，转而系统评估RUL归因图是否可信。整体框架分三步：首先在NASA C-MAPSS官方FD001/FD003划分上，使用分段RUL上限125和PHM08非对称评分，训练三种标准架构——1D CNN、LSTM和小型Transformer编码器；然后为每个模型附加三种归因图：Integrated Gradients（零基线、24步黎曼近似）、Occlusion（将3×1的时间×传感器补丁置零，归因于RUL预测的下降）以及Transformer最后一层自注意力（以最后时间步为查询，并将该时间轮廓广播到所有传感器，因此只能选时间、不能选传感器）；最后用XAI-for-PdM文献常忽略的四类检查进行评测。

关键技术包括：一是忠实性检查，按绝对归因排序，删除或插入前0%、5%、10%、20%、40%的单元，观察预测变化速度；二是稳定性检查，在已归一化窗口上加入N(0,0.05²)噪声后重算归因图，报告展平绝对归因的Spearman ρ；三是种子一致性，用seed 1重训LSTM，在相同40台测试发动机上比较IG/Occlusion图；四是RUL分箱内一致性，在[0,30)、[30,80)、[80,130)区间内报告图之间的平均成对余弦相似度。此外，论文还在AI4I 2020故障数据集上做了表格型补充验证，发现树模型重要性呈现相同的删除模式。

创新点在于：首次在C-MAPSS上系统区分“对传感器抖动的稳定性”与“对重训练的稳定性”，指出所有图在5%输入噪声下几乎不变，但IG/Occlusion在两个LSTM种子间仅中等一致；并给出实践建议——面向维护工程师的报告应使用Occlusion或IG，原始注意力权重仅作可视化。

### Q4: 论文做了哪些实验？

论文在NASA C-MAPSS官方FD001和FD003划分上训练了1D CNN、LSTM和小型Transformer编码器三种架构，采用分段RUL上限125循环和PHM08非对称评分。随后附加三种归因图：积分梯度（IG）、遮挡（occlusion）和末层注意力，并从删除/插入忠实性、传感器尺度噪声下的Spearman稳定性、跨训练种子一致性及RUL分箱内余弦一致性四个维度评估。主要结果：FD001上LSTM最优（RMSE 15.54，评分436.1），Transformer次之（16.13/807.0），CNN较弱（18.70/905.1）；FD003上LSTM为13.67/324.5。删除20%最重要单元后，IG和遮挡使预测RUL变化约35循环，注意力仅13循环；插入曲线同样显示IG/遮挡恢复更快。噪声稳定性ρ均约0.98，但种子间Spearman ρ仅为IG 0.63、遮挡0.56，说明抗抖动稳定不等于抗重训练稳定。此外在FD002/FD004六工况子集上验证，遮挡删除量（60.8/51.6）仍高于IG（41.5/35.1）；在AI4I 2020数据集上用XGBoost做表格验证，树重要性也呈现相同删除模式。

### Q5: 有什么可以进一步探索的点？

论文的局限主要集中在评估范围与实验设定上：未覆盖FD002/FD004的多架构对比，注意力机制无法与IG在传感器身份层面直接比较，噪声尺度仅沿用z-score惯例而非真实传感器规格。未来可探索的方向包括：一是将忠实性与稳定性评估扩展到多故障模式、多工况数据集，检验结论是否具有跨域泛化性；二是引入更高效的归因方法（如基于梯度的随机路径近似）以替代计算代价高昂的KernelSHAP；三是建立“解释稳定性”与“模型不确定性”之间的理论联系，例如用贝叶斯深度集成量化归因方差；四是结合领域知识设计传感器分组归因，使解释更贴近工程师的故障推理逻辑。此外，可将归因一致性作为正则项嵌入训练目标，从源头提升解释可靠性，而非仅在事后评估。

### Q6: 总结一下论文的主要内容

论文针对NASA C-MAPSS数据集上深度剩余寿命（RUL）预测模型的可解释性问题展开研究。作者指出，热力图看似合理并不等于工程师可据此采取行动。为此，他们在FD001和FD003官方划分上训练了1D CNN、LSTM和小型Transformer编码器三种标准架构，并附加Integrated Gradients、遮挡法和末层注意力三种归因图，系统评估了删除/插入忠实性、传感器尺度噪声下的Spearman稳定性、跨训练种子的致性以及RUL分箱内的余弦一致性。主要结论是：IG与遮挡法在LSTM上忠实性相近；Transformer注意力虽计算廉价且时间平滑，但忠实性较弱；三种归因图在5%输入噪声下几乎不变，但IG与遮挡法在两个LSTM种子间仅中等一致，说明对传感器扰动的稳定性不等于对重训练的稳定性。作者建议面向维护工程师的C-MAPSS报告优先采用遮挡法或IG，并将原始注意力权重仅视为可视化工具。
