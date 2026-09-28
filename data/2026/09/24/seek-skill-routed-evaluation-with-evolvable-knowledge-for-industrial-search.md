---
title: "SEEK: Skill-Routed Evaluation with Evolvable Knowledge for Industrial Search"
authors:
  - "Zhongxin Huang"
  - "Songyang Li"
  - "Renzhe Zhou"
  - "Feiran Zhu"
  - "Chenglei Dai"
  - "Zhen Xiao"
  - "Xuanping Li"
  - "Jingwei Zhuo"
date: "2026-09-24"
arxiv_id: "2609.29803"
arxiv_url: "https://arxiv.org/abs/2609.29803"
pdf_url: "https://arxiv.org/pdf/2609.29803v1"
categories:
  - "cs.IR"
  - "cs.AI"
tags:
  - "Skill-Routed Evaluation"
  - "Evolvable Knowledge"
  - "LLM-based Evaluation"
  - "Industrial Search"
  - "Failure Mode Attribution"
  - "Skill Bank"
  - "Replay-Gated Update"
  - "Listwise Evaluator"
  - "Diagnostic Signals"
  - "Kuaishou Deployment"
relevance_score: 6.5
---

# SEEK: Skill-Routed Evaluation with Evolvable Knowledge for Industrial Search

## 原始摘要

Search quality evaluation provides essential supervision and diagnostic signals for the development and iteration of industrial search systems. Although large language models (LLMs) offer a scalable alternative to manual assessment, reliable automatic evaluation remains challenging: users experience search results at the page level, while the applicable evaluation criteria are multi-dimensional and continuously evolving. Packing all evaluation criteria into a unified prompt introduces irrelevant context and potential criterion interference, whereas internalizing them through post-training tightly couples rule updates with costly model retraining cycles.
  To address these issues, we propose Skill-routed Evaluation with Evolvable Knowledge (SEEK). Specifically, SEEK externalizes specific search evaluation criteria into a skill bank, dynamically routes relevant skills for each query-result list pair, and employs a task-adapted listwise evaluator to produce page-level judgments and failure mode attribution. A two-stage training pipeline teaches the evaluator to align evaluation criteria with human preferences, while a replay-gated skill bank allows recurring evaluation knowledge gaps to be incorporated without model retraining. Experiments on industrial short-video search show that SEEK improves listwise quality evaluation accuracy and achieves significant progress in attribution diagnosis. SEEK has been deployed at Kuaishou, a short-video platform with over 400 million daily active users, significantly improving the scale and quality of online search evaluation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业搜索系统的迭代高度依赖搜索质量评估提供的监督与诊断信号，但传统人工评估成本高、周期长，难以覆盖快速变化的流量、长尾查询和频繁的系统迭代。大语言模型为规模化自动评估提供了可能，然而直接使用通用LLM仍面临两大挑战：其一，用户是以页面为单位体验搜索结果的，页面质量取决于相关性、排序、内容质量、冗余度、意图覆盖和来源权威性等多维因素，而现有自动评估方法多聚焦于单条目相关性或排序，难以联合预测页面级质量及其退化原因；其二，评估知识丰富且持续演化，将所有规则、边界案例和证据要求塞入单一提示会引入大量无关上下文并造成标准间干扰，而通过SFT或RL将知识内化到模型参数中，又会使规则更新与昂贵的重训练周期紧密耦合，难以在知识快速更新与模型稳定之间取得平衡。因此，本文提出SEEK框架，核心目标是解耦显式评估知识与模型能力，通过技能路由为每个查询-结果列表动态选取相关评估技能，实现页面级质量判断与失败归因，并借助可演化技能库在不重训练模型的前提下持续纳入新出现的评估知识。

### Q2: 有哪些相关研究？

现有相关研究大致可分为三类。方法类方面，LLM-as-a-Judge 被广泛用于相关性、有用性等搜索质量评估，近期工作进一步面向工业目标，如有用性监督、细粒度意图满足和 web 级相关性评估，显著降低标注成本；但多数方法依赖预定义准则或通过后训练将知识内化到模型参数中，难以在不重训评估器的情况下快速纳入新准则。评测类方面，传统 IR 评估将条目级相关性聚合成 Precision、MAP、nDCG 等指标，虽有效但未显式建模结果间交互；RAG 评估、列表级重排与整页评估开始联合建模检索列表，但工业搜索还需细粒度归因诊断，尤其短视频搜索中体验依赖异构信号、位置与结果交互。知识解耦类方面，近期研究将人类判断准则、策略、先例等外化为显式知识接口或可复用技能，并支持从执行反馈中持续修正、在固定模型参数下优化外部技能、通过交互经验更新技能库。与上述工作不同，SEEK 将评估准则外化为技能库并动态路由，配合任务适配的列表级评估器与 replay-gated 技能库，在评估器相对稳定下实现评估知识的受控演化，兼顾局部更新、可靠性与向后兼容，并已在快手部署验证。

