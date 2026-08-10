---
title: "LLMRouter: Unified Infrastructure for Developing, Evaluating, and Deploying LLM Routers"
authors:
  - "Tao Feng"
  - "Fangxu Yu"
  - "Haozhen Zhang"
  - "Zhongjie Dai"
  - "Liangqi Yuan"
  - "Zijie Lei"
  - "Weizhi Zhang"
  - "Kunlun Zhu"
  - "Haodong Yue"
  - "Keyang Xuan"
  - "Ge Liu"
  - "Jiaxuan You"
date: "2026-08-07"
arxiv_id: "2608.06867"
arxiv_url: "https://arxiv.org/abs/2608.06867"
pdf_url: "https://arxiv.org/pdf/2608.06867v1"
categories:
  - "cs.CL"
tags:
  - "LLM Router"
  - "Model Routing"
  - "Time-Series Routing"
  - "Unified Infrastructure"
  - "Benchmark"
  - "Sequential Decision Process"
  - "Cost-Effective Deployment"
  - "Personalized Routing"
relevance_score: 7.5
---

# LLMRouter: Unified Infrastructure for Developing, Evaluating, and Deploying LLM Routers

## 原始摘要

No single large language model (LLM) is optimal across all queries and budget constraints, making model routing essential for cost-effective deployment. Existing routers adopt diverse formulations and implementations, making fair comparison and extension difficult. We present a unified formulation of LLM routing as a sequential decision process characterized by five components: context encoders, model encoders, scoring functions, decision rules, and learning signals, covering single-turn, multi-turn, and personalized routing. Based on this formulation, we develop an automated pipeline for constructing routing supervision and evaluating routers jointly on response quality and inference cost. The resulting benchmark, xRouteBench, spans generic LLM, memory-augmented, vision, time-series, and personalized routing tasks. We further introduce LLMRouter, an open-source modular infrastructure with more than 16 representative routers. Our empirical study shows that learned routers outperform the strongest fixed-model baseline by 14.6% relatively, lightweight routers become more competitive under tight cost constraints, and user-conditioned routing consistently improves personalization.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着大语言模型生态的快速扩张，不同模型在成本和能力上差异显著，没有任何单一模型能在所有查询和预算约束下表现最优，因此模型路由成为经济高效部署的关键。然而，现有路由研究面临两大障碍：其一，各类路由器采用不同的形式化定义、独立代码库、不兼容接口、不同监督信号和候选池，导致难以公平比较和隔离真正影响性能的设计要素；其二，路由评估比单模型评估复杂得多，需要为每个查询运行所有候选模型并逐条评分，而现有基准仅覆盖单轮路由，缺乏多轮和个性化路由的标准化成本感知评估框架，且无法为新基准或候选池自动生成监督数据。本文提出LLMRouter统一基础设施，将路由形式化为包含上下文编码器、模型编码器、评分函数、决策规则和学习信号五个组件的序列决策过程，覆盖单轮、多轮和个性化路由三类方法。同时构建自动化流水线生成路由监督并联合评估响应质量与推理成本，产出跨通用、记忆增强、视觉、时间序列和个性化任务的xRouteBench基准，旨在解决路由方法难以比较、复用和从离线研究迁移到实际部署的核心问题。

### Q2: 有哪些相关研究？

在LLM路由领域，相关研究可大致分为三类。**方法类**包括：二元路由器（在强弱模型间仲裁）、成本感知级联、奖励引导集成、对比与图路由、个性化路由（适配用户偏好）以及强化学习训练的智能体路由。本文的贡献在于提出统一形式化框架，将上述方法抽象为上下文编码器、模型编码器、评分函数、决策规则和学习信号五个组件，从而兼容并统一了这些分散的方法。**评测类**方面，现有基准如RouteLLM等虽预计算了固定模型池的响应，但局限于单轮路由且缺乏生成监督的自动化流程。本文构建的xRouteBench则覆盖通用、记忆增强、视觉、时间序列及个性化任务，并统一了质量与成本评估协议。**应用类**上，已有工作多聚焦于特定场景（如级联用于降本），而本文的LLMRouter基础设施支持多轮、个性化路由，并提供OpenAI兼容服务器与可视化界面，便于实际部署。与现有工作相比，本文的核心区别在于：一是通过统一抽象消除了不同实现在接口、监督和候选池上的差异，使公平对比成为可能；二是自动化了监督构建与评估流程，显著降低了新基准和候选池的扩展成本；三是实证研究系统比较了三大路由家族，揭示了无单一主导路由、学习路由优于固定基线、多轮未必优于单轮、个性化需良好用户建模等关键发现。

