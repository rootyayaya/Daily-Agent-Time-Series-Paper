---
title: "When Text and Numbers Disagree: Evidence Arbitration in Large Language Models"
authors:
  - "Mattia Carletti"
  - "Edward Phillips"
  - "Fredrik K. Gustafsson"
  - "Patitapaban Palo"
  - "Lei Clifton"
  - "Danielle Belgrave"
  - "Xiao Gu"
  - "David A. Clifton"
date: "2026-08-20"
arxiv_id: "2608.20116"
arxiv_url: "https://arxiv.org/abs/2608.20116"
pdf_url: "https://arxiv.org/pdf/2608.20116v1"
categories:
  - "cs.CL"
tags:
  - "LLM证据仲裁"
  - "时间序列与文本冲突"
  - "工具增强决策"
  - "多模态证据融合"
  - "时间序列报告"
  - "可解释诊断"
  - "模型可靠性"
  - "合成基准"
relevance_score: 8.5
---

# When Text and Numbers Disagree: Evidence Arbitration in Large Language Models

## 原始摘要

Large language models (LLMs) are increasingly used in settings where textual summaries, numerical observations, and external tool outputs may provide conflicting evidence. We study how LLMs arbitrate between such sources when they support opposing decisions. To do so, we introduce a controlled synthetic benchmark in which latent risk trajectories generate both numerical time series and natural language summaries, allowing us to construct conflicts where exactly one evidence source is aligned with the ground-truth label. This design lets us independently manipulate modality, temporal recency, source reliability, and evidence provenance. Across open-weight instruction-tuned models, we find that arbitration behaviour is systematic rather than random: models exhibit distinct text-versus-number preferences, follow temporal recency more consistently than explicit reliability cues, and can over-rely on external forecasts even when they conflict with direct contextual evidence. These results suggest that current LLMs often rely on heuristic arbitration strategies when integrating heterogeneous evidence, highlighting a failure mode for tool-augmented decision systems.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

在医疗、制造等高风险决策场景中，LLM常需整合文本摘要、数值时间序列及外部工具输出等多源证据，但这些来源可能支持相互矛盾的结论。现有研究主要关注文本间冲突、参数知识与外部知识冲突或跨模态（如图文）冲突，缺乏对文本与数值证据对立时模型如何仲裁的系统性刻画。真实数据中，各来源的可靠性、时效性和真实性难以明确，导致难以隔离仲裁行为的影响因素。为此，本文构建了一个受控合成基准，通过潜在风险轨迹同时生成数值序列和文本摘要，并构造恰好一个来源与真实标签一致的冲突场景，从而独立操控模态、时间近因、来源可靠性和证据来源。核心问题是：当文本与数值证据支持相反决策时，LLM究竟依据何种线索进行仲裁？研究发现模型表现出系统性的启发式策略——存在文本/数值偏好、更依赖时间近因而非明确可靠性提示，并可能过度信任外部预测，即使其与直接上下文证据矛盾。这揭示了工具增强决策系统在异构证据整合中的关键失效模式。

### Q2: 有哪些相关研究？

相关研究主要围绕三个方向展开。在冲突消解与证据仲裁方面，已有工作考察了检索增强生成中参数化知识与上下文知识的冲突，并提出神经元重加权、共享-私有语义建模和自适应解码等改进机制；文本冲突研究则揭示了模型存在位置和风格偏差，且很少表达不确定性；多模态冲突研究关注视觉证据与常识或文本推理的不一致。本文的独特之处在于聚焦文本与数值证据的冲突，这是此前未被系统探索的盲区。

在数值任务方面，已有工作通过重编程、多模态提示和跨模态对齐提升LLM的数值能力，同时也有研究质疑其数值推理的可靠性，指出校准差、噪声敏感和时序推理薄弱等问题。本文通过将任务简化为二元预测而非精确数值预测，规避了数值推理能力不足的干扰，从而更纯粹地研究证据仲裁机制。

在工具增强与智能体系统方面，相关工作强调迭代推理、规划、反馈和外部工具使用，并已扩展到时间序列分析领域。本文与此类系统密切相关，但重点揭示了模型在整合数值与文本证据时可能过度依赖外部预测或采用启发式策略的失败模式。

### Q3: 论文如何解决这个问题？

本文通过构建一个受控的合成基准框架来系统研究LLM在文本与数值证据冲突时的仲裁行为。核心方法包含三个模块：时间序列生成器、文本生成器和提示生成器。

