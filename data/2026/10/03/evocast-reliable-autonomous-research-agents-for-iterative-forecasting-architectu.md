---
title: "EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution"
authors:
  - "Kaipeng Xu"
  - "Xianli Yan"
  - "Yan Wang"
  - "Xiang Liu"
  - "Shan Liu"
date: "2026-10-03"
arxiv_id: "2610.04517"
arxiv_url: "https://arxiv.org/abs/2610.04517"
pdf_url: "https://arxiv.org/pdf/2610.04517v1"
github_url: "https://github.com/18e0-x/EvoCast"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Autonomous Research Agent"
  - "Time Series Forecasting"
  - "Architecture Evolution"
  - "LLM Agent"
  - "Mechanism Ablation"
  - "Evidence-Grounded Reasoning"
  - "Cognition-Authority Separation"
  - "Iterative Optimization"
  - "AutoML"
  - "Agentic Time Series"
relevance_score: 7.5
---

# EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution

## 原始摘要

Deep time-series forecasting models have rapidly diversified, yet adapting them to a specific task still requires extensive expert effort in model selection, mechanism diagnosis, architecture design, implementation, and evaluation. Existing AutoML methods are constrained by predefined search spaces, while general-purpose LLM research agents lack reliable control over experimental protocols and model promotion. We introduce EvoCast, a fully autonomous research-agent system for iterative forecasting architecture evolution. EvoCast first establishes and diagnoses a task-specific baseline through executed mechanism ablations, then generates evidence-grounded research directions from dataset characteristics, diagnostic results, prior rounds, and failure records. Its central design, cognition-authority separation, assigns open-ended hypothesis generation and code implementation to LLM agents, while deterministic program authorities control source-edit boundaries, canonical evaluation, and promotion decisions. Experimental outcomes are accumulated as evidence to guide subsequent rounds. Results show that EvoCast completes complex architecture modifications with higher implementation success and lower agent-side token/time cost, and develops task-specific architectures that outperform selected baselines, strong forecasting models, and agent baselines in three real-world forecasting cases. The code is available at https://github.com/18e0-x/EvoCast.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

深度时间序列预测模型近年来快速多样化，涵盖分解建模、频域建模、patch 分词、变量中心建模等多种范式，形成异构且快速演进的模型生态。然而真实预测任务在周期性、分布漂移、变量交互、预测长度和噪声特性上差异巨大，单一通用架构难以在所有场景中占优。因此，为特定任务开发合适架构仍需大量专家投入，包括基线选择、机制诊断、架构设计、代码实现与受控评估。现有 AutoML 方法受限于预定义搜索空间，难以进行跨文件信息流重构和任务特定机制插入；通用 LLM 研究智能体虽具备开放生成能力，却缺乏对实验协议和模型晋升的可靠控制，容易导致失败解释、评估假设与晋升决策相互污染，浪费 token 与时间预算。本文提出 EvoCast，旨在解决如何在固定评估协议下实现可靠自主的预测架构迭代演化这一核心问题。其关键设计是认知-权限分离：LLM 智能体负责开放式假设生成与代码实现，确定性程序权威控制源码编辑边界、规范评估、指标比较与模型晋升，从而在保持研究灵活性的同时确保实验可比性与可审计性。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类。方法类方面，AutoML、超参数优化和神经架构搜索在预设模板或算子空间内自动化模型选择与配置，但受限于预定义搜索空间；近期LLM辅助方法通过多智能体架构设计、有界任务搜索和运行时修复扩展了该过程。应用类方面，语言模型被用于预测、时间推理和多模态建模，TimeSeriesScientist自动化数据理解、规划、验证与报告，SEA-TS和GenAutoML通过迭代反馈生成预测代码或任务特定架构。评测与自主研究智能体方面，MLAgentBench提供标准化实验环境，AIDE通过代码空间搜索探索候选，R&D-Agent协调研发角色，AutoResearch通过执行反馈验证候选，MLE-STAR利用执行消融定位高影响代码区域，ResearchLoop、AIRA²、FML-bench、ResearchGym和Arbor则强调任务契约、一致评估、执行基础设施与跨轮证据管理。与上述工作不同，EvoCast从可执行仓库基线出发，通过实时路径机制诊断与跨轮证据引导有界源码修改，并以确定性程序控制边界验证、规范评估、模型晋升和证据回写，实现认知与权限分离，将研究方向生成与实验裁决统一在同一固定协议下。

### Q3: 论文如何解决这个问题？

EvoCast 将任务特定的预测架构开发组织为一个固定协议的自主研究闭环，核心创新在于“认知-权限分离”设计。整体框架包含五个阶段：任务锚定、基线建立、基线诊断、正式迭代研究和最终报告。

