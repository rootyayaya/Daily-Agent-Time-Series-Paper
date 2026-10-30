---
title: "Testimony from Timelines: Evidence-Grounded Significance Testing of Temporal Clinical Hypotheses"
authors:
  - "Chengyang He"
  - "Wenlong Zhang"
  - "Koduvayur Subbalakshmi"
  - "Ping Wang"
date: "2026-10-29"
arxiv_id: "2610.40619"
arxiv_url: "https://arxiv.org/abs/2610.40619"
pdf_url: "https://arxiv.org/pdf/2610.40619v1"
categories:
  - "cs.CL"
  - "cs.IR"
tags:
  - "时序假设检验"
  - "证据检索"
  - "可解释性"
  - "临床时间线"
  - "LLM验证"
  - "基准测试"
  - "决策可追溯"
  - "工具调用"
relevance_score: 7.5
---

# Testimony from Timelines: Evidence-Grounded Significance Testing of Temporal Clinical Hypotheses

## 原始摘要

Ask a language model whether sales tend to dip after a product recall, or whether one side effect tends to follow another after a vaccine, and it answers in a fluent sentence that reads like a finding, with no test behind it. Assertions about how events unfold across many cases fill the Web, and each is a temporal hypothesis that only a significance test over the right records can settle. The verifier must specify the null, select the test and decide which records bear on the hypothesis, and any of these choices can go wrong while the conclusion still comes out right. Yet benchmarks for language-model data analysis grade only the conclusion, with the relevant data handed over. We study the problem in health, where a wrong verdict is costly, and present STRATA, a benchmark that grades every decision on the way to a verdict: 8,735 hypotheses over the clinical timelines of vaccine adverse-event reports, with gold plans, evidence sets, p-values and verdicts derived under a released codebook and reproduced by a deterministic oracle. We also propose ART (articulate, retrieve, test), a staged paradigm that exposes each decision as an inspectable output. Extensive experiments with five model configurations show that systems fail mostly at choosing which records count, a verdict-evidence gap that accuracy alone conceals. ART closes most of this gap and brings a 31B open model to within 0.01 of the frontier models under the same paradigm; the frontier models succeed once given the codebook.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是“时间假设验证”问题：给定一个关于某群体临床时间线中事件顺序或时序的假设（如接种某疫苗后疼痛通常先于乏力出现），系统需要陈述零假设、选择显著性检验、判定哪些记录能作为证据，并给出支持、反驳或证据不足的结论。研究背景是，网络上大量此类时序断言由语言模型生成和传播，语气笃定却缺乏统计检验支撑；在医疗等高风险领域，错误结论代价很高。现有基准的不足在于：它们只评判最终结论，且往往把相关数据直接交给模型，从不检查使结论具备统计意义的中间决策——零假设设定、检验选择、证据集筛选等。这些决策中任何一步出错，结论仍可能碰巧正确，形成“结论—证据鸿沟”，而现有基准对此毫无约束。因此，本文的核心问题是：如何构建一个对验证过程中每一步决策都提供金标准标注的基准，并设计一种让每个决策都成为可检查输出的分阶段验证范式，从而暴露并缩小仅看准确率所掩盖的结论—证据鸿沟。为此作者提出STRATA基准（8,735条基于疫苗不良事件临床时间线的假设，含计划、证据集、p值和结论的金标准）以及ART三阶段范式（articulate、retrieve、test）。

### Q2: 有哪些相关研究？

相关研究可分为三类。方法类：StatQA考察统计检验的选择，StatFormBench考察检验族的表述，StatABench对固定工具函数下分析运行的最终答案打分；P-Bench与Fisher-R1最接近本文，代理在给定原假设、相关数据CSV和术语表后编写R代码计算p值，并按决策与p值评分；LATCH在EHR数据上通过确定性R流水线执行LLM选定的分析，VERITAS是带确定性证据分类器的多代理协同科学家。应用类：DiscoveryBench与BLADE按评分细则评估开放式发现代理；临床时序方面，TIMER与CRAFT用语言模型抽取并精炼临床时间线，EHRSQL、EHRAgent及OmniSQL面向临床数据库问答。评测类：时间推理基准多针对单一文本、事件图或时间序列，时序事实核查针对单条陈述及其检索证据。区别在于：上述工作的数据要么作为相关子集直接给出，要么完全交由代理选择，假设只涉及表格变量，且仅对最终答案或评分细则打分；本文的STRATA对原假设、检验选择、检验运行、证据记录集与裁决逐阶段提供金标准，并首次要求系统判定统计量在哪些记录上计算，ART则将每项决策暴露为可检查输出。

### Q3: 论文如何解决这个问题？

