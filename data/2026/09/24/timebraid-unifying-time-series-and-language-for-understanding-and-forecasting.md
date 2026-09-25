---
title: "TimeBraid: Unifying Time Series and Language for Understanding and Forecasting"
authors:
  - "Xinyue Wang"
  - "Jiacheng Pang"
  - "Kun Zhou"
  - "Kexin Zhang"
  - "Defu Cao"
  - "Fan Feng"
  - " Faisal"
  - "Songyao Jin"
  - "Yan Liu"
  - "Biwei Huang"
date: "2026-09-24"
arxiv_id: "2609.29792"
arxiv_url: "https://arxiv.org/abs/2609.29792"
pdf_url: "https://arxiv.org/pdf/2609.29792v1"
categories:
  - "cs.CL"
  - "cs.AI"
  - "cs.CE"
tags:
  - "时间序列与语言统一建模"
  - "时序基础模型"
  - "LLM"
  - "多模态对齐"
  - "零样本预测"
  - "指令微调"
  - "时序理解与推理"
  - "语义报告生成"
relevance_score: 7.5
---

# TimeBraid: Unifying Time Series and Language for Understanding and Forecasting

## 原始摘要

We present TimeBraid, a series of unified time-series and language models that align pretrained language models and pretrained time-series foundation models through interleaved global residual attention layers. Each model inherits knowledge, instruction following, and reasoning from one side, continuous-signal perception and zero-shot forecasting from the other, and fuses the two in a shared representation space where both modalities are understood and generated. We study the design choices that make such unified modeling work: where to align the two representation spaces, how to ground language in temporal structure, how to balance understanding with generation, and how to keep joint optimization stable. The resulting recipe combines a unified prompting scheme for diverse time-series and text tasks, stabilized joint training, and supervision from 2.2M curated series--text pairs and 4.9M instruction-tuning samples. Across benchmarks spanning time-series perception, understanding, reasoning, and both context-aided and unimodal forecasting, TimeBraid remains competitive with far larger general-purpose models and task-specific counterparts.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列数据广泛存在于生理、电力、金融、气候等领域，但其数值记录本身缺乏语义上下文，难以被识别和解释。语言可以为时间序列提供语义锚定，将其与更广阔的世界知识连接起来，因此将时间序列纳入统一多模态模型具有重要意义。然而，现有连接时间序列与语言的方法通常是在预训练语言模型或时间序列模型上附加专门组件，如投影层或信号分词器。这类做法会引入表征鸿沟，导致语义错位，并损害预训练模型原有的能力；同时，每个系统往往只覆盖时间序列—语言双向接口的某一片段。因此，如何在基本保留两个预训练宿主模型能力的前提下，对齐它们的原生表征，仍是一个尚未充分探索的问题。本文提出TimeBraid，试图在单一模型权重中统一时间序列与语言的理解与生成。其核心挑战在于：连续信号与离散语言之间存在固有语义鸿沟，对齐需要大规模配对预训练，并且要平衡理解与生成、保持联合优化稳定。TimeBraid通过交错全局残差注意力连接预训练语言模型与预训练时间序列基础模型，在共享表征空间中融合两种模态，从而同时获得语言侧的指令遵循与推理能力，以及时间序列侧的连续信号感知与零样本预测能力。

### Q2: 有哪些相关研究？

现有研究大致可分为三类。方法类方面，早期多模态系统采用“组合式”工作流，将分别训练的模态专用模块拼接；统一多模态模型则尝试在单一权重内学习共享表示以理解与生成异构信号，但时间序列长期被排除在外。连接时间序列与语言的工作通常通过投影层或信号分词器等专用组件，将时间序列接入预训练语言模型或时间序列基础模型，然而这些组件引入表示鸿沟，导致语义错位并损害预训练能力，且每个系统仅覆盖双向接口的片段。应用与评测类方面，已有 TSAQA、Time-MMD、GIFT-Eval、CaTS-Bench、CGTSF 等基准，分别考察时间序列问答、多域预测、零样本预测、描述生成与条件预测，但多由任务专用模型或通用大模型分别应对。本文与上述工作的区别在于：TimeBraid 不添加外部分词器，而是用交错全局残差注意力对齐语言与时间序列两个预训练宿主，保留各自能力并实现双向理解与生成，同时以 2.2M 序列—文本对和 4.9M 指令样本进行两阶段联合训练，在十二个基准上同时覆盖感知、理解、推理与预测。

### Q3: 论文如何解决这个问题？

