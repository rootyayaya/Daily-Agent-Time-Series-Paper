---
title: "TSFLab: A Self-Improving Agent-Agnostic Workbench for Time Series Forecasting Research"
authors:
  - "ChengAo Shen"
  - "Yanjun Zhao"
  - "Haoxin Liu"
  - "Bonnie Chen"
  - "Miles Ma"
  - "Dongjin Song"
  - "Hanghang Tong"
  - "Qingsong Wen"
  - "Jingrui He"
  - "Jingchao Ni"
date: "2026-10-29"
arxiv_id: "2610.40901"
arxiv_url: "https://arxiv.org/abs/2610.40901"
pdf_url: "https://arxiv.org/pdf/2610.40901v1"
github_url: "https://github.com/D2I-Group/TSFLab"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "LLM Agent"
  - "时间序列预测"
  - "自动基准测试"
  - "自改进工作台"
  - "工具调用"
  - "代码智能体"
  - "研究自动化"
relevance_score: 7.5
---

# TSFLab: A Self-Improving Agent-Agnostic Workbench for Time Series Forecasting Research

## 原始摘要

As publications and products on time series forecasting (TSF) proliferate, researchers face a growing burden of analyzing existing work. First, not all publications release code. For instance, only about 20% of arXiv TSF papers have a code link in the surveyed period. Second, released code also requires manual maintenance. Thus, TSF researchers must constantly adapt or implement existing works. However, independent implementations can differ in experimental settings and are difficult to maintain. We therefore propose to use AI agents for benchmarking TSF research and even supporting autoresearch, e.g., developing new TSF models. Yet directly applying existing coding agents, such as Claude Code and Codex, is suboptimal: prohibitive costs, limited scalability to large research projects (e.g., benchmarking), and lack of self-maintenance. To address these challenges, we propose TSFLab, a self-improving agent-agnostic "workbench" that equips compatible coding agents with shared resources and tools for low-cost TSF research and continuous maintenance of research resources. Our experiments cover reproduction, benchmarking, and new method development. In reproduction and benchmarking, TSFLab improves task completion by 20-163% and cuts fresh tokens per completed task by 11-66% across baselines. A pilot study of agent-driven method development also shows improved forecasting accuracy via TSFLab, with 32.8-73.6% fewer fresh tokens and 9.2-68.8% less development time than the other settings.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

时间序列预测（TSF）领域论文数量快速增长，但可复现研究资源严重不足：调查期内仅约20%的arXiv TSF论文提供代码链接，且已有代码库维护困难——TSLib在2024年以来新增1200余篇论文的背景下仅从18个方法扩充到41个，并宣布因维护人力不足停止维护。研究者（尤其是新手）不得不手动重实现基线并搭建评测流程，而独立实现之间实验设置不一致，导致结果难以比较、实验重复浪费。AI智能体为自动化基准测试乃至自主研究提供了可能，但直接使用Claude Code、Codex等通用编码智能体存在成本高昂、难以扩展到大规模研究项目、缺乏自我维护能力等问题；现有TSF智能体研究又聚焦于与特定智能体绑定的harness，无法随新智能体出现而自动受益。因此，本文的核心问题是：如何构建一个与智能体无关、可跨智能体与团队复用、并能持续自我维护的TSF研究工作台，以低成本解决知识更新滞后与实验设置不一致两大瓶颈，支撑复现、基准测试和新方法开发等研究任务。

### Q2: 有哪些相关研究？

本文的相关工作可分为四类。方法/资源类：TSLib、BasicTS、TFB、NeuralForecast 提供实现与评测流水线，GIFT-Eval 评测时间序列基础模型；但它们的评测设置与调参预算不透明，方法靠人工维护，覆盖范围滞后于文献，TSFLab 以知识卡片逐层描述模型与数据集，覆盖方法更多。研究智能体类：现有智能体可复现论文、运行机器学习实验与提出新方法，ChemCrow、PantheonOS 分别加入化学与基因组学工具；TimeSeriesScientist、TimeCopilot、MetaCaster 等 TSF 智能体只编排预测器或优化训练，产出预测而非开展研究，且领域支持内嵌于单一智能体的 harness，换智能体需重建；TSFLab 则对任意兼容智能体保持不变。智能体工作台类：ToolUniverse、Scientific Agent Skills、Biomni-E1 将工具与流程移出智能体，但面向通用科学或生物医学，而非声明式评测协议下的 TSF 方法；TSFLab 以 TSF-Domain Guide、Knowledge Structurer、Experiment Workflower 在共享显式协议下执行比较。自改进智能体类：STOP、Darwin Gödel Machine、Voyager 及记忆系统改进单个智能体，而 TSFLab 的 Recursive Improver 改进共享工作台，核验并合并方法、单元、数据集与发现，使每次任务产出同时反哺工作台改进与维护。

### Q3: 论文如何解决这个问题？

