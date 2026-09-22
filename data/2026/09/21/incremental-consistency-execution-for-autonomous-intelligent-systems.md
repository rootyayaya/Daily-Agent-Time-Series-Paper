---
title: "Incremental Consistency Execution for Autonomous Intelligent Systems"
authors:
  - "Cheng Li"
  - "Jiexiong Liu"
  - "Yixuan Chen"
  - "Ziheng Huang"
date: "2026-09-21"
arxiv_id: "2609.24090"
arxiv_url: "https://arxiv.org/abs/2609.24090"
pdf_url: "https://arxiv.org/pdf/2609.24090v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "工业故障诊断"
  - "增量一致性执行"
  - "任务事实契约"
  - "依赖掩码"
  - "状态扰动不变量"
  - "LLM多工具助手"
  - "可追溯诊断链"
  - "执行优化"
  - "自主智能系统"
relevance_score: 7.5
---

# Incremental Consistency Execution for Autonomous Intelligent Systems

## 原始摘要

Long-horizon autonomous intelligent systems rely on heterogeneous components such as large language models, databases, external APIs, and rule engines, while their external states continuously change during execution. Re-executing the entire workflow after every change introduces substantial redundant computation. This paper proposes an incremental consistency execution method based on task fact contracts, field-level dependency masks, and state perturbation result invariant domains. After an initial verified execution, the system constructs conservative invariant domains for critical inputs and uses them to determine whether downstream results can be safely renewed without re-invoking expensive components. When re-execution is required, only the smallest affected output fields are recomputed, and an equivalence barrier prevents unnecessary downstream propagation. A submission-time version consistency gate further ensures the safety of side-effecting actions. Experiments on industrial fault diagnosis, enterprise analytics, and LLM-based multi-tool assistants show that the proposed method significantly reduces expensive component calls and end-to-end latency while maintaining high consistency and low incorrect-reuse rates.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决长时程自主智能系统在外部状态持续变化时，如何避免全流程重执行所带来的大量冗余计算问题。这类系统通常由大语言模型、数据库、外部API、规则引擎等异构组件编排而成，传感器采样、数据库记录、配置参数、第三方响应等环境状态在执行过程中不断变化，系统必须在不重启整个任务的前提下保持结果与最新环境一致。现有方法存在三方面不足：其一，主流工作流以步骤成功或失败为控制信号，一旦上游输入变化就将所有依赖步骤标记为失效并从头重执行，甚至触发全路径重规划，错误地将“输入已变”等同于“下游结论必错”，忽略了大量扰动并不改变契约级结论的事实；其二，基于内容哈希、时间戳或版本号的缓存方法只能判断输入是否完全一致，任一键值变化即整体失效，且对象级依赖跟踪只能决定是否重新验证，无法回答“输入在多大变化范围内仍保持指定输出字段的契约语义”这一可机器执行的问题；其三，LLM等组件的非确定性使字符串或哈希比较会把语义等价的输出误判为新结果，而模糊相似度又可能在数值、权限或业务约束已变时错误复用旧结果；此外，步骤级依赖表达过度近似了真实影响关系，难以实现真正的最小重算。为此，本文提出基于任务事实契约、字段级依赖掩码和状态扰动结果不变域的增量一致性执行方法，在初次验证执行后为关键输入构造保守不变域，据此判断下游结果能否安全续期，仅在必要时重算最小受影响字段，并通过等价屏障与提交时版本一致性门分别控制传播范围与副作用安全。

### Q2: 有哪些相关研究？

围绕增量计算与缓存复用，相关研究可分为几类。方法类方面，编程语言与数据库领域的增量求值、有限差分、自适应计算，以及数据流系统中的增量数据流和差分数据流，均在记录级追踪依赖并只重算受影响算子；但这些经典框架假设程序纯函数式、变更集可精确识别、输出等价可由结构相等判定，难以应对含概率与学习组件的现代自治系统。缓存类方面，物化视图、ETag/内容哈希、以及近期 LLM 服务中的提示缓存、响应缓存和工具结果缓存，通常以完整输入哈希为键，任一字段变化即整体失效，或依赖用户声明的提示，仍是“全有或全无”。工作流类方面，Airflow、Argo、Temporal 以 DAG 编码步骤依赖并对失败作出反应，反应式与自适应系统加入运行时监控，但缺乏机器可执行的“输入变了输出仍契约等价”概念及保守边界。鲁棒性类方面，敏感性分析、局部解释与不变性验证可给出影响归因或认证区域，却局限于特定模型架构与输出类型，无法处理学习模型、规则引擎与外部服务混合的流水线。溯源类方面，数据溯源、时态数据库、事件溯源与区块链将计算与提交解耦，可审计 AI 强调记录证据，本文的提交时版本一致性门受此启发。与上述工作相比，本文区别在于：将外部观测与中间结果统一表示为带版本、有效性谓词和验证规则的一等任务事实；显式构造状态扰动结果不变域作为保守边界并支持在线收缩扩展；将计算有效性更新与副作用提交解耦，避免域命中静默绕过不可逆动作。

