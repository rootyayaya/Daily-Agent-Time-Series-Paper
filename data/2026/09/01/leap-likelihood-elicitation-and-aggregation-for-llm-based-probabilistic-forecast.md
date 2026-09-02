---
title: "LEAP: Likelihood Elicitation and Aggregation for LLM-based Probabilistic Forecasting"
authors:
  - "Yufei Chen"
  - "Yiran Zhao"
  - "Xiaogang Xu"
  - "Qipeng Xie"
  - "Jiafei Wu"
  - "Zhe Liu"
date: "2026-09-01"
arxiv_id: "2609.01337"
arxiv_url: "https://arxiv.org/abs/2609.01337"
pdf_url: "https://arxiv.org/pdf/2609.01337v1"
github_url: "https://github.com/layingfish/LEAP"
categories:
  - "cs.AI"
tags:
  - "LLM-based forecasting"
  - "probabilistic forecasting"
  - "evidence aggregation"
  - "likelihood elicitation"
  - "agent workflow"
  - "calibration"
  - "monolithic prediction"
  - "evidence contribution"
relevance_score: 7.5
---

# LEAP: Likelihood Elicitation and Aggregation for LLM-based Probabilistic Forecasting

## 原始摘要

LLM-based forecasting systems have improved on real-world tasks such as financial markets and sports outcomes, largely through stronger search and tool use. Many systems still ask an LLM to read all collected evidence together and produce the final forecast. We call this design Monolithic Prediction. It can obscure how individual evidence items affect the result and collapse uncertainty across competing outcomes. We propose LEAP (Likelihood Elicitation and Aggregation for Probabilistic forecasting), which reorganizes how collected evidence is used in the prediction stage. LEAP examines each evidence item separately and elicits likelihood parameters that describe its implications for the target. An explicit prior and a deterministic probabilistic model then combine these likelihoods into a posterior distribution. This procedure supports continuous, single-choice, and multi-choice forecasts while preserving reproducible evidence contributions. We build a benchmark covering forecasting, information-seeking, and browsing tasks, and evaluate LEAP on our own agent loop and several agent CLI frameworks. Given the same evidence, LEAP improves most prediction and calibration metrics across models and remains stronger under controlled comparisons of prior access, inference budget, and aggregation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着大语言模型（LLM）与智能体框架的成熟，基于LLM的预测系统已广泛应用于金融、体育和地缘政治等真实世界任务。现有系统通常先通过智能体循环搜集网络证据，再让LLM一次性阅读全部证据并输出最终预测，本文称之为“整体预测”设计。然而，该设计存在两个核心缺陷：其一，预测过程不透明，用户无法追溯每条具体证据对结果的独立影响，且模型可能将竞争性结果间的不确定性压缩为单一答案；其二，长上下文下LLM需融合多源证据，容易引发遗忘和幻觉，导致预测偏差。

为克服上述不足，本文提出LEAP（似然抽取与聚合的概率预测框架）。其核心思路是将预测阶段重组：不再让LLM整体阅读证据，而是将其作为局部解释器，逐条独立分析每条证据，抽取其对目标的似然参数；同时构建先验分布，再通过确定性概率模型将这些似然与先验聚合为后验分布。该框架支持连续、单选和多选预测，并保证证据贡献的可复现性。LEAP旨在解决“给定固定证据集，如何以可审计、概率化且抗遗忘的方式生成最终预测”这一核心问题，从而提升预测准确率与校准质量，并实现证据级别的可解释性。

### Q2: 有哪些相关研究？

相关研究主要分为四类。**方法类**中，AutoCast、AutoCast++及ForecastBench构建了带时间戳的预测基准与检索系统，但最终预测仍由LLM整体阅读证据生成，即“Monolithic Prediction”；LEAP则聚焦证据收集后的预测阶段，逐条评估证据并显式聚合。**贝叶斯推断类**中，BIRD利用LLM生成因子参数化贝叶斯模型，Nafar等从LLM eliciting条件概率构建预定义贝叶斯网络，Bayesian Linguistic Forecaster在迭代搜索中维护语言信念状态；与这些方法不同，LEAP不依赖预定义网络或迭代信念更新，而是对每条证据独立eliciting似然，再用确定性概率模型计算后验。**智能体评测类**中，ReAct、WebGPT等关注检索与推理结合，但评测通常打分整个系统；LEAP通过固定证据集，隔离并单独评估“证据到预测”的转换环节。**可解释性类**中，ERASER和faithful chain-of-thought强调推理轨迹与计算过程耦合；LEAP遵循该原则，由LLM提供局部证据解释，而最终后验与证据贡献由显式概率更新计算，避免事后生成的自由文本解释。总体而言，LEAP的独特贡献在于将证据收集与预测分离，以证据级似然elicitation和显式聚合提升可审计性与校准度，且接口可适配连续、单选和多选预测任务。

