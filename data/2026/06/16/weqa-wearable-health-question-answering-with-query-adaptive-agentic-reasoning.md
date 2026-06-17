---
title: "WEQA: Wearable hEalth Question Answering with Query-Adaptive Agentic Reasoning"
authors:
  - "Yuwei Zhang"
  - "Tong Xia"
  - "Bianca Emmerich"
  - "Yu Yvonne Wu"
  - "Dimitris Spathis"
  - "Xin Liu"
  - "Daniel McDuff"
  - "Cecilia Mascolo"
date: "2026-06-16"
arxiv_id: "2606.18147"
arxiv_url: "https://arxiv.org/abs/2606.18147"
pdf_url: "https://arxiv.org/pdf/2606.18147v1"
categories:
  - "cs.AI"
tags:
  - "Agentic Time Series"
  - "LLM/Agent"
  - "可穿戴健康数据"
  - "查询自适应推理"
  - "工具调用"
  - "传感器分析"
  - "医疗问答"
  - "多模态时间序列"
  - "证据路由"
  - "外部知识审计"
relevance_score: 8.5
---

# WEQA: Wearable hEalth Question Answering with Query-Adaptive Agentic Reasoning

## 原始摘要

Language models are remarkably capable at medical question answering, in some cases surpassing the accuracy of general physicians. However, answering questions about wearable health data remains challenging and understudied, as these ubiquitous sensors produce continuous, high-dimensional, and longitudinal data, which is non-trivial to align with text-centric distributions in LLM pretraining. The diversity of sensor modalities and user intents cannot be effectively handled by a fixed reasoning workflow or a single pretrained foundation model. To address these challenges, we propose WEQA, a query-adaptive agent framework that unifies LLM reasoning with specialized wearable analytical and modeling tools. An LLM controller is employed to synthesize execution plans and dynamically route each query to the appropriate combination of sensor analysis and pretrained models, and perform grounded response auditing with external knowledge. We also curate a benchmark spanning four open wearable datasets comprising analytic and predictive tasks in three different health domains. Experiments show that our framework is 24% more accurate than LLM and agentic baselines, and a blinded study with 12 medical experts and 8 users shows substantial gains in usefulness and clinical soundness.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

可穿戴健康问答面临两大核心挑战。研究背景是，虽然大语言模型在通用医学问答上表现优异，但处理可穿戴设备产生的连续、高维、纵向生理信号时存在根本性困难。现有方法的不足体现在三个方面：一是纯文本LLM无法理解传感器数据的波形形态、时序动态和跨传感器交互等原生特征；二是固定推理流程或单一预训练模型无法应对用户意图的多样性，如从简单统计查询到长期趋势分析、从原始信号预测到个性化证据综合等异构任务；三是缺乏对回答结果进行传感器证据和医学知识验证的机制。本文要解决的核心问题是：如何构建一个能够自适应地结合LLM语言理解能力与专用可穿戴分析建模工具的统一框架，使系统能根据用户查询意图和传感器上下文动态选择计算路径，从而实现对异构可穿戴健康问题的准确、个性化且临床合理的回答。

### Q2: 有哪些相关研究？

在相关研究方面，本文主要涉及三个类别：

**1. 可穿戴健康大语言模型与智能体：** 现有方法通常将传感器数据摘要为文本输入LLM，但会丢失精细的时间结构和信号形态。近期智能体系统通过规划、工具使用和多步推理增强了能力，但仍依赖预聚合的粗粒度特征，局限于统计分析。本文提出的WEQA框架则实现了传感器原生理解与自适应推理工作流的结合，能泛化到不同任务、模态和时间范围。

**2. 可穿戴健康基础模型：** 大规模预训练已用于活动识别、心血管监测等任务，近期传感器-语言模型进一步对齐了信号与语言接口。但这些模型通常针对预定义模态和固定领域，难以扩展到更广泛的健康查询。WEQA不训练单一通用模型，而是通过统一智能体框架动态组合LLM推理与专用传感器分析工具，将问题求解视为自适应推理过程。

**3. 自适应智能体框架：** 近期工作探索了自动化工作流设计和模块化智能体优化，但通常基于数据集级别进行迭代搜索。与之不同，可穿戴健康智能体需要在推理时根据用户查询、传感器上下文和个性化需求动态调整。WEQA实现了无需训练、查询自适应的框架，在基准测试中准确率比LLM和智能体基线高24%，并在医学专家和用户盲审中展现出显著优势。

### Q3: 论文如何解决这个问题？

