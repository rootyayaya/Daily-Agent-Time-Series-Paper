---
title: "ADMITBench: A Safety-Governed Reference Framework for Evaluating the Admissibility of Industrial LLM Advisories"
authors:
  - "Yash Misra"
  - "Javal Vyas"
  - "Siddharth Gutta"
  - "Mehmet Mercangöz"
date: "2026-08-04"
arxiv_id: "2608.03866"
arxiv_url: "https://arxiv.org/abs/2608.03866"
pdf_url: "https://arxiv.org/pdf/2608.03866v1"
categories:
  - "cs.AI"
  - "eess.SY"
tags:
  - "工业LLM咨询"
  - "安全治理评估"
  - "证据支持检查"
  - "行动级评估"
  - "参考框架"
  - "版本化评估契约"
  - "非补偿性检查"
  - "时间序列诊断"
  - "可解释故障诊断"
relevance_score: 8.5
---

# ADMITBench: A Safety-Governed Reference Framework for Evaluating the Admissibility of Industrial LLM Advisories

## 原始摘要

This white paper presents ADMITBench, a reference framework for evaluating industrial LLM advisories at the level of the proposed action. The framework implements a versioned, safety-governed evaluation contract that checks whether a recommendation is supported by the available evidence, permitted under the stated authority and procedure, and acceptable under the plant-specific consequence checks encoded in the selected evaluation profile. In this report, \emph{safety-governed} means that eligibility is determined through explicit, non-compensatory checks derived from a versioned plant profile; it does not mean that the evaluator, model, or plant has been safety-certified. Release 0.1.0 is a public reference implementation for technical and research evaluation, not an authorisation for physical execution.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业场景中，大语言模型（LLM）生成的诊断建议可能被操作员采纳，但现有评估体系仅关注“答案是否正确”（如故障分类、传感器解释或知识检索），未验证“建议动作是否可执行”。这导致一个核心缺口：即使诊断正确，后续动作仍可能违反操作规程、超越授权权限、依赖失效证据或引发不可接受的物理后果。现有方法缺乏对“诊断到动作”这一关键环节的结构化评估机制。

本文提出ADMITBench参考框架，将评估单元从自然语言答案转向结构化“动作记录”，并基于版本化的工厂配置文件（cartridge）实施安全治理的评估契约。该契约通过T0–T4非补偿性硬门检查，依次验证记录完整性、证据与状态有效性、危害理解、动作可准入性、物理后果及审计追溯性。核心创新在于：诊断质量与动作可准入性分离报告；将“验证”“保持”“升级”视为证据不足时的合法动作；任何未通过硬门的记录直接标记为不合格并排除在效用排名外。

研究旨在解决工业LLM评估中“诊断正确但动作不可接受”的盲区，为技术研究提供可复现、可审计的评估基准，而非部署授权或安全认证。

### Q2: 有哪些相关研究？

ADMITBench 的相关研究可归为四类。**通用智能体评测**方面，AgentBench 和 TheAgentCompany 通过多轮交互评估长程规划与任务完成能力，但只关注任务是否完成，而非动作在领域安全案例下是否可接受；ADMITBench 则聚焦于动作级可准入性。**工业与故障预测基准**中，PHM-Bench 评估大模型在预测与健康管理任务上的多维能力，AssetOpsBench 考察资产运维工作流，PHMForge 通过 MCP 工具和确定性检查评估工具接地预测；这些基准覆盖面更广，而 ADMITBench 缩小目标至具体动作记录，并强调每个门控判决可针对版本化安全案例重放。**运行时防护栏**方面，AgentSpec、GuardAgent 和 ShieldAgent 为智能体提供在线执行约束，ADMITBench 则是离线评测框架，且采用非补偿性规则——T0至T4任一硬失败即不产生聚合排名，而非允许其他维度弥补。**运行时保障**中，Simplex 和 Black-Box Simplex 架构将高性能组件视为不可信并依赖可信决策模块维持安全；ADMITBench 借鉴其分离原则，但并非实时切换控制器，也不具备形式化安全保证，而是将分离原则应用于基准设计：LLM 提出动作，独立评估器判定资格并输出首个失败门控的可审计解释。

### Q3: 论文如何解决这个问题？

ADMITBench提出了一种安全治理的参考框架，用于评估工业大语言模型建议的可接受性。其核心方法是将评估从自由文本层面提升到结构化行动记录层面，通过版本化的“契约”机制实现确定性检查。

