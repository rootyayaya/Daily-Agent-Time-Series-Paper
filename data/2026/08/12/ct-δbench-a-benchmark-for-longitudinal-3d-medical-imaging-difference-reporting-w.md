---
title: "CT-$Δ$Bench: A Benchmark for Longitudinal 3D Medical Imaging Difference Reporting with Vision-Language Models"
authors:
  - "Kegeng Tang"
  - "Jingbo Wang"
  - "Shaogang Ren"
  - "Zihao Wang"
date: "2026-08-12"
arxiv_id: "2608.11534"
arxiv_url: "https://arxiv.org/abs/2608.11534"
pdf_url: "https://arxiv.org/pdf/2608.11534v1"
categories:
  - "cs.CL"
  - "cs.CV"
tags:
  - "medical imaging"
  - "longitudinal comparison"
  - "difference reporting"
  - "vision-language model"
  - "benchmark"
  - "temporal reasoning"
relevance_score: 6.5
---

# CT-$Δ$Bench: A Benchmark for Longitudinal 3D Medical Imaging Difference Reporting with Vision-Language Models

## 原始摘要

In medical imaging, the clinical value of Computed Tomography (CT) lies not only in depicting current disease status, but crucially in enabling longitudinal comparison of serial scans to determine disease evolution, a process that underpins response assessment, recurrence detection, and ongoing patient management. Yet, despite this central role of temporal comparison in clinical decision-making, existing medical foundation models remain largely confined to single-study understanding, leaving temporally grounded cross-examination insufficiently addressed. To address this gap, we study longitudinal imaging difference reporting, a task in which a model takes two temporally separated scans from the same patient and generates a clinically meaningful report describing interval changes between them. We introduce CT-$Δ$Bench, a dedicated benchmark for this task with patient-level splitting to prevent information leakage. To better evaluate this task beyond surface-level text similarity, we further develop change-aware metrics specifically designed to capture clinically meaningful longitudinal changes, and conduct an independent physician validation to assess the reliability of the synthesized references and event extraction pipeline. We also compare direct paired-CT reasoning with an indirect two-stage pipeline that first generates single-timepoint reports and then performs textual differencing. Finally, we propose DeltaMed, a baseline model for direct paired-CT difference reporting, and train it on the benchmark training set. Together, these contributions lay the groundwork for temporally aware medical foundation models that better reflect real-world longitudinal clinical reasoning.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

医学影像中CT的临床价值不仅在于描述当前病灶，更在于通过纵向比较系列扫描来评估疾病演变，这对疗效评估、复发检测和患者管理至关重要。然而，现有医学基础模型和CT报告生成研究大多局限于单次影像理解，缺乏对时间配对扫描的直接推理能力，导致纵向跨影像对比这一核心临床任务未被充分解决。此外，纵向CT差异报告面临计算成本高、解剖对应不完美、细微变化易遗漏以及生成文本易出现幻觉等挑战，传统基于文本相似度的评估指标也无法捕捉临床意义上的变化。为此，本文提出CT-ΔBench基准，通过患者级数据划分防止信息泄漏，并开发变化感知评估指标及独立医生验证，系统性地研究直接配对CT推理与间接两阶段文本差分两种范式，最终提出基线模型DeltaMed，旨在推动时间感知医学基础模型的发展，使其更贴近真实临床纵向推理需求。

### Q2: 有哪些相关研究？

在相关研究方面，本文首先与自动医学报告生成领域紧密相关，尤其是基于X光胸片的数据集（如IU X-Ray、MIMIC-CXR、CheXpert）和图像到文本模型。早期方法多采用通用图像描述架构，后续工作强调长文本生成、视觉-文本对齐和临床事实一致性，但大多局限于单次检查（single-study）的生成，未显式建模跨时间的患者内关系。本文区别于这些方法，聚焦于成对CT扫描的纵向差异报告，而非单次检查的描述。

其次，在纳入时间上下文的工作中，如Longitudinal-MIMIC利用既往X光和报告辅助当前报告撰写，BioViL-T建模图像-报告序列的时间结构，MAIRA-2在生成中引入既往检查作为上下文。这些方法仍以“当前检查报告”为框架，将历史数据作为辅助信息，而非直接生成以总结间隔变化为核心的差异报告，且多限于2D影像。本文则强调直接成对CT推理，并以差异报告为主要输出。

在数据集与基准方面，CT-RATE、RadBench、M3D-Bench等扩展了3D影像和多模态交互，但主要评估单次研究的描述、分类或问答，缺乏跨时间点的差异报告任务。本文提出的CT-$Δ$Bench填补了这一空白，采用患者级划分防止信息泄漏，并开发了变化感知指标。

在评估方法上，传统词法指标（BLEU、ROUGE）与临床正确性相关性差，后续工作如CheXbert、RadGraph、RadCliQ和GREEN转向事实和临床意义的评估。本文继承了这一趋势，但专门针对纵向变化设计指标，并通过医生验证确保参考报告和事件提取的可靠性。

### Q3: 论文如何解决这个问题？

