---
title: "Diagnosing as Cardiologists Do: ECG Agents with Doctor-Grounded Priors for Clinical Reasoning Across Diseases and Populations"
authors:
  - "Hongxiang Gao"
  - "He-yang Xu"
  - "Yuwen Li"
  - "Minghui Zhao"
  - "Zhipeng Cai"
  - "Xingyao Wang"
  - "Chenxi Yang"
  - "Jianqing Li"
  - "Chengyu Liu"
date: "2026-08-10"
arxiv_id: "2608.09053"
arxiv_url: "https://arxiv.org/abs/2608.09053"
pdf_url: "https://arxiv.org/pdf/2608.09053v1"
categories:
  - "eess.SP"
  - "cs.CV"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "ECG 诊断"
  - "视觉语言模型"
  - "临床推理"
  - "可解释诊断"
  - "测量引导推理"
  - "零样本迁移"
  - "报告生成"
relevance_score: 8.5
---

# Diagnosing as Cardiologists Do: ECG Agents with Doctor-Grounded Priors for Clinical Reasoning Across Diseases and Populations

## 原始摘要

Cardiologists interpret electrocardiograms by localizing waveform components, measuring rhythm and interval patterns, and translating these structured observations into diagnostic evidence. Whether this expert reading process can serve as an effective prior for ECG agents remains unclear. To address this question, we introduce LuminaECG, a clinically structured ECG reasoning framework that reformulates ECG interpretation as measurement-grounded visual reading. ECG signals are rendered on standard electrocardiographic grid paper to preserve the spatial and scale cues used in clinical reading. P-wave, QRS-complex, and T-wave boundaries are explicitly delineated, and color-coded segmentation decomposes the waveform into discrete visual measurement primitives. A general 2B vision-language backbone is then trained with low-rank supervised fine-tuning to associate these primitives with diagnostic reasoning, without architectural modification. Across open, proprietary, and ECG-specialist zero-shot baselines, LuminaECG improves both waveform measurement and diagnostic recovery. It reaches a clinically meaningful reader tier on the CODE-test benchmark, transfers across geographically diverse ECG datasets without retraining, and generates reports whose structure contains an emergent prognostic signal. These findings suggest that effective ECG agents require not only larger models, but supervision that preserves the alignment between measurable waveform evidence and clinical knowledge.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

心电图（ECG）是临床中最密集的测量手段之一，但现有自动化解读方法存在明显不足：传统监督模型在固定标签空间外泛化能力差，而多模态大语言模型虽灵活，却缺乏波形定位、间期测量及形态证据与诊断标准对应的领域先验，导致模型虽“知道”疾病概念，却无法在具体心电图上定位支持性证据，难以可靠部署于真实临床。

本文核心问题是：心内科专家“先定位波形、再测量间期、最后整合为诊断证据”的阅读流程，能否作为ECG智能体的有效先验？为此提出LuminaECG框架，将心电图渲染到标准网格纸上保留时空尺度，显式勾画P波、QRS波和T波边界，并通过彩色分割将波形分解为可测量的视觉基元，再用轻量2B视觉-语言模型进行低秩微调，使其将测量基元与诊断推理关联。

该工作旨在验证：相比单纯扩大模型规模，保留临床测量证据与知识对齐的监督数据构建，是否更能提升ECG智能体的诊断性能、跨人群泛化能力及报告的结构化预后信息。

### Q2: 有哪些相关研究？

相关研究可归为三类。**方法类**中，传统深度学习诊断系统（如基于CNN/自监督的模型）是闭集分类器，仅输出标签而无解释性证据，跨设备与人群泛化差；本文通过结构化视觉读取和测量基元显式关联波形与诊断，弥补了可解释性与泛化短板。**多模态LLM类**，现有工作如信号编码器+文本解码器生成报告，或如ECG-R1引入诊断协议与强化学习，但均以报告文本为监督目标，未显式绑定发现与波形证据；本文在标准网格纸上渲染信号、分割P/QRS/T波并编码颜色，将测量基元与推理对齐，且仅用低秩微调通用2B视觉-语言模型，无需架构改动。**先验注入类**，已有研究在损失函数、课程学习或视觉提示中注入单一先验（如区域框选、注意力增强），但缺乏多层级联合；本文创新性地在同一训练样本中融合三类先验——度量坐标框架、波形成分身份、测量到诊断的因果链，形成“可见先验阶梯”，并验证模型确实依赖这些先验而非捷径。与ECG-R1等相比，本文强调测量基元的显式可视化而非仅协议约束，且跨数据集零样本迁移能力更强。

### Q3: 论文如何解决这个问题？

