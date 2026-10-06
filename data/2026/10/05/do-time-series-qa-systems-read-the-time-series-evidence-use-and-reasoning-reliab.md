---
title: "Do Time-Series QA Systems Read the Time Series? Evidence Use and Reasoning Reliability"
authors:
  - "Zhuomin Chen"
  - "Jingchao Ni"
  - "Xu Zheng"
  - "Janki Bhimani"
  - "Mo Sha"
  - "Wei Cheng"
  - "Dongsheng Luo"
date: "2026-10-05"
arxiv_id: "2610.05686"
arxiv_url: "https://arxiv.org/abs/2610.05686"
pdf_url: "https://arxiv.org/pdf/2610.05686v1"
categories:
  - "cs.AI"
tags:
  - "Time-Series QA"
  - "LLM Evaluation"
  - "Evidence Use"
  - "Reasoning Reliability"
  - "Rationale Audit"
  - "Intervention Benchmark"
  - "Time-Series Understanding"
  - "Numerical Grounding"
  - "Agentic Time Series"
relevance_score: 7.5
---

# Do Time-Series QA Systems Read the Time Series? Evidence Use and Reasoning Reliability

## 原始摘要

In recent years, time-series question answering (QA) systems have made significant progress. However, generating a correct answer does not show whether retaining the supplied numerical series improves task performance, nor whether the prediction is sensitive to changes in that input. While some systems provide rationales, answer accuracy also does not show whether their numerical claims are grounded in the supplied series or whether the stated inference is valid. In this work, we focus on evaluating four time-series QA systems: TimeOmni-1, ChatTS, TimeOmni-VL, and Time-MQA. First, for three systems with released evaluation data, we reproduce their reported results and compare the performance of the systems with their backbones. Then, we introduce a benchmark named COMMON-TSQA, which collects public evaluation datasets from existing time-series benchmarks and unifies their sample representation, task definitions, and answer schemas, while evaluating each system through its own interface under common evaluation criteria. The evaluation uses the original condition and six interventions while keeping the question and target fixed. Our analysis shows that aggregate performance alone can obscure how systems use numerical evidence. Similar task-level scores can arise despite substantial changes in individual predictions. Some interventions induce simple fallback behavior rather than preserved task ability. We also evaluate rationales for factual grounding, inference validity, and consistency with the final answer. We find that rationales often contain time-series claims unsupported by the input. Moreover, the rationale audit shows that agreement between a rationale and its final answer can coexist with incorrect numerical descriptions or invalid intermediate inferences.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

近年来，时间序列问答系统通过扩展大语言模型，在预测、模式识别、因果诊断等任务上取得了显著进展，并声称相较其语言模型骨干有大幅提升。然而，现有评估主要依赖最终答案准确率，这无法揭示系统是否真正利用了输入数值序列，也无法判断预测是否对数值证据的变化敏感。即使系统提供了自然语言推理理由，答案正确也不代表其中的数值陈述有输入序列支撑，或推理过程本身有效。已有工作分别质疑了强时间序列性能是否反映对数值输入的有意义使用，以及生成解释的正确性，但缺乏统一、系统的评估。本文要解决的核心问题是：当同一问题的数值证据被改变时，预测如何响应，这种响应是否与修改后的证据相匹配；对于暴露推理理由的系统，其数值事实是否由输入序列支撑，结论是否能从所述前提中有效推出。为此，作者构建了统一基准 COMMON-TSQA，在原始条件和六种干预下评估四个时间序列问答系统，并审计推理理由的事实依据、推理有效性与答案一致性。

### Q2: 有哪些相关研究？

相关研究主要分为三类。方法类方面，ChatTS 采用专用时间序列编码器并与语言模型对齐，ChatTime 将时间序列视为“外语”统一建模数值与文本，Time-MQA 构建覆盖预测、插补、异常检测等任务的大规模多任务语料，TimeOmni-1 结合监督微调与强化学习支持场景理解、因果发现和决策，PATRA 引入模式感知对齐与任务平衡奖励，ARTIST 通过控制器—推理器架构实现推理与自适应时间片段选择，TimeOmni-VL 则以视觉为中心在时间序列与图像间映射。本文与这些工作不同，不提出新系统，而是对 TimeOmni-1、ChatTS、TimeOmni-VL 和 Time-MQA 四个系统进行统一评测。证据依赖与行为评测类方面，已有工作通过消融语言模型组件、构造必须依赖文本的预测任务、研究多模态预测中文本作用，以及在选择题中移除序列输入，质疑强性能是否真正依赖全部输入。本文延续这一思路，通过六种干预检验系统对数值序列的敏感性。忠实性与可靠性类方面，ERASER、FaithCoT-Bench、RFEval 等评估解释是否反映真实推理，TSQueryBench 关注时间序列解释的数值正确性。本文进一步审计理由的事实依据、推理有效性与答案一致性，发现理由常含无输入支撑的数值断言。

### Q3: 论文如何解决这个问题？

