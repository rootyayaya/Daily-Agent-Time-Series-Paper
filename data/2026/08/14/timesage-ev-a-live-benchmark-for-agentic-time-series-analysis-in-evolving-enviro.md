---
title: "TimeSage-EV: A Live Benchmark for Agentic Time Series Analysis in Evolving Environments"
authors:
  - "Qingren Yao"
  - "Yaxuan Kong"
  - "Yuqi Nie"
  - "Yichen Li"
  - "Stefan Zohren"
  - "Anna Vettoruzzo"
  - "Qingsong Wen"
  - "Ming Jin"
  - "Joaquin Vanschoren"
date: "2026-08-14"
arxiv_id: "2608.14270"
arxiv_url: "https://arxiv.org/abs/2608.14270"
pdf_url: "https://arxiv.org/pdf/2608.14270v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Time Series QA Benchmark"
  - "Evolving Environments"
  - "Self-Evolving Agent"
  - "Skill Library"
  - "Temporal Validity"
  - "LLM Agent"
  - "Time Series Analysis"
  - "Failure Mode Analysis"
  - "Live Benchmark"
relevance_score: 9.5
---

# TimeSage-EV: A Live Benchmark for Agentic Time Series Analysis in Evolving Environments

## 原始摘要

Time series analysis in high-stakes domains relies on recurring data releases, where new observations can alter the evidence base and the validity of later conclusions. Existing time series QA benchmarks mostly rely on fixed snapshots, leaving temporal validity and cutoff-aware evidence use unevaluated. We introduce TimeSage-EV, a live benchmark for agentic time series analysis in evolving environments. It tracks 60 real institutional scenarios across 6 domains, comprising 1,485 scenario-period QA pairs from Feb 2023 to May 2026 and spanning monthly, weekly, daily, and irregular release cadences. At each period, large language model (LLM) agents receive time series data and source reports, while the withheld target release provides ground truth. TimeSage-EV evaluates state identification, data summarization, and outlook reasoning. Experiments with frontier LLM agents and TimeSage-1.0, a novel self-evolving agent with a reusable analytical skill library, reveal significant performance gaps across model tiers and recurring failures in temporal validity, exogenous context use, and adaptation. We release TimeSage-EV as a research resource with monthly updates, code, a leaderboard, and failure-mode analyses.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在金融、医疗、交通等高风险领域，时间序列分析并非一次性预测，而是随新数据定期发布不断更新的循环工作流。然而，现有研究存在明显不足：一方面，传统时间序列问答基准（如ChatTime-TSQA、Time-MQA）基于固定快照构建问答对，无法评估模型在证据随时间变化时的适应能力；另一方面，通用Agent基准侧重代码、网页导航等能力，未针对周期性时间序列分析设计，缺乏对时间戳感知证据追踪和跨模态信息综合的考察。因此，当前尚无基准能回答“LLM智能体能否在动态证据环境下维持时间有效性并持续更新分析结论”这一核心问题。本文提出TimeSage-EV，旨在填补这一空白，通过构建基于真实机构发布节奏的实时基准，严格设置信息截止点，并设计多维度评估协议，系统检验智能体在演化环境中的状态识别、数据总结和前瞻推理能力，揭示其在时间有效性维护和证据使用上的缺陷。

### Q2: 有哪些相关研究？

相关研究主要分为两条主线。**语言化时间序列分析**方面，LLMTime和Time-LLM将时序数据重构为语言模型可处理的格式；ChatTime、ChatTS、Time-MQA、TSRBench、TimeSeriesExam、TimeSage-MT及TemporalBench通过自然语言问答评估时序推理能力；TimeSeriesGym则评测端到端机器学习任务。这些工作均基于静态快照，问题固定、证据不变，未涉及跨发布周期的分析更新。**长周期实时智能体基准**方面，ReAct、Toolformer、AutoGen等构建了工具调用与记忆机制，WebArena、GAIA、Tau-Bench、SWE-bench覆盖网页导航、对话与软件工程任务；LiveBench和LiveCodeBench通过刷新题库降低污染，ForecastBench在结果揭晓后评估预测。但这些基准仍是“刷新快照”，而非重复发布、证据累积的演化场景。本文的独特定位在于填补两者交叉空白：TimeSage-EV是首个同时支持数值时序证据、文本文档证据、智能体交互、实时更新、场景演化及周期隔离的基准，将时序分析从静态问答拓展为动态长程智能体工作流。

### Q3: 论文如何解决这个问题？

