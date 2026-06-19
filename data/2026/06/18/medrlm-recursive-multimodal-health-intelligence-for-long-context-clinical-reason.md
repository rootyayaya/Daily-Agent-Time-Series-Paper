---
title: "MedRLM: Recursive Multimodal Health Intelligence for Long-Context Clinical Reasoning, Sensor-Guided Screening, Evidence-Grounded Decision Support, and Community-to-Tertiary Referral Optimization"
authors:
  - "Aueaphum Aueawatthanaphisut"
date: "2026-06-18"
arxiv_id: "2606.20164"
arxiv_url: "https://arxiv.org/abs/2606.20164"
pdf_url: "https://arxiv.org/pdf/2606.20164v1"
categories:
  - "cs.CL"
  - "cs.AI"
  - "cs.LG"
  - "q-bio.QM"
tags:
  - "LLM/Agent用于时间序列异常检测"
  - "传感器引导推理"
  - "临床决策支持"
  - "多模态健康智能"
  - "证据图记忆"
  - "递归推理"
  - "不确定性门控精炼"
  - "长上下文推理"
  - "传感器信号分析"
  - "可追溯诊断链"
relevance_score: 7.5
---

# MedRLM: Recursive Multimodal Health Intelligence for Long-Context Clinical Reasoning, Sensor-Guided Screening, Evidence-Grounded Decision Support, and Community-to-Tertiary Referral Optimization

## 原始摘要

Real-world clinical decision support requires reasoning over heterogeneous and longitudinal patient information rather than answering isolated medical questions. However, current medical large language models and retrieval-augmented generation systems often rely on single-step prompting or retrieval, which can be fragile when clinical evidence is distributed across long electronic health records, medical images, sensor streams, guidelines, and referral constraints. This paper proposes MedRLM, a Recursive Multimodal Health Intelligence framework for long-context clinical reasoning, sensor-guided screening, and community-to-tertiary referral support. Instead of compressing all patient information into one prompt, MedRLM treats the patient case as an external clinical environment that can be recursively inspected, decomposed, retrieved, verified, and synthesized. The framework coordinates specialized agents for clinical text, longitudinal EHR, medical imaging, physiological sensor signals, guideline retrieval, uncertainty auditing, and referral planning. It further introduces a Clinical Evidence Graph Memory to connect patient-specific observations with retrieved evidence, standardized definitions, sensor-derived biomarkers, and referral criteria. A sensor-guided recursive triggering mechanism activates deeper reasoning when abnormal physiological or behavioral patterns are detected, while uncertainty-gated refinement supports clinician review for high-risk or low-confidence cases. We also outline a real-data evaluation design using public and credentialed clinical datasets spanning EHR, radiology, ECG, ICU time series, and referral-proxy outcomes. MedRLM aims to move medical AI from static question answering toward auditable, multimodal, and workflow-aware clinical decision support.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

临床决策支持系统需要处理异质且纵向的患者信息，而不仅仅是回答孤立的医学问题。然而，当前的医学大语言模型和检索增强生成系统通常依赖单步提示或检索，当临床证据分布在长程电子健康记录、医学影像、传感器数据、临床指南和转诊约束中时，这种处理方式容易导致上下文丢失、幻觉、可追溯性差和推理不可靠。现有长上下文模型存在长上下文退化问题，即位于长输入中间的信息被利用不足，且性能随上下文长度和任务复杂度增加而下降。此外，大多数医学RAG系统以检索为中心，未能将临床工作流建模为整合患者长期病史、传感器生物标志物、多模态证据、不确定性估计和转诊决策的递归过程。本文提出MedRLM框架，旨在解决上述问题，将患者数据视为可递归检查、分解、检索、验证和综合的外部临床环境，通过协调专门智能体、构建临床证据图记忆、引入传感器引导的递归触发和不确定性门控精炼，实现从静态问答向可审计、多模态、工作流感知的临床决策支持的转变。

### Q2: 有哪些相关研究？

相关研究主要分为四类。第一类是长上下文推理方法，如LongBench揭示了长上下文理解的困难，而递归语言模型（如SRLM、λ-RLM）通过外部化长提示并递归处理信息来应对。MedRLM借鉴了递归思想，但将应用领域从通用任务转向临床推理，并协调多模态数据而非仅处理文本。第二类是医学大语言模型，如Med-PaLM系列和LLaVA-Med，它们在医学问答和视觉-语言任务上表现出色。然而，这些模型主要作为答案生成系统，缺乏对长病史、传感器触发推理和转诊路径优化的显式机制。MedRLM通过将LLM定位为递归临床控制器来弥补这一不足。第三类是检索增强生成（RAG）系统，如MEDRAG和MIRAGE，它们通过外部知识检索提升事实性。MedRLM扩展了RAG，将其整合到递归工作流中，使检索结果不仅用于回答问题，还用于更新风险评估、不确定性评估和转诊规划。第四类是纵向电子健康记录（EHR）建模，如EHRSHOT，但仅关注结构化数据。MedRLM则结合了纵向患者表征、传感器数字生物标志物和多模态证据检索，专门优化社区到三级医院的转诊决策，这与现有系统仅关注问答或单模态分析有本质区别。

