---
title: "Explainability Assistant: A Conversational XAI Interface for Interpreting Energy Consumption Models"
authors:
  - "Rodion Krjutškov"
  - "Eduard Barbu"
  - "Nikos Sakkas"
  - "Sofia Yfanti"
date: "2026-09-10"
arxiv_id: "2609.11860"
arxiv_url: "https://arxiv.org/abs/2609.11860"
pdf_url: "https://arxiv.org/pdf/2609.11860v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "Conversational XAI"
  - "LLM Function Calling"
  - "Energy Consumption Forecasting"
  - "Explainability Assistant"
  - "Natural Language Interaction"
  - "Intent Parsing"
  - "Time Series Interpretation"
  - "Human-in-the-loop Evaluation"
relevance_score: 7.5
---

# Explainability Assistant: A Conversational XAI Interface for Interpreting Energy Consumption Models

## 原始摘要

Energy consumption forecasting relies on increasingly complex machine learning (ML) models, such as Genetic Programming-based symbolic regressors, whose predictions can be difficult for facility managers and building operators to interpret. Explainable Artificial Intelligence (XAI) techniques address this opacity, but traditional XAI dashboards require substantial technical expertise and provide limited flexibility for dynamic, context-aware inquiry. Conversational XAI systems offer a promising alternative; however, previous approaches, such as TalkToModel, were constrained by rigid custom grammars and achieved only 76.8% intent-parsing accuracy. This paper introduces the Explainability Assistant, an open-source conversational XAI system that leverages the function-calling capabilities of modern Large Language Models (LLMs) to overcome these limitations. The system achieves 94% intent-parsing accuracy, supports flexible natural language interaction, and adapts to different ML problem types without task-specific fine-tuning. We present the system's architecture and report results from a comparative evaluation conducted with energy domain specialists, contrasting the Explainability Assistant with a traditional XAI dashboard. The evaluation suggests improved usability and consistent task accuracy, with all experts unanimously preferring the conversational interface for practical use.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

随着机器学习模型在建筑能耗预测等领域日益复杂，设施管理者难以理解模型为何给出特定预测。LIME、SHAP、反事实解释等后验可解释性技术虽能缓解模型黑箱问题，但传统可解释性仪表盘要求用户具备较高技术专长，且交互僵化，难以支持动态、迭代、结合上下文的追问。已有的对话式XAI系统TalkToModel虽提供了自然语言交互思路，却受限于自定义语法，意图解析准确率仅76.8%，且难以适配不同任务类型。本文提出Explainability Assistant，旨在利用现代大语言模型的函数调用能力，构建一个开源对话式XAI系统，解决三个核心问题：提升自然语言意图解析准确率至94%；支持灵活的自然语言交互，无需任务特定微调即可适配不同ML问题类型；并通过与能源领域专家的对比评估，验证对话式界面在可用性和任务准确性上优于传统仪表盘，从而让非数据科学背景的领域专家也能便捷地理解能耗预测模型。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，早期工作聚焦于内在可解释模型，随后出现面向黑箱模型的事后解释方法，如LIME和SHAP用于特征重要性、反事实解释用于识别最小输入变化、梯度方法用于可视化神经网络行为。应用与交互类方面，语言可解释性工具和What-If Tool等仪表盘系统将多种解释技术集成到统一界面，但要求用户自行判断应执行何种操作；TalkToModel引入自然语言对话式可解释性，但依赖定制语法和微调语言模型，意图解析准确率仅76.8%，且需复杂的任务特定适配。LLM驱动类方面，LLMCheckup通过提示工程和上下文学习实现对话式解释，依赖提示链调用解释方法；Samimi等人为糖尿病风险预测构建了视觉对话界面，结合微调T5解析器与LLM对话，仍保留任务特定微调组件；MAIA则是多模态智能体，通过自主实验解释神经网络内部，面向研究者而非终端用户。本文的Explainability Assistant与上述工作的区别在于：采用结构化LLM函数调用将自然语言查询映射为可解释性操作，比提示链更可预测，无需任务特定微调，并聚焦面向能源管理等应用场景中领域专家的预测级解释。

### Q3: 论文如何解决这个问题？

