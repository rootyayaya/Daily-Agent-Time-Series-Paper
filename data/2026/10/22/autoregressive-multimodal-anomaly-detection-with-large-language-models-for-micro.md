---
title: "Autoregressive Multimodal Anomaly Detection with Large Language Models for Microservice Systems"
authors:
  - "Yixiang Tang"
  - "Fagui Liu"
  - "Guoxiang Zhong"
  - "Xi Yao"
  - "C. L. Philip Chen"
date: "2026-10-22"
arxiv_id: "2610.31722"
arxiv_url: "https://arxiv.org/abs/2610.31722"
pdf_url: "https://arxiv.org/pdf/2610.31722v1"
categories:
  - "cs.LG"
  - "cs.AI"
  - "cs.SE"
tags:
  - "多模态异常检测"
  - "微服务系统"
  - "LLM用于时序分析"
  - "自回归预测"
  - "模态特定重建"
  - "身份捷径问题"
  - "工业监控"
relevance_score: 6.5
---

# Autoregressive Multimodal Anomaly Detection with Large Language Models for Microservice Systems

## 原始摘要

Microservice systems have become a dominant architecture for large-scale cloud applications, enabling rapid deployment and elastic scaling. However, ensuring the reliability and availability of microservice systems critically relies on effective anomaly detection, as failures and performance anomalies can quickly propagate across services and severely impact end-to-end system behavior. Existing multimodal anomaly detection approaches for microservice systems often struggle with two fundamental limitations: (i) the neglect of modality-specific characteristics in favor of cross-modality fusion, and (ii) the "identity-shortcut" problem that affects the feature reconstruction process. To address these issues, we propose LLMMAD, an autoregressive multimodal anomaly detection framework for microservice systems based on Large Language Models (LLMs). Initially, to reconcile cross-modality fusion with modality-specific preservation, LLMMAD embeds and recombines multimodal data into a unified sequence for LLM processing to model inter-modality relationships, while employing modality-wise reconstruction heads to retain modality-specific information. Subsequently, to eliminate the identity-shortcut, we implement a prediction-driven autoregressive objective, under which the model predicts future states rather than copies current inputs. Finally, we conduct extensive experiments on three real-world datasets. The results demonstrate that LLMMAD consistently outperforms state-of-the-art methods, achieving F1-score improvements of 3.1%, 1.4%, and 0.9%, respectively, thereby providing a more reliable solution for microservice monitoring.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决微服务系统多模态异常检测中的两个核心问题。研究背景方面，微服务架构已成为大规模云应用的主流范式，但其分布式和动态特性使故障容易跨服务传播，因此及时准确的异常检测对保障系统可靠性至关重要。现有研究已从单模态转向融合指标、日志和追踪的多模态方法，以获得更全面的系统健康视图。然而，现有方法存在两方面不足：其一，过度关注跨模态融合而忽视模态特有信息，基于GNN的方法将各模态纠缠在一起，基于注意力、小波或拼接的融合方法也优先建模跨模态关系，导致仅在单一模态中显现的异常线索被忽略；其二，基于重建架构的无监督方法易受“身份捷径”问题影响，解码器无视语义直接复制输入，在多模态场景下因数据复杂度增加而更为严重，使模型难以产生有判别力的异常表示。本文的核心问题是：如何在保留各模态特有信息的同时建模跨模态关系，并消除身份捷径，从而构建更鲁棒、更准确的多模态异常检测框架。为此作者提出基于大语言模型的LLMMAD框架加以解决。

### Q2: 有哪些相关研究？

本文的相关工作主要可分为三类。方法类方面，跨模态知识迁移研究如One-Fits-All利用冻结预训练Transformer处理时间序列，OneLLM通过通用投影模块将八种异构模态对齐到语言表示空间，但均未涉及微服务系统中多模态数据的统一语言表示。基于重构的异常检测依赖正常数据可被忠实重构的假设，然而You等人系统分析了“身份捷径”问题，指出MLP、CNN、Transformer等架构在重构目标下易退化为恒等映射；现有缓解手段包括结构语义指令、记忆机制、迭代精炼、掩码重构和伪异常合成，但LLM作为重构器时因参数规模庞大仍易受此问题影响。应用类方面，DeepLog基于日志序列用LSTM做下一事件预测，Donut用VAE重构季节性KPI，TraceVAE用双变量图变分自编码器编码调用链结构与节点执行时间，但这些方法仅能检测单一模态中的异常。多模态融合类方面，MSTGAD构建以调用链为中心的图骨架并融入指标与日志特征，AnoFusion将各模态嵌入通道视为图节点并以互信息估计边权，Hades用模态特定提取器加跨模态注意力融合，FUSION在小波域序列化融合并用扩散网络建模。与上述工作不同，LLMMAD通过预测驱动的自回归目标解耦输入与重构目标以消除身份捷径，并采用模态特定重构头在融合的同时保留各模态特性。

