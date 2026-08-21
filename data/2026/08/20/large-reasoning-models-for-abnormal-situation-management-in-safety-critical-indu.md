---
title: "Large reasoning models for abnormal situation management in safety-critical industrial processes"
authors:
  - "Khalid Alhazmi"
date: "2026-08-20"
arxiv_id: "2608.19819"
arxiv_url: "https://arxiv.org/abs/2608.19819"
pdf_url: "https://arxiv.org/pdf/2608.19819v1"
categories:
  - "eess.SY"
tags:
  - "LLM/Agent for time series anomaly detection"
  - "fault diagnosis"
  - "industrial process safety"
  - "tool use"
  - "programmatic verification"
  - "reasoning model"
  - "abnormal situation management"
  - "root-cause analysis"
  - "auditable decision chain"
relevance_score: 8.5
---

# Large reasoning models for abnormal situation management in safety-critical industrial processes

## 原始摘要

Automation operates safety-critical processes inside their design envelope and leaves abnormal situations to human operators. Mismanagement of these situations is a leading contributor to process-safety incidents and a hindrance to achieving autonomy. Here we show that a general-purpose large reasoning model, with no task-specific training and only the information available to an operator, manages abnormal situations at run time through a bounded, programmatically verified action interface. Across 39 abnormal situations and operating-point changes on a plant-wide industrial benchmark process, the reasoning model maintained the plant within all hard constraints in all 39, while basic regulatory control failed in 15. It matched the plant's expert-engineered advanced control and diagnosed the root-cause fault in 15 of 15 safety-critical situations. Three independently developed models spanning a thirty-fold cost range exceeded the baseline. In a fully auditable evaluation, these results demonstrate run-time abnormal situation management without a human in the loop.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于安全关键工业过程中的异常情况管理（ASM）问题。研究背景是：现代自动化系统在设计包络内已能媲美甚至超越人类专家，但异常工况（如设备退化、传感器故障、设计基准外扰动）仍依赖控制室操作员手动处理，而操作失误是过程安全事故的主要诱因。现有方法的不足体现在三方面：一是传统控制层级（如PID、MPC）仅在过程模型有效且处于设计包络内时才能保证约束满足，一旦超出包络便失效；二是安全仪表系统只能通过停车（trip）进入安全状态，但化工过程停车会引发启停瞬态，反而集中安全风险；三是大语言模型此前仅被用于控制回路外的辅助角色（如故障诊断、高层规划），缺乏闭环性能的共享基准测试，且模型对物理过程的权限范围与输出验证方式未被精确量化，导致其因“随机性”被排除在安全关键回路之外。本文核心问题是：能否让一个通用大推理模型，在无任务特定训练、仅凭操作员可得信息的情况下，通过一个有界且程序化验证的动作接口，在运行时可靠地执行异常情况管理，从而在无需人工介入的前提下维持工厂运行在硬约束内，并匹配专家设计的先进控制性能。

### Q2: 有哪些相关研究？

相关研究主要分为以下几类：

**方法类**：一是将大语言模型（LLM）用于控制设计阶段，如奖励合成、控制器调参、代码生成和将自然语言目标转化为可执行规范；二是运行时的高层规划与故障诊断，但通常不具备执行权限，且容忍延迟和偶发错误。本文与这些工作的区别在于，将推理模型置于闭环控制回路之上，通过有界且可编程验证的动作接口直接干预运行，而非仅做离线辅助或低维可行性演示。

**应用类**：已有研究尝试将LLM嵌入经典控制回路，但多为低维演示，缺乏稳定性保证和约束满足性验证。本文在田纳西-伊斯曼工业基准上实现了全厂范围的异常工况管理，覆盖39种场景，且模型无需任务特定训练，仅依赖操作员可见信息。

**评测类**：近期评估指出过程控制是LLM在过程系统工程中成熟度最低的应用，呼吁建立共享基准和失败模式表征。本文回应了这一需求，提供了首个可比较的闭环基准和审计协议，并量化了模型与验证机制各自对安全性的贡献，同时对比了三种独立开发的推理模型，跨越三十倍成本范围。

### Q3: 论文如何解决这个问题？

论文提出了一种基于大型推理模型的异常工况管理（ASM）层，部署在工业过程现有的分散式比例积分（PI）调节层之上，无需任何任务特定训练即可在运行时管理异常工况。整体框架包含四个核心组件：过程状态摘要生成器、有界动作接口、程序化验证器和前向仿真器，由两部分的提示词驱动。

