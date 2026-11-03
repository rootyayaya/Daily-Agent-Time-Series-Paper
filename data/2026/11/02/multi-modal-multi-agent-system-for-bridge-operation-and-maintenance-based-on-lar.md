---
title: "Multi-Modal Multi-Agent System for Bridge Operation and Maintenance based on Large Language Model"
authors:
  - "Xiangyun Luo"
  - "Yunkai Zhang"
  - "Yong Huang"
  - "Stephen Wu"
  - "Hui Li"
date: "2026-11-02"
arxiv_id: "2611.02738"
arxiv_url: "https://arxiv.org/abs/2611.02738"
pdf_url: "https://arxiv.org/pdf/2611.02738v1"
categories:
  - "cs.MA"
tags:
  - "Agentic Time Series"
  - "工业故障诊断"
  - "多智能体系统"
  - "知识图谱增强"
  - "可解释决策"
  - "桥梁运维"
  - "LLM Agent"
  - "物理机理约束"
relevance_score: 8.5
---

# Multi-Modal Multi-Agent System for Bridge Operation and Maintenance based on Large Language Model

## 原始摘要

Bridges are critical transportation infrastructure, and reliable operation and maintenance (O&M) is essential for traffic safety and long-term structural performance. However, bridge O&M faces key bottlenecks: no unified architecture coordinates heterogeneous resources; model inferences lack clear links to physical-mechanical laws; and experts' tacit knowledge remains difficult to formalize. This study proposes a knowledge-enhanced autonomy formalization methodology and apply it to construct the Bridge O&M Multi-Modal Multi-Agent System (BOMMA), which integrates heterogeneous diagnostic actions, physics-mechanics-informed representations, long-term memory, and structured experiential knowledge within a coordinated multi-agent workflow, enabling interpretable and traceable scheduling, analysis, and decision-making. On 3,492 multi-source instructions, the proposed method achieves scheduling recalls of 85.37% for simple and 99.40% for composite tasks, with 95.35% BERT F1-score for O&M action reasoning. Ablation studies confirm the contributions of the components in the autonomy. This study bridges general LLM reasoning and specialized bridge O&M requirements.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文针对桥梁运维（O&M）领域存在的三大瓶颈：缺乏统一架构协调异构资源、模型推理与物理力学规律脱节、专家隐性知识难以形式化。现有AI方法（如车辆荷载识别、损伤诊断、状态评估等）虽在各自子任务上表现良好，但作为孤立模块无法建立多源数据、多类算法与多级运维任务之间的系统级协同调度机制，导致“模块强、系统弱”的结构性矛盾。同时，通用LLM及其Agent在高度专业化的桥梁运维中面临“认知翻译障碍”：专家判断依赖难以言表的隐性知识，而现有方法通过自然语言提示扁平化注入领域知识，受限于上下文窗口和参数记忆幻觉，无法刻画实体间的层次、因果或逻辑关系。此外，即使通过知识图谱和RAG注入结构化知识，推理过程仍缺乏与底层物理机制的可解释映射，本质仍是统计关联驱动，难以满足高风险工程场景对安全性、可追溯性和可信性的严苛要求。因此，论文旨在提出一种知识增强的自主性形式化方法，将异构诊断动作、物理力学表征、长期记忆和结构化经验知识整合到协调的多智能体工作流中，实现可解释、可追溯的调度、分析与决策。

### Q2: 有哪些相关研究？

相关工作主要分为三支：其一，桥梁运维中的AI方法，包括Zhang等基于HardNet的车辆重识别、Deng等物理信息神经网络用于影响面识别、Zhang等SDIGLM多模态思维链损伤识别、Wei等VRNN生成式健康诊断、Deng等RoMS损伤识别、Qu等MVO-CNN-BiLSTM变形预测、Ju等ATT-BiGRU预警、Wei等深度强化学习维护决策、Zhang等MARPPO桥梁网络生命周期维护等，这些工作聚焦单一技术点，缺乏系统级协同。其二，LLM与Agent在土木工程的应用，如Yan等基于ReAct的智能建筑通用Agent、Deng等BIMgent、Du等Text2BIM多智能体框架、Chen等钢筋混凝土结构设计多智能体框架，以及数字孪生、城市管理、灾后恢复等场景，展示了Agent潜力但未解决领域知识形式化问题。其三，知识图谱与RAG增强LLM，如Lewis等RAG、Edge等Graph RAG、Luo等RoG，以及桥梁运维KG应用（Zhang等BMKG、Wang等BMKG-DCoT、Luo等桥梁检测KG、Fang等桩基施工KG、Gao等GraphSAGE嵌入学习等）。论文指出，这些KG/RAG方法虽缓解幻觉，但推理仍缺乏与物理力学原理的可解释对应，本文通过物理-力学动作空间和结构化知识图谱的协同设计来弥补这一空白。

