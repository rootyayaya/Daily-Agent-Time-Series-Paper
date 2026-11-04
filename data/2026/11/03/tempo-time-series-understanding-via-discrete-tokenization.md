---
title: "TEMPO: Time Series Understanding via Discrete Tokenization"
authors:
  - "Riccardo Maggioni"
date: "2026-11-03"
arxiv_id: "2611.04482"
arxiv_url: "https://arxiv.org/abs/2611.04482"
pdf_url: "https://arxiv.org/pdf/2611.04482v1"
categories:
  - "cs.CL"
tags:
  - "时间序列理解"
  - "离散标记化"
  - "LLM接口"
  - "轴承故障诊断"
  - "信号到文本"
  - "有限标量量化"
  - "DoRA适配器"
  - "多模态时序"
  - "工业诊断"
relevance_score: 7.5
---

# TEMPO: Time Series Understanding via Discrete Tokenization

## 原始摘要

Time-series interpretation often requires both numerical observations and textual context. Integrating these inputs into a pretrained language model raises a representation question: how should a signal enter the model's token sequence? We present TEMPO, which extends an LLM's vocabulary with discrete codes from a context-aware Transformer tokenizer using finite scalar quantization. A frozen tokenizer maps four-step patches to a 625-code vocabulary; signal tokens, scale statistics, and text are then processed by the LLM's existing self-attention layers. Adaptation updates the new token embeddings and DoRA adapters. With a Qwen3-4B backbone and task-specific fine-tuning, TEMPO achieves macro-F1 scores of 89.0% on activity recognition, 85.0% on sleep staging, and 86.0% on bearing-fault diagnosis. Time-series question answering and qualitative bearing-diagnosis examples further illustrate how this interface combines signal representations with textual context. Together, these results demonstrate the utility of discrete vocabulary extension for time-series understanding.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是如何让预训练大语言模型（LLM）直接“理解”时间序列信号，从而把数值观测与文本上下文（运行工况、维护历史、用户提问）统一到同一个模型中处理。研究背景在于：时间序列记录系统演化，而文本描述其解释条件，例如同一段振动信号在调试期与常规运行期的含义可能不同，因此解读往往需要二者结合。现有方法的不足体现在两方面：任务专用分类器虽能给出预测，但输出接口通常是固定标签集，缺乏自然语言交互与解释能力；而将信号接入LLM的既有途径——数值文本序列化、连续编码器嵌入、学习式离散token——在序列长度、表示形式和与语言模型的融合方式上各有折衷，难以兼顾上下文感知与统一建模。本文要解决的核心问题是：信号应以何种表示进入LLM的token序列。为此提出TEMPO，用上下文感知的Transformer分词器经有限标量量化把四步patch映射为625个离散码，扩展LLM词表，使信号token与文本共享同一自注意力层，并以通道均值、标准差作为文本保留尺度信息，再通过新嵌入与DoRA适配器完成两阶段适配，在活动识别、睡眠分期、轴承故障诊断与时间序列问答上验证该离散接口的有效性。

### Q2: 有哪些相关研究？

主要相关研究可分为三类。方法类方面，时间序列基础模型如Chronos通过对标量值量化实现基于token的预测，TimesFM和Moirai构建预训练预测模型，Mantis学习分类表示，但它们主要输出预测、分类或嵌入，不涉及与自然语言问题的融合。信号与LLM集成方面，ChatTS、OpenTSLM、TsLLM和ITFormer通过连续表示（软提示或交叉注意力）连接时间序列编码器与语言模型；离散方法包括Chat-TS的标量分箱和TokenCast的学习向量量化表示；TempoGPT与本文最接近，量化时间嵌入并在时间与文本token间共享嵌入层。本文区别在于采用带全局注意力的Transformer编码器使每个patch表示依赖上下文，再用有限标量量化（FSQ）映射到固定标量网格，并结合直接词表扩展与分阶段LLM适配。应用与评测类方面，FactoryBench评估LLM对工业机器人遥测的推理，发现前沿模型在结构化层级和决策任务上表现不佳，凸显工业时间序列推理的困难，这正是TEMPO面向信号与文本上下文结合接口的动机所在。

### Q3: 论文如何解决这个问题？

TEMPO 的核心思路是把时间序列“翻译”成 LLM 词表中的离散 token，从而让信号与文本在同一自注意力序列中自然融合，而无需为信号设计新的注意力或门控模块。

整体框架由三部分组成：一个独立训练且全程冻结的信号 tokenizer、扩展后的 LLM 词表、以及两阶段适配流程。预处理阶段对每个通道做均值-标准差归一化，并把均值、标准差等尺度统计量写入文本上下文，从而在保留形状表示的同时不丢失绝对尺度信息。