### Q3: 论文如何解决这个问题？

SEEK的核心思路是将“评估能力”与“评估知识”解耦，通过外置可演化的技能库来解决工业搜索评估中标准多维且持续演化的问题。整体框架包含三个组件：技能库、技能路由器和列表级评估器。

技能库存储12个诊断技能，覆盖相关性、质量、多样性、权威性和异构性五个维度。每个技能由两部分组成：路由描述（何时激活）和操作指南（如何应用），从而实现路由与执行的表示分离。技能路由器对每个查询-结果列表对估计各技能的激活分数，通过阈值筛选出紧凑的相关技能集合，避免将所有标准塞入统一提示造成上下文干扰。列表级评估器接收原始查询-列表对和选中技能的操作指南，联合推理整个排序列表，输出页面级质量标签和结构化归因，而非独立评估单个结果。

训练采用两阶段流程：先用教师模型将人工标注转化为技能路由标签和证据支撑的评估轨迹，路由器以多标签分类的二元交叉熵独立训练；评估器先进行监督微调，再用DAPO强化学习对齐人类偏好，奖励函数包含任务正确性、技能诊断质量和冲突惩罚。技能库演化则通过回放门控机制实现：当同一知识缺口在多个样本中反复出现时，仅修订操作指南而保持路由语义和模型参数不变，候选修订需在新模式上提升且在历史回放集上不退化才被接受。这样，显式知识可快速更新，而路由和执行能力的更新则通过较慢的周期性模型训练完成。

### Q4: 论文做了哪些实验？

论文围绕SEEK开展了四组实验。实验数据来自快手搜索日志，构建了169,434个查询-结果列表训练对和17,000个独立测试对，每条样本含页面级{good, fair, bad}标签及Relevance、Quality、Diversity、Authority、Heterogeneous五个归因维度标注。对比方法分三类：开源LLM（Qwen3-8B、DeepSeek-R1-Distill-Qwen-7B、Gemma-3-12B-IT）、API LLM（Qwen3-235B-A22B、MiniMax-M2.5、Gemini 3.1 Pro、GPT-5.6 Sol）以及同骨干的任务后训练模型（SFT+DPO、SFT+GRPO）。主要结果：SEEK在三分类Macro-F1达0.6555、准确率0.6618，优于SFT+GRPO的0.6418/0.6527；二分类Macro-F1为0.7374、准确率0.7520；五个归因维度中四项最优，Authority和Heterogeneous提升最大。消融实验表明动态技能路由与评估器后训练互补，DAPO优化和层级奖励（R_task+R_skill+C_conflict）效果最佳；动态路由仅需3.4个技能即达0.752准确率，接近Oracle的0.768。持续适应实验中，Skill-only Evolution三轮后Binary F1从0.7814升至0.7957，Attribution F1从0.7458升至0.7594。SEEK已部署于快手，服务超4亿日活用户。

### Q5: 有什么可以进一步探索的点？

SEEK 的主要局限在于技能路由仍与 Oracle 存在差距，说明技能选择机制尚未充分利用实例语义；技能库的演化依赖人工审核反馈，闭环自动化程度有限；评估器仍绑定 Qwen3-8B 规模，未验证跨模型泛化性。未来可从三方面探索：一是引入可学习的技能检索器或对比式路由训练，缩小与 Oracle 的差距并支持技能组合推理；二是构建自动化的技能挖掘与冲突检测机制，从线上日志中主动发现新失效模式，减少人工介入；三是将技能库扩展为跨任务、跨语言的共享知识层，验证其在多模态搜索、推荐等场景的迁移能力。此外，可探索技能与模型参数的协同演化，避免技能库膨胀带来的路由噪声，并研究评估结果的可解释性如何反哺排序策略优化。

### Q6: 总结一下论文的主要内容

SEEK 针对工业搜索质量评估中页面级判断与多维准则持续演化的难题，提出技能路由评估框架。问题定义上，给定查询与排序结果列表，需联合输出页面级质量标签（good/fair/bad）及五维结构化归因。方法上，SEEK 将评估准则外化为可演化的技能库，用轻量路由器为每个查询-列表对动态选择相关技能，再由任务适配的列表式评估器生成页面级判断与归因；训练采用教师蒸馏路由监督与证据化轨迹，结合SFT与DAPO分层奖励对齐人类偏好；技能库通过错误归因与回放门控实现免重训的局部演化。实验表明，SEEK在页面级评估与细粒度归因上优于开源、API及同骨干后训练基线，并已部署于快手，显著提升在线搜索评估的规模与质量。
