---
title: "TT-SAX: A Two-Track Time Series Symbolization for Natural Language Shape Querying"
authors:
  - "Zhao Tan"
  - "Xianglong Bao"
  - "Zhipeng Xi"
  - "Ming Jin"
date: "2026-10-22"
arxiv_id: "2610.30593"
arxiv_url: "https://arxiv.org/abs/2610.30593"
pdf_url: "https://arxiv.org/pdf/2610.30593v1"
github_url: "https://github.com/Atlamtiz/tt-sax"
categories:
  - "cs.DB"
  - "cs.CL"
tags:
  - "时间序列符号化"
  - "自然语言查询"
  - "形状查询"
  - "LLM"
  - "语义桥接"
  - "时序数据库"
  - "SAX改进"
  - "NLQTSBench"
  - "可解释时序分析"
relevance_score: 7.5
---

# TT-SAX: A Two-Track Time Series Symbolization for Natural Language Shape Querying

## 原始摘要

Natural language querying for time series databases aims to let users find what they need in long histories of data by asking in plain language. Shape queries ask how a series moves. They are the main challenge of this task. Recent work makes them feasible by using symbolization as a bridge between the query and the long history. However, existing symbolizations were designed for compression, similarity indexing, or classification. What a symbolization should provide for natural language querying has not been systematically studied. We therefore examine the definitions of six classical symbolizations against this task and identify three limitations. (1) Direction is missing from the string, (2) direction is measured at too small a scale, and (3) the letters are arbitrary. Three design principles follow. We follow these principles and make a minimal redesign of SAX called TT-SAX (two-track SAX). The level letters stay. Each segment gains a trend letter. It is measured across neighboring segments rather than inside one, and graded to match the adjectives that queries use. We conduct extensive experiments on the public NLQTSBench benchmark, comparing TT-SAX with the six classical symbolizations across six LLMs. TT-SAX outperforms all six on shape queries, and ablations trace its gains back to the three limitations one by one. This paper is the first systematic study of time series symbolization with natural language querying as the design goal. It provides a foundation for future research on this task. Our code is available at https://github.com/Atlamtiz/tt-sax.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注自然语言查询时间序列数据库（NLQ4TSDB）中的形状查询问题，即用户用一句话询问序列“怎么变化”，例如“价格哪天暴跌后迅速回升”。这类查询是 NLQ4TSDB 的核心难点。近期 Sonar-TS 借助符号化把长序列压缩成离散符号串，再由 LLM 将查询编译为正则表达式进行匹配，使数据库规模的形状查询成为可能。但现有符号化方法（如 SAX、ESAX、1d-SAX 等）原本是为压缩、相似性索引或分类设计的，并未系统研究“面向自然语言查询的符号化应提供什么”。作者据此审视六种经典符号化，指出三大不足：一是方向信息缺失，涨跌只能靠层级字母的顺序隐含，正则难以精确表达；二是方向在单个短分段内测量，易受噪声干扰，长趋势被写成断裂的趋势字母串；三是字母编码任意抽象，如 1d-SAX 用“e”表示陡升，对 LLM 检索不友好。论文的核心问题即：如何以自然语言查询为设计目标重新设计时间序列符号化，使形状方向显式、在查询所描述的尺度上测量、且字母对 LLM 具有可解释性，从而提升形状查询的准确性。

### Q2: 有哪些相关研究？

相关研究可分为四类。方法类：SAX及其衍生符号化方法，包括ESAX（增加极值字母）、1d-SAX（回归斜率字母）、TFSAX（趋势角度字母）、TSAX（斜率符号）、TVA（段内斜率助记字母），以及Zalewski等跨段量化相邻段均值差的做法——后者是本文趋势词最接近的先例；ABBA采用自适应多边形链聚类，SFA与SPARTAN基于频域/投影系数，因无法按时间顺序表达形状而被排除。应用类：Sonar-TS在SAX词上做正则检索并用原始值验证，其NLQTSBench是本文评测基准，但它固定使用SAX、未质疑符号化选择；SAXRegEx在SAX串上跑正则，但模式需人工示例调优；SDL要求用户写形式化形状表达式；Qetch等草图接口降低编写门槛但不解决规模；ShapeSearch经固定解析器进入封闭代数；Qute将趋势词汇映射为数值形状；TSseek用空间索引达数据库规模但查询为形式化趋势表达式。评测类：既有符号化比较以重构、距离和分类为指标，本文首次以LLM自然语言查询为设计目标进行系统研究。神经类：时间序列语言模型与对比检索器直接处理语言，但需对每个候选窗口跑模型，难以扩展到数据库规模。

### Q3: 论文如何解决这个问题？