### Q3: 论文如何解决这个问题？

论文提出知识增强的自主性形式化方法，并构建BOMMA（Bridge O&M Multi-Modal Multi-Agent System），核心是一个三层互补的自主性机制。第一层是组织层：高度自主的多智能体框架，支持自导向管理、可扩展扩展、深思熟虑的任务规划和自适应串并行动作空间分配，以处理复合运维场景。第二层是执行层：物理-力学增强的动作空间，将分散的检测、监测和评估工具整合为标准化的、语义可调度的功能单元，包括数据质量评估（DQA）、车辆荷载时空分布识别（VEH）、多模态思维链表观损伤诊断（VIS）、车-损解耦在线损伤诊断（VDD）、结构响应相关性状态诊断（STG）、自适应桥梁预警（AEW）和运维专家知识库（KMD）等，每个动作都嵌入物理力学原理，为动作理解、调度和结果分析提供严谨可解释的推理链。第三层是经验知识层：通过知识图谱增强的领域知识模块，利用LLM的少样本/零样本能力从非结构化历史检测报告中自动抽取四层本体（结构实体层、缺陷/损伤演化层、危险约束层、运维处置层）的图谱元组，构建结构化语义嵌入，在决策阶段通过语义嵌入相关性匹配起始节点并进行L跳扩展检索，形成可追溯的专家推理证据链。整个工作流以“理解-分解-执行-决策”闭环运行：指令首先根据动作空间分解为子任务序列，子智能体并行执行并反思，动作推理基于物理原理生成，最终决策融合检索到的知识子图和全部前置推理。论文还给出了形式化概率分解（式1-4）和伪代码，强调通过模块干预钩子在推理各阶段注入事实约束，缩短黑箱推理跨度，使可解释性源于知识约束的刻意放置而非事后解释。

### Q4: 论文做了哪些实验？

论文在3,492条多源指令上评估BOMMA。主要结果：简单任务调度召回率达85.37%，复合任务调度召回率达99.40%，运维动作推理的BERT F1-score为95.35%。实验还定义了复合指令的调度精确率C-Pre、召回率C-Rec、ExactMatch（无需进一步干预即完全满足意图的复合指令比例）、平均人工干预次数Itv、平均相对任务时间R-Time等指标，以及BERT精确率、召回率和F1。消融实验验证了自主性各组件（如记忆模块、物理-力学动作空间、知识图谱检索等）的贡献，通过比较完整架构与不完整架构下零人工干预完成意图的复合指令数量（n_Com vs n_Inc）以及额外人工干预次数和任务时间，确认了各组件的必要性。论文未提及与传统基线（如纯LLM提示、无知识图谱的Agent）的详细对比数值，但通过消融和指标设计展示了系统在调度准确性和动作推理质量上的优势。

### Q5: 有什么可以进一步探索的点？

论文的局限性包括：实验主要在自构建的3,492条指令集上进行，缺乏与公开基准或真实桥梁长期运维数据的广泛验证；知识图谱的自动构建依赖LLM抽取质量，可能存在噪声和覆盖不全；物理-力学动作空间目前以预定义动作单元为主，对新动作的自动创建和演化机制（如ACR动作创建器）仅简要提及，其可靠性和泛化性有待深入；多智能体工作流的反思终止条件和干预钩子的设计细节未充分展开；系统在实时性、计算开销和部署成本方面未做评估。未来方向可包括：将框架迁移到其他基础设施（如大坝、隧道）的运维；引入更严格的verifier和证据路由机制以提升决策可信度；探索self-evolving skill和反馈优化，使动作空间和知识图谱能持续从运维反馈中学习；结合时序基础模型增强对监测数据的语义描述和报告生成能力；开展真实桥梁的长期部署与专家对比评估。

### Q6: 总结一下论文的主要内容

论文提出了一种知识增强的自主性形式化方法，并构建了基于大语言模型的桥梁运维多模态多智能体系统BOMMA。该系统通过三层设计解决桥梁运维中资源协调、物理机理脱节和隐性知识形式化三大瓶颈：组织层采用多智能体工作流实现自主任务规划与调度；执行层构建物理-力学增强的动作空间，将异构诊断工具标准化为可调度单元并提供可解释推理链；经验知识层利用LLM自动从历史报告中抽取知识图谱，形成四层本体和可追溯证据链。系统以“理解-分解-执行-决策”闭环运行，在3,492条指令上实现简单任务85.37%、复合任务99.40%的调度召回率，动作推理BERT F1达95.35%，消融实验验证了各组件贡献。该工作桥接了通用LLM推理与专业桥梁运维需求，为高风险工程场景提供了可解释、可追溯的智能决策范式。