TimeSage-EV通过构建一个“活体基准”来解决演化环境中时间序列分析的时间有效性问题。其核心创新在于将传统静态快照评估转变为跨发布周期的递归任务，每个周期都构成一个时间隔离的评估单元。

整体框架包含三个层次：**环境定义**明确了场景任务（固定问题模板与答案模式）、周期实例（累积时间序列、截止前文档、外部证据）以及智能体状态（可跨周期携带的记忆或分析工件）。**数据流水线**采用六阶段自动化构建：从500个公共机构源中筛选出60个场景，通过属性过滤、源验证、证据收集、问题生成和地面真值提取，最终形成1,485个周期实例，覆盖月/周/日/不规则发布节奏，并经过自动审计与人工复核确保时间隔离性。

**关键技术**在于三方面：一是“截止感知”的证据设计，目标期文档被严格 withheld，仅作为地面真值来源，强制智能体不得使用未来信息；二是双模式评估协议，对结构化答案采用规则评分（关键点准确率），对自由文本报告采用LLM评判（覆盖率、忠实度、质量），其中忠实度专门检测是否引用了截止后证据；三是支持独立评估（每周期重置）与顺序评估（跨周期携带状态）两种模式，以区分单次推理能力与持续适应能力。

该基准的创新点在于：首次将“时间有效性”作为核心评估维度，通过递归发布机制模拟真实决策场景；引入可复用的分析技能库（TimeSage-1.0智能体），使智能体能够跨周期积累分析经验；并提供持续更新的排行榜与失败模式分析，揭示模型在时间推理、外生情境利用和适应性方面的系统性缺陷。

### Q4: 论文做了哪些实验？

论文构建了TimeSage-EV动态基准，包含60个真实机构场景、1485个问答对，覆盖2023年2月至2026年5月，按月度、周度、日度及不规则频率发布。实验采用smolagent框架，评估六种LLM（Sonnet-4.6、GPT-5.4、Kimi-K2.6、Qwen-3.5-397B、Devstral-2-123B、Gemma-4-31B），设置温度0、32768 token输出预算、20步或2700秒限制，使用DeepSeek-V4-Flash作为评判模型。结果显示GPT-5.4综合得分最高（86.0），Qwen-3.5-397B（84.2）和Sonnet-4.6（82.4）次之；简单任务均超92分，但困难任务最佳仅72.7分。按题型分析，状态识别、变化检测和构成题较易（最强模型85-95分），而归因和预测题最难（最佳分别46.7和43.0）。Token成本差异超4倍，GPT-5.4最省（84M）且效率最高。失败模式包括推理失败、时间误用和报告不完整。记忆实验表明Qwen受益于序列评估，而Gemma后期记忆反而成为负担。TimeSage-1.0自进化技能库在中等和困难场景提升性能，降低18% token成本，但技能归纳集中在早期阶段。

### Q5: 有什么可以进一步探索的点？

TimeSage-EV的局限为后续研究提供了清晰方向。首先，当前基准仅覆盖英文公共机构报告，未来可扩展至多语言、多地域数据源，并纳入企业级私有数据或非结构化文档，以检验模型在更广泛场景下的泛化能力。其次，基准排除了图表等视觉信息，而真实分析常依赖多模态输入，因此可探索将图表解析与数值序列联合建模的Agent架构。在评估层面，LLM裁判的噪声问题可通过引入更细粒度的可验证指标或对抗性校验来缓解。此外，实验依赖smolagent框架，未来应解耦模型能力与工具链影响，设计更中立的Agent测试环境。最后，当前静态快照与实时分支的对比设计很好，但可进一步研究Agent如何主动感知数据发布节奏、动态更新其技能库，甚至利用历史失败模式进行元学习，以实现真正的自适应时间序列推理。

### Q6: 总结一下论文的主要内容

TimeSage-EV是一个面向演化环境中智能体时间序列分析的实时基准。现有时间序列QA基准多依赖固定快照，无法评估时间有效性和截止感知的证据使用。该基准追踪6个领域60个真实机构场景，包含2023年2月至2026年5月间1485个场景-周期问答对，覆盖月、周、日及不规则发布节奏。每个周期，LLM智能体接收时间序列数据和源报告，以 withheld 目标发布作为真值，评估状态识别、数据摘要和展望推理三个任务。实验使用前沿LLM智能体和TimeSage-1.0（一种带可复用分析技能库的自演化智能体），揭示了不同模型层级间的显著性能差距，以及在时间有效性、外生情境使用和适应性方面的反复失败。该基准以月度更新、代码、排行榜和失败模式分析的形式发布，为开发能随证据演化可靠更新时间序列分析的稳健分析智能体提供了诊断工具。
