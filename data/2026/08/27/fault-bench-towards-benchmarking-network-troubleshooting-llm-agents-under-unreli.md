---
title: "FaulT-Bench: Towards Benchmarking Network Troubleshooting LLM Agents under Unreliable User Tickets"
authors:
  - "Kuan-Hao Tseng"
  - "Niruth Bogahawatta"
  - "Yasod Ginige"
  - "Kunjan Patel"
  - "Kosta Dakic"
  - "Suranga Seneviratne"
date: "2026-08-27"
arxiv_id: "2608.27021"
arxiv_url: "https://arxiv.org/abs/2608.27021"
pdf_url: "https://arxiv.org/pdf/2608.27021v1"
categories:
  - "cs.NI"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "网络故障诊断"
  - "LLM Agent"
  - "基准测试"
  - "不可靠用户工单"
  - "诊断推理"
  - "工具调用"
  - "LLM评估"
relevance_score: 8.5
---

# FaulT-Bench: Towards Benchmarking Network Troubleshooting LLM Agents under Unreliable User Tickets

## 原始摘要

LLM-based agents are increasingly proposed for network fault diagnosis, but existing benchmarks evaluate them only on accurate tickets and always assume a fault is present, conditions rarely met in practice. We present FaulT-Bench, a benchmark of 200 troubleshooting scenarios across eight network topologies, five reimplemented from public practitioner labs, spanning genuine faults, false fault reports, incorrect device attribution, and incorrect root-cause claims. To isolate how ticket wording affects diagnosis, we further rewrite 72 false-premise tickets into five reporter personas that vary reporter confidence and verifiable detail one factor at a time, holding the network state fixed. Our automated harness deploys each scenario in Kathará, lets agents interact through the NIKA tool interface, and scores free-text diagnoses with an LLM judge across outcome, fix, and reasoning quality. Evaluating SADE, ReAct, and Claude Code, we find all three are near-saturated on accurate tickets and robust to misdirection, yet degrade sharply when the network is healthy and the ticket is wrong, probing until a benign condition can be promoted to a root cause rather than concluding nothing is wrong. Persona rewrites show that how a ticket is written matters more than what it claims: a confidently wrong report is handled about as well as an accurate one, while a vague, underspecified report degrades performance sharply. The three agents also fail differently, from constant over-diagnosis to unanswered runs, at very different cost. These results position FaulT-Bench as a benchmark for developing agentic systems that can reason reliably over the noisy, unreliable tickets of real-world network troubleshooting.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着网络规模扩大，故障诊断日益复杂，LLM智能体被广泛用于自动化网络排障。然而，现有基准如NIKA存在关键缺陷：它们假设故障必然存在，且用户工单准确描述故障，这与现实严重不符。实际运维中，工单常由人类撰写，可能模糊、不完整，甚至包含错误前提（如健康网络被误报故障、设备归因错误或根因判断错误）。若智能体无法甄别这些不可靠信息，将导致误诊，误导工程师修复健康设备而遗漏真实问题，造成运维灾难。

为此，本文提出FaulT-Bench基准，旨在系统评估LLM智能体在不可靠用户工单下的排障能力。该基准包含200个场景，覆盖真实故障、错误前提、错误设备归因和错误根因四类，并设计了五种报告人风格以隔离工单措辞的影响。核心问题是：现有智能体能否在工单信息不准确或网络实际健康时，仍做出正确诊断而非过度诊断？通过自动化评估，本文揭示了智能体在错误前提场景下性能急剧下降，常将良性状态误判为根因，凸显了构建能可靠处理现实噪声工单的智能体的必要性。

### Q2: 有哪些相关研究？

相关研究主要分为以下几类：

**方法类**：早期工作包括零接触服务管理、意图网络和静态分析工具，随后发展为基于图神经网络的机器学习方法。近期研究聚焦于LLM智能体，如ReAct式工具循环和程序化策略的结构化诊断，以及将LLM智能体应用于云和微服务系统的根因分析。

**应用类**：工业部署包括字节跳动的对话式诊断、Meta的多智能体事件处理和阿里的故障定位系统。这些系统均在“故障真实存在且报告准确”的假设下开发评估。

**评测类**：通用AI智能体基准不含网络环境，网络专项基准多针对配置合成、管理任务或云事件生命周期。最接近的NIKA提供数百个Kathará仿真网络上的事件，但同样假设故障必然存在，任务以结构化规格呈现，评分仅匹配标签掩码。

**本文区别**：FaulT-Bench首次系统性地评测了“健康网络误报故障”和“被错误报告误导”两种失效模式，包含170个自由文本工单，采用多数反例设计，并通过LLM裁判对开放式诊断进行评分，填补了现有基准无法奖励“无故障”结论、无法测试模糊或自信错误报告鲁棒性的空白。

### Q3: 论文如何解决这个问题？

FaulT-Bench通过构建一个包含200个故障排查场景的基准测试框架，系统性地解决了现有网络故障诊断基准仅评估准确工单且假设故障必然存在的问题。其核心方法分为三个层面：