TimeBraid 的核心思路是通过“交错全局残差注意力”将预训练语言模型与预训练时间序列基础模型对齐，从而在共享表示空间中统一理解与生成两种模态。整体架构采用 Mixture-of-Transformers（MoT）的“三专家”设计：感知专家编码上下文时间序列片段，推理专家处理文本指令与语言响应，预测专家生成目标时间序列片段。三个专家分别用对应的预训练模型初始化，其中感知与预测专家可共享同一底层模型（双塔），也可解耦为三塔。

关键创新在于全局残差注意力层。由于时间序列塔层数少于语言塔，其每层与一个语言层配对并均匀交错，未配对的剩余语言层仅处理自身 token。在每个配对层，两个塔先各自经过原生块得到隐藏状态，再通过流特定的 RMSNorm 和线性投影映射到共享注意力空间，按时间线位置 τ 重排为单一全局序列，在因果掩码下联合注意力，最后将输出路由回各自位置。输出投影零初始化，使全局层初始为恒等映射，保证训练稳定。位置编码采用解耦设计：语言塔用 RoPE，时间序列塔用段内原生位置，残差注意力用全局有序位置 τ 上的 RoPE。

训练上采用两阶段课程：第一阶段用 2.23M 配对数据做对齐，覆盖形态描述、上下文描述、可编程描述及可控预测；第二阶段用 4.88M 异构指令数据做监督微调。联合损失为文本交叉熵与时间序列多 patch 预测损失之和，后者包含点回归与分位数 pinball 损失。为稳定联合优化，引入 asinh 鲁棒归一化和损失封顶，抑制非平稳段回归损失尖峰对语言学习的干扰。推理时还提供文本强度调制，通过插值 λ 控制文本条件对预测的影响。

### Q4: 论文做了哪些实验？

论文围绕时间序列理解与预测开展了系统实验。实验设置覆盖感知、问答与推理、上下文描述、上下文/受控/单模态预测等任务，对比对象包括通用语言模型、视觉-语言模型、专用时间序列模型和统一模型。数据集与基准包括TSAQA、TimeSeriesExam、TemporalBench MCQ、CaTS-Bench、TimeMMD、CGTSF以及自建的Ctrl-F受控预测集。主要结果：TimeBraid-6.7B在TSAQA总体准确率达80.65%，TimeSeriesExam达63.14%，TB-MCQ达36.58%，均优于GPT-5.4的63.10%、67.83%和38.50%中的部分指标；在CaTS-Bench上SimCSE达0.886为最佳，DeBERTa-F1为0.712；在CGTSF上取得最佳Macro MSE与MAE，TimeMMD九个域中八个进入前三；Ctrl-F上Top-1准确率43.33%，显著高于33.33%随机水平。

### Q5: 有什么可以进一步探索的点？

TimeBraid 的主要局限在于：其一，模型规模仍受限于 1.2B–6.7B，与前沿通用大模型相比在复杂推理上仍有差距；其二，依赖 2.2M 配对数据与 4.9M 指令样本，而高质量时序-文本配对数据稀缺，跨领域泛化可能受限；其三，全局残差注意力虽保留预训练能力，但长序列下的计算开销与对齐稳定性仍是隐患。未来可探索的方向包括：引入更多模态（如事件日志、图结构）形成真正的多感官时序理解；设计自适应对齐机制，按任务动态调节时序与语言的融合权重；研究无配对或弱配对场景下的自监督跨模态对齐，降低数据依赖；以及将 TimeBraid 扩展到在线、流式与因果推断场景，验证其在真实工业闭环中的鲁棒性。此外，可解释性——让模型显式输出时序证据链——也是值得深入的方向。

### Q6: 总结一下论文的主要内容

TimeBraid提出了一系列统一的时序与语言模型，旨在打通连续信号与离散语言之间的表示鸿沟。问题定义上，现有方法多通过投影层或信号分词器拼接模态，导致语义错位并损害预训练能力。方法上，TimeBraid采用混合Transformer架构，将预训练语言模型与时序基础模型通过全局残差注意力层对齐，在共享表示空间中实现双向理解与生成；并设计两阶段训练配方，先在大规模配对数据上对齐，再以异构指令数据微调，同时引入稳健归一化与损失封顶稳定联合优化。主要结论显示，在十二项理解与预测基准上，1.2B至6.7B参数的TimeBraid在TSAQA达80.65%，超越GPT-5.4，并在上下文预测与零样本预测中保持竞争力，验证了共享注意力空间与对齐阶段的关键作用。
