---
title: "TimeLitmus: A Diagnostic Benchmark for Cross-Modal Understanding and Explanation Faithfulness in Event-Conditioned Time-Series Prediction"
authors:
  - "Jie Gong"
  - "Maowei Jiang"
  - "Zhiwei Liu"
  - "Yankai Chen"
  - "Guojun Xiong"
  - "Xue Liu"
  - "Min Peng"
  - "Qianqian Xie"
  - "Sophia Ananiadou"
date: "2026-09-21"
arxiv_id: "2609.24677"
arxiv_url: "https://arxiv.org/abs/2609.24677"
pdf_url: "https://arxiv.org/pdf/2609.24677v1"
categories:
  - "cs.AI"
tags:
  - "Time Series"
  - "LLM"
  - "Cross-Modal Understanding"
  - "Explanation Faithfulness"
  - "Event-Conditioned Prediction"
  - "Diagnostic Benchmark"
  - "Counterfactual Evaluation"
  - "Contrastive Interventions"
  - "Shortcut Controls"
  - "Semantic Report"
  - "Evidence Routing"
  - "Industrial Diagnosis"
relevance_score: 7.5
---

# TimeLitmus: A Diagnostic Benchmark for Cross-Modal Understanding and Explanation Faithfulness in Event-Conditioned Time-Series Prediction

## 原始摘要

Large language models (LLMs) are increasingly used to make predictions from numerical time-series histories and textual events. Yet accuracy alone cannot reveal whether correct answers reflect effective integration of the two inputs or instead arise from event polarity, unimodal priors, or superficial cues. Likewise, plausible explanations may rationalize predictions without faithfully reflecting the evidence that drives model behavior. We introduce TimeLitmus, a diagnostic benchmark for cross-modal understanding and explanation faithfulness in event-conditioned time-series prediction. TimeLitmus contains 4,856 evaluation records across Finance and Traffic, combining natural prediction with controlled counterfactual and contrastive interventions, explanation-targeted faithfulness tests, and systematic shortcut controls. Across ten representative LLMs, standard prediction accuracy substantially overstates reliable cross-modal understanding: Hard Paired Contrast (HPC) pair correctness peaks at only 19.2% in Finance and 11.7% in Traffic, and all ten models show lower-than-expected consistency on Finance series-side controls. Models often recognize scenario relations explicitly yet fail to apply them during independent prediction. Explanation faithfulness shows a similar gap: in Traffic, most models cite the manipulated temporal factor in over 90% of cases, while behavioral support remains below 22%. Human annotators outperform LLMs on matched controlled and hard-pair diagnostics, confirming that these distinctions are recoverable from the inputs. Natural-only adaptation yields selective gains in evidence selection and input sensitivity, but not consistent gains in controlled or hard-pair behavior. The benchmark, evaluation suite, and supervised adaptation data will be released publicly.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是事件条件下的时间序列预测任务，即模型需结合历史数值序列与文本事件来预测未来走势。研究背景在于，大语言模型正越来越多地被用于此类跨模态预测，但仅凭预测准确率无法判断模型是否真正整合了两种模态的信息。现有基准如MTBench、TemporalBench、Time-MQA等主要衡量任务性能或答案正确性，无法区分正确输出究竟来自历史序列与文本事件之间的条件关系，还是来自事件极性、单模态先验或浅层统计匹配等捷径；同时，TFRBench等解释评估基准只关注推理链是否完整连贯，未检验解释中引用的因素是否真正驱动了模型预测行为。

因此，本文要解决的核心问题是：如何诊断LLM在事件条件时间序列预测中的跨模态理解是否真实，以及其生成的解释是否忠实。为此，作者提出TimeLitmus基准，通过受控反事实干预、困难配对对比、解释针对性干预和捷径控制，分别评估预测正确性、反事实机制一致性、解释忠实性和捷径鲁棒性，从而揭示准确率所掩盖的跨模态理解与解释忠实性缺口。

### Q2: 有哪些相关研究？

相关研究主要分为三类。方法类方面，Time-MMD 和 TimeText Corpus 将数值序列与文本信息对齐，用于多模态时间序列建模；Context is Key、MTBench 和 TemporalBench 评估基于外部描述与事件的条件预测或推理；Fidel-TS 强调多模态预测中的数据完整性、泄漏控制和基准有效性。这些工作主要关注模型能否给出正确答案或预测，但未系统区分真正的事件—序列整合与由单一模态、主导先验或表面线索带来的成功。本文的 TimeLitmus 则将诊断视角引入事件条件时间序列预测，结合独立评估的受控端点、自然硬配对对比、不变性测试和部分模态控制，以分离跨模态整合与捷径成功。评测类方面，捷径学习和多模态偏差研究表明，强基准表现可能源于标注伪影或主导的单模态信号；对比集、反事实增强数据和行为测试通过修改任务相关因素来检验预测是否相应变化，TimeLitmus 延续了这一思路。解释类方面，ERASER 评估证据充分性与全面性，XForecast 评估预测解释质量，TFRBench 评估数值 grounded 推理轨迹，近期基于评判器的方法评估解释是否正确描述时间模式。TimeLitmus 进一步提出基于声明条件的行为测试：当解释引用事件或时间因素时，用受控配对检验模型预测是否遵循基准定义的相应转变，从而区分正确提及因素与行为上受支持的依赖。

