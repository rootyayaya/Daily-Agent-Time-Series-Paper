---
title: "Guarded Agent-in-the-Loop Residual Adaptation for Evolving Wind Power Regimes"
authors:
  - "Yuhang Dong"
  - "Min Xia"
  - "Jinghong Li"
  - "Yue Dai"
  - "Xinyue Wang"
  - "Shi Liang"
date: "2026-10-26"
arxiv_id: "2610.34968"
arxiv_url: "https://arxiv.org/abs/2610.34968"
pdf_url: "https://arxiv.org/pdf/2610.34968v1"
categories:
  - "cs.MA"
tags:
  - "Agentic Time Series"
  - "LLM/Agent 用于时间序列"
  - "残差适应"
  - "场景感知路由"
  - "风功率预测"
  - "预测性维护"
  - "在线学习"
  - "专家混合"
  - "工业传感器解释"
  - "可解释诊断链"
relevance_score: 8.5
---

# Guarded Agent-in-the-Loop Residual Adaptation for Evolving Wind Power Regimes

## 原始摘要

Wind power forecasting models are often deployed as fixed temporal backbones, but the errors they make can vary across meteorological regimes such as cold waves, heat-and-calm periods, productive typhoon, and destructive storms. We present a guarded Agent-in-the-loop residual adaptation framework that leaves the temporal backbone unchanged and adapts only a small set of scene-conditioned residual experts. An Agent layer interprets external scene information, identifies the current regime, selects residual experts, and applies a correction only when recent observed errors support it. New experts enter the pool after they outperform their initializations on a validation set, keeping model growth under explicit control. Backbone-only and Agent-enhanced forecasts are compared at lead times of 4, 8, 12, 24, and 48 across nine time-series backbones. Across these runs, the guarded framework lowers both MAE and RMSE for all 45 backbone-horizon combinations, with average MAE reductions ranging from 11.21% to 20.26% across backbones. Online-selection baselines, component ablations, and routing analyses identify the roles of residual experts, scene-aware routing, and the online acceptance rule. Candidate-scene runs evaluate the promotion path under controlled conditions; long-term unattended deployment was not evaluated.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决风电功率预测模型在部署阶段难以适应气象场景变化的问题。研究背景是：短期风电预测普遍采用神经时间序列骨干模型，将历史功率、风机信号和气象输入映射为未来发电量，时间建模能力已显著提升，但部署方式基本是静态的——训练完成后，同一套映射被用于常态运行、寒潮、高温无风、台风增产和破坏性风暴等截然不同的场景。现有方法的不足在于：仅用输入分布漂移不足以刻画部署难题，因为这些场景还会重塑原本较强的时间模型所留下的残差误差结构；而重新设计骨干模型代价高、风险大，且缺乏对修正何时可以启用的显式控制，容易在证据不足时盲目适配。因此本文的核心问题是：在不改动时间骨干的前提下，如何利用外部场景信息识别当前气象状态、路由到场景条件化的残差专家，并且只在近期观测误差支持时才接受修正，从而把适配从骨干重设计转化为受控的残差控制，同时把模型增长控制在显式规则之下。

### Q2: 有哪些相关研究？

本文的相关研究主要分为三类。方法类上，现有风电预测工作多聚焦于改进时间预测器本身，包括基于注意力的序列建模、高效Transformer、循环概率预测、可解释多步网络与神经基展开模型，以及近年通过稀疏注意力、分解、频率建模、patch token、时序变化建模和倒置通道表示增强骨干的长序列模型；本文将这类模型视为可复用的时间引擎，重点不在替换骨干，而在残差路径上引入可审计的Agent层。条件计算与轻量适配方面，混合专家方法将输入路由到专用参数，LoRA式更新表明适配无需改动全部参数；本文与它们最接近，但选择对象是骨干之后的残差专家，且每次比较保持预测骨干固定，并非独立的MoE或适配器基准。部署与评测类上，在线专家加权、动态模型平均、选择性预测与概率预测评估提供了“守卫式”部署视角，但其目标与本文不同：本文关注守卫式残差控制，并借助证据Agent、场景Agent、路由Agent与候选场景Agent分工完成在线适配与注册验证。持续学习关注能力保持与扩展，本文则强调稀有事件证据稀疏和未来泄漏风险下的显式职责划分；多模态编码器与语言模型Agent为证据层提供接口，数值预测器仍保持独立。

### Q3: 论文如何解决这个问题？