关键技术是上下文感知的离散 tokenization。tokenizer 将归一化后的单通道信号切成不重叠的 4 步 patch，投影到 128 维后经四层 Transformer 编码器做全局自注意力，再投影到 4 维潜变量，并用有限标量量化（FSQ）将每一维量化为 5 个等级，隐式构成 5^4=625 个码字的词表。由于编码器使用全局自注意力，同一 patch 可根据周围信号获得不同表示，优于独立标量分箱和感受野受限的卷积编码器。tokenizer 通过对称 Transformer 解码器以重构、多尺度频谱和时间平滑损失预训练，之后保持冻结。

词表扩展方面，向 LLM 加入 625 个信号码和 <ts_start>、<ts_end> 两个定界符，新嵌入按现有嵌入的平均范数随机初始化，并用梯度掩码只更新新条目。Stage 0 仅训练这 627 个新嵌入，混合判别任务、掩码码预测和 M4 描述，使离散信号词表对齐到语言模型表示空间；Stage 1 联合更新新嵌入与 DoRA 适配器（rank=32），并混入约 5 万条纯文本指令以缓解语言遗忘。最后按领域做任务特定微调。创新点在于用 FSQ 离散码扩展词表、以尺度统计量保留数值信息，并用冻结 tokenizer 加轻量适配实现多任务时间序列理解。

### Q4: 论文做了哪些实验？

论文围绕离散词表扩展的时间序列理解框架TEMPO开展了多组实验。实验以Qwen3-4B为骨干，先在领域训练集上微调Stage 1检查点，再在留出测试集上评估。任务包括HAR活动识别、睡眠分期、轴承故障诊断（均用macro-F1）、TSAQA分类与异常检测（用准确率），以及Time-MQA迁移测试。对比方法涵盖专用分类器（随机森林、AttnSleep、WDCNN）、文本序列化基线（GPT-4o零样本、LLaMA3.1-8B微调）、软提示与Flamingo交叉注意力（Llama3.2-3B）。主要结果：TEMPO在HAR达89.0%、睡眠分期85.0%、轴承诊断86.0%，均超过OpenTSLM的SoftPrompt（64.87%/54.40%）和Flamingo（62.77%/45.45%）；但专用模型在两项任务上更优（随机森林HAR 96.0%，WDCNN轴承99.2%）。TSAQA上分类80.5%、异常检测91.3%，与8B LLaMA3.1基线（91.3%/91.0%）异常检测相当而分类落后。Time-MQA上1.7B模型分类62%，高于Qwen-2.5-7B的52%和GPT-4o的32%，但异常检测与判断分数较低。此外还分析了625个码字的激活分布（归一化熵0.889）及轴承诊断的定性案例。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要有两点：一是有限标量量化在压缩率与时间细节之间形成权衡，四步patch、625码本的离散化可能丢失细粒度瞬态特征，对短时冲击类故障或高频振荡信号不够敏感；二是各通道独立token化导致序列长度随通道数线性增长，多传感器场景下计算与显存开销显著。未来可探索通道感知的压缩方案，例如跨通道共享码本、通道注意力聚合或可学习的通道合并，将多变量信号压缩为定长token序列。其次，当前tokenizer与LLM主干均冻结，仅训练新嵌入和DoRA适配器，可尝试轻量联合微调tokenizer编码器以提升域适应能力。此外，可引入多尺度patch或残差量化，用分层码本兼顾粗粒度趋势与细粒度细节，缓解量化损失。评估上可扩展到FactoryBench中的干预、反事实与决策类工业问答，检验模型在因果推理与操作建议上的能力；也可探索跨域迁移与少样本适配，以及将离散码与文本统计之外的物理先验（如频谱、包络）结合，增强可解释性。

### Q6: 总结一下论文的主要内容

论文针对如何将时间序列信号接入预训练语言模型这一表示问题，提出 TEMPO 框架。其核心思路是扩展 LLM 词表：用一个上下文感知的 Transformer 分词器，经有限标量量化（FSQ）将四步一组的信号片段映射为 625 个离散码，作为新词元与文本、通道均值/标准差统计量共同进入同一自注意力序列。适配分两阶段：Stage 0 仅训练新增的 627 个嵌入以对齐语言模型表示空间；Stage 1 联合更新新嵌入与 DoRA 适配器，分词器与基座权重保持冻结。在 Qwen3-4B 上，TEMPO 在活动识别、睡眠分期和轴承故障诊断上分别取得 89.0%、85.0% 和 86.0% 的 macro-F1，优于同规模软提示与交叉注意力方案，并支持时间序列问答及依赖工况上下文的定性诊断。结果表明，离散词表扩展是一种紧凑有效的时间序列理解接口，但其精度仍落后于专用分类器。
