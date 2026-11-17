---
title: "Language Models Meet Vibration Testing for LEO Constellation Satellites with Calibrated Response Prediction from Few-show Sweeps"
authors:
  - "Jun Wu"
  - "Deming Li"
  - "Zhenming Zheng"
  - "Honghao Yue"
  - "Fei Yang"
  - "Hao Sun"
date: "2026-11-16"
arxiv_id: "2611.20579"
arxiv_url: "https://arxiv.org/abs/2611.20579"
pdf_url: "https://arxiv.org/pdf/2611.20579v1"
categories:
  - "cs.CL"
  - "cs.AI"
  - "cs.LG"
tags:
  - "LLM-driven engineering analysis"
  - "deterministic validation gates"
  - "hallucination detection"
  - "structured information extraction"
  - "vibration testing"
  - "calibrated response prediction"
  - "conformal prediction"
  - "industrial fault diagnosis"
relevance_score: 8.5
---

# Language Models Meet Vibration Testing for LEO Constellation Satellites with Calibrated Response Prediction from Few-show Sweeps

## 原始摘要

Large language models (LLMs) increasingly drive engineering analysis end to end, turning textual records into the inputs of numerical programs, but a plausible and wrong value can pass silently into a decision. We propose deterministic validation gates for LLM-driven engineering analysis, a general paradigm in which a typed configuration produced by LLMs is consumed only after it passes deterministic checks on units, physical consistency, verbatim quotes, agreement between independent models, consistency with measurement exports and the applicability of trained models. The gates target hallucinations from two directions, since quote checking catches fabricated content while agreement between models catches errors of omission that quote checking misses. We instantiate the paradigm on sine vibration acceptance testing for low Earth orbit mega-constellation satellites, where DeepSeek V4.1 Flash and Qwen-plus read Chinese test records and extract a configuration of 76 fields. Fact-level F1 ranged from 0.98 to 1.0 on five input variants, with all repairs frozen on development inputs and evaluated on held-out inputs. With all gates, 20 of 20 configurations produced notching results bit for bit identical to the gold run, and all 17 real and injected errors in consumed fields were stopped, of which 16 would have run without gates. Retraining the bound model on a dataset built from an LLM configuration reproduced its results within GPU nondeterminism. We also report a negative result of practical value. Direct LLM curve forecasting only matches linear extrapolation, whereas a small physics-structured network reduces the over-notched bandwidth by 86% to 89% at calibrated coverage c = 0.90, which delineates where direct LLM prediction should give way to a trained model.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文针对的是 LLM 在工程分析端到端流程中的一个关键风险：LLM 从文本记录中提取的数值或配置可能看似合理但实际错误，并且这种错误会静默地传入下游数值程序，导致错误的工程决策。作者以低轨巨型星座卫星的正弦振动验收测试为具体场景，其中测试条件（输入剖面、响应限值、运行序列、控制方案、传感器列表等）以中文文本记录形式存在，需要被提取为结构化配置来驱动数值分析（如陷波决策）。传统上这些条件由人工编码，但人工编码存在错误且难以扩展。论文旨在设计一种通用范式，通过确定性的验证门（validation gates）来确保 LLM 输出的配置在被数值阶段消费之前经过严格检查，从而消除静默错误，同时保持低误停率。此外，论文还探究了 LLM 是否可以直接用于曲线预测（负结果），并对比了物理结构化网络与线性外推的性能，明确了 LLM 在数值预测任务中的边界。

### Q2: 有哪些相关研究？

相关工作主要分为四个方向：1）LLM 结构化提取：LLM 已用于从科学文本中提取实体、关系和记录，如基于 schema 的提示提取、生成式信息抽取综述，以及飞机维护记录处理；输出格式可通过语法约束解码或 JSON 模式强制。2）LLM 驱动工具：通过交错推理与行动、学习调用工具、委托计算给解释器，LLM 可控制外部程序；在化学领域，LLM 连接专家工具规划合成并运行实验。这些系统让模型控制工作流，而本文保持工作流固定且确定性，仅让模型提供配置并接受检查。3）幻觉与验证：基于采样的一致性检查可检测幻觉内容，跨样本一致性提升推理，计划验证问题减少幻觉；本文的门使用逐字引用、第二模型、测量文件和物理约束。4）LLM 用于数值与校准代理：LLM 可将数值序列写作文本进行预测（如 LLMTime），但消融实验发现移除 LLM 往往不损害性能；虚拟振动台模型预测正弦测试响应，关节结构展示非线性幅值依赖动力学；结构振动响应已用神经网络和神经算子预测，保形预测提供覆盖保证。本文在这些基础上，将 LLM 定位为配置提取器而非数值预测器，并用确定性门确保可靠性。

### Q3: 论文如何解决这个问题？

论文提出“确定性验证门”范式：LLM 从中文测试记录中提取一个包含 76 个字段的类型化配置（32 个数值、19 个类别、25 个列表），然后该配置必须通过六个确定性门才能被数值阶段消费。门 G1 检查单位解析与转换（如 m/s² 转 g，峰峰值转零峰值），保留源精度；G2 检查物理合理性（如剖面连续性、响应限值在输入电平的 1-20 倍之间、运行列表以低电平扫描开始和结束）；G3 使用逐字引用验证器检查证据模式输出中的引用是否在原文中逐字出现且数值一致；G4 比较两个独立模型（DeepSeek V4.1 Flash 和 Qwen-plus）对同一输入的提取结果；G5 将字段与测量导出文件中的事实（如控制谱、限值标记、验收文件数量、轴顺序）进行一致性检查；G6 检查训练模型的适用性（频带和电平在训练范围内 2% 以内）。决策策略包括宽松、共识（默认）和严格：共识策略要求 G4 通过，当模型分歧时以通过 G5 且引用不矛盾的值优先。此外，还设计了两种修复：阶段 A 扩展引用验证器处理省略引用（省略号分隔的片段需按序逐字出现）；阶段 B 对仍失败的消费字段，用仅包含相关文本块的模板重新询问同一模型。门和修复均不接触金标准。数值阶段根据配置选择文件、排序运行、计算传递率、评估输入剖面、构建数据集，并复用已训练的 WarpNet-CQR 模型进行陷波决策。最后，可选地由 LLM 生成陷波摘要，但摘要不参与决策，且有一个检查器验证摘要中每个数字的归属。