### Q3: 论文如何解决这个问题？

LEAP的核心思路是将LLM从“直接给出最终预测”的角色中解放出来，转而让其专注于局部证据的解读，最终判断交由显式概率模型完成。整体框架分为两个阶段：局部参数elicitation和确定性聚合。

在局部参数elicitation阶段，系统为每个证据项单独调用LLM，模型仅能看到目标任务和该单一证据，无法接触其他证据或中间结果。LLM的任务不是预测，而是输出结构化参数：对于连续目标，提取目标尺度的观测值作为似然均值，并用定性标签确定标准差；对于单选项目标，输出对各选项的支持程度标签；多选项目标则输出支持/反对标签。这些定性标签通过标准映射转换为似然参数。同时，先验参数由历史数据或单独的无证据LLM调用确定。

在确定性聚合阶段，系统采用贝叶斯共轭模型进行闭式更新：连续目标用高斯共轭对，单选项用多项分布，多选项用独立伯努利。最终预测直接从后验分布读出。关键技术包括：依赖聚类（通过依赖键识别同源证据并只保留代表项）、可靠性采样（重复查询同一证据，用一致性调整似然幅度）、异常值拒绝（对数据先验的连续任务，若证据均值偏离先验超4个标准差则剔除）。此外，系统还提供留一法贡献Δj，可复现地展示每条证据对最终预测的影响。

创新点在于：将LLM的推理能力限定在局部似然估计这一受约束任务上，避免了整体预测中不确定性坍缩和证据贡献不可解释的问题，同时保持了计算的确定性和可复现性。

### Q4: 论文做了哪些实验？

论文构建了一个覆盖预测、信息检索和浏览任务的基准（源自FutureX、GAIA和BrowseComp），在两种设置下评估LEAP：一是使用ReAct风格agent循环，在DeepSeek-V3.2、Gemini-3.1-Flash-Lite、Claude-Haiku-4.5、GPT-5.4-mini和Grok-4.20-Fast五个基座模型上对比Monolithic与LEAP；二是将LEAP作为概率技能应用于DeerFlow、Hermes、OpenClaw和MiroFlow四个外部agent框架的未修改轨迹。主要指标包括FutureX综合分、准确率、Brier分数、Spherical分数和NCRPS。

结果显示，在自有agent循环中，LEAP在所有模型上均提升FutureX（绝对增益3.6至18.1点）、Spherical和准确率，并改善NCRPS；在外部框架中，LEAP在宏平均上全面领先，FutureX提升9.8点、Brier降低16.5点。消融实验表明，移除先验影响最大（FutureX降至0.643，ECE升至0.213），依赖聚类和可靠性采样也有贡献。校准诊断显示LEAP将ECE从0.184降至0.088，过度自信从0.317降至0.150。随预测时域延长，LEAP优势扩大；在控制先验访问和推理预算下，LEAP仍优于线性意见池及同等预算的Monolithic基线。

### Q5: 有什么可以进一步探索的点？

LEAP的局限为后续研究提供了清晰方向。首先，其仅优化“预测阶段”而忽视“证据收集”上游，未来可探索将LEAP的似然聚合机制与主动信息检索结合，让Agent根据当前后验不确定性动态决定下一步搜索，形成闭环推理。其次，当前评估限于英语和固定协议，可扩展至多语言、科学文献（如医学或气候）及长时序预测，验证其跨域泛化性。在方法上，LEAP对每条证据独立采样多次以验证局部一致性，虽提升可审计性但增加推理成本，未来可引入“证据重要性加权”或“缓存相似证据的似然”来降低开销。此外，当前似然参数由LLM直接生成，缺乏显式不确定性校准，可考虑用贝叶斯神经网络或集成方法对单条证据的似然分布建模。最后，LEAP的确定性聚合模型虽透明，但面对复杂交互证据（如矛盾或条件依赖）时可能过于简化，探索基于图神经网络或因果模型的结构化聚合将是重要突破点。

### Q6: 总结一下论文的主要内容

本文提出LEAP框架，用于改进基于大语言模型的概率预测系统。传统方法采用“整体预测”模式，让模型一次性阅读所有证据后直接输出结果，这掩盖了单个证据的影响并导致不确定性坍缩。LEAP将预测过程重组：先单独分析每条证据，提取其似然参数，再通过显式先验和确定性概率模型将这些似然聚合为后验分布。该方法支持连续、单选和多选预测，且证据贡献可复现。作者构建了涵盖预测、信息搜索和浏览任务的基准，在自建代理循环和多个外部代理框架上验证。结果表明，在证据固定条件下，LEAP在五个基础模型和四个框架中显著提升预测准确性和校准质量，将期望校准误差和过度自信约减半，且预测跨度越长优势越明显。由于推理为闭式解，可通过逐一移除证据重跑后验更新来审计贡献，弥补了自由文本解释的不足。
