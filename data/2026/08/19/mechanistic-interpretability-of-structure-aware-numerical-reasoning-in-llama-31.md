---
title: "Mechanistic Interpretability of Structure-Aware Numerical Reasoning in LLaMA 3.1 8B"
authors:
  - "Rahul Chowdhury"
  - "Timothy A Rupprecht"
  - "Senhao Cao"
  - "Jiahao Liu"
  - "Octavia Camps"
  - "David Bau"
  - "Pu Zhao"
  - "Yanzhi Wang"
date: "2026-08-19"
arxiv_id: "2608.18419"
arxiv_url: "https://arxiv.org/abs/2608.18419"
pdf_url: "https://arxiv.org/pdf/2608.18419v1"
categories:
  - "cs.LG"
  - "cs.AI"
tags:
  - "Mechanistic Interpretability"
  - "LLM Time-Series Prediction"
  - "In-Context Learning"
  - "Activation Patching"
  - "Probing"
  - "Induction Circuit"
  - "Numerical Reasoning"
  - "First Differences"
relevance_score: 7.5
---

# Mechanistic Interpretability of Structure-Aware Numerical Reasoning in LLaMA 3.1 8B

## 原始摘要

Recent work has shown that large language models (LLMs) exhibit strong numerical sequence modeling capabilities and show promise in time-series prediction. While LLMs display in-context learning capabilities, the mechanisms with which they accomplish time-series prediction remain unclear. Specifically, whether they truly understand the underlying structure, which at a minimum requires reasoning over first differences in the sequence of numbers. To study this, we investigate Llama 3.1-8B from a mechanistic interpretability point of view. Mechanistic interpretability is an emerging field concerned with the reverse engineering of the algorithms learned by neural networks such as LLMs. To assess Llamas' numerical sequence modeling capabilities and to facilitate our mechanistic interpretability analysis, we create a sequence modeling task that cannot be solved without picking up structural cues. Specifically, we sample n random numbers and repeat them with an offset. We find that Llama displays strong performance on our tasks suggesting that it can pick up on the underlying structure. To understand the mechanisms that allow it to do so, we perform probing experiments and activation patching based counterfactual analysis. Probing reveals that the model computes and stores first differences in its internal representations without explicit supervision, indicating that it tracks structural information about the sequence. Activation patching reveals that Llama retrieves the relevant first-difference with a mechanism similar to an induction circuit and subsequently adds it to the current value. Notably, our work represents one of the first studies to identify this form of concept induction in LLMs.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

大型语言模型（LLM）在数值序列建模和时间序列预测中展现出强大能力，但其内部工作机制尚不明确。现有研究多关注LLM的上下文学习能力，却未深入探究其是否真正理解序列的底层结构——至少需要推理相邻数值的一阶差分。本文针对这一空白，从机械可解释性角度研究LLaMA 3.1-8B模型。现有方法主要依赖黑箱评估或浅层分析，无法揭示模型是否通过记忆训练模式而非通用结构推理来完成任务，也无法定位具体计算回路。为此，作者设计了一个必须捕捉结构线索才能解决的序列任务：随机采样n个数字并以偏移量重复，确保无法通过token级复制或简单记忆完成。核心问题是：LLM能否识别并利用序列中的重复差分结构进行外推？其内部是否真正计算和存储一阶差分？又是通过何种机制检索并应用这些差分？通过线性探针和激活修补实验，作者旨在揭示模型是否具备概念归纳能力，即对潜在结构进行推理而非表面模式匹配，从而为理解LLM的抽象推理机制提供首个证据。

### Q2: 有哪些相关研究？

相关研究主要围绕LLM的数值序列建模、时间序列预测及可解释性展开。在方法类工作中，有研究证明LLM可通过上下文学习完成序列补全，但未深入分析其是否依赖记忆或理解时序结构；LLM-Time探索了无需微调即可使预训练LLM适配时间序列预测，而Time-GPT和Lag-Llama则是专门针对时间序列训练的Transformer基础模型，这些工作虽验证了Transformer的序列建模能力，但聚焦于专用模型而非通用LLM。在可解释性类工作中，有研究通过玩具模型分析上下文学习机制，但未检验LLM对未显式训练任务的序列结构推断；另有工作运用机械可解释性识别简单递增序列延续中的共享电路，但仅覆盖熟悉模式，未涉及抽象或不规则数值结构。本文与上述工作的核心区别在于：首次针对通用LLM（Llama 3.1-8B）设计需依赖结构线索（任意一阶差分）才能解决的序列任务，通过探针实验发现模型内部会无监督计算并存储一阶差分，且激活修补揭示其采用类似归纳电路的机制检索相关差分并叠加到当前值。这超越了表面序列扩展，首次识别出LLM中的“概念归纳”机制，填补了从机制层面理解抽象数值推理的空白。

