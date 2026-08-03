---
title: "Rehearse: Stepping Back from the Confidence Cliff in Self-Improving Autoresearch"
authors:
  - "Jiazhen Ji"
  - "Shouhong Ding"
date: "2026-07-30"
arxiv_id: "2607.27687"
arxiv_url: "https://arxiv.org/abs/2607.27687"
pdf_url: "https://arxiv.org/pdf/2607.27687v1"
categories:
  - "cs.AI"
tags:
  - "LLM Agent"
  - "自进化"
  - "反思"
  - "记忆"
  - "时间序列预测"
  - "自动研究"
  - "置信度评估"
  - "工具调用"
relevance_score: 7.5
---

# Rehearse: Stepping Back from the Confidence Cliff in Self-Improving Autoresearch

## 原始摘要

Autoresearch improves machine-learning code by proposing changes, running full training jobs, and keeping changes that improve the metric. The efficiency of this loop depends not only on generating ideas, but also on the agent's ability to decide, before spending a training run, whether a proposed modification is likely to work. We study how the reliability of this pre-execution judgment changes over the course of an autoresearch trajectory. In public AutoSOTA logs (Li et al., 2026; Tsinghua FIB Lab, 2026), the fraction of helpful modifications falls from 70% in the first two iterations to 43% by iteration 6+. On 296 same-baseline modification pairs from 39 paper-derived AutoSOTA tasks, each containing one modification that improved the metric and one that did not, with measured outcomes hidden, an LLM judge given candidate rationales but no prior-attempt history reaches 79.5% accuracy on the pairs where strict consensus returns a verdict. On the full 366-pair benchmark, however, this ability weakens substantially late in the loop. As successful changes accumulate, selective accuracy - accuracy conditioned on a strict-consensus verdict - falls from 82.8% to 56.9%, while the judge remains willing to decide. We call this operational pattern the confidence cliff. Rehearse implements the loop change as a lightweight skill for autoresearch loops: propose several ideas, compare them before execution, run the most promising, and judge with a focused memory of similar past attempts and outcomes. This focused outcome memory raises late selective accuracy to 83.5%. Across 4,000 budgeted training runs over three loops, Rehearse improves the endpoint under the same training-run budget on nanochat, image classification, and time-series forecasting.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文聚焦于“自动研究”（Autoresearch）系统中智能体改进机器学习代码的效率问题。研究背景是：智能体通过提出修改、运行完整训练任务并保留有效改动来迭代优化，但这一循环高度依赖训练预算，而无效修改会浪费大量计算资源。

现有方法的不足在于：以往研究主要关注如何生成更多改进想法，却忽视了智能体在执行训练前对候选修改进行预判的能力。公共AutoSOTA日志显示，随着循环深入，有效修改的比例从初期70%骤降至43%，且收益大幅缩水。更关键的是，智能体的预执行判断能力会随累积成功次数增加而急剧退化——选择性准确率从82.8%跌至56.9%，但判断意愿却未下降，形成所谓的“置信度悬崖”（confidence cliff）。这种晚期判断失灵导致大量训练预算被浪费在注定失败的修改上。

本文要解决的核心问题是：如何在自动研究循环中维持智能体对候选修改的预执行判断可靠性，避免晚期判断退化。为此，作者提出Rehearse技能，通过“提出多个候选→执行前比较→仅运行最有希望的→用聚焦的相关历史结果辅助判断”这一轻量级机制，将晚期选择性准确率恢复至83.5%，并在有限训练预算下显著提升三个不同任务（nanochat、图像分类、时间序列预测）的最终性能。

### Q2: 有哪些相关研究？

相关研究主要分为三类。**方法类**中，AIDE将ML工程建模为带评分的解树搜索，FunSearch/AlphaEvolve等进化方法维护程序档案并变异生成候选，Aster和Bilevel Autoresearch聚焦迭代效率，MLR-Copilot在执行前规划但依赖外部研究工件。**评测类**包括MLE-Bench等ML工程基准，以及LLAMBO等贝叶斯优化/AutoML系统在数值配置空间中选择实验。**最接近的工作是ForeAgent**，它在执行前比较完整实例化的ML方案代码，并用置信度门控的成对过滤决定验证候选，但其离线语料在任务内穷举重组完整工作流，判断的是"哪个完整方案更好"；Rehearse则比较共享同一基线的待定增量提案（描述、假设、实现计划），研究"下一步哪个修改值得运行"，并揭示判断准确率随接受改进累积而下降的深度索引可靠性曲线。**记忆与自改进类**包括Generative Agents、MemGPT、Voyager、Reflexion等，它们存储经验但未用于门控训练运行；EvoScientist和AutoResearchClaw蒸馏历史经验，但Rehearse更窄地记录具体候选-结果对，在付费训练前读取。与自我微调方法不同，Rehearse保持代理权重和源码固定，仅改变循环的选择与记忆机制。

### Q3: 论文如何解决这个问题？

