---
title: "DiagChain: A Diagnostic Benchmark for Evaluating LLM Agents on Evidence-Grounded Attack Chain Reconstruction"
authors:
  - "Xuyang Liu"
  - "Yibin Han"
  - "Zhenwei Zhang"
  - "Kai Chang"
  - "Zhiwei Xu"
  - "Tian Qiu"
  - "Weixian Deng"
  - "Jiabao Gao"
  - "Xiaolin Peng"
  - "Hai Wan"
  - "Xibin Zhao"
date: "2026-08-04"
arxiv_id: "2608.03591"
arxiv_url: "https://arxiv.org/abs/2608.03591"
pdf_url: "https://arxiv.org/pdf/2608.03591v1"
categories:
  - "cs.CR"
  - "cs.AI"
tags:
  - "LLM Agent"
  - "Evidence-Grounded Reasoning"
  - "Attack Chain Reconstruction"
  - "Retrieval-Augmented Generation"
  - "Stage-wise Evaluation"
  - "Diagnostic Benchmark"
  - "Evidence Routing"
  - "Cybersecurity"
relevance_score: 7.5
---

# DiagChain: A Diagnostic Benchmark for Evaluating LLM Agents on Evidence-Grounded Attack Chain Reconstruction

## 原始摘要

Large Language Model (LLM) agents offer a promising approach to attack chain reconstruction by retrieving and interpreting heterogeneous telemetry to infer ordered attacker actions. However, existing benchmarks mainly evaluate final outputs or aggregate accuracy, providing limited insight into how errors arise and propagate across intermediate reasoning stages. We present DiagChain, a diagnostic benchmark for evidence-grounded attack chain reconstruction that enables stage-wise evaluation of LLM agents. DiagChain includes MAIN-69, a suite of 69 scenarios spanning multiple operating systems, evidence noise levels, and chain lengths. It further introduces Evidence-Centric Retrieval-Augmented Generation (ECRAG), which couples evidence retrieval with an evolving structured representation of the reconstructed chain. Five complementary metrics are introduced to assess distinct stages of the reconstruction process and support systematic failure diagnosis. Based on evaluations using 6 LLMs, DiagChain reveals that even the strongest configuration succeeds on only 39.6% of the 849 reference steps in MAIN-69. Our analysis further shows that smaller models struggle with the more basic task of incorporating retrieved evidence into their outputs, whereas larger models can proceed to later steps, where correctly ordering that evidence becomes the main bottleneck. These results validate the importance of diagnostic evaluation beyond end-to-end accuracy and provide actionable insights for improving evidence-grounded cybersecurity agents.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

本文聚焦于网络安全领域中LLM智能体进行“证据驱动的攻击链重建”任务，旨在解决现有评测基准无法细粒度诊断智能体中间推理过程错误的问题。研究背景是LLM智能体已能通过检索和解释异构遥测数据来推断有序攻击步骤，但现有基准大多只评估最终输出或整体准确率，无法揭示错误在证据发现、分组、排序、归因等中间阶段如何产生与传播。具体不足体现在三方面：场景覆盖有限（缺乏跨系统、噪声水平与链长多样性）、诊断能力缺失（无法定位失败环节）、工作流评估不完整（未结合动态证据状态）。为此，论文提出DiagChain基准，包含69个多系统场景（MAIN-69），并引入ECRAG机制将证据检索与结构化链表示耦合，同时设计五个互补指标分别评估重建各阶段。核心目标是实现对攻击链重建过程的阶段级诊断，超越端到端准确率，为改进证据型安全智能体提供可操作见解。实验显示最强配置仅完成39.6%参考步骤，且小模型在证据融入上失败，大模型则在证据排序上受限，验证了细粒度诊断的必要性。

### Q2: 有哪些相关研究？

相关研究可分为三类。**方法类**中，SLEUTH通过审计事件溯源重建精简攻击场景，为DiagChain的证据链模型提供直接动机；POIROT、NoDoze、UNICORN等溯源系统分别实现CTI图谱对齐、告警分流和APT检测，但均未面向LLM智能体的分阶段诊断。**评测类**是主要对比对象：CTIBench和AttackSeqBench侧重静态知识或序列推理，缺乏智能体交互；ExCyTIn-Bench通过SQL交互评估调查图路径，但仅部分支持诊断；Cyber Defense Benchmark、SIR-Bench和SIABench引入交互式环境，却未显式建模攻击链输出；AuditBench和HIDBench覆盖多系统与噪声，但未结合RAG或诊断；RAG-SIA和OCR-APT虽支持证据检索与链重建，却未将链长和噪声作为联合分层变量。**应用类**中，ProvSEEK结合智能体与溯源检索，但未提供阶段级指标。DiagChain的独特性在于同时具备智能体、RAG、显式攻击链、多系统覆盖、阶段诊断及链长/噪声双轴分层，并通过ECRAG和五类指标实现错误溯源，弥补了现有工作仅评估最终准确率而忽视中间推理错误传播的不足。

