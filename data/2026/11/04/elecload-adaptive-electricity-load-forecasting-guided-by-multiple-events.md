---
title: "ElecLoad: Adaptive Electricity Load Forecasting Guided by Multiple Events"
authors:
  - "Huajian Zhang"
  - "Mingyue Cheng"
  - "Xingpeng Gao"
  - "Xiaoyu Tao"
  - "Zhiding Liu"
  - "Jiqian Yang"
  - "Zhi Li"
date: "2026-11-04"
arxiv_id: "2611.06508"
arxiv_url: "https://arxiv.org/abs/2611.06508"
pdf_url: "https://arxiv.org/pdf/2611.06508v1"
github_url: "https://github.com/zhjai/ElecLoad"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "多事件上下文感知"
  - "电力负荷预测"
  - "多智能体协作"
  - "自适应预测过程"
  - "反馈优化"
  - "子智能体精炼"
  - "事件交互分析"
relevance_score: 7.5
---

# ElecLoad: Adaptive Electricity Load Forecasting Guided by Multiple Events

## 原始摘要

Accurate electricity load forecasting provides critical decision support for energy procurement, generation scheduling, and supply-demand balancing, contributing to the economic efficiency and operational reliability of power systems. However, future electricity demand can be affected by the complex interplay of multiple events described in Web notices, weather alerts, and event schedules. Their effects vary over time and can reinforce or offset one another, making electricity load difficult to forecast accurately. While existing methods can incorporate context as additional input, how to use the effects of multiple events and their interactions to guide the load forecasting process itself remains to be explored. To address this gap, we propose ElecLoad, a context-aware agent for multi-event electricity load forecasting that adaptively organizes the forecasting process. Specifically, we train ElecLoad to combine historical load with context to analyze each event's relevance to the target load, the timing of its effects, and potential interactions among events. Guided by this analysis, ElecLoad adaptively chooses to forecast the entire forecast horizon directly or to partition it into segments according to changes in event effects. When the horizon is partitioned, sub-agents independently generate initial forecasts for each segment. The main agent then reviews these forecasts, and the sub-agents perform selective refinement guided by its feedback. Experiments on multiple electricity load datasets show that ElecLoad achieves state-of-the-art performance in most evaluation scenarios. Code is available at https://github.com/zhjai/ElecLoad.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决多事件影响下电力负荷难以准确预测的问题。研究背景方面，电力系统需要提前进行购电、发电调度和备用分配，准确的负荷预测对系统经济性与运行可靠性至关重要，而极端天气、大型体育赛事、电力系统运行事件等会使负荷偏离常规模式，Web 上的天气预警、新闻报道和运行通知可提供事件时间、区域等线索。现有方法的不足在于：通用预测方法虽能引入协变量或文本信息，MMGPT4LF、ITA-LF、NACF 等电力负荷方法也能对齐融合文本表示、分析新闻相关性方向与持续时间或编码新闻语义与发布时间，但它们多将上下文作为额外输入，尚未充分利用多事件效应及其相互作用来指导预测过程本身。本文的核心问题是：如何分析多个事件与目标负荷的相关性、其影响在预测窗口内出现的时间以及事件间可能的相互增强或抵消，并据此自适应地组织预测流程——直接预测整个窗口，还是按事件效应变化分段预测，再通过主代理审查与子代理选择性修正来提升逐时数值负荷预测及负荷峰值时机与幅度的准确性。

### Q2: 有哪些相关研究？

相关研究主要分为三类。方法类聚焦时序表示与外部条件建模：PatchTST用patch编码局部子序列，ConvTimeNet用可变形patch与层次卷积捕获多尺度依赖，TimeDART以因果Transformer结合扩散去噪进行自监督预训练，OneCast分解季节与趋势分量分别建模；Chronos-2与TimesFM-3支持带协变量的零样本预测，EventTSF将事件嵌入对齐到固定长度片段并自回归预测。LLM预测类将上下文理解与推理引入数值预测：TokenCast离散化时序为token并与上下文对齐，TimeReasoner进行多步推理，MemCast构建层次记忆引导推理与反思，AlphaCast以调查—生成—反思角色协作，CastFlow由冻结语言模型规划与反思、微调模型出数值预测，CastFSR自适应检索证据并反思修正局部不一致，MoiraiAgent将上下文预测与专家模型选择解耦。应用类针对电力负荷与事件信息：高斯过程迁移学习用异常事件下少量观测校准先验预测，News and Load及其后续工作将新闻与经济指标用于多horizon负荷预测，MMGPT4LF用GPT-2编码日历、温度与负荷趋势并经交叉注意力融合，ITA-LF用LLM agent分析新闻相关性与影响方向、时长并反思新闻选择，NACF以事件条件网络生成事实与反事实预测，AutoLFM用agent自动开发楼宇负荷预测器。区别在于：ElecLoad不把上下文仅作附加输入，而是分析多事件相关性、影响时机与事件间交互，并据此自适应决定直接预测全horizon或按事件效应变化分段，再由子agent生成初稿、主agent审查并选择性精修，从而将事件效应用于引导预测过程本身。

### Q3: 论文如何解决这个问题？