该论文通过构建专用基准和提出基线模型，系统性地解决了纵向3D医学影像差异报告任务中缺乏评估基准和有效方法的问题。核心贡献包括三个方面：

**基准构建**：基于CT-RATE数据集，筛选同一患者不同时间点的两次CT扫描形成配对样本，利用Gemini-2.5-Flash从原始报告中提取Findings和Impression部分，生成结构化的差异参考报告（包含Difference Findings和Difference Impression）。采用患者级划分防止信息泄漏，训练集2638对、验证集169对。为确保合成数据可靠性，邀请两位独立医生进行临床验证，结果显示参考报告可接受性达4.82/5，事件提取正确率4.83/5。

**评估体系**：提出双轨评估机制。文本层面使用ROUGE-L、BERTScore和BLEURT衡量表面相似性；事件层面设计五类可解释变更标签（New/Resolved/Increased/Decreased/Stable），通过Qwen2.5-14B提取原子变更事件，计算Change-F1、Missing Rate、Hallucination Rate和Change Type Accuracy四个指标，精确捕捉临床意义上的纵向变化。

**DeltaMed模型**：采用双分支视觉语言架构，使用共享权重的MedSigLIP编码器分别处理前后两次CT，显式构造差分分支（z_t2 - z_t1）编码时间变化，将三个特征流拼接后经轻量融合模块（线性投影+归一化）输入Gemma 3 4B生成报告。训练时仅更新融合模块和LoRA适配器，冻结视觉编码器和基础语言模型，实现参数高效微调。该设计直接进行配对CT联合推理，避免了间接两阶段方法的信息损失。

### Q4: 论文做了哪些实验？

论文在CT-ΔBench基准上开展了三类实验。首先，零样本评估了五个医学视觉语言模型（MedGemma-1.5-4B、M3D-LaMed-Phi-3-4B、RadFM-13B、Med3DVLM-Qwen2.5-7B、Merlin-RadLLaMA-7B）直接处理配对CT的能力，结果显示所有模型在变化感知指标上表现极差，Change-F1仅0至0.0175，其中RadFM完全失败（Change-F1=0），即使最优的MedGemma也仅达0.0175，且缺失率高达0.9849，表明现有模型难以正确识别临床时间变化。

其次，测试了两阶段流程（先分别生成单次CT报告，再进行文本差分），结果好坏参半：RadFM和Med3DVLM的Change-F1分别提升至0.0542和0.0614，但Merlin-RadLLaMA反而降至0，说明中间报告的错误传播会损害最终结果。

最后，在1%、10%、100%三种训练数据比例下对DeltaMed和MedGemma基线进行LoRA微调。DeltaMed在所有数据规模下均优于基线，例如1%数据时Change-F1从0.001提升至0.091，100%时达0.198（对比MedGemma的0.158），且缺失率和幻觉率更低，验证了其更强的纵向变化理解归纳偏置。实验使用ROUGE-L、BERTScore、BLEURT及Change-F1、缺失率、幻觉率、变化类型准确率等指标，在两张80GB A100 GPU上完成。

### Q5: 有什么可以进一步探索的点？

当前工作仍存在若干可拓展方向。首先，CT-ΔBench仅基于CT模态，未来可引入MRI、PET等多模态影像，并联合结构化电子病历（如病理报告、用药记录）构建多源异构的时序推理基准，更贴近真实临床决策。其次，DeltaMed的差分分支依赖显式特征相减，对非线性形变（如肿瘤不规则生长）敏感度有限，可探索基于可变形配准或隐式神经场（NeRF）的时序对齐模块，提升对细微病灶变化的捕捉能力。第三，现有事件级指标仍依赖预定义事件类型，未来可设计开放式事件抽取与语义验证机制，结合大语言模型进行自由文本的临床合理性校验。此外，当前模型缺乏对扫描间期（如3个月vs. 1年）的先验建模，可引入时间间隔编码器或生存分析损失，使模型感知时间尺度对变化幅度的影响。最后，可探索主动学习策略，让模型在低标注资源下优先选择信息量最大的CT对进行人工复核，缓解医学标注瓶颈。

### Q6: 总结一下论文的主要内容

本文提出了CT-ΔBench基准，聚焦纵向3D医学影像差异报告任务，即模型需输入同一患者两次不同时间的CT扫描，生成描述期间临床变化的报告。现有医学基础模型多局限于单次影像理解，缺乏时间维度推理能力。作者构建了患者级划分的基准以避免信息泄漏，并设计了能捕捉临床意义变化的评估指标，经独立医生验证确保参考报告与事件提取的可靠性。研究对比了直接配对CT推理与先生成单时间点报告再文本差异化的两阶段流程，并提出基线模型DeltaMed，通过配对推理与差异分支显式建模时间变化。实验表明，现有模型在此任务上表现不足，尤其在事件级变化正确性上；DeltaMed在多种微调设置下，尤其监督有限时，事件级检测优于直接配对CT的MedGemma基线。该工作为时间感知医学基础模型提供了清晰任务定义、可复现评估框架与强基线，推动纵向临床推理研究。