论文提出“带守卫的智能体在环残差自适应”框架，核心思想是冻结原有时间序列骨干模型，只让智能体层根据场景证据选择并门控少量残差专家来修正预测。整体流程为：先将异构场景证据（历史功率与SCADA、气象、视觉/现场证据、事件上下文）编码为因果输入包并映射为场景状态；智能体层据此决定动作，骨干网络输出基础预测，智能体再叠加残差修正。系统由四组智能体构成：外部证据智能体对齐异步数据源、去除可能泄漏标签的元数据，并用冻结的视觉语言编码器融合卫星、图像、视频和报告证据；场景认知与决策智能体将场景表示与已知场景原型记忆比对，输出已知场景概率、未知置信度和路由或候选决策；路由智能体把场景信念转为专家权重，采用自适应与均匀混合的软路由防止专家坍缩；在线残差接受智能体维护滚动误差账本，用MAE、RMSE和分位数误差构造因果可靠性分数，只有超过阈值才接受修正。对于新场景，新颖性智能体缓冲候选窗口，参数演化智能体从最近已验证专家插值初始化虚拟残差专家，仅在验证集上优于初始化一定幅度后才允许入池，骨干始终冻结，并由大语言模型生成可审计的注册表描述。创新点在于将模型演化限制为残差专家路由与验证门控的池更新，使增长可控、过程可审计，并在45个骨干-预测步组合上同时降低MAE和RMSE。

### Q4: 论文做了哪些实验？

论文在空间动态风电预测数据集（SDWPF功率/SCADA记录，结合气象事件资源、IBTrACS热带气旋记录与脱敏卫星快照）上开展实验，所有骨干网络采用相同的时间顺序训练/验证/测试划分、输入长度与预测步长，评估提前期为4、8、12、24、48步，指标为相对配对基线的MAE与RMSE降低。实验一在9个时间序列骨干（PatchTST、PatchTST-Zoo、GTR-PatchTST、FACT、CrossLinear、XLinear、TQNet、TimeBase、DFreqLinear）上比较多步预测，结果显示全部45个骨干-步长组合的MAE和RMSE均下降，各骨干平均MAE降低11.21%（DFreqLinear）至20.26%（TimeBase），RMSE降低7.52%至14.97%；移动块自助法给出总体MAE降低15.72%（95%区间15.44–15.99%）、RMSE降低10.68%（10.46–10.94%）。实验二将场景条件残差修正与通用上下文向量对比，并进行候选场景流证据边界检查。消融显示仅残差池带来5.50% MAE与3.33% RMSE降低，加入在线门控后提升至15.57%与10.59%。在线选择基线对比中，Agent门控MAE降低15.77%、RMSE降低10.77%，优于EMA（13.89%/9.31%）、DMA、Hedge、随机匹配覆盖等，接近非因果Oracle上界（20.70%/13.22%）。

### Q5: 有什么可以进一步探索的点？

论文的局限主要在于：长期无人值守演化未评估，新专家晋升依赖有限候选场景，稀有事件（如破坏性风暴）样本支撑不足，且缺少延迟与参数量分析；LLM仅用于场景证据编码，数值Agent与场景信念的耦合仍较浅。未来可探索：一是在多风电场、跨区域事件不相交数据上验证专家池的持续演化与遗忘问题，引入专家淘汰与合并机制控制池规模；二是将场景信念建模为带不确定性的概率分布，使守卫规则从“接受/拒绝”扩展为置信度加权的软校正；三是把事后诊断日志转化为在线反馈，形成“预测—复盘—再训练”闭环；四是补充推理延迟、显存与边缘部署成本评估，并研究极端稀有事件下的小样本专家初始化与合成场景增强；五是将该残差适配框架迁移到光伏、负荷等其他受气象 regime 影响的时序任务，检验其通用性。

### Q6: 总结一下论文的主要内容

论文针对风电功率预测模型部署后固定不变、难以适应寒潮、高温静风、台风等气象场景导致残差误差变化的问题，提出一种带防护的Agent在环残差自适应框架。其核心思想是保持时间序列骨干网络不变，仅通过Agent层解读卫星、气象、事件等外部场景信息，识别当前场景并路由一组场景条件残差专家，且仅当近期观测误差支持时才接受修正；新专家须在验证集上优于初始化后才允许入池。实验在9种骨干网络、4至48步预测跨度共45个组合上均降低MAE和RMSE，平均MAE降低11.21%至20.26%，消融与在线选择对比表明残差专家、场景感知路由和在线接受规则各自发挥作用。该工作将时间建模、场景推理与残差修正解耦，为可审计、可控的预测自适应提供了新范式。
