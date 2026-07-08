---
title: "Onnes: A Physics-Grounded Multi-Agent LLM Simulator for Cryogenic Fault Diagnosis in Quantum Computing Infrastructure"
authors:
  - "Praneeth Narisetty"
  - "Uday Kumar Reddy Kattamanchi"
  - "Shiva Nagendra Babu Kore"
date: "2026-07-07"
arxiv_id: "2607.05805"
arxiv_url: "https://arxiv.org/abs/2607.05805"
pdf_url: "https://arxiv.org/pdf/2607.05805v1"
github_url: "https://github.com/Onnes-Research/onnes"
categories:
  - "cs.AI"
  - "cs.LG"
  - "quant-ph"
tags:
  - "Agentic Time Series"
  - "可解释故障诊断"
  - "多智能体LLM"
  - "物理数字孪生"
  - "低温故障诊断"
  - "零样本LLM"
  - "对比少样本演示"
  - "自一致性投票"
  - "置信门控"
  - "工业传感器解释"
  - "量子计算基础设施"
relevance_score: 9.5
---

# Onnes: A Physics-Grounded Multi-Agent LLM Simulator for Cryogenic Fault Diagnosis in Quantum Computing Infrastructure

## 原始摘要

Dilution refrigerators are the enabling infrastructure of superconducting quantum computers, yet their fault diagnosis is still dominated by threshold alarms that report that something is wrong, not what. We present Onnes, a physics-grounded digital-twin simulator of a dilution refrigerator (a forward physics model with a learned real-fridge noise fingerprint) that drives a live multi-agent LLM operations layer, and use it for a controlled head-to-head between a zero-shot LLM agent panel and a supervised ML classifier on cryogenic fault diagnosis. The twin couples a real dilution-cooling floor, a noise-and-correlation fingerprint learned from real BlueFors logs, and six physics-grounded fault classes, three engineered to overlap on temperature but separate on flow and pressure. Across a 1000-turn evaluation the zero-shot panel shows no significant difference from the classifier on detection but trails on classification, its errors concentrating on the confusable faults. Curated contrastive few-shot demonstrations and self-consistency voting then raise classification accuracy from 0.685 to 0.990, matching the supervised classifier (0.985) with no parameter updates and six labeled demonstrations; an ablation attributes the gain almost entirely to the demonstrations. Run as a continuous monitor across a nine-run fault-by-seed sweep, the agent catches every developing fault within one poll interval, and a confidence gate suppresses pre-onset false alarms whose rate is backend-dependent. As a first sim-to-real check, a detector trained purely on real BlueFors telemetry posts a real-hardware false-alarm rate of 6.4% and 100% recall on physics faults injected onto real held-out windows. All numbers are drawn verbatim from released run logs.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

稀释制冷机是超导量子计算机的关键基础设施，其故障诊断目前主要依赖阈值报警，只能报告“有异常”而无法定位具体故障类型。现有方法面临三重现实挑战：降温过程耗时数天且成本高昂，停机代价巨大；硬件故障（如泄漏、堵塞）罕见且多为一次性事件，导致带标签的故障样本极度稀缺；每台新制冷机在投运时都没有自身的历史故障记录。因此，将遥测数据转化为具体的故障名称和操作建议，同时应对真实世界中的标签稀缺问题，是本文要解决的核心问题。

现有基于阈值的监控系统无法提供细粒度诊断，而监督学习方法虽然性能优越，但严重依赖大量标注数据，在故障样本稀缺的工业场景中难以落地。本文提出Onnes系统，构建了一个基于物理的数字孪生模拟器，耦合真实制冷机噪声指纹与六类物理故障，并驱动一个多智能体LLM操作层。核心目标是：在零样本或少样本条件下，评估LLM智能体在低温故障诊断中能否达到甚至超越监督学习模型的性能，并探索通过对比少样本演示和自一致性投票等上下文学习机制来弥补性能差距的有效性。

### Q2: 有哪些相关研究？

在低温监控领域，现有工作主要依赖阈值告警（如Grafana/Slack），而机器学习方法已应用于大型低温系统（如CERN的LHC超导磁体LSTM监控、SRF腔故障分类等）。Onnes在此基础上增加了基于物理的稀释制冷机数字孪生和LLM推理层，而非固定ML模型。在量子计算低温基础设施方面，现有研究聚焦于超导量子比特规模化（如单制冷机内500+量子比特封装）、低温CMOS控制架构等，Onnes则为其提供运维层以保障日益负载的制冷机健康。在LLM方法上，上下文学习（ICL）方面，Onnes采用精选对比示例而非多示例堆叠，因为2026年研究表明多示例规则在推理任务上失效；自一致性投票被采用（优于自精炼，后者在2026年研究中导致-4.6至-9.1点准确率下降）；多智能体辩论被避免，因其优势被证明主要来自测试时计算增加而非协调。在LLM故障诊断领域，2025年已有大量工作应用于旋转机械、建筑系统、电网等，Onnes的区别在于：1）物理基础性——故障由稀释冷却正向模型生成，包含真实制冷机噪声指纹，混淆类具有物理退化原因；2）目标领域——量子计算低温基础设施，具有微瓦级冷却预算、mK工作点和安全联锁（如禁止磁体失超）。据我们所知，这是首个在稀释制冷机故障诊断上进行受控智能体vs监督分类器对比的研究。