WEQA 的核心方法是一个查询自适应的智能体框架，通过动态编排推理路径来解决可穿戴健康问答的挑战。其整体架构分为三个阶段：查询感知规划、证据构建和基于证据的响应审计。

**核心方法与架构设计**：
1.  **查询感知规划**：采用LLM作为控制器，将用户查询、传感器元数据、可用工具集和历史示例映射为结构化执行计划。控制器首先识别查询目标、所需模态、时间范围、推理类型和风险等级，然后规划分析步骤。规划是动态的，每步执行后可根据累积证据修订计划，从而处理异构查询并应对执行错误或数据缺失。
2.  **证据构建**：包含两条互补的执行路径，均由LLM控制器编排：
    *   **传感器分析推理**：针对可直接回答的查询，执行代码调用分析工具（如统计、趋势、相关性分析），生成分析证据。
    *   **自适应预测推理**：针对需要推断的查询，调用专用预测模型（包括任务特定模型和可穿戴基础模型）。模型选择基于查询类型，并包含不确定性估计。控制器进行不确定性感知编排，若模型置信度低，则查询额外模型并比较/组合输出。个性化通过少样本适应或历史感知模型实现。
3.  **基于证据的响应审计**：合成分析证据和预测证据，生成最终响应。其功能包括：验证主要主张有传感器证据支持、校准不确定性沟通、以及整合外部医学知识以提供临床适当的指导。

**关键技术**：动态规划、不确定性感知模型编排、个性化适应（少样本/历史基线）、以及基于证据的审计与外部知识融合。

### Q4: 论文做了哪些实验？

论文在可穿戴健康问答领域进行了全面的实验验证。实验设置包括：使用Gemini-3.0-Flash作为默认LLM骨干，构建了包含358名用户、1123个问答对、6种传感模态的基准测试，覆盖TILES（日常生理行为）、COVID-19 Sounds（呼吸音频）、PPG-BP（血压估计）四个数据集。对比方法包括：数据输入基线（LLM-Text文本序列化、LLM-Image多模态推理）和智能体架构（ReAct迭代推理、Multi-Agent多智能体编排）。主要结果：WEQA在短时分析QA上达到95.6%精确匹配（EM）和9.2 MAE，远超ReAct（64.8%/31.3）和Multi-Agent（72.0%/157.2）；长时分析QA上达到94.0%数值推理EM和95.1%趋势相关性准确率；预测推理QA上分类平衡准确率达83.9%（ReAct为59.2%），血压回归MAE为10.9（最优）。效率方面，WEQA仅用约10k tokens/查询，远低于基线方法的31k-42k。盲法人类评估中，12名医学专家和8名用户对WEQA在准确性、个性化、有用性和临床合理性四个维度的评分均最高（专家平均3.9分，ReAct为3.1分，Multi-Agent为2.9分），72.5%的对比中评估者更偏好WEQA。消融实验证实了自适应推理和响应审计组件的关键作用，且框架在不同LLM骨干（Gemini/Qwen）上表现稳健。

### Q5: 有什么可以进一步探索的点？

首先，当前基准仅涵盖四个公开数据集，缺乏对真实世界中传感器噪声、人群异质性及临床场景多样性的覆盖。未来可构建包含多设备、多人群、多病种的更大规模基准，并引入对抗性样本测试鲁棒性。其次，框架依赖预定义的分析工具和预测模型，扩展新模态或任务需手动集成。一个关键方向是赋予Agent自动发现、检索和适配外部工具与基础模型的能力，例如通过工具库动态组合或元学习生成任务特定管线。此外，人类评估样本量较小，可设计更高效的交互式评估协议，结合用户反馈进行在线学习。最后，尽管引入了不确定性感知，但模型仍可能产生过度自信的预测。可探索将可解释性模块（如注意力归因、反事实解释）与Agent推理过程深度耦合，使LLM能基于传感器数据的时间模式生成可验证的临床推理链，同时通过外部知识库进行事实核查。

### Q6: 总结一下论文的主要内容

论文提出WEQA框架，解决可穿戴健康数据问答中连续高维时序数据与LLM文本分布不匹配、固定推理流程无法处理多模态用户意图的问题。核心贡献是设计查询自适应智能体系统，通过LLM控制器动态编排传感器分析、时序推理、预测建模、个性化模型适配和安全审计工具，实现从查询到响应的灵活执行路径。在四个公开数据集、三类健康任务的基准测试中，WEQA相比LLM和智能体基线准确率提升24%；12位医学专家和8位用户的盲评显示其回答在实用性、临床合理性上显著更优。结论表明，有效可穿戴健康助手需设计为协调专业生理模型与安全推理的自适应系统，而非依赖单一语言模型。
