---
title: "Reason Wide, Not Deep: Amortizing the Reasoning Premium into Distilled Skills"
authors:
  - "Agamdeep Singh"
  - "Srishti Gautam"
  - "Priyanshu Gupta"
  - "Nikita Mehrotra"
  - "Tanmay Bakshi"
  - "Sumit Gulwani"
date: "2026-08-08"
arxiv_id: "2608.07885"
arxiv_url: "https://arxiv.org/abs/2608.07885"
pdf_url: "https://arxiv.org/pdf/2608.07885v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "Skill Distillation"
  - "LLM Agent"
  - "Reasoning Amortization"
  - "Tool Use"
  - "Self-Evolving Skills"
  - "Trajectory Analysis"
  - "System Prompt Injection"
relevance_score: 7.5
---

# Reason Wide, Not Deep: Amortizing the Reasoning Premium into Distilled Skills

## 原始摘要

Reasoning modes of language models outperform their non-reasoning counterparts on multi-step agentic tasks, but pay a 3-6x premium in output tokens on every episode -- much of it spent re-deriving procedures that are shared across episodes of the same domain. We show this recurring cost can be amortized: a coding agent analyses a small corpus of existing trajectories from a training split and compiles a compact natural-language skill that is injected into the non-reasoning model's system prompt. Across four agentic benchmarks (ALFWorld, tau$^2$-bench telecom and retail, and SpreadsheetBench-Verified), skills recover 55%-100%+ of the reasoning gap for GPT-5.4-mini on held-out tasks -- exceeding the reasoning mode outright on two of four -- while emitting 2.7-6x fewer output tokens and zero reasoning tokens. Notably, reasoning traces are not a prerequisite: skills distilled from non-reasoning trajectories alone remain competitive with skills distilled from paired reasoning/non-reasoning corpora, with domain-dependent differences between the two sources. We interpret these results through a search lens: test-time reasoning is deep search inside a single episode, re-paid at every deployment, while corpus distillation is wide search across episodes, paid once. The two recover overlapping procedural knowledge, and width over cheap trajectories is often the better buy -- with the residual gap on some domains (telecom, SpreadsheetBench) delineating where genuinely per-instance deep search remains necessary.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文针对的是推理模式（reasoning mode）在大模型智能体任务中带来的高额推理开销问题。研究背景是，虽然推理模式（如思维链）能显著提升多步智能体任务的性能，但其输出token数是普通模式的3-6倍，且每次任务执行都会重新生成这些推理过程，造成持续的算力浪费。现有方法的不足在于，这种“深度搜索”式的逐实例推理没有利用跨任务共享的程序性知识——同一领域内大量推理是在重复推导领域共通的规则（如工具调用顺序、命令语义），而非解决实例特有难题。

本文要解决的核心问题是：能否将这种逐次支付的推理开销转化为一次性的离线成本？具体而言，通过从少量历史轨迹中蒸馏出紧凑的自然语言技能（skill），注入非推理模型的系统提示中，从而在不牺牲性能的前提下大幅减少推理token。作者提出的被动技能蒸馏方法，用编码智能体分析轨迹语料并编译规则，实验证明可恢复55%-100%的推理性能差距，同时减少2.7-6倍输出token。这本质上是将“宽搜索”（跨轨迹的语料蒸馏）替代“深搜索”（单实例的推理），验证了程序性知识可通过廉价轨迹预先获取。

### Q2: 有哪些相关研究？

相关研究主要围绕三个方向展开。**测试时推理与成本控制**方面，CoT提示和RL训练推理模式通过增加token换取准确性，但存在“过度思考”问题，已有工作通过精简草稿或token预算在单次episode内压缩推理；本文则跨episode摊销推理成本，并发现RL推理可能只是激活了基座模型已有知识，与本文用提示词唤起相同程序性知识的结果一致。**提示优化**方面，OPRO、DSPy/MIPROv2、TextGrad和GEPA等方法通过大量评分rollout搜索提示空间，本文虽目标互补但成本更低——仅由强编码agent对现有语料做一次反思性处理，无优化循环，并在实验中与GEPA直接对比。**智能体经验学习**方面，Voyager在线构建代码技能库，Reflexion将口头自我批评用于同任务重试，ExpeL和Agent Workflow Memory从经验中提取洞察或工作流；本文共享“一次提取、永久复用”的前提，但差异化在于将技能视为昂贵推理模式的替代品，以恢复“思考/不思考”差距的token效率为评估标准，且技能由外部编码agent而非行动模型自身生成。

### Q3: 论文如何解决这个问题？

论文通过“被动技能蒸馏”（Passive Skill Distillation）框架，将推理模式的高昂成本转化为可复用的领域技能，核心思路是“宽搜索替代深搜索”。整体框架分三步：

**第一步：收集训练语料**。在训练集上分别用推理模式和非推理模式滚动生成轨迹，形成配对语料（含思考与无思考轨迹）或仅无思考语料。这些是普通评估轨迹，无需额外采样。