论文提出的 Explainability Assistant 采用前后端解耦的模块化架构来解决传统 XAI 系统依赖刚性语法、难以灵活交互的问题。前端基于 Next.js 实现对话式界面，管理会话历史、用户认证，并支持用户在 Llama-3.3-70B-Instruct、Gemini-2.0-Flash、Gemini-2.5-Flash 等多个 LLM 之间切换；后端基于 FastAPI，负责数据操作、模型推理、执行预定义可解释性函数，并通过 API 与外部 LLM 通信。

核心创新在于用现代 LLM 的函数调用能力取代任务特定语法微调：系统将用户查询、对话历史和可用函数的 JSON 规范（名称、描述、参数）一并提供给 LLM，由 LLM 决定调用哪些函数并生成结构化参数。这一范式带来四方面优势：意图解析准确率超过 90%（Gemini-2.5-Flash 达 93–94%），远高于 TalkToModel 基于 T5 语法的 76.8%；LLM 被约束输出含强制自由文本解释字段的 JSON，暴露系统计划动作以增强透明度和可信度；函数在本地后端执行，仅发送查询与工具模式，保护数据隐私；仅需修改配置即可适配新数据集和模型类型。

系统集成了三类事后解释技术：基于 SHAP 的特征重要性分析（支持单样本与全局）、基于 DiCE 的反事实解释，以及用户主导的 What-If 情景分析。通过能耗回归与心脏病分类两个用例验证了其跨任务、免微调的适应能力。

### Q4: 论文做了哪些实验？

论文开展了两个互补实验。第一是LLM意图解析准确率评估：构建了三个金标准解析数据集，A（20条）人工编写覆盖20个核心功能，B和C（各80条）由GPT-5和Gemini-2.5-Pro生成并人工校验。评估了GPT-5-mini、Llama-3.3-70B-Instruct、Gemini-2.0-Flash和Gemini-2.5-Flash四个模型，在A+B和A+C（各100条）上测精确匹配准确率。结果显示Gemini-2.5-Flash最高，达94%（A+B）和93%（A+C），Gemini-2.0-Flash为88%和91%，GPT-5-mini为74%和79%，Llama-3.3-70B为78%和74%，均超过早期语法系统约75%的水平。第二是专家验证：3位能源领域专家（10-20年经验）参与被试内对比研究，在模拟商业建筑能耗管理场景中，对比传统Explainer Dashboard（ED，含SHAP、what-if滑块）与会话式Explainability Assistant（EA），完成10道任务题（每个界面5道），并从易用性、信任、系统理解、未来使用意愿四个维度进行五点李克特评分。结果显示任务准确率ED为93%、EA为100%；EA在易用性和再次使用意愿上获一致高分（均为5），而ED评分差异较大（2-5），专家一致偏好会话界面。

### Q5: 有什么可以进一步探索的点？

论文的主要局限在于评估规模较小，仅面向能源领域专家，且“信任输出”和“理解系统”两项评分仅为中等，说明用户对LLM驱动的解释仍持保留态度。此外，系统依赖前沿LLM的函数调用能力，在离线或隐私敏感场景下部署受限，且94%的意图解析准确率仍有提升空间。未来可从三方面探索：一是构建对话与可视化混合界面，发挥传统仪表盘在全局概览上的优势；二是引入不确定性量化与解释溯源机制，让用户了解每条解释的可信度来源，从而提升信任度；三是将该框架扩展到更多ML问题类型和领域（如医疗、金融），并开展更大规模的纵向用户研究，检验长期使用下的学习曲线与依赖风险。此外，可探索轻量级本地模型替代方案，以降低部署门槛。

### Q6: 总结一下论文的主要内容

论文针对能耗预测中复杂机器学习模型（如遗传规划符号回归器）难以被设施管理者理解的问题，提出“Explainability Assistant”——一个开源对话式可解释AI系统。传统XAI仪表盘需要较高技术门槛且交互僵化，而早期对话系统（如TalkToModel）受限于自定义语法，意图解析准确率仅76.8%。本系统利用现代大语言模型的函数调用能力，实现94%的意图解析准确率，支持灵活的自然语言交互，且无需针对特定任务微调即可适配不同ML问题类型。作者与能源领域专家开展对比评估，结果显示该系统可用性更高、任务准确率稳定（100% vs 93%），三位专家一致偏好对话界面。研究表明，对话式XAI能降低领域专家理解模型的门槛，提升可解释性技术的可及性与实用性。