### Q3: 论文如何解决这个问题？

论文通过提出统一的LLM路由形式化框架和开源模块化基础设施来解决模型路由中存在的碎片化问题。核心创新在于将看似多样的路由方法（二元路由、级联、图路由、智能体路由等）统一为序贯决策过程，由五个关键组件刻画：上下文编码器、模型编码器、评分函数、决策规则和学习信号。

整体框架包含两大模块：**xRouteBench基准**和**LLMRouter基础设施**。xRouteBench采用三阶段自动化流水线：查询策展（从源基准采样并统一schema）、响应收集（将查询分发给候选池并记录token数）、指标评分与定价（生成稠密的查询-模型性能/成本矩阵）。该矩阵同时作为路由监督信号和测试平台，使新任务或候选池只需修改配置文件即可接入。

LLMRouter实现了16种以上代表性路由器，覆盖单轮、多轮（含智能体）和个性化三类路由家族。技术关键点包括：上下文编码器支持嵌入式和文本式两种形态，模型编码器涵盖静态元数据、历史画像和可学习嵌入，决策规则支持贪心、成本感知阈值和终止动作，学习信号则包含无参数、监督、偏好和强化学习四种范式。

主要创新体现在：一是统一了路由器的数学表达，使公平比较和扩展成为可能；二是自动化了路由监督构建和评估流程；三是实证表明学习型路由器相对最强固定模型基线有14.6%的相对提升，轻量路由器在严格成本约束下更具竞争力，用户条件路由持续改善个性化效果。

### Q4: 论文做了哪些实验？

实验基于xRouteBench基准，涵盖通用LLM、记忆增强、视觉、时间序列和个性化五大任务轨道，共8个测试集。候选模型池包含18个开源模型（7B至671B参数），通过Together API和NVIDIA NIM API提供，如Gemma-2-9B、Mistral-7B、Qwen2.5-7B、Llama-3-70B、DeepSeek-V3.1等。实现了超过16种路由器，分为三类：单轮路由器（如kNNRouter、SVMRouter、MLPRouter、EloRouter、RouterDC、AutoMix、GraphRouter等）、多轮路由器（Router-R1及kNN/LLM变体）和个性化路由器（GMTRouter、PersonalizedRouter）。评估协议采用加权奖励α·perf - β·cost，从质量优先(α=1.0, β=0.0)到成本优先(α=0.2, β=0.8)共5种权重设置。个性化任务使用DeepSeek-V3.1作为裁判，按胜负平计分。主要结果显示：学习型路由器相对最强固定模型基线提升14.6%；在严格成本约束下轻量路由器更具竞争力；用户条件路由持续改善个性化效果。记忆轨道检索最多5个记忆项作为上下文，使用token级F1评分。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是路由决策依赖固定的候选模型池，难以动态扩展新模型；二是当前评估聚焦于单次查询的独立路由，对多轮对话中的长期成本-质量权衡建模不足；三是时间序列等非文本任务的路由特征提取仍较浅层，未充分利用时序结构信息。

未来可从以下方向探索：1）设计自适应候选池更新机制，结合模型性能漂移检测实现动态路由；2）引入强化学习优化多轮累积奖励，而非单步决策；3）针对时间序列任务开发专用上下文编码器，如利用频域特征或分段符号化表示；4）探索元学习框架，使路由器能快速适应新任务或新模型组合；5）研究路由决策的可解释性，为用户提供模型选择理由，增强部署可信度。此外，将路由与模型微调联合优化，可能实现“路由即训练”的闭环范式。

### Q6: 总结一下论文的主要内容

本文提出LLMRouter，一个用于开发、评估和部署LLM路由策略的统一基础设施。核心贡献在于将路由问题形式化为由上下文编码器、模型编码器、评分函数、决策规则和学习信号五部分组成的序列决策过程，涵盖单轮、多轮和个性化路由三类方法。基于此，作者构建了自动化监督生成与评估流水线，并推出跨通用LLM、记忆增强、视觉、时间序列及个性化任务的基准xRouteBench，集成超过16种代表性路由器。实验发现：学习型路由相比最强固定模型基线相对提升14.6%；在严格成本约束下轻量路由器更具竞争力；多轮路由未必优于单轮；用户条件路由能稳定提升个性化效果，但依赖对用户上下文的准确建模。该工作为路由方法提供了统一比较框架，降低了新方法开发与部署成本，推动该领域系统化研究。
