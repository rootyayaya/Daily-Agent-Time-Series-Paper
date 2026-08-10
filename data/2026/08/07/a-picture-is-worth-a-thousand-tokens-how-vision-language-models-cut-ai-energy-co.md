---
title: "A Picture is Worth a Thousand Tokens: How Vision Language Models Cut AI Energy Costs While Improving Accuracy"
authors:
  - "Bhavika Jalli"
  - "Nikhil Korati Prasanna"
  - "Jayanta Choudhury"
date: "2026-08-07"
arxiv_id: "2608.07427"
arxiv_url: "https://arxiv.org/abs/2608.07427"
pdf_url: "https://arxiv.org/pdf/2608.07427v1"
categories:
  - "cs.AI"
  - "cs.PF"
tags:
  - "Vision-Language Model"
  - "Time-Series Analysis"
  - "Anomaly Detection"
  - "Energy Efficiency"
  - "Telecom Network Analytics"
  - "Multivariate KPI"
  - "Token Reduction"
  - "Numerical Time-Series Data Analysis"
relevance_score: 8.5
---

# A Picture is Worth a Thousand Tokens: How Vision Language Models Cut AI Energy Costs While Improving Accuracy

## 原始摘要

LLM inference accounts for over 90% of AI operational energy, scaling directly with input token count---a critical inefficiency for telecom network analytics and numerical time-series data analysis (NTSDA), where raw multivariate KPI windows from 4G/5G cell sites expand into thousands of floating-point tokens. Vision-Language Models (VLMs) eliminate this mismatch by encoding time-series as 2D plots, achieving 3.6-10.4x input token reduction across Llama-3.2-90B, Qwen2.5-VL-72B, and Pixtral-12B architectures. This translates to 1.8-2.5x measured inference energy reduction, saving approximately 7.2 MJ/day at telecom edge deployments and CloudRAN that monitor 200 cells per 15-minute interval. Critically, efficiency gains do not sacrifice accuracy: a fine-tuned Llama-3.2-90B-Vision VLM achieves 220.7% higher precision than its text-only counterpart and outperforms LSTM and ARIMA baselines by over 144% on telecom anomaly detection. On public benchmarks, Pixtral-12B achieves a 20.6x improvement in J/F1 score at mean F1 = 0.82. At 24 KPIs, text representations exceed the 128K context window of most production LLMs, rendering text-only processing infeasible without truncation, while visual representations remain within standard limits. These results establish VLMs as an energy-efficient and accuracy-superior modality for numerical time-series workloads, providing empirical grounding for AI inference systems that treat energy consumption as a first-class engineering constraint.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着AI数据中心能耗激增（预计2035年达123GW），LLM推理占AI全生命周期能耗超90%，且能耗与输入token数线性相关，成为可持续部署的关键瓶颈。现有方法直接让LLM处理数值时间序列，但原始多变量KPI窗口（如8个指标、381个时间点）会膨胀为4.6万至6万token，远超生产模型上下文窗口，导致推理能耗极高，甚至因内存限制而物理不可行。此外，数值token化不增加信息密度，反而引入分词错误风险。本文核心问题是：能否通过视觉语言模型（VLM）将时间序列编码为2D图像，大幅压缩token数量，从而在降低推理能耗的同时保持甚至提升分析精度？作者首次跨三种视觉编码器架构（Llama-3.2-90B、Qwen2.5-VL-72B、Pixtral-12B）直接对比LLM与VLM在时间序列异常检测上的能耗与精度，验证VLM作为数值时间序列分析的高效替代模态，为将能耗作为一等工程约束的推理系统提供实证基础。

### Q2: 有哪些相关研究？

相关研究主要围绕三个方向展开。**方法类**工作聚焦于LLM推理能耗与输入token数的直接耦合关系，发现输入长度从100增至900 token时能耗提升2.19倍，凸显prefill阶段的优化空间；同时有研究指出VLM虽因视觉编码器带来更高单token功耗，但视觉token存在大量冗余，仅少量关键token即可支撑准确生成。**应用类**研究验证了VLM在时间序列异常检测中的优越性，其通过视觉表示放大粗粒度时间结构，在范围级和变量级定位上均优于纯文本方法，且少样本视觉提示即可超越全监督数值基线，性能提升最高达433%。**部署约束类**工作包括Shi等人对边缘GPU（如RTX A6000）的显存 profiling，证明超过6万token会触发OOM，而Kang等人提出异构GPU集群的能耗感知调度策略。本文与上述工作的核心区别在于：首次直接对比LLM与VLM在时间序列异常检测上的端到端能耗，而非仅关注单token成本或算法精度。现有研究要么忽略视觉编码器的额外开销，要么未将token压缩量化为实际能耗收益。本文通过实测证明，尽管VLM单token能耗更高，但其3.6-10.4倍的token压缩率带来1.8-2.5倍的净能耗降低，且精度不降反升（最高提升220.7%），从而将能耗作为一等工程约束纳入模型选型依据，填补了该实证空白。

### Q3: 论文如何解决这个问题？