在数据集设计上，基准覆盖八种网络拓扑（其中五种从公开实践实验室复现），每拓扑25个场景，包含80个真实故障场景（注入实际故障且工单准确描述）、72个虚假前提场景（网络健康但工单报告不存在故障）、24个错误设备场景（故障真实但工单指向健康设备）和24个错误原因场景（故障真实但工单断言错误机制）。特别地，对72个虚假前提工单采用五种报告人设进行受控改写，包括新手（非技术、不确定、省略原因）、新手自信（保留信息但语气强硬）、天真（非技术、紧急、断言原因）、天真不确定（去除确定性）和天真无细节（移除所有可验证标识符），每次仅改变一个因素以隔离工单措辞的影响。

在评估框架上，系统采用Kathará容器化网络模拟器部署每个场景，通过NIKA工具接口让代理与网络交互，并使用LLM评判器对自由文本诊断结果从结果正确性、修复质量和推理质量三个维度打分。场景文件包含对代理可见的工单和隐藏的故障注入命令、验证探针、地面真值、修复规范及评分标准。

在创新点上，该基准首次系统性地评估代理在不可靠工单下的表现，通过控制变量法分离工单内容与表述风格的影响，并揭示了现有代理在健康网络场景下倾向于将良性条件升级为根因而非得出“无故障”结论的关键缺陷。

### Q4: 论文做了哪些实验？

在实验设置上，论文构建了包含200个故障排查场景的FaulT-Bench基准，覆盖8种网络拓扑（其中5种来自公开实践实验室），并设计了核心基准（E1）与人物角色改写（E2）两组实验。E1中，三个智能体（SADE、Claude Code-Baseline、ReAct）在全部200个场景上各运行3次，共1800次；E2中，针对72个错误前提票据的5种人物角色改写各运行2次。所有实验在Kathará模拟环境中通过NIKA工具接口执行，每个智能体拥有22个工具和20轮交互预算，由LLM裁判对结果、修复和推理质量进行评分。

主要结果包括：在80个正确故障场景中，三个智能体表现接近饱和（SADE 0.912、CC-Baseline 0.942、ReAct 0.941）；在72个错误前提场景中，性能显著下降（平均0.820，Δ=-0.112），且17%的应答运行出现过度诊断；在错误设备（0.957）和错误原因（0.911）场景中表现相对稳健。人物角色实验表明，自信但错误的报告处理效果接近准确报告，而模糊不明确的报告导致性能急剧下降。此外，三个智能体失败模式各异，从持续过度诊断到无应答超时（超时率0-5%），且运行成本差异显著。

### Q5: 有什么可以进一步探索的点？

基于论文的实验结果，未来可从以下几个方向深入探索：

**一、核心局限与改进**
1. **健康网络场景的过度诊断问题**：当前所有智能体在健康网络下均倾向于将良性状态误判为故障根因，这暴露了诊断逻辑中缺乏“无故障”假设的验证机制。未来可引入显式的健康状态先验或“排除法”推理策略，并设计专门的否定性诊断奖励函数。
2. **模糊票单的鲁棒性**：实验表明票单措辞的模糊性比错误内容更具破坏性，建议开发主动澄清机制，让智能体在信息不足时主动追问而非盲目猜测，同时可训练票单信息量评估模块来动态调整推理深度。

**二、架构与评估扩展**
3. **多智能体协作与反思机制**：当前单智能体在错误票单下表现脆弱，可探索“诊断-验证”双智能体架构，或引入自我批判循环来抑制过度自信。
4. **动态票单生成**：现有persona重写仅固定网络状态，未来可联合扰动网络拓扑、故障类型与票单质量，构建更真实的组合空间，并加入时间序列日志数据以测试智能体的时序推理能力。

**三、实用化方向**
5. **成本-性能联合优化**：论文已揭示不同智能体在超时率和诊断成本上差异显著，可设计自适应推理预算分配策略，根据票单置信度动态调整探索深度。
6. **跨域泛化测试**：当前拓扑规模有限，可扩展至云原生或5G核心网场景，验证方法在更大规模、更异构基础设施上的可迁移性。

### Q6: 总结一下论文的主要内容

FaulT-Bench是一个用于评估LLM智能体在网络故障诊断中处理不可靠用户工单能力的基准测试。现有基准仅基于准确工单且假设故障必然存在，与真实运维场景不符。该基准包含200个场景，覆盖8种网络拓扑，分为四类：正确故障、错误前提（网络健康但工单误报）、错误设备归属和错误根因断言。此外，通过五种报告者人设重写72个错误前提工单，控制报告者信心和可验证细节，以隔离工单措辞对诊断的影响。自动化评估框架在Kathará模拟器中部署场景，通过NIKA工具接口交互，并用LLM裁判从结果准确性、修复建议和推理质量三维度评分。评估SADE、ReAct和Claude Code发现：三者对准确工单表现饱和且能抵抗误导，但在健康网络和错误工单下性能显著下降，倾向于将良性条件误判为根因。工单写法比内容更重要：自信的错误报告处理效果接近准确报告，而模糊报告导致性能大幅下降。FaulT-Bench为开发能在真实嘈杂工单环境中可靠推理的智能体系统提供了基准。
