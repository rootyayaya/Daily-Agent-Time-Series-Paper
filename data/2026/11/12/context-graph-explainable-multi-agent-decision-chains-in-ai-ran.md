---
title: "Context Graph: Explainable Multi-Agent Decision Chains in AI-RAN"
authors:
  - "Xijun Wang"
  - "Zhaoyang Liu"
  - "Xiang Chen"
  - "Howard H. Yang"
  - "Chenyuan Feng"
date: "2026-11-12"
arxiv_id: "2611.16879"
arxiv_url: "https://arxiv.org/abs/2611.16879"
pdf_url: "https://arxiv.org/pdf/2611.16879v1"
categories:
  - "cs.NI"
  - "cs.AI"
  - "cs.IT"
tags:
  - "多智能体决策链"
  - "可解释性"
  - "因果追溯"
  - "反事实验证"
  - "AI-RAN"
  - "故障诊断"
  - "上下文图"
  - "Agentic诊断"
relevance_score: 7.5
---

# Context Graph: Explainable Multi-Agent Decision Chains in AI-RAN

## 原始摘要

AI-RAN distributes network control across multiple autonomous agents, namely xApps and rApps operating over shared radio resources. When an alert or degradation appears, operators currently lack a structured way to trace which decision caused it, what context triggered that decision, and how other agents interacted. Existing explainability tools focus on single-model feature attribution or linear event logging, neither of which captures cross-agent decision chains. We propose the Context Graph, a heterogeneous directed graph that organizes policies, measurements, decisions, and alerts into a queryable explanation layer. Its foundational primitive is the Decision-Event node acting as a causal junction, where incoming edges capture triggering context and outgoing edges track downstream consequences that are progressively upgraded through counterfactual verification. Instantiated over existing E2, A1, and O1 data flows, our proof-of-concept demonstrates that compliance and diagnosis queries are resolved at sub-millisecond latency over graphs of tens of thousands of nodes, while reliably distinguishing true causal impacts from spurious correlations.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决AI-RAN多智能体架构下系统级可解释性缺失的问题。研究背景方面，O-RAN将网络智能分散到多个并行的xApps和rApps中，它们共享无线资源、观测重叠的网络状态并各自做出决策，网络行为因此成为多个学习型智能体集体决策的结果，而非单一模型所能解释。现有方法的不足体现在三个层面：可解释AI研究多聚焦于单模型的特征归因，只能解释某一次预测；AI-RAN框架虽引入证据记录与推理轨迹，但这些轨迹是线性的“发生了什么”记录，缺乏表达“为何在该上下文中采取该行动”以及后果如何分支的结构；冲突管理方法虽建模xApp间交互，但目标是检测或缓解近实时环路中的竞争行为，轻量运行时监控也只能标记异常发生，无法定位导致异常的决策链。同时，E2测量、A1策略、O1告警和决策记录等原始证据分散在不同接口与时间尺度上，彼此孤立，无法拼成从上下文到决策再到后果的完整路径。因此，本文的核心问题是：如何构建一个基于现有O-RAN数据流的系统级解释层，将策略、测量、决策与告警组织成可查询的跨智能体决策链，使运维人员能从告警回溯到候选决策及其触发上下文，并区分真实因果影响与虚假相关。

### Q2: 有哪些相关研究？

现有工作可分为三类。方法类方面，单模型可解释性方法（如特征归因、SHAP、注意力可视化）聚焦于解释单个模型的输出依据，但无法刻画跨智能体的决策链；事件日志与追踪系统（如线性日志、分布式追踪）能记录操作序列，却缺乏因果结构与上下文对象化表达；因果推断方法（如反事实分析、因果图）提供了因果验证手段，但多用于离线分析，未与在线RAN控制流结合。应用类方面，O-RAN智能控制器（xApp/rApp）相关研究多关注策略优化与资源分配性能，对多智能体耦合行为的可解释性讨论较少；故障诊断与合规审计工具通常基于KPI阈值或告警关联，难以回溯到具体决策及其触发上下文。评测类方面，现有可解释性评测多针对单模型忠实度、稳定性等指标，缺少面向跨智能体、跨时间决策链的结构化查询与因果区分评测基准。本文与上述工作的区别在于：将策略、测量、决策与告警组织为异构有向图，以Decision-Event节点作为因果枢纽，并通过反事实验证将时间相关升级为因果影响；同时直接实例化于E2、A1、O1现有数据流，实现亚毫秒级合规与诊断查询，弥补了单模型解释与线性日志在跨智能体决策链追溯上的空白。

### Q3: 论文如何解决这个问题？

