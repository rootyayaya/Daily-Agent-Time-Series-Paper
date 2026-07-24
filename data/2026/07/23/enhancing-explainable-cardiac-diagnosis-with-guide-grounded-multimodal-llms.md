---
title: "Enhancing Explainable Cardiac Diagnosis with Guide-Grounded Multimodal LLMs"
authors:
  - "Hai-Nam Duy Vuong"
  - "Duy-Anh Bui"
  - "Trong-Nghia Nguyen"
  - "Kim-Ngan Thi Nguyen"
  - "Trang Mai Xuan"
  - "Tien-Cuong Nguyen"
  - "Van-Dem Pham"
  - "Thien Van Luong"
date: "2026-07-23"
arxiv_id: "2607.20814"
arxiv_url: "https://arxiv.org/abs/2607.20814"
pdf_url: "https://arxiv.org/pdf/2607.20814v1"
categories:
  - "cs.AI"
tags:
  - "time series report"
  - "semantic description"
  - "自然语言报告生成"
  - "LLM/Agent用于时间序列异常检测"
  - "可解释时序诊断"
  - "多模态LLM"
  - "Grad-CAM"
  - "ECG诊断"
  - "guide grounding"
  - "知识注入"
  - "BERTScore"
relevance_score: 8.5
---

# Enhancing Explainable Cardiac Diagnosis with Guide-Grounded Multimodal LLMs

## 原始摘要

The electrocardiogram (ECG) is a cornerstone of cardiac as- sessment, yet clinical deployment of deep learning models remains con- strained by limited interpretability and the hallucination risk of large language models (LLMs). Existing CNN+Grad-CAM+multimodal LLM frameworks can generate ECG reports, but their explanations are often only weakly grounded in established diagnostic criteria, reducing trust- worthiness and reproducibility. We propose a guide-grounded multimodal framework that explicitly anchors report generation in curated clinical knowledge. A convolutional neural network (CNN) and Grad-CAM first produce class probabilities and class-specific heatmaps from 12-lead ECG images. In parallel, authoritative ECG textbooks and guideline materials are distilled offline into a structured ECG Interpretation Guide, which is injected as a fixed knowledge block for every sample. Conditioned on the ECG image, Grad-CAM overlay, CNN-derived fact pack, and the in- jected guide, a multimodal LLM generates structured diagnostic reports with guideline-consistent terminology and criteria usage. Experiments on the full PTB-XL test set demonstrate that guide grounding improves se- mantic quality and perceived consistency of generated reports while pre- serving competitive classification performance. In particular, our method increases the average BERTScore of generated impressions from 0.818 to 0.953 relative to a strong CNN+Grad-CAM+MLLM baseline, indicat- ing closer alignment with reference reports. These findings suggest that injecting a distilled interpretation guide into the multimodal prompting pipeline offers a practical pathway to reduce hallucinations and enhance the clinical plausibility of LLM-based ECG explanations, bringing ex- plainable cardiac diagnosis closer to real-world deployment.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

心电图（ECG）是心脏评估的核心工具，但深度学习模型的临床应用受限于可解释性不足和大语言模型（LLM）的幻觉风险。现有方法如CNN+Grad-CAM+多模态LLM框架虽能生成ECG报告，但其解释往往仅弱依赖于既定的诊断标准，导致可信度和可重复性降低。本文旨在解决这一问题，提出一种基于指南引导的多模态框架，通过将权威ECG教科书和指南材料离线蒸馏为结构化的ECG解释指南，并将其作为固定知识块注入每个样本的提示中，从而明确地将报告生成锚定在临床知识上。核心目标是减少LLM的幻觉，增强生成报告与临床指南的一致性，提升语义质量和感知一致性，使基于LLM的ECG解释更接近实际临床部署。

### Q2: 有哪些相关研究？

本文的相关研究主要分为三类。第一类是**可解释AI（XAI）方法**，如Grad-CAM、LIME和SHAP，它们被用于ECG分析以生成类激活热图，提供视觉解释。本文在此基础上，进一步将Grad-CAM热图作为多模态LLM的输入，但指出其仍需领域专家解读，且无法直接转化为临床报告文本。

第二类是**多模态大语言模型（MLLM）在医学报告生成中的应用**。现有工作如CNN+Grad-CAM+MLLM框架，能够从ECG图像生成自由文本报告。本文指出这些系统严重依赖LLM内部知识，缺乏对权威ECG教科书或临床指南的显式锚定，易产生幻觉。本文的核心区别在于引入了结构化的“ECG解读指南”作为固定知识块注入提示，强制报告生成遵循指南术语和标准。

第三类是**LLM自动评估方法**，例如使用Gemini等强LLM对生成报告进行评分或比较，以评估解释质量。本文也采用了类似的LLM自动评估作为报告质量评价信号，但主要贡献在于通过指南锚定提升报告的可信度和一致性，而非评估方法本身。

### Q3: 论文如何解决这个问题？