在每次模型调用时，ASM软件首先从测量信号中计算派生量，包括约束裕度及带符号的到达极限时间、趋势斜率、控制器诊断、一致性残差和投影值，形成token受限的过程状态摘要，替代原始测量向量。模型基于此摘要返回一个来自预定义十二项词汇表的诊断和一个来自有界接口的动作，该接口仅允许设定点变更、配置激活、预审计程序、无动作或有序停机，直接操作执行器不可表示。

关键技术在于程序化验证器，它对每个提议执行静态检查（接口成员、范围、速率、冷却时间和预算）以及影子前向仿真——在名义模型上模拟6小时闭环，比较提议动作与保持动作，若预测会触发联锁或比保持更早触发则拒绝，并返回机器可读原因允许一次修订。前向仿真同时服务于模型推理（查询候选动作效果）和架构保护（影子回滚验证）双重角色。

创新点包括：将慢速监督推理与快速调节控制解耦的架构设计；通过程序化验证实现有界安全保证；过程无关的提示词设计使系统可迁移到不同过程仅需重新生成过程描述；以及零样本推理能力，在39个异常工况中全部维持硬约束，诊断准确率达84.6%。

### Q4: 论文做了哪些实验？

论文在田纳西-伊士曼（Tennessee Eastman）工业基准过程上进行了系统实验，涵盖39个情景（13类场景×3个配对噪声种子）。实验设置包括三类测试：5个无需干预场景（基线可维持约束）、5个安全缺口场景（基线触发联锁但参考控制器可恢复）、3个质量缺口场景（产品等级设定点变化超出基线跟踪能力）。对比方法包括基线监管控制、专家设计的参考控制器、以及Claude Sonnet-5（高/低推理强度）、GLM-5.2和DeepSeek-V4-Flash三个推理模型，均采用零样本提示和相同的受限动作接口。

主要结果：基线在39个情景中仅24个维持约束（15个安全缺口全部跳闸），而Sonnet-5高推理强度在所有39个情景中均维持约束，配对差异+0.385（95% CI [+0.22, +0.54]，McNemar p=6×10⁻⁵）。参考控制器同样达到39/39，与模型无差异。三个模型均显著优于基线（差异+0.33至+0.39），成本跨度超过30倍（每情景0.07至2.32美元），最便宜的DeepSeek-V4-Flash也达到100%约束维持率。在安全缺口类中，模型15/15正确诊断根因，而脚本规则表仅2/15。一个关键案例显示，Sonnet-5低推理强度在S4场景中误诊为阀门粘滞导致跳闸，高推理强度正确识别反应物成分失衡并稳定运行。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下方向展开：首先，当前验证仅基于单一仿真平台，需在第二类化工过程或连续/批处理混合流程中验证架构的通用性，并量化“仿真到现实”的差距，尤其是模型对真实扰动和噪声的鲁棒性。其次，现有逐动作验证无法捕捉跨时间步的轨迹级风险，未来应开发基于滚动时域或因果推理的轨迹验证器，以识别“逐步安全但整体危险”的序列。第三，诊断与干预的耦合机制尚不清晰，可引入可解释的根因定位模块，将推理过程与物理约束显式关联，提升故障归因的可靠性。此外，当前模型在安全恢复后过度减产，可设计自适应恢复策略，在约束满足后动态调整生产负荷，平衡安全与经济性。最后，需构建能区分不同推理模型能力的更严苛场景库，并探索多模型集成或分层决策框架，以增强对未预演异常的处理能力。

### Q6: 总结一下论文的主要内容

该论文展示了通用大推理模型在安全关键工业过程中的异常情况管理能力。问题定义上，传统自动化系统在异常情况下需人工干预，而管理不善常导致安全事故。方法上，模型无需任务特定训练，仅通过操作员可得信息和有界、程序化验证的动作接口，在运行时管理异常情况。在包含39种异常场景和操作点变化的工业基准测试中，模型在所有场景中维持工厂硬约束，而基础控制失败15次；其性能媲美专家设计的先进控制，并在15个安全关键场景中准确诊断根因故障。三个独立模型（成本跨度30倍）均超越基线。结论表明，通用推理模型结合有界接口和独立验证层，可在无人工干预下实现运行时异常管理，为部署自主系统提供了可审计的架构范式，但研究局限于仿真环境，未与人类操作员比较。
