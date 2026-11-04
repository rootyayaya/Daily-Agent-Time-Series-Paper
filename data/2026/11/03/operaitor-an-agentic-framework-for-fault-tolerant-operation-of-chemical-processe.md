---
title: "OperAItor: An Agentic Framework for Fault-Tolerant Operation of Chemical Processes"
authors:
  - "Javal Vyas"
  - "Mehmet Mercang{ö}z"
date: "2026-11-03"
arxiv_id: "2611.05179"
arxiv_url: "https://arxiv.org/abs/2611.05179"
pdf_url: "https://arxiv.org/pdf/2611.05179v1"
categories:
  - "eess.SY"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "故障诊断"
  - "工业过程监控"
  - "LLM Agent"
  - "知识图谱检索"
  - "动作验证"
  - "多变量统计过程监控"
  - "可解释诊断"
  - "化学过程"
  - "基准测试"
relevance_score: 8.5
---

# OperAItor: An Agentic Framework for Fault-Tolerant Operation of Chemical Processes

## 原始摘要

OperAItor, an open-source framework for developing and evaluating large language model agents for supervisory fault management in chemical processes. The framework is demonstrated on a dynamic reactor-distillation process representing isopropanol dehydrogenation, with physically based thermodynamics and modified reaction kinetics to permit liquid-phase operation. The process is represented by a 113-variable differential-algebraic model and operates at a nominal feed rate of 100kmol/h, producing approximately 4t/h of acetone. The simulated plant includes 8 PI control loops, 22 process alarms, 5 duty-standby pump trains, and 11 independent safety instrumented functions. The agent architecture integrates multivariate statistical process monitoring, fault diagnosis, knowledge-graph retrieval, action planning, and supervisory action generation. Five action-validation configurations are investigated, comprising operation without validation, an LLM-based judge, digital-twin simulation, and deterministic admissibility checks with and without consequence projection. The framework is evaluated using four LLMs across 20 scenarios involving single and multiple simultaneous faults. Without agent intervention, 18 scenarios result in plant stops, corresponding to an economic loss of $399,000 relative to fault-free operation under the assumed benchmark economics. For GPT-5 nano, Qwen3 8B, and Mistral 7B, validated agent configurations reduce the number of stops to 5-8 and recover $265,000 of the loss. The study provides a reproducible benchmark for comparing agent architectures, language models, and action-validation methods for supervisory fault management in chemical processes.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于化工过程 supervisory 故障管理中的一个关键缺口：当过程出现异常工况时，BPCS 只能调节正常操作、SIS 只针对特定危险条件提供保护，二者都无法决定故障后最合适的纠正性干预，这一职责通常落在操作员身上，需要其解读报警、判断故障原因、评估可用干预并在保护性停车前采取行动。现有 FDD 与 FTC 方法虽能检测偏差、隔离故障或重构控制，但获得故障诊断并不等于能确定合适的操作员级干预——恢复可能涉及离散设备操作、上层设定值调整或多单元协调，其可行性取决于过程状态、执行器可用性、操作规程与干预权限。LLM 智能体为这类监督决策提供了可能，已有研究证明其在知识检索、规划与仿真验证结合下可生成有意义的监督干预，但仍无法排除错误归因、不当控制动作或“单独可执行但当前状态下不可取”的干预。因此本文的核心问题是：给定一个 LLM 生成的操作员动作，应如何评估其是否适合执行？作者指出动作生成与动作验证是两个不同问题，验证层必须在排除不良动作与保留故障恢复机会之间取得平衡，且其有效性不能仅靠文本有效性或接受率衡量，而应通过闭环过程行为评估。为此论文提出 OperAItor 开源框架与基准，在含 113 变量 DAE 模型、8 个 PI 回路、22 个报警、5 组 duty-standby 泵和 11 个安全仪表功能的反应器-精馏案例上，对比无验证、LLM 评判、数字孪生仿真、确定性 ADMIT 准入检查（含/不含后果投影）五种验证配置，跨四个 LLM、20 个单故障与多故障场景，以停车频率、经济性能、拒绝行为和计算成本进行系统评估。

### Q2: 有哪些相关研究？

本文的相关研究主要可分为三类。方法类方面，统计过程监控（如PCA）为检测偏离正常工况提供了成熟方法；基于模型的诊断与主动容错控制进一步实现了故障隔离与控制重构，但诊断结果并不自动决定合适的操作员干预。近年来，LLM智能体被用于工业过程控制与故障恢复，已有架构结合知识检索、规划与基于仿真的动作验证；ADMIT框架则通过一系列确定性检查（可选配后果投影）对LLM生成的工业动作进行验证，利用P&ID和操作约束等工程信息。应用类方面，已有研究展示了LLM智能体在工业过程监督控制中的可行性。评测类方面，Tennessee Eastman过程等基准广泛用于故障检测、监控与控制研究，但传统故障检测基准缺乏设备冗余、动作权限、报警处理和独立安全联锁等完整监督环境，且检测精度不能反映干预是否避免停车。本文与上述工作的区别在于：提出开源OperAItor框架，构建包含113变量DAE模型、8个PI回路、22个报警、5组泵和11个安全仪表功能的动态基准，将动作生成、验证与执行分离，系统比较无验证、LLM评判、数字孪生仿真及ADMIT确定性准入等五种验证配置，并以停车频率和经济损失等闭环指标评估，弥补了现有基准与验证方法比较的不足。

