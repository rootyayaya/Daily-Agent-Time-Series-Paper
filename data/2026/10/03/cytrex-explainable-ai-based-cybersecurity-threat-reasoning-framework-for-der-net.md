---
title: "CyTReX: Explainable AI-Based Cybersecurity Threat Reasoning Framework for DER Networks"
authors:
  - "Damilola Popoola"
  - "Souradeep Bhattacharya"
  - "Manimaran Govindarasu"
date: "2026-10-03"
arxiv_id: "2610.04286"
arxiv_url: "https://arxiv.org/abs/2610.04286"
pdf_url: "https://arxiv.org/pdf/2610.04286v1"
categories:
  - "cs.CR"
  - "cs.AI"
  - "cs.LG"
tags:
  - "LLM Agent"
  - "可解释AI"
  - "证据路由"
  - "SHAP归因"
  - "MCP工具调用"
  - "威胁推理"
  - "异常检测"
  - "网络安全"
  - "DER网络"
  - "可追溯诊断链"
  - "SOC分诊"
  - "结构化证据包"
relevance_score: 7.5
---

# CyTReX: Explainable AI-Based Cybersecurity Threat Reasoning Framework for DER Networks

## 原始摘要

Distributed Energy Resource (DER) environments rely on network communication protocols to coordinate control commands, measurements, and device states across edge assets and cloud systems. Edge anomaly detection systems (ADS) monitor this traffic to identify deviations from normal communication behavior, flagging suspicious flows for further investigation. When the ADS flags abnormal network traffic, a single attack label is often insufficient for operational response: the label reports the detector's selected class but does not expose alternative threat interpretations that may warrant investigation. This paper presents Cybersecurity Threat Reasoning with Explainable Artificial Intelligence (CyTReX), an evidence-grounded threat reasoning framework for DER security that transforms network-level anomaly alerts into ranked, analyst-facing threat hypotheses designed to support Security Operations Center (SOC) triage and investigation. CyTReX constrains large language model (LLM) reasoning through a structured evidence packet, defined as a consolidated record of detection outputs, model explanations, and cyber threat intelligence (CTI) context. The evidence packet integrates edge-layer anomaly detection evidence, cloud reasoning layer attack interpretation, Shapley Additive Explanations (SHAP) network-feature attributions, surrogate decision rules, and Model Context Protocol (MCP)-enabled CTI enrichment. This ensures that every ranked hypothesis and attack-tree branch is traceable to explicit evidence rather than free-form LLM inference, and that incomplete or conflicting evidence is communicated rather than suppressed. Evaluation across five configurations shows that additional reasoning components improve hypothesis specificity, evidence traceability, and analytical grounding, with the complete pipeline providing the richest evidence-grounded reasoning context.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在DER环境中，DNP3等通信协议承载着控制命令、设备状态与量测数据的协调传输，重放攻击、未授权控制命令或DoS等异常流量均可能表现为网络级异常。现有基于AI/ML的边缘异常检测系统虽能提升检测覆盖率，但仅输出单一攻击类别标签，既不揭示哪些网络特征驱动了告警，也不说明还有哪些替代威胁解释仍然合理，更无法指出需要哪些额外证据加以区分。这导致SOC分析人员缺乏可靠的分类、升级与响应依据，且边缘层与云层各自都无法提供完整证据上下文。本文提出CyTReX框架，其核心问题是：如何将ML生成的网络异常告警转化为面向分析人员的、有证据支撑的排序威胁假设。具体而言，CyTReX通过结构化证据包约束LLM推理，该证据包整合边缘异常检测证据、云推理层攻击解释、SHAP网络特征归因、代理决策规则以及MCP驱动的CTI增强，确保每个排序假设和攻击树分支都可追溯至显式证据，而非LLM的自由推断，并且不完整或冲突的证据应被明确传达而非被抑制。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，基于机器学习的异常检测已被广泛用于网络化信息物理系统、工业控制系统和电网通信环境，DNP3赋能的DER网络中也有监督分类器用于区分多种攻击类别，但这类工作主要识别异常行为，缺乏攻击语义，且闭集分类精度无法保证对训练外未知攻击的可靠性。可解释AI方法如SHAP和LIME被用于解释异常检测决策、识别关键特征，但仅停留在特征层面，无法判断证据是否与合理的网络威胁假设一致。应用类方面，近期DER安全研究提出自验证异常检测，利用解释一致性评估异常证据可靠性；CTI仓库如STIX/TAXII、MITRE ATT&CK for ICS和CAPEC提供行为级TTP与攻击模式知识，可丰富告警解读，但需与观测证据绑定以避免无依据关联。评测类方面，LLM与生成式AI已被探索用于安全决策支持、事件摘要、威胁分析和CTI合成，但其输出易受提示设计影响，可能过度泛化或引入无依据的CTI关联。综上，现有方法或聚焦孤立检测，或仅提供无操作上下文的特征级解释，或应用LLM却缺乏严格证据约束。本文CyTReX的区别在于通过结构化证据包约束LLM推理，将边缘检测证据、SHAP归因、代理决策规则与MCP赋能的CTI上下文整合，生成可追溯、排序化的威胁假设，填补了低层证据与证据落地威胁推理之间的空白。