时间序列生成器采用带高斯噪声的随机线性过程生成潜在风险轨迹，通过先采样标签、斜率和阈值边距，再反向生成观测序列，确保目标值与真实标签严格对齐。文本生成器提取序列的高层特征（初始水平、趋势方向与强度、阈值穿越情况等），离散化为语义类别后通过模板和同义词采样生成自然语言描述，且刻意避免包含具体数值，保证文本与数值证据的独立性。

提示生成器以模块化方式组装任务描述、证据呈现和二元选择问题，并系统控制证据呈现顺序。为解耦不同仲裁线索的影响，论文设计了四种冲突场景：基线模态先验（文本与数值仅模态不同）、时间近因冲突（时间戳明确且更新源与真相一致）、可靠性冲突（通过NaN掩码或显式损坏声明标记不可靠源）、工具预测冲突（外部预测与上下文证据矛盾）。

创新点在于：一是通过合成数据实现证据来源与真实标签的精确对齐控制，使冲突设置可独立操纵模态、时间近因、可靠性和来源出处；二是采用粗粒度二元预测目标而非精确数值预测，有效隔离了仲裁行为与细粒度数值预测能力的混淆；三是系统评估了多个开源指令微调模型家族，揭示了模型在证据冲突时依赖启发式策略的系统性行为模式。

### Q4: 论文做了哪些实验？

论文构建了受控合成基准，系统评估LLM在文本与数值证据冲突时的仲裁行为。实验设置包含四种冲突场景：基线模态偏好、时间近因、来源可靠性和工具预测冲突，每种场景生成2000个平衡样本（1000/标签），敏感性分析使用1000个样本。数据集通过潜在风险轨迹同时生成数值时间序列和自然语言摘要，确保仅一个证据源与真实标签对齐。

对比模型涵盖Qwen、Llama、Mistral和Gemma系列的开源指令微调模型。主要结果包括：所有模型在单模态下均达到很高准确率，冲突场景下的差异反映仲裁策略而非任务难度。Qwen系列系统性偏向数值证据，Llama和Mistral更依赖文本，Gemma最为均衡。时间近因是强仲裁线索，但显式可靠性提示影响较弱。工具预测冲突导致最严重性能下降，模型过度依赖外部预测，尤其Qwen和Gemma在上下文证据先出现时准确率接近零。证据顺序显著影响结果，后出现的证据源更受重视。敏感性分析显示领域和答案选项扰动影响有限，但答案配置可显著改变冲突准确率，且Qwen系列14B模型鲁棒性最佳。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要在于其完全依赖合成数据，缺乏真实世界场景的验证，且将预测简化为二分类任务，忽略了数值预测的连续性和复杂性。未来可从以下方向探索：一是引入真实多源数据（如医疗诊断、金融风控中的文本报告与传感器数据），验证仲裁偏见的实际影响；二是设计连续值预测任务，考察模型在更精细冲突下的权衡机制；三是开发针对性的校准或干预策略，如通过提示工程、注意力重加权或工具输出置信度显式建模，抑制对时间近因和外部预测的过度依赖；四是探索多智能体辩论或证据溯源机制，让模型显式评估各来源可信度后再决策；五是研究模型规模、训练数据分布与仲裁偏好的非线性关系，揭示其内在机制。此外，可结合可解释性方法定位引发系统性偏差的注意力头或内部表征，为构建更稳健的决策系统提供理论支撑。

### Q6: 总结一下论文的主要内容

本文研究了大型语言模型（LLM）在文本摘要、数值观测和外部工具输出等证据来源相互冲突时如何进行仲裁。作者构建了一个受控合成基准，其中潜在风险轨迹同时生成数值时间序列和自然语言摘要，并构造出恰好一个证据源与真实标签一致的冲突场景，从而独立操控模态、时间近因性、来源可靠性和证据来源。实验发现，开源指令微调模型的仲裁行为是系统性的而非随机：模型表现出明显的文本与数值偏好差异，对时间近因性的遵循程度高于显式可靠性线索，并可能过度依赖与直接上下文证据冲突的外部预测。这些结果表明，当前LLM在整合异构证据时往往依赖启发式仲裁策略，揭示了工具增强决策系统的一个关键失败模式。该研究强调，仅评估LLM在孤立文本、数值或工具任务上的表现不足以理解其在多源决策中的行为，基于冲突的评估为证据整合提供了有效的压力测试。
