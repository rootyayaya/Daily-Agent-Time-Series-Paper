---
title: "SEAM: Global consistency beyond local accuracy in scientific machine learning"
authors:
  - "Gnankan Landry Regis N'guessan"
  - "Bum Jun Kim"
date: "2026-08-06"
arxiv_id: "2608.05702"
arxiv_url: "https://arxiv.org/abs/2608.05702"
pdf_url: "https://arxiv.org/pdf/2608.05702v1"
categories:
  - "cs.LG"
  - "cs.CE"
tags:
  - "可解释性"
  - "全局一致性"
  - "科学机器学习"
  - "解释审计"
  - "分布偏移监测"
  - "传感器"
  - "多区域分析"
relevance_score: 6.5
---

# SEAM: Global consistency beyond local accuracy in scientific machine learning

## 原始摘要

Scientific machine learning commonly validates models at the level of a subdomain, a benchmark split, or an explanation for one prediction. Yet such local checks cannot establish whether the resulting explanations can be assembled into one globally admissible explanation. We introduce Scientific Explanation-Admissibility Machines (SEAM), a generator-agnostic framework that makes this local-to-global consistency question computable across regions, sensors, regimes, and model components. The finite explanation-sheaf instantiation SEAM-$Ω$ represents each region by a structured explanation with state, closure, and observation channels together with optional contract metadata; compares neighboring explanations on their overlaps; and converts disagreement into a channel-resolved obstruction. This obstruction locates inconsistency and tests competing declared accounts by restricting each repair to the revisions that one account permits. Exact feasibility refutes or retains an account; when exact repair is unavailable, residual-aware regularized records provide a separately labeled empirical attribution. The framework also separates inconsistency from non-identifiability and monitors learned generators under distribution shift. We establish theorems for minimum-cost intervention and conservation-contract detectability, together with companion results for identifiability and closure recoverability. Across nineteen experiments involving synthetic partial differential equation systems and out-of-distribution Fourier neural operator (FNO) monitoring, SEAM detects incompatible explanations even when local predictions are accurate, and attributes failures to specific channels and overlaps. SEAM adds a global explanation-consistency audit to existing solvers and learning models, testing whether their local explanations form a coherent scientific account.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

科学机器学习（Scientific Machine Learning）的现有验证范式存在根本性局限：模型通常仅在子域、基准划分或单次预测的局部层面被检验，例如CFD求解器在特定子域验证、神经算子在测试集上评估、区域回归模型在留出折上测试。这些局部检查无法回答一个关键问题——不同区域的解释能否拼接成一个全局一致的科学解释。论文指出，一组各自局部合理的解释可能在科学上不可采纳：每个部分看似正确，但整体无法粘合为连贯图景。典型场景包括：两个区域PDE求解器各自通过残差测试却在共享边界冲突；季节性模型在各自季节拟合良好却在过渡期矛盾；工业监测系统中漂移传感器导致相邻区域推断出相互矛盾的源项。

现有方法如PINN、cPINN、XPINN虽引入界面兼容性约束，但未将“解释可采纳性”作为独立科学对象系统处理。SEAM框架的核心贡献在于将局部到全局的一致性检验变为可计算问题：通过有限解释层（explanation sheaf）将区域解释结构化，在重叠区域比较相邻解释，将不一致转化为通道分辨的阻碍（obstruction），并支持假设检验式的干预分析——区分传感器漂移、物理缺失、界面校准等竞争性解释，而非简单打分。这解决了“多个解释同时与观测一致时如何判别”的核心难题。

### Q2: 有哪些相关研究？

本文的核心贡献在于提出“解释可容许性”这一科学对象，与现有工作形成显著区别。相关研究主要分为以下几类：

**方法类**：Physics-informed neural networks (PINNs) 将PDE残差嵌入训练损失，universal differential equations 将可训练组件置于微分方程内部，神经算子学习函数空间映射。这些方法关注局部精度，而SEAM审计的是局部解释能否全局粘合。域分解PINN变体（cPINN、XPINN、FBPINN）虽在子域界面施加通量或解相容性，但SEAM进一步将相容性检查扩展到结构化通道（状态、闭合、观测），并支持假设检验式干预。

**应用类**：区域PDE求解器、季节需求模型、工业监控系统、神经算子等均存在局部验证通过但全局不一致的问题。SEAM通过19个实验（含合成PDE系统和分布外FNO监控）证明其能检测局部预测准确时的全局不相容。

**理论类**：与层论一致性方法相比，SEAM整合了命名科学通道、残差感知预算假设评估、可辨识性和流式监控，将局部到全局问题形式化为有限解释层，通过上边界矩阵计算缺陷。

**评测类**：现有基准测试仅评估局部精度，SEAM提供全局解释一致性审计，补充了现有求解器和学习模型的验证工具链。

### Q3: 论文如何解决这个问题？

