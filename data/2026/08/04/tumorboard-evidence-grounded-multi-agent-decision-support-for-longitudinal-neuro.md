---
title: "TumorBoard: Evidence-Grounded Multi-Agent Decision Support for Longitudinal Neuro-Oncology"
authors:
  - "Yantong Liu"
  - "Zheyu Zhang"
  - "Runpeng Liu"
  - "Mu Xitang"
  - "Seong-Yoon Shin"
  - "Hyun-Ae Lee"
date: "2026-08-04"
arxiv_id: "2608.03190"
arxiv_url: "https://arxiv.org/abs/2608.03190"
pdf_url: "https://arxiv.org/pdf/2608.03190v1"
categories:
  - "cs.AI"
tags:
  - "multi-agent"
  - "evidence routing"
  - "safety governor"
  - "adversarial critic"
  - "longitudinal case state"
  - "claim-evidence ledger"
  - "medical decision support"
  - "neuro-oncology"
  - "LLM agent"
  - "auditable reasoning"
relevance_score: 7.5
---

# TumorBoard: Evidence-Grounded Multi-Agent Decision Support for Longitudinal Neuro-Oncology

## 原始摘要

Neuro-oncology decisions require coordinated interpretation of serial MRI, pathology, molecular markers, treatment history, performance status, and evolving guidelines. We present TumorBoard, a multi-agent decision-support system built around a shared longitudinal case state and an auditable claim-evidence ledger. Specialist agents for radiology, neuropathology, molecular diagnosis, guidelines, and therapy planning produce atomic claims with provenance. An adversarial critic exposes contradictions, and a safety governor releases, qualifies, or defers recommendations according to evidence sufficiency and temporal validity. On a 360-case hidden benchmark at a matched token budget, TumorBoard achieved an action F1 of 0.772 and evidence entailment of 0.914. It exceeded the strongest typed-council baseline by 3.1 percentage points (95% CI: 1.6 to 4.7, adjusted p = 0.0012), while recommendation-to-evidence coverage reached 0.927. Under evidence deletion, the system deferred 84.2% of unsafe cases and limited harmful recommendations to 5.8%. The safety governor reduced harmful release by 7.8 percentage points at a false-deferral cost of 4.3 percentage points. Ablation studies of the ledger, critic, and governor produced the predicted failure patterns, establishing structured coordination as the source of the measured multi-agent advantage.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

TumorBoard旨在解决神经肿瘤学中多学科、纵向决策支持的核心难题。研究背景在于，神经肿瘤诊疗需整合序列MRI、病理、分子标志物、治疗史及体能状态等多源异构信息，且决策随疾病进展和分子重分类而动态变化，单一信息源或静态模型难以胜任。

现有方法存在显著不足：一是多智能体系统常因提示词更长、token更多或重复采样而虚增性能，缺乏对协调机制本身的严格对照；二是智能体间易产生“伪协作”，即重复陈述相同模型信念、放大早期错误，却未引入独立证据；三是临床决策缺乏可审计的证据溯源和时序有效性验证，导致推荐可能在新诊断时正确、进展后错误，或技术上成立但临床不安全。

因此，本文核心问题是：如何设计一个以证据为基础、可审计的多智能体协调协议，在严格控制推理预算的前提下，实现优于单模型和简单多智能体基线的决策支持，同时具备安全治理能力——在证据不足或时序失效时主动延迟或拒绝推荐，从而建立结构化协调带来的真实多智能体优势，而非token或提示工程造成的假象。

### Q2: 有哪些相关研究？

相关研究可归为三类。**方法类**：ReAct、Toolformer、Reflexion奠定了行动、工具调用与自我批判基础；AutoGen、CAMEL、MetaGPT、AgentBench提供多智能体编排模式。TumorBoard与它们的区别在于用类型化协议取代自由对话，消息携带声明、证据指针与前提条件，使协调失败可观测为图缺陷。**应用类**：临床知识基准与面向医生的研究进展迅速，证据总结与检索系统强调源绑定生成。TumorBoard聚焦纵向决策构建，处理时间上不相容的事实（如术前病理与术后增强），通过共享状态维护有效期与取代边，这是现有系统未专门设计的。**评测类**：AgentBench等提供评测经验，但TumorBoard引入可消融的协议字段（账本、批判者、安全阀）来验证结构化协调的贡献。与医学检索系统相比，TumorBoard要求工具返回带版本证据，且指南智能体保留人群、疾病状态等限定条件，安全阀在释放前检查患者状态是否满足前提，避免无依据综合。其核心差异在于将临床协调需求（版本化证据、源事件与派生结论分离、风险终止）显式编码为可审计协议。

