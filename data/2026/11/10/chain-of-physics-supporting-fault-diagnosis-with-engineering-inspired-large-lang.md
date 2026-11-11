---
title: "Chain of Physics: Supporting Fault Diagnosis with Engineering-Inspired Large Language Model Reasoning"
authors:
  - "Wenqi Zhou"
  - "Leonardo Baldo"
  - "Kai Goebel"
  - "Manuel Arias Chao"
date: "2026-11-10"
arxiv_id: "2611.14263"
arxiv_url: "https://arxiv.org/abs/2611.14263"
pdf_url: "https://arxiv.org/pdf/2611.14263v1"
categories:
  - "cs.LG"
  - "eess.SP"
tags:
  - "LLM故障诊断"
  - "知识图谱"
  - "RAG"
  - "工业传感器解释"
  - "可解释诊断链"
  - "证据路由"
  - "物理量-故障关联"
  - "Chain of Physics"
  - "FailureSensorIQ"
  - "约束知识图谱"
relevance_score: 8.5
---

# Chain of Physics: Supporting Fault Diagnosis with Engineering-Inspired Large Language Model Reasoning

## 原始摘要

Fault diagnosis in complex systems requires linking observed changes in physical quantities to the failure mechanisms that produce them. Experienced engineers perform this task by combining sensor information with knowledge of system behavior and fault propagation. Large Language Models (LLMs) can support this process, but their diagnostic reasoning depends on the availability of asset-specific engineering knowledge and on how this knowledge is represented and used during inference. This work introduces Chain of Physics (CoP), an LLM-based fault-diagnosis framework built around a Constrained Knowledge Graph (CKG) generated automatically from asset-specific reference documentation. CoP addresses failure-sensor association from textual engineering knowledge. The CKG stores diagnostic chains connecting failure modes, changes in physical quantities, and monitoring sensors. During inference, semantically similar graph paths are retrieved for each question and used as both information and in-context examples for the reasoning process. Candidate failure modes are extracted from the question and analysed independently through dedicated LLM calls, which generate plausible failure-to-observation chains. A final decision module compares these chains with the available answer choices. CoP is evaluated on the FailureSensorIQ benchmark across four industrial asset classes and three LLMs. Compared with direct prompting and conventional Retrieval-Augmented Generation (RAG), CoP improves diagnostic accuracy across all evaluated models, with gains ranging from 7.8 to 19.6 percentage points and from 11.7 to 18.2 percentage points, respectively. The results show that structured engineering knowledge can improve LLM-based diagnostic reasoning when graph retrieval is combined with in-context examples of fault propagation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于复杂系统故障诊断中“从工程知识到故障—传感器关联”的推理问题。研究背景是：故障诊断需要将观测到的物理量变化与产生该变化的失效机制联系起来，经验丰富的工程师依靠系统行为知识和故障传播规律完成这一任务；而相关工程知识通常分散在技术手册、故障排查流程和维护记录中，其整合高度依赖人工。大语言模型虽可辅助这类知识密集型任务，但往往缺乏资产专用的工程知识，容易产生幻觉或物理上不一致的诊断解释。现有方法存在两方面不足：一是任务专用模型需要代表性标注数据，且新资产或新故障出现时需重新训练；二是常规检索增强生成（RAG）虽能引入外部文档，但仅提供非结构化信息，不能保证模型重建“故障—物理量变化—传感器观测”这一物理序列。此外，手工构建资产专用知识图谱工程量大，且普通图谱未必保留诊断所需的物理链条。因此，本文要解决的核心问题是：如何自动从资产参考文档中构建受约束的知识图谱，并在推理时以结构化的故障到观测链条同时作为领域知识和上下文推理范例，引导LLM生成物理一致的诊断链，从而在无需任务专用训练的情况下提升故障—传感器关联诊断的准确性。

### Q2: 有哪些相关研究？

本文相关工作主要分为三类。方法类：RAG（Lewis等）从外部文档检索文本作为上下文；StructGPT（Jiang等）让LLM通过接口访问结构化数据；图检索方面，Knowledge Graph Prompting（Wang等）、RoG（Luo等）和Think-on-Graph 2.0（Ma等）利用实体、关系与路径组织外部知识；ICL方面，KICGPT（Wei等）将KG结构知识编码为示例引导推理。应用类：PHM领域有Li、Chen、Tsallis等的综述及Razaq对37项LLM+KG故障诊断研究的系统回顾；Liu等在航空装配、Nie等在CNC设备上结合KG与检索；Ma等提出FDRKG-LLM；Guo等用约束因果发现构建旋转机械故障传播图；Lin和Miao用双模式KG检索提升汽车故障诊断。知识构建类：Liao等、Wang等（GraphRAG-KM）、Marandi等从技术文档自动抽取KG。区别在于：CoP使用预定义约束模式（失效模式—物理量变化—传感器）构建CKG，并同时将检索路径作为信息与上下文示例，且在FailureSensorIQ多资产基准上以选择题准确率对比直接提示与常规RAG，而上述工作多限于单一设备或开放式生成评测。