论文提出STRATA基准与ART（articulate, retrieve, test）分阶段范式来解决“语言模型给出时间假设结论却无统计检验支撑”的问题。核心思路是把一次不可审计的模型判断拆解为三个可检查、可打分的决策：先表述、再取证、最后检验，使最终结论成为统计决策而非模型主观判断。

整体框架分三阶段。S1“表述”：模型依据代码本（codebook）将假设文本组合成计划π，明确事件、数量、分母原语（如ordered_pair、all_present_unique_first）、臂、零假设类型与p0或参考人群、尾别、检验族及下限；提示中刻意隐去“措辞→假设类型”的映射，迫使模型真正组合计划而非查表，并由harness通过字段反查推导假设类型。S2“检索”：模型针对每个臂写一条SQL，在时间线数据库（两表三视图）上为每份报告返回“入分母/入分子/排除”三个布尔标记及可选单元格标签；harness在只读沙箱中执行并聚合为每臂的(n,k)与标识符集合，使证据可与金标准集合逐条审计。S3“检验”：确定性函数按计划执行二项检验（对照p0，数据驱动零假设取检索分母上的平均机会）、两臂Fisher检验（共享报告互换）或argmax假设的命名单元格对最强竞争者检验，并施加下限，返回双尾p值与裁决。

关键创新有三：一是“契约”（contract）机制，harness把计划解析为假设类型后，只向S2注入该原语对应的条件规则与臂计划，避免模型面对整本代码本；二是两处有界的“验证—修复”循环，PlanChecks与RowChecks仅依据契约、代码本和数据（绝不看金标准）标出违规并重问，最多两次；三是全程可检查输出——计划、证据集、p值与裁决分别可对金标准打分，从而暴露出“结论对但证据错”的裁决—证据鸿沟。消融显示去掉验证修复、去掉harness检验（改用模型裁决）或把计划降为散文，性能均显著下降，证明各组件缺一不可。

### Q4: 论文做了哪些实验？

论文在STRATA基准上开展了三类实验。实验设置：测试集为1,500条Original语域假设，覆盖8,735条疫苗不良事件临床时间线；模型配置包括Qwen2.5-32B双模型、qwen3.8-27B、gemma4-31B及前沿模型Claude Opus 5.5和GPT-5.6，开源模型以4-bit运行于单张RTX A5000，前沿模型经API调用，共约355 GPU小时和246美元API费用。对比方法包括EHRSQL、EHRSQL-C、EHRAgent、DiscoveryBench参考智能体，以及分阶段基线（普通提示、CoT、OmniSQL-32B、StatQA）和消融（无contract、verify-and-repair）。主要结果：ART在所有开源模型上端到端最优，较EHRSQL-C分别提升0.23、0.13、0.12（p<0.001）；gemma4在ART下达0.981，与前沿模型差距在0.01内；前沿模型获得codebook后准确率达0.98–1.00。分阶段看，S1 Articulate准确率0.915–0.992，S2 Retrieve为0.833–1.000，S3 Test均为1.000；开源模型主要失误在证据集选择，如Qwen2.5对first/last族证据错误率0.78。证据指标上ART的Trace分数为0.635–0.967，显著高于基线。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三。其一，基准仅覆盖疫苗不良事件这一单一临床场景，假设形态也限于少数几类，未来可扩展到电子病历、药物警戒之外的时序数据（如工业传感、金融事件流），检验跨领域迁移下计划与证据选择是否仍成立。其二，ART 的规划、检索、检验三阶段仍以文本代码本为契约，对弱模型依赖较强，且验证-修复循环对前沿模型反而有损，可探索自适应触发修复、引入可学习的计划校验器（如检查否定与尾方向一致性）来消除 qwen3.8 在 negated position 上的方向性错误。其三，当前只评估结论与证据，未评估 p 值校准与多重比较控制，未来可加入统计功效分析与不确定性度量；同时探索让模型自生成可复现的检验代码并由确定性 oracle 审计，以缩小 verdict-evidence gap。

### Q6: 总结一下论文的主要内容

论文针对语言模型对时间性临床假设（如疫苗不良事件先后顺序）给出流畅结论却缺乏统计检验的问题，提出时间假设验证任务：系统需明确零假设、选择检验方法、确定相关记录并给出支持、反驳或证据不足的判定。为此构建STRATA基准，基于疫苗不良事件临床时间线生成8,735条假设，每条均配有金标准计划、证据集、p值与判定，并由确定性预言机复现。同时提出ART分阶段范式，将假设表述为计划、按契约检索证据、确定性执行检验，使每步决策可检查。实验表明系统主要失误在证据记录选择，准确率掩盖了判定与证据间的鸿沟；ART显著缩小该差距，使31B开源模型接近前沿模型水平，前沿模型在获得规则手册后即可成功。