整体框架分为三个层次：上层为场景包、模型交互和行动记录，捕获建议系统的交互过程；下层为版本化契约、评估检查和评估报告，执行规则与模型检查。关键设计是“弹药筒”机制，将通用评估逻辑、可复用模式与工厂特定内容分离，使新增工厂只需提供清单、系统图、安全案例图和程序案例四个文件。

评估层级采用T0至T6七级架构，其中T0至T4为不可补偿的硬性门槛，分别检查记录完整性、证据有效性、危险理解、行动可接受性和物理后果验证；T5仅用于合格行动间的效用排序；T6记录审计追踪。任何硬门槛失败都导致记录不合格，不参与后续排名。

创新点在于：一是权威模型A0/A1/A2区分了咨询、监督和受限自主三种部署配置，权威只能收窄不能扩张；二是非补偿性评估原则，硬门槛失败不可被其他分数抵消；三是确定性执行，T0至T4不依赖语言模型作为主评判，而是基于声明规则和后果模型，确保可复现性；四是聚合分数仅作为合格记录的次要摘要，报告保留完整门槛结果和审计追踪。

### Q4: 论文做了哪些实验？

ADMITBench 0.1.0版本的实验围绕两个内置的工业过程档案（cartridges）展开：cstr_alpha（夹套冷却连续搅拌釜反应器）和column_alpha（精馏塔操作）。实验采用标准化场景输入，包含工厂状态、报警、传感器信任标志、程序上下文和权限级别，将模型输出转换为结构化咨询记录（含建议动作、诊断、置信度、引用证据、验证步骤、升级决策等字段）。评估协议设计了四个核心问题：正确诊断是否伴随可采纳建议、证据降级时行为是否保持、特定档案是否暴露硬门控失败率差异、以及轨迹质量与硬门控资格和效用排序的区分度。当前版本未提供正式的训练/测试/对抗性划分，仅基于各档案内的procedures_cases.jsonl案例集进行评估，结果应视为对发布案例套件的评估而非泛化证据。column_alpha特别包含D03权限不匹配案例，要求升级而非直接行动，以观察委托权限和升级义务的差异。实验未报告具体数值指标，强调解析器兼容性、T4验证时域由档案级规则决定，且明确区分安全治理（非补偿性检查）与安全认证。

### Q5: 有什么可以进一步探索的点？

ADMITBench的局限性与未来探索方向可从以下层面展开：

**1. 跨领域泛化验证**  
当前仅验证了CSTR和蒸馏塔两个同源场景，缺乏对复杂工业系统（如田纳西-伊斯曼过程）的移植测试。未来应构建异构场景的基准测试集，验证评估框架的通用性。可探索将知识图谱与因果推理结合，提升对未知故障模式的适应性。

**2. 对抗性鲁棒性**  
现有分层评估机制未考虑对抗性攻击场景。建议引入对抗样本生成技术，测试模型在恶意篡改传感器数据或误导性证据下的表现。可借鉴对抗训练思想，在评估框架中加入动态对抗校验模块。

**3. 动态安全边界建模**  
当前安全约束基于静态规则，难以应对工况漂移。未来可探索在线学习机制，使安全谓词能根据实时运行数据自适应调整，同时保持非补偿性校验的严格性。

**4. 人机协同决策**  
置信度校准虽被提及，但未深入探讨人机交互策略。可研究自适应置信度阈值调整机制，结合操作员反馈优化选择性风险控制，避免自动化偏差。

**5. 可解释性与安全性的平衡**  
当前将解释性置于辅助地位，但实际工业场景中操作员可能依赖解释判断。未来可探索因果解释生成技术，在保证安全校验优先的前提下，提供可验证的推理路径。

### Q6: 总结一下论文的主要内容

ADMITBench提出了一种面向工业大语言模型（LLM）咨询的安全治理评估框架，核心在于将评估单元从自然语言答案转向“提议动作”。该框架通过版本化的“工厂配置文件”（cartridge）实施非补偿性、分层的安全评估契约，涵盖记录完整性、证据有效性、危害理解、动作可接受性、物理后果验证及审计追踪等层级（T0–T4）。任何未通过硬性门槛的记录即被判定为不合格，不参与效用排序。0.1.0版本提供了统一动作记录格式、评估层级及两个示例配置文件（cstr_alpha和column_alpha），后者包含需升级而非直接操作的权限不匹配案例。该框架强调诊断质量与动作可接受性分离报告，并区分可信来源与模型断言。其主要贡献在于弥合“正确诊断”与“可执行动作”之间的差距，但当前版本仅作为技术研究参考，不构成部署授权或安全认证，工业通用性及可移植性尚待验证。
