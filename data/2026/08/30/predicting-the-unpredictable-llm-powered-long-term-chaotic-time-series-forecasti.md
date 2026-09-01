---
title: "Predicting the Unpredictable: LLM-powered Long-term Chaotic Time Series Forecasting under Short-term Observations"
authors:
  - "Yuhang Yao"
  - "Bohan Jiang"
date: "2026-08-30"
arxiv_id: "2608.29579"
arxiv_url: "https://arxiv.org/abs/2608.29579"
pdf_url: "https://arxiv.org/pdf/2608.29579v1"
categories:
  - "cs.LG"
tags:
  - "LLM for time series forecasting"
  - "chaotic time series"
  - "phase-space embedding"
  - "multivariate fusion"
  - "gated weighting"
  - "short-term observations"
  - "long-term prediction"
relevance_score: 7.5
---

# Predicting the Unpredictable: LLM-powered Long-term Chaotic Time Series Forecasting under Short-term Observations

## 原始摘要

Chaotic time series forecasting is a challenging task due to its sensitivity to initial conditions and long-term unpredictability. Traditional methods typically rely on sufficient temporal trajectories to learn long-term dynamics, which limits their applicability when only short-term observations are available. While recent Large Language Models (LLMs) have shown great potential for time series forecasting, their temporal representations are not explicitly tailored to the phase-space structure and nonlinear evolution of chaotic systems. To address these issues, we propose PAC-LLM, a phase-space-aware adaptive fusion framework for long-term chaotic time series forecasting powered by LLMs. PAC-LLM leverages learned phase-space features and textual information to fully enable LLM's time series forecasting capacity. In particular, we design an auxiliary feature module and a gated weighting mechanism for multivariate coupling information fusion and selection. Extensive experiments on representative chaotic systems demonstrate that our method outperforms existing fine-tuned and zero-shot baselines in both short-term and long-term predictions. Our ablation study further confirms the effectiveness of each key component in PAC-LLM.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

混沌时间序列预测在气象、神经科学和金融建模等领域具有重要价值，但其对初始条件的高度敏感性和长期不可预测性构成核心挑战。现有方法主要依赖足够长的历史轨迹来学习系统动力学，然而在实际场景中，由于传感时长限制、系统新部署或在线预测需求，往往只能获得短期观测数据，这严重制约了传统方法的适用性。

尽管大语言模型（LLM）在通用时间序列预测中展现出潜力，但其时间表示并未针对混沌系统的相空间结构和非线性演化特性进行专门设计，直接应用难以捕捉混沌动力学的本质。此外，多变量混沌系统中变量间的耦合关系会导致预测误差随时间累积，而现有方法缺乏有效的多变量信息融合机制。

本文旨在解决短期观测条件下长期混沌时间序列预测这一难题，核心挑战在于如何从有限观测中恢复局部动力学状态，并充分利用LLM的通用时序知识。为此，作者提出PAC-LLM框架，通过可学习的延迟坐标嵌入构建相空间感知表示，结合门控自适应加权机制融合多变量耦合信息，从而在短期观测下实现准确的长期混沌预测。

### Q2: 有哪些相关研究？

混沌时间序列预测的相关研究主要分为三类。**传统动力学方法**包括状态空间重构、储备池计算（如ESN）及其扩展，以及NVAR（非线性向量自回归），这些方法依赖显式非线性特征或随机储备池，但对状态构建和超参数敏感，且需要充足轨迹。**深度学习方法**涵盖LSTM、GRU、TCN等循环/卷积模型，以及Transformer、GNN、CNN等架构，用于捕捉长程依赖和变量耦合，但缺乏对混沌系统相空间结构的显式建模。**LLM基方法**包括Chronos（通用时序基础模型）、DynaMix（上下文驱动的动力学重建）、Panda（大规模合成系统学习），以及PromptCast、Time-LLM、CrossTimeNet、LLM-Mixer、TimeCMA、LLM-PS和TimeReasoner等通用时序LLM适配方法。这些方法虽展示了LLM的潜力，但大多依赖足够长的输入上下文，且未针对混沌系统的局部敏感性和误差累积设计专门机制。本文PAC-LLM的独特之处在于：首次在短观测条件下，将相空间特征与文本提示融合，通过门控加权机制实现多变量耦合选择，从而在统一评测设置下显著提升长期预测精度与稳定性，弥补了现有方法在混沌动力学适配上的空白。

### Q3: 论文如何解决这个问题？

PAC-LLM通过四个核心模块解决短观测下混沌时间序列长期预测的难题。整体框架采用“相空间重构+LLM时序建模+通道交互+自适应融合”的架构。