论文通过将时间序列数据从文本模态转换为视觉模态，利用视觉语言模型（VLM）实现能耗与精度的双重优化。核心方法分为三个阶段：首先，将单变量或多变量KPI时间序列渲染为二维图像，去除坐标轴刻度、数值标签和网格线等文本伪影，避免视觉编码器处理无关字符；对于多变量数据，采用垂直堆叠子图布局，各子图共享时间轴，保持变量间对齐的同时保留独立视觉特征，这种设计在几何上对应高维流形的横截面投影，使模型能联合关注跨变量的形态特征。

其次，通过补丁生成与异常区间提议机制，将图像分割为视觉token序列，并利用结构化提示词注入检测目标与领域形态先验（如尖峰、驼峰、振荡偏差），引导模型聚焦波形几何特征。最后，在推理阶段对比三种视觉编码策略：Llama-3.2-90B-Vision采用固定6404 token的交叉注意力融合，Qwen2.5-VL-72B使用动态分辨率分块，Pixtral-12B则用16×16像素补丁保留细节，以验证方法的普适性。

创新点在于：一是将VLM4TS从单面板扩展到多变量堆叠子图，系统评估图像分辨率随变量数线性增长时的token效率边界；二是建立精确的token计量与能耗测量框架，利用Zeus和NVML硬件计数器获取GPU累计能耗，排除采样误差；三是证明视觉模态在24个KPI场景下仍保持在128K上下文窗口内，而文本模态已不可行。实验表明，视觉输入实现3.6-10.4倍token压缩和1.8-2.5倍能耗降低，同时微调后的Llama-3.2-90B-Vision在电信异常检测中精度比文本模型提升220.7%，比LSTM/ARIMA基线高144%，确立了视觉模态在数值时间序列分析中的能效与精度双重优势。

### Q4: 论文做了哪些实验？

论文在公共基准和真实电信网络数据上开展了全面的实验验证。公共实验使用realAWSCloudwatch数据集（VLM4TS基准子集），在3块NVIDIA RTX A6000 GPU上以4-bit NF4量化加载模型，对比文本（逗号分隔浮点数序列）与图像（堆叠子图）两种模态，评估Llama-3.2-90B、Qwen2.5-VL-72B和Pixtral-12B三种架构。结果显示图像模态的F1分数（0.70-0.88）全面优于文本模态（0.58-0.66），且能耗降低4.5倍、13.8倍和18.3倍；Pixtral-12B在图像模态下达到最佳J/F1效率（2,538 vs 52,356，20.6倍提升），平均F1=0.82。

电信实验使用2025年4月真实4G/5G网络数据（209个小区、24个KPI、15分钟间隔），对比ARIMA、LSTM、文本LLM、零样本VLM和LoRA微调VLM。微调后的Llama-3.2-90B-Vision达到精确率0.465，比文本LLM（0.145）提升220.7%，F1达0.464，远超ARIMA（0.186）和LSTM（0.190），同时token数减少7.2倍。额外实验表明，将图像分辨率从150 DPI降至75 DPI可减少70%视觉token和24%能耗（8,818J降至6,660J），且F1不降反升（0.354 vs 0.347），验证了低分辨率图像在保持检测精度的同时进一步优化能源效率。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从四个层面展开。首先，当前仅评估三种VLM架构且采用单GPU配置，未来可探索混合专家（MoE）或稀疏注意力机制的新型视觉模型，并量化多GPU并行推理下的通信开销与能量-吞吐量权衡。其次，固定256输出token限制了对长诊断文本的适用性，可设计动态输出预算机制，在生成质量与能耗间自适应平衡。第三，视觉编码策略存在“压缩率-保真度”矛盾，可引入基于信号复杂度（如频谱熵、突变检测）的自适应分辨率选择，对平稳段用粗粒度编码、对异常段用细粒度编码。第四，当前仅测推理能耗，未来应建立涵盖数据预处理、图像渲染、内存搬运的全系统能量模型，并开发流式推理下的能量感知批调度算法。此外，跨运营商、跨行业的泛化验证，以及将碳强度实时校准纳入可持续性报告，也是重要方向。

### Q6: 总结一下论文的主要内容

该论文针对LLM推理能耗高、文本token膨胀导致数值时间序列分析低效的问题，提出利用视觉语言模型（VLM）将多变量KPI窗口编码为2D图像，替代文本token表示。方法上，在Llama-3.2-90B、Qwen2.5-VL-72B和Pixtral-12B三种架构上验证，实现3.6-10.4倍输入token缩减和1.8-2.5倍推理能耗降低，边缘部署每日可节省约7.2MJ。关键结论是效率提升不牺牲精度：微调的Llama-3.2-90B-Vision相比纯文本模型精度提高220.7%，比LSTM和ARIMA基线高144%以上；Pixtral-12B在公共基准上J/F1分数提升20.6倍。此外，24个KPI时文本表示已超出128K上下文窗口，而视觉表示仍合规，且降低分辨率至75DPI可额外节能24%。该研究确立了VLM作为数值时间序列任务中能效更优、精度更高的模态，为将能耗作为一等工程约束的AI推理系统提供了实证基础。