### Q4: 论文做了哪些实验？

实验围绕提取准确性和端到端驱动结果展开。提取实验使用五种输入变体（精选摘录、分块摘录、完整记录、布局扰动、单位与措辞扰动），比较 DeepSeek V4.1 Flash、Qwen-plus 和基于规则基线在 224 个原子事实上的表现。DeepSeek 的 F1 在 0.991-1.000 之间，精确率均为 1.0；Qwen-plus 的 F1 在 0.980-0.998 之间；规则基线在布局扰动下 F1 骤降至 0.126。错误分类显示 DeepSeek 的错误均为传感器方向列表的缺失元素（审计字段），Qwen-plus 的错误包括将 65g 响应限值误作中止阈值、轴顺序错误和角色混淆。证据接地实验（E1）通过引用验证将精确率提升至 1.0（Qwen-plus 在所有输入上），但召回率下降（如 Qwen-plus 降至 0.915）。跨模型检查（E2）中 DeepSeek 标记了 Qwen-plus 7 个已知错误中的 5 个且无误报，反向检查则标记 0 个且误报 13 个。重复运行（E3）显示温度 0 下 API 输出仍非确定性，Qwen-plus 在 76 个字段中有 1-2 个不一致。端到端实验比较了 20 个 LLM 配置（2 模型×5 输入×2 模式）在五个管道版本下的驱动结果：无门（v0）时 16 个完全一致、1 个静默错误；最终版本（v3 加修复 A/B 和共识策略）下 20 个全部与金标准逐位一致，无静默错误，8 次升级均为审计字段标记。注入 19 个错误（16 个消费字段、3 个审计字段）测试门策略：共识策略下所有 16 个消费错误被停止，3 个审计错误被标记；宽松策略无 G5 时放过 2 个遗漏错误。数值预测探针中，LLM 直接预测曲线仅与线性外推相当（logRMSE 0.104-0.187 vs 0.102-0.186），而 WarpNet-CQR 达到 0.085-0.155，且在 c=0.90 时过陷波带宽减少 86%-89%。

### Q5: 有什么可以进一步探索的点？

论文的局限性指出了多个未来方向：1）评估仅基于单一产品的一次完整验收测试活动，需要扩展到更多产品、更多测试类型和更大规模数据集以验证泛化性；2）金标准由编码代理辅助准备，第二标注也由编码代理完成，未来应引入人类专家间一致性评估；3）标注规则中关于推断值的处理（如中止阈值）影响错误计数，可探索更灵活的标注规则；4）字段特定的引用规则是在检查错误后编写的，存在乐观偏差，需在独立数据上验证；5）跨模型检查仅基于 9 个已知错误，需扩大错误库；6）API 端点是别名且模型可能变化，结果仅通过缓存响应可复现，需探索稳定版本或本地部署；7）门、舍入规则和修复在同一活动上开发和评估，虽有留出分割，但需更多独立验证；8）常规运行复用存储的模型预测，仅测试了一个配置的重训练，需研究错误改变数据集时的下游影响；9）G5 读取与数值阶段相同的测量导出，是一致性检查而非独立真值，可探索独立数据源；10）注入错误由作者设计，未穷举所有可能错误；11）训练模型固定了 0.5g 到 8g 的电平比，可扩展到其他电平比和测试条件；12）可将自供电传感器（如摩擦电传感器、热电发电机）集成到铰链和压紧点，实现批量测试中的连续监测。此外，可将确定性门范式迁移到其他工程领域（如故障诊断、预测性维护）的 LLM 驱动分析中。

### Q6: 总结一下论文的主要内容

论文提出了一种用于 LLM 驱动工程分析的确定性验证门范式，并以低轨星座卫星的正弦振动验收测试为实例。LLM（DeepSeek V4.1 Flash 和 Qwen-plus）从中文测试记录中提取 76 字段的类型化配置，该配置必须通过六个确定性门（单位、物理一致性、逐字引用、跨模型一致性、测量导出一致性、模型适用性）才能驱动数值陷波决策。实验表明，在共识策略下，所有 20 个 LLM 配置产生的陷波结果与金标准逐位一致，所有 17 个真实和注入的消费字段错误被停止（其中 16 个无门时会静默通过），且无误停。证据接地将精确率提升至 1.0 但牺牲召回率；跨模型检查中 DeepSeek 作为检查者有效，反向则无效。论文还报告了一个有价值的负结果：LLM 直接曲线预测仅与线性外推相当，而小型物理结构化网络 WarpNet-CQR 在 c=0.90 校准时将过陷波带宽减少 86%-89%，明确了 LLM 直接预测应让位于训练模型的边界。核心贡献在于将 LLM 的角色限定为配置提取器，并通过确定性门确保可靠性，为工程分析中的 LLM 集成提供了可追溯、可验证的范式。