论文的核心方法是提出 TT-SAX（双轨 SAX），对经典 SAX 符号化做最小化重设计，使其服务于自然语言形状查询。整体框架上，每个窗口被写成由竖线分隔的两个词：水平词（level word）保留原 SAX 的 w 个字母，由窗口归一化后各段均值的 Gaussian 断点生成；趋势词（trend word）为每段新增一个趋势字母，两词逐位对齐，从而在同一位置同时表达“处于什么水平”和“朝哪个方向变化”。

关键技术有三点。其一，趋势测量跨段而非段内：对第 i 段，用相邻段真实均值 p 的中心差分 d_i=(p_{i+1}-p_{i-1})/2 计算，两端用单边差分。这相当于平滑，能抵抗长趋势内部的噪声，并与自然语言宏观描述形状的方式一致；同时中心化使方向归属于中心段，与水平字母对齐。其二，趋势分级采用两个固定阈值 τ1=0.10、τ2=0.30（在窗口归一化尺度上），把变化幅度分为稳定、缓慢、陡峭三档，符号决定方向，阈值在实验前固定，未用标签调参。其三，设计面向 LLM 的助记字母表：f 表示下降、s 表示稳定、r 表示上升，大小写区分缓慢与陡峭，得到 F、f、s、r、R，且上升与下降对称。

创新点在于：不是引入新的数值运算，而是将“宽度与水平网格解耦的上下文趋势测量、双轨对齐、面向语言的字母表”三者组合起来，系统性地回应现有符号化缺失方向、方向尺度过小、字母任意这三大局限，并在 NLQTSBench 上跨六个 LLM 验证其在形状查询上的优势。

### Q4: 论文做了哪些实验？

论文在公开基准 NLQTSBench 上开展实验，其复合趋势子集包含 220 条查询，覆盖多领域真实通道，查询由 rise、fall、stable 及 rapid、slow、steady、fluctuating 等形容词构成二至四段趋势模式。评测流程统一为符号化、LLM 编译正则、匹配三步，唯一变量是符号化方法。对比对象为六种经典符号化：SAX、ESAX、1d-SAX、TFSAX、TSAX、ABBA，统一设置 w=24、α=5，主实验用 DeepSeek-V4-Flash，并在 DeepSeek-V4-Pro、Gemini-3.7-Flash、GPT-5.6-Luna、Qwen3.6-35B、Claude Haiku 4.5 上做稳健性验证。指标为 Recall、Candidates 和 Lift。无 skills 时 TT-SAX 的 Lift 为 2.42，是 1d-SAX（1.42）的 1.7 倍，其余基线均低于 1.5；有 skills 时 TT-SAX 达 3.04，为次优的 1.4 倍。消融显示去掉趋势字母后 Lift 降至 1.00，去掉层级字母仍保持 2.03；趋势测量跨两个邻居段最佳；字母含义与大小写配对影响明显，交换大小写使 Recall 从 0.71 降至 0.61。跨模型平均 Lift 无/有 skills 分别为 1.81 和 3.28，优于最佳经典方法的 1.24 和 1.93；在 1000 条新查询压力测试中结果稳定。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有三。其一，TT-SAX 仅在 SAX 上做最小改造，趋势字母采用离散分级，粒度与阈值依赖人工设定，未来可研究自适应分级或数据驱动地学习字母边界，使符号化与查询形容词分布对齐。其二，趋势跨相邻段测量虽缓解了尺度问题，但段长、窗口等超参对多尺度形状（如缓慢漂移与突变）的鲁棒性尚未系统分析，可引入多分辨率双轨表示。其三，实验集中于 NLQTSBench 与六个 LLM，缺乏对噪声、缺失、非平稳及跨域迁移的检验，也未评估符号串长度对上下文窗口的压缩收益。此外，可探索将趋势字母与 LLM 的推理链结合，让模型显式引用符号证据以提升可解释性；或将双轨符号化推广到多变量序列，刻画通道间趋势耦合。

### Q6: 总结一下论文的主要内容

论文针对自然语言时间序列数据库查询中的形状查询问题展开研究，即用户希望用一句话描述序列的走势（如“先暴跌后快速回升”）并在长历史数据中检索。现有做法以符号化为桥梁，将序列压缩为离散字符串，再由大模型把查询编译为正则表达式匹配。但经典符号化是为压缩、相似性索引或分类设计的，论文系统分析六种经典方法后指出三大局限：字符串中缺少方向信息、方向在单个短分段内测量易受噪声干扰、字母编码任意且对LLM不友好。据此提出三条设计原则，并对SAX做最小改造，得到TT-SAX：保留原水平字母词，另增一条对齐的趋势词，每个分段依据相邻分段计算中心差分，用F、f、s、r、R五个助记字母表示陡降、缓降、平稳、缓升、陡升。在NLQTSBench上跨六个LLM的实验表明，TT-SAX在形状查询上优于全部六种基线，消融实验逐项验证了三个设计选择的贡献。该文是首个以自然语言查询为设计目标的时间序列符号化系统研究，为后续工作奠定基础。