ElecLoad 的核心思路是让 LLM 智能体先理解“多个事件如何影响负荷”，再用这种理解自适应地组织预测流程，而非把上下文简单拼进输入。整体框架由主智能体与子智能体构成，二者共享同一套 LLM 参数（基于 Qwen3.5-4B），每次调用都接收完整的原始输入（历史负荷与上下文），并通过四个功能模块协同工作。

T1 事件分析与预测规划：主智能体分析每个事件与目标负荷的相关性、影响方向与“影响窗口”（含延迟响应与事后恢复），并考察事件先后顺序及效应叠加——是相互强化还是彼此抵消。据此它选择两条路径之一：直接预测整个预测域，或按事件效应变化（效应起始、衰减、恢复开始、多效应重叠变化）把预测域切分为若干连续、无重叠的时段。

T2 数值预测：直接路径下一次生成全段预测即结束；分段路径下各子智能体独立生成所属时段的初始预测，彼此不共享预测结果，以抑制自回归生成中的误差跨段传播，同时保留完整原始上下文以支持跨边界效应。

T3 选择性精化：主智能体检查初始预测与输入、事件分析、分段报告的一致性，选出问题最突出的一个时段给出诊断性反馈（可高亮关注区间），由对应子智能体修订；每轮修订后主智能体重新评估整体预测，在精化预算内决定继续或停止。

T4 边界协调：检查相邻时段接缝处的数值跳变是否符合事件起始、衰减或恢复，仅对接缝附近数值做 KEEP 或 REGENERATE 修补，分段结构保持不变。

训练上采用两阶段：先进行推理初始化（SFT+RL 学习基础数值预测与事件理解），再进行智能体优化，用 SFT 学习完整工作流演示、用 RL 以“预测误差+调用成本”的效用函数优化路径选择、精化决策与边界协调等角色行为。

### Q4: 论文做了哪些实验？

论文在多个电力负荷数据集上进行了实验，覆盖小时级家庭、区域和系统负荷，将每个电力系统视为一个域。域内数据包括GEFCom2014负荷赛道、Nord、PJM、SPP、LCL和iFlex；域外测试使用AEMO（96小时多日预测）和ERCOT（24小时日前预测）。Nord、PJM、SPP同时使用24小时和96小时预测窗口，GEFCom2014仅用96小时，LCL和iFlex仅用于日前预测。数据集总计2,935个案例，其中训练1,800、验证300、域内测试600、域外测试235。对比方法共14个外部基线，包括ARIMAX、LightGBM、PatchTST、TimeXer、EventTSF、TimesFM-3、Chronos-2、TimeReasoner、MemCast、AlphaCast、CastFSR、MMGPT4LF、NACF和ITA-LF。主要指标为WAPE，次要指标为NRMSE。结果显示，ElecLoad在22项指标比较中13项排名第一、6项排名第二，全部18项域内比较均进入前二；在GEFCom2014上相对最强基线MemCast将WAPE和NRMSE分别降低18.3%和18.6%；域外AEMO和ERCOT四项指标比较中排名第二至第四。此外还进行了消融实验（输入、规划、精炼、边界协调）、不同事件条件实验（无事件、单事件、多事件、无关事件）以及WAPE与token成本分析。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有以下几点。其一，事件效应建模依赖合成案例：GEFCom2014 的多事件数据是按预设幅度与时序人工注入的，真实电网中事件文本噪声大、效应强度未知，未来可引入真实公告与负荷的因果标注或弱监督学习，检验模型在开放域事件上的鲁棒性。其二，OOD 泛化仍不足：AEMO 与 ERCOT 上 ElecLoad 仅列第二至第四，说明事件语义与负荷模式的跨系统迁移有限，可探索事件类型层面的解耦表示或元学习式快速适配。其三，规划与精修机制较刚性：最多 4 段、每段至少 6 小时、精修预算 2 次均为固定超参，可让智能体自主学习分段粒度与预算分配，并结合不确定性估计决定何时停止。其四，事件交互仅考虑加性与顺序叠加，可引入图结构建模事件间的强化/抵消关系，并输出可解释的效应归因。此外，当前仅用 WAPE/NRMSE 评估，未来可加入概率预测与决策成本指标，并探索更小骨干模型以降低推理开销。

### Q6: 总结一下论文的主要内容

论文针对电力负荷预测中多事件影响随时间变化且相互叠加或抵消、难以准确预测的问题，提出 ElecLoad——一个上下文感知的多事件负荷预测智能体。其核心思路是：主智能体结合历史负荷与网页通知、天气预警等上下文，分析各事件与目标负荷的相关性、影响出现的时间窗口及事件间潜在交互，并据此自适应决定直接预测整个时段，还是按事件效应变化将预测区间分段；分段时由子智能体独立生成初始预测，主智能体审查并选择性反馈，子智能体迭代修正，最后进行边界协调。模型基于 Qwen3.5-4B，采用推理初始化与智能体优化两阶段训练。实验表明，ElecLoad 在多数评估场景（含域内多日与日前预测及跨域系统）取得最优或次优性能，验证了以事件效应变化引导预测过程的有效性。
