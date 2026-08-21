---
title: "From Noise to Signal: Improving Security Log Anomaly Detection Using LLMs with Endpoint-Specific Logs"
authors:
  - "Christopher Henshaw"
  - "Gour Karmakar"
date: "2026-08-20"
arxiv_id: "2608.19938"
arxiv_url: "https://arxiv.org/abs/2608.19938"
pdf_url: "https://arxiv.org/pdf/2608.19938v1"
categories:
  - "cs.CR"
  - "cs.LG"
tags:
  - "LLM-based anomaly detection"
  - "security log analysis"
  - "instruction-tuned LLM"
  - "authentication behavior"
  - "rule-based vs statistical vs LLM"
  - "borderline anomaly detection"
  - "structured output"
  - "cybersecurity testbed"
relevance_score: 8.5
---

# From Noise to Signal: Improving Security Log Anomaly Detection Using LLMs with Endpoint-Specific Logs

## 原始摘要

Existing approaches to anomalous behaviour log detection, such as Wazuh rely primarily on predefined detection rules, while statistical anomaly detection approaches such as OpenSearch identify deviations from previously observed behavioural patterns. Recent research has investigated LLMs for log anomaly detection because of their ability to interpret semantic and contextual information. However, LLM-based approaches can be affected by prompt construction, noisy log data, and reliance on generic datasets that may lack endpoint-specific authentication behaviours. To address these limitations, this study develops a standardised instruction-based LLM classification framework for detecting anomalous authentication behaviours, including borderline cases. A controlled cybersecurity testbed was developed to generate endpoint-specific authentication data, producing a curated dataset comprising normal, borderline, and anomalous behavioural scenarios. Three instruction-tuned LLMs, Meta Llama 3.1 8B Instruct, Qwen 2.5 7B Instruct, and GPT-OSS 20B, were evaluated against Wazuh rule-based detection and OpenSearch Anomaly Detection using a common ground-truth severity framework. Meta Llama 3.1 8B Instruct achieved the strongest overall end-to-end detection performance, with an accuracy of 89.3%, recall of 88.2%, F1-score of 91.8%, and false negative rate of 11.8%. In comparison, Wazuh achieved an accuracy of 52.0% and false negative rate of 68.6%, while OpenSearch achieved an accuracy of 49.3% and false negative rate of 74.5%. Meta Llama also detected 80% of the borderline anomalous scenarios, compared with 20% for Wazuh and 15% for OpenSearch. Qwen achieved lower overall detection performance than Meta Llama but recorded the lowest average inference latency and 100% structured-response validity. GPT-OSS demonstrated strong classification performance when valid responses were produced.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

论文针对现有安全日志异常检测方法的局限性，特别是规则检测（如Wazuh）和统计异常检测（如OpenSearch）在识别边界性、持续性或模仿性可疑行为时的不足。这些方法依赖预定义规则或统计偏差，难以捕捉需要跨事件语义推理的复杂行为。同时，现有LLM-based日志异常检测研究多依赖公共数据集（如HDFS、BGL），缺乏端点特定的认证行为数据，且提示词设计、噪声日志和泛化问题影响性能。论文旨在开发一个标准化的指令式LLM分类框架，用于检测端点特定认证行为中的异常，包括边界案例，并与传统基线进行公平对比。核心研究问题是：在受控网络安全测试环境中，近期指令调优的LLM相比Wazuh和OpenSearch在端点特定认证行为检测上的表现如何。

### Q2: 有哪些相关研究？

相关工作包括：1) 规则检测：Wazuh基于预定义规则和签名，依赖规则覆盖和配置。2) 统计异常检测：OpenSearch使用Random Cut Forest (RCF)算法，识别时间序列数据中的统计偏差，但受特征选择、概念漂移影响。3) 传统ML/DL：决策树、SVM、LSTM、Transformer等，但依赖数据质量、可解释性差。4) LLM-based检测：Qi et al. (2023) 使用ChatGPT进行日志异常检测，强调提示词和领域知识；Han et al. (2023) 提出LogGPT学习正常日志序列；Guan et al. (2024) 提出LogLLM结合BERT和Llama；Hadadi et al. (2024) 研究不稳定日志下的GPT模型；Song et al. (2025) 使用对比学习微调LLM检测内部威胁；Zhang et al. (2024) 提出LogRAG结合RAG；Patel (2026) 比较传统ML、微调Transformer和提示LLM。本文与这些工作的区别在于：使用端点特定认证行为数据（而非公共数据集），直接对比指令调优LLM与Wazuh/OpenSearch，并强调边界案例检测。

