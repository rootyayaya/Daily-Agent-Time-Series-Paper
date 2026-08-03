---
title: "TFGformer: Multivariate Time Series Forecasting via Time-Frequency Graph Learning and Covariate Fusion"
authors:
  - "Yu Sun"
  - "Yuan Chang"
  - "Xiaohou Shi"
  - "Yan Sun"
date: "2026-07-31"
arxiv_id: "2607.29459"
arxiv_url: "https://arxiv.org/abs/2607.29459"
pdf_url: "https://arxiv.org/pdf/2607.29459v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Retrieval-Augmented Generation"
  - "Time Series Forecasting"
  - "Multivariate Time Series"
  - "Shape-Aware Memory"
  - "Contrastive Learning"
  - "Cross-Attention Fusion"
  - "Predictive Maintenance"
  - "IoT Sensors"
relevance_score: 8.5
---

# TFGformer: Multivariate Time Series Forecasting via Time-Frequency Graph Learning and Covariate Fusion

## 原始摘要

Large-scale multivariate time series from heterogeneous IoT sensors demand accurate long-term forecasting for resource scheduling and predictive maintenance. While recent time series foundation models exhibit strong generalization, they rely on static parametric knowledge and lack dynamic access to external historical patterns during inference. Retrieval-Augmented Generation (RAG) offers a potential remedy, yet its application to time series forecasting is challenged by magnitude variations across heterogeneous sources and the mismatch between historical similarity and future consistency. We propose CrossRAG, a retrieval-augmented forecasting framework that integrates Shape-Aware Memory (SAM) with RevIN normalization for magnitude-robust shape-level retrieval, Future-Consistent Contrastive (FCC) learning to distinguish informative references from hard negatives with similar history but divergent futures, and Cross-Attention Temporal Fusion (CATF) to fuse retrieved historical--future reference pairs into the backbone's representations at the representation level. Experiments on seven public benchmarks show that CrossRAG consistently outperforms both parametric-only baselines and existing retrieval-augmented forecasting methods.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

本文聚焦于多元时间序列长期预测中动态变量依赖建模与外部协变量融合两大核心挑战。研究背景在于，物联网异构传感器产生的大规模多元时间序列，其变量间关系复杂且随时间演化，而现有Transformer架构存在明显不足：PatchTST采用通道独立处理，缺乏跨变量显式建模与可解释性；iTransformer虽引入通道混合注意力，却忽略单变量内部细粒度时序动态；TimerXL虽联合建模内外部模式，但假设变量关联静态不变，难以适应稀疏或时变依赖场景。同时，现有模型对日历属性、设备元数据等协变量的利用多采用简单拼接或额外通道方式，易引入噪声且忽视其内在结构，TiDE和ChronosX虽展示了专用融合优势，但分别受限于MLP架构和单变量token化设计，不适用于多元patch化场景。为此，本文提出TFGformer框架，核心创新在于：一是设计基于短时傅里叶变换和马氏距离的时频图结构学习模块，在联合时频域估计变量间动态非线性关系概率，自适应构建注意力掩码以精确建模复杂交互；二是引入MLP协变量融合模块，通过残差连接整合历史与未来协变量，保留原始数据特征并充分利用先验趋势知识。实验在电力、交通、天气等七个基准数据集上验证了该方法在多预测步长和评估指标下的最优性能。

### Q2: 有哪些相关研究？

在时间序列预测领域，相关研究主要分为以下几类：

**方法类**：基于Transformer的模型，如Informer、Autoformer、PatchTST和iTransformer。其中，通道独立方法（如PatchTST）关注变量内部时序模式，通道混合方法（如iTransformer）建模变量间关系，而混合设计（如TimerXL）结合两者优势。本文与这些工作的区别在于，它们假设所有变量对具有相同相关强度，无法区分动态变化的关系，而本文通过时间-频率图学习显式建模变量间时变相关性。

**频率域方法**：近期研究利用频域特征刻画多元同步性和周期性，但多数依赖全局傅里叶变换，忽略时间局部性。本文采用局部频率分解，能捕捉非平稳、时变的相关结构。

**协变量融合方法**：主流模型采用简单拼接或将协变量作为附加变量处理，易引入噪声。ChronosX虽引入融合模块，但仅针对单变量token框架。本文提出协变量融合机制，在patch级别有效整合异构协变量信息。

**评测与应用**：本文在多个公开基准上验证，相比参数化基线和现有检索增强预测方法均取得更优性能，体现了其在工业故障诊断等实际场景中的潜力。

### Q3: 论文如何解决这个问题？

TFGformer通过一个三阶段架构解决多变量时间序列预测中的跨变量依赖建模和协变量融合问题。整体框架包含三个核心模块：时间-频率图学习模块（TFG）、协变量特征融合模块（CFM）和Transformer序列建模模块。

