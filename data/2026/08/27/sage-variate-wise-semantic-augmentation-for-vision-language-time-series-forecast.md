---
title: "SAGE: Variate-Wise Semantic Augmentation for Vision-Language Time Series Forecasting"
authors:
  - "Haizhao Fan"
  - "Xinyi Le"
date: "2026-08-27"
arxiv_id: "2608.26829"
arxiv_url: "https://arxiv.org/abs/2608.26829"
pdf_url: "https://arxiv.org/pdf/2608.26829v1"
categories:
  - "cs.LG"
  - "cs.CV"
tags:
  - "Time Series Forecasting"
  - "Vision-Language Model"
  - "CLIP"
  - "Semantic Augmentation"
  - "Multimodal Learning"
  - "Variable-Specific Description"
  - "Statistical Descriptors"
  - "Contrastive Learning"
  - "Long-Term Forecasting"
  - "M4 Benchmark"
relevance_score: 7.5
---

# SAGE: Variate-Wise Semantic Augmentation for Vision-Language Time Series Forecasting

## 原始摘要

Time series forecasting models operate on raw numerical sequences, lacking the semantic knowledge that domain experts implicitly leverage, such as the physical meaning of each variable, its statistical behavior, and its temporal dynamics. Recent efforts to bridge this gap fall into two camps. Some rely on large language models at inference time, which is computationally expensive. Others apply uniform textual prompts at the dataset level, ignoring the heterogeneous semantics across individual variates. We propose SAGE (Seeing and Augmenting with Grounded Encoding), an end-to-end CLIP-based framework that jointly models temporal, cross-variable, textual, and visual information. The CLIP text encoder processes frequency-enhanced patches and variable tokens, while gated residual paths inject variable-specific descriptions and statistical descriptors. In parallel, the frozen CLIP vision encoder aligns rendered series with temporal representations through a training-only contrastive objective. This dual use of CLIP adds complementary semantic and visual supervision without placing an LLM in the forecasting loop. Across eight long-term benchmarks and M4, SAGE achieves state-of-the-art accuracy. Ablations confirm complementary gains from multimodal alignment and variable-level knowledge.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列预测模型通常直接处理原始数值序列，缺乏领域专家隐式依赖的语义知识（如每个变量的物理含义、统计行为和时间动态）。现有弥补这一差距的方法存在明显不足：一类方法在推理时依赖大语言模型，计算成本高昂；另一类方法在数据集层面应用统一的文本提示，忽略了不同变量之间的异质语义。此外，许多多模态方法仅将语言模型用作冻结的特征提取器或辅助提示生成器，未能充分利用视觉-语言模型（如CLIP）的双重结构——其文本编码器可作时序主干，视觉编码器可提供互补的视觉监督。

本文提出SAGE框架，核心目标是构建一个端到端的CLIP-based预测模型，同时建模时间、跨变量、文本和视觉信息。通过模板化知识注入和变量级门控机制，在训练中注入变量特定描述和统计描述符，无需在预测循环中调用LLM；同时利用冻结的CLIP视觉编码器通过对比学习对齐渲染的序列图像与时间表示。该设计旨在以紧凑的可训练主干替代亿级参数模型，实现多模态对齐与变量级知识注入的互补增益，最终提升长期预测的准确性。

### Q2: 有哪些相关研究？

相关研究可分为以下几类：

**1. 基于LLM的时间序列预测方法**：如GPT4TS、LLMTime、Time-LLM和TEST，它们利用预训练语言模型作为骨干或通过文本提示对齐时间序列。本文指出这些方法将语言模型视为通用特征提取器，而非真正的时间知识来源，且推理时计算开销大。

**2. 多模态融合方法**：Time-VLM、Aurora和VLM4TS结合视觉、文本与时间序列，但多将语言模型作为冻结特征提取器或辅助提示生成器，未在统一训练框架中充分利用视觉-语言模型的双分支。SAGE则同时利用CLIP的文本和视觉编码器，通过端到端训练实现互补监督。

**3. 监督式时间序列架构**：Autoformer、PatchTST、iTransformer、TimesNet及FredFormer、DUET、Amplifier、SRSNet等近期基线，专注于分解、通道独立或频域建模，但缺乏语义知识注入。SAGE在这些强基线上进行基准测试，并通过多模态对齐超越它们。

**4. 基础模型**：TimesFM、Chronos、MOMENT、Moirai和Time-MoE依赖大规模预训练，而SAGE遵循OccamVTS的思路，证明无需十亿级数据即可利用预训练视觉-语言表征中的可迁移时间知识。

**5. 对比学习表示方法**：TS-TCC、TS2Vec、CoST、TF-C、Soft-CL和FACL均在时间序列模态内构建正样本对。SAGE的独特之处在于跨模态对比学习，将时间表示与视觉渲染配对，提供超越模态内增强的互补监督信号。

