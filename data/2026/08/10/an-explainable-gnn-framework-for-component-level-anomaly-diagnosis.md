---
title: "An Explainable GNN Framework for Component-Level Anomaly Diagnosis"
authors:
  - "Sena Ozgunay"
  - "Louise Travé-Massuyès"
  - "Jean-Michel Loubes"
  - "Raul Sena Ferreira"
date: "2026-08-10"
arxiv_id: "2608.09246"
arxiv_url: "https://arxiv.org/abs/2608.09246"
pdf_url: "https://arxiv.org/pdf/2608.09246v1"
categories:
  - "cs.AI"
tags:
  - "可解释GNN"
  - "组件级诊断"
  - "多变量时间序列"
  - "异常检测"
  - "工业系统"
  - "传感器影响分析"
relevance_score: 6.5
---

# An Explainable GNN Framework for Component-Level Anomaly Diagnosis

## 原始摘要

Industrial processes are complex systems composed of multiple interacting sensors that generate multivariate time series (MTS). Detecting anomalies in such systems is critical for reliability and safety, yet understanding their origin is equally important. Existing Graph Neural Network (GNN)based methods for anomaly detection primarily focus on sensor-level deviations and either attribute anomalies directly to the deviating sensors. When diagnosis is attempted, generally, the most deviated sensor is identified as a root cause of a system fault. However, in many industrial systems, anomalies do not arise from faulty sensors but from disruptions in the influences governing the system dynamics. We propose an explainable GNN-based anomaly detection framework that shifts the perspective from sensor-level anomalies to component-level diagnosis, hypothesizing that anomalous measurements are symptoms of altered inter-sensor influences. Experiments show that the method effectively identifies and prioritizes the true faulty components, providing interpretable insights into system failures.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

工业系统通常由多个相互作用的传感器构成，产生多变量时间序列，其异常检测对可靠性与安全性至关重要。现有基于图神经网络（GNN）的异常检测方法主要聚焦于传感器级别的偏差，诊断时往往直接将偏差最大的传感器视为故障根因。然而，在许多实际工业场景中，异常并非源于传感器自身故障，而是由于物理组件（如管道泄漏）扰乱了系统动态中的传感器间影响关系，导致功能正常的传感器产生异常读数。因此，传感器层面的归因会误导诊断。

本文提出可解释的 XS2C（eXplainable Sensor-to-Component）框架，将视角从传感器级异常转向组件级诊断，核心假设是异常测量是传感器间影响关系改变的症状而非故障本身。该框架结合基于注意力机制的GNN与基于一致性的模型诊断（MBD），通过神经格兰杰因果构建图结构，利用微调学习异常行为并计算注意力变化，再通过路径搜索与一致性推理识别真正的故障组件，最终生成排序后的全局解释。其核心问题是解决现有方法无法区分传感器症状与组件根因的局限，提供组件级别的可解释诊断。

### Q2: 有哪些相关研究？

本文的相关研究主要围绕图神经网络（GNN）在多变量时间序列异常检测与诊断中的应用，可分为以下几类：

**方法类**：包括图结构学习与异常检测框架。GDN通过可学习节点嵌入的余弦相似度端到端学习图结构，并结合图注意力网络（GAT）进行预测，为每个传感器计算异常分数。此外，还有基于重建和预测混合策略的方法，通过重建误差与预测偏差联合判定异常。本文与这些方法的区别在于，现有方法主要关注传感器级别的偏差，而本文将诊断视角提升至组件级别，假设异常测量是传感器间影响关系改变的“症状”。

**因果推断类**：神经格兰杰因果（NGC）方法可捕捉传感器间的有向数据驱动影响，相比相似度度量或领域知识构建的图，能提供更丰富、可解释的因果结构。本文借鉴NGC思想构建图结构，但进一步将因果影响的变化作为组件级故障诊断的依据，而非仅用于预测或传感器级归因。

**可解释性研究**：关于GNN中注意力机制的解释性存在争议，有研究质疑注意力系数是否忠实反映模型预测依据。本文承认这一争议，但提出在MTS场景中，注意力系数可作为传感器影响演变的指示信号，用于对比正常与故障状态下的影响变化，从而支持组件级诊断。

综上，本文在现有GNN异常检测基础上，创新性地将诊断对象从传感器转向组件，利用因果图与注意力变化提供可解释的故障定位，弥补了现有方法在根因解释上的不足。

### Q3: 论文如何解决这个问题？

XS2C框架将异常诊断从传感器层面转向组件层面，核心假设是异常测量是传感器间影响关系改变的“症状”，而非传感器本身故障。整体架构包含三个模块：

