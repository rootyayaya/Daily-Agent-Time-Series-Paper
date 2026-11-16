---
title: "Aligned, Conflicting, or Unspecified? A Diagnostic Benchmark for Multimodal Time Series Forecasting"
authors:
  - "Xintong Wang"
  - "Haihan Nan"
  - "Ruidong Li"
date: "2026-11-13"
arxiv_id: "2611.17680"
arxiv_url: "https://arxiv.org/abs/2611.17680"
pdf_url: "https://arxiv.org/pdf/2611.17680v1"
github_url: "https://github.com/Shelton1202/ACU-Bench"
categories:
  - "cs.AI"
tags:
  - "多模态时间序列预测"
  - "文本-历史关系诊断基准"
  - "AIoT"
  - "错误分解"
  - "预测修正控制"
  - "零样本评估"
  - "时间序列与文本对齐"
relevance_score: 6.5
---

# Aligned, Conflicting, or Unspecified? A Diagnostic Benchmark for Multimodal Time Series Forecasting

## 原始摘要

Artificial Intelligence of Things (AIoT) systems increasingly combine sensed time series with external text such as expert reports and news, yet how reliably models use text that agrees or conflicts with the sensed history remains unclear. We introduce the first real-world diagnostic benchmark organized by text-history relationship: 1,762 text-window pairs across sensor telemetry (Weather), web-service traffic (Wikipedia), and market data streams (Finance), each labeled Aligned, Conflicting, or Unspecified by whether the text's direction agrees with the historical trend, opposes it, or is not stated. Across ten pretrained models evaluated zero-shot, we investigate text selection and combination under text-history relationships (RQ1) and error diagnosis and horizon-scaled revision control (RQ2). For RQ1, we compare two types of text on paired Weather windows: one directly forecasts temperature changes, while the other describes related weather conditions, such as winds and fronts. Under Aligned, the first type yields the lowest error for most models. Under Conflicting, it increases most models' error above the no-text baseline; we therefore add only its stated magnitude and timing to the second type. Compared with either type alone, this combination lowers mean absolute scaled error (MASE) for six models and raises directional accuracy (DA) for seven. For RQ2, an error decomposition attributes the error increase to oversized revisions, and a training-free rule that limits them outperforms forecasts both with and without text for the four models with this trade-off, lowering MASE by 4.49%-21.98% and raising DA by 2.99%-9.71%. Our dataset is available at https://github.com/Shelton1202/ACU-Bench.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注 AIoT 系统中融合传感时间序列与外部文本（如专家报告、新闻）进行预测的可靠性问题。现实中，外部文本可能揭示传感历史尚未体现的变化，也可能与历史趋势相矛盾，因此模型必须妥善处理两种信息源之间的一致或冲突，而不能默认它们彼此吻合。然而，现有评估多只考察文本相对数值历史“额外贡献了什么”，例如 Time-MMD、TimesX 将文本与序列配对，Context is Key 构造文本不可或缺的任务，Zhang 等与 CFA 通过受控实验分析文本的信息增益和对错误文本的鲁棒性，What If TSF 则考察模型对情景变化的修订是否合理；这些工作都没有按真实文本与历史趋势的关系来组织评估。真实报告可能顺应趋势、背离趋势，或根本不陈述方向，缺乏相应基准使得“文本何时有用、何时有害”难以诊断。为此，本文构建首个按文本—历史关系组织的真实世界诊断基准，包含 Weather、Wikipedia、Finance 三个领域的 1,762 个文本—窗口对，并标注为 Aligned、Conflicting、Unspecified，进而研究两个核心问题：在一致与冲突条件下应选择或组合何种文本，以及为何加入文本会提升方向准确率却恶化 MASE，并能否通过限制过度修订同时改善二者。

### Q2: 有哪些相关研究？

本文的相关研究主要可分为三类。方法类方面，Time-MMD 将真实世界时间序列与跨领域报告配对，TimesX 进一步扩展到更多领域和上下文类型（含事件报告），二者为多模态时间序列评测奠定数据基础；Context is Key 通过设计文本上下文不可或缺的任务，检验模型是否真正依赖文本；Zhang 等人用受控实验分析文本是否带来历史之外的信息、以及文本对未来的描述是否显式；CFA 则用受控合成描述测试约束融合对错误或无关文本的鲁棒性。评测类方面，What If TSF 在固定历史与领域背景的前提下，变化事实与假设情景，检验预测修正是否满足预期的方向与强度关系。与上述工作相比，本文的区别在于：现有评测关注文本相对数值历史的增量价值、文本必要性或情景响应，但均未按真实文本与历史趋势的关系（一致、冲突、未指明）组织评测。本文构建首个按文本—历史关系标注的真实世界诊断基准（1,762 对文本—窗口，覆盖 Weather、Wikipedia、Finance），并在此基础上开展文本选择与组合（RQ1）以及误差分解与修正幅度控制（RQ2）研究，弥补了该空白。

### Q3: 论文如何解决这个问题？

