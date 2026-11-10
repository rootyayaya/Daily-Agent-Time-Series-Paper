---
title: "PIA: Agentic Physics-Informed Runtime Anomaly Detection"
authors:
  - "Ali Mohammadi Ruzbahani"
  - "Abbas Yazdinejad"
  - "Hadis Karimipour"
date: "2026-11-07"
arxiv_id: "2611.11009"
arxiv_url: "https://arxiv.org/abs/2611.11009"
pdf_url: "https://arxiv.org/pdf/2611.11009v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "LLM Agent"
  - "Physics-Informed"
  - "Anomaly Detection"
  - "Industrial CPS"
  - "Runtime Monitoring"
  - "Human-Readable Detector"
  - "Evaluation Workbench"
  - "BATADAL"
  - "Attack Attribution"
relevance_score: 8.5
---

# PIA: Agentic Physics-Informed Runtime Anomaly Detection

## 原始摘要

Runtime anomaly detectors for cyber-physical systems are either learned as black boxes from normal data, which miss stealthy manipulations that keep every signal inside its normal range, or derived by hand from physical models, which requires expert effort for every plant. We introduce physicsinformed agents (PIA), in which a large language model agent writes the detector itself as a set of physical residuals, such as pump characteristics, tank mass balances, and controller logic, and refines every candidate against normal operating data through an evaluation workbench before deployment. The result is a compact, human-readable detector that runs in milliseconds and names the component behind each alarm. On the BATADAL water distribution attack benchmark, PIA with Claude Opus 5.5 reaches an F1 of 0.878 on the test attacks against 0.504 for the strongest of six statistical and deep baselines, keeps detecting attacks concealed by replayed and offset sensor readings, and attributes every detected test attack to the attacked component. Ablations show that testing hypotheses against data is decisive: agents that write residuals from the plant description alone lose up to 0.28 F1, whereas agents that see only anonymized signals recover most of the physical structure.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注信息物理系统（CPS）运行时异常检测这一关键问题。此类系统（如供水管网、工业装置）在运行中可能遭受攻击，攻击者会刻意让每个传感器读数都保持在正常范围内，从而实施隐蔽操纵。现有方法存在两类明显不足：一类是纯数据驱动的黑箱检测器（如自编码器、循环预测器），它们只学习传感器信号的联合统计分布，不了解哪些关系在物理上是必须成立的，因此对“重放”的罐液位或“偏移”的压力读数这类统计上仍合理的隐蔽攻击无能为力，而且报警时无法指出问题出在哪个部件；另一类是手工推导的物理残差检测器，虽然灵敏且可解释，但每条残差都需要工程师针对具体工厂进行推导、参数化和调优，专家成本高、难以规模化。

因此，本文要解决的核心问题是：如何自动构建既具备物理残差检测器的灵敏度和可解释性、又无需人工逐厂推导的轻量级运行时攻击检测器。作者将这一问题形式化为“智能体程序合成”，让大语言模型智能体根据工厂的自然语言描述提出物理残差（如泵特性、储罐质量平衡、控制器逻辑），并通过在正常数据上的评估工作台反复检验和修正候选残差，最终生成确定性、毫秒级运行、能定位到具体被攻击部件的可读检测器。

### Q2: 有哪些相关研究？

相关研究可分为四类。方法类：基于物理模型的攻击检测通过比较传感器读数与系统模型预测、对残差设阈值报警，其优势是隐蔽攻击须同时维持多个耦合读数一致，但需为每套装置手工建模；统计过程监控方法（PCA、孤立森林、循环预测器、自编码器及对抗训练自编码器）从正常数据学习行为、不含物理结构，是本文的基线。物理信息机器学习将已知定律嵌入学习，稀疏回归从数据发现控制方程，但均假定候选项由建模者给定。应用与评测类：BATADAL 竞赛建立了配水网络攻击的公共基准，本文在其上评测。LLM 与智能体类：语言模型配合自动评估器可通过迭代搜索发现新程序；FedReason 将 LLM 用作异构联邦学习的权重空间元聚合器，记忆投毒、智能体能源系统中的联邦遗忘等研究关注智能体环境的安全与治理。区别在于：PIA 让 LLM 在检测器构建阶段提出物理残差假设并由评测工作台用数据检验，所得检测器固定、可读、运行时不依赖 LLM，而上述工作或依赖手工建模、或缺乏物理结构、或作用于模型参数与持久记忆而非合成可解释的物理一致性检查。

### Q3: 论文如何解决这个问题？

