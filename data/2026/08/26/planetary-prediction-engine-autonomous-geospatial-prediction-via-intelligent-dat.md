---
title: "Planetary Prediction Engine: Autonomous Geospatial Prediction via Intelligent Data Selection and Foundation Model Embeddings"
authors:
  - "Evelyn Ma"
  - "Rama Kumar Pasumarthi"
  - "Kishwar Shafin"
  - "Mandar Sharma"
  - "Mimi Sun"
  - "Hamed Sadeghi"
  - "Dav M. Ebengo"
  - "Mbulayi Onesime"
  - "Rouslan Solomakhin"
  - "John Wamburu"
  - "William Ogallo"
  - "Aisha Walcott-Bryant"
  - "Sanxing Chen"
  - "Arbaaz Muslim"
  - "Yael Mayer"
  - "Ronald Ho"
  - "Roy Lee"
  - "Ruth Alcantara"
  - "Abdoulaye Diack"
  - "Monica Bharel"
date: "2026-08-26"
arxiv_id: "2608.26088"
arxiv_url: "https://arxiv.org/abs/2608.26088"
pdf_url: "https://arxiv.org/pdf/2608.26088v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Agentic Time Series"
  - "Autonomous Data Selection"
  - "Geospatial Foundation Model Embeddings"
  - "Multimodal Data Fusion"
  - "Natural Language Query"
  - "Automated Model Selection"
  - "Spatiotemporal Prediction"
  - "End-to-End Workflow"
  - "Planetary-Scale Analytics"
relevance_score: 7.5
---

# Planetary Prediction Engine: Autonomous Geospatial Prediction via Intelligent Data Selection and Foundation Model Embeddings

## 原始摘要

Addressing critical global challenges, from food security and disaster risk to disease outbreaks and socio-economic vulnerability, demands high-fidelity geospatial modeling. However, building predictive planetary models remains bottlenecked by a fragmented data ecosystem, requiring manual data retrieval, multimodal data curation and fusion along with iterative model selection. We present the Planetary Prediction Engine (PPE), an autonomous AI system that executes this end-to-end workflow directly from natural-language queries. PPE synthesizes multimodal datasets on the fly, retrieving spatiotemporally relevant covariates across open-web and Earth observation platforms (Data Commons, Google Earth Engine) and fusing them with geospatial foundation model embeddings (PDFM, AlphaEarth). Simultaneously, it searches over task-tailored model architecture families with automated overfitting guards. Across diverse tasks, geographies, and scientific domains, PPE consistently outperforms state-of-the-art or manually tuned expert baselines. For US spatial regression, PPE improves mean $R^2$ across 21 CDC health indicators (76.8% vs. 60.0%), FEMA national risk indices (64.9% vs. 60.0%), and the Social Vulnerability Index (66.2% vs. 58.6%). For spatial downscaling in data-scarce settings, PPE integrates localized proxies to double baseline accuracy in Nigerian food security indicators ($R^2$ of 66.1% vs. 31.5%). For epidemiological nowcasting of the 2026 DRC Bundibugyo Ebola outbreak, PPE achieves a Recall@10 of 83.3% (identifying 15 of 18 newly invaded health zones across five weekly forecasts), a +10.3 percentage-point improvement over the public state-of-the-art modeling (~73%). By combining autonomous multimodal planetary data discovery with targeted model optimization, PPE lowers the technical barrier to planetary-scale analytics, enabling rapid, customized, expert-level deployment.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

全球粮食安全、灾害响应、疾病暴发追踪等关键问题亟需高精度地理空间建模，但现有预测流程严重依赖人工：研究者需手动检索分散的数据源、清洗融合多模态数据、设计模型并防止空间泄漏，单个流行病建模流程可涉及700余步操作，耗时数周，难以应对紧急人道主义需求。现有AutoML框架和AI科学发现系统（如ERA、AlphaEvolve）虽能优化预定义目标，但仅适用于干净表格数据或软件工程任务，缺乏自主发现大规模地理空间数据、融合异构嵌入向量（如PDFM、AlphaEarth）以及参数化流行病学机制模型的能力。因此，核心问题是：如何构建一个端到端自主系统，仅凭自然语言查询即可自动完成数据发现、多模态融合、模型选择与验证，从而打破地理空间建模的技术壁垒，让非专家也能快速部署专家级预测模型，尤其服务数据稀缺或危机频发地区。

### Q2: 有哪些相关研究？

相关研究主要分为以下几类：  
**方法类**：包括空间回归、超分辨率降尺度、流行病学即时预测与空间传播建模等传统统计与机器学习方法，如基于贝叶斯平滑和空间通量方程的传播模型。本文与之区别在于，PPE将这些方法整合进自动化流水线，无需人工干预即可完成端到端建模。  
**AutoML与AI科学发现系统**：如ERA、AlphaEvolve等，通过LLM与程序搜索优化预定义指标，但依赖清晰目标和预清洗数据。PPE则能自主发现并融合多源地理空间数据，处理异构嵌入向量，并参数化机制性流行病学模型，突破了现有框架对结构化表格数据的限制。  
**LLM智能体与数据科学自动化**：近期工作探索LLM驱动的代码生成、调试和假设提出，但通常局限于干净表格数据或软件工程任务。PPE专门针对地理空间数据生态，具备数据检索、融合和泄漏防护能力。  
**地理空间基础模型**：如PDFM（人口动态）和AlphaEarth（土地利用语义），提供高维嵌入。PPE将其与统计协变量智能组合，超越单一嵌入或人工特征工程的效果。  
总体而言，PPE的贡献在于将数据发现、多模态融合和模型选择整合为自主系统，填补了现有AutoML和LLM智能体在地理空间预测领域的空白。

