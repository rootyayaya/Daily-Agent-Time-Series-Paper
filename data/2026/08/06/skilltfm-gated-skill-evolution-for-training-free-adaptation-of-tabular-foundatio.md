---
title: "SkillTFM: Gated Skill Evolution for Training-Free Adaptation of Tabular Foundation Models"
authors:
  - "Yi He"
  - "Zhengkang Guan"
  - "Anpeng Wu"
  - "Peng Cui"
  - "Fei Wu"
  - "Kun Kuang"
date: "2026-08-06"
arxiv_id: "2608.06137"
arxiv_url: "https://arxiv.org/abs/2608.06137"
pdf_url: "https://arxiv.org/pdf/2608.06137v1"
categories:
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "Tabular Foundation Models"
  - "Skill Evolution"
  - "Gated Skill"
  - "Training-Free Adaptation"
  - "Boundary Evidence"
  - "Electricity Price Forecasting"
  - "Reusable Skills"
  - "Verification"
relevance_score: 7.5
---

# SkillTFM: Gated Skill Evolution for Training-Free Adaptation of Tabular Foundation Models

## 原始摘要

Tabular data are ubiquitous in real-world applications and are crucial for data-driven prediction and decision-making across science, industry, finance, healthcare, and public services. Tabular foundation models (TFMs) have emerged as a promising paradigm for general-purpose tabular learning, offering reusable predictors across diverse datasets and substantially reducing the need for task-specific training, tuning, and model development. However, their practical deployment remains constrained by distribution shifts, heterogeneous feature semantics, and task-specific patterns that are difficult to capture without costly fine-tuning or additional labeled data.
  To this end, we propose SkillTFM, a training-free system that shifts TFM adaptation from parameter updates to the gated evolution of agentic skills. The core of SkillTFM is a verifiable and extensible skill bank that couples boundary evidence identification with gated skill evolution: the former characterizes task structure and base-model failure patterns, whereas the latter retrieves and extends reusable skills subject to explicit validation. Across simulated boundary settings and real-world electricity-price forecasting, SkillTFM improves AUC by 0.128--0.142, raises nonlinear-boundary AUC from 0.699 to 0.898. Furthermore, experiments across TFM backbones demonstrate the effectiveness and generality of SkillTFM.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

表格数据在科学、金融、工业等领域广泛存在，但传统建模需针对每个数据集进行特定选择、调参和预处理。表格基础模型（TFM）虽能作为通用预测器减少任务特定训练，但在实际部署中面临分布偏移、特征语义异质和任务特定模式等挑战，直接使用会产生系统性边界错误。现有方法如固定预处理、规则修复或校准，往往将修复视为默认动作，可能对基础模型已可靠的任务造成不必要的干预，且难以适应复杂非线性结构。

本文核心问题是：如何在不进行训练或依赖额外标注数据的前提下，让TFM自适应地扩展其可用边界，仅在证据充分时进行选择性修复，同时避免对可靠预测的破坏。为此提出SkillTFM，一种无训练自适应系统，将参数更新转变为技能的门控演化。它通过可验证的技能库提取边界证据，经运行时证书验证后决定是否执行修复，否则回退至基础预测，从而实现安全、可控且可迁移的TFM边界扩展。

### Q2: 有哪些相关研究？

表格基础模型（TFMs）与边界修复方面，相关工作包括先验数据拟合网络（如TabPFN）、上下文学习器、超网络预测器，以及针对架构扩展、结构感知、真实数据预训练和稳定性/因果性优化的变体。鲁棒表格学习研究则聚焦类别不平衡、缺失值、标签噪声、分布外检测和校准预测集。这些工作通常引入新骨干网络或固定流程，而SkillTFM将修复视为证据条件化动作，通过外部技能状态实现执行、回退或拒绝，而非依赖单一机制。

技能学习与验证门控更新方面，近期研究涉及智能体技能库、记忆复用、自进化智能体及经验性分析，相关系统利用工具、反思和体验记忆，提示/程序优化将文本或模块视为可修订对象。然而，这些方法多绑定特定LLM和领域问题，跨模型迁移性有限。SkillTFM将技能适应引入表格基础模型，以即插即用方式连接不同TFM骨干和LLM技能提议器，通过门控更新维护外部表格修复状态，仅接受显式验证通过的候选技能，从而区别于现有语言智能体或提示级方法。

### Q3: 论文如何解决这个问题？

