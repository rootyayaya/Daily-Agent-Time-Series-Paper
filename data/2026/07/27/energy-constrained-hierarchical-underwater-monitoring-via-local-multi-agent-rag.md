---
title: "Energy Constrained Hierarchical Underwater Monitoring via Local Multi-Agent RAG"
authors:
  - "Mohamed Amine Janati"
  - "Laurent Gautier"
  - "Stéphane Barbot"
date: "2026-07-27"
arxiv_id: "2607.24313"
arxiv_url: "https://arxiv.org/abs/2607.24313"
pdf_url: "https://arxiv.org/pdf/2607.24313v1"
categories:
  - "cs.IR"
  - "cs.CV"
  - "cs.MA"
  - "cs.RO"
tags:
  - "Multi-Agent RAG"
  - "Edge AI"
  - "Underwater Monitoring"
  - "LangChain"
  - "Multimodal Embedding"
  - "Energy-Constrained System"
  - "Automated Reporting"
  - "Retrieval-Augmented Generation"
  - "Hierarchical Architecture"
relevance_score: 7.5
---

# Energy Constrained Hierarchical Underwater Monitoring via Local Multi-Agent RAG

## 原始摘要

Marine life monitoring is limited by strict energy constraints, poor underwater connectivity, and the high cost of transmitting raw multimodal data from remote deployments. This paper proposes a low-consumption underwater monitoring architecture that combines always-on edge sensing with selective high-performance local reasoning. The system follows a hierarchical master--satellite design in which ultra-low-power MAX78000/MAX78002 microcontrollers continuously monitor visual and acoustic signals, while an NVIDIA Jetson Orin NX is activated only for scheduled processing, event-driven analysis, or researcher interaction. Once active, the Jetson executes a fully local multimodal pipeline for data ingestion, visual target extraction, embedding-based indexing, species identification, retrieval-augmented reasoning, and automated reporting. BioCLIP/OpenCLIP embeddings are used to organize mission data, marine taxonomic references, scientific documents, and operational metadata in local ChromaDB collections. A dedicated identification layer combines visual similarity search, centroid-based classification, and supervised classifiers to support adaptive species recognition. A LangChain-based multi-agent framework coordinates query routing, structured analysis, energy management, hardware reconfiguration, and report generation. The architecture is evaluated through visual and acoustic monitoring case studies. The proposed system bridges ultra-low-power continuous sensing with local multimodal intelligence, enabling underwater stations to produce structured, researcher-ready knowledge while compressing local data for flexible acoustic, optical, or satellite transmission, minimizing both energy use and communication overhead.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

海洋生态系统监测面临严峻的能源约束、水下通信带宽有限以及远程部署原始多模态数据传输成本高昂等挑战。现有方法存在两难困境：持续运行高性能处理器（如GPU）会导致能耗过高，无法支持数月级的水下自主部署；而仅依赖超低功耗微控制器进行简单事件检测，又无法提供物种识别、上下文推理等高级科学分析能力。此外，传统监测流程往往依赖本地存储数据并在回收后处理，缺乏实时感知与自适应能力。本文旨在解决的核心问题是：如何设计一种层次化、能量自适应的水下监测架构，在保持超低功耗连续感知的同时，通过选择性激活高性能边缘计算节点，实现本地多模态检索、物种识别与智能推理，从而在严格能源约束下生成结构化的科研级知识，并压缩数据以适应声学、光学或卫星等低功耗传输方式。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**方面，TinyML和MCUNet等框架使微控制器能运行卷积模型，本文采用MAX78000/MAX78002实现超低功耗持续感知，但区别于这些纯微控制器方案，本文引入层级级联设计，仅在必要时激活高性能Jetson平台。**应用类**方面，现有工作如基于Raspberry Pi的入侵物种检测、Jetson深海爬行器部署等展示了各平台层的实用性，但本文创新性地将三者结合，形成“始终在线微控制器+按需激活高性能节点”的混合架构。**评测与模型类**方面，BioCLIP、CLIBD等视觉-语言模型及FishNet基准数据集为物种识别提供了基础，本文在此基础上构建了基于ChromaDB的检索增强管道，并引入LangChain多智能体框架进行查询路由、能量管理和报告生成，区别于传统单一模型推理，实现了可解释的检索增强式物种识别与结构化知识产出。

### Q3: 论文如何解决这个问题？

