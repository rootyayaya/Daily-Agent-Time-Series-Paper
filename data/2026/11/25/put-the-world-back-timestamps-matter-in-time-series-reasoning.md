---
title: "Put the World Back: Timestamps Matter in Time Series Reasoning"
authors:
  - "Tingrui Huang"
  - "Yuanyuan Deng"
  - "Qingren Yao"
  - "Joaquin Vanschoren"
  - "Mykola Pechenizkiy"
  - "Songgaojun Deng"
date: "2026-11-25"
arxiv_id: "2611.34848"
arxiv_url: "https://arxiv.org/abs/2611.34848"
pdf_url: "https://arxiv.org/pdf/2611.34848v1"
github_url: "https://github.com/tingrui-huang/timestamps-matter"
categories:
  - "cs.LG"
tags:
  - "时间序列推理"
  - "LLM评估"
  - "时间戳因果结构"
  - "事件-序列对齐"
  - "诊断协议"
  - "捷径学习"
  - "世界状态投影"
relevance_score: 6.5
---

# Put the World Back: Timestamps Matter in Time Series Reasoning

## 原始摘要

Large language models (LLMs) are increasingly applied to time series reasoning. However, current evaluations often give models events in chronological order and already matched to the time series. This makes it unclear whether models use timestamps to connect events with observations or simply take shortcuts. To expose this ambiguity, we reformulate time series reasoning from a world-to-series projection perspective, viewing timestamps as explicit indices that connect numerical observations and external events to shared world states. We identify three structures that timestamps can make explicit: temporal causal structure, time semantics, and event-series alignment. Building on this perspective, we develop a diagnostic protocol that distinguishes timestamp-grounded reasoning from correlational shortcuts, a distinction that accuracy-based benchmarks cannot make. Controlled interventions on 310 questions from two tasks show that high accuracy can persist when timestamps are replaced by relative offsets or removed, while breaking event-series alignment induces systematic failures. When context is pre-aligned, models barely need timestamps. When order is missing, they use dates to recall world knowledge. Without dates, they rely on correlational shortcuts and rarely notice incorrect timestamps. These findings show that high accuracy on pre-aligned, ordered inputs does not establish that a model uses timestamps to synchronize observations with the world. We release our code, model outputs, and trajectory labels at https://github.com/tingrui-huang/timestamps-matter.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是大语言模型在时间序列推理中是否真正使用了时间戳这一问题。研究背景在于，LLM 正被广泛用于解释时间序列模式、预测未来走势和辅助决策，但现有评测通常把事件按时间顺序排列好、并已与时间序列手工对齐后直接喂给模型，时间序列被当作自包含的数值对象，脱离了真实世界的时间线。这种设定带来的不足是：模型可能根本不依赖时间戳，而是走捷径——顺着给定的事件顺序作答，或把事件与邻近文本做表面匹配，因此仅凭准确率无法区分“真正基于时间戳的时序推理”和“相关性捷径”，也无法判断模型是否把观测动态与背后的事件联系起来。本文的核心问题即由此而来：作者从“世界到序列投影”的视角重新表述时间序列推理，把时间戳视为连接数值观测与外部事件、指向共同世界状态的显式索引，并识别出时间戳可显式化的三种结构——时间因果结构、时间语义和事件-序列对齐；在此基础上提出诊断协议，通过受控干预检验模型是否真正使用时间戳，从而暴露预对齐、有序输入下高准确率所掩盖的捷径行为。

### Q2: 有哪些相关研究？

主要相关研究可分为三类。方法类方面，现有时间序列推理工作多将序列视为自包含数值对象，依赖人工对齐的事件文本进行建模，如各类时间序列问答与预测方法；这类工作关注数值模式建模，但默认事件与序列已对齐，未考察时间戳的作用。应用类方面，事件序列对齐、时间语义理解等研究在信息抽取与知识图谱中已有探索，强调时间戳作为跨模态索引连接文本记录与观测，但较少用于LLM时间序列推理评测。评测类方面，现有基准（如TSRBench）以准确率为核心指标，输入通常按时间顺序排列且事件已与序列配对，因而无法区分模型是真正利用时间戳进行世界状态对齐，还是走事件顺序与邻近文本匹配的捷径。本文与上述工作的区别在于：提出世界到序列投影视角，将时间戳视为连接观测与事件的显式索引，并设计时间因果诊断协议（TCDP），通过替换、移除时间戳及破坏事件-序列对齐等干预，区分基于时间戳的推理与相关性捷径，从而揭示准确率评测掩盖的评测盲区。

### Q3: 论文如何解决这个问题？