该论文通过构建“测量-可视化-报告”三阶段临床监督框架，将心电图解读重构为基于测量的视觉阅读任务，核心创新在于用医生式阅读先验替代模型架构扩展。整体框架包含三个离线处理模块：首先，基于NeuroKit的波形描绘器在十二导联上定位P、QRS、T、U波特征点，提取303维临床特征面板（含194维逐导联特征和109维全局特征），涵盖波幅、ST段水平、QT间期、电轴等量化指标，所有数值均源于此测量步骤而非自由文本标签。其次，将信号渲染为标准心电图纸（25mm/s、10mm/mV）上的6×2布局十二导联图像，并用绿、红、蓝三色分别覆盖P波、QRS波群和T波段，使视觉编码器同时获得临床图像和自明的分割线索，网格固定了像素空间中的时间/电压尺度。最后，gpt-4o仅依据设备测量值和数值面板（不接触波形）生成八段式中文报告，通过接地协议约束其只断言测量支持的诊断，例如一度房室阻滞必须锚定PR>200ms，并链接每个结论到具体测量值或颜色标识的波形。

模型采用Qwen2B视觉-语言骨干网络，仅训练低秩适配器，不添加任何任务特定架构模块，刻意隔离临床阅读先验的影响。训练数据来自MIMIC-IV-ECG的719,828份记录，每份样本为三元组（波形标注图像、固定八段指令、接地报告），在8块H100上微调两个epoch。该方法在CODE-test基准上达到临床有意义的阅读者层级，无需重训练即可迁移至PTB-XL等地理分布不同的数据集，且报告结构蕴含预后信号，证明有效的心电智能体需要保持可测量波形证据与临床知识对齐的监督，而非单纯扩大模型规模。

### Q4: 论文做了哪些实验？

论文围绕LuminaECG框架设计了一套统一评估协议，涵盖报告生成、数值测量、临床诊断和跨队列迁移四个维度。实验设置上，报告生成与数值测量在MIMIC-IV-ECG留出集（n=79,981）上进行，采用BLEU、ROUGE-L、CIDEr评估报告质量，以MAE评估心率、PR间期、QRS时限的测量精度。对比方法包括GPT-5.4、Claude-Opus-4.7、Qwen3-VL系列等通用视觉语言模型，以及ECG-R1等专科模型。结果显示LuminaECG在BLEU-1达0.853、BLEU-4达0.741、ROUGE-L达0.808、CIDEr达0.896，显著优于所有零样本基线；心率MAE仅0.43 bpm，PR和QRS MAE分别为8.97 ms和4.48 ms，远低于最强基线。在CODE-test（n=827）上，LuminaECG-2B的宏F1为0.840、微F1为0.852，超过医学生（0.817）和急诊住院医（0.829）层级，接近心内科住院医（0.862）。跨队列测试覆盖巴西、中国、德国数据，宏F1保持在0.644-0.840，而ResNet1d-101在PTB-XL上仅0.049。在PTB-XL关键发现召回测试中，LuminaECG-2B恢复50.8%的紧急诊断，远超所有零样本系统（<10.3%）。此外，在Sami-Trop队列（n=1,631）中，报告特征将Harrell's C从0.678提升至0.764（ΔC=+0.086）。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从以下层面展开：首先，当前监督仅停留在报告级模仿，未显式建模医生“测量-定位-推理”的完整认知链条，未来可引入导联级证据、形态学细粒度描述及医生验证的推理链，使模型从模板生成转向证据驱动的因果推理。其次，模型缺乏对患者多模态临床上下文（症状、用药、实验室指标、既往心电图）的整合，可探索将时序信号与结构化电子病历联合建模，提升跨人群泛化中的个体化诊断能力。第三，现有评测侧重静态基准，未来需设计动态人机协作场景，评估模型在交互式追问、不确定性表达及可修正推理上的表现。此外，可尝试将医生先验嵌入到架构层面（如可微分波形测量模块）而非仅依赖数据增强，以增强测量与诊断间的可解释对齐。最后，跨设备、跨采集协议的域偏移仍是挑战，可结合自监督预训练与因果不变性学习，提升对采集伪影的鲁棒性。

### Q6: 总结一下论文的主要内容

本文提出LuminaECG，一个以医生诊断逻辑为先验的心电图推理框架。其核心贡献在于将心电图解读重构为基于测量的视觉阅读过程：信号被渲染于标准网格纸上以保留空间尺度，P波、QRS波和T波边界被显式分割并颜色编码，形成可量化的视觉基元。方法上，作者用低秩监督微调训练一个通用2B视觉-语言骨干模型，使其将这些基元与诊断推理关联，无需修改架构。实验表明，LuminaECG在波形测量和诊断恢复上超越开放、专有及心电图专科零样本基线，在CODE-test基准达到临床有意义的阅读水平，并能跨地理数据集泛化，其生成报告的结构还蕴含预后信号。结论强调，可靠医疗推理不仅依赖模型规模，更依赖训练数据是否保留临床证据与知识间的对齐，专家诊断先验应作为医学多模态模型的基础。
