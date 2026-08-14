---
title: "OmniScientist: An Omni-Modal Omni-Discipline AI Scientist"
authors:
  - "Bobo Li"
  - "Hao Fei"
  - "Tianjie Ju"
  - "Mong-Li Lee"
  - "Wynne Hsu"
date: "2026-08-13"
arxiv_id: "2608.13558"
arxiv_url: "https://arxiv.org/abs/2608.13558"
pdf_url: "https://arxiv.org/pdf/2608.13558v1"
categories:
  - "cs.AI"
  - "cs.CL"
tags:
  - "Agentic Time Series"
  - "LLM/Agent 工作流"
  - "多模态感知"
  - "科学发现自动化"
  - "证据路由"
  - "可追溯性"
  - "统计验证"
  - "多智能体协作"
  - "时序信号处理"
  - "端到端研究自动化"
relevance_score: 7.5
---

# OmniScientist: An Omni-Modal Omni-Discipline AI Scientist

## 原始摘要

Recent advances in foundation models have enabled AI scientists to automate increasingly complete research workflows, from hypothesis generation and code execution to manuscript preparation. Yet workflow coverage alone does not provide access to the full evidence on which scientific discovery depends. Existing systems typically reason over text, code, labels, or precomputed summaries, leaving scientifically decisive spatial, temporal, cross-channel, and procedural relations unavailable to the agent. We introduce OmniScientist, an end-to-end, omni-modal AI scientist that conducts multidisciplinary research directly from heterogeneous raw evidence. A perception layer and 3 autonomous agents for ideation, experiment, and writeup operate within a deterministic pipeline, allowing observations to shape research questions, experimental decisions, and final claims throughout the research lifecycle. By running idea, rigour, and claim checks in code, the system enforces novelty screening, statistical validity, execution provenance, and numerical traceability. We evaluate OmniScientist on 36 real-data cases spanning 5 discipline families, 4 families of scientific evidence, and modalities including images, signals, audio, video, 3-D structures, trajectories, tables, formulae, and graphs. The system completes the full path from raw data to a compiled manuscript in all 36 cases and achieves a mean overall paper score of 6.3 with the reference reasoning backbone. In paired comparisons against a blind variant that receives only precomputed scalar features, direct perception improves all 7 evaluation dimensions and wins 85% of head-to-head judgments. These results show that lifecycle-wide perception is essential for evidence-grounded scientific discovery and provides a practical path toward broadly capable AI scientists.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

现有AI科学家系统虽已覆盖从假设生成到论文撰写的完整工作流，但存在根本性缺陷：它们仅能处理文本、代码、标签或预计算摘要，无法直接访问原始科学证据中蕴含的空间、时间、跨通道和过程性关系。这种“工作流完整但证据不完整”的接口设计，导致智能体在探究开始前就继承了人为选择的表征，严重限制了其发现异常、提出假设和支撑结论的能力。尽管多模态模型已很强大，但科学多模态基准通常预先固定观测和问题，而现有科学智能体仅在局部环节（如图表检查）使用感知，未能建立观测驱动研究重定向的闭环。本文核心问题是：如何构建一个端到端、全模态、跨学科的AI科学家，使原始异构证据在整个研究生命周期中持续塑造问题选择、实验设计、结果审查和最终论文声明，同时通过代码强制检查确保新颖性、统计有效性、执行溯源和数值可追踪性，防止数据泄露和HARKing等问题。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**：早期工作聚焦单领域单仪器自动化（如实验室流程执行），后续扩展到跨学科真实数据（如基于衍射图谱提出假设）；近期系统如AI Scientist系列在软件仓库上实现从想法生成到稿件撰写的全流程自动化，并引入协作生态。**感知类**：通用多模态模型（如CLIP、视觉-语言模型）已具备强大感知能力，科学基准（如MicroVQA）在图表、显微图像、实验视频等上评测感知，但均将感知视为独立问答任务，由人类选择观测、提问并评判。**智能体类**：Agent实验室将工作分配给规划、编码、评审等角色，虚拟实验室协调领域专家，但均通过提示词和生成消息编排，阶段转换依赖模型输出可靠性。

本文与上述工作的核心区别在于：现有系统仅处理已被人类转化为文本、代码或数值的证据，忽略原始观测本身；且感知仅用于孤立阶段（如检查自身图表、读取软件界面）。OmniScientist首次让感知贯穿研究全生命周期——从问题形成到论文主张验证，并通过确定性流水线（代码控制阶段转换、验证输出锚定于真实观测、失败时回溯）克服了提示词编排的脆弱性，在36个跨学科真实案例上验证了全周期感知对证据驱动发现的关键作用。

### Q3: 论文如何解决这个问题？