### Q3: 论文如何解决这个问题？

论文提出一个标准化指令式LLM分类框架，包含三个核心组件：1) 受控网络安全测试环境：使用VirtualBox搭建Wazuh服务器、Ubuntu端点（Wazuh agent）和Kali Linux攻击主机，生成端点特定认证事件（正常、边界、异常），记录于/var/log/auth.log，并整理为75个行为场景（20正常、24边界、31异常）。2) 标准指令框架：每个LLM接收相同的行为描述、七个行为线索（如认证成功/失败、重复访问、时间模式、一致性、自动化指标）、六点严重度评分（0-5，阈值2为异常）、二元分类要求和JSON响应格式。3) 评估流程：使用Python程序通过Hugging Face Router API调用三个指令调优LLM（Meta Llama 3.1 8B Instruct, Qwen 2.5 7B Instruct, GPT-OSS 20B），温度设为0.0，最大响应长度300 tokens，验证结构化响应有效性，记录推理延迟，并与Wazuh和OpenSearch基线对比。基线系统分别使用Wazuh规则（如Rule 5710检测非存在用户SSH尝试）和OpenSearch RCF算法。所有检测结果映射到统一二元分类框架（Anomaly为正类），计算准确率、召回率、F1等指标。

### Q4: 论文做了哪些实验？

实验在受控测试环境中进行，评估了三个LLM（Meta Llama 3.1 8B Instruct, Qwen 2.5 7B Instruct, GPT-OSS 20B）与Wazuh和OpenSearch的检测性能。数据集包含75个行为场景，其中24个正常（含4个severity-1边界）、51个异常（含20个severity-2边界）。主要结果：Meta Llama取得最佳整体性能，准确率89.3%、召回率88.2%、F1分数91.8%、假阴性率11.8%；Wazuh准确率52.0%、假阴性率68.6%；OpenSearch准确率49.3%、假阴性率74.5%。在20个severity-2边界异常场景中，Meta Llama检测出80%，Qwen 55%，Wazuh 20%，OpenSearch 15%。GPT-OSS在有效响应时表现良好，但结构化输出有效性低（仅5/20边界场景有效），降低了端到端可靠性。Qwen延迟最低且100%结构化响应有效。实验还记录了Wazuh规则警报分布（如Rule 5710产生644次警报）。

### Q5: 有什么可以进一步探索的点？

论文存在以下局限和未来方向：1) 数据集规模较小（75个场景），未来可扩展更大数据集和更多端点环境。2) 测试环境为受控虚拟环境，真实网络复杂性未充分体现，需在真实企业环境中验证。3) 仅关注认证行为，可扩展到其他攻击类别（如网络扫描、数据外泄）。4) 未进行LLM微调，未来可探索指令微调或RAG增强。5) 结构化输出可靠性问题（GPT-OSS）需改进，可研究更稳健的响应解析或自一致性机制。6) 未深入分析LLM的决策可解释性，可结合XAI技术提供更透明的诊断链。7) 可探索多智能体协作或LLM与规则/统计方法的集成框架，实现证据路由和自适应阈值。8) 推理延迟和计算成本需优化，以适应实时SOC环境。

### Q6: 总结一下论文的主要内容

论文提出并评估了一种基于指令调优LLM的认证行为异常检测方法，旨在补充传统规则和统计检测的不足。作者构建了受控网络安全测试环境，生成端点特定认证数据（正常、边界、异常），并开发标准化指令框架，使三个LLM（Meta Llama 3.1 8B, Qwen 2.5 7B, GPT-OSS 20B）在相同条件下进行分类。实验显示Meta Llama在整体检测性能上显著优于Wazuh和OpenSearch，尤其在边界异常场景中（80% vs 20%和15%），同时保持较低假阴性率。Qwen在延迟和响应有效性上表现最佳，GPT-OSS则受限于结构化输出问题。研究证明了LLM作为语义分析层的潜力，为安全监控提供了可解释、上下文感知的补充手段。主要贡献包括测试环境、标准化指令框架和对比评估方法，为未来在更大规模、更多攻击类型上的研究奠定了基础。
