---
title: "Pneuma: A Large-Scale Real-World Time Series Benchmark for Commercial Aircraft Predictive Maintenance"
authors:
  - "Jiafeng Lin"
  - "Yutian Zhang"
  - "Huan Zhang"
  - "Yuxuan Wang"
  - "Jinyan Feng"
  - "Yuhui Liu"
  - "Zhongyi Pei"
  - "Jianmin Wang"
date: "2026-10-27"
arxiv_id: "2610.37563"
arxiv_url: "https://arxiv.org/abs/2610.37563"
pdf_url: "https://arxiv.org/pdf/2610.37563v1"
categories:
  - "cs.LG"
tags:
  - "预测性维护"
  - "工业时序基准"
  - "航空发动机引气系统"
  - "多变量时序"
  - "故障分类"
  - "无监督异常检测"
  - "真实维护日志标签"
  - "大规模时序数据集"
  - "时序基础模型评估"
  - "类别不平衡"
  - "故障演化模式"
relevance_score: 6.5
---

# Pneuma: A Large-Scale Real-World Time Series Benchmark for Commercial Aircraft Predictive Maintenance

## 原始摘要

Predictive maintenance is vital for commercial aviation, yet progress remains hindered by the lack of public, large-scale real-world datasets. As a result, most methods are developed and evaluated on proprietary data, limiting reproducibility. We introduce Pneuma, the first publicly available large-scale benchmark for predictive maintenance using onboard time series from in-service commercial aircraft. Built around bleed air systems, Pneuma contains over 920 million multivariate time steps across four aircraft types and 9 verified fault scenarios, directly aligned with real maintenance logs. The dataset exhibits key real-world challenges, including substantial class imbalance, subtle fault evolution patterns, and significant variance across aircraft configurations. We structure the benchmark around three tasks: multivariate forecasting, supervised fault classification, and unsupervised anomaly detection, with labels derived from actual maintenance records. Under unified settings, we evaluate over 25 models from four methodological families on 9 carefully curated subsets. The results reveal that even strong contemporary models struggle with subtle fault signatures. Further analyses show consistent gains from additional in-context examples and multivariate inference, while forecasting quality is strongly associated with anomaly detection performance. Together, these findings provide practical insights into effectively modeling complex real-world aviation time series. We hope Pneuma will serve as a rigorous and reproducible foundation for advancing data-driven predictive maintenance toward real-world deployment in commercial aviation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决商业航空预测性维护领域缺乏公开、大规模、真实世界基准数据集的问题。研究背景方面，现代飞机持续记录多变量传感器数据，为数据驱动的预测性维护提供了基础，但机上测量受飞行阶段、运行环境、飞机配置和机队类型影响显著，早期故障征兆往往微弱且易被正常运行波动掩盖，因此开发可靠模型需要来自真实航空运营的代表性数据。现有方法的不足主要体现在三方面：一是广泛使用的航空预测基准多依赖模拟退化过程或受控实验环境，无法反映日常航线运营的变异性；二是已有公开真实飞行日志数据集多局限于小型通用航空机队，难以覆盖空客A320、波音B777等主流干线机型的复杂系统架构与多样故障模式；三是基于商业机队运营数据的研究通常使用专有数据，任务定义碎片化、数据划分随意、评价指标不一致，导致可复现性差、难以进行公平的跨方法比较。本文的核心问题是：构建首个公开的、基于在役商业飞机机载时间序列的大规模真实世界预测性维护数据集与基准Pneuma，聚焦引气系统，涵盖超过9.2亿个时间步、4种机型、9个经维护记录验证的故障场景，并围绕多变量预测、监督故障分类和无监督异常检测三项任务建立统一的数据划分与评估协议，系统评测25个以上模型，以回答当前时间序列模型能否在真实飞机配置与故障场景间泛化的问题。

### Q2: 有哪些相关研究？

本文的相关研究可按三类组织。方法/评测基准类：UCR、UEA提供分类数据集与划分；M4在10万条真实序列上比较统计、机器学习与混合预测方法；TFB提供统一的预测评测流水线；TIME面向基础模型零样本预测；TSB-AD构建大规模异常检测基准并改进评测可靠性。这些通用基准便于跨模型比较，但难以保留特定领域的数据结构、标签与评测需求。领域基准类：WeatherBench为全球天气预报建立数据、指标与基线；LargeST刻画真实交通网络的规模与长期覆盖；BatteryLife整合多化学体系与工况的电池退化记录，支持专用方法与通用时序模型对比。它们说明好的领域基准应兼具代表性数据、明确任务、标准协议与可复现基线。航空时序类：C-MAPSS与N-CMAPSS提供仿真涡扇发动机退化轨迹，是RUL估计的标准基准；NASA DASHlink发布单一支线客机真实机载记录及进近阶段多类异常检测数据；NGAFID将通航飞行记录与计划外维修事件关联；GATS扩展到三种螺旋桨机型并建立机型分类与缺失重建基准；CAFUC2结合四种通航机型与物理故障注入构造正常/异常样本。区别在于，上述资源或聚焦通航、或仅覆盖单一支线机型、或依赖合成故障注入；Pneuma则基于四种干线商用客机的真实机载时序，围绕引气系统提供与维修日志对齐的多任务统一基准，填补了多机型真实故障关联数据的空白。

