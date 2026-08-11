---
title: "Defending Retrieval-Augmented Intrusion Detection Against Knowledge Poisoning and Prompt Injection"
authors:
  - "Kaysarul Anas Apurba"
  - "Md. Hasibul Hasan"
  - "Mahedee Zaman Moon"
  - "Sk. Md. Mizanur Rahman"
  - "Atsuo Inomata"
date: "2026-08-08"
arxiv_id: "2608.08100"
arxiv_url: "https://arxiv.org/abs/2608.08100"
pdf_url: "https://arxiv.org/pdf/2608.08100v1"
categories:
  - "cs.CR"
  - "cs.AI"
  - "cs.LG"
tags:
  - "RAG"
  - "multi-agent"
  - "intrusion detection"
  - "network traffic classification"
  - "prompt injection"
  - "knowledge poisoning"
  - "retrieval-boundary defense"
  - "explainable AI"
  - "incident report generation"
  - "security"
relevance_score: 8.5
---

# Defending Retrieval-Augmented Intrusion Detection Against Knowledge Poisoning and Prompt Injection

## 原始摘要

Retrieval-Augmented Generation (RAG) enables large language models to classify network flows and generate human-readable incident reports by retrieving semantically similar historical traffic from a vector knowledge base. However, the retrieval layer introduces vulnerabilities to knowledge poisoning and prompt-injection attacks. We present RAG-IDS, a three-tier multi-agent intrusion detection framework with a retrieval-boundary defense combining soft trust scoring, label-embedding consistency checking (LECC), and prompt sanitization, designed to recover classification quality under retrieval-layer attack. Experiments on CIC-UNSW-NB15 show recovery relative to clean undefended performance ranging from R=1.0 at 1% poisoning to R=0.57 at 30%, with negligible clean-performance overhead. Under prompt injection, multi-document retrieval limits label-flip success to 0.6-2.4%, compared with 35-55% for single-document retrieval. Ablation results show that LECC is the primary contributor to robustness, while soft trust-based demotion outperforms hard filtering. The defended RAG pipeline offers an explainable, attack-resilient foundation for intrusion detection, well suited for hybrid deployment alongside high-throughput classifiers.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

现代企业网络每天面临数百万条流量，现有检测手段存在明显不足：基于签名的系统无法应对新型攻击变体，ML分类器虽具适应性但输出缺乏可解释性且易受分布偏移影响。检索增强生成（RAG）通过将LLM推理锚定在历史攻击流知识库上，能同时实现流量分类、自然语言解释和攻击战术映射，为入侵检测提供了新路径。

然而，现有RAG-IDS系统（如CyberRAG、MA-IDS）均未审视RAG管道自身的安全性。向量知识库是可持久写入的数据结构，攻击者只需部分写权限即可污染检索上下文，系统性地误导LLM而不触发任何检测规则。具体威胁包括两类：一是检索投毒——攻击者注入被重标为Benign的攻击类文档，因保留原始嵌入，投毒文档对攻击查询排名最高，导致误分类；二是提示注入——附加在合法检索文档中的指令覆盖载荷在推理时劫持LLM输出，完全绕过基于相似度的防御。

通用RAG防御（如FilterRAG、RAGForensics）虽能应对检索腐败，但在IDS工作负载下——极端类别不平衡、操作级FPR约束、流到文本检索语义——的领域特定评估仍属空白。本文核心问题是：如何在RAG-IDS的检索边界构建有效防御，在知识投毒和提示注入攻击下恢复分类质量，同时保持可解释性和极低的干净性能开销。

### Q2: 有哪些相关研究？

相关研究可分为四类。**传统IDS方法**：基于误用与异常的检测系统（Buczak & Guven综述）、树模型与LSTM序列模型、Kitsune无监督在线检测等，本文继承其流量分类目标，但指出其闭世界假设与基率谬误的固有缺陷。**RAG与LLM安全**：Lewis等人提出RAG框架，Karpukhin等人验证稠密检索优势，Gao等人综述RAG范式并指出知识库安全为开放挑战；Huang等人确认检索增强可缓解幻觉。**RAG攻击研究**：PoisonedRAG展示小规模文档注入即可实现知识破坏，Greshake等人刻画间接提示注入，Phantom提出触发器后门，CorruptRAG扩展为单文档攻击。**RAG防御研究**：FilterRAG利用统计特征过滤对抗文本，RAGForensics实现溯源追踪，SafeRAG提供通用NLP防御基准。本文与上述工作的核心区别在于：首次将RAG安全防御系统性地应用于网络入侵检测这一特定领域，面临流量语义、极端类别不平衡与误报率约束的独特挑战；提出的LECC机制针对PoisonedRAG式重标签攻击设计，而非通用检索过滤，并通过多文档检索天然抑制提示注入，实现了领域定制化的攻击韧性。

