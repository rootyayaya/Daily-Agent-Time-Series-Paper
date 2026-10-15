---
title: "Text-Informed Training Data Filtering for Enhanced Virtual Flow Meter Performance"
authors:
  - "Kristoffer Hjelmen Nesland"
  - "Bjarne Grimstad"
  - "Antorweep Chakravorty"
  - "Dan Sui"
date: "2026-10-14"
arxiv_id: "2610.19860"
arxiv_url: "https://arxiv.org/abs/2610.19860"
pdf_url: "https://arxiv.org/pdf/2610.19860v1"
categories:
  - "stat.ML"
  - "cs.LG"
tags:
  - "LLM"
  - "多模态融合"
  - "异常检测"
  - "工业传感器"
  - "数据过滤"
  - "虚拟流量计"
  - "软测量"
  - "文本信息"
  - "训练数据质量"
  - "预测性维护"
relevance_score: 7.5
---

# Text-Informed Training Data Filtering for Enhanced Virtual Flow Meter Performance

## 原始摘要

In sectors such as energy, aquaculture and chemical processing, the effectiveness of both mechanistic and data-driven models is frequently limited by poor-quality training data, which obscures underlying physical laws and degrades predictive accuracy. Such quality issues commonly manifest as anomalies in the dataset, ranging from sensor faults to process upsets and incorrect operator inputs. While traditional rule-based filtering can remove a subset of the anomalies, it is unable to leverage contextual information stored as unstructured text, such as engineer comments and operational logs that explain under what conditions the data was collected. We propose a text-informed data filtering method that leverages large language models (LLMs) to integrate unstructured operational data with tabular sensor data. The method consists of two steps: (1) contextual anomaly detection by reasoning over both data modalities, and (2) generation of a binary mask that is applied to filter the training dataset for model development. To investigate the potential benefit, a steady-state soft-sensor regression model, namely a virtual flow meter that estimates well flow rates, is used as the downstream evaluation target. Experiments on a synthetic oil and gas dataset show improved model performance compared to traditional rule-based filtering. Ablation studies show that textual operator comments can provide filtering-relevant signals beyond sensor data alone, with the multimodal approach reducing downstream MAPE from 7.1% to 5.4% relative to sensor-only filtering. This work demonstrates that integrating unstructured operational knowledge with sensor data through LLMs can improve data quality for industrial machine learning applications, offering a scalable alternative to manual data curation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在能源、水产养殖和化工等行业，机理模型与数据驱动模型的效果常受限于训练数据质量。传感器故障、过程扰动和操作员误输入等异常会掩盖潜在物理规律，降低预测精度。传统基于规则的过滤虽能剔除部分异常，却无法利用工程师注释、操作日志等非结构化文本中蕴含的上下文信息——这些文本恰恰解释了数据采集时的工况条件。现有异常检测方法多为单模态，仅依赖传感器数据，而工业异常往往是上下文相关的：一个在历史统计范围内看似正常的读数，若当时设备正发生仪表故障，仍属不可靠数据。因此，仅凭传感器统计特性不足以识别此类异常。本文要解决的核心问题是：给定配对的传感器测量与操作员注释数据集，如何判断哪些数据点应被标记为异常并在模型训练前剔除。作者将其形式化为为每个数据点分配二值权重（1表示保留，0表示排除），并提出文本知情的数据过滤方法，利用大语言模型联合推理表格化传感器数据与非结构化操作注释，先进行上下文异常检测，再生成二值掩码过滤训练集，最终以虚拟流量计这一软测量回归模型作为下游评估目标。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，Brown等人证明大语言模型具备广泛的少样本学习能力，后续工作将其扩展至表格数据分类与表格异常检测；Wu等人进一步提出多模态上下文异常检测，在单一LLM上下文中融合结构化与非结构化输入。本文与这些工作的区别在于，它们的目标是异常分类本身，而本文聚焦工业模型训练的数据质量过滤，以提升下游预测性能为最终目标。应用类方面，Souza等人综述了基于回归的软传感器方法，用于估计难以直接测量的过程变量；在油气领域，基于神经网络的虚拟流量计已在多种井配置下展现良好性能。但这类模型的预测质量高度依赖训练数据，而系统性数据过滤对下游软传感器性能的影响此前鲜有研究。评测类方面，本文以简单软传感器模型作为下游评估目标，使各过滤策略的影响可直接量化，并通过消融实验验证文本操作员注释能提供传感器数据之外的过滤信号，从而填补了上述空白。

### Q3: 论文如何解决这个问题？