### Q3: 论文如何解决这个问题？

LLMMAD 的核心思路是围绕“多模态统一建模 + 模态特性保留 + 预测式自回归”来重构异常检测流程。整体框架分为四个阶段：多模态数据时间对齐与归一化、嵌入层、基于 LLM 的融合与分离、模态级重建与异常评分。

首先，在数据层，论文将指标、日志和追踪三类监控数据统一对齐到固定滑动时间窗口：指标按采样点拼接为扩展时间序列，日志经模板解析后用 Word2Vec 得到模板嵌入并与二值出现矩阵相乘，追踪则按调用-被调用-操作组聚合时长统计量。随后采用多阶段归一化（对数压缩、常数缩放、基于中位数与 IQR 的鲁棒归一化）缓解指标尺度异质性。

其次，嵌入层由 1D CNN、线性投影和 LayerNorm 组成，将各模态映射到 LLM 的隐空间。LLM 主干冻结，仅保留位置嵌入和 Transformer 层，并引入 LoRA 进行高效微调，实现预训练语义空间与多模态嵌入的双向对齐。

关键创新在于“重组/逆重组”操作：重组将三个模态的嵌入沿时间轴交错排列成统一序列，使 LLM 能建模跨模态关系；逆重组在 LLM 输出后将其拆回各模态流，并整体偏移一个时间步以对应下一时刻预测。最后，三个独立的模态级重建头分别输出各模态的预测值，既保留模态特有信息，又避免跨模态融合淹没模态特性。

为消除“身份捷径”，训练采用预测驱动的自回归目标：第 t 步输出预测第 t+1 步输入，配合 decoder-only LLM 的因果掩码，模型只能依赖历史上下文，无法直接复制当前输入。总损失为三模态一步预测 MSE 之和。检测阶段仅预测窗口后部固定比例的时间步，异常分数超过阈值即触发告警。

### Q4: 论文做了哪些实验？

论文在三个真实微服务数据集上进行了实验：SN（SocialNetwork，9,870秒、12实例、7类指标、94,319条日志、1,438,191条span）、TT（TrainTicket，74,340秒、27实例、65,616条日志、158,238条span）和MSDS（OpenStack云系统并发请求部分，11,160秒、5实例、130,326条日志、1,514,358条span），分别注入CPU过载、网络延迟、丢包及容器重启、服务API故障、网络代理中断等故障。实验在八块NVIDIA Tesla V100的Linux服务器上用PyTorch实现，日志经Drain3解析并用skip-gram Word2Vec生成64维嵌入，骨干LLM为GPT-2（117M），结果取20次运行平均，阈值百分位在{0.999,0.995,0.99,0.98,0.95,0.90}中选取。实验围绕五个研究问题展开：RQ1检测准确性，与最先进方法对比，F1分数分别提升3.1%、1.4%和0.9%；RQ2消融分析各组件与模态贡献；RQ3评估参数规模与时间开销效率；RQ4验证对“identity shortcut”问题的缓解效果；RQ5考察不同LLM骨干与超参数下的鲁棒性。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点。其一，实验仅采用GPT-2（117M）作为骨干，虽在RQ5考察了不同LLM骨干的鲁棒性，但对更大规模或领域专用模型的适配性、推理成本与检测精度的权衡仍缺乏系统分析，未来可探索轻量化蒸馏或参数高效微调以降低部署开销。其二，数据集仅覆盖三种基准系统和有限故障类型（CPU过载、网络延迟、丢包等），对级联故障、慢故障演化及跨系统迁移场景的泛化能力尚不明确，可引入在线增量学习与少样本异常检测。其三，预测式自回归目标虽缓解identity-shortcut，但预测步长与多步误差累积对检测灵敏度的影响值得研究，可结合不确定性建模或对比学习增强对微弱异常的敏感性。其四，当前仅输出异常分数，缺乏根因定位与可解释性，未来可将LLM的推理能力用于故障传播链分析与自然语言解释生成，提升运维实用性。

### Q6: 总结一下论文的主要内容

论文针对微服务系统异常检测中现有多模态方法的两大缺陷展开研究：一是过度关注跨模态融合而忽视各模态自身特征，二是基于重构的无监督方法易陷入“恒等捷径”问题，即解码器直接复制输入而丧失对异常模式的判别力。为此，作者提出LLMMAD框架：先将指标、日志、链路三类模态数据做时间对齐与归一化，经嵌入层映射后按时间交错重组为统一序列，输入参数冻结、经LoRA微调的LLM建模跨模态关系；再通过逆重组将输出拆回各模态，由独立的模态级重构头保留模态特有信息；同时采用预测驱动的自回归目标，利用因果掩码让模型预测下一时刻状态而非复制当前输入，从根本上消除恒等捷径。在三个真实数据集上的实验表明，LLMMAD持续优于现有最先进方法，F1分数分别提升3.1%、1.4%和0.9%，为微服务监控提供了更可靠的方案。