论文的核心思路是把时间序列重新表述为“世界过程的有损投影”：真实世界过程 W 由带时间戳的事件流 E={(τ_j,e_j)} 近似，再经投影 π 压缩为离散观测 X={(t_i,x_i)}。时间戳 τ_j 与 t_i 是事件与数值观测共享的显式索引，是模型把观测“放回世界”的唯一桥梁。基于此，作者识别出时间戳应显式承载的三种结构：一是时间因果结构（why），即因果滞后长度与同时性，仅靠顺序无法区分一小时与一周的滞后；二是时间语义（when），即每个 t_i 是检索世界知识的键，同一模式在不同日期对应不同世界状态；三是事件—序列对齐（what），即时间戳决定事件与观测窗口是重叠、先于还是落在窗口之外，从而判断其是否为有效证据。

在架构上，论文提出时间因果诊断协议（TCDP），将上述三种结构操作化为一组二元规则清单，按三个族分组，逐条审计 LLM 的推理轨迹。其设计要点是：准确率只记录结论对错，TCDP 检查结论如何得出；每条规则都是“时间戳接地推理”的必要条件而非评分，并先判断基准是否要求该规则才能答对，再检查轨迹是否遵循。关键技术是受控干预：对两个任务共 310 道题，分别用相对偏移替换时间戳、删除时间戳、破坏事件—序列对齐，观察模型表现。结果显示，替换或删除时间戳后高准确率仍可维持，而对齐被破坏则引发系统性失败，说明模型在预对齐、有序输入下依赖相关性捷径而非时间戳同步，从而把“时间戳接地推理”与“相关性捷径”区分开来。

### Q4: 论文做了哪些实验？

论文在TSRBench的两个任务上开展实验：NBA（150题）要求从四个候选事件中选出缺失事件，GDELT（160题）要求从四个选项中选出真实事件顺序，且事件时间随机排列、不与摘要配对。实验设置三种干预：Relative（将时间改为相对偏移，保留顺序与间隔）、No-TS（删除所有时间戳）、Shuffled（保留序列但将时间错配到其他事件，破坏事件-序列对齐）。对比模型包括Sonnet-5、GLM-5.3-Flash、Qwen3.6-35B-A3B和Qwen3.5-9B（NBA），以及GLM-5.3-Flash和Sonnet-5（GDELT），并用LLM对GLM-5.3-Flash的轨迹标注决策方法。主要结果：NBA上三个较强模型在Relative下准确率与Full无显著差异（如GLM-5.3-Flash 98.7% vs 97.3%），No-TS略降（94.7%），Shuffled降幅最大（86.7%）；Qwen3.5-9B例外，No-TS降至51.3%。GDELT上GLM-5.3-Flash在No-TS下准确率从52%骤降至12%，Relative降至40%，Shuffled降至32%，且仅约三分之一运行察觉时间错配。轨迹分析显示模型多依赖捷径（如61–66%读取标记行分数变化、29–57%用故事语气匹配GoldStein值），很少真正校验时间戳。

### Q5: 有什么可以进一步探索的点？

论文的局限主要在于：诊断仅覆盖两个任务（NBA、GDELT）和有限模型，结论的普适性有待验证；干预手段以时间戳替换、移除和错位为主，尚未系统考察多粒度时间语义（时区、粒度聚合、模糊表述）的影响；轨迹标注依赖人工或规则，规模与一致性受限。未来可探索的方向包括：构建更大规模、跨领域（金融、医疗、工业传感）的时间戳诊断基准；引入反事实训练与时间戳扰动增强，迫使模型真正对齐事件与观测；设计可解释的轨迹级评测指标，将“是否使用时间戳”量化为可训练信号；结合工具调用与外部日历/知识库，检验模型在缺失或错误时间戳下的纠错能力。我的补充思路是：可将时间戳视为可学习的位置编码注入 LLM，并在推理链中显式要求引用时间索引，从而把诊断协议转化为训练约束，缓解相关性捷径问题。

### Q6: 总结一下论文的主要内容

论文针对大语言模型时间序列推理评测中时间戳作用被高估的问题，提出“世界到序列投影”视角，将时间戳视为连接数值观测与外部事件、指向共享世界状态的显式索引，并据此识别时间因果结构、时间语义和事件-序列对齐三种结构。作者构建诊断协议，区分基于时间戳的推理与相关性捷径，并对两个任务共310个问题进行受控干预实验。结果表明：当上下文已预对齐时，模型几乎不需要时间戳；当顺序缺失时，模型利用日期回忆世界知识；当日期被移除时，模型依赖相关性捷径，且很少发现错误时间戳。破坏事件-序列对齐会引发系统性失败。论文结论是，预对齐有序输入上的高准确率并不能证明模型真正使用时间戳同步观测与世界，基准评测应同时检查推理路径而非仅看准确率。
