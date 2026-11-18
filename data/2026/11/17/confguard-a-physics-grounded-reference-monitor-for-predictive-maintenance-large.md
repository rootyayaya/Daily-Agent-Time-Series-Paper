---
title: "ConfGuard: a physics-grounded reference monitor for predictive-maintenance large-language-model agents"
authors:
  - "Arunkumar V"
  - "Gangadharan G. R."
  - "S. Senthilkumar"
date: "2026-11-17"
arxiv_id: "2611.22288"
arxiv_url: "https://arxiv.org/abs/2611.22288"
pdf_url: "https://arxiv.org/pdf/2611.22288v1"
categories:
  - "cs.AI"
  - "cs.CR"
  - "cs.LG"
tags:
  - "LLM Agent"
  - "预测性维护"
  - "物理约束"
  - "参考监控器"
  - "对抗攻击防御"
  - "传感器异常检测"
  - "C-MAPSS"
  - "工业故障诊断"
  - "时序报告生成"
  - "证据路由"
relevance_score: 8.5
---

# ConfGuard: a physics-grounded reference monitor for predictive-maintenance large-language-model agents

## 原始摘要

Large-language-model agents now close the industrial predictive-maintenance loop, reading sensor windows, retrieving procedures and dispatching work orders. Two attack channels meet there: injected text in a retrieved document can hijack the decision, and a bounded sensor perturbation can corrupt the remaining-useful-life estimate behind it. Recent agent defenses police data provenance and tool privilege but cannot tell whether a prognostic quantity is physically plausible. ConfGuard is a reference monitor with a physics-grounded policy. Its conformal monitor tests each prediction, anchored to the asset's admitted history, against degradation physics: capped remaining life never rises and falls at most one cycle per cycle. Calibrating its threshold over whole asset trajectories lets the operator set the expected share of a clean asset's windows the running monitor escalates. A physics-policy validator checks the agent's maintenance-urgency decision against the decision a deterministic policy derives from the same interval. On all 10,196 C-MAPSS test windows the monitor cuts a covert attacker's reach on healthy assets from 0.529 to 0.046 and closes suppression of failing assets (0.151 to 0), escalating 0.027 of clean windows against a 0.05 target, while the fixed physical range it replaces leaves both attacks open. Behind a Qwen3-14B planner the composed monitors hold urgency-class injection to 0.00 and the universal sensor attack to 0.12, against 0.29 and 0.54 for a defended prompt. An adaptive attacker defeats a Mahalanobis detector on 0.504 of windows and adversarial training on 0.485. We report an attack class the projection misses.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于工业预测性维护（PdM）中LLM智能体面临的安全风险。随着LLM智能体被用于读取传感器窗口、检索维修规程并派发工单，两条攻击通道同时威胁同一决策：检索文档中的注入文本可劫持智能体策略，而对传感器窗口的有界扰动可使剩余使用寿命（RUL）估计严重偏离。现有防御（如CaMeL、Progent、IPIGuard）沿用操作系统参考监视器思路，其策略建立在数据来源、工具权限与控制流之上，只能回答“智能体能否用来自不可信数据的参数调用该工具”，却无法判断维护决策是否与机器真实物理状态一致——例如对健康设备给出3个周期的RUL，虽在权限与来源上合法，却在物理上错误且代价高昂。本文的核心问题是：如何为PdM智能体构建一个以物理过程为基准的参考监视器，使其能够检验预测量的物理合理性。为此作者提出ConfGuard，利用保形预测区间与基于退化物理（剩余寿命不上升、每周期至多下降一个周期）的物理可行支撑，将交换性被破坏本身作为检测信号，并辅以物理策略校验器核对维护紧迫度决策，从而在有限样本下可控误报率地识别注入与传感器攻击。

### Q2: 有哪些相关研究？

本文的相关工作可分为三类。方法类：CaMeL从可信查询中提取控制流与数据流，在受限解释器中跟踪来源执行计划；Progent以策略语言表达工具调用的最小权限并强制单调约束；IPIGuard构建工具依赖图并拒绝越界调用；MELON则遮蔽用户提示重放轨迹并比对动作。这些系统与ConfGuard同属“模型外确定性策略”家族，但它们的策略作用于值的来源与工具权限，而ConfGuard作用于数值是否与资产物理模型一致，二者可组合使用。应用类：Spotlighting等提示级防御作用于模型输入而非动作，在自适应攻击下易失效；有工作将共形预测用于C-MAPSS的RUL区间报告，本文则将其作为运行时监测器的参照而不依赖其覆盖保证；物理信息网络、隐藏物理架构等方法让预测器f更可信，本文不对f作假设，只约束由f得出的决策，因而互补。评测类：已有工作提出RUL回归的通用对抗扰动及多变量时序PGD/FGSM/BIM攻击，并以对抗训练或离群检测加固预测器，但均未将预测对抗扰动传播至智能体回路、测量其对派发维修决策的影响，这正是本文填补的空白。

### Q3: 论文如何解决这个问题？