### Q3: 论文如何解决这个问题？

论文提出了一套基于“任务事实契约”的增量一致性执行方法。整体框架以任务事实为最小可版本化单元，每个事实包含唯一标识、字段路径、值或摘要、来源组件、版本、指纹、有效性谓词、验证程序、前驱集合及状态（VALID/RENEWED/INVALID），从而在字段粒度上识别变化而无需复制大体积数据。

核心模块包括三部分。第一，任务事实契约将每个执行步骤绑定为输入/输出规范，其中字段级依赖掩码 M_i 明确标注哪些输入字段会影响哪些输出字段，使同一步骤的不同输出具有差异化失效范围；掩码通过接口声明、动态追踪、单字段扰动和人工预注册四种来源取并集获得。第二，状态扰动结果不变域：对已验证步骤，围绕关键输入构造保守的 Ω̂_i(a,b) 子集，用区间、超矩形、枚举集或谓词表示，并通过约束扰动、边界搜索与保守收缩算法构建，记录组件版本、契约版本与等价性版本，任一版本变化即强制重验证。第三，运行时决策：通过输入字段到（步骤,输出字段）的倒排索引 O(1) 定位消费者，对每个受影响输出依次检查身份条件、前置条件与域成员条件；若全部满足则直接续期输出，否则仅重算最小受影响字段，并由等价屏障阻止不必要的下游传播。提交时还设有版本一致性门，确保副作用动作仅在其前置条件成立时提交。

创新点在于：将 LLM 等非确定性组件的等价性判定建立在结构化输出而非原始字节上；用保守不变域替代全量重执行；以字段级掩码和等价屏障实现最小化重算与传播阻断；并通过持续反例监控与受控扩张维持域的保守性与安全性。

### Q4: 论文做了哪些实验？

论文在三个任务族上评估了所提方法：工业设备故障诊断、企业分析报告和基于LLM的多工具助手。系统实现为Python服务，集成LLM编排器、关系数据库、时序数据库、外部定价API和模型注册表。对比基线为全量重执行和粗粒度缓存。评估指标包括：每次变更避免的昂贵组件调用数、端到端延迟、通过独立验证的续期比例、提交时门控正确阻止副作用动作的比例。

主要结果：所提方法每次变更昂贵调用仅0.18次（全量重执行1.00，粗粒度缓存0.84）；端到端延迟65ms（全量380ms，缓存120ms）；续期验证通过率98.6%（缓存91.4%）；错误传播率0.4%（缓存3.8%）；提交时门控阻止精度100%。在1200个测试提案中，门控正确阻止47个因权限事实变更而本应被静默绕过的支付动作，批准1153个，未观察到静默绕过。工业诊断场景中，电机转速从1490变为1502 rpm时跳过故障分类GPU推理，延迟从380ms降至65ms；企业分析场景每次刷新减少1次LLM调用，延迟降低约4.2秒。

### Q5: 有什么可以进一步探索的点？

论文的局限主要集中在四点：一是保守域构建依赖无副作用的验证执行环境，在真实系统中往往难以获得；二是等价性判据要求每个输出字段都有确定性可执行规则，对自由文本输出不友好；三是高维字段空间下联合域构建成本可能超过收益；四是现场校验假设源系统在变更时可重读，网络分区或离线场景下需延迟续期。

未来可从三方面深入：其一，将等价判据本身交由强化学习智能体从决策结果中学习，替代人工规则，从而适配自然语言等非结构化输出；其二，研究去中心化的分布式续期协调协议，使边缘设备在间歇连接下也能独立决策；其三，将保守不变域与形式化验证结合，为自动化动作给出可认证的安全边界。此外，我认为可探索“自适应粒度”机制：根据历史误复用率动态调整域的保守程度，在安全与开销之间取得更优平衡。

### Q6: 总结一下论文的主要内容

论文针对长时程自主智能系统在环境持续变化时全量重执行导致大量冗余计算的问题，提出基于任务事实契约、字段级依赖掩码与状态扰动结果不变域的增量一致性执行方法。核心思路是：初次验证执行后，为关键输入构建保守不变域，据此判断下游结果能否安全续期而无需重新调用昂贵组件；需重执行时仅重算最小受影响输出字段，并通过等价屏障阻止不必要的下游传播；提交时版本一致性门进一步保障副作用动作安全。论文形式化了任务事实、契约与不变域等运行时对象，设计了字段级依赖索引、保守域构造算法及变更处理流水线。在工业故障诊断、企业分析与LLM多工具助手三类场景中，该方法显著减少昂贵组件调用与端到端延迟，续期验证通过率保持98.6%以上，错误复用率低，且提交门能正确阻断因域命中而被静默跳过的支付类动作。