论文提出的PIA（Physics-Informed Agents）将检测器设计从人工建模或黑箱学习转变为由大语言模型智能体自主编写物理残差。整体框架分为设计阶段与运行阶段：设计阶段智能体在系统提示（含残差形式、表达式语言、工厂描述P，包括信号含义与单位、泵罐阀拓扑、罐体尺寸、控制器切换规则）指导下，通过多轮会话与四工具工作台交互——信号统计摘要、任意表达式与全信号相关性分析、候选残差在正常数据上的拟合/评估（返回解释方差、误报率、评估与拟合尾分位数之比以暴露漂移或过拟合、以及合成操纵检测率）、候选集组装为完整检测器并报告误报率与未覆盖信号；最终提交4至24个残差。每个残差由目标表达式g_k与可选输入表达式h_k构成，原始残差为g_k减去θ_k^T h_k，θ_k由正常数据最小二乘拟合以吸收罐截面积、泵增益等未知常数，结构关系则由智能体提供。残差经中位数与MAD标准化、短窗平均、按正常数据上分位数归一化得到统一尺度的u_{k,t}，检测分数取各残差最大值，超过阈值τ即报警，并按报警片段内累积u_{k,t}最大的残差所涉部件进行归因。创新点在于让语言模型贡献假设空间、工作台负责证伪，兼顾可读性、毫秒级运行与逐行审计；消融表明仅凭工厂描述写残差会损失至多0.28 F1，而仅见匿名信号的智能体仍能恢复大部分物理结构，说明用数据检验假设是关键。

### Q4: 论文做了哪些实验？

论文在BATADAL水分配网络攻击基准上开展实验，使用C-Town网络43个SCADA信号（7个水箱液位、11台泵与1个阀的流量和状态、12个泵阀站节点压力）。训练仅用一年正常运行数据，六个月Dataset 2（7次攻击）与三个月测试集（7次攻击）仅用于评估，标签取自官方攻击时间表。对比方法包括PCA监控（T²+Q统计）、孤立森林、稠密自编码器、LSTM预测器、LSTM自编码器和USAD，所有方法共享相同的分数平滑与分位数阈值规则，随机基线用5个种子训练；PIA使用Claude Sonnet 5.5与Opus 5.5，每种配置5个独立会话、每个会话限40轮。评价指标为逐点精确率、召回率、F1、AP及竞赛分数S。主要结果：测试集上Opus版PIA将F1从最强基线PCA的0.504提升到0.878，AP从0.713升至0.899，S从0.784升至0.927；Dataset 2上F1从0.628升至0.824。增益主要来自召回率（0.349→0.874），基线在攻击隐蔽后失效，而物理残差在整个攻击期间持续报警。Opus在5个会话中4次检出全部7次测试攻击，且每次检出的残差均涉及被攻击部件。消融显示：去掉评估工作台使Opus测试集F1下降0.28、Sonnet下降0.22；仅看匿名信号的盲配置仍达0.858和0.842 F1，但组件定位准确率从1.0降至0.714。部署检测器约含20个拟合表达式，拟合耗时0.13秒，三个月测试期评分仅33毫秒。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于：残差程序目前是一次性设计、静态部署，当管网拓扑、工况或传感器可靠性发生变化时缺乏自适应修订机制；评估仅限BATADAL单一基准，未覆盖多类CPS与真实在线漂移场景；归因只到组件级别，未区分操纵类型；且依赖LLM一次性生成候选关系，搜索效率与关系完备性缺乏保证。未来可探索：一是引入持续验证与增量修订流程，在保留可解释性与毫秒级推理的前提下，用正常数据在线校验并替换失效残差，可结合机器遗忘思想实现局部更新；二是让智能体直接读取工程文档、P&ID图或仿真网络模型，提升关系提出的语义精度；三是将归因从“哪个组件”细化到“何种操纵”（重放、偏置、协同伪造），并研究攻击者伪造重叠关系时的对抗鲁棒性；四是扩展到电力、化工等多领域基准，检验跨系统迁移能力。此外，可探索人机协同的设计会话，让工程师反馈融入关系搜索循环，形成可审计、可维护的检测器生命周期管理。

### Q6: 总结一下论文的主要内容

论文针对信息物理系统运行时异常检测的两难问题：统计与深度学习方法作为黑箱难以发现所有信号仍处于正常范围的隐蔽操纵，而手工推导物理模型又需针对每套设备投入专家成本。为此提出物理信息智能体（PIA），让大语言模型智能体自行编写由泵特性、储罐质量平衡、控制器逻辑等物理残差构成的检测器，并在部署前通过评估工作台用正常运行数据逐一检验和精炼候选残差，最终得到紧凑、人类可读、毫秒级运行且能指明故障部件的检测器。在BATADAL供水管网攻击基准上，PIA配合Claude Opus 5.5取得F1为0.878，显著优于六个统计与深度基线中最强者的0.504，并能识别重放与偏移传感器读数所掩盖的攻击，且对每个检出的测试攻击均正确归因到受攻击部件。消融实验表明，用数据检验假设至关重要：仅依据设备描述编写残差的智能体F1最多下降0.28，而仅见匿名信号的智能体仍能恢复大部分物理结构。该工作表明，智能体式程序合成可为缺乏手工物理模型的设备提供可解释、低成本的运行时监测路径。
