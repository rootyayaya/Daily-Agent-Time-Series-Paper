---
title: "A Fuzzy Rule-based Neuro-Symbolic Approach for Pipe Severity Prediction in Sewer Networks"
authors:
  - "Ngoc Thai Le"
  - "Thanh Ma"
  - "Umberto Straccia"
date: "2026-07-30"
arxiv_id: "2607.28481"
arxiv_url: "https://arxiv.org/abs/2607.28481"
pdf_url: "https://arxiv.org/pdf/2607.28481v1"
categories:
  - "cs.AI"
tags:
  - "neuro-symbolic reasoning"
  - "fuzzy logic"
  - "sewer pipe severity prediction"
  - "interpretable classification"
  - "Swin Transformer"
  - "decision tree to rules"
  - "LLM for label generation"
  - "imbalanced classification"
  - "traceable reasoning"
relevance_score: 7.5
---

# A Fuzzy Rule-based Neuro-Symbolic Approach for Pipe Severity Prediction in Sewer Networks

## 原始摘要

Standard automated sewer pipe severity assessment relies on direct image classification, creating a "black box" where the link between visual defects and final severity scores remains implicit. This study introduces a modular, fuzzy rule-based neuro-symbolic framework that bridges this gap by decoupling neural perception from symbolic reasoning. The perception module utilizes a Swin Transformer to predict 14 multilabel inspection CODE degrees directly from images. For reasoning, a DT, specifically Weka's J48, algorithm is trained on ground-truth CODEs and severity labels, and its paths are converted into 19 fixed IF--THEN rules. Inference operates via fuzzy logic: t-norm activations from CODE conditions are weighted by rule confidence and combined with corresponding s-norms to produce interpretable class evidence. We assessed Product, Łukasiewicz, and Hamacher operator pairs using a dataset of 3,244 images spanning five highly imbalanced severity classes. Ground-truth labels were robustly generated via consensus from five independent large language models analyzing original inspector notes. Our results show an improvement of accuracy, balanced accuracy, Macro F1 and MCC by 17.9%, 12.2%, 23.0%, and 17.3%, respectively, over image-only based classification.
  Overall, the framework combines competitive class-balanced performance with traceable reasoning from predicted CODE degrees to rule supports and severity evidence.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

sewer networks are critical urban infrastructure, and their deterioration can lead to hydraulic failures, blockages, and costly emergencies. Regular inspection and reliable condition assessment are therefore essential for maintenance planning and rehabilitation prioritization. In practice, inspectors first identify standardized defect CODEs from visual observations and then determine the overall severity according to guidelines, meaning severity assessment is a reasoning process over intermediate defect semantics rather than a direct visual classification task.

However, most existing deep learning approaches formulate pipe severity prediction as a direct image-to-severity classification problem. This creates a "black box" where the link between visual defects and final severity scores remains implicit. Such models may achieve good predictive performance but fail to explicitly represent the defect-level reasoning process, making it difficult to explain predictions or verify which defect evidence supports a particular maintenance recommendation. Additionally, sewer inspection images suffer from low illumination, blur, occlusion, and high class imbalance, further complicating the task.

To address these limitations, this paper proposes a fuzzy rule-based neuro-symbolic framework that decouples neural perception from symbolic reasoning. It introduces defect CODEs as an intermediate semantic representation between raw images and severity classes, enabling transparent, traceable severity inference through explicit IF-THEN rules. The core problem is to achieve competitive predictive performance while providing interpretable reasoning that links visual evidence to severity decisions.

### Q2: 有哪些相关研究？

相关研究可分为以下几类：

**方法类**：早期工作采用特征工程与神经模糊分类器识别管道缺陷（如裂缝、孔洞），但仅关注缺陷识别；深度学习方法中，Kumar等用CNN集成识别多缺陷类型，Li等引入层次分类处理类别不平衡，Hassan等构建卷积框架进行缺陷分类与状态评估。本文与这些工作的区别在于，它们将缺陷证据与最终严重度决策隐含在端到端模型中，而本文显式解耦感知与推理。

**应用类**：Sewer-ML数据集推动多标签缺陷识别，Cross-Task GNN联合预测缺陷、水位等任务间关系；Wang和Zhou等通过缺陷定位、分割和几何测量量化严重度。这些方法依赖可测量的缺陷范围，而本文针对从标准化CODE组合推断单一严重度类别的场景，且不依赖几何信息。

**评测与解释类**：概念瓶颈模型（CBM）暴露中间变量，但下游映射仍可能是统计性的；神经符号系统（如NeurASP、Logic Tensor Networks）通常采用端到端可微推理或联合学习。本文采用模块化设计：神经网络预测CODE度，规则库从真实标签中独立提取并固定，不参与训练。模糊推理方面，Chae和Abraham及后续神经模糊分类器虽有先例，但未结合现代多标签CODE预测与显式可追踪的严重度规则库。

综上，本文首次将多标签CODE识别、CODE到严重度的可解释映射、以及模糊传播三者联合，填补了现有研究空白。

