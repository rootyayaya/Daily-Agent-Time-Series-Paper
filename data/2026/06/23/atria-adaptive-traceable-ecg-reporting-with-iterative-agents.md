---
title: "ATRIA: Adaptive Traceable ECG Reporting with Iterative Agents"
authors:
  - "Donggyun Hong"
  - "Kyuhwan Lee"
  - "Junmyung Kwon"
  - "Yong-Yeon Jo"
date: "2026-06-23"
arxiv_id: "2606.24392"
arxiv_url: "https://arxiv.org/abs/2606.24392"
pdf_url: "https://arxiv.org/pdf/2606.24392v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "可解释时间序列分析"
  - "工业故障诊断"
  - "LLM/Agent 工作流"
  - "multi-agent reasoning"
  - "证据路由"
  - "可追溯诊断链"
  - "time series report"
  - "自然语言报告生成"
  - "迭代式报告生成"
  - "临床ECG报告"
  - "交互式验证"
relevance_score: 8.5
---

# ATRIA: Adaptive Traceable ECG Reporting with Iterative Agents

## 原始摘要

Existing ECG report generation is tightly coupled -- interpretation and reporting fused end-to-end, so errors propagate without stage-level recourse -- while agent-based systems decouple tasks but remain single-pass, never revisiting earlier outputs. Clinical ECG reporting instead unfolds iteratively, requiring progressive context integration and bidirectional editing. We present \textsc{ATRIA}, a multi-agent ECG reporting system that mirrors the clinician's iterative workflow: it binds every report claim to its supporting evidence, flags statements unsupported by that evidence, incorporates additional context mid-session, and lets clinicians verify and revise individual findings rather than accept one opaque output. Because its agents use ECG analysis models already in clinical use, the underlying findings are clinically trustworthy; and as a cloud-based web service, \textsc{ATRIA} is ready for immediate deployment. We demonstrate \textsc{ATRIA} through four interaction cases, with a live demo and video available.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

现有ECG报告生成方法存在两大不足：一是端到端流水线将ECG解读与报告生成紧密耦合，导致错误无法在阶段层面修正而直接传播至最终报告；二是基于智能体的系统虽解耦了任务，但仍是单次处理模式，不会回溯或优化早期输出。临床ECG报告撰写本质上是一个迭代过程，需要逐步整合上下文（如中途加入化验值、比较既往记录）并进行双向编辑。本文提出的ATRIA系统旨在解决上述问题，其核心目标是将ECG报告生成从不可追溯的单次输出转变为可审计、可交互的迭代工作流。具体而言，ATRIA通过多智能体协作实现四个关键特性：阶段级可追溯性（每个报告声明绑定证据源）、渐进式上下文整合（支持中途补充信息）、双向迭代使用（无需重跑流水线即可处理后续请求），并集成已在临床使用的ECG分析模型以确保结果可信。最终使临床医生能够验证、追踪和修正每个发现，而非被动接受单一不透明输出。

### Q2: 有哪些相关研究？

相关研究可分为三类。**方法类**包括基于LLM的零样本诊断、指令微调、多模态心电-语言建模和检索增强推理，这些方法将心电解释与报告生成融合为端到端步骤，错误会传播且无法分阶段纠正。**系统类**是Agent系统，它们将任务解耦为多个专用代理，但仍是单次处理，不回溯或优化早期输出。**应用类**是临床心电报告流程，需要迭代式上下文整合和双向编辑（如中途加入化验值、对比既往记录）。本文与上述工作的核心区别在于：ATRIA通过多代理系统模拟临床医生的迭代工作流，实现了**阶段级可追溯性**（每个报告声明绑定证据）、**渐进式上下文整合**（允许会话中补充输入）、**双向迭代使用**（无需重新执行即可处理后续请求），并集成了临床已部署的心电模型，而非研究原型。这解决了端到端方法错误传播和单次Agent系统无法迭代修改的问题。

### Q3: 论文如何解决这个问题？

ATRIA通过多智能体协作架构将临床心电图报告的迭代工作流形式化。核心设计围绕**阶段级可追溯性**、**渐进式上下文整合**和**双向迭代使用**三个需求展开，采用两个关键架构决策：阶段级交接（每个阶段输出显式可检查的中间产物）和共享存储（所有智能体读写同一存储，支持增量更新）。