在任务锚定阶段，系统读取数据集、目标、回看窗口、预测步长、预测模式和评估指标，将其冻结为任务协议 P，并提取数据集特征作为后续规划的证据。基线建立阶段在协议 P 下执行所有可运行基线模型，选择指标最优者作为唯一正式比较锚点，确保整个运行过程中数据划分、指标、训练策略和评估路径完全一致。基线诊断阶段分析最优基线的活跃预测路径，提取可消融机制，并在同一协议下执行消融，记录 Δ(a)=m(a;P)−m(b*;P)，从而判断哪些机制应保留、哪些存在冗余或任务不匹配、哪些实现风险需规避。

正式迭代研究是最大的闭环区域。每轮中，研究规划器 Π 读取冻结协议 P 和当前研究状态 S_r，综合任务证据、当前模型活跃源码路径、诊断消融结果、已接受结果、有效负例、不稳定增益以及失败记录，生成一个研究方向 d_r，指定目标机制、源码插入点、可检验假设、预期信息流变化、需避免的失败和预期知识增益。随后构建器 β 将 d_r 编译为有界实现任务，仅允许在模型侧源码区域内插入新模块、重路由信息流或局部重构，而数据路径、评估器、指标计算、训练预算和提升逻辑保持冻结。执行器 Γ 进行源码边界验证、规范训练与评估、指标比较和提升裁决，仅当候选通过边界验证、产生有效规范指标并满足固定多种子比较规则时，才将其提升为当前最优模型。状态更新 U 记录模型状态、机制证据和工程记忆，有效负例调整机制判断，不稳定增益指示证据强度，工程失败识别实现风险。预算耗尽后，报告叙事智能体仅读取冻结事实生成最终 HTML 报告。

### Q4: 论文做了哪些实验？

论文围绕三个研究问题展开实验。RQ1为实现可靠性，构建了包含10个预测骨干、30个任务的想法到代码基准，分局部修改、跨模块集成、新模块插入三个复杂度级别，对比Direct Independent Edit、mini-SWE-agent、AIDE、R&D-Agent和AutoResearch。EvoCast成功率达96.7%（29/30），保真度100%，修复率95.7%，平均Token 27,618、成本0.0137美元、耗时153秒，均优于或接近最优基线。RQ2在Air Quality（MM）、Melbourne Pedestrian T33（SS）、Steel Industry（MS）三个真实任务上，与Sundial、Toto-2.0-2.5B、Time-VLM、TimeCMA及AIDE、R&D-Agent等对比。EvoCast在三任务上MSE最低，相对所选基线分别降低2.04%、12.10%、8.67%，MAE分别降低1.90%、6.97%、9.24%，且有效轮次比例最高（100%、90%、90%），Token与成本低于R&D-Agent。RQ3通过移除五个组件的消融实验验证设计必要性，完整系统最终MSE为0.162579，优于各消融变体。

### Q5: 有什么可以进一步探索的点？

EvoCast在三个真实案例上验证了认知-权限分离机制的有效性，但仍存在可拓展空间。首先，其评估依赖单一任务指标，缺乏对架构鲁棒性、泛化性与不确定性的多目标考量，未来可引入多目标进化或帕累托前沿搜索。其次，系统仅在单机单任务上迭代，未探索跨任务知识迁移与经验复用，可构建共享证据库以加速新场景冷启动。第三，LLM生成的假设空间仍受提示与先验知识限制，可结合检索增强或程序合成扩展搜索边界。此外，当前权限控制为确定性规则，未来可引入可学习的安全边界，在保证可审计性的同时提升探索效率。最后，论文未涉及计算预算与碳排放约束，绿色AutoML视角下的资源感知调度值得进一步研究。

### Q6: 总结一下论文的主要内容

EvoCast面向特定任务的时间序列预测架构开发，将其形式化为固定协议下的自主研究闭环：先建立并诊断任务专属基线，再基于数据特征、机制消融证据、历史轮次与失败记忆生成研究方向，随后在受限源码边界内实现候选架构，经统一评测与晋升规则裁决后更新证据状态。其核心设计是“认知—权限分离”：LLM智能体负责开放式假设生成与代码实现，确定性程序权威控制源码有效性、规范评测、模型晋升与状态更新，从而避免评测假设与晋升决策污染后续轮次。实验表明，EvoCast在仓库级实现任务中成功率更高、修复能力更强且token与时间成本更低；在空气质量、墨尔本行人流量和钢铁工业三个真实预测案例中，均优于所选基线、强预测模型及智能体基线，并形成任务自适应架构。该工作推动了自主时间序列建模向可执行、可审计、场景自适应的研究范式发展。
