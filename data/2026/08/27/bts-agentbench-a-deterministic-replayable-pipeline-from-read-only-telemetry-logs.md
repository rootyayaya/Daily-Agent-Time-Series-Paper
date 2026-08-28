---
title: "BTS-AgentBench: A Deterministic, Replayable Pipeline from Read-Only Telemetry Logs to Agent Benchmarks"
authors:
  - "Jeong-Yoon Kim"
date: "2026-08-27"
arxiv_id: "2608.27334"
arxiv_url: "https://arxiv.org/abs/2608.27334"
pdf_url: "https://arxiv.org/pdf/2608.27334v1"
github_url: "https://github.com/kjy7567/BTS-AgentBench"
categories:
  - "cs.CL"
  - "cs.SE"
tags:
  - "Agentic Time Series"
  - "Telemetry Logs"
  - "Time Series Report"
  - "Benchmark Construction"
  - "Evidence Attribution"
  - "Read-Only Tool Store"
  - "Multi-Turn Episodes"
  - "Industrial Diagnostics"
  - "LLM Agent Evaluation"
  - "Replayable Pipeline"
relevance_score: 7.5
---

# BTS-AgentBench: A Deterministic, Replayable Pipeline from Read-Only Telemetry Logs to Agent Benchmarks

## 原始摘要

Industrial sites contain large volumes of read-only telemetry, but few benchmarks specify how to compile these records into executable multi-turn agent tasks. We present a telemetry-to-episode construction method instantiated as BTS-AgentBench. The pipeline normalizes BTS metadata and raw histories into a read-only tool store, compiles static tasks with tool-derived gold answers and evidence, and lifts retained tasks into typed, bounded operator-facing episodes. The 532-row release adds clarification, goal revision, timestamp policy, quality-gated reporting, and evidence attribution while preserving the source computation and split. Coded contract preflight reports zero findings, and the construction-exclusion controller completes 0/532 rows. Two independent raw-to-episode builds match all 11 logical tool-store exports and reproduce the released 356/87/89 train/dev/test artifact exactly. Applying the shared construction path to XAI4HEAT produces 204 episodes; on its 41-row held-out test split, the controller completes 0 rows and the retained GPT-5.5 execution completes all 41. Code, artifacts, and replay reports are available at https://github.com/kjy7567/BTS-AgentBench.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业设施中积累了海量只读遥测数据，但现有基准测试缺乏将这些原始记录系统转化为可执行多轮智能体任务的标准方法。手动构建场地级数据成本极高——仅BTS数据集就产生约219万天窗口候选和599万成对候选，无法规模化推广。同时，通用智能体数据缺乏设施特有的命名、关系和观测信息，无法支撑实际运维场景。

本文提出BTS-AgentBench，一个确定性的遥测到任务构建流水线。其核心贡献在于：从标准化元数据和原始历史中自动生成只读工具库、静态可执行任务及带证据的黄金答案，并将任务提升为包含澄清、目标修订、时间戳策略、质量门控报告和证据归因的多轮操作员交互。该流水线具备完全可重放性，相同输入必然生成相同基准产物，并通过编码契约预检和构建排除控制器确保数据质量。最终发布532行基准，覆盖九类任务族，并在XAI4HEAT上验证了跨语料库的可移植性。

### Q2: 有哪些相关研究？

相关研究可归为四类。**交互式工具使用基准**方面，API-Bank提供可运行的工具对话，ToolSandbox引入状态与隐式依赖，τ-bench结合模拟用户与策略评分，ACEBench细粒度评估多轮错误；本文区别于这些从零构建任务的方法，直接从现有遥测语料编译可执行任务与片段。**运维与工业智能体基准**中，ITBench和AssetOpsBench评估结构化运维流程，ReAct Meets Industrial IoT探索工业遥测的语言智能体访问；本文补充了将只读遥测编译为有界、确定性评估片段的环节。**遥测数据与元数据构建**上，BTS提供标准化建筑时序数据，Brick定义传感器与设备关系；本文基于此基质派生可执行的遥测分析任务。**可执行工件基准构建**方面，SUPER评估研究仓库的可执行完成度；本文则从遥测与元数据出发，编译静态任务并转换智能体接口，用确定性控制器作为构建审计工具，识别并修复脆弱行。整体上，本文的创新在于提出了从遥测日志到多轮智能体基准的确定性、可重放流水线，并强调可复现性与质量门控。

### Q3: 论文如何解决这个问题？

该论文提出了一条从只读遥测日志到可执行多轮智能体基准的确定性、可重放流水线，核心方法分为三个层次：静态任务构建、智能体回合编译和控制器感知验收。