整体框架包含五个智能体模块：
1. **编排器智能体**：负责会话状态维护和任务路由，不执行分析或生成。它将多个分析产物绑定到同一会话，使下游报告可跨记录推理。
2. **分析智能体**：调用临床已部署的AiTiA ECG模型（检测左心室收缩/舒张功能障碍、主动脉瓣狭窄、急性心梗等），结合实验室值等可选上下文，生成结构化发现和信号级证据，输出分析清单。
3. **报告智能体**：消费分析清单生成分节报告（临床印象、特征摘要、AI/规则发现、导联观察、建议、注意事项、附件）。每个报告节绑定到上游产物子集，支持部分重写——仅当相关产物变化时才重新生成受影响节段。
4. **文献智能体**：为报告声明提供外部证据，自动选择跨产物支持弱的声明或用户指定的声明，从ECG知识库检索相关段落作为文献证据产物。
5. **审查智能体**：检查草稿与所有累积产物的一致性，识别遗漏发现、证据与内容不匹配、无支持或矛盾声明，返回结构化反馈给报告智能体和编排器进行定向修订。

创新点在于：将临床迭代工作流映射为多智能体系统，实现报告声明与证据的双向绑定；通过共享存储和部分重写机制支持增量更新，避免全流水线重执行；所有分析模型已在临床使用，确保底层发现可信；通过聊天界面降低临床采用门槛。

### Q4: 论文做了哪些实验？

论文通过四个交互用例展示了ATRIA系统的核心功能，每个用例模拟了临床医生在ECG报告解读与修正中的常规步骤。实验设置基于多智能体工作流，包括编排器、分析、报告、审查和文献智能体。没有使用标准数据集或基准测试，而是通过具体案例演示系统能力。主要结果如下：**用例1**展示审查智能体标记初始报告中缺乏上游证据支持的陈述，例如引用了指南内容但未提供相应数据。**用例2**演示用户附加实验室值（如肌钙蛋白0.06 ng/mL、BNP 155 pg/mL）后，系统重新调用分析智能体，仅更新受影响部分（临床印象从“无明确STEMI证据”改为“轻度肌钙蛋白升高，不能排除急性心肌损伤”），并新增关于心血管风险因素的建议。**用例3**中，用户对“窦性心动过缓（HR ~48 bpm）”陈述请求文献证据，文献智能体检索到相似度0.76-0.83的段落，并绑定为证据。**用例4**展示比较两份ECG记录（宽QRS心动过速 vs. 房颤），系统逐节段生成对比报告，突出心率、QRS时限、电轴等关键差异。这些用例验证了系统在证据追溯、上下文整合和双向编辑方面的能力。

### Q5: 有什么可以进一步探索的点？

论文的主要局限性在于：当前ATRIA系统仅通过四个交互案例进行演示，缺乏大规模临床验证和定量评估，其可追溯性和迭代编辑的实际效果尚未在真实临床环境中得到严格测试。此外，系统依赖的ECG分析模型虽已临床使用，但多智能体协作的延迟和计算开销可能影响实时性，且证据绑定机制对复杂心律失常的覆盖范围有限。

未来可探索的方向包括：1）引入更丰富的临床上下文，如患者病史、用药记录和连续ECG趋势，增强渐进式上下文整合能力；2）强化验证模块，例如结合因果推理或对抗性验证来检测虚假关联，提升证据链的鲁棒性；3）扩展人机交互方式，支持医生通过自然语言直接修正特定发现，而非仅通过预设接口；4）在真实临床工作流中部署并开展前瞻性研究，评估其对报告准确性、医生工作负荷和患者预后的影响。此外，可探索将多模态数据（如超声心动图）纳入智能体协作框架，实现更全面的心脏诊断支持。

### Q6: 总结一下论文的主要内容

论文提出ATRIA系统，针对现有ECG报告生成中端到端耦合导致错误传播、以及基于智能体的单次处理无法迭代修正的问题。核心贡献是设计了一个多智能体系统，模拟临床医生迭代式ECG报告工作流程。方法上，ATRIA将报告中的每个声明绑定到其支持证据，并验证声明是否被证据支持；支持渐进式上下文整合（如中途加入化验值、既往记录）和双向迭代编辑，允许医生验证和修改单个发现，而非接受单一不透明输出。系统集成了已在临床使用的ECG分析模型，并作为云Web服务部署，具备即时可用性。通过四个交互案例演示，ATRIA实现了阶段级可追溯、可迭代修正的报告生成，将一次性生成转变为可审计、交互式的工作流，提升了临床报告的可信度和实用性。
