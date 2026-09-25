---
title: "WeatherDiagFlow: Evidence-Grounded Radar Nowcasting with Diagnostic Flow Refinement"
authors:
  - "Chunlei Shi"
  - "Yufeng Zhu"
  - "Yixiao Liang"
  - "Dan Niu"
  - "Yongchao Feng"
  - "Qiliang Wu"
  - "Jiong Wang"
date: "2026-09-24"
arxiv_id: "2609.29772"
arxiv_url: "https://arxiv.org/abs/2609.29772"
pdf_url: "https://arxiv.org/pdf/2609.29772v1"
categories:
  - "cs.LG"
  - "cs.MM"
tags:
  - "雷达临近预报"
  - "证据接地报告生成"
  - "多智能体工作流"
  - "可审计验证"
  - "结构化诊断证据"
  - "预报-公报-审计任务"
  - "工业气象诊断"
  - "泄漏控制协议"
  - "时序语义报告"
  - "Agentic Time Series"
relevance_score: 8.5
---

# WeatherDiagFlow: Evidence-Grounded Radar Nowcasting with Diagnostic Flow Refinement

## 原始摘要

Radar nowcasting is essential for short-term warning and emergency response, yet conventional systems mainly return future radar fields and provide limited support for operational communication and post-event verification. We formulate radar nowcasting as an evidence-grounded forecast--bulletin--audit task, in which a numerical forecaster produces both future radar fields and structured diagnostic evidence. Forecast-time bulletins use only model-available evidence, whereas post-event audits incorporate future radar truth only after the forecast horizon is observed. Based on this task formulation, WeatherDiagFlow predicts motion, growth and decay, heavy-echo risk, and uncertainty to condition rolling flow refinement, while frozen-scaffold residual calibration improves long-lead strong-echo preservation. A multi-agent layer converts the structured evidence into operational bulletins and independently generates verification audits without feeding textual outputs back into the forecaster. Experiments on FJRADAR demonstrate competitive overall performance and improved strong-echo event skill. WeatherDiagFlow therefore connects numerical prediction, evidence-grounded reporting, and auditable verification under a leakage-controlled protocol.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

雷达临近预报对强对流预警、城市防汛和航空保障至关重要，但现有数据驱动方法大多遵循“预测中心”范式，即直接把历史雷达回波映射为未来反射率场。这类方法存在两方面不足：一是随预报时效增加，强回波容易被平滑、弱事件偏差加剧，而仅用MAE等平均误差指标无法反映对预警最关键的强回波保持能力；二是模型通常只输出未来场，缺乏关于位移、生消、强回波风险与不确定性的结构化证据，难以支撑业务发布与事后核验。与此同时，数值预报、业务通报与事后审计彼此割裂：语言模型生成的报告可能缺乏数值依据，而基于未来观测的核验信息又绝不能回流到已发布的预报中。因此，本文要解决的核心问题是：如何将雷达临近预报重构为一个“有证据支撑的预报—通报—审计”任务，在严格的信息边界下，让数值预报器同时输出未来雷达场和结构化诊断证据，并由多智能体层生成业务通报与独立核验，从而在提升强回波预报技巧的同时实现可追溯、可审计的业务闭环。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，数据驱动雷达临近预报已从循环和卷积预测器发展到生成模型、残差扩散、级联、局部感知和运动感知模型，近期还探索像素空间流生成、结构化雷达表示和物理引导动态关系。本文与这些工作的区别在于：多数方法采用以预测为中心的范式，直接将雷达历史映射到未来反射率场，随预报时效增加易丢失强回波，且不提供位移、生消、强回波风险和不确定性的结构化证据；WeatherDiagFlow则将这些诊断量作为条件引导滚动流细化，并通过冻结骨架残差校准保持长时效强回波。应用类方面，已有研究将多模态模型和LLM智能体用于天气报告生成和极端天气预警，但数值预报、业务报告与事后核验彼此分离。本文通过多智能体层将结构化证据转为业务公报并独立生成核验审计，且不将文本输出反馈给预报器。评测类方面，本文提出证据接地的“预报—公报—审计”任务，在FJRADAR上采用泄漏控制协议，明确区分预报时可用证据与事后雷达真值，避免未来观测进入已发布指导。

### Q3: 论文如何解决这个问题？

