---
title: "ProfiLLM: Utility-Aligned Agentic User Profiling for Industrial Ride-Hailing Dispatch"
authors:
  - "Tengfei Lyu"
  - "Zirui Yuan"
  - "Xu Liu"
  - "Kai Wan"
  - "Zihao Lu"
  - "Li Ma"
  - "Hao Liu"
date: "2026-06-17"
arxiv_id: "2606.18803"
arxiv_url: "https://arxiv.org/abs/2606.18803"
pdf_url: "https://arxiv.org/pdf/2606.18803v1"
categories:
  - "cs.AI"
  - "cs.CY"
tags:
  - "LLM Agent"
  - "工业应用"
  - "用户画像"
  - "工具增强"
  - "下游效用对齐"
  - "DPO微调"
  - "大规模系统"
relevance_score: 6.5
---

# ProfiLLM: Utility-Aligned Agentic User Profiling for Industrial Ride-Hailing Dispatch

## 原始摘要

Bringing Large Language Models (LLMs) into industrial ride-hailing dispatch as semantic feature extractors over platform-scale behavioral logs is a compelling but under-explored data systems problem. Production matching pipelines remain dominated by structured numerical features, yet decisive behavioral signals (e.g., a driver's habitual aversion to certain regions) are inherently contextual and naturally expressible as LLM-generated user profiles. However, scaling such profiling to a live, millisecond-latency dispatcher faces three intertwined constraints rarely addressed together: on a platform with millions of daily orders, logs exceed any LLM's context window by orders of magnitude; most users are long-tail, with too few interactions for per-user profiling; and surface-fluent profiles do not necessarily improve downstream prediction utility. We present ProfiLLM, an agentic LLM data pipeline that operationalizes utility-aligned user profiling for production matching systems through two modules. (1) Tool-Augmented Global Knowledge Mining equips an LLM agent with 27 analytical tools to mine platform-scale data, producing reusable global knowledge, adaptive user clustering rules, and region-level supply-demand priors. (2) Utility-Aligned Profile Exploration generates multiple candidate profiles per cluster, evaluates them via a lightweight downstream utility proxy, iteratively refines the best candidates and constructs preference pairs for DPO fine-tuning. Deployed on DiDi's production dispatcher, ProfiLLM achieves up to +6.14% relative AUC improvement in outcome prediction, up to +4.35% GMV gain in dispatching simulation, and consistent improvements in a 14-day online A/B test including +0.47% GMV, +0.33% Completion Rate, and -0.82% Cancel-Before-Accept rate.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

网约车调度系统是城市交通的核心基础设施，其订单分配依赖对司机接单、乘客取消等行为的精准预测。当前生产系统主要使用结构化数值特征（如距离、价格），但决定用户行为的信号往往是隐式的、上下文相关的，例如司机对某些区域的长期偏好或乘客在特定时段的紧迫性。大型语言模型（LLM）具备从行为轨迹中提炼语义化用户画像的能力，有望弥补这一不足。

然而，将LLM画像部署到工业级在线系统面临三大挑战：第一，平台每日百万级订单远超LLM上下文窗口，无法直接处理全量日志；第二，用户分布呈严重长尾（96%乘客订单数≤30），低频用户缺乏足够历史数据支撑个性化画像；第三，LLM生成的流畅画像并不保证能提升下游预测效用，甚至可能因引入噪声而降低AUC。

本文提出ProfiLLM，旨在解决上述问题。其核心目标是构建一个实用化的LLM数据管道，通过工具增强的全局知识挖掘从海量数据中提取可复用的运营知识、自适应用户聚类规则和区域供需先验，再通过效用对齐的画像探索机制，以预测效用为优化信号迭代生成和精炼聚类级用户画像，最终实现离线生成、在线零延迟调用的工业级部署。

### Q2: 有哪些相关研究？

相关研究可分为三类：**LLM用户画像方法**、**工业匹配系统优化**和**LLM与数据系统结合**。

在**LLM用户画像方法**方面，现有工作多聚焦于高频用户或静态文本数据，如利用LLM总结社交媒体行为或购物记录生成画像。本文与之区别在于：首先，针对网约车场景中96%乘客为低频用户（≤30单）的长尾分布，提出**自适应用户聚类**，而非逐用户画像；其次，引入**效用对齐机制**，通过轻量级下游预测代理（LOGIC规则）评估画像质量，并用DPO微调优化，解决了“画像流畅但预测无用”的问题。

在**工业匹配系统优化**方面，传统方法依赖结构化数值特征（如距离、价格），而本文首次将LLM生成的语义画像作为特征嵌入，与结构化特征融合用于实时订单匹配。与仅在高频用户上离线验证的初步研究相比，本文实现了生产级部署，在线推理仅增加亚毫秒延迟。

在**LLM与数据系统结合**方面，现有工作常受限于上下文窗口和实时性约束。本文设计**工具增强的全局知识挖掘**模块，通过27个分析工具和“探索-深化-验证-综合”范式，从平台级日志（如38天4400万条记录）中提取可复用的全局知识、聚类规则和区域供需先验，解决了数据规模超限问题。这是首个在工业网约车调度系统中部署的LLM用户画像管道。

### Q3: 论文如何解决这个问题？

ProfiLLM通过一个严格解耦的离线-在线三层流水线解决工业级网约车调度中的用户画像问题。核心创新在于将LLM作为离线数据挖掘引擎，而在线服务仅使用轻量级缓存结果。

**整体框架**分为三层：**第一层（离线）** 是工具增强的全局知识挖掘。LLM智能体配备27个可组合的分析工具（如统计、时空分析、因果检验），遵循“探索-深化-验证-综合”四阶段范式，自动挖掘平台级日志，产出三个可复用工件：全局行为知识K、可解释的用户聚类规则集A（布尔规则分类器）和区域供需先验R。这解决了海量日志超出LLM上下文窗口的问题。

**第二层（离线）** 是效用对齐的画像探索。针对每个聚类，LLM基于K和聚合历史生成K个候选画像，每个画像包含分析、语义描述和可执行逻辑规则三部分。关键创新在于使用轻量级LOGIC规则代理评估画像效用：将规则预测与基线模型输出融合，计算AUC提升作为画像质量指标。通过迭代优化最佳候选，并构建偏好对进行DPO微调，使LLM生成与下游预测效用对齐的画像。这解决了长尾用户数据稀疏和画像表面流畅但无实际效用的问题。

**第三层（在线）** 是预测与匹配。在线服务仅执行两项操作：根据规则集A确定用户所属聚类，从缓存中获取预计算的聚类嵌入向量。这些嵌入与结构化特征拼接后输入生产级多任务预测模型，匹配流程不变。整个路径无LLM推理，每对订单-司机开销低于0.01毫秒，满足200毫秒端到端延迟预算。

### Q4: 论文做了哪些实验？

论文在滴滴出行真实工业数据集上进行了全面实验。实验设置使用巴西三个城市（A、B、C）38天历史数据训练，5天测试。对比方法包括传统方法（TVal、GRC）和多种LLM基线（Llama-3.3-70B、Qwen3-Next-80B、DeepSeek-R1、Kimi-K2、Gemini-3-Flash/Pro、GPT-OSS-120B），以及ProfiLLM及其DPO变体。

主要结果分两个层面：1）预测层面（AUC）：ProfiLLM在三个城市所有任务上均取得一致正提升，最高达+6.14%（City A的P-Cancel），而基线LLM常出现负收益（如Kimi-K2在City B的P-Cancel下降6.33%）。2）调度层面：模拟器实验中ProfiLLM-DPO实现最高GMV提升（City C +4.35%），ProfiLLM实现最高完成率提升（City C +7.53%）。14天在线A/B测试显示：GMV +0.47%、完成率+0.33%、取消率-0.82%。消融实验证实全局知识挖掘和用户聚类是关键组件，去除后性能显著下降。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：ProfILLM依赖预定义的27个分析工具进行全局知识挖掘，工具集可能无法覆盖所有长尾用户的独特行为模式；DPO微调依赖下游代理的效用评估，但代理本身的预测偏差可能传播到用户画像中；此外，画像生成仍基于聚类而非个体，对高度异质的长尾用户可能不够精准。

未来可探索的方向包括：引入自适应工具生成机制，让LLM Agent根据数据分布动态创建新工具；结合在线强化学习，使画像随用户行为实时演化；探索多模态用户行为（如轨迹、订单文本）的联合建模；设计更细粒度的个体级画像生成策略，例如利用小样本学习从少量交互中推断用户偏好；在工业系统中验证画像的可迁移性，即同一画像能否服务于调度、推荐等多个下游任务。

### Q6: 总结一下论文的主要内容

ProfiLLM针对工业网约车调度中LLM用户画像部署的三个核心挑战：海量日志超出现有LLM上下文窗口、长尾用户数据稀疏、以及生成的画像无法保证提升下游预测效用。论文提出了一种智能LLM数据流水线，包含两个模块：(1) 工具增强的全局知识挖掘，为LLM智能体配备27种分析工具，从平台级数据中挖掘可复用的全局知识、自适应用户聚类规则和区域供需先验；(2) 效用对齐的画像探索，为每个聚类生成多个候选画像，通过轻量级下游效用代理进行评估和迭代优化，并构建偏好对进行DPO微调。在滴滴生产调度系统部署后，ProfiLLM实现了结果预测AUC提升最高6.14%，模拟调度GMV提升4.35%，并在14天在线A/B测试中取得GMV+0.47%、完成率+0.33%、取消率-0.82%的显著改进。该工作首次将LLM用户画像成功部署于生产级网约车调度系统。