### Q3: 论文如何解决这个问题？

论文提出的 Chain of Physics（CoP）框架将诊断推理组织为“故障机制→物理量变化→可观测传感器”的因果链，整体分为离线与在线两个阶段。离线阶段针对每类工业资产只执行一次：先用 Docling 将参考文档转为 Markdown 并按约 2000 字符分块；每个文本块送入专门的 LLM 调用，按结构化输出模式抽取一条连贯的监测场景，即一个故障模式、1 至 5 个有序的物理量变化（含变量、位置与增减方向）以及最终监测传感器。该抽取提示同时充当“接地门控”，只有文本块完整支持故障—物理变化—传感器关系时才保留，理论描述、设计公式等被丢弃；随后再做一次校验，剔除缺失节点、无物理变量步骤或存在重复节点（可能形成人为环）的候选链。被接受的链按固定关系转换为三元组：故障到首个物理效应用 results in，中间传播用 leads to，末端物理效应到传感器用 is monitored by，并用 KGGen 对各文本块生成的小图取并集，聚合成资产专属的约束知识图谱（CKG）。该图谱结构统一、紧凑，便于专家逐条核对与修正。在线阶段对每个问题独立执行：先澄清问题，一方面从 CKG 检索并扩展语义相似的诊断路径，另一方面抽取问题中的候选故障模式；随后对每个候选故障模式分别发起独立的 LLM 调用，以检索到的路径同时作为信息和上下文示例，生成该故障到观测的合理传播链；最后由 Judge 模块将各候选链与选项比对，完成答案选择。其创新点在于用结构化工程知识约束 LLM 推理、将复杂诊断分解为多次专用调用，并把图谱检索与故障传播的上下文示例相结合。

### Q4: 论文做了哪些实验？

论文在FailureSensorIQ基准上评估CoP框架，覆盖四类工业资产（如航空燃气轮机等）和三种LLM。任务为多项选择问答，包含失效模式到传感器（FM2Sensor）和传感器到失效模式两个方向，要求模型基于文本工程知识进行诊断关联推理，而非基于实测传感器数据的故障分类。对比方法为直接提示（direct prompting）和常规检索增强生成（RAG）。CoP先离线从资产参考文档构建约束知识图谱（CKG），在线检索语义相似路径作为上下文示例，并对每个候选失效模式独立调用LLM生成失效到观测的推理链，最后由决策模块与选项比对。主要结果显示，CoP在所有评估模型上均提升诊断准确率：相较直接提示提升7.8至19.6个百分点，相较RAG提升11.7至18.2个百分点。这表明将图检索与故障传播的上下文示例结合，可有效利用结构化工程知识改进LLM诊断推理。

### Q5: 有什么可以进一步探索的点？

论文的局限性与可探索方向主要有以下几点：其一，CKG 依赖资产专属参考文档自动抽取，抽取质量受文档完整性与表述规范性制约，对文档稀缺或非结构化的老旧设备适应性未知，未来可研究跨文档冲突消解与增量更新机制。其二，评估仅限 FailureSensorIQ 的多选题设定，未涉及真实传感器时序信号与连续工况，后续可将 CoP 与信号分类模型结合，实现"文本知识链+实测数据"的联合推理。其三，推理链由 LLM 生成但缺乏物理一致性校验，可引入定性物理仿真或 SDG 约束对生成链做可执行性验证，减少幻觉。其四，当前各候选故障模式独立分析，未建模多故障耦合与故障传播的时序演化，可扩展为动态因果图并支持多故障并发诊断。此外，检索仅基于语义相似度，可探索按物理量类型与传播路径的结构化检索策略。

### Q6: 总结一下论文的主要内容

论文针对复杂系统故障诊断中LLM缺乏资产专属工程知识、易产生物理不一致解释的问题，提出Chain of Physics（CoP）框架。其核心是从资产技术文档自动构建约束知识图谱（CKG），仅保留连接故障模式、物理量变化与监测传感器的完整诊断链。推理时，为每个问题检索语义相似的图谱路径，既作为资产知识，又作为上下文推理示例；随后提取候选故障模式并逐一独立分析，生成新的故障到观测链，最后由独立决策模块结合选项给出答案。在FailureSensorIQ基准上，覆盖四类工业资产与三种LLM，CoP相较直接提示和传统RAG分别提升7.8–19.6和11.7–18.2个百分点。结果表明，将结构化工程知识与图检索、故障传播示例相结合，可显著增强LLM诊断推理的准确性与物理一致性。
