---
title: "Multi-Agent System-driven Digital Twins for predictive maintenance: architectures, technologies and open research challenges"
authors:
  - "Korota Arsène Coulibaly"
  - "Mohamed Hamlich"
date: "2026-07-24"
arxiv_id: "2607.21873"
arxiv_url: "https://arxiv.org/abs/2607.21873"
pdf_url: "https://arxiv.org/pdf/2607.21873v1"
categories:
  - "cs.AI"
tags:
  - "Multi-Agent System"
  - "Digital Twins"
  - "predictive maintenance"
  - "Industry 4.0"
  - "Industry 5.0"
  - "explainable AI"
  - "resource-constrained"
  - "hierarchical orchestration"
  - "systematic review"
relevance_score: 7.5
---

# Multi-Agent System-driven Digital Twins for predictive maintenance: architectures, technologies and open research challenges

## 原始摘要

Digital twins have emerged as a foundational technology within the context of Industry 4.0, offering a paradigm for the real-time virtual representation of physical systems. However, managing their growing complexity, particularly in distributed industrial environments, requires intelligent architectures capable of autonomous decision-making, dynamic adaptability, and inter-agent coordination. This systematic review explores the intersection between Multi-Agent Systems and Digital Twins, with a particular focus on predictive maintenance applications in resource-constrained contexts. Through a critical analysis of over 547 papers published in high-impact journals (IEEE Transactions, Nature, Elsevier, MDPI), we establish a taxonomy of existing hybrid architectures, identify persistent technological bottlenecks, and formulate three open research questions concerning: (i) the deployment of artificial intelligence on resource-constrained microcontrollers, (ii) distributed multi-node coordination via lightweight communication protocols, and (iii) the hierarchical orchestration of Digital Twins toward smart factory control integrating residual life estimation and explainable Artificial Intelligence. The results of this analysis reveal that, despite significant progress, no existing system offers an integrated embedded-distributed hierarchical solution that simultaneously meets the requirements of Industry 5.0.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在工业4.0背景下，数字孪生作为实时虚拟映射物理系统的关键技术得到广泛应用，但随着分布式工业环境日益复杂，现有数字孪生架构面临根本性局限：大多数实现依赖集中式或半集中式模型，将推理和决策能力集中于远程服务器或云端，导致延迟过高，无法满足工业预测性维护的实时性要求。此外，现有文献对数字孪生与多智能体系统交叉领域缺乏系统性批判性综述，尤其在资源受限的嵌入式系统上进行预测性维护的研究存在空白。本文旨在解决的核心问题是：如何通过多智能体系统驱动的数字孪生架构，实现分布式工业环境中自主决策、动态适应与智能体间协调，从而克服集中式架构的延迟瓶颈，并满足工业5.0对人机协作、可持续性和韧性的新要求。具体而言，本文提出一种边缘-雾-云三层多智能体数字孪生架构，将感知、诊断和预测功能分布在不同抽象层次的自治协作智能体中，以实现嵌入式、分布式、层次化的预测性维护解决方案。

### Q2: 有哪些相关研究？

相关研究主要分为三类：一是数字孪生架构研究，如Grieves的三维模型和Tao等的五维模型，以及Liu等提出的四轴分类法；本文在此基础上进一步提出五维分类体系（物理抽象、部署架构、嵌入式智能、时间粒度、交互模式），并指出当前缺乏满足工业5.0要求的集成嵌入式-分布式分层方案。二是多智能体系统与数字孪生的融合研究，包括Vrabic等提出的韧性智能体架构、Latsoú等的异常检测方法、Wan等的递归多智能体数字孪生模型，以及Borangiu等的生产控制实现；本文系统梳理了这些混合架构，但指出多数方案在服务器而非嵌入式微控制器上运行，且协调机制未在真实网络条件下验证。三是预测性维护应用研究，涉及边缘-雾-云集成架构在能源、微电网、增材制造等领域的实现；本文聚焦资源受限场景，提出三个开放问题：微控制器上的AI部署、轻量级通信协议下的分布式多节点协调、融合剩余寿命估计与可解释AI的分层数字孪生编排。与现有工作相比，本文的创新在于通过547篇论文的系统综述建立了混合架构分类法，并明确指出了当前缺乏同时满足工业5.0要求的集成嵌入式-分布式分层解决方案这一关键空白。

### Q3: 论文如何解决这个问题？