OmniScientist通过一个端到端的全模态AI科学家框架来解决现有系统无法直接感知原始多模态证据的问题。其核心架构由感知层和三个自主智能体（构思、实验、撰写）组成，运行在确定性流水线中。

感知层是核心创新，它将原始证据按推理范式分为感知、符号、定量和程序四类证据家族，并细分为12种模态（图像、信号、音频、视频、3D结构、轨迹、表格、公式、图等）。该层采用分层观察策略：优先对原始数据进行原生数值分析（如提取FFT峰值、趋势点），仅在需要空间或结构模式时才调用视觉渲染，并通过预算约束控制视觉处理成本，实现灵活高效的感知。

三个智能体各司其职：构思智能体通过ReAct循环建立材料清单、检索文献（OpenAlex/Crossref）、生成至少5个候选想法并筛选最优假设；实验智能体在受控的run_python环境中迭代生成代码、调试执行，并整合至少4项分析（主检验+基线/消融/机制/敏感性）；撰写智能体根据5种结构规范生成符合学科惯例的论文，从执行记录中提取内容，确保数据一致性。

关键创新在于代码强制检查机制：构思阶段通过结构完整性、新颖性筛查和泄漏检查；实验阶段通过退出检查验证结果来源、多重比较校正、反HARKing保护；撰写阶段通过声明检查确保所有数字和主张可追溯到执行记录。这种以执行记录为唯一事实来源的设计，保证了从原始数据到最终论文的全程可追溯性和统计有效性。

### Q4: 论文做了哪些实验？

论文在36个真实数据集上进行了全面实验，覆盖5大学科家族和4类科学证据模态（图像、信号、音频、视频、3D结构、轨迹、表格、公式、图）。实验设置中，推理骨干模型（Claude Sonnet 5为主）驱动全部3个阶段，感知模型固定为Sonnet 5，评分由两个外部裁判（deepseek-v4-flash和gemini-2.5-flash-lite）完成。对比模型包括GPT-5.6、GLM-5.2、Kimi K2.7及开源Qwen3.5（9B/27B/122B）和Gemma-4（26B/31B）系列。

主要结果：Sonnet 5在全部36个案例中完成论文，平均综合得分6.5（全套均分6.3）；GLM-5.2在18个案例中完成17个，得分6.7；Kimi K2.7完成6/9个，得分6.5；GPT-5.6完成9/10个，得分5.7；开源模型中Qwen3.5 122B完成30/34个，得分5.4，而小模型表现较差（如Qwen3.5 9B仅4.1分）。消融实验显示，与仅接收预计算标量特征的盲变体相比，直接感知在全部7个评估维度（新颖性、严谨性、清晰度、重要性、可复现性、多模态接地、事实准确性）上均胜出，并在85%的成对比较中获胜。各学科和模态的中位综合得分稳定在6.1-7.1之间，且分数与篇幅相关性极低（ρ=0.16），排除了冗长偏差。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下几个方向展开：首先，当前系统虽覆盖多模态原始证据，但感知层仅依赖单一固定模型（Claude Sonnet 5），未来可探索多感知模型协同或自适应感知策略，以提升对复杂跨模态关系的捕捉能力。其次，评估维度虽含多模态grounding，但缺乏对科学发现“真理性”的深层验证——可引入外部知识库或实验复现机制，增强结论的可信度与可迁移性。第三，当前确定性流水线虽保证可追溯性，但可能限制创造性假设生成，可尝试引入动态反馈回路或强化学习，让系统根据中间实验结果自适应调整研究路径。此外，成本与步数限制（如50步实验、150秒超时）可能制约复杂任务深度，未来可设计分层预算分配或增量式探索策略。最后，可扩展至多智能体协作场景，让不同专长智能体并行处理多源证据，并通过辩论机制提升结论鲁棒性。这些方向将推动AI科学家从“流程自动化”向“深度科学推理”演进。

### Q6: 总结一下论文的主要内容

OmniScientist提出了一种端到端、全模态、跨学科的AI科学家系统，旨在直接从异构原始证据（如图像、信号、视频、3D结构等）中开展科学研究，解决现有系统仅依赖文本、代码或预计算摘要而丢失关键时空与跨通道关系的问题。方法上，系统通过感知层与三个自主智能体（构思、实验、写作）在确定性流水线中协作，并利用代码强制检查确保新颖性、统计有效性、执行溯源与数值可追溯性。在涵盖5个学科家族、4类证据家族的36个真实数据案例中，系统全部完成从原始数据到成稿论文的流程，平均论文得分6.3；与仅接收预计算标量特征的盲变体相比，全感知版本在全部7个评估维度上提升，并在85%的对比中胜出。该工作表明，全生命周期感知对证据驱动的科学发现至关重要，为构建广泛能力的AI科学家提供了可行路径。