论文的核心解决思路是构建一个统一的评测基准 COMMON-TSQA，并通过“输入干预 + 理由审计”来检验时间序列 QA 系统是否真正使用了数值序列证据。整体框架分为三部分：基准构建、干预评测和理由审计。

首先，COMMON-TSQA 不新建任务语料，而是从 GIFT-Eval、SciTS、TIME、TSAQB、CaTS-Bench、FactoryBench 等十个公开基准中收集评测集，统一样本表示、任务定义和答案模式，同时保留源任务语义与目标。每个样本包含时间序列、问题、选项、目标、来源划分及任务/领域元数据，并确保与所评系统的训练数据不重叠。四个系统 TimeOmni-1、ChatTS、TimeOmni-VL 和 Time-MQA 均通过各自原生接口接收相同规范样本，仅输入渲染格式不同。

其次，评测在原始条件下引入六种只修改数值证据、固定问题与目标的干预：Shuffle 打乱序列内数值顺序；Flat 用均值替换；Noise 用同均值方差高斯噪声替换；Swap 换成其他样本的兼容序列；Answer-only 完全移除序列；Zero 将数值置零。通过比较原始与干预条件下的预测变化，可判断系统是否依赖真实时序结构，还是仅凭问题或简单回退作答。

最后，论文对系统给出的理由进行事实依据、推理有效性和答案一致性审计，检查数值陈述是否被输入支持、中间推断是否合法。创新点在于：将“答案正确”与“证据使用”解耦，用统一基准和干预实验揭示聚合分数掩盖的预测不稳定与回退行为，并系统审计理由中的无依据数值声明，从而更可靠地评估时间序列 QA 系统。

### Q4: 论文做了哪些实验？

论文围绕四个时间序列QA系统（TimeOmni-1、ChatTS、TimeOmni-VL、Time-MQA）开展了三类实验。首先，对三个已公开评测数据的系统进行复现，并与各自匹配的骨干模型（Qwen2.5-7B、Qwen2.5-14B、BAGEL-7B）对比，复现结果与报告值接近（ChatTS六项指标差异≤4.0%，TimeOmni-1八项中六项差异≤3.3%），且专门化系统在原生任务上普遍优于骨干模型。其次，构建统一基准COMMON-TSQA，涵盖预测、异常检测、模式识别、跨序列比较、因果诊断、决策干预六类任务，在原始条件及六种干预（Shuffle、Flat、Noise、Swap、Answer-only、Zero）下评测。结果显示原始条件并非总是最优：Flat取得最低预测MASE（TimeOmni-1为1.321），异常检测中Answer-only导致单类回退（准确率约45.61%），模式识别中相似总体准确率下样本级预测变化显著（如TimeOmni-VL改变率47.95%）。最后，用GPT-5.6 Sol审计TimeOmni-1与TimeOmni-VL的推理依据，发现仅约49.4%和50.1%的数值断言有输入支撑，推理有效性通过率分别为27.3%和34.3%，而结论一致性却高达64.0%和92.2%，说明结论一致并不保证推理可靠。

### Q5: 有什么可以进一步探索的点？

论文的核心局限在于：现有时间序列QA系统的训练目标偏重任务级答案正确性，而中间推理的数值接地性与逻辑有效性未被充分约束。TimeOmni-1的CoT监督虽提升最终答案，却无法保证rationale中的数值陈述可靠；ChatTS任务覆盖广，但在已见任务族内仍出现证据响应错误；Time-MQA的LoRA适配在模式识别上提升了输出有效性却降低了配对准确率，说明适配收益并不均匀。

未来可从三方面探索：其一，将中间数值验证纳入训练信号，例如对rationale中的每个数值声明做可执行校验，构建过程级奖励而非仅结果奖励；其二，设计证据敏感性正则化，使模型在输入序列被干预时产生一致且可解释的预测变化，而非退化为fallback策略；其三，建立细粒度的推理审计基准，区分“结论一致”与“推导有效”，并覆盖跨序列、因果诊断等不同任务族，检验适配方法在有效性与正确性之间的权衡机制。

### Q6: 总结一下论文的主要内容

本论文聚焦时间序列问答（QA）系统的可靠性评估，指出仅凭答案准确率无法判断系统是否真正利用了输入数值序列，也无法验证其推理过程的有效性。作者首先复现了TimeOmni-1、ChatTS、TimeOmni-VL和Time-MQA四个系统的报告结果，并与各自骨干模型对比。随后提出统一基准COMMON-TSQA，整合现有公开评测数据，统一样本表示、任务定义与答案模式，并通过各系统原生接口在相同标准下评测。评估采用原始条件加六种干预，保持问题与目标不变。分析发现：总体性能会掩盖系统对数值证据的实际使用方式，相似任务分数下个体预测可能大幅变动；部分干预仅引发简单回退行为而非保留任务能力；理由常包含输入不支持的数值断言，且理由与最终答案一致时仍可能存在错误数值描述或无效中间推理。结论强调预测性能、证据响应行为与理由可靠性应分开评估。