TFG模块是核心创新点。它首先对每个变量通道执行短时傅里叶变换（STFT），获得时频域幅度谱图，将时间与频率信息联合编码为通道特征向量。随后引入可学习的马氏距离度量，通过二次型形式计算通道间距离，该度量能捕捉时频特征空间的协方差结构，比简单加权距离更灵活。距离矩阵经倒数变换和最大归一化得到概率矩阵，再通过Gumbel-Softmax重参数化采样生成离散二值邻接矩阵，实现可微分的图结构学习。该邻接矩阵与因果时间掩码做Kronecker积，生成最终注意力掩码，在Transformer注意力计算中显式约束跨变量交互。

CFM模块分为输入融合（I-CFM）和输出融合（O-CFM）两个子模块。I-CFM在输入阶段将历史协变量与patch嵌入拼接，经ReLU激活和MLP变换后通过残差连接注入，使嵌入携带历史上下文信息。O-CFM在解码端将未来协变量与Transformer隐藏状态融合，通过类似结构调制表示，并对缺失协变量采用前向填充和零填充策略保证鲁棒性。

Transformer骨干采用多头自注意力，注意力分数通过掩码加法实现因果性和通道选择性。最终线性输出头生成预测。创新点在于：将时频分析与图学习结合，通过马氏距离和Gumbel-Softmax实现端到端可微的稀疏图结构发现；双阶段协变量融合使模型同时利用历史与未来外生信息；整体计算复杂度为O(C²·L)，兼顾效率与表达能力。

### Q4: 论文做了哪些实验？

论文在四个真实世界多元时间序列数据集上进行了实验：ETT（含ETTh1、ETTh2、ETTm1、ETTm2四个子集）、ECL（321个客户端）、Traffic（862个道路传感器）和Weather（21个气象指标）。数据划分遵循惯例，ETT数据集按6:2:2比例分为训练、验证和测试集，其余数据集按7:1:2划分。输入长度固定为96，预测长度评估{96, 192, 336, 720}，使用MSE和MAE作为核心指标。模型采用Adam优化器，学习率从{1e-4, 5e-4, 1e-3}中调优，配合学习率退火和早停策略，在单张NVIDIA A800-SXM4-40GB GPU上运行。

对比方法包括iTransformer、TiDE、PatchTST、Autoformer、FEDformer和DLinear六个代表性基线。结果显示TFGformer在7个数据集中的6个（ETTh2、ETTm1、ETTm2、Weather、Electricity、Traffic）上取得最优平均MSE和MAE，在ETTh1上保持竞争力。平均而言，TFGformer相比iTransformer降低MSE 3.6%，相比PatchTST降低6.4%，相比TiDE降低5.2%，相比FEDformer降低16.4%。

消融实验验证了TFG和CFM模块的有效性：移除CFM导致平均MSE增加3.0%，移除TFG导致平均MSE增加6.0%。此外，通过热力图可视化展示了TFG模块学习到的变量相关性结构，并对Gumbel-Softmax温度参数τ进行了敏感性分析，发现τ=0.5时Weather数据集取得最优MSE（0.162）。

### Q5: 有什么可以进一步探索的点？

TFGformer在时频图构建和协变量融合上展现了优势，但仍存在可探索空间。首先，其可学习的马氏距离图结构虽能捕捉动态依赖，但图拓扑的稀疏性阈值和频段选择依赖人工设定，未来可引入自适应稀疏化或神经架构搜索，以提升对不同数据分布的鲁棒性。其次，STFT的固定窗长限制了时频分辨率，可尝试小波变换或多尺度频谱分解，以更好处理非平稳信号。在模型扩展上，当前仅关注预测任务，向异常检测和插补迁移时，需重新设计图构建的损失函数以适配重构目标。此外，协变量融合模块对缺失或噪声协变量的敏感性未充分讨论，可引入不确定性量化或门控机制增强鲁棒性。最后，向大规模基础模型扩展时，TFGformer的图学习计算开销可能成为瓶颈，可探索图稀疏化加速或蒸馏策略，并考虑与预训练模型结合，以提升跨域泛化能力。

### Q6: 总结一下论文的主要内容

TFGformer提出了一种面向多变量时间序列预测的新框架，核心贡献在于结合时频图学习与协变量融合。问题定义上，它针对异构传感器产生的大规模多变量序列，需实现长期精准预测以支持资源调度和预测性维护。方法上，该框架包含两个关键模块：一是时频图模块，利用短时傅里叶变换（STFT）和可学习的马氏距离构建稀疏动态依赖图，以此引导注意力机制并有效过滤噪声；二是基于MLP的协变量融合模块，用于整合历史与未来上下文信息。实验在七个公开基准数据集上进行，结果显示TFGformer在六个数据集上取得了优于现有方法的性能，验证了其有效性和泛化能力。该工作的意义在于为多变量时间序列建模提供了结合频域特征与动态图结构的新思路，未来计划将架构扩展至异常检测、数据填补及大规模基础模型领域。