论文通过引入“Propose–Predict–Execute”循环和“聚焦结果存储”来解决自改进自动研究中的“置信度悬崖”问题。整体框架将传统的一次一想法-运行循环改造为多候选生成、执行前排序、仅运行最优候选的流程。

核心架构包含两个关键组件：**预测操作**和**聚焦结果存储**。预测操作采用成对锦标赛机制，由LLM法官在共享任务上下文（目标论文/代码库摘要、目标指标、基线状态）下比较两个候选修改，每个候选携带描述、假设（机制性理由）、实现字段和粗略类型。为缓解位置偏差，每对候选以两种顺序呈现，仅在严格共识下计票，分歧则双方不得票，按票数排序后仅运行前k个候选（实验中k=1）。

聚焦结果存储记录已执行尝试，检索时限制为同任务、当前步骤之前、余弦相似度≥0.40的过往尝试，每条序列化为单行（变更内容+二元结果），避免完整历史造成的噪声。检索到的先例可改变成对投票或降权类似已耗尽方向的候选。

创新点在于：将比较从隐式变为显式外部化，用推理成本替代训练成本；假设通道使法官能评估机制而非仅编辑内容（消融显示移除假设和实现字段导致最大性能下降）；选择性记忆而非全量历史，显著提升后期选择性准确率至83.5%。Rehearse作为轻量技能封装，无需微调或修改目标训练代码，仅替换控制器决策策略并添加文件存储，在4,000次预算训练运行中持续改善nanochat、图像分类和时间序列预测的端点性能。

### Q4: 论文做了哪些实验？

论文围绕“预执行判断”在自动研究循环中的可靠性展开实验，分为单轮基准测试和多轮实时循环评估两部分。

**单轮基准测试**：基于39个论文衍生AutoSOTA任务的366对候选修改（296对类型1：一成一败；70对类型2：双成但幅度不同），采用严格共识（双序一致才判定）评估。对比无记忆、全历史转储、自反思缓冲、LLM摘要和Rehearse（聚焦检索）五种记忆形式。结果显示：无记忆时整体选择性准确率77.6%，但在深度决策（≥3次成功积累）上从82.8%骤降至56.9%，且判定覆盖率反升至85%，形成“置信度悬崖”。Rehearse在悬崖桶上达83.5%选择性准确率（覆盖率77%），显著优于全历史转储（70.8%）、自反思（74.1%）和LLM摘要（80.9%）。消融实验表明，移除候选理由、想法文本或聚焦检索均使准确率降至约70%，而添加失败原因反而有害（降至80.6%）。

**多轮实时评估**：在nanochat（100次实验，5种子）、CIFAR-10和ETTh1三个循环上共运行4000次预算训练。nanochat上Rehearse终点改进10.7%，优于vanilla（7.1%）、propose-many（6.9%）和select（8.4%）。CIFAR-10上Rehearse提升2.85% vs vanilla 2.10%；ETTh1上MSE降低54.0% vs 40.1%，且Rehearse在9/10种子中领先，并分别节省46%和37%的实验次数。

### Q5: 有什么可以进一步探索的点？

论文的局限性为后续探索提供了多个切入点。首先，当前证据仅覆盖三个可量化结果的循环，且单次配置平均仅五次种子，未来可扩展至更大规模种子实验，并纳入以新颖性或论文评分为导向的系统，以检验方法的泛化性。其次，Rehearse仅从提议者生成的候选中选择，未测试其他记忆形式（如结构化知识图谱或反思性摘要）及不同候选数量对效果的影响，这为优化“广度-选择-记忆”的交互提供了空间。此外，置信悬崖现象表明，随着成功修改累积，判断准确性下降，未来可探索动态调整判断策略——例如在循环后期引入不确定性估计或主动降低决策阈值，甚至结合元认知机制让智能体识别自身“知识饱和”点并主动切换搜索策略。最后，当前预算仅统计训练运行次数，未计入提议生成与判断的计算成本，未来可构建更全面的成本模型，并研究如何通过分层筛选或代理模型减少昂贵训练前的判断开销。

### Q6: 总结一下论文的主要内容

本文研究自动研究（Autoresearch）循环中“执行前判断”的可靠性随轨迹深度变化的问题。作者发现，随着成功修改的累积，判断器的选择性准确率从冷启动时的82.8%骤降至56.9%，而覆盖率反而上升，形成“置信度悬崖”。基于39个论文衍生任务构建的366对结果标注基准，无记忆判断器在严格共识对上的准确率仅79.5%，且后期显著退化。为此，提出Rehearse技能：先提出多个候选方案，执行前比较筛选，仅运行最有希望的方案，并利用聚焦的相关历史结果记忆辅助判断。该机制将后期选择性准确率提升至83.5%。在4000次预算训练运行中，Rehearse在nanochat、图像分类和时间序列预测三个循环上均以相同预算取得更优终点。核心贡献在于系统刻画了自动研究中的判断退化现象，并验证聚焦记忆可有效缓解该问题。