论文针对“文本与历史趋势一致/冲突/未指明”三种关系下模型使用外部文本不可靠的问题，提出了一套诊断基准与免训练修正方法。整体框架分为“基准构建—诊断评估—误差归因—修订控制”四步。

首先构建 ACU-Bench：从 Weather、Finance、Wikipedia 三个领域收集 1,762 个“文本—窗口”对，每个实例用预测起点前 96 步历史预测未来 12 步。通过比较历史末两段 12 步均值确定历史方向，并用 GPT-6 Astra 三次独立标注确定文本方向，组合得到 Aligned、Conflicting、Unspecified 三类条件，且标注时看不到数值历史与未来，保证诊断的纯净性。

在评估阶段，对十个预训练模型做零样本预测，比较无文本、方向性文本、非方向性文本三种输入，发现方向性文本在 Aligned 下最优，但在 Conflicting 下反而抬高 MASE。为此提出选择性增强：以非方向性文本为基底，仅追加方向性文本中关于幅度与时机的原文片段，避免整段方向陈述引发过度修订，使六个模型 MASE 下降、七个模型 DA 上升。

进一步做误差分解，按“方向是否正确”的四组窗口归因 MASE 变化，发现净误差集中在最大 25% 的修订上。据此提出免训练的 horizon-scaled revision control：用窗口自身历史估计单步典型变化量，按预测步长缩放为允许位移，对文本引起的均值位移做收缩插值，保留小修订、限制大修订，无需条件标签或调参，在四个模型上同时降低 MASE 4.49%–21.98%、提升 DA 2.99%–9.71%。创新点在于以文本—历史关系组织基准、揭示“方向对但数值差”的机理，并给出可解释的修订控制规则。

### Q4: 论文做了哪些实验？

论文在自建的真实世界诊断基准 ACU-Bench 上开展实验，该基准包含 Weather（传感器遥测）、Wikipedia（Web 服务流量）和 Finance（市场数据流）三个领域共 1,762 个文本-窗口对，按文本方向与历史趋势的关系标注为 Aligned、Conflicting、Unspecified。评测采用零样本设定，不训练、不微调、不使用上下文示例，共评估十个预训练模型：六个语言模型（GPT-6.1 Sol、GPT-6 Luna、Claude Sonnet 5.5、Claude Haiku 5.5、Qwen3-8B、TableGPT2-7B）和四个时间序列模型（Aurora、TimeOmni-1-7B、DoubleCast、TimeBraid-2.5B）。指标为 MASE（越低越好）和方向准确率 DA（越高越好），并定义归一化预测修正幅度 R_i 与误差贡献 C_g 做误差分解。主要结果：Aligned 下方向性文本使九个模型 MASE 下降、九个 DA 上升；Conflicting 下方向性文本使七个模型 MASE 高于无文本基线，仅四个下降；在 165 个 Conflicting Weather 窗口上，以非方向性文本为底、仅补充方向性文本中的幅度与时序信息的选择性增强，使六个模型 MASE 低于两种单一文本、七个模型 DA 更高；误差分解显示最大修正四分位窗口贡献了 60.74%–89.98% 的净 MASE 增量；无训练的地平线缩放修正控制使四个模型同时优于有文本与无文本预测，MASE 降低 4.49%–21.98%，DA 提升 2.99%–9.71%。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三。其一，基准仅覆盖天气、维基流量与金融三类数据，且文本-历史关系由人工标注为三分类，未来可扩展到工业传感、故障日志等AIoT场景，并引入细粒度关系（如部分冲突、时序错位）与自动标注以提升规模。其二，RQ1仅比较两类文本，选择性增强规则较启发式，可探索学习式文本选择器，依据关系类型动态加权或门控融合。其三，RQ2的无训练修订控制虽有效，但仅对存在该权衡的四个模型生效，未来可将文本选择与修订控制联合建模，按关系类型自适应调节修订幅度，并结合不确定性估计与可解释诊断，提升跨模型泛化性。

### Q6: 总结一下论文的主要内容

论文针对AIoT系统中外部文本与传感时间序列可能一致或冲突的问题，构建了首个按“文本—历史关系”组织的真实世界诊断基准：涵盖天气、金融、维基百科三个领域共1762个文本—窗口对，依据文本方向与历史趋势是否一致，标注为Aligned（一致）、Conflicting（冲突）或Unspecified（未指明）。作者对十个预训练模型进行零样本评测，发现一致条件下文本普遍降低误差，而冲突条件下文本虽提升方向准确率却常使数值误差上升。围绕RQ1，研究发现冲突时方向性文本有害、非方向性文本较安全，仅保留非方向性文本并补充变化幅度与时机的选择性增强可同时改善六个模型的MASE和七个模型的DA。围绕RQ2，误差分解表明冲突下的误差增量主要来自过大的预测修正，据此提出无需训练、按预测跨度缩放的修正控制规则，使四个模型的MASE降低4.49%–21.98%、DA提升2.99%–9.71%。该工作为多模态时间序列预测中文本的可靠使用提供了诊断工具与改进思路。
