---
title: "Enabling Privacy-Preserving Natural Language Access to Industrial Smart Meter Data"
authors:
  - "Carlos Martín-Abellán"
  - "Mark Kröll"
date: "2026-11-06"
arxiv_id: "2611.09372"
arxiv_url: "https://arxiv.org/abs/2611.09372"
pdf_url: "https://arxiv.org/pdf/2611.09372v1"
categories:
  - "cs.AI"
  - "cs.CL"
  - "cs.DB"
  - "cs.MA"
tags:
  - "多智能体系统"
  - "自然语言查询"
  - "智能电表数据"
  - "隐私保护"
  - "本地LLM"
  - "工业时序分析"
  - "异常检测"
  - "SQL生成"
  - "可解释报告"
  - "能源管理"
relevance_score: 7.5
---

# Enabling Privacy-Preserving Natural Language Access to Industrial Smart Meter Data

## 原始摘要

Energy management officers and grid operators increasingly rely on smart meter data for anomaly detection, performance monitoring, and strategic decision-making. However, extracting actionable insights from large-scale, heterogeneous telemetry databases requires advanced SQL and data engineering expertise, creating a critical bottleneck for non-technical personnel. Furthermore, the strict data privacy regulations and security constraints inherent to critical energy infrastructure often prohibit the routing of sensitive consumer data through cloud-based Large Language Models (LLMs). To address these challenges, we present OpenMeter, a schema-agnostic Multi-Agent System (MAS) designed to translate natural language queries into executable code and human-readable insights. This architecture lowers the technical barrier for day-to-day utility operations by empowering non-expert personnel to interact with complex databases through intuitive natural language dialogue, transforming raw telemetry into a highly valuable tool for routine grid workflows and strategic decisions. Multi-scenario ablation studies over this environment demonstrate that full multi-agent orchestration shows its largest observed accuracy gains on resource-constrained local hardware (+6.1 pp EX-R over the strongest single-agent configuration); at frontier scale, individual components retain value but should be enabled selectively, indicating that the cost of full orchestration is justified specifically where privacy demands local execution.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于工业智能电表数据分析中的“数据可及性”瓶颈。研究背景是：高级计量基础设施大规模部署后，智能电表以10–15分钟间隔持续产生涵盖有功电能、电压、无功功率和电能质量等指标的海量时序数据，但这些数据对能源管理官等非技术运维人员几乎不可用。作者与工业合作方共同识别出四类高频分析任务——上报频率核查、数据可用性审计、结构质量评估和异常检测——均需数据库工程支持才能完成，形成明显的运营瓶颈。现有方法存在两方面不足：一是传统方式要求用户掌握SQL和数据工程技能，非专家难以直接从异构遥测数据库中提取洞见；二是消费者用电数据高度敏感，可被用于推断居住模式、作息乃至身份（再识别准确率可达99%），严格的隐私法规与关键能源基础设施的安全约束禁止将数据经云端LLM API处理，而现有系统尚未整合LLM驱动的多智能体编排、Text-to-SQL、本地开源权重模型执行与领域可解释性。因此，本文的核心问题是：如何在数据不出本地的前提下，构建一个模式无关的多智能体系统，将自然语言查询翻译为可执行代码并生成人类可读的洞见，从而让非专家人员以对话方式安全访问复杂电表数据库，并进一步厘清多智能体编排在资源受限本地硬件与前沿规模模型下各自的收益边界。

### Q2: 有哪些相关研究？

本文的相关研究可分为四类。方法类：Ali等提出分层多智能体系统用于分布式能源管理，但仅作后端控制器、无自然语言接口；Xiao和Xu将LLM多智能体用于建筑能源审计，采用Planner-Researcher-Advisor三角色；He等将“编排者-程序员-审查者”模式形式化于软件工程；Gao等证明以CREATE TABLE语句表示模式对Text-to-SQL最有效；Ojuri等将智能体与LLM结合以降低数据库访问门槛。应用类：Gamage等的多智能体RAG系统面向净零管理，但依赖云端且无Text-to-SQL能力；Intelli-Dispatch-SQL是最接近的工作，用单一LLM智能体完成意图识别、SQL生成与校验，但基于合成数据、架构单体且缺乏可解释性指标。评测类：Spider 2.0显示最佳解析器仅5.7% EX、智能体方法21.3%；BIRD表明需引入模式外领域知识；Nascimento等在IndDB上发现多数提示策略低于30% EX，模式链接错误占53.3%。安全与可解释类：Dong等警示云端LLM的网络安全与隐私风险，Madani等指出隐私是主要技术挑战且多数用例停留概念阶段；现有可解释性多为事后XAI。与上述工作不同，OpenMeter在真实工业智能电表数据上结合MAS编排与Text-to-SQL，加入确定性模式校验与自纠错循环、基于领域规则的本地化解释，并首次给出单智能体与多智能体的受控消融对比。

### Q3: 论文如何解决这个问题？