论文提出的 ConfGuard 是一个基于物理约束的参考监视器，嵌入在预测性维护 LLM 智能体的执行图中，由两个确定性检查组成。第一个是共形支持监视器 Gconf，运行在规划器之前，可弃权。它不采用固定的资产类别区间，而是以资产自身已接纳的历史为锚，构造“物理时钟”不变量：封顶剩余寿命非增，且低于封顶时每周期恰好下降一个周期。具体地，用最近 k 个已接纳预测的中位数构造下降锚 A↓ 与上升锚 A↑，并计算物理时钟得分 s(x_t)=max(B_lo−ℓ, A↓−f, f−A↑, 0)，超过阈值 τ_ρ 即弃权并转人工，且被拒窗口不进入历史以防污染。阈值校准按整条轨迹而非逐窗口进行，利用共形风险控制给出期望误弃权率不超过 ρ 的保证，并允许阈值形状 τ⁰ 与缩放 λ 分离。第二个是物理策略验证器 Vphys，运行在规划器之后、工具执行器之前，将智能体给出的维护紧迫度决策与由同一共形区间经确定性策略 πref 导出的决策比对，不一致或参数越界即拒绝，拒绝后允许一次有界重试，再转人工。创新点在于：用机器物理性质而非数据分布定义支持集，使上升攻击（抑制故障资产）也能被检测；以资产自身近期历史替代全舰队上限，使攻击预算随资产衰减而不随剩余寿命增长；以及整轨迹共形校准，在无需传感器分布假设下控制误报率。

### Q4: 论文做了哪些实验？

论文在三个RUL回归基准上评估：C-MAPSS FD001（单一工况，隔离机制）、FD004（六工况两故障模式，检验Mondrian分区与工况漂移下的鲁棒性）和MetroPT-3（真实流式数据）。骨干为双向LSTM回归器，窗口长度30，C-MAPSS的RUL截断于125周期；共形校准α=0.1，FD001上q̂=27.89周期；监控阈值ρ=0.05，在1745个干净验证窗口上校准，测试引擎交叉拟合（FD001各50台、FD004各124台）。规划器为Qwen3-14B（Q4_K_M，温度0，JSON约束解码），另有四个其他模型族的开放规划器。攻击库包括A0干净、A1-a紧迫度类注入（200条，四目标四编码）、A1-b投影外注入、A2通用传感器扰动、A3混合攻击、A4-s规避型传感器攻击与A4-t策略一致注入；对比对象为固定物理范围、防御性提示、Mahalanobis检测器和对抗训练。主要结果：全部10,196个C-MAPSS测试窗口上，监控器将隐蔽攻击者对健康资产的攻击成功率从0.529降至0.046，将故障资产抑制从0.151降至0，干净窗口升级率0.027（目标0.05）；Qwen3-14B后紧迫度注入保持0.00、通用传感器攻击0.12，而防御性提示为0.29和0.54；自适应攻击者分别以0.504和0.485的成功率击败Mahalanobis检测器与对抗训练。

### Q5: 有什么可以进一步探索的点？

论文的局限主要有三：其一，威胁模型被窄化为“紧迫度类别翻转”，对零件号、技师资质、服务窗口等未保护字段不作覆盖声明，作者以期望损失论证其合理性，但未量化这些坐标被污染后的级联风险；其二，A2（传感器攻击）臂仅条件成立，依赖松弛不等式这一经验量，在高松弛输入上会失效，且慢速持续漂移可移动时钟锚点，使共形监测失去参照；其三，物理策略验证器在传感器攻击通过 Gconf 时反而会“强制执行被污染决策”，有界重试还会迫使原本会犹豫的规划器顺从，形成防御反噬。未来可探索：将参考监视器从单点区间扩展到多资产、跨工序的退化一致性约束，用图结构物理先验替代“剩余寿命不回升”这一单调度量；对锚点引入不可篡改的硬件根或时间序列水印，抵御慢漂移；把验证器改为“拒绝并请求人类复核”而非强制合规，切断反噬路径；并针对投影外攻击类别建立分级损失感知的覆盖度量，而非二元通过/拒绝。

### Q6: 总结一下论文的主要内容

论文针对工业预测性维护中 LLM 智能体面临的两类攻击——检索文档注入文本与传感器窗口有界扰动——提出 ConfGuard 参考监视器。现有防御只校验数据来源与工具权限，无法判断预测值是否符合物理规律。ConfGuard 将策略建立在物理过程之上：第一道门是共形支持监视器，以设备自身已接纳历史为锚，检验预测是否满足退化物理约束（剩余寿命不上升、每周期至多下降一个周期），并按整条轨迹校准阈值，使操作者可设定干净窗口的期望升级率；第二道门是物理策略校验器，将智能体给出的维护紧迫度与确定性策略从同一区间导出的决策比对。在 C-MAPSS 全部 10,196 个测试窗口上，隐蔽攻击者影响从 0.529 降至 0.046，故障设备压制攻击从 0.151 降至 0，干净窗口升级率 0.027 低于 0.05 目标；在 Qwen3-14B 规划器后，紧迫度注入成功率降至 0.00，通用传感器攻击降至 0.12。论文还给出检测能力与操作余量的定量关系，并指出未防御的攻击类别。