### Q3: 论文如何解决这个问题？

论文提出RAG-IDS，一个三层多智能体入侵检测框架，核心创新在于检索边界的对抗防御模块，而非对检索文档进行硬过滤。整体架构分为三层：第一层检测智能体负责特征提取、检索与分类；第二层推理智能体基于MITRE ATT&CK知识库生成事件报告；第三层响应智能体通过规则剧本执行阻断、限速或告警动作。

防御模块位于第一层检索边界，由三个组件构成复合怀疑评分。D1软信任分数计算文档与查询的余弦相似度，低于阈值θ=0.40时施加惩罚，量化检索可信度。D2标签-嵌入一致性检查（LECC）将文档嵌入与各类别质心比较，若最近质心与文档声明标签不符则施加一致性惩罚；若一致则回退到基于干净训练数据校准的每类95百分位离群点检查。LECC直接针对PoisonedRAG策略：被重标签的攻击文档保留原始嵌入，因此更接近攻击质心而非声明的良性质心。D3提示清洗器通过正则模式库和注入样本嵌入相似度双重评分，识别并抑制提示注入。

最终检索分数为原始检索分数减去λ倍的三个惩罚项之和，λ=0.3，文档按新分数重排序后进入LLM上下文。这种软降级而非硬过滤的设计保留了上下文多样性，同时抑制恶意检索结果。实验表明，在1%投毒率下恢复性能为R=1.0，30%投毒率下为R=0.57；多文档检索将标签翻转成功率限制在0.6-2.4%，远低于单文档检索的35-55%。消融实验显示LECC是鲁棒性的主要贡献者，软信任降级优于硬过滤。

### Q4: 论文做了哪些实验？

论文在CIC-UNSW-NB15数据集上开展了多组实验。实验设置包括：知识库含2000条文档（每类200条），使用BGE-M3嵌入和FAISS索引，Mistral-7B模型4-bit量化，检索k=5，随机种子{42,123,7}，主要指标为宏平均F1。

数据集与基准：对比了Random Forest、XGBoost和CNN-LSTM。在完整测试集上，RF宏F1为0.4678，XGB为0.4752，CNN-LSTM仅0.0987；在CEXP04同集对比中，XGB达0.678±0.022，而RAG-IDS清洁未防御仅0.270±0.016。

主要实验包括：1）知识投毒防御（CEXP04）：在1%-30%投毒率下，恢复率R从1.002±0.006单调降至0.573±0.057，清洁时无性能损失（0.270→0.274）；2）低量投毒探测（CEXP08）：注入1-2条毒文档不影响性能（R=1.010）；3）提示注入攻击（CEXP04）：多文档检索下标签翻转成功率仅0.6%-2.4%，单文档下升至35%-55%；4）消融实验（CEXP05）：LECC是主要鲁棒性贡献者，软信任降级优于硬过滤。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是检索层在低命中率（Hit@5仅0.19）下仍依赖脆弱的知识库，当检索质量本身不足时，防御机制可能放大噪声而非提升鲁棒性；二是当前防御主要针对静态投毒和单轮注入，对自适应攻击者（如动态污染、跨会话多跳注入）缺乏验证；三是软信任评分和LECC依赖标签分布假设，在类别极不均衡或标签噪声高的真实工业场景中可能失效。

未来可探索的方向包括：1）设计检索质量感知的自适应防御，将检索置信度与分类器输出动态融合，避免低质量检索对决策的过度影响；2）引入对抗训练或鲁棒检索器，使向量表示本身对投毒不敏感，而非仅依赖后处理过滤；3）构建多智能体间的交叉验证机制，利用不同模型对同一流量的独立判断降低单点被攻击风险；4）探索在线学习框架，使防御策略能根据攻击模式实时更新，而非静态配置。此外，可考虑将可解释性从“报告生成”延伸至“防御决策解释”，帮助安全分析师理解为何某条检索被降权或过滤，提升人机协同的可信度。

### Q6: 总结一下论文的主要内容

本文提出RAG-IDS，一个针对检索增强生成（RAG）入侵检测系统的三层多智能体防御框架。RAG通过检索历史流量向量库辅助LLM分类，但检索层易受知识投毒和提示注入攻击。方法上，作者在检索边界部署三重防御：软信任评分过滤（D1）、标签嵌入一致性检查（LECC，D2）和提示清理器（D3）。在CIC-UNSW-NB15数据集上，该防御在1%投毒时恢复性能达干净基线（R=1.0），30%投毒时仍恢复57%；提示注入下，多文档检索将标签翻转成功率从单文档的35-55%降至0.6-2.4%。消融实验表明LECC是鲁棒性主因，软信任降级优于硬过滤。该工作首次系统化解决IDS场景下RAG检索层安全，为可解释、抗攻击的混合部署入侵检测提供了坚实基础。