**图构建模块**：利用神经Granger因果（NGC）从正常训练数据中提取有向因果图。采用组件式MLP（cMLP）作为预测模型，通过组Lasso惩罚将不相关的历史输入权重压缩为零，以因果分数\(s_{ij}\)量化传感器j对i的时序影响，再通过行分位数阈值筛选邻居节点，形成稳定的因果图结构。

**GNN异常检测模块**：基于GDN的注意力预测架构，为每个传感器学习全局嵌入向量，通过融合嵌入的注意力机制计算边权重\(\alpha_{ij}(t)\)，聚合邻居信息预测当前测量值。创新点在于采用传感器级自适应阈值策略——在验证集上根据目标正预测率（PPR）选择分位数作为各传感器独立阈值，避免传统系统级阈值忽略渐进式或异质性异常的问题。检测后通过最大间隔法从异常发生频率中自动筛选症状传感器集合。

**异常诊断模块**：核心创新在于“半冻结微调”策略——保留正常模型的图拓扑和传感器嵌入，仅微调其余权重以学习故障状态下的行为变化。通过对比正常模型与故障模型在故障周期内的平均注意力系数，计算边注意力变化\(\Delta\alpha_{ij}\)作为影响关系改变的量化指标。基于一致性诊断理论，将因果图作为系统描述（SD）、边作为组件（COMPS）、症状标签作为观测（OBS），通过冲突识别与最小命中集计算生成最小诊断集合，并利用注意力变化大小对候选诊断进行排序，最终输出最可能的故障组件。

该框架的关键创新在于：将诊断对象从传感器转移到边（影响关系），通过注意力变化捕捉系统动力学改变，结合模型诊断理论提供可解释的组件级故障归因。

### Q4: 论文做了哪些实验？

论文在TEP和SWaT两个基准数据集上评估了XS2C框架的异常检测与诊断性能。TEP包含20种故障场景（IDV1-20），共33个变量，训练集3330个样本；SWaT含51个变量，训练集47515个样本。实验对比了GDN、MTAD-GAT和CST-GL三种GNN基线方法，采用宏F1分数和MCC作为评估指标。检测时通过聚合传感器级预测进行系统级判定（TEP用N=2，SWaT用N=15）。

主要结果显示：在TEP上，XS2C的平均F1为0.70、MCC为0.59，显著优于GDN（0.31/0.18）、MTAD-GAT（0.57/0.47）和CST-GL（0.62/0.51），尤其在IDV4、10、12、13、16-20等持续或结构化异常场景中表现最佳；在SWaT上，XS2C的F1为0.88、MCC为0.78，略优于基线。此外，论文以IDV1和IDV14为案例进行诊断分析，通过提取局部因果子图并搜索最小冲突路径，成功识别出与流4进料扰动相关的关键影响边（如e_{13,4}、e_{13,26}）及反应器冷却系统相关边（如e_{32,9}），验证了框架从组件层面解释故障根源的能力。

### Q5: 有什么可以进一步探索的点？

该论文提出的XS2C框架在组件级异常诊断上展现了创新性，但仍存在若干可探索的方向。首先，当前方法依赖NGC模块学习静态因果图，难以捕捉工业过程中时变的动态因果关系，未来可引入时序因果发现或在线图结构更新机制，以适配非平稳工况。其次，诊断结果仅通过案例研究定性验证，缺乏与真实故障根因的定量对比指标，可构建带组件级标注的基准数据集或利用仿真平台注入已知故障来评估诊断精度。第三，注意力权重变化作为解释依据可能受噪声干扰，可结合因果干预或反事实推理增强解释的鲁棒性。此外，当前框架在弱扰动故障（如IDV3、IDV5）上检测性能不佳，可探索多尺度特征融合或异常传播动力学建模来提升敏感性。最后，将诊断结果与领域知识（如控制回路拓扑）融合，构建人机协同的交互式诊断Agent，可进一步提升实用性和可操作性。

### Q6: 总结一下论文的主要内容

本文提出了一种面向工业系统组件级异常诊断的可解释GNN框架XS2C，核心创新在于将异常视角从传感器级偏差转向组件级故障。问题定义上，作者认为多变量时间序列中的异常测量是传感器间影响关系被破坏的症状，而非传感器自身故障，例如管道泄漏会导致多个健康传感器读数异常。方法上，框架首先利用神经格兰杰因果构建图结构，并基于GDN进行异常检测；随后用含异常测试数据微调模型以学习异常行为，计算微调前后注意力变化；最后通过图结构中的路径搜索与一致性诊断推理，识别故障组件并生成排序后的全局解释。实验表明，该方法能有效识别并优先排序真实故障组件，为复杂工业系统提供可解释的故障洞察。其意义在于首次统一了注意力GNN与一致性诊断，推动异常诊断从“定位异常传感器”向“解释系统故障根源”的范式转变。