### Q3: 论文如何解决这个问题？

MedRLM通过将患者数据视为可递归检查的外部临床环境来解决长上下文临床推理问题，核心设计包括四个主要组件：

1. **递归临床控制器**：这是框架的核心，通过上下文复杂度函数κ(q, E_p)评估任务难度。当复杂度超过安全阈值K时，控制器将临床查询分解为多个模态特定的子任务（如文本、EHR、影像、传感器、指南等），分别处理后再通过合成算子Ω(·)整合结果。这种递归机制避免了将长序列压缩到单一提示中的信息损失。

2. **多模态专业智能体**：每个子任务由专门的智能体处理，包括文本实体提取、EHR时间线分析、图像VLM异常检测、传感器编码器生物标志物触发、临床RAG指南匹配和转诊路径规划。这些智能体并行工作，各自输出专业分析结果。

3. **临床证据图记忆**：构建可审计的知识图谱，节点代表患者观察、临床实体、异常发现、生物标志物、指南陈述和转诊标准，边表示时序、语义或因果关系。每个证据节点以三元组（观察、来源、临床定义）形式存储，确保可追溯性。

4. **传感器引导的递归触发与不确定性门控**：当传感器检测到异常生理或行为模式时，自动触发更深层的推理。同时，不确定性审计器评估自一致性、置信度和冲突，对高风险或低置信度案例启动人工审核循环。

创新点包括：递归临床分解策略、多模态证据图记忆、传感器触发的自适应推理，以及不确定性门控的转诊优化，最终输出风险评分、证据解释、转诊建议和完整审计轨迹。

### Q4: 论文做了哪些实验？

论文使用多个真实临床数据集构建了MedRLM的评估基准，覆盖其核心输入模态。实验设置包括：MIMIC-IV v3.1（364,627名患者，546,028次住院）用于长上下文EHR推理；MIMIC-CXR-JPG v2.1.0（377,110张胸片）和CheXpert（224,316张胸片）用于影像-报告多模态证据对齐；PTB-XL v1.0.3（21,799份12导联ECG）用于传感器引导的递归筛查；PhysioNet/CinC Challenge 2012（12,000次ICU住院）用于生理时间序列死亡率预测；eICU-CRD v2.0（超过200,000次ICU入院）用于外部ICU验证和转诊代理决策。对比方法方面，论文未明确列出具体基线模型，但通过数据集设计隐含对比了单步提示或检索的现有方法。主要结果显示，该基准成功覆盖了MedRLM所需的所有证据通道，但指出直接社区-三级转诊标签在公共数据集中稀缺，因此转诊实验需使用临床可辩护的代理结局（如ICU入院、院内死亡率、急性恶化、再入院、专科升级或远程ICU干预）。关键数据指标包括：MIMIC-IV的94,458次ICU停留、PTB-XL的18,869名患者、CheXpert的65,240名患者等。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在：1) 框架复杂度高，多智能体协调与递归推理可能带来计算开销和延迟，影响实时性；2) 依赖外部知识库和传感器数据的质量与标准化程度，实际部署中数据异构性和缺失问题可能削弱性能；3) 不确定性门控机制虽引入人工审核，但未明确如何量化“高风险”或“低置信度”的阈值，可能增加临床负担。未来可探索：1) 设计轻量化递归推理策略，如自适应深度控制或知识蒸馏，平衡效率与准确性；2) 引入在线学习或联邦学习，使模型能动态适应不同医疗机构的本地数据分布；3) 开发可解释的置信度校准方法，结合贝叶斯不确定性估计或对抗验证，减少人工干预需求；4) 扩展至多中心前瞻性临床试验，验证框架在真实转诊流程中的鲁棒性与临床效益。

### Q6: 总结一下论文的主要内容

MedRLM提出了一种递归多模态健康智能框架，旨在解决真实临床决策中需处理异构、纵向患者信息而非孤立问答的挑战。当前医疗大语言模型和检索增强生成系统常因单步提示或检索而脆弱，尤其当证据分散于长电子健康记录、医学影像、传感器数据、指南和转诊约束中。MedRLM将患者案例视为可递归检查、分解、检索、验证和综合的外部临床环境，协调文本、EHR、影像、生理信号、指南检索、不确定性审计和转诊规划等专业智能体。其核心创新包括临床证据图记忆，连接患者观察与检索证据及转诊标准；传感器引导的递归触发机制，在检测到异常生理模式时启动深度推理；以及不确定性门控精炼，支持高风险病例的临床审查。该框架旨在推动医疗AI从静态问答转向可审计、多模态、工作流感知的临床决策支持，特别适用于资源有限的社区医疗场景，优化从社区到三级医疗的转诊路径。