### Q3: 论文如何解决这个问题？

论文的核心方法是构建一个面向商用航空引气系统预测性维护的大规模真实基准 Pneuma，并围绕统一评测框架系统化地解决“缺乏公开真实数据、难以复现比较”的问题。整体框架分为数据构建、任务定义与基准评测三部分。

在数据构建上，方法首先从航空公司日常维修日志中提取已确认的故障事件，确定受影响飞机、目标部件、事件时间戳与诊断描述，作为可靠的真值标签；随后回溯对应的 QAR 机载遥测数据，剔除变量缺失或传感器流损坏的航班，按机型与故障场景组织成 9 个子集，覆盖 A320、A321、B787、B777 四种机型、9 类故障场景，共 71,451 个航班、逾 9.2 亿时间步。数据处理遵循两条关键原则：一是变量选择，仅保留与引气系统运行和故障机理直接相关的压力、温度、阀门状态、发动机工况与飞机构型变量，去除背景噪声；二是飞行阶段对齐，围绕滑行—起飞、起飞—爬升、爬升—巡航、巡航—下降四个关键转换点提取固定长度窗口，将长短不一的航班转化为可比较的标准片段，突出故障症状最易显现的系统响应。

在标注设计上，方法以故障事件为时间参照，定义“故障预警池”（事件前连续 100 个航班）与“正常池”（与所有事件保持 500 航班前、50 航班后排除边界的干净样本），形成 400 航班的缓冲带，兼顾症状相关性与实际预警提前量。

在任务与评测上，基准设置多变量预测、监督故障分类与无监督异常检测三类任务：预测任务仅在正常池上训练，用 MAE/RMSE 评估；分类与异常检测统一采用航班级序列表示，并以 P@R10（召回达 10% 时的精度）作为指标，反映实际运维中对误报成本的约束。创新点在于首个公开的商用飞机真实预测性维护基准、基于维修记录的可信标注体系、阶段对齐的标准化表示，以及三类任务统一可复现的评测协议。

### Q4: 论文做了哪些实验？

论文在Pneuma基准上围绕三个任务开展实验：多变量预测、监督故障分类和无监督异常检测，覆盖9个飞机系统子集（如320-DIFF、787-CAC、777-PRSOV等）。预测任务评估了10个全样本训练的模型（Autoformer、TimesNet、DLinear、PatchTST、iTransformer、TimeXer、TimeMixer、DUET、xPatch、OLinear）以及5个时间序列基础模型（TimesFM-2.5、Moirai-2.0、Chronos-2、TiRex-2、Toto-2.0，严格5-shot）。分类任务对比MambaSL、VSFormer、LITE、MiniROCKET、MultiROCKET及改造后的TimesNet、PatchTST、DLinear、iTransformer；异常检测对比KAN-AD、Anomaly Transformer、TranAD、USAD、OmniAnomaly，共25+模型。主要结果：预测中DLinear总分最高76.65，在9个数据集中8个误差最低；基础模型中Toto-2.0最佳（70.95），但均未超过DLinear。分类中VSFormer总分最高60.22，LITE次之53.12。异常检测整体较差，最佳Anomaly Transformer仅23.11。消融分析显示：上下文示例从2增至12时预测损失单调下降；多变量联合推理优于单变量；patch长度存在架构相关最优值；预测误差与异常检测Precision@R10显著负相关（Pearson r=-0.954，p=0.003）。

### Q5: 有什么可以进一步探索的点？

论文的局限与可探索方向主要有以下几点：其一，基准目前仅聚焦引气系统，未来可扩展到液压、起落架、发动机等更多子系统，并引入跨系统耦合故障，检验模型在更复杂物理关联下的泛化能力。其二，标签仅来自维修记录，存在记录滞后与漏报噪声，可探索弱监督或半监督标签校正，结合专家知识构建更细粒度的故障严重度分级。其三，分析显示预测质量与异常检测强相关（r=-0.954），但仅基于重建误差，未来可研究预测残差与对比学习、因果发现相结合的检测范式，提升对细微早期故障的敏感性。其四，当前仅考察上下文示例数量与patch长度等浅层因素，可进一步探索面向飞行阶段转换的物理约束建模、跨机型迁移学习以及类别不平衡下的代价敏感训练策略。此外，可引入可解释性分析，将模型关注点与真实故障机理对齐，增强工业部署的可信度。

### Q6: 总结一下论文的主要内容

论文针对商用航空预测性维护缺乏公开大规模真实数据、现有方法多在私有数据上评估而难以复现的问题，提出了 Pneuma——首个基于在役商用飞机机载时间序列的公开大规模预测性维护基准。数据聚焦易故障的引气系统，覆盖空客A320、A321与波音B787、B777四种机型、9个经维修记录核实的故障场景，包含71,451个航班、逾9.2亿个多变量时间步，并保留类别不平衡、故障演化微弱、构型差异大等真实挑战。基准围绕多变量预测、监督故障分类和无监督异常检测三项任务，提供统一数据划分与评估协议，评测了四类方法族共25个以上模型。结果表明，即使先进模型也难以捕捉细微故障特征；增加上下文示例与多变量联合推理可稳定提升性能，且预测质量与异常检测表现显著相关。该工作为航空预测性维护提供了可复现的评测基础。
