---
title: "AI-Driven Framework for Adaptive Water Network Management with Proof-of-Concept Implementation: Addressing Non-Revenue Water in Jordan"
authors:
  - "Mohammed Fasha"
  - "Nahel Al-Maayta"
  - "Bilal Sowan"
  - "Mohammad Athamneh"
  - "Husam Barham"
date: "2026-06-14"
arxiv_id: "2606.15709"
arxiv_url: "https://arxiv.org/abs/2606.15709"
pdf_url: "https://arxiv.org/pdf/2606.15709v1"
categories:
  - "cs.AI"
  - "cs.MA"
tags:
  - "LLM Agent"
  - "时间序列异常检测"
  - "RAG"
  - "工具调用"
  - "数字孪生"
  - "工业故障诊断"
  - "可解释报告"
  - "传感器数据"
  - "水网管理"
  - "自适应决策"
relevance_score: 8.5
---

# AI-Driven Framework for Adaptive Water Network Management with Proof-of-Concept Implementation: Addressing Non-Revenue Water in Jordan

## 原始摘要

Jordan faces severe water scarcity with 50\% of water produced is lost to leakage, theft and metering issues also known as non-revenue water (NRW). Traditional reactive approaches have proven insufficient for sustained NRW reduction. This paper proposes an intelligent framework integrating EPANET hydraulic modeling, digital twin technology, SCADA systems, and large language model (LLM)-based AI agents for continuous network monitoring and adaptive decision-making. The system combines real-time data streams with physics-based simulation to detect anomalies, employing retrieval-augmented generation (RAG) for policy interpretation and function calling for network control. A proof-of-concept implementation validates technical feasibility using EPYT with offline LLMs (llama3.1:8b via Ollama) on a 1,164-junction Amman district network. The system demonstrates automated hydraulic simulation, flow-based anomaly detection aligned with water distribution zone (DZ) practice, and AI-generated health reports with response times under 2 minutes and zero API costs. Burst detection relies on local flow anomaly analysis: a 30.1~L/s simulated leak produces measurable flow redistribution in 15 pipes, flagging a 15-junction cluster that localises the burst -- confirming alignment with water distribution zone (DZ) monitoring practice. The framework accommodates Jordan's intermittent supply patterns and limited automation through phased implementation, offering a scalable pathway for water-scarce regions to leverage intelligent automation for NRW reduction and operational efficiency.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

约旦面临严重的水资源短缺问题，全国约50%的产水因泄漏、盗窃和计量误差而成为无收益水（NRW）。传统的水务管理方法主要依赖定期巡检和人工分析，属于被动响应模式，难以实现持续、智能的监控与决策。尽管国际组织投入了大量资金进行干预，NRW水平在短期下降后往往因缺乏持续智能管理而反弹。现有方法的核心不足在于：泄漏检测是周期性的而非连续的，运营决策依赖人工分析，且缺乏对间歇性供水模式的适应性。本文旨在解决的核心问题是：如何构建一个集成实时水力建模、数字孪生、SCADA系统和基于大语言模型（LLM）的AI代理的智能框架，实现对配水管网的连续监测与自适应决策，从而在无需云API、零成本且保障数据安全的前提下，自动完成水力模拟、异常检测和生成可操作的健康报告，为水资源匮乏地区提供可扩展的NRW降低与运营效率提升路径。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及以下三类工作：

**方法类**：基于EPANET的液压建模与数字孪生技术。已有研究利用EPANET和SCADA数据实现实时模型校准与泄漏检测（如WNTR、EPYT接口），本文在此基础上进一步整合LLM Agent，实现从“被动监测”到“主动决策”的升级。与纯物理模型方法相比，本文引入了RAG和函数调用机制，使系统能自动解释政策并执行网络控制。

**应用类**：非收益水（NRW）管理与间歇供水系统。Jordan等地区已有大量关于物理损失（爆管、泄漏）和商业损失（盗水、计量误差）的研究，但多采用事后修复策略。本文的创新在于将AI Agent与数字孪生结合，针对间歇供水模式（24-48小时周期）设计自适应框架，并通过30.1 L/s模拟泄漏验证了流量异常检测与区域定位的可行性。

**评测类**：LLM在工业场景中的部署与成本优化。现有工作多依赖云端API，本文则采用离线LLM（llama3.1:8b）实现零API成本、响应时间<2分钟，证明了在资源受限地区部署的可行性。与通用LLM应用不同，本文专门针对水网领域进行了液压仿真与异常检测的集成验证。

### Q3: 论文如何解决这个问题？