**第二步：编码智能体蒸馏**。使用Claude Code等编码智能体A，读取轨迹文件并执行固定自然语言指令P，输出40-130行的Markdown技能文档。A通过对比成功/失败轨迹、计算失败模式频率、识别动作循环等统计信息，提取可追溯的具体规则（如零售领域“调用find_user_id_by_email前必须验证邮箱存在”）。蒸馏成本仅1.28-2.44美元/域，且A无环境访问权限，仅依赖静态文件分析。

**第三步：部署注入**。将技能原样追加到非推理模型的系统提示中，形成π_skl = M_nr(·|sys⊕skl)。除提示前缀外，解码、工具调用等均不变，前缀可缓存复用。

**核心创新**在于：1）将跨episode的共享程序性知识从推理轨迹中剥离，以自然语言技能形式固化；2）证明推理轨迹并非必需——仅用非推理轨迹蒸馏的技能与配对语料蒸馏效果相当；3）通过“搜索透镜”解释：测试时推理是单episode内的深度搜索，每次部署重复付费；语料蒸馏是跨episode的宽度搜索，一次付费永久受益。在四个基准上，技能恢复了55%-100%+的推理差距，同时减少2.7-6倍输出token，零推理token，且在ALFWorld和零售域上超越推理模式。

### Q4: 论文做了哪些实验？

论文在四个基准上评估了“技能蒸馏”方法：ALFWorld（文本家务任务，50个留出任务，胜率）、SSB-Verified（真实表格操作，50个任务，修改准确率）、τ²-bench的电信和零售域（对话客服，各40个任务，通过率）。实验使用GPT-5.4-mini（reasoning_effort设为none/medium）和Qwen（enable_thinking设为false/true），每个条件取3个随机种子的均值，技能由Claude Sonnet 5从训练轨迹中蒸馏一次。

主要对比三种模式：思考模式（think）、非思考模式（no-think）、非思考+蒸馏技能（no-think+skill）。结果显示，对GPT-5.4-mini，技能恢复了55%-100%+的推理差距，在ALFWorld（0.787 vs 0.713）和零售（0.408 vs 0.350）上超过思考模式，同时输出token减少2.9-4.5倍且零推理token。对Qwen，技能在三个基准上有效（ALFWorld达0.980，电信匹配思考模式0.933），但零售域出现4.2点回退。

消融实验对比了从纯非思考轨迹与配对思考/非思考轨迹蒸馏的技能，两者在ALFWorld（0.787 vs 0.813）和电信（0.333 vs 0.325）上接近，零售上配对更优（0.458 vs 0.408），SSB上纯非思考反而高10点（0.560 vs 0.460）。与GEPA提示优化器相比，蒸馏技能在零售（45.8% vs 39.2%）和电信（32.5% vs 30.8%）上均胜出，生产成本低4.1倍（$3.72 vs $15.28）。

### Q5: 有什么可以进一步探索的点？

论文的核心局限在于技能蒸馏过程的稳定性和泛化性未被充分验证。未来可从三方面深入：其一，量化蒸馏方差，当前仅评估了推理方差，而Qwen在零售域的退化表明蒸馏本身存在随机性，可引入多轮蒸馏集成或基于验证集反馈的迭代式技能筛选机制，提升鲁棒性。其二，探索跨模型迁移，技能目前绑定单一模型，可尝试将技能抽象为与模型无关的中间表示（如伪代码或结构化规则），再通过适配层注入不同规模模型，降低重复蒸馏成本。其三，细化“宽搜索”与“深搜索”的边界，论文显示电信和表格域仍依赖实例级推理，未来可设计动态路由机制——根据任务难度或技能置信度自动选择技能复用或触发深度推理，混合策略或能进一步压缩token开销。此外，技能的可组合性也值得探索，即从不同领域抽取的技能能否拼接以应对复合型任务，这需要更细粒度的技能分解与冲突消解机制。

### Q6: 总结一下论文的主要内容

本文提出了一种将推理成本摊销为可复用技能的方法，旨在解决推理模型在智能体任务中输出token数高出3-6倍的问题。作者让编码代理从训练轨迹的小型语料库中提取简洁的自然语言技能，注入非推理模型的系统提示中。在ALFWorld、tau²-bench（电信和零售）及SpreadsheetBench四个基准上，该方法恢复了GPT-5.4-mini推理差距的55%-100%以上，其中两个基准甚至超过推理模式，同时输出token减少2.7-6倍且无需推理token。关键发现是，推理轨迹并非必需——仅从非推理轨迹蒸馏的技能与从配对语料蒸馏的技能竞争力相当。作者通过搜索视角解释：测试时推理是单集内的深度搜索，每次部署重复付费；语料蒸馏是跨集的广度搜索，一次性付费。两者恢复的程序知识重叠，而廉价轨迹的广度搜索往往更划算，但电信和SpreadsheetBench上的残余差距表明，某些领域仍需真正逐实例的深度搜索。