### Q3: 论文如何解决这个问题？

OperAItor 的核心思路是把“故障证据”与“可执行响应”连接起来，构建一个位于 BPCS 与 SIS 之上的监督层智能体框架。整体架构以 LangGraph 状态机实现，形成一条从感知到执行的闭环流水线：在决策点，多变量统计过程监控模块提供异常统计量与过程趋势；故障诊断模块据此形成故障假设；知识图谱检索模块识别相关设备、约束条件与候选干预措施；规划模块构造操作简报；随后由 LLM 动作智能体提出结构化操作计划。该计划先经过统一的可行性检查，再通过所选的动作验证机制后才被下发执行；若提案被拒绝，验证结果会经重提示边返回动作智能体，触发重新规划。

关键设计在于动作验证层。论文考察了五种配置：无验证、基于 LLM 的裁判、数字孪生仿真、确定性可接受性检查，以及带后果投影的确定性检查。这一层是框架安全性的核心，确保智能体不会下达违反工艺约束或安全联锁的命令。此外，框架严格限制智能体的权限边界：常规控制器继续调节过程，保护性联锁保持最高优先级，智能体只能通过监督接口施加操作员级干预，从而不替代既有控制与安全层。

创新点体现在三方面：一是将统计监控、故障诊断、知识图谱检索、规划与动作生成集成为可复现的智能体流水线；二是引入多种可插拔的动作验证机制并系统比较其效果；三是在包含 113 变量微分代数模型、8 个 PI 控制回路、22 个报警、5 组备用泵与 11 个独立安全仪表功能的反应-精馏动态过程上建立基准，用 20 个单/多故障场景和四种 LLM 评估框架，证明验证配置可将停车场景从 18 个降至 5–8 个并挽回约 26.5 万美元损失。

### Q4: 论文做了哪些实验？

论文在集成反应器-精馏基准上开展实验，该过程由113变量微分代数模型描述（41个微分变量、72个代数变量），标称进料100 kmol/h、产丙酮约4 t/h，含8个PI控制回路、22个过程报警、5套一用一备泵组和11个独立安全仪表功能。故障库含18种故障机制，评估选用其中10种（进料泵、回流泵、馏出泵、釜液泵跳车，反应器出口能力损失，氢气排放退化，加热器高卡，压力传感器偏置，冷凝器冷却失效，回流罐泄漏），并叠加有限时扰动与测量噪声。实验设置考察5种动作校验配置：无校验、LLM评判、数字孪生仿真、确定性可接受性检查（含与不含后果预测）；使用4种LLM在20个单故障与多故障同时发生的场景中评估。主要结果：无智能体干预时18个场景导致装置停车，相对无故障运行经济损失399,000美元；对GPT-5 nano、Qwen3 8B和Mistral 7B，经校验的智能体配置将停车数降至5–8个，挽回265,000美元损失。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点。其一，数字孪生验证采用匹配模型设定，未考察模型失配下的鲁棒性，未来可引入参数漂移、动力学偏差与噪声，检验验证层在真实工业场景中的可靠性。其二，案例仅覆盖单一反应-精馏流程与20个故障场景，故障类型和工艺拓扑有限，可扩展到多单元耦合、间歇过程及更复杂的多故障并发情形。其三，验证机制以规则与仿真为主，缺乏对LLM推理过程的可解释性评估，可探索将诊断置信度、反事实解释融入验证决策。其四，当前智能体权限限于监督层，未来可研究人机协同与操作员信任校准。此外，可引入在线学习与记忆机制，使智能体从历史拒绝与恢复案例中持续改进策略，并系统比较不同LLM规模与推理成本之间的权衡。

### Q6: 总结一下论文的主要内容

论文针对化工过程异常工况下LLM智能体生成的监督操作动作是否适合执行这一核心问题，提出了开源框架OperAItor。问题定义上，现有故障检测与容错控制无法自动确定合适的操作员级干预，而LLM生成的动作可能归因错误或加速保护停车，因此需要系统评估动作验证机制。方法上，框架构建了包含113变量微分代数模型的反应-精馏基准过程，集成8个PI控制回路、22个报警、5套备用泵和11个安全仪表功能，并将PCA监测、故障诊断、知识图谱检索、规划与LLM动作生成通过模块化验证接口连接，比较无验证、LLM评判、数字孪生仿真、ADMIT确定性准入检查及带后果投影的ADMIT五种配置。主要结论是：无智能体干预时20个场景中18个导致停车，经济损失39.9万美元；采用验证配置后，GPT-5 nano、Qwen3 8B和Mistral 7B将停车降至5-8次并挽回26.5万美元损失。该工作为比较智能体架构、语言模型与动作验证方法提供了可复现基准。