论文将雷达临近预报重构为“证据锚定的预报—公报—审计”任务，并据此提出 WeatherDiagFlow 框架。整体上，系统先由粗预报器根据过去10帧生成未来30帧的确定性“脚手架”，提供低方差的整体位移与覆盖估计，避免后续模块重复学习整个预报时段。随后，诊断编码器仅利用历史与粗预报，输出运动场、回波增长/衰减、强回波风险与不确定性四类结构化证据，分别以未来真值、亮度恒常与平滑约束进行监督，但这些真值只用于训练，不作为预报时条件输入。

核心预测模块是滚动流细化：将30帧分为三个1小时片段，在每个片段内以像素空间流模型估计速度场，条件包括当前噪声插值、滚动上下文、粗预报及诊断证据，通过8步欧拉积分生成该片段，并更新上下文进入下一片段。为抑制自回归误差放大，方法冻结粗诊断流脚手架，仅学习残差修正，并采用正负残差分离缩放、软回波面积与质量匹配、时间趋势一致性、持续回波保护及混合历史训练；下一片段上下文锚定于粗预报，减少反馈漂移。抗衰减扩展进一步加入漏报惩罚、可微CSI、面积与质量保持及后期片段加权。

最后，多智能体层将数值输出转化为三类产品：预报时公报仅使用模型可用证据，事后审计在真值到达后加入误差、漏报、虚警与不确定性重叠等证据；五个角色智能体分别完成报告生成、指标评判、视觉一致性、质量评估与风险分级，且文本不回流至预报器，保证无泄漏的可审计验证。

### Q4: 论文做了哪些实验？

论文在FJRADAR福州雷达组合反射率数据集上开展实验，样本为300×270、10帧历史输入与30帧未来输出（间隔6分钟），按时间划分训练/验证/测试集（30,665/6,345/2,125），并筛选未来任一帧有≥5%有效像素超10 dBZ的事件子集。所有方法共享2,125例测试清单，指标在有效掩码上全局池化计算，包括SSIM、LPIPS、CSI10/20/30、POD20/30、HSS20/30。对比基线有SmaAt-UNet、Rolling pMF+coarse、DiffCast、CasCast/EarthFormer、exPreCast。主要结果：WDF-RC-AD取得最佳SSIM 0.3730、LPIPS 0.2146、CSI20 0.2448、CSI30 0.1351、POD30 0.3384、HSS30 0.2273；CasCast在CSI10（0.3110）上最强。消融显示残差校准将CSI30/POD30从0.0274/0.0298提升至0.1284/0.3005，AD进一步达0.1351/0.3384。诊断分支检查中，运动残差0.0151、增长MAE 2.2935、风险CSI 0.2078、POD 0.2603、FAR 0.3624、不确定性与误差相关性0.3706。另构建32例任务集评估公告与审计质量。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：一是诊断证据仅覆盖运动、生消、强回波风险与不确定性四类，缺乏对风暴形态演变、多单体相互作用等更复杂动力过程的刻画；二是多智能体层生成的公报与审计质量尚未通过预报员主观评估或业务可用性指标验证，仅停留在自动指标层面；三是实验仅在FJRADAR单一数据集上完成，跨区域、跨季节的泛化性未知。未来可探索的方向包括：引入物理约束或雷达回波三维结构信息以增强证据的可解释性；将公报有用性纳入人机协同评估框架，形成预报员反馈闭环；设计自适应证据边界机制，在保证无泄漏前提下动态调整预报时可用信息；此外，可将该框架扩展至降水临近预报之外的对流初生、雷暴大风等灾害性天气诊断任务，并探索诊断证据与数值模式集合预报的融合路径。

### Q6: 总结一下论文的主要内容

论文将雷达临近预报重新定义为“预报—公报—审计”三位一体的证据落地任务：数值预报器不仅输出未来雷达场，还输出运动、回波生消、强回波风险与不确定性等结构化诊断证据。方法上，WeatherDiagFlow 利用这些证据条件化滚动流细化，并通过冻结骨架残差校准（WDF-RC）提升长预报时效下强回波的保持能力；多智能体层将结构化证据转为业务公报，并独立生成事后验证审计，且文本输出不回馈预报器，从而严格控制未来观测泄漏。在 FJRADAR 数据集上，该方法整体性能具竞争力，强回波事件技巧提升。其意义在于把数值预测、证据化报告与可审计验证统一在防泄漏协议下，增强临近预报的业务沟通与事后核验能力。