### Q3: 论文如何解决这个问题？

CyTReX 的核心思路是将边缘层异常告警转化为可供 SOC 分析师研判的、按可信度排序的威胁假设与攻击树，而不是给出单一攻击标签。整体采用边缘—云协同架构：边缘层贴近 DER 资产监测通信与遥测行为，输出异常证据，包括异常描述、偏离强度、通信上下文及贡献特征，但不做最终攻击归因；云推理层负责威胁解释、模型解释、CTI 富化和 LLM 推理。

关键组件有四部分。一是云分类器给出攻击类别解释，并保留多假设排序而非单一判定。二是模型解释层，结合 SHAP 特征归因与代理决策规则，显式暴露驱动分类的行为特征，并对 SHAP 与规则证据做一致性检查，生成证据质量信号，使证据薄弱时保留不确定性。三是 CTI 层，通过 MCP 接口以行为为导向检索 MITRE ATT&CK for ICS 的战术、技术与缓解措施，以及 CAPEC 攻击模式，提供带来源的威胁情报。四是 LLM 推理层，其输入是统一证据包，整合边缘证据、云层攻击解释、SHAP 归因、代理规则、CTI、证据质量与来源元数据。

创新点在于：用结构化证据包约束 LLM 推理，使每条排序假设和攻击树分支都可追溯到显式证据，避免自由生成；允许并显式表达不完整或冲突证据；输出攻击树包含根事件、排序假设、支撑证据、不确定性说明和证据缺口，服务于分析师决策而非自动响应。

### Q4: 论文做了哪些实验？

论文围绕CyTReX框架开展了检测性能与威胁推理行为两方面实验。实验在Apple M4（16GB RAM、macOS 15.5）上以Python 3.13实现，使用Streamlit界面和本地Ollama运行的llama3.1:8b模型，三个虚拟DER设备实时模拟DNP3流量。数据集为DNP3通信数据，按70:30划分训练/测试，包含NORMAL及REPLAY、COLD_RESTART、WARM_RESTART、STOP_APP、DISABLE_UNSOLICITED、INIT_DATA六类攻击标签，DNP3_ENUM和DNP3_INFO作为OOD测试。边缘层对比Isolation Forest+最近邻、Isolation Forest、Extended Isolation Forest，最终选用Isolation Forest+最近邻，准确率98.43%、F1为99.21%；云层对比LightGBM、XGBoost、Random Forest，选用LightGBM，准确率与F1均为99.58%。威胁推理设置C1至C5五种配置，评估H1假设、延迟、证据溯源与不确定性处理。结果显示C3标签锚定最强，C5语义解释更丰富但会向广义威胁偏移；REPLAY在五种配置中均为H1，平均延迟以C3最低、C2最高。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于：评估仍以离线配置对比和少量案例为主，缺乏真实SOC环境下的分析师可用性实验与端到端时延、吞吐测试；LLM推理虽由证据包约束，但仍可能产生幻觉或对冲突证据处理不当；SHAP与代理规则在高维、概念漂移的DER流量下解释稳定性不足；CTI经MCP获取的时效性与覆盖度也未被量化。未来可探索：一是引入不确定性量化与校准，让假设附带置信区间并显式标注证据缺口；二是构建人机协同闭环，用分析师反馈持续微调推理链与排序策略；三是扩展到多模态证据，如物理量测、拓扑与告警日志的联合推理；四是研究对抗场景下证据包被投毒时的鲁棒性；五是建立标准化基准与在线A/B评测，比较不同LLM、检索策略与攻击树生成方法的成本效益。此外，可将推理结果反哺检测器，形成检测—解释—响应的自适应迭代。

### Q6: 总结一下论文的主要内容

本文针对分布式能源（DER）网络中单一异常检测标签无法揭示多种威胁解释的问题，提出了CyTReX框架。该框架将边缘层异常检测证据、云端攻击分类、SHAP特征归因、代理决策规则及MCP协议支持的威胁情报整合为统一证据包，约束大语言模型生成可排序、可追溯的威胁假设与攻击树，供安全运营中心分诊使用。在DNP3协议上的五配置评估表明，增加推理组件可提升假设特异性与证据可追溯性，完整流程提供最丰富的证据支撑推理；对未见攻击类型的测试也显示其能生成安全相关假设，但需开放集检测以避免将未知行为强行归入已知类别。