该论文提出了一种集成物理仿真与大语言模型智能体的自适应水网管理框架，核心方法是通过数字孪生与AI协同实现实时监测与决策。整体架构包含五个核心模块：数据采集层（SCADA、智能水表、IoT传感器）、大数据平台（实时流处理、时序数据库、异常初筛）、数字孪生/水力模型（EPANET物理仿真引擎）、AI智能体层（基于LLM的决策核心）和网络控制系统（阀门/泵/减压阀执行器）。

关键技术包括：1）**数字孪生与实时数据融合**：EPANET持续运行水力仿真，通过比较模拟值与传感器实测值的偏差（如压力低于1bar或高于5bar、流量偏差超过25%）检测异常，并适应约旦间歇性供水模式，区分计划停水与真实故障。2）**检索增强生成（RAG）**：将运维策略文档转化为向量嵌入（如FAISS数据库），当智能体检测到异常时，通过语义搜索检索最相关的操作策略，实现政策解释与决策推理。3）**函数调用机制**：LLM通过预定义函数（如close_valve()、adjust_pump_speed()、isolate_zone()）与物理基础设施交互，每个函数包含参数验证、安全约束和审计日志。4）**分层部署策略**：分三阶段实施——第一阶段仅监测与告警，第二阶段AI辅助建议需人工批准，第三阶段实现自主控制但保留人工监督，所有推理过程以自然语言记录，低置信度决策需人工确认。

创新点在于：首次将离线LLM（llama3.1:8b）与EPANET物理模型结合，在1164节点真实管网中验证了30.1L/s泄漏检测能力（15根管道流量重分布，定位15节点簇），响应时间低于2分钟且零API成本，为缺水地区提供了可扩展的智能化NRW治理路径。

### Q4: 论文做了哪些实验？

论文开展了一个概念验证（Proof-of-Concept）实验，以验证所提出框架的技术可行性。实验设置采用三层架构：第一层使用EPYT（EPANET-Python工具包）进行水力模拟；第二层用Python脚本提取统计指标（均值、范围、分布）并基于阈值（压力<20米或>60米）进行异常检测；第三层通过Ollama本地部署的llama3.1:8b离线大语言模型（LLM）生成网络健康报告。数据集/基准测试使用一个代表约旦安曼典型供水区（DZ）的1164节点网络，包含1310段管道和2个水源，总基础需水量149.6 L/s，采用间歇性供水模式。实验对比了两种运行场景：场景1（基线网络行为）和场景2（模拟管道爆裂）。主要结果包括：在基线场景下，系统识别出105个节点（9.0%）压力低于20米（标记为供水不足区）和113个节点（9.7%）压力高于60米（标记为需安装减压阀）。在爆裂场景下，通过引入30.1 L/s的模拟泄漏，系统检测到15根管道流量偏差超过1 L/s，并成功定位到一个包含15个节点的爆裂集群，最大局部流量增加10.5%。LLM生成的健康报告响应时间在15-30秒内，且由于完全离线运行，实现了零API成本。实验证明，该框架能有效进行自动化水力模拟、基于流量的异常检测和AI驱动的决策支持。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：(1) 仅基于单一流量异常检测，缺乏多模态数据融合（如压力、声波、水质），易产生误报；(2) 离线LLM（llama3.1:8b）的推理能力有限，复杂策略解释和跨时段模式识别能力不足；(3) 间歇性供水场景下，模型对瞬态压力与真实泄漏的区分依赖阈值设定，缺乏自适应学习机制；(4) 验证仅基于模拟数据，未在真实物理管网中部署。

未来可探索：(1) 引入多模态时间序列编码器（如Transformer+图神经网络）融合压力、流量、声波信号，提升异常定位精度；(2) 采用混合专家LLM架构，将小模型用于实时推理，大模型用于离线策略优化；(3) 设计基于强化学习的自适应阈值调整机制，使系统能根据供水周期动态学习正常波动模式；(4) 构建数字孪生与物理系统的闭环反馈，通过主动注入测试信号验证模型鲁棒性；(5) 开发可解释性模块，利用LLM生成自然语言诊断报告，辅助操作员理解异常根因。

### Q6: 总结一下论文的主要内容

该论文提出了一种面向约旦无收益水（NRW）危机的智能自适应供水网络管理框架。核心贡献在于将EPANET水力建模、数字孪生、SCADA系统与大语言模型（LLM）智能体相结合，实现连续监测与自适应决策。方法上，系统融合实时数据流与物理仿真进行异常检测，采用检索增强生成（RAG）解释政策，并通过函数调用控制网络。在安曼一个1164节点区域的概念验证中，系统实现了端到端响应时间低于2分钟、零API成本，并通过局部流量异常分析成功定位30.1升/秒模拟爆管（标记15根管道和15个节点）。主要结论表明，该离线、低成本的框架能适应约旦间歇性供水模式，通过分阶段部署为缺水地区提供可扩展的NRW减少与运营效率提升路径。