### Q3: 论文如何解决这个问题？

Onnes通过构建一个物理驱动的数字孪生模拟器，结合多智能体LLM操作层，来解决量子计算基础设施中稀释制冷机的故障诊断问题。核心方法包括三个部分：

**1. 物理数字孪生（Digital Twin）**：该孪生体由三部分组成：(a) 真实T²稀释冷却物理模型，精确模拟MXC温度与热负载的平方根关系，并包含脉冲管冷却的上层温度；(b) 从真实BlueFors日志中学习的噪声指纹，包括每级相对波动（MXC 0.74%，50K 1.6%，流量2.3%）和跨级相关性；(c) 六个物理接地故障类（正常、热负载尖峰、氦泄漏、磁体失超、布线热侵入、阻塞阻抗），其中三个热故障特意设计为温度重叠但流量和压力可区分。

**2. 多智能体操作层（Multi-Agent Operations Layer）**：采用固定的五角色流水线架构——哨兵（检测异常）、诊断师（分类+严重性）、操作员（建议动作）、守护者（安全否决）、监督者（最终裁决）。每个角色是单次LLM调用，窗口数据以紧凑数值摘要呈现。两个可选杠杆附着在诊断师上：对比式少样本演示和自我一致性投票（N=3）。

**3. 关键技术**：零-shot面板在检测上与监督ML分类器无显著差异，但分类准确率仅0.685。通过对比式少样本演示（6个标注示例）和自我一致性投票，分类准确率提升至0.990，匹配监督分类器（0.985），且无参数更新。消融实验表明增益几乎全部来自演示。连续监控测试中，智能体在一个轮询间隔内捕获所有发展中的故障，置信门控抑制了预触发误报。

### Q4: 论文做了哪些实验？

根据论文内容，实验主要围绕基于物理的多智能体LLM模拟器Onnes在低温故障诊断中的性能评估展开。实验设置包括一个耦合了真实稀释制冷机冷却层、从真实BlueFors日志中学习的噪声与相关性指纹，以及六个基于物理的故障类别（其中三个在温度上重叠但可通过流量和压力区分）的数字孪生模拟器。数据集/基准测试方面，使用了1000轮评估、n=24的验证集和n=200的大规模种子集，对比方法包括零样本LLM智能体面板、监督式机器学习分类器（随机森林）以及增强后的智能体面板（加入对比性少样本演示和自一致性投票）。主要结果显示：零样本面板在检测上与分类器无显著差异，但分类准确率仅为0.685，错误集中在易混淆故障上；通过引入k=6个对比性少样本演示和N=3次自一致性投票，增强面板的分类准确率从0.685提升至0.990（n=200），与监督式随机森林的0.985持平，且无需参数更新；在n=24验证集上准确率从0.50提升至1.00。消融实验表明，性能提升几乎完全归因于少样本演示。此外，在连续监控实验中，智能体在每个轮询间隔内捕获所有发展中的故障，置信门控机制抑制了预发作假警报。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：零样本LLM在分类混淆故障时仍落后于监督模型，且依赖精心设计的对比示例和自一致性投票来弥补差距，这在实际部署中可能难以持续。此外，数字孪生仅模拟了六类故障，未涵盖更复杂的多故障并发或罕见故障场景；连续监控实验仅持续24小时，缺乏长期稳定性验证。

未来可探索的方向包括：1）引入主动学习或在线微调，使LLM能动态适应新故障模式，减少对预定义示例的依赖；2）扩展数字孪生以模拟更多故障类型和噪声模式，提升泛化能力；3）结合物理先验与因果推理，增强模型对混淆故障的区分能力；4）探索多智能体协作的优化策略，如动态角色分配或基于置信度的任务委派，而非固定五角色结构；5）在真实量子计算基础设施中部署长期监控，验证系统在数月尺度上的可靠性与误报率。

### Q6: 总结一下论文的主要内容

本文提出Onnes，一个基于物理的多智能体LLM模拟器，用于量子计算基础设施中稀释制冷机的故障诊断。核心问题是将遥测数据转化为具体故障诊断和操作建议，克服真实标签稀缺的挑战。方法上，Onnes构建了一个物理数字孪生体，结合真实制冷机噪声指纹和六类物理故障（其中三类在温度上混淆），驱动一个五角色LLM智能体面板（哨兵、诊断师、操作员、守护者、监督者），并与监督式ML分类器进行头对头对比。主要结论：在1000轮评估中，零样本智能体面板在检测上与分类器无显著差异，但在分类上落后；通过引入对比性少样本演示和自一致性投票，分类准确率从0.685提升至0.990，匹配监督分类器（0.985），且无需参数更新。消融实验表明增益几乎完全来自演示。连续监控实验显示，智能体能在一次轮询间隔内捕获所有发展中的故障。该工作贡献了一个可复现的、受物理约束的基准测试，并展示了LLM智能体在标签稀缺的工业诊断任务中的潜力。
