---
title: "Verifiable abstention makes AI leak diagnosis accountable in water distribution networks"
authors:
  - "Tianwei Mu"
  - "Yue Wang"
  - "Mingzhe Yuan"
  - "Manhong Huang"
  - "Wenhong Wang"
  - "Xuerui Yin"
  - "Qing Luo"
  - "Min Xiao"
  - "Hui Yang"
  - "Jun Li"
  - "Dan Xue"
date: "2026-08-19"
arxiv_id: "2608.18836"
arxiv_url: "https://arxiv.org/abs/2608.18836"
pdf_url: "https://arxiv.org/pdf/2608.18836v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "可解释故障诊断"
  - "LLM/Agent"
  - "可验证弃权"
  - "数字孪生"
  - "证据路由"
  - "监督者-执行者架构"
  - "工业传感器解释"
  - "预测性维护"
  - "自然语言报告"
relevance_score: 9.5
---

# Verifiable abstention makes AI leak diagnosis accountable in water distribution networks

## 原始摘要

Utilities lose a substantial share of treated water to leakage, yet rarely trust artificial-intelligence localizers to dispatch crews: guessing everywhere cannot justify excavation. The gap is accountability, not accuracy: no method proves when it should not act. Here we recast leak localization as decision-making under verifiable abstention. A physics-grounded executor agent falsifies hypotheses (leak, demand, sensor, valve) against a digital twin; an independent supervisor agent, with a large-language-model (LLM) auditor, checks evidence against a code-verifiable contract, then certifies a dispatch, requests evidence or abstains. Under field-grade noise, a 32% forced baseline becomes 96% decision precision on acted events. On an independently generated benchmark it acts on only 4 of 33 leaks, all correct. A 194-event register of audited real leak locations with twin-simulated pressures and flows yields five excavation dispatches, three correct, and 44% survey recovery at full district precision. Accountable abstention offers a defensible route to autonomous water-infrastructure operation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

供水管网漏损造成大量水资源浪费，但人工智能定位器因缺乏问责机制而难以被信任用于实际调度：现有方法在野外噪声下准确率仅30-40%，却被迫对每个事件给出猜测性定位，错误开挖代价高昂。核心矛盾并非精度不足，而是系统无法证明“何时不应行动”——即缺乏可验证的弃权能力。

现有方法存在三重缺陷：一是数据驱动定位器强制输出答案，无法表达不确定性；二是选择性分类或保形预测虽可弃权，但仅基于标量分数，缺乏可审计的推理依据；三是新兴LLM智能体虽能编排仿真，却不具备行动门控功能。逆问题本身病态（候选位置远超传感器数），且异常来源混杂（需求波动、传感器漂移、阀门误操作均产生类泄漏信号），使盲目行动风险极高。

本文创新性地将漏损定位重构为“可验证弃权下的问责决策”：由物理驱动的执行体智能体在数字孪生中证伪竞争假设，独立监督智能体依据代码可验证的契约和LLM审计员核查证据，最终签发调度证书、索要补充证据或提供弃权档案。该框架将强制基线32%的决策精度提升至行动事件上的96%，在独立基准上仅对4处泄漏行动且全部正确，实现了从“预测精度”到“可辩护决策”的目标转变。

### Q2: 有哪些相关研究？

本文的核心创新在于将漏损定位从“预测精度”转向“可验证弃权下的问责决策”，其相关研究可归为四类：

**方法类**：传统数据驱动定位器（如图神经网络、突发检测序列模型、迁移学习、物理信息模型）及BattLeDIM基准，均强制对每个事件输出排名猜测，在实地噪声下精度仅30-40%，无法证明何时不应行动。本文以数字孪生作为证伪工具，通过执行器-监督器双智能体架构实现可审计弃权，区别于仅提供标量覆盖保证的选择性分类、学习延迟和共形预测。

**应用类**：水行业新兴的LLM智能体（如自然语言驱动水力仿真、领域适配的效用知识工作模型）虽能编排仿真和提供可解释性，但缺乏问责门控——智能体可调用模拟器却无法证明不应行动。本文将LLM仅用于规划和独立审计，所有决策数值均来自物理工具。

**评测类**：现有基准（如BattLeDIM L-Town）仅评估定位精度，本文引入独立生成的基准和194条实地审计记录，新增“弃权质量”和“决策精度”指标，并设计32包腐败压力测试验证审计器的可靠性。

**核心区别**：本文首次将“不行动”转化为可证明、可审计的结果，通过代码可验证的六项硬谓词合约和独立LLM审计器，实现执行与评判的分离，杜绝自我评分共谋。

### Q3: 论文如何解决这个问题？

