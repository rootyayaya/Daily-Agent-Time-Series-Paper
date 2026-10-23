---
title: "Agri-SCHOLAR: Simulation-Grounded In-Season Rolling Advisories for Agricultural Crops Using LLM-Bounded Optimization"
authors:
  - "Geetha Charan"
  - "Vedant Balasubramaniam"
  - "Manojkumar Patil"
  - "V. Priyanka"
  - "Kodur Sai Vinay Sathvik"
  - "Rohit P Suresh"
  - "Mohammad Sufyan Azam"
  - "Y. Narahari"
date: "2026-10-22"
arxiv_id: "2610.31003"
arxiv_url: "https://arxiv.org/abs/2610.31003"
pdf_url: "https://arxiv.org/pdf/2610.31003v1"
categories:
  - "cs.AI"
  - "cs.MA"
tags:
  - "LLM-Agent"
  - "多智能体系统"
  - "仿真优化"
  - "滚动决策"
  - "农业时序数据"
  - "多目标优化"
  - "闭环系统"
  - "预测性维护"
relevance_score: 6.5
---

# Agri-SCHOLAR: Simulation-Grounded In-Season Rolling Advisories for Agricultural Crops Using LLM-Bounded Optimization

## 原始摘要

Existing agricultural advisories to farmers suffer from several limitations: (a) remain largely expert-driven, (b) do not adequately account for in-season weather, and (c) do not scale to individual farms. In this paper, our objective is to close these gaps by developing Agri-SCHOLAR (Simulation-Grounded Crop Harvest Optimization with LLM-Guided In-Season Advisory Rollouts). Agri-SCHOLAR is a rolling, in-season advisory framework that issues, at intervals of every few days or every week, a personalized advisory using the following information: soil and crop properties, observed weather to date, short-range forecast of weather, and a season extrapolation of weather based on historical analogs. The novelty and depth of Agri-SCHOLAR lies in each advisory being produced by a closed-loop system which couples multiple LLM agents with a powerful crop simulator (such as APSIM in our case). The simulator crucially serves as an evaluation oracle. In Agri-SCHOLAR, the LLM agents propose agronomically sound and feasible bounds on actionable parameters and an optimizer searches within those bounds against a multi-objective reward spanning yield, resource utilization, and economic feasibility. We conduct a detailed 11-year analysis of the maize crop in two selected locations of South Asia and show that Agri-SCHOLAR consistently outperforms the region's standard packages of practice and satisfactorily addresses the limitations of existing agricultural advisories.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决现有农业咨询建议在实际部署中的三个核心问题。研究背景方面，全球尤其是发展中国家的农业咨询仍主要依赖农艺专家小团队，面向广大区域发布统一建议，难以适应同一区域内不同农场在土壤、品种、播期和管理历史上的差异，也无法针对单个农场实现规模化、个性化服务。现有方法的不足体现在两方面：一是近期工作尝试用DSSAT、APSIM等作物模拟器验证LLM生成的整季建议，虽解决了农艺可行性问题，但评估整季方案需要提前获得整个生长季的天气，而现有预报系统无法在数月尺度上提供足够精度的季节天气，导致该类流程无法前瞻性部署；二是实际业务化咨询（如印度AMFU每周两次发布建议）虽采用“随天气更新滚动修订”的原则，却仍由专家驱动、以行政区为粒度发布，且未经过作物机理模型校验。因此，本文要解决的核心问题是：如何构建一个可部署的、以模拟器为评估依据的滚动式生长季内咨询框架，在仅有观测天气、短期预报和基于历史相似年的季节外推条件下，为单个农场生成农艺可行、兼顾产量、资源利用效率与经济可行性的个性化建议，并随新天气信息不断重优化，从而避免依赖准确的整季天气预报，同时克服传统整季通用型模拟建议的前瞻性局限。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类。方法类方面，基于检索增强的农业咨询系统（如ShizishanGPT、AgriGPT、AgriRegion、AgroAskAI）将通用LLM与知识图谱、地理空间重排序或多智能体治理结合，以减少上下文幻觉；但这类系统仅关注问答准确性，不检验建议在作物生理上是否可行。另一类工作将LLM输出锚定于过程式作物模拟器：DSSAT-LM以DSSAT为确定性符号骨架，由LLM解读问题并生成答案；Agri-SAGE将多智能体LLM推理与APSIM耦合，比较Plan-and-Solve、Tree of Thoughts和Reflexion等策略。本文在Agri-SAGE基础上改进三点：仅用当日可得信息逐周决策并滚动重优化，而非用全季天气制定一次性计划；LLM只设定农艺可行边界，由数值优化器在边界内大量评估候选方案；优化目标为净利润而非单一产量，并覆盖灌溉与雨养两种水情。应用类方面，gym-DSSAT等工作将作物模拟器作为强化学习环境训练施肥与灌溉策略，但输出数值方案而非可解释的农户咨询。评测类方面，AGXQA、AgriBench、AgMMU、AgEval等基准仅评估问答与多模态推理能力。此外，GraphCast、Pangu-Weather、GenCast、Aurora等天气预报模型仅约两周有效，短于作物周期，故印度GKMS、中国气象服务、越南农业气候公报等业务系统采用短周期滚动发布，但均为专家驱动、区域尺度；本文借鉴其滚动节奏，并增加农场级个性化与机理验证。

### Q3: 论文如何解决这个问题？