在静态任务层，论文先将BTS元数据与原始流归档预处理，规范化站点、设备等文本，构建点清单并扫描时间戳覆盖，仅将能匹配原始历史的元数据点提升为工具就绪点。随后物化一个基于DuckDB的只读工具存储，包含流索引、质量统计、聚合和日历画像。家族构建器应用固定资格谓词生成九类任务，通过多样性上限面板和预定义分割规则保留532行，每行记录查询、规范调用、可接受替代、结构化金标、证据和验证器。

在回合编译层，编译器将静态任务转换为有界操作员回合，核心创新是分离源计算、交互契约和表面实现。它定义了一个有限交互语法，组合澄清、状态携带、修订、时间戳策略、质量承诺和证据等类型化义务，而不改变底层计算。确定性渲染器将类型化字段词法化为操作员回合，用户模拟器是有限状态过程，仅在智能体提出匹配澄清问题时释放缺失信息。契约表示为C=(Q,Φ,A,E,V)，每个阶段φᵢ=(fᵢ,gᵢ,Rᵢ)包含类型、结构化金标和评分字段。确定性契约变换按固定顺序执行，每个阶段先运行类型化谓词，再执行只读操作并原子更新所有相关字段，确保源保留、执行接地和话语对齐。

最后，控制器感知验收使用无学习的分支控制器审计状态携带、时间戳策略、聚合、质量决策等，只有控制器无法完成的行才被发布，最终0/532行被控制器完成，验证了构建排除声明的有效性。

### Q4: 论文做了哪些实验？

论文构建了BTS-AgentBench基准，包含532行任务（train/dev/test=356/87/89），覆盖9个任务族（如点消歧、日均值查询、窗口均值、时间戳查询、质量门控等）。实验首先验证了发布工件的可执行合约，所有532行通过契约预检，且构造排除控制器无法解决任何任务（0/532）。随后在89行测试集上评估了三个前沿LLM智能体：GPT-5.5、Gemini 3.1 Pro和Claude Opus 4.7，使用确定性用户模拟器、只读工具和固定评分器。

主要结果：GPT-5.5整体成功率最高（79/89，88.8%），Gemini 3.1 Pro次之（71/89，79.8%），Claude Opus 4.7最低（58/89，65.2%）。直接查找和聚合类任务表现较好（多数达90-100%），而交互敏感型任务（成对比较、排序、点消歧）成功率较低。诊断分解显示，GPT-5.5的Final分数0.978、Evidence 0.955、Phase 0.949、Task 0.965，协议完成86/89行；Gemini和Claude在协议完成上均为81/89。此外，将同一构造路径应用于XAI4HEAT语料库，生成204个episodes（132/31/41），在41行测试集上GPT-5.5全部完成，验证了管线的可移植性。

### Q5: 有什么可以进一步探索的点？

论文的局限性为后续研究提供了清晰方向。首先，当前仅覆盖只读遥测的搜索、聚合等基础操作，未来可探索写侧控制、安全关键执行与长时程故障排查任务，但需设计安全的模拟环境与回滚机制。其次，确定性用户回合虽利于评估，却牺牲了对话多样性，可引入大语言模型驱动的用户模拟器生成更自然的澄清、纠偏与多轮追问，同时保持可复现性。第三，缺少领域专家系统审计，建议构建专家反馈循环，将人工标注的交互质量纳入基准迭代。此外，XAI4HEAT的迁移表明跨语料泛化可行，但事件或状态转换类日志需新工具与任务族，可研究元任务模板自动适配不同遥测结构。最后，当前评分聚焦最终动作，可开发过程级评估指标，细粒度追踪状态携带、策略合规与证据归因的中间失败模式，并探索将控制器审计扩展为对抗性生成，以暴露更隐蔽的构造缺陷。

### Q6: 总结一下论文的主要内容

BTS-AgentBench提出了一种从只读遥测日志构建多轮智能体基准的确定性流水线。该方法将建筑遥测元数据和原始历史记录标准化为只读工具存储，编译出带工具生成答案和证据的静态任务，并进一步转化为类型化、有界操作员交互场景。发布的基准包含532行数据，新增了澄清、目标修正、时间戳策略、质量门控报告和证据归因功能，同时保留源计算和划分。通过编码契约预检和构建排除控制器验证，流水线实现了零缺陷，且两次独立构建完全复现了356/89/87的训练/开发/测试划分。将该方法应用于XAI4HEAT生成了204个场景，在41行测试集上控制器完成0行，GPT-5.5执行全部完成。该工作将工业日志语料视为可复用基底，实现了从原始日志到静态任务再到智能体场景的确定性编译，为工业故障诊断智能体基准构建提供了可复现的标准化路径。