TSFLab 的核心思路是构建一个与具体智能体无关的“工作台”，在不修改底层模型与执行框架（harness）的前提下，通过共享资源与工具增强任意兼容的编码智能体，从而降低 TSF 研究成本并实现研究资源的持续自维护。整体框架由四个模块组成。第一，TSF-Domain Guide 提供入口说明与任务级技能，把数据集成、方法实现、评估协议等领域知识转化为可执行步骤、检查项与常见陷阱，例如引导智能体识别时间字段、采样频率与评估设置，并通过统一接口注册数据、检查划分与缩放，避免各自维护加载与切分代码。第二，Knowledge Structurer 以摘要、卡片、源码三级渐进披露组织方法、数据集与单元知识：卡片描述能力边界、参数接口与验证记录，源码提供论文与参考实现，使智能体按需检索而无需重读原始材料；同时把 RevIN、序列分解、注意力变体等通用模块抽取为共享单元，支持复用与集中维护。第三，Experiment Workflower 通过统一 runner 执行智能体声明的实验，方法规格定义参数、构造与输入输出接口，配合 Compose、Override、Sweep 组合预设并展开运行矩阵，训练前校验配置、数据、兼容性与预算，支持断点恢复、状态管理与一致的数据划分、缩放和评估。第四，Recursive Improver 通过可用性、复杂度与一致性三类检查，把验证过的外部资源与智能体产出回灌到工作台，形成共享更新循环。创新点在于智能体无关的增强接口、三级知识披露、共享单元复用以及可自我修复的工作台维护机制。

### Q4: 论文做了哪些实验？

论文围绕复现、基准测试和新方法开发三类研究任务展开实验。实验设置上，以 Codex CLI 搭配 GPT-6 Luna 为主，统一提示、数据、网络访问和预算，并与 Time-Series-Library（TSLib）、TFB 两个代码库以及无工作台（空目录+PyTorch）三种基线对比，同时做模块消融（去掉 TSF-Domain Guide、Knowledge Structurer、Experiment Workflower）和智能体消融（Claude Code+Sonnet 5.5、Codex CLI+GPT-6 Sol）。任务包括：复现四篇无官方代码的近期论文（RhyMix、StateFlow、AdaRDiff、CoRe，每篇三次尝试）；在 ERCOT 和 Openmeteo 两个新数据集上按统一协议评测八种方法（DLinear、PatchTST、iTransformer、TimeAlign、GTR、TimeMosaic、PHAT、EMAformer）；在 ETTh1 和 Weather 上做方法开发试点。主要结果：TSFLab 完成全部 12 次复现和 48 个基准结果中的 42 个，为各设置最高；96 个复现结果中 73% 的 MSE 与论文相对误差在 10% 以内，其他设置仅 21–46%；每个完成任务的新鲜 token 减少 11–66%，任务完成率提升 20–163%；复现代码新增函数少 15–29%、新增圈复杂度低 18–28%。方法开发试点取得最低测试 MSE，新鲜 token 少 32.8–73.6%，开发时间少 9.2–68.8%。消融显示去掉任一模块都会降低完成率，其中去掉领域指南降幅最大（仅 3/12）。

### Q5: 有什么可以进一步探索的点？

论文的局限本身指向了几个可探索方向。其一，TSFLab 目前只覆盖时间序列预测，其资源描述、检查机制与实验接口都绑定 TSF 协议，未来可将其抽象为领域无关的"资源—工具—校验"层，迁移到分类、异常检测乃至因果推断等任务，验证工作台范式的通用性。其二，方法开发实验在有限搜索时间内未产出显著超越现有领先模型的新方法，说明智能体的搜索策略仍偏局部，未来可引入更强的探索机制，如多智能体分工、进化式候选池、基于误差分解的定向改进，以及更长的研究周期与预算调度。其三，自维护能力值得深挖：当前侧重资源复用与低成本，但代码漂移、依赖升级与环境失效的自动修复尚缺系统评估，可构建"研究资源健康度"指标与回归测试闭环。此外，可探索人机协同的中间产物审计、跨论文实验设置对齐，以及将失败案例沉淀为可检索的经验库，从而让工作台在复现之外真正支撑自主科研。

### Q6: 总结一下论文的主要内容

论文针对时间序列预测（TSF）研究中代码缺失、复现与维护成本高的问题，提出TSFLab——一个自改进、与具体智能体无关的“工作台”，为兼容的编码智能体提供共享资源与工具，实现低成本的TSF研究及研究资源的持续维护。方法上，它整合领域指导、结构化知识、可复用单元、执行环境与经验证的资源更新，使智能体能够复用已验证的实现与修复结果。实验覆盖复现、基准测试和新方法开发三类任务：在复现与基准测试中，任务完成率提升20%–163%，每个完成任务的新增token消耗降低11%–66%；在智能体驱动的方法开发试点中，预测精度提升，token消耗减少32.8%–73.6%，开发时间缩短9.2%–68.8%。消融实验表明，领域指导、资源组织与共享执行三者互补。该工作使验证过的改进可跨智能体、跨团队累积复用，为TSF研究提供可持续的自动化基础设施。