### Q3: 论文如何解决这个问题？

TumorBoard通过一个多智能体协作框架解决神经肿瘤学纵向决策支持问题，其核心是共享的病例状态和可审计的声明-证据账本。整体架构包含五个关键模块：时间线策展器、专科智能体、对抗性评论家、安全治理器和主席总结器。

时间线策展器负责从原始数据中提取带时间戳的事件，区分事件时间与文档时间，规范化药物、影像、病理和分子实体，并标记时间矛盾。专科智能体包括放射学、神经病理学、分子诊断、指南和治疗规划五个角色，每个角色只能生成原子声明，且受角色边界限制——放射学智能体不能给出治疗建议，治疗规划器不能解读病理切片。

所有声明进入声明-证据账本，这是一个有向图结构，包含支持边、冲突边、取代边和依赖边，并强制图不变量：证据节点不可变，派生声明不能支持自身祖先，循环支持被拒绝。对抗性评论家接收病例状态和声明图，而非其他智能体的隐藏推理，通过固定挑战库检查缺失前提、过时来源、时间不一致、人群不匹配等问题，被挑战的智能体必须通过新证据、缩小声明、降低置信度或接受延迟来回应。

安全治理器按风险分层评估每条建议，检查前提完整性、证据蕴含、指南时效、矛盾状态和风险等级，输出支持、限定、延迟和阻止四种状态。主席汇总接受的声明，保留分歧，生成行动导向的笔记，但不能覆盖阻止状态。创新点在于结构化协调机制：账本保证可审计性，评论家防止虚假共识，治理器在证据不足时延迟84.2%的不安全病例，将有害建议限制在5.8%，消融实验证实了这三个组件各自贡献了可预测的失败模式。

### Q4: 论文做了哪些实验？

实验基于360例隐藏基准测试集，涵盖初诊、术后规划、监测、复发及安全集五个分层（共360例）。对比方法包括直接单模型提示、RAG智能体、单智能体计划-批评、自由聊天多智能体、无安全调控器的类型化协议多智能体及完整TumorBoard，所有变体在相同证据、检索、模型版本和token预算下运行。

主要结果：TumorBoard达到动作F1为0.772、证据蕴含0.914，超过最强类型化基线3.1个百分点（95% CI: 1.6-4.7，调整p=0.0012），推荐-证据覆盖率达0.927。在证据删除场景下，系统延迟84.2%不安全案例，有害推荐降至5.8%。安全调控器将有害发布降低7.8个百分点，误延迟成本为4.3个百分点。机制消融实验显示：移除账本使F1下降0.039，移除批评者使矛盾解决率下降0.112，移除调控器使有害发布增加0.078。系统每案例生成14,220 tokens，中位延迟21.8秒。

### Q5: 有什么可以进一步探索的点？

TumorBoard在结构化协同上展现了显著优势，但仍有若干可探索的深化方向。首先，当前证据账本依赖专家Agent的原子化声明，可引入跨模态时序推理，例如将MRI影像的纵向变化与分子标记动态关联，构建更细粒度的因果证据链。其次，对抗性批评者仅处理矛盾，可扩展为主动生成反事实场景（如“若延迟放疗会如何”），以强化决策鲁棒性。安全治理器的阈值虽可调，但可进一步设计自适应机制，根据病例风险等级动态调整释放/延迟策略，而非固定阈值。此外，系统在证据缺失时高度依赖延迟，未来可探索部分证据下的概率性推荐，并量化不确定性。最后，多Agent协同的token开销仍高，可引入分层路由或稀疏激活机制，仅对复杂病例启用全量专家，同时探索轻量级批评者蒸馏，以降低推理成本而不牺牲可审计性。

### Q6: 总结一下论文的主要内容

TumorBoard提出了一种面向神经肿瘤纵向诊疗的多智能体决策支持系统，核心贡献在于将跨学科推理转化为可审计的声明-证据流程。问题定义上，它需协调序列MRI、病理、分子标志物、治疗史及指南等多模态信息。方法上，系统构建共享纵向病例状态和证据账本，由放射学、神经病理学等专家智能体生成带溯源原子声明，对抗性评论者识别矛盾，安全治理器依据证据充分性和时间有效性决定发布、限定或延迟建议。在360例隐藏基准测试中，系统动作F1达0.772，证据蕴含0.914，超出最强基线3.1个百分点；证据删除时延迟84.2%不安全案例，有害建议仅5.8%。消融实验证实账本、评论者和治理器各自贡献，验证了结构化协调是多智能体优势来源，为高风险医疗场景提供了可衡量的协调架构。