论文提出一种文本知情的数据过滤方法，利用大语言模型将非结构化运维文本与表格化传感器数据融合，为每个数据点生成二值权重，从而在训练虚拟流量计前剔除异常样本。整体框架分为两步：第一步进行上下文异常检测，LLM 同时推理传感器测量值与工程师评论；第二步生成二值掩码，应用于训练集过滤，随后用加权回归目标拟合下游软测量模型。

核心方法上，对每口井的数据集，目标是确定权重向量，权重为1表示保留、为0表示剔除。LLM 过滤函数以系统指令、参考数据集和目标数据集为输入，独立作用于每口训练井，无需梯度训练，完全依赖上下文学习。提示词包含四部分：任务描述、特征字典、带已知权重的参考数据集作为少样本示例、以及待预测的目标数据集。数据以 JSON 数组呈现，每条记录含输入对象（传感器值与评论）和输出对象（待预测权重）。LLM 返回结构化 JSON，每个数据点包含二值权重和简短自然语言推理。特征字典用于解释领域缩写字段的物理含义与单位，使模型能调用预训练领域知识。

创新点在于：首次将工程师评论、操作日志等非结构化文本通过 LLM 与传感器数据联合推理，突破传统规则过滤无法利用上下文信息的局限；采用少样本上下文学习而非微调，具备可扩展性；通过消融实验验证文本模态提供传感器之外的过滤信号，多模态方法将下游 MAPE 从仅传感器过滤的7.1%降至5.4%。

### Q4: 论文做了哪些实验？

论文在合成油气数据集上开展实验，以稳态软测量回归模型（虚拟流量计，估计油井流量）作为下游评估目标。评估指标为MAPE、MSE和预测值落在真实值10%范围内的比例W10，采用10,000次重采样的百分位自助法计算95%置信区间。对比方法包括：无过滤（Uniform）、经典规则过滤（Tukey、Mahalanobis）、多模态LLM过滤（Claude Sonnet 4.6，每口井独立运行3次）、纯文本LLM、纯传感器LLM、LLM+Tukey、LLM+Mahalanobis，以及Oracle（真实标签）作为参考上界。主要结果：无过滤最差（MSE 148，MAPE 12.5%，W10 51%）；经典方法中Mahalanobis的MAPE最低（9.4%），Tukey的MSE最低（112）；多模态LLM全面优于经典方法（MSE 53，MAPE 5.4%，W10 87%），置信区间无重叠。消融显示文本信息有独立贡献：相比纯传感器LLM，MAPE从7.1%降至5.4%，MSE从88降至53，W10从84%升至87%。LLM+Mahalanobis表现最佳（MSE 47，MAPE 5.1%，W10 89%），接近Oracle（MSE 36，MAPE 4.1%，W10 90%）。稳定性分析显示纯文本LLM运行间一致率100%，纯传感器仅92.7%，多模态为96.6%。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点。首先，实验仅基于13口井的合成数据集，且文本信息量是按真实资产人为校准的，未来需在真实工业数据上验证泛化性，并研究文本收益对参考数据规模与构成的敏感性。其次，研究仅使用单一LLM（Claude Sonnet 4.6），不同模型的过滤决策与下游指标可能差异显著，值得开展跨模型对比与鲁棒性分析。第三，时间依赖性问题尚未解决，尤其是文本信息在异常评估中的有效期限，可探索带时间衰减的文本权重机制。第四，可解释性不足，需进一步量化传感器数据与文本各自的相对重要性。此外，LLM方法存在推理延迟高、非确定性、依赖专有模型带来的隐私与可用性风险，未来可研究轻量级本地模型或蒸馏方案，以适配延迟敏感与安全受限的工业场景。

### Q6: 总结一下论文的主要内容

本文针对工业场景中训练数据质量差、异常难以识别的问题，提出一种文本信息驱动的数据过滤方法。传统规则过滤仅依赖传感器数值，无法利用工程师注释、操作日志等非结构化文本中蕴含的上下文信息。作者将问题定义为：给定传感器测量与操作员注释配对的数据集，为每个数据点分配二值权重，决定其是否进入模型训练。方法上，利用大语言模型联合推理表格型传感器数据与非结构化文本，通过少样本上下文学习生成异常判定及简要理由，进而构造二值掩码过滤训练集。在合成油气数据集上，以虚拟流量计软测量为下游任务，多模态过滤将MAPE从仅传感器过滤的7.1%降至5.4%，优于Tukey和Mahalanobis等传统方法。消融实验表明，文本注释携带传感器数据之外的过滤信号，多模态联合推理可显著提升工业机器学习的数据质量。