该论文提出了一种层级式低功耗水下监测架构，核心设计是将持续运行的超低功耗边缘感知与按需激活的高性能本地推理相结合。整体框架采用主从（master-satellite）结构：底层由MAX78000/MAX78002微控制器作为哨兵节点，持续运行轻量级神经网络模型进行声学与视觉事件检测，但不做完整科学解释；上层以NVIDIA Jetson Orin NX作为计算中枢，仅在定时调度、事件驱动或研究人员交互时被唤醒，执行完整的本地多模态处理流水线。

主要模块包括：1）检测感知数据摄取模块，负责从哨兵节点接收并规范化数据；2）目标定位模块，使用Grounding DINO Tiny（基于Swin-T骨干的开放词汇目标检测器）通过文本提示从图像中提取感兴趣区域；3）物种识别与嵌入索引模块，利用BioCLIP/OpenCLIP生成多模态嵌入，结合基于质心的分类、SVM监督分类器和视觉相似性搜索实现自适应物种识别，并将嵌入与元数据存入本地ChromaDB集合；4）检索增强推理模块，基于LangChain的多智能体框架协调查询路由、结构化分析、能量管理、硬件重配置和报告生成。

创新点在于：通过硬件唤醒与自保持电路实现微控制器到Jetson的低延迟事件驱动激活；构建完全离线的多模态RAG流水线，使水下监测站能在无云连接下生成结构化科研知识；支持三种运行模式（自主批处理、事件驱动混合、研究人员交互）以灵活权衡能耗与实时性。

### Q4: 论文做了哪些实验？

论文围绕能量约束下的分层水下监控系统，设计了视觉和声学两个监测案例实验。实验设置包括：超低功耗MAX78000/MAX78002微控制器持续感知，NVIDIA Jetson Orin NX在触发后执行本地多模态管道。视觉实验使用FishDet-M数据集（整合13个公开水下数据集，含105,556张图像和296,885个标注实例），训练时限制每图≤5个目标，最终训练集76,202张图像、95,199个实例，验证集9,626张、12,290个实例，测试集10,645张、14,060个实例。声学实验使用Watkins Marine Mammal Sound Database（12个主要鲸豚物种）和DeepShip噪声数据集，生成96×64 log-Mel频谱图，按70%/20%/10%划分训练/验证/测试集。对比方法方面，视觉模型采用Tinyissimo YOLO（原作者报告限制5目标后mAP提升约20%），声学模型在MAX78000上运行。主要结果：系统在视觉和声学案例中均实现了低功耗持续感知与本地多模态智能的融合，能够生成结构化知识并压缩数据用于灵活传输，显著降低能耗和通信开销。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：1) 物种识别依赖预定义分类中心和监督分类器，对未见类或罕见物种的泛化能力有限；2) 多智能体框架的协调逻辑相对简单，缺乏动态任务分解和自适应学习能力；3) 评估仅基于案例研究，缺乏量化能耗对比和长期部署的鲁棒性验证。

未来可探索：1) 引入增量学习或小样本学习机制，使识别层能在线适应新物种；2) 设计元学习或强化学习驱动的智能体调度策略，根据能量预算和任务优先级动态分配计算资源；3) 研究跨模态知识蒸馏，将Jetson的推理能力压缩到微控制器端，减少主节点唤醒频率；4) 探索联邦学习框架，使多个部署站点共享嵌入空间和分类器更新，提升群体智能。

### Q6: 总结一下论文的主要内容

该论文提出了一种面向水下监测的低能耗分层架构，结合了持续边缘感知与选择性高性能本地推理。系统采用主从设计，由超低功耗MAX78000/78002微控制器持续监测视觉和声学信号，而NVIDIA Jetson Orin NX仅在计划处理、事件驱动或研究人员交互时激活。激活后，Jetson执行完全本地的多模态流水线，包括数据摄取、视觉目标提取、基于BioCLIP/OpenCLIP嵌入的索引、物种识别、检索增强推理和自动报告。一个基于LangChain的多智能体框架协调查询路由、结构化分析、能量管理和报告生成。通过案例研究验证，该架构在降低能耗和通信开销的同时，能将原始水下数据转化为结构化的、可供研究人员直接使用的知识，实现了超低功耗持续感知与本地多模态智能的有效结合，对长期自主水下监测具有重要意义。