论文提出的 OpenMeter 是一个模式无关的多智能体系统（MAS），核心目标是在隐私受限的工业能源环境中，将自然语言查询转化为可执行代码与可读洞察。整体框架采用“先规划后执行”的 O→CA→O→IA 顺序流水线，由三个智能体协同完成。

架构上包含三个主要组件：编排智能体（O）作为中央协调器，负责意图分类（13 类分析类别）、难度评估、生成结构化执行计划，并从领域知识库中筛选与当前查询相关的术语和规则；编码智能体（CA）负责 Text-to-SQL 与 Python 可视化代码生成，接收结构化模式上下文（列名、类型、基数统计、枚举值域、样本行），在只读沙箱中执行 DuckDB 查询，并具备对 O 完全透明的自主纠错循环——执行出错时将列级诊断信息追加到上下文进行定向修正；解释智能体（IA）作为最终综合层，结合原始查询、原始输出和结果感知的领域上下文，生成事实摘要、异常刻画（区分统计异常与逻辑异常并引用 KB 规则）以及不确定性感知的语言表达。

三个关键创新点：一是隐私即架构，全部 LLM 推理运行于本地开源权重模型，遥测数据、查询与结果不出受控环境；二是智能体分离，编码与解释结构解耦，缓解推理-行动不匹配的失败模式；三是 LLM 即策展人，由 O 在单次推理中动态过滤知识库，无需嵌入模型或向量数据库等外部 RAG 基础设施，同时避免注意力退化并优化上下文窗口利用。

### Q4: 论文做了哪些实验？

论文在工业智能电表部署环境上开展实验，采用2×2因子设计对比单智能体（S-Base、S+SC）与多智能体（M-Base、M+SC、M+KB、M+Full）共6种配置，覆盖本地9B（RTX A5000）与云端397B-A17B MoE两个硬件层级，模型为Qwen3.5系列，每个场景独立运行5次并舍弃预热轮。数据集来自工业伙伴真实部署的三张测量表（EMSify、LP3、LPR），约750万行，含EAV与Wide两种模式，保留通信中断、计数器重置等真实伪影；金标准为62对人工校验NL→SQL（49对留作评测），覆盖13类分析任务与3个难度级别。评价指标包括EX-S/P/R、EM、CM、ESR、VER、SER，以及解释质量（Grd/Rel/Coh）与可视化质量（Align/Pres）的1–5分Likert评分，另测自纠正ROI、端到端延迟与token效率。主要结果：本地层级M+Full取得最高EX-R 42.4%，较最强单智能体S+SC（36.3%）提升6.1个百分点；M+SC的ESR（77.6%）与VER（56.6%）最高；自纠正带来+15.1至+20.0个百分点ESR提升。前沿层级M+KB的EX-S最高（38.0%），但EX-R最高为S-Base（54.7%），ESR接近饱和（≥94.7%），重试收益有限（ΔESR≤1.6个百分点）。人工评审对语义等价SQL的接受率显著高于LLM评审（如S+SC本地由5.0%升至30.0%），说明自动评测低估了实际可用性。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有以下几点：其一，评测规模偏小，仅49条查询、EM普遍低于16%，且LLM判官与人类评估存在系统性偏差（人类接受率可达70–100%），未来可构建更大规模、多行业schema的基准，并引入更可靠的过程级与结果级混合评估。其二，多智能体编排在本地小模型上收益明显（+6.1pp EX-R），但在前沿模型上反而拖累结构与执行指标，说明编排策略应自适应：可按查询复杂度、ESR置信度动态启用子智能体，而非全量编排。其三，KB注入存在可执行性与语义准确性的权衡，可探索检索式、按需注入及冲突消解机制。其四，当前仅覆盖SQL生成与可视化，未来可扩展到多轮澄清、时序异常解释、根因诊断等智能体工作流，并结合本地隐私约束下的模型蒸馏与工具调用优化。

### Q6: 总结一下论文的主要内容

论文针对智能电表数据分析中的双重瓶颈：一方面，能源管理人员的领域专长与SQL/数据工程技能之间存在鸿沟，难以从大规模异构遥测数据库中提取可操作洞察；另一方面，用能数据高度敏感（用户重识别准确率可达99%），受数据主权法规约束，无法将查询路由至云端LLM。为此，作者提出OpenMeter——一个模式无关的多智能体系统，将自然语言查询翻译为可执行代码并生成可读解释。系统遵循隐私即架构、智能体分离、LLM作为知识策展人三项设计原则，采用“先规划后执行”的O→CA→O→IA流水线，由编排器完成意图分类与知识筛选，编码智能体生成DuckDB SQL并自纠错，解释智能体输出有据可依的结论。作者还构建了62条经三步验证的能源领域Text-to-SQL评测集，并开展加性消融实验。结果表明：在资源受限的本地9B模型上，完整多智能体编排相对最强单智能体配置提升EX-R达6.1个百分点；而在前沿规模模型上，各组件仍有价值但应按需启用，说明全编排的成本仅在隐私要求本地执行时才合理。