### Q3: 论文如何解决这个问题？

论文提出了一种名为“行星预测引擎”（PPE）的全自主AI系统，旨在解决地理空间预测中数据碎片化、人工流程繁琐的瓶颈。其核心方法是将端到端预测工作流分解为三个模块化阶段，并利用现成的大语言模型（LLM）作为各阶段的编排器。

整体框架包含三大模块：**智能数据选择**、**多模态数据集构建**和**自动模型构建与预测**。在智能数据选择阶段，系统首先解析用户自然语言查询，自动识别任务类型（如空间回归、超分辨率降尺度、流行病学即时预测），并据此约束后续数据检索策略。随后，系统从开放网络和地球观测平台（如Data Commons、Google Earth Engine）动态检索时空相关的协变量，同时融合地理空间基础模型嵌入（如PDFM和AlphaEarth），实现异构数据的对齐与融合。在数据集构建阶段，系统执行严格的目标泄漏缓解协议，防止空间信息泄漏。最后，自动模型构建模块迭代搜索多种模型家族（正则化线性模型、梯度提升树、极端梯度提升、多层感知机），并配备多层过拟合防护与自我纠正循环，以选择最优模型生成最终预测。

该论文的创新点包括：一是实现了完全自主的模块化代理架构，无需人工干预即可完成从数据发现到模型评估的全流程；二是通过任务自动识别与目标对齐，使AutoML能够针对代理定义的目标进行优化；三是智能数据选择协议系统性地探索了人类从业者可能忽略的特征组合；四是自动模型构建协议结合过拟合防护，确保了模型泛化能力。实验证明，PPE在多种地理空间任务上均显著优于专家基线，如美国CDC健康指标R²从60.0%提升至76.8%，尼日利亚粮食安全降尺度精度翻倍。

### Q4: 论文做了哪些实验？

论文围绕三种预测范式设计了系统性实验：**机制性即时预测（Nowcasting）、超分辨率降尺度（Downscaling）和空间回归（Spatial Regression）**，覆盖流行病、粮食安全、公共健康、环境风险和社会脆弱性等主题。

**实验设置与数据**：Nowcasting任务追踪2026年刚果（金）Bundibugyo Ebola疫情，覆盖519个卫生区，训练7周、测试5周；降尺度任务包括尼日利亚FCG粮食安全（30州训练→581个LGA测试，40个月）和美国SVI（县→ZCTA）；空间回归使用CDC 21项健康指标、FEMA 21项风险指数（约8.4万个人口普查区，80:20划分）及SVI县级数据。

**对比方法**：基线包括传统专家手工管道（如贝叶斯模型、宏协变量+插值）和独立基础模型嵌入；消融层级包括仅协变量（PPE-Covariates）、协变量+嵌入（PPE-Embeddings）和完整系统（PPE-Full Stack）。

**主要结果**：①疫情热点检测中，PPE完整系统Recall@10达83.3%（识别18个新入侵区中的15个），较SOTA基线（73%）提升10.3个百分点；②尼日利亚粮食安全降尺度中，PPE的R²达66.1%，是基线（31.5%）的两倍多，MAE从13.6%降至10.0%；③美国空间回归中，PPE在CDC健康指标（R² 76.8% vs 60.0%）、FEMA风险指数（64.9% vs 60.0%）和SVI（66.2% vs 58.6%）上均显著优于专家调优基线。

### Q5: 有什么可以进一步探索的点？

论文的局限性与未来探索方向可从三方面展开：其一，当前系统在跨分辨率任务中暴露的噪声-精度权衡（如SVI从县到ZIP尺度下AEF特征导致R²下降），未来可引入自适应特征筛选机制，根据目标尺度动态调整多模态特征的融合权重，或采用对抗训练抑制高频噪声干扰。其二，智能数据选择依赖预定义检索源和启发式优先级，对非结构化数据（如社交媒体文本、卫星影像时序）的语义理解仍有限，可探索将LLM与图神经网络结合，构建动态知识图谱以捕捉地理实体间的隐式关联，提升数据发现的因果推理能力。其三，自动化模型搜索目前侧重监督学习范式，对时空动态演化（如疫情传播中的干预措施反馈）建模不足，可引入神经微分方程或状态空间模型，结合强化学习实现模型与数据选择的闭环在线优化，同时需扩展不确定性量化框架以支持高风险决策场景。此外，跨域迁移时如何平衡预训练嵌入的通用性与任务特异性，也是值得深挖的方向。

### Q6: 总结一下论文的主要内容

该论文提出了行星预测引擎（PPE），一个端到端的自主AI系统，旨在解决全球性挑战中的地理空间建模难题。其核心问题在于传统预测流程依赖手动数据检索、多模态融合和模型选择，耗时且门槛高。PPE通过三个模块化阶段实现自动化：智能数据选择、多模态数据集构建和自动模型构建与预测。系统利用LLM作为编排器，从自然语言查询中自动识别任务类型（如空间回归、超分辨率、流行病预测），动态检索开放网络和地球观测平台数据，并与地理空间基础模型嵌入（PDFM、AlphaEarth）融合。主要结论显示，PPE在多种任务中超越专家基线：美国CDC健康指标R²达76.8%（基线60.0%），尼日利亚粮食安全降尺度精度翻倍（66.1% vs 31.5%），并在2026年埃博拉疫情预测中Recall@10达83.3%。该系统的意义在于大幅降低行星尺度分析的技术门槛，使非专家也能快速构建定制化、专家级预测模型。