Agri-SCHOLAR 的核心思路是把“LLM 智能体”与“作物模拟器”耦合成一个闭环滚动决策系统，让 LLM 负责提出农学上合理、可执行的管理边界，而由优化器在边界内搜索最优方案，模拟器则充当评估“神谕”。

整体框架包含五个智能体：上下文检索智能体（CRA）将数值化的天气、土壤和作物阶段特征转为自然语言查询，在农学文献与区域指南向量库上做稀疏+稠密混合检索，输出紧凑的上下文包；预季智能体（PSA）在季初依据降雨起始规则（6月1日至7月15日滑动三日窗口，首个累计降雨≥20mm窗口的末日为播期）确定播期、覆盖与基肥；咨询边界智能体（ABA）结合检索上下文，为每项管理操作生成可行边界；优化智能体（OA）在边界内用 Optuna（TPE）搜索最大化期望经济回报的方案；验证与反馈智能体（VFA）把候选动作转为 APSIM 调用，在当前周期“构造天气”（已观测+带噪7天预报+历史相似年尾部）上模拟并回传产量、氮平衡、排水、淋失等指标。

关键创新有三点：一是用 LLM 生成的边界同时缩小搜索空间并防止优化器“钻模拟器空子”（如施入生理上不合理的巨量氮肥）；二是多目标奖励 R = 收入 − 生产成本 − 可持续性惩罚，把涝渍、氮过量、深排水、氮淋失、有机碳损失折算为货币影子成本；三是三层嵌套循环——内层 OA-VFA 搜索、中层 ABA 依据反馈自反思调整边界、外层每周用最新观测重跑全流程，仅提交当周动作，后续计划丢弃并在下周重新优化，形成真正的滚动咨询。

### Q4: 论文做了哪些实验？

论文在实验部分对南亚两个水资源条件不同的地区（灌溉区和雨养区）的玉米进行了11个连续kharif季（2015–2025）的模拟评估。实验设置上，所有语言智能体使用google/gemma-4-E4B-it，天气数据取自ERA5（1980–2025），土壤剖面由当地农业专家提供，成本参数经专家整理并按购买力平价折算为美元。基准对比方法为区域标准实践包（PoP），即固定的施肥与灌溉日历；两种方法采用相同的播种日期规则，因此差异仅来自季内管理。Agri-SCHOLAR每周发布一次建议，仅使用截至决策日的信息，随后在APSIM中以真实天气回放整个季节。

主要结果：Agri-SCHOLAR在两个地区的每个季节均优于PoP。灌溉区平均增产15.18%（单季增益6.57%–29.45%），雨养区平均增产22.43%（15.14%–27.72%）。灌溉区平均净利润提高17.2%，雨养区提高22.8%。以灌溉区为例，平均产量由6,477.55 kg/ha升至7,461.00 kg/ha，净利润由5,959.33升至7,025.09 $/ha，可持续性惩罚由495.33降至267.05 $/ha；雨养区产量由5,909.36升至7,234.55 kg/ha。灌溉区深层排水与硝酸盐淋失分别平均减少52.8%和52.7%。案例研究（2023灌溉季）中，Agri-SCHOLAR仅用180 kg/ha尿素N和一次灌溉即获11,028 kg/ha产量，而PoP多五次灌溉、多约77%氮肥却仅得8,519 kg/ha。消融实验则对比了ABA生成的边界与宽松固定边界、无边界两种替代方案。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点。其一，评估仅覆盖南亚两地的玉米、11个生长季，且以APSIM模拟为唯一真值，缺乏真实田间验证；未来可在多作物、多气候带开展实地试验，并检验更换模拟器后的稳健性。其二，LLM智能体仅用gemma-4-E4B，边界生成的质量与幻觉风险未系统评估，可探索多模型集成、置信度校准及人在回路审核。其三，天气仅用7天预报加历史类比外推，极端天气与预报误差下的鲁棒性不足，可引入集合预报与分布鲁棒优化。其四，奖励权重与影子成本依赖专家设定，可研究自适应权重与农户风险偏好个性化。其五，当前为开环建议，未考虑农户执行偏差与反馈学习，可构建执行监测与在线校正闭环。此外，可扩展到病虫害、碳足迹等多目标，并探索轻量化部署以适配小农户。

### Q6: 总结一下论文的主要内容

论文针对现有农业建议依赖专家、忽视当季天气且难以覆盖个体农场的问题，提出 Agri-SCHOLAR——一种滚动式、当季个性化的作物管理建议框架。其核心思路是将多个 LLM 智能体与作物模拟器 APSIM 耦合为闭环系统：LLM 智能体基于检索到的农艺知识，为灌溉与施肥等可操作参数提出农艺上合理且可行的边界；优化器则在这些边界内搜索，以 APSIM 作为评估预言机，最大化兼顾产量、资源利用效率与经济可行性的多目标奖励。每个建议仅使用截至决策日的观测天气、短期预报和基于历史相似年的季节外推，并每周重新优化，从而避免依赖准确的整季天气预报。作者在南亚两个灌溉与雨养玉米区开展 11 年评估，结果表明该方法在各季均优于区域标准实践：灌溉区平均增产 15.18%、雨养区增产 22.43%，净利润分别提升 17.2% 和 22.8%，灌溉区深层排水与硝态氮淋失均降低约 53%，可持续性惩罚下降 46.1%。消融实验进一步证明 LLM 生成的农艺边界对防止优化器“钻模拟器空子”和提升实际可行性至关重要。