### Q3: 论文如何解决这个问题？

该论文提出了一种模块化的模糊规则神经符号框架，将管道缺陷严重性预测分解为两个可解释的阶段：神经感知和符号推理。

**整体框架**包含离线规则库构建和在线图像推理两个阶段。离线阶段使用Weka的J48决策树算法，基于真实缺陷CODE标注和严重性标签训练分类器，将每条根到叶路径转换为IF-THEN规则，共提取19条固定规则，涉及14种缺陷CODE条件，每条规则附带基于叶节点样本分布计算的置信度。在线阶段采用Swin Transformer作为多标签视觉感知模块，通过sigmoid输出预测14个缺陷CODE的模糊隶属度向量，再输入符号规则库进行推理。

**核心推理机制**采用模糊逻辑：每个规则条件根据CODE预测值计算满足度（正条件用预测值，负条件用1-预测值），通过t-norm算子计算规则激活度，乘以规则置信度得到加权支持度，最后用s-norm算子按严重性类别聚合所有规则证据，选择聚合度最高的类别作为预测结果。论文比较了Product、Łukasiewicz和Hamacher三种模糊算子对。

**创新点**在于：(1) 将黑盒图像分类解耦为可解释的缺陷语义层和规则推理层；(2) 利用多LLM共识协议从检查员笔记生成可靠的严重性标签；(3) 通过模糊逻辑实现从视觉特征到规则证据的平滑推理，在保持竞争性能的同时提供完整的决策追踪链。实验表明该方法相比纯图像分类在准确率、平衡准确率、Macro F1和MCC上分别提升17.9%、12.2%、23.0%和17.3%。

### Q4: 论文做了哪些实验？

实验使用法国某排水管道检测项目 proprietary 数据集，共3,244张图像，按2592/326/326划分训练/验证/测试集，严重度分为5类且高度不平衡（类1占2109张，类5仅57张）。严重度标签由5个独立大语言模型对检查员文本描述进行共识投票生成，未使用CODE标注。

对比方法包括：图像直接分类基线（Swin Transformer→严重度）、提出的多标签+模糊规则框架（Swin Transformer预测14个CODE→固定规则推理）、以及Oracle CODE+规则上界（使用真实CODE标注）。规则库由J48决策树在训练集提取19条IF-THEN规则，采用Product、Łukasiewicz、Hamacher三种模糊算子对，并比较软度模式和9个阈值（0.1-0.9）的推理模式。

结果显示，相比图像直接分类，提出的框架在准确率、平衡准确率、Macro F1和MCC上分别提升17.9%、12.2%、23.0%和17.3%，在保持可解释性的同时实现了竞争性的类平衡性能。Oracle实验表明主要瓶颈在神经CODE预测而非规则推理。

### Q5: 有什么可以进一步探索的点？

论文在多个方面仍有探索空间。首先，规则提取仅依赖单一决策树（J48），可尝试RIPPER、Fuzzy ID3或基于进化算法的规则学习，以生成更紧凑且覆盖度更高的规则集，并对比不同规则提取方法对推理可解释性和性能的影响。其次，当前规则库在提取后固定不变，缺乏与神经感知模块的联合优化；可引入端到端的可微模糊推理层，使规则置信度或隶属函数参数能随训练数据微调，从而在保持可解释性的同时提升适应性。第三，模糊算子仅测试了三种固定组合，未来可探索自适应算子选择机制，或根据类别不平衡动态调整t-norm/s-norm的权重。此外，多LLM共识生成标签虽提升了标注质量，但未分析LLM间分歧对规则提取的潜在偏差，可设计不确定性量化框架来过滤低置信度样本。最后，当前方法仅处理单张图像，可扩展至视频序列或相邻管段的多帧信息，利用时间上下文增强缺陷CODE预测的鲁棒性，并进一步验证规则在不同管道材质、环境条件下的泛化能力。

### Q6: 总结一下论文的主要内容

该论文提出了一种模糊规则神经符号框架，用于污水管道严重程度预测。传统方法直接从图像分类得到严重等级，形成“黑箱”过程，缺乏视觉缺陷与最终评分间的显式关联。该框架将神经感知与符号推理解耦：感知模块采用Swin Transformer预测14种多标签缺陷CODE等级；推理模块使用Weka J48决策树从真实CODE与严重标签中提取19条固定IF-THEN规则，并通过模糊逻辑（t-norm激活、规则置信度加权、s-norm聚合）生成可解释的类别证据。实验基于3,244张图像、五个高度不平衡的严重类别，利用五个大语言模型共识生成真实标签。结果显示，相比纯图像分类，准确率、平衡准确率、Macro F1和MCC分别提升17.9%、12.2%、23.0%和17.3%。该框架在保持竞争性分类性能的同时，实现了从预测CODE到规则支持再到严重证据的可追踪推理，为工程师提供了透明、可验证的维护决策支持，且模块化设计便于适应不同视觉骨干或检测标准。
