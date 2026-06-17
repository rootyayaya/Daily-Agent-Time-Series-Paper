---
title: "DiagFlowBench: Evaluating How Language Models Handle Off-Procedure Inputs in Grounded Diagnostic Dialogue"
authors:
  - "Guillermo Gil de Avalle"
  - "Laura Maruster"
  - "Shaina Raza"
  - "Christos Emmanouilidis"
date: "2026-06-16"
arxiv_id: "2606.17904"
arxiv_url: "https://arxiv.org/abs/2606.17904"
pdf_url: "https://arxiv.org/pdf/2606.17904v1"
categories:
  - "cs.AI"
tags:
  - "LLM/Agent用于故障诊断"
  - "工业诊断对话"
  - "grounded对话系统"
  - "幻觉检测"
  - "流程合规性"
  - "多轮对话评估"
  - "基准数据集"
relevance_score: 7.5
---

# DiagFlowBench: Evaluating How Language Models Handle Off-Procedure Inputs in Grounded Diagnostic Dialogue

## 原始摘要

Language models increasingly serve as advisory systems in maintenance operations. To prevent hallucination, recent systems ground these models in procedural documentation to constrain them to approved steps. In practice, however, operator queries frequently stray from this path, requiring models to recognise out-of-scope inputs mid-conversation, a dynamic that current benchmarks rarely prioritise. We introduce DiagFlowBench, a dataset of 50 industrial diagnostic flowcharts from a consumer manufacturer converted into 1,676 multi-turn conversations that contrast compliant with out-of-scope utterances. Evaluating a panel of ten commercial and open-weight models reveals high variability in abstention rates, with models commonly selecting a real but contextually inadequate step rather than fabricating facts. The inherent plausibility and authority of this mapped but wrong advice exposes a challenging vulnerability for grounding systems.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

大型语言模型（LLM）越来越多地被部署为工业维护咨询系统，通过自然语言对话帮助操作员查阅程序文档。然而，现有方法存在显著不足：一方面，基于流程图（flowchart）的基准测试通常只评估模型在符合程序的标准输入上的合规性；另一方面，对“脱离程序”输入的识别评估往往局限于单轮对话中的“拒绝回答”能力。现实中的诊断对话是两者的混合体，操作员会在对话中途提出程序未预见的症状或问题，这些“脱离程序”的输入与合规输入交织出现，要求模型在推进程序的同时识别并处理这些偏离。现有基准未能模拟这种动态混合场景，导致评估存在盲区。本文旨在解决这一核心问题：如何评估LLM在真实的、多轮混合对话中，同时处理合规输入和“脱离程序”输入的能力。为此，作者提出了DiagFlowBench数据集，包含50个工业流程图转换成的1676个多轮对话，每个对话都包含合规和“脱离程序”两种类型的语句，从而填补了现有评估的空白。

### Q2: 有哪些相关研究？

相关研究主要分为两类：任务导向对话（TOD）中的流程图对话系统和拒绝回答（abstention）检测。在流程图对话系统方面，FloDial 开创性地将故障排查流程图转化为对话，评估模型遵循流程的能力；PFDial 和 GuideBench 分别通过 UML 图合成和动态规则变更来扩展规模与测试合规性；SOP-Bench 则要求模型以工具调用形式执行工业操作流程。这些工作均假设用户查询总能映射到流程内，忽略了超出范围的情况。在拒绝回答检测方面，传统研究聚焦于单轮输入，发现 LLM 常误判自身知识边界而倾向于回答而非拒绝。当扩展到多轮对话时，CGoDial 和 FlowAgent 将离程输入视为干扰，仅要求模型检测并忽略或返回固定回复，未评估模型在未拒绝时具体返回了什么步骤。DiagFlowBench 的独特贡献在于首次同时满足五个关键评估条件：图结构流程、基于观测的对话、真实文档、多轮交互以及显式包含离程输入。它要求模型不仅判断是否拒绝，还需在未拒绝时定位到流程中具体但上下文不合适的步骤，从而揭示“映射错误”这一更隐蔽的漏洞，填补了现有基准在评估离程输入时仅关注二分类而忽视响应内容质量的空白。

### Q3: 论文如何解决这个问题？

