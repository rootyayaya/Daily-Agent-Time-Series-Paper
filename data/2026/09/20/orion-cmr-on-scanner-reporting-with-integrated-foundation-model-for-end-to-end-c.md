---
title: "ORION-CMR: On-scanner Reporting with Integrated Foundation Model for End-to-End Cardiac MRI Analysis and Interpretation"
authors:
  - "Omer Burak Demirel"
  - "Kelly K. Horst"
  - "Alessio Perazzolo"
  - "Elisa Bruno"
  - "Kenan Kaya"
  - "Rongzhen Ouyang"
  - "Enas Ahmed"
  - "Jouke Smink"
  - "Spencer L. Waddle"
  - "Zainudeen Kallumpurath"
  - "Tzu Cheng Chao"
  - "Dinghui Wang"
  - "Steve G. Langer"
  - "Timothy L. Kline"
  - "Panagiotis Korfiatis"
  - "Jacinta Browne"
  - "Ivana Isgum"
  - "Tim Leiner"
date: "2026-09-20"
arxiv_id: "2609.23950"
arxiv_url: "https://arxiv.org/abs/2609.23950"
pdf_url: "https://arxiv.org/pdf/2609.23950v1"
categories:
  - "eess.IV"
  - "cs.CV"
  - "cs.LG"
  - "physics.med-ph"
tags:
  - "医学影像基础模型"
  - "报告生成"
  - "LLM报告生成"
  - "端到端诊断"
  - "心脏MRI"
  - "临床验证"
  - "多任务学习"
  - "异常检测"
  - "疾病分类"
  - "序列分类"
  - "心室功能评估"
  - "瘢痕分割"
  - "多模态融合"
  - "扫描仪原生AI"
  - "实时分析"
relevance_score: 6.5
---

# ORION-CMR: On-scanner Reporting with Integrated Foundation Model for End-to-End Cardiac MRI Analysis and Interpretation

## 原始摘要

Cardiovascular magnetic resonance (CMR) provides comprehensive cardiac assessment but remains underutilized because of the complexity of acquisition, post-processing, and interpretation. Existing artificial intelligence (AI) methods address isolated tasks, limiting clinical integration. We present ORION-CMR (On-scanner Reporting with Integrated fOunda-tioN Model), the first clinically evaluated scanner-native end-to-end CMR foundation model. Pretrained on 12,896,733 CMR images from 9,258 studies, ORION-CMR performs sequence classification, ventricular function assessment, late gadolinium enhancement (LGE) detection, binary and multiclass disease classification, and local large language model-based report generation in approximately 90 seconds. The framework. was evaluated on public benchmarks and clinically validated in a multi-vendor cohort of 68 subjects with normal examinations, congenital heart disease, dilated cardiomyopathy, and myocardial infarction. ORION-CMR outperformed supervised baselines and the previously published CMR foundation model (CMR-FM), achieving state-of-the-art performance for LGE classification and scar segmentation. Clinical evaluation achieved an AUC of 0.96 for normal-versus abnormal classification and 0.88 for multiclass disease classification, while generated reports demonstrated 81.4% agreement with expert interpretation. These results demonstrate the feasibility of real-time scanner-native AI-assisted CMR analysis and automated report generation.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

心血管磁共振（CMR）是评估心脏结构与功能的金标准，但因其采集、后处理和解读流程复杂，且依赖专业软件与稀缺的专科医师，临床普及率极低——美国仅有不到1000名医师能解读CMR，近7000万人距最近服务点超过50英里。现有深度学习虽提升了自动化分析能力，但大多局限于分割、分类或组织表征等单一任务，难以融入完整临床工作流；近期出现的CMR基础模型也仍聚焦于个别下游任务，缺乏统一、可临床部署的端到端方案。此外，解读需整合多序列图像、定量指标与临床背景，跨软件操作导致耗时增加、读者间差异大。为此，本文提出ORION-CMR——首个经临床评估的扫描仪原生端到端CMR基础模型，基于9258项研究的1289万余张图像预训练，用单一编码器统一支持序列分类、心室功能评估、LGE检测、二分类与多分类疾病诊断，并借助本地大语言模型自动生成报告，约90秒完成全流程，旨在实现实时、扫描仪端的AI辅助CMR分析与报告生成。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，现有深度学习 CMR 方法多为单任务设计，如分割、分类或组织表征，代表性工作包括基于自监督 Vision Transformer 的 CMR 分割与疾病分类研究，以及已发布的 CMR 基础模型 CMR-FM。本文与它们的核心区别在于：ORION-CMR 是首个经临床评估的扫描仪原生端到端 CMR 基础模型，单一预训练编码器统一支持序列分类、心室功能评估、LGE 检测、二分类与多分类疾病诊断及报告生成，而非局限于单一任务。应用类方面，既往研究多聚焦 LGE 识别与心肌瘢痕量化，但缺乏与临床工作流的整合；本文在 68 例多厂商队列中完成临床验证，覆盖正常、先天性心脏病、扩张型心肌病和心肌梗死，并实现约 90 秒内完成全流程分析。评测类方面，本文在公开基准上超越监督基线及 CMR-FM，在 LGE 分类和瘢痕分割上达到 SOTA，并首次系统评估了 LLM 生成报告与专家解读的一致性（81.4%）。