首先，**相空间感知表示学习**模块基于Takens嵌入定理，设计可学习延迟嵌入层，通过可微插值核为每个变量构建延迟坐标向量，自适应提取吸引子结构，避免固定延迟参数。随后提取混沌统计量（复杂度、峰度、谱熵）经MLP生成FiLM参数，对相空间表示进行通道级调制，增强对系统动力学状态的敏感性。

其次，**LLM时序建模**模块将调制后的表示分割为重叠patch，通过可重编程模块（交叉注意力）将patch token映射到LLM语义空间，同时构造动力学感知文本提示（趋势、能量、形态描述）嵌入LLM，两者拼接后输入冻结的LLM骨干网络，捕获长程时间依赖。

第三，**辅助通道交互模块**沿变量维度执行多头自注意力，显式建模多变量耦合关系，并通过相似度门控（余弦相似度+门控网络）对辅助特征进行修正，抑制与主分支不一致的通道信息。

最后，**加权融合预测**模块通过可靠性门控（sigmoid网络）自适应控制辅助修正项的注入强度，生成融合特征后经残差预测头输出未来轨迹。训练采用融合损失与辅助损失的加权组合，约束辅助分支有效性。创新点在于将相空间拓扑结构与LLM语义空间对齐，并通过双重门控机制实现主辅分支的可靠融合。

### Q4: 论文做了哪些实验？

论文在四个混沌系统（Lorenz63、Rossler、Chua、Lorenz96）及IBM双摆真实噪声数据集上进行了实验。实验采用自回归滚动预测协议，输入窗口固定为30步，测试评估30、120、300步（约1、4、10个Lyapunov时间）的预测性能。对比方法涵盖六类基线：动力学模型（NVAR、ESN）、LLM方法（TimeLLM、LLMMixer）、Transformer（Crossformer）、CNN/RNN（TimesNet、LSTNet）、MLP（NBEATS）和基础模型（Panda）。

主要结果：PAC-LLM在全部对比中取得23项最优、1项次优。以Lorenz63为例，sMAPE@1为8.14（次优12.55），sMAPE@10为81.51（次优93.31），VPT达4.57（次优3.40）；Rossler系统sMAPE@1仅2.24，VPT达9.53。在吸引子重建指标上，Lorenz63的D_frac为0.060、D_stsp为0.043，均显著优于基线。消融实验表明，移除辅助分支导致MSE和MAE分别增加57.9%和62.2%，移除时间特征模块增加44.6%和49.1%，验证了各关键组件的有效性。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下几个方向展开：

**1. 高维与真实复杂系统的泛化**  
当前实验仅覆盖3-8维混沌系统，而真实工业/气象系统往往具有数十至数百维状态空间。可探索如何将延迟嵌入维数m自适应扩展到高维场景，并验证在含噪声、非平稳的真实传感器数据（如电力负荷、金融序列）上的表现。

**2. 理论保障与可解释性**  
PAC-LLM依赖经验性的相空间重构，缺乏对Lyapunov指数估计误差的理论界分析。未来可研究融合物理信息（如已知动力学方程）或引入符号回归，使预测轨迹不仅统计上接近，更能从动力学机制上可解释。

**3. 计算效率与轻量化**  
当前使用GPT-2/Qwen-3B等大模型，推理成本较高。可探索知识蒸馏、量化或设计轻量级混沌专用Transformer，在保持精度的同时降低部署门槛，尤其适用于边缘计算场景。

**4. 多尺度与跨系统迁移**  
不同混沌系统的时间尺度差异大，当前需针对每个系统单独训练。未来可研究元学习或预训练-微调策略，使模型能快速适应新系统，甚至实现零样本跨系统预测。

**5. 不确定性量化**  
混沌预测本质具有不确定性边界，当前方法仅输出点预测。可引入概率预测头或集成方法，输出预测轨迹的置信区间，为决策提供风险度量。

### Q6: 总结一下论文的主要内容

本文提出PAC-LLM框架，用于解决短时观测下的长期混沌时间序列预测难题。问题定义上，混沌系统对初值敏感且长期不可预测，传统方法依赖充足历史轨迹，而实际场景常仅有短期观测。方法上，PAC-LLM结合大语言模型与相空间理论：通过可学习的延迟坐标嵌入补充局部动态状态信息，构建相空间感知表示；利用预训练LLM提取时间演化模式，并设计辅助特征模块引入多变量耦合信息；采用门控自适应加权机制控制辅助修正强度，避免冗余耦合噪声干扰。实验覆盖合成与真实混沌系统，对比九个微调及零样本基线，PAC-LLM在短期与长期预测中均取得最优精度，有效预测时间更长，且能保持长期动态结构。消融实验验证了各关键组件的有效性。该工作首次将LLM能力与混沌相空间结构显式结合，为有限数据下的混沌预测提供了新范式，对气象、神经科学等领域的工程应用具有重要价值。