### Q3: 论文如何解决这个问题？

SAGE提出了一种端到端的多模态时间序列预测框架，核心思路是同时利用CLIP的文本编码器和视觉编码器，在不引入LLM推理开销的前提下注入语义知识。整体架构包含五个模块：频率增强语言模块、变量间依赖模块、多视图文本语义融合模块、视觉-语言对比对齐模块和预测生成器。

在数值流中，输入序列先经过RevIN归一化，然后被切分为重叠补丁。每个补丁同时生成时域token和经Hann窗FFT变换后的频域token，通过可学习的交叉注意力将频域信息融合进时域表示，其中融合权重α初始化为零以避免干扰预训练知识。随后，这些token与可学习的[CLS] token一起送入共享的CLIP文本Transformer（不使用词嵌入层），得到时间表示和变量级摘要。

变量间依赖模块将每个变量的完整序列映射为token，并添加可学习的变量标识符，同样经过CLIP文本编码器获得跨变量上下文表示，再通过交叉注意力让时间摘要查询全局变量信息。

多视图文本语义融合是核心创新。它离线为每个变量构建多种文本描述（语义、行为、关系、时间模式），由CLIP文本编码器编码后缓存。变量级交叉注意力以时间表示为查询聚合这些文本视图，并通过可学习门控控制注入强度。同时，12维统计特征（分布、趋势、频谱等）通过独立的MLP旁路注入，避免占用注意力容量。此外还设计了文本对齐损失促使时间表示与文本嵌入一致。

视觉流仅在变量数不超过50时激活：将每个变量序列渲染为折线图，用冻结的CLIP视觉编码器编码，通过双向InfoNCE损失与时间表示进行对比对齐，并采用课程学习逐步增加难负样本浓度。该模块只在训练时生效。

最终，增强后的表示与补丁表示拼接，经两层MLP解码并反归一化输出预测。总损失为预测MSE加上两个对齐损失的加权和。

### Q4: 论文做了哪些实验？

实验在8个长期预测基准（ETTh1/ETTh2/ETTm1/ETTm2、ECL、Traffic、Weather、Exchange）和M4短期预测数据集上进行，lookback固定为96，预测长度涵盖{96,192,336,720}，M4覆盖6种频率共10万条序列。长期预测以MSE和MAE为指标，短期采用SMAPE、MASE和OWA。对比方法包括DLinear、TimesNet、PatchTST、FredFormer、iTransformer、Amplifier、DUET和SRSNet。

主要结果显示：SAGE在8个长期数据集中获得7个最佳平均MSE和6个最佳平均MAE，整体平均MSE为0.331，较iTransformer的0.345降低4.1%；在M4上以OWA 0.834全面领先（TimesNet为0.851）。消融实验表明：文本增强在31/32的组合中有效，平均MSE降低2.8%，其中+Stat模式最稳定（45.2%组合选为最优），Exchange上+Stat+Dyn取得6.3%最大提升；视觉对齐在6个适用数据集上平均带来1.6%的MSE降低，ETTm2增益最大（2.5%）。训练成本方面，单epoch从ETTh1的17秒到Traffic的290秒不等，完整651次运行约消耗1000单GPU小时。

### Q5: 有什么可以进一步探索的点？

SAGE的局限性为后续研究提供了多个切入点。首先，其文本生成依赖手工模板，缺乏端到端学习能力，未来可探索用小型语言模型蒸馏领域专家知识，自动生成更灵活、更具适应性的变量描述。其次，在高维数据集上文本增益减弱，说明逐变量独立门控机制可能无法有效捕捉变量间的相关性，可设计分组或层次化的门控结构，让相关通道共享文本表示，以提升可扩展性。第三，当前描述仅基于元数据和训练集统计，未纳入外部事件或本体知识，引入这些信息有望增强模型对由外部因素驱动的时序突变的建模能力。最后，SAGE目前主要面向单变量预测，扩展至多变量到多变量的生成任务及概率预测，将使其更贴近实际决策场景，同时也可探索将视觉监督从训练阶段推广到推理阶段，以进一步提升预测的鲁棒性。

### Q6: 总结一下论文的主要内容

SAGE提出了一种基于CLIP的视觉-语言时间序列预测框架，旨在解决传统数值序列缺乏语义知识的问题。该方法通过联合建模时间、跨变量、文本和视觉信息，利用CLIP文本编码器处理频率增强的补丁和变量令牌，并通过门控残差路径注入变量特定描述和统计特征；同时，冻结的视觉编码器通过训练期间的对比目标对齐渲染序列与时间表示。该框架无需在预测循环中引入大语言模型，避免了高计算成本。在八个长期基准和M4数据集上，SAGE取得了最优精度，消融实验证实了多模态对齐和变量级知识的互补增益。核心贡献在于设计了双用CLIP骨干、变量特定多视图知识注入和频率增强编码，实现了高效且可解释的预测。