### Q3: 论文如何解决这个问题？

TimeLitmus 的核心解决思路是将“预测是否正确”与“模型是否真正实现了跨模态理解”彻底解耦，通过一套受控诊断基准来暴露准确率背后的虚假信号。整体框架围绕四个互补维度构建：自然任务正确性、受控变化下的一致性、解释声称的行为支持度，以及捷径鲁棒性。

在架构设计上，基准覆盖 Finance 与 Traffic 两个领域，共 4,856 条评测记录。其关键方法是“单侧干预、独立评估”：对每个受控对，固定一个模态，仅对另一侧施加经过验证的变换（序列侧改变事件前时序状态，事件侧改变机制相关的事件属性），并强制两端 gold 标签不同。两个端点分别独立呈现给模型，使其无法从提示中推断配对身份或预期转变。评测指标包括 CF-PC（两端点均正确才算对）和 Δ_CF（与端点独立假设下期望正确率的差值），从而区分真正的配对一致性与单纯的端点难度。

解释忠实性方面，论文提出“声称条件化”测试：先检查解释是否引用了被操纵的因子（Citation Rate），再检查该引用是否伴随精确的配对级行为支持（CSDR），即引用因子且两端点均正确。此外还设置证据有效性检查与链接忠实性指标，要求正确预测与有效证据归因同时成立。

捷径鲁棒性则通过仅事件、仅序列输入、无关线索变换和保标签变换，检测模型是否依赖单模态先验或表面线索。辅助关系探针将两个场景联合呈现，用于区分“显式识别对比关系”与“在独立预测中一致应用该关系”。

创新点在于：用规则锚定的受控干预替代纯自然评测，用行为支持度约束解释忠实性，并用硬配对对比和捷径控制揭示准确率与可靠跨模态理解之间的系统性差距。

### Q4: 论文做了哪些实验？

论文围绕三个研究问题展开实验：跨模态整合、解释忠实性和适配迁移。实验评估了10个LLM，包括DeepSeek R1、DeepSeek v4 Flash、Gemini 3.5 Flash、MiniMax-M3、Qwen-Plus、GPT-5.4、Claude Sonnet 4.6、GLM-5、Qwen3.5-9B和Qwen3.5-4B，并对Qwen3.5-4B和9B进行QLoRA微调。基准测试TimeLitmus包含4,856条评估记录，覆盖Finance和Traffic两个领域，采用自然预测、反事实配对、对比干预、解释忠实性测试和捷径控制等诊断。主要结果：自然准确率在Finance达51.3%、Traffic达42.1%，但HPC配对正确率仅最高19.2%（Finance）和11.7%（Traffic）；所有模型在Finance序列侧ΔCF为负（-16.4至-6.3）；Traffic序列侧引用率超90%但CSDR低于22%。人类标注者在所有维度上优于LLM，如Finance序列CF-PC人类53.3%对比LLM 20.0%。仅自然任务适配仅在证据选择上有选择性提升，未持续迁移到受控或硬配对行为。

### Q5: 有什么可以进一步探索的点？

TimeLitmus 的核心局限在于其诊断维度仍以“预测正确性”和“因子引用”为主，尚未深入刻画模型内部如何表征事件与序列的交互。未来可探索的方向包括：一是引入机制可解释性方法，如注意力流、激活修补或因果追踪，定位跨模态整合失败发生在哪一层；二是将基准从金融、交通扩展到医疗、能源等高风险领域，检验诊断结论的领域泛化性；三是设计训练干预，例如反事实数据增强或过程监督，验证能否将“识别关系”转化为“应用关系”；四是研究解释忠实性的生成机制，区分事后合理化与真实证据依赖。此外，当前人类评估规模有限，可扩大标注并引入多轮交互协议，考察模型在追问下能否修正不一致行为。这些方向有望把诊断基准从“测量差距”推进到“解释并缩小差距”。

### Q6: 总结一下论文的主要内容

TimeLitmus 是一套面向事件条件时间序列预测的诊断基准，旨在检验大语言模型能否真正融合数值历史与文本事件，而非依赖事件极性、单模态先验或表面线索。论文将问题定义为两个诊断任务：正确预测是否源于事件与序列的条件关系，以及解释中引用的因素是否获得行为支持。基准包含 4,856 条记录，覆盖金融与交通领域，通过受控反事实、难配对对比、解释忠实性干预和捷径控制进行系统评估。对十个代表性 LLM 的实验表明，自然预测准确率显著高估了跨模态理解能力：难配对正确率最高仅 19.2%（金融）和 11.7%（交通），多数模型在交通序列侧引用操纵因素超 90%，但行为支持率低于 22%。人类标注者在匹配诊断上明显优于 LLM，证明这些区分可从输入中恢复。仅自然数据适配只带来选择性增益，无法一致迁移到受控或难配对行为。