论文通过构建DiagFlowBench基准数据集和评估协议，系统性地研究语言模型在工业诊断对话中处理偏离规程输入的能力。核心方法是将工业诊断流程图转化为有向图结构，每个节点代表诊断状态，边代表允许的转换并携带观测标签。对话中，操作员的每轮话语要么符合当前节点的出边标签（on-procedure），要么不符合任何出边（off-procedure）。对于off-procedure输入，模型应正确弃权（CA），即拒绝给出操作建议，而非错误映射（FM）或捏造（FA）。

架构设计上，评估协议将流程图以结构化JSON形式嵌入系统提示，要求模型在每轮对话中输出下一步操作，并在到达终端节点时停止。所有模型使用温度0进行确定性推理。评估分为on-procedure和off-procedure两部分：on-procedure通过词级Jaccard相似度计算步骤准确率（SA）和终止识别率（TR）；off-procedure则使用独立的语言模型裁判（Claude Haiku）将自由文本响应分类为CA、FM或FA，并通过人工标注验证一致性（κ=0.79）。

关键技术包括：1）固定参考路径设计，使所有模型看到相同对话，独立评分on-和off-procedure轮次；2）强制映射（FM）作为新发现的失败模式，模型选择图中真实但上下文不相关的节点，这种“合理但错误”的建议比捏造更难检测；3）跨模型分析维度，涵盖商业与开源、不同架构（指令、MoE、推理模型）和规模差异。创新点在于揭示了语言模型在接地系统中对off-procedure输入的脆弱性，特别是FM模式暴露了传统接地检查仅验证结构有效性而忽略上下文相关性的缺陷。

### Q4: 论文做了哪些实验？

论文构建了DiagFlowBench数据集，包含50个工业诊断流程图转化为的1,676轮多轮对话，分为合规与越界两类。实验评估了10个模型（包括商业模型Gemini 2.5 Flash、GPT-4o Mini，开源模型Qwen3系列、Mistral Small 24B等，以及Llama系列规模测试）。主要指标包括：步骤准确率（SA）、终止识别率（TR）、虚构率（FA）、强制映射率（FM）和正确弃权率（CA）。结果显示，在流程内任务中SA达70.1%-85.0%，但TR波动大（38.8%-98.5%）。在流程外任务中，FA极低（2.2%-8.6%），但FM成为主要失败模式（15.7%-67.4%），且CA虽为多数模型的主要响应，但失败率仍不可忽视。关键发现：1) 模型规模、架构或参数数量无法可靠预测流程外可靠性；2) 强制映射后，后续步骤恢复率骤降至1.0%-9.1%，远低于基线SA；3) 词汇重叠是FM的主要驱动因素。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：1）离线生成而非真实部署场景的对话数据，可能无法完全反映实际运维中的噪声和歧义；2）仅使用单一工业领域流程图，跨领域泛化性存疑；3）评估时要求模型输出具体步骤节点，导致FM率混杂了提示遵循度的影响。未来可探索的方向包括：引入检索增强生成（RAG）机制，在运行时从更大语料库动态获取流程文档，测试模型在信息不完整时的鲁棒性；设计显式的“弃权”机制（如特殊token或分类头），降低模型被迫选择不恰当步骤的概率；构建跨领域（如航空、医疗）的流程图数据集，验证FM现象的通用性；开发上下文蕴含验证层作为外部守卫，实时检测对话状态与当前步骤的语义匹配度，而非仅依赖模型自身判断。此外，可研究如何区分“专业术语相似但实际无关”与“语义等价”的输入，例如通过对比学习或因果推理增强模型的上下文敏感性。

### Q6: 总结一下论文的主要内容

DiagFlowBench 是一个用于评估语言模型在接地诊断对话中如何处理偏离规程输入的新基准。该研究针对工业维护中，操作员查询常偏离标准流程，而现有基准很少关注此动态的问题。方法上，作者将来自消费制造商的50个工业诊断流程图转换为1,676个多轮对话，对比了合规与偏离规程的表述。通过评估十种商业和开源模型，发现模型在拒绝回答率上存在高度差异，且常见失败模式是选择一个真实但上下文不合适的步骤，而非捏造事实。核心贡献在于揭示了这种映射错误建议的固有合理性和权威性，构成了接地系统的一个脆弱性挑战。主要结论是，仅约束模型遵循文档步骤并不能防止失败，反而将传统幻觉替换为一种更隐蔽的失败模式。该工作强调了评估咨询系统可靠性时，不仅要衡量接地合规性，还需衡量当现实偏离手册时模型如何安全地失败。