SEAM通过一个生成器无关的局部到全局一致性审计框架来解决科学机器学习中局部验证无法保证全局解释一致性的问题。其核心是有限解释层（SEAM-Ω）实例化，采用五阶段数据流：生成（Generate）、限制（Restrict）、阻碍（Obstruct）、诊断（Diagnose）和干预（Intervene），并扩展了识别（Identify）与监控（Monitor）功能。

在架构上，每个区域Ui携带结构化局部解释ei=(ui,ci,oi,εi)，包含状态场、闭合参数、观测摘要和可选契约元数据四个通道。重叠区域Uij上定义限制映射ρi,ij，将相邻区域的解释投影到共享比较空间。通过组装所有重叠上的不一致性，构建阻碍对象ω=Ds，其中D是上边缘算子，s是解释向量。当ω=0时，解释族全局可容许；否则，系统通过通道分解定位不一致来源。

关键技术包括：将不一致性分解为命名通道（状态、闭合、观测、元数据），实现通道级归因；干预预算用正交投影算子P表示，硬可行性条件ω∈im(DP)可精确检验科学假设；残差感知正则化记录提供经验归因。框架还区分了不一致性与不可辨识性，并通过监控扩展支持流式ω(t)评估。

创新点在于：将局部验证提升为全局可计算的一致性检查，形式化定义了科学解释的可容许性；通过有限层理论实现闭式诊断与干预算子；能够检测局部预测准确但全局不一致的解释，并归因到具体通道和重叠区域。

### Q4: 论文做了哪些实验？

论文围绕SEAM框架开展了19项实验，覆盖合成偏微分方程（PDE）系统与分布外傅里叶神经算子（FNO）监测两大场景。实验设置采用区域覆盖（cover）构造，通过域分解设定重叠比例，或按时间序列的机制分解设定重叠窗口，并利用通道分解（状态、闭包、观测、元数据）计算局部解释间的邻接不一致性（obstruction）。

数据集方面，合成PDE系统用于验证框架对解释一致性的检测能力，FNO监测则针对训练-测试分布偏移场景。对比方法包括仅依赖局部预测准确性的传统验证方式，以及未引入全局一致性审计的基线模型。

主要结果显示：SEAM即使在局部预测准确的情况下，也能成功检测出不相容的解释，并将失败归因到特定通道（如状态或闭包通道）和重叠区域。关键指标包括最小成本干预定理、守恒契约可检测性、可辨识性与闭包可恢复性等理论结果，以及通道解析的障碍值（如ω_ij = ρ_j,ij s_j − ρ_i,ij s_i）用于量化不一致程度。实验还区分了不一致性与不可辨识性，并监测了学习生成器在分布偏移下的行为，验证了SEAM作为全局解释一致性审计工具的有效性。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从以下几方面展开。首先，SEAM-Ω的线性限制映射和向量空间stalk假设虽便于计算，但难以刻画非线性物理过程或复杂传感器耦合，未来可引入非线性或概率化sheaf结构，以处理更真实的科学模型。其次，当前框架依赖手工设计的限制映射，在覆盖区域动态变化或拓扑复杂时缺乏自适应能力，可探索从数据中学习限制映射或自动构建覆盖的算法。第三，干预预算的设定依赖专家先验，未来可结合因果推断或贝叶斯模型选择，自动生成候选假设并评估其可信度。第四，实验主要基于合成PDE系统，在真实工业故障诊断中，传感器噪声、缺失数据和异构采样率会显著影响obstruction计算，需开发鲁棒性更强的诊断方法。最后，SEAM目前是事后审计工具，未来可将其嵌入在线学习循环，实现“检测-干预-再训练”的闭环，使模型在分布偏移时能主动调整解释结构，而不仅是监控ω(t)。此外，将SEAM与LLM结合，自动生成自然语言形式的故障归因报告，可提升可解释性和人机协作效率。

### Q6: 总结一下论文的主要内容

SEAM提出科学机器学习中一个被忽视的关键问题：局部验证无法保证全局解释的可组合性。论文将“解释可采纳性”定义为局部到全局的一致性——相邻区域的解释必须在重叠部分相互兼容，即使每个区域单独看都高度准确。作者引入生成器无关的SEAM框架，包含Generate、Restrict、Obstruct、Diagnose、Intervene五个阶段，并扩展了可辨识性与流式监控。其有限实现SEAM-Ω利用细胞层论将区域解释编码为状态、闭包、观测和元数据通道，通过上边缘算子计算障碍ω，将不一致性分解到具体通道和重叠区域。干预阶段通过预算化修复检验竞争性科学假说：只有允许的修订能消除全部障碍的假说才存活，否则被反驳并留下不可约残差。19项实验表明，SEAM能在局部预测准确时检测出不相容解释，并将故障归因于特定通道，为现有求解器和学习模型补充了全局解释一致性审计能力。