该论文提出了一种基于指南引导的多模态框架，通过显式锚定临床知识来增强心电图诊断的可解释性并减少大语言模型的幻觉。整体架构分为三个阶段：

**第一阶段：信号预处理与CNN分类**  
首先对12导联心电图波形进行去噪（移动平均平滑、陷波滤波、高通巴特沃斯滤波），然后渲染为单张堆叠轨迹图像。使用ResNet-50作为CNN骨干网络，采用多标签sigmoid输出，生成5个诊断超类（PTB-XL）的概率向量。对Top-3预测类别应用Grad-CAM，从最后一个卷积层生成类激活热图，上采样后叠加到原始心电图上作为视觉证据。

**第二阶段：离线知识蒸馏与指南构建**  
从权威心电图教科书和指南中提取页面级文本，分块（每块70万字符，共3块）后使用LLM嵌入器建立向量数据库。通过检索提示让LLM（gpt-5-mini）识别并请求最相关的页面/章节，返回的检索块经过去重、去页眉页脚等压缩处理（禁止摘要和删除医学内容），最后用gpt-4o-mini合成结构化的ECG Interpretation Guide，包含心电图生理学、系统解读步骤、主要病理诊断标准（含STEMI/NSTEMI详细章节）及快速参考表格。

**第三阶段：多模态报告生成**  
多模态LLM接收四个输入：原始心电图图像、Grad-CAM叠加图、CNN事实包（全概率向量+Top-3类别）、以及固定注入的ECG Interpretation Guide。采用证据层级提示策略：Grad-CAM作为主要诊断证据，心电图图像辅助定位显著区域，事实包作为辅助信息，指南支持术语一致性。模型强制输出固定JSON结构，包含发现（按导联/节段描述形态）、印象（临床摘要）、证据（导联-特征-原理三元组）、一致性（对齐/部分/冲突）、置信度和建议。与标准RAG不同，该方法将完整领域知识压缩为单个文档注入每个样本的上下文窗口，避免逐案例检索。实验表明，该方法将生成印象的BERTScore从0.818提升至0.953，显著增强了报告与参考标准的一致性。

### Q4: 论文做了哪些实验？

实验在PTB-XL数据集上进行，包含21,837条12导联ECG记录，分为5个诊断超类（Normal、Conduction Disturbance、Hypertrophy、Myocardial Infarction、ST/T Change）。采用官方分层训练/验证/测试划分，多标签多热向量表示。对比方法包括基线（CNN+Grad-CAM+MLLM，无解释指南）和本文方法（额外注入结构化ECG解释指南）。CNN主干经对比DenseNet、Inception-v3、ResNet-50、VGG-16后，选择ResNet-50（F1=0.82）。主要结果：在跨语言BERTScore（德语参考vs英语生成）上，基线F1为0.818，本文方法提升至0.982；在翻译参考BERTScore（德语翻译为英语后）上，基线F1为0.818，本文方法提升至0.953。此外，在200样本定性子集上采用LLM盲审强制选择，Gemini法官下本文方法胜率62%（基线38%），GPT-4o-mini法官下胜率76%（基线24%）。实验表明指南注入显著提升了报告语义质量和事实一致性。

### Q5: 有什么可以进一步探索的点？

该论文在可解释心脏诊断方面取得了显著进展，但仍存在若干可探索的方向。首先，当前框架依赖离线蒸馏的静态知识指南，无法动态适应最新临床指南或个体化患者差异，未来可引入在线知识更新机制，使LLM能实时检索最新文献或医院本地知识库。其次，Grad-CAM热力图仅提供粗粒度的空间定位，缺乏对时序波形形态（如ST段抬高幅度、QT间期变化）的精确解释，可探索结合时序注意力机制或波形分割模型生成更细粒度的诊断依据。此外，PTB-XL数据集规模有限且标签较为宏观，未来应在更大规模、多中心、含罕见病的数据集上验证，并引入对抗性测试评估模型对噪声或伪影的鲁棒性。最后，当前报告生成仍以文本为主，可扩展为多模态交互式诊断助手，支持医生通过自然语言追问特定导联或波形细节，进一步提升临床实用性和信任度。

### Q6: 总结一下论文的主要内容

该论文提出了一种基于指南约束的多模态框架，用于增强可解释的心脏诊断。核心问题在于现有深度学习模型和LLM在ECG报告生成中存在可解释性不足和幻觉风险。方法上，首先利用CNN和Grad-CAM从12导联ECG图像生成类别概率和热力图；同时，离线蒸馏权威教科书和指南构建结构化的ECG解读指南，作为固定知识块注入每个样本。随后，多模态LLM基于ECG图像、Grad-CAM叠加图、CNN事实包和注入的指南，生成符合指南术语和标准的诊断报告。在PTB-XL测试集上的实验表明，该方法在保持分类性能的同时，将生成印象的BERTScore从0.818提升至0.953，显著提高了语义质量和一致性。该工作通过注入蒸馏指南，有效减少了LLM的幻觉，增强了临床可信度，为可解释AI辅助心脏诊断的实际部署提供了可行路径。