### Q3: 论文如何解决这个问题？

该论文通过构建一个无法仅靠表面统计规律解决的数值序列预测任务，结合机械可解释性分析方法，揭示了LLaMA 3.1-8B内部如何实现结构感知的数值推理。核心方法分为三个层面：

**任务设计**：构造由两段组成的序列——第一段为随机游走（相邻差值在-9到9之间且不重复），第二段完全复用第一段的差值序列。模型必须识别出差值的重复模式，并定位对应位置才能正确预测，排除了记忆或简单插值的可能性。

**探测实验**：在模型内部表示上训练线性探针，检测各层隐藏状态是否编码了“当前差值”信息。结果显示，从第12层开始，差值信息以线性可分离的形式出现在残差流中，且无需显式监督，说明模型自发计算并存储了一阶差分。

**激活修补**：采用因果干预方法，在特定层和注意力头替换激活值，观察预测变化。发现模型通过类似“归纳头”的机制工作：后段序列的某个注意力头会检索前段中相同差值模式出现的位置，然后将该位置的差值“复制”到当前token的表示上，最后通过加法运算完成预测。

**创新点**：首次在LLM中识别出“概念归纳”机制——模型不仅复制token，还复制抽象的数值关系（差值）。整体架构验证了Transformer通过“差值追踪-模式匹配-加法运算”的三步流水线实现结构推理，而非简单的表面模式匹配。

### Q4: 论文做了哪些实验？

实验基于自建的数值序列预测任务，使用LLaMA 3.1-8B模型（32层、32注意力头）进行机制可解释性分析。数据集包含10,000条序列，每条由59个token组成（含BOS和逗号），要求模型预测第30个数字。序列设计为两段式：前段为随机游走（差值唯一），后段重复前段的差值序列，迫使模型必须识别结构规律才能正确预测。

实验设置包括三类分析：1）**行为评估**：直接测试模型预测性能，采用MAE和R²指标，模型取得MAE=4.2748、R²=0.9958，表明能有效捕捉序列结构；2）**探针实验**：训练线性探针检测模型内部表示是否编码一阶差分信息，结果显示模型在无显式监督下自发计算并存储差值，验证了结构追踪能力；3）**激活修补**：基于反事实分析定位关键计算回路，发现模型通过类似归纳头的机制检索相关差值并加到当前值上，该机制在特定注意力层中实现。

对比方法方面，论文未设置传统基线，而是通过消融性干预（如修补特定层激活）验证因果贡献。主要结果揭示了LLaMA 3.1-8B具备概念归纳能力，这是首次在LLM中识别出此类结构感知推理机制。所有实验借助NNsight和NDIF框架完成激活追踪与干预，确保分析的可控性和可重复性。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在任务设计相对简化，仅基于随机数加偏移的线性结构，未能覆盖更复杂的非线性或周期性时间序列模式。未来可从以下方向深入探索：一是将机制分析扩展到多步依赖、噪声干扰或混合结构序列，检验模型是否仍能提取并组合多个一阶差分；二是结合因果干预方法，定位更精细的注意力头或MLP子层，构建完整的计算图，以区分“概念归纳”与通用模式匹配；三是探索该机制是否可迁移至其他推理任务，如算术运算、逻辑推理或代码执行中的状态追踪。此外，可尝试通过微调或提示工程强化这种结构感知能力，或设计更严格的对照实验，排除数据分布偏差对结论的影响。最后，将可解释性发现应用于实际时间序列预测，验证其在金融或工业场景中的鲁棒性与泛化性，是极具价值的落地方向。

### Q6: 总结一下论文的主要内容

本研究针对大语言模型（LLM）在数值序列建模中的机制可解释性问题，以LLaMA 3.1-8B为对象，设计了一个必须依赖结构线索才能解决的序列任务：采样随机数并附加偏移重复出现。研究发现，模型能有效捕捉底层结构并准确预测。通过探针实验，作者发现模型在无显式监督下，内部表征中计算并存储了序列的一阶差分，表明其追踪结构信息。激活替换的反事实分析进一步揭示，模型通过类似归纳回路的机制检索相关一阶差分，并将其加到当前值上完成预测。这是首次在LLM中识别出此类概念归纳形式，证明LLM虽未专门训练高精度数值任务，却涌现出结构外推能力，为理解其潜在推理机制及拓展至其他依赖隐结构的推理任务提供了重要基础。