论文通过系统性文献综述方法，提出了一个面向预测性维护的多智能体系统与数字孪生融合的参考架构。核心方法遵循PRISMA协议，从547篇论文中筛选出73篇高质量文献进行主题分析。架构设计上识别出五大混合架构家族：富客户端-服务器架构、分布式雾-边缘架构、全息递归架构、嵌入式自主智能体架构和工业元宇宙架构。关键技术包括：在通信协议层面，推荐MQTT-SN和Nanopb（Protobuf）作为嵌入式MAS的轻量级方案，其消息体积比JSON减少60-80%；在硬件平台层面，提出三层部署体系——STM32F4系列微控制器（2MB Flash/256KB RAM）作为本地智能体、Raspberry Pi/Jetson Nano作为雾协调器、云端服务器作为工厂级管理；在AI方法层面，创新性地提出混合自编码器+1D-CNN架构，自编码器作为无监督异常检测哨兵（MSE重建误差），1D-CNN作为监督故障分类专家，通过级联逻辑仅在检测到异常时激活高计算量模型，平均计算负载降低。此外，结合LSTM进行剩余寿命估计，并集成SHAP等可解释AI技术提升运维决策可信度。该架构的核心创新在于首次系统性地解决了资源受限嵌入式环境下的分布式多节点协调、轻量级通信协议选择、以及层次化数字孪生编排三大技术瓶颈。

### Q4: 论文做了哪些实验？

该论文是一篇系统性综述，并未进行新的实验，而是对现有文献进行了批判性分析。论文基于对547篇高影响力期刊论文的回顾，建立了混合架构的分类法，并识别了技术瓶颈。论文通过对比分析，总结了五大类混合数字孪生与多智能体系统架构：富客户端-服务器、分布式雾-边缘、全息递归、嵌入式自主智能体和工业元宇宙架构。在通信协议方面，论文比较了MQTT、OPC-UA、CoAP、Nanopb等协议的开销、QoS、安全性和MCU兼容性，指出Nanopb消息大小比JSON减少60-80%。在硬件平台方面，对比了STM32、ESP32、Raspberry Pi、NVIDIA Jetson Nano等平台的CPU、内存、成本和适用角色。在AI方法方面，对比了自编码器、1D-CNN、LSTM等模型在MCU上的Flash占用、推理延迟和精度，其中1D-CNN紧凑模型精度达88-97%，混合AE+CNN-1D模型精度>85%。主要发现是，尽管已有显著进展，但尚无系统能同时满足工业5.0的集成嵌入式-分布式分层解决方案要求。

### Q5: 有什么可以进一步探索的点？

尽管该综述系统性地梳理了多智能体系统与数字孪生在预测性维护中的融合架构，但现有方案仍存在显著局限。首先，**嵌入式与分布式层级间的深度集成尚未实现**：现有工作要么聚焦于云端高性能计算，要么局限于单一微控制器的轻量推理，缺乏一套能在资源受限节点上同时运行轻量级XAI（如简化版SHAP）并支持多节点协同的完整框架。其次，**可解释性与实时性的矛盾未有效解决**：SHAP和Grad-CAM的计算开销在工业RTOS环境下难以满足毫秒级响应，未来可探索基于知识蒸馏的轻量级解释器，或利用联邦学习在边缘侧分布式计算特征贡献度。此外，**跨生命周期的一致性维护**是盲区：物理系统的概念漂移要求数字孪生持续更新，但现有MAS缺乏层级间模型版本同步与错误传播抑制机制。建议引入基于区块链的轻量级共识协议（如改进的PBFT）来记录模型更新日志，并结合元学习实现自适应漂移检测。最后，**安全攻击面**的防御仍停留在理论层面，可设计一种“哨兵-智能体”架构，通过对抗性训练和异常行为模式库实时检测传感器欺骗与模型窃取攻击。

### Q6: 总结一下论文的主要内容

这篇综述论文系统探讨了多智能体系统与数字孪生在预测性维护中的融合。核心贡献在于：针对工业4.0背景下数字孪生日益增长的复杂性，提出了一种混合架构分类法，并识别了关键研究空白。方法上，作者批判性分析了547篇高影响力期刊论文，建立了从架构、技术到开放问题的系统性框架。主要结论指出，尽管已有显著进展，但现有系统均未能提供一个同时满足工业5.0要求的集成式嵌入式-分布式层次化解决方案。论文明确提出了三个开放研究挑战：资源受限微控制器上的AI部署、基于轻量级通信协议的分布式多节点协调，以及融合剩余寿命估计与可解释AI的智能工厂层次化数字孪生编排。该研究的意义在于为未来构建自主、动态、可解释的工业预测性维护系统指明了方向。