### Q3: 论文如何解决这个问题？

论文通过构建一个分阶段可诊断的基准框架DiagChain来系统解决攻击链重建中错误溯源困难的问题。核心创新在于将评估从单一的端到端准确率分解为五个互补的细粒度指标，从而定位错误发生在检索、分组、排序还是证据引用阶段。

整体框架包含三个层次：首先构建了MAIN-69数据集，从AutoLabel、ExCyTIn-Bench和OTRF APT29三个来源整合23个源单元，每个案例生成干净、噪声和原始三种证据配置文件，覆盖多操作系统和不同链长度。其次设计了证据中心检索增强生成（ECRAG）机制，该机制先通过TF-IDF获取种子文档，再利用证据-实体检索图进行实体扩展和时序扩展（获取同一来源中相邻记录），最后通过融合文本相似度、词元重叠、实体匹配和元数据奖励的排序函数返回证据卡片。

工作流采用循环智能体架构，状态包含已观察卡片、工作链和压缩记忆。模型每轮选择类型化动作（查询证据、执行操作或提交），未受支持的链步骤会触发进一步检索，最终提交时仅保留有证据引用的步骤。五个评估指标分别衡量：检索步骤覆盖率（证据可用性）、分组F1（证据分簇质量）、排序准确率（步骤时序正确性）、证据引用F1（引用精确性）和归因差距率（发现但未使用的证据比例）。这种设计使研究者能区分“未能找到证据”与“未能组织好已找到证据”两类根本性失败，实验证明小模型主要卡在证据整合环节，而大模型则受限于证据排序。

### Q4: 论文做了哪些实验？

实验围绕四个研究问题展开，使用MAIN-69基准（含69个场景，覆盖多操作系统、证据噪声等级和链长），并划分R12与R24子集进行消融和预算敏感性分析。评估了6种LLM（含GPT-5.5、GLM-5.2变体、Qwen-3-32b、Llama4-17b-Scout、DeepSeek-V4-Pro），采用15轮交互上限、检索宽度k=32的固定设置，提出五类指标（检索覆盖、分组F1、排序、接地、归因差距）分阶段诊断。

RQ1显示无模型全面占优：GPT-5.5在检索和排序上最强，GLM-5.2归因差距最小。长链场景中Qwen和Llama的分组F1仅0.18-0.25，而GPT-5.5达0.53-0.81。RQ2首次失败分解表明，小模型（Qwen、Llama）主要失败于“观察到但未使用证据”，大模型则瓶颈后移至“证据排序”。RQ3消融显示完整脚手架（含结构化记忆、反思、支持审计）相比仅检索，排序从0.764升至0.943，归因差距从0.306降至0.054，但检索覆盖略降。RQ4表明增加预算（k>32或轮数>15）主要提升覆盖率和分组，却损害排序稳定性，且token消耗从93K升至130K。最强配置在849个参考步骤上仅成功39.6%，验证了分阶段诊断的必要性。

### Q5: 有什么可以进一步探索的点？

论文的进一步探索可从以下几个方向展开：首先，当前基准仅覆盖69个场景且集中于少数操作系统，未来可扩展至更多样化的系统环境、攻击战术（如MITRE ATT&CK全覆盖）及真实APT案例，提升泛化性。其次，ECRAG的检索与结构化表示耦合仍较简单，可探索更细粒度的证据置信度建模、时序因果推理或图神经网络增强的链式推理，以缓解长链场景下的排序瓶颈。第三，现有指标侧重阶段准确性，可引入错误传播路径分析、不确定性量化或人类专家对比评估，更深入诊断模型失败模式。第四，针对小模型“证据融入”能力不足，可设计专门的微调策略或检索增强训练目标；对大模型的排序问题，可尝试引入显式的时序约束解码或外部规划器。最后，可探索多智能体协作框架，让不同专长模型分别负责证据筛选、排序和验证，以突破单一模型的性能天花板。

### Q6: 总结一下论文的主要内容

DiagChain是一个用于评估LLM智能体在证据驱动的攻击链重建任务中表现的诊断性基准。现有基准主要评估最终输出或聚合准确率，难以揭示错误在中间推理阶段的产生与传播。为此，DiagChain构建了MAIN-69数据集，包含69个覆盖多操作系统、不同证据噪声水平和链长度的场景，并引入证据中心检索增强生成（ECRAG）方法，将证据检索与重建链的结构化表示相结合。同时提出五个互补指标，分别评估重建过程的不同阶段，支持系统性故障诊断。基于6种LLM的评估显示，最强配置也仅在849个参考步骤中成功完成39.6%。分析表明，较小模型难以将检索到的证据整合到输出中，而较大模型则能在后续步骤中正确排序证据，这是主要瓶颈。该工作验证了超越端到端准确率的诊断评估的重要性，为改进证据驱动的网络安全智能体提供了可行见解。