该论文将漏损定位重新定义为“可验证弃权”下的决策问题，核心创新在于构建了一个“执行器-监督器”双智能体架构，使AI系统在无法提供可靠证据时主动弃权，而非强行猜测。

整体框架分为三大模块。**执行器**（橙色）负责生成和检验假设：它枚举互斥的假设空间（拓扑分区漏损、区域需求异常、传感器故障、阀门误状态或无异常），将每个假设在WNTR/EPANET数字孪生中实例化，通过残差似然函数剔除无法复现观测数据的假设，再用带奥卡姆惩罚的贝叶斯后验融合幸存假设，防止过灵活的漏损拟合伪装成需求异常。**监督器**（蓝色）不进行定位，只审计数值证据包是否满足目标合约——六个确定性谓词（存在性、区域大小、裕度、替代假设、物理复现、安全性）的合取。**LLM审计器**仅作为附加否决层，可拒绝但不可推翻硬检查失败的结果。

关键技术在于三点：一是物理驱动的假设检验，所有进入决策的数字均来自物理工具，语言模型仅在规划器选择需额外审查的非漏损假设和审计器审查数值摘要时介入；二是可验证弃权机制，系统输出三类结果——带SHA-256签名证书的行动、供人工审查的弃权档案、或触发主动感知的证据请求；三是拓扑感知检索库仅作为证据源之一而非答案，配合Leiden液压分区和传感器优化布置构成离线计算的空间支架。该设计使系统在被迫回答时精度仅32%，但通过弃权将行动决策精度提升至96%。

### Q4: 论文做了哪些实验？

论文在供水管网泄漏诊断中构建了“执行器-监督器”双智能体系统，并设计了统一的五维评估协议。实验覆盖五个网络：EXA7（381节点/15区/30传感器）、KY4、City H、City D及第三方基准L-Town，另含City D的194条真实泄漏工单（含双胞胎模拟压力/流量）。在模拟数据上，每网络生成550个事件（5种子），涵盖泄漏（2-50 L/s）、需水量异常、传感器故障和阀门误操作，噪声σ=0.05m（L-Town用竞赛噪声，现场寄存器σ=0.15m）。

对比方法包括强制top-1检索定位器、四种训练型定位器（最强余弦kNN达72.0%）、标量存在阈值基线。主要结果：EXA7上强制检索仅31.7%准确率，执行器提升至81.7±5.0%；监督器在40.5%覆盖率下决策精度达96.0%，收紧残差门控可达100%精度（13%覆盖率）。跨网络转移中，KY4精度96.3%、City H 91.5%、City D 81.8%，无泄漏对照误报率0-2/50。L-Town上仅对33个泄漏中的4个采取行动且全部正确（100%精度）。现场寄存器中5次开挖3次正确（60%），85次调查全部命中区域（100%）。McNemar检验显示执行器显著优于检索基线（χ²=171，p<0.001），多谓词契约全面优于标量阈值。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下方向展开：其一，当前所有实验均基于仿真数据或孪生模拟，缺乏真实SCADA遥测验证，未来应在实际管网部署，检验证书链在真实控制室中的可操作性。其二，主动感知在当前传感器密度下收益有限，可探索动态传感器调度策略，在关键决策节点自适应提升信息增益。其三，LLM审计器仅部分泛化于枚举规则之外，可引入可验证的推理链或形式化验证工具，增强其对未预见表征的判别能力。其四，当前假设类别（泄漏、需求、传感器、阀门）源自文献先验，实际场景中可能存在未知混杂因素，需建立开放集识别机制。其五，可考虑将选择性预测与在线学习结合，利用拒绝样本的后续确认信息持续优化决策边界，而非依赖固定阈值。最后，跨域迁移值得验证——将框架应用于电力故障或气体管道诊断，检验其领域无关性假设的边界条件。

### Q6: 总结一下论文的主要内容

本文提出“可验证弃权”机制，将供水管网漏损定位重构为可问责的决策问题，核心贡献在于解决AI定位器因缺乏“何时不行动”的证明能力而难以被信任的痛点。方法上采用“执行器-监督器”双智能体架构：物理驱动的执行器基于数字孪生对漏损、需水、传感器、阀门等假设进行证伪；独立监督器结合大语言模型审计员，依据代码可验证的契约检查证据，决定派工、索证或弃权。实验表明，在实地噪声下，强制基线32%的决策精度提升至96%；在独立基准上仅对4/33处漏损行动且全部正确；真实事件登记中，5次派工3次正确，并以44%的勘测恢复率实现全区域精度。该方法将可审计的弃权机制引入选择性预测，为自主水务基础设施运行提供了可辩护的路径，且架构可推广至电力、燃气等网络化物理故障诊断场景。