论文提出的核心方法是构建一个名为“上下文图”（Context Graph）的异构图，作为AI-RAN中多智能体决策链的可解释层。整体框架分为三层：数据生产层由现有O-RAN组件通过E2SM-KPM、A1策略和O1 VES事件产生证据；近实时时间戳层部署轻量级Context-Logger xApp，订阅E2指示消息并为决策记录打上亚秒级时间戳、标注网络实体后转发至非实时域；非实时图组装层由Context Graph Engine聚合多源数据，构建节点与边，执行反事实推理并响应查询。图模式定义了七类节点，以Decision-Event节点为核心因果枢纽，入边捕获触发上下文（策略、KPM快照、告警），出边追踪下游后果；边分为时间、实体、语义和因果四类。关键技术包括：渐进式因果标注，先建立candidate_effect候选边，再通过基于无线环境模型的反事实验证将显著差异的边升级为causes；物理可达性约束防止虚假候选边；意图感知查询路由，按合规、诊断、策略优化等意图仅遍历相关边类型，使查询延迟随解释路径长度而非图规模增长。创新点在于将每个决策建模为因果枢纽、区分相关与因果的渐进标注机制、近实时捕获与非实时推理的解耦设计，以及基于标准接口的非侵入式集成，从而在保持控制环路响应的同时实现跨智能体决策链的可审计追溯。

### Q4: 论文做了哪些实验？

论文围绕Context Graph在AI-RAN场景中的有效性开展了三类实验。实验设置上，构建了12小区密集城区的合成但符合标准的场景，包含URLLC与eMBB切片，由功率xApp与PRB xApp控制，模拟器生成A1策略、1Hz KPM报告、条件触发决策和O1 SLA告警，流量动态变化且测量含噪声。第一类为端到端案例走查：在t=294.0s小区10高负载触发功率xApp提升发射功率，使邻区2的SINR下降1.2dB，PRB xApp在URLLC优先策略下于t=295.9s重分配资源块，导致小区2 eMBB吞吐下降7.1Mbps，并于t=296.1s触发O1告警；诊断查询经4跳回溯到功率与PRB两个决策，合规查询则追溯至policy-4与KPM快照。第二类为可扩展性与延迟实验，覆盖6/12/24小区×5min及12/24小区×30min五种配置，图规模从1,944节点/4,162边增至45,267节点/96,002边；装配时间0.029–0.76s，候选边生成0.0062–0.11s，因果标注0.018–2.0s；合规与诊断查询延迟均稳定在约0.005ms。第三类为因果验证实验，基于30个种子的反事实重放建立真值，仅依赖时间邻近或KPM波动阈值的精度低于10%，而反事实验证在2dB链路增益误差下达到87.3%精度和86.6%召回，遥测延迟60s时精度仍超83%，8dB严重信道误差下降至约50%。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：一是因果边可靠性受模型保真度与时钟同步制约，仿真偏差和跨域时钟偏移可能颠倒动作与后果的时序；二是xApp决策日志私有化，Context-Logger只能从KPM变化事后推断，带来事件时序与控制幅度的不确定性；三是高频KPM遥测导致图无界增长，简单时间剪枝可能切断审计所需的因果链。未来可探索：定义E2SM决策上报服务模型，从源头补齐溯源信息并研究最小因果验证schema；设计自适应生命周期策略，按因果相关性区分节点（摘要孤立遥测、归档完整决策链），在限定内存的同时保持长程可遍历性；将图积累的因果知识反哺多智能体学习，但需解决策略更新引起的分布漂移与多智能体同步适应导致的振荡，关键是提取策略不变的因果知识；结合LLM实现意图感知查询，以类型化图schema作为约束动作空间，防止生成接口幻觉出不存在的因果依赖。此外，可引入不确定性标注与置信度传播，将推断决策标记为临时证据，提升多厂商部署下的可信度。

### Q6: 总结一下论文的主要内容

论文针对AI-RAN中多智能体（xApps与rApps）共享无线资源、告警或性能劣化出现时运营商难以追溯“哪个决策导致问题、何种上下文触发该决策、其他智能体如何交互”的系统级可解释性缺口，指出现有工具仅支持单模型特征归因或线性事件日志，无法刻画跨智能体决策链。为此，作者提出Context Graph——一种将策略、测量、决策与告警组织为可查询解释层的异构有向图，其基本原语为充当因果交汇点的Decision-Event节点：入边记录触发上下文，出边追踪下游后果，并通过反事实验证逐步升级因果关系。该方法基于现有E2、A1、O1数据流实例化，无需修改控制面协议，并将图推理隔离在Non-RT层。概念验证表明，在数万节点图上合规与诊断查询可在亚毫秒级完成，并能可靠区分真实因果影响与虚假相关。其意义在于为自主、自演化无线接入网奠定信任与溯源基础。