SkillTFM将表格基础模型的免训练适配问题形式化为“证据条件下的边界扩展决策”，核心思想是将模型适配从参数更新转变为智能体技能的门控演化。整体框架由两大部分构成：下部是运行时推理系统，上部是技能演化闭环。

在运行时，系统首先通过证据提取模块从当前任务和基模型行为中抽取多维信号，包括分布变化、标签-特征关系、预测偏差、趋势周期性、缺失模式和扰动敏感性等，形成证据向量z_T。随后，修复技能库根据证据激活候选技能，每个技能声明适用条件和禁忌条件，只有同时满足才进入候选集。候选技能经过可审计的排序元组（包含证据支持度、历史可靠性、执行风险、记忆约束和干预成本）进行字典序排序，再由运行时证书逐一扫描：证据充分、风险可接受、未被历史拒绝路线阻止且目标对齐的技能才被认证执行，否则回退到基模型预测。

技能演化方面，每次执行产生完整轨迹，轨迹生成候选编辑（可修改技能库、证据规则、排序规则、风险守卫等），但必须通过晋升门验证：在选拔任务上能力提升达到阈值、在守卫任务上伤害率低于限制、通过回归审查和格式校验，才能更新部署状态。被拒绝的编辑作为约束存入技能记忆，影响未来决策。创新点在于将修复有效性视为证据区域相关的局部属性而非全局属性，通过验证门控实现安全边界扩展，并利用历史失败经验约束未来演化。

### Q4: 论文做了哪些实验？

SkillTFM围绕四个问题展开实验。在受控边界基准上，采用TabPFN、TabICL、TabDPT和LimiX作为基座模型，覆盖不稳定依赖、分布偏移、缺失、不平衡、标签噪声、高维干扰和非线性结构等边界条件，报告AUC、AUC提升、伤害率和回退率。结果显示，在留出、混合和生成器/严重度三种设置下，SkillTFM将AUC从0.644-0.697提升至0.772-0.832，提升0.128-0.142，且零伤害。消融实验表明，移除证据条件检索使AUC降至0.736、回退率升至63.3%；移除运行时证书则伤害率达0.087；完整系统AUC为0.817。在非线性边界上，技能进化将AUC从0.699提升至0.898。跨基座模型迁移实验中，四个模型的AUC提升为0.139-0.148，回退率保持在0.425-0.463。跨优化器测试中，Qwen、Gemini和Claude均生成合规编辑但未被提升。在真实电力价格预测中，SkillTFM将整体MAE从53.02降至25.16，覆盖83.4%的大误差点，激活率38.2%，零伤害。

### Q5: 有什么可以进一步探索的点？

SkillTFM的核心局限在于其“训练-free”特性本质上受限于预定义技能库的覆盖范围。当前方法依赖边界证据识别来触发技能检索，但若遇到未建模的边界族（如非平稳分布漂移、跨域特征组合或对抗性扰动），系统仍可能失效。未来可探索以下方向：一是引入在线技能生成机制，利用LLM的推理能力动态构造新技能，并通过元验证器在少量标注数据上快速评估其有效性，从而突破静态技能库的瓶颈；二是将技能演化从离散门控扩展为连续加权混合，允许不同技能按任务上下文自适应组合，提升对复杂边界的表达能力；三是结合可解释性分析，将技能选择过程映射为人类可理解的规则或因果图谱，增强工业场景下的可信度；四是探索跨任务技能迁移的泛化边界，研究如何从历史任务中抽象出可复用的元技能，减少对验证数据的依赖。此外，当前验证门控依赖回归检查，可引入不确定性量化或校准误差作为额外门控信号，以应对标签噪声场景。

### Q6: 总结一下论文的主要内容

SkillTFM提出了一种无需训练的表格基础模型（TFM）自适应方法，核心创新在于将模型适配从参数更新转变为“门控技能演化”的智能体技能状态。该方法针对TFM在实际部署中因分布偏移、特征语义异质和任务特定模式导致的性能退化问题，构建了一个可验证且可扩展的技能库。该技能库通过边界证据识别刻画任务结构和基础模型失败模式，并采用门控技能演化机制，在显式验证下检索和扩展可复用技能。实验表明，在模拟边界设置和真实电价预测任务中，SkillTFM将AUC提升0.128至0.142，非线性边界AUC从0.699提升至0.898，并在多种TFM骨干网络上验证了其有效性和通用性。该研究的意义在于，通过外部技能状态而非参数更新实现选择性干预，既扩展了TFM的能力边界，又保持了干预的谨慎性，为无标注场景下的表格学习提供了新范式。