### Q3: 论文如何解决这个问题？

ORION-CMR 的核心思路是构建一个扫描仪原生的端到端 CMR 基础模型，将序列识别、分割、疾病分类与报告生成整合为统一工作流。整体框架以共享 ViT 编码器为骨干，采用 DINO 式自监督教师-学生蒸馏，在 12,896,733 张多 vendor CMR 图像上预训练，无需人工标注。预训练后编码器保持冻结，仅训练轻量任务头：序列分类用最后两个 Transformer 块拼接的 1536 维嵌入加 MLP；cine-SAX 与 LGE-SAX 分割拼接最后四块 patch token，经轻量卷积解码器输出全分辨率分割；疾病与 LGE 分类则提取 CLS token 嵌入，经线性 SVM 完成。多序列（2ch/4ch/SAX/LGE）嵌入拼接为 4×1536 维受试者级表示，用于多分类及正常/异常二分类。所有量化测量与分类结果被整合为结构化表示，再交由本地部署的 Qwen2.5-14B-Instruct 生成放射科风格报告，全程在扫描仪端约 90 秒完成，无需外部网络。创新点在于：首次实现扫描仪原生实时端到端 CMR 分析；用自监督基础模型统一多任务；引入 ViT-B8 细粒度 patch 提升小结构表征；并以结构化表示约束 LLM 减少幻觉，实现与专家报告 81.4% 的一致性。

### Q4: 论文做了哪些实验？

论文在公共基准和多厂商临床队列上系统评估了ORION-CMR。公共基准方面，LGE分类在EMIDEC上达到0.930，超过此前SoTA（0.920）和CMR-FM（0.733）；在ACDC上以0.820超过CMR-FM（0.700）和监督基线（0.480，P<10⁻²）。分割任务中，ACDC上LV、心肌、RV的D/d_H差异分别为（0.007,1.377）、（0.044,7.717）、（0.011,1.956）；EMIDEC上心肌和瘢痕Dice达0.915和0.799，超过此前SoTA（0.879和0.712，P<10⁻²）。临床验证纳入68例多厂商受试者，涵盖正常、先天性心脏病、扩张型心肌病和心肌梗死。正常vs异常分类AUC为0.96，多分类AUC为0.88；LGE分类AUC 0.826，二分类疾病AUC 0.960，均优于ResNet-18。生成报告与专家解读一致率81.4%±1.7%，中等13.7%，不一致4.9%，Cohen's κ为0.41–0.61。全流程约90秒，其中序列分类11.2秒、cine SAX分割51.6秒、LGE与疾病分类9.7秒、报告生成11.2秒。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要集中在验证规模与评估方式上：临床验证仅来自单中心、小样本队列（先心病亚组仅7例），且心室功能指标以原始临床报告记录为参考，而非专家手工勾画的轮廓，可能引入标注偏差。此外，作者也指出缺乏对各模块的消融实验，以及LLM提示设计与结构化数据schema的进一步评估。未来可从三方面深入：一是开展多中心、多 vendor、大样本前瞻性验证，并纳入更多罕见病种；二是用专家轮廓作为金标准重新评估分割与功能量化，并系统消融预训练策略、ViT patch 尺寸、LLM提示模板等组件；三是探索从"确定性结构化输出+规则生成"向可溯源、可校准的多模态推理演进，例如引入不确定性估计与幻觉检测机制，同时将报告生成扩展到纵向随访与治疗决策支持，并评估其在真实临床工作流中对读片效率与诊断准确率的实际影响。

### Q6: 总结一下论文的主要内容

ORION-CMR是首个经临床评估的扫描仪原生端到端心脏磁共振（CMR）基础模型，旨在解决CMR采集、后处理与解读流程复杂、专业人才稀缺导致其临床应用不足的问题。该模型基于9,258项研究、共12,896,733张多厂商CMR图像，采用DINO自蒸馏框架预训练ViT-Base编码器，单一共享编码器支持序列分类、心室功能评估、LGE检测、二分类及多分类疾病诊断，并由本地部署的LLM生成结构化报告，全流程约90秒完成。在ACDC和EMIDEC公开基准上，ORION-CMR超越监督基线和此前的CMR-FM，在LGE分类和瘢痕分割上达到最优性能；在68例多厂商临床队列中，正常与异常分类AUC达0.96，多分类AUC为0.88，生成报告与专家解读一致率达81.4%。结果表明，扫描仪原生实时AI辅助CMR分析与自动报告生成具有临床可行性。
