---
title: "FinReportBench: Measuring and Improving Institution-Grade Financial Report Generation"
authors:
  - "Yinghao Tang"
  - "Tan Zhenwei"
  - "Yiyao Wang"
  - "Wanli Gu"
  - "Xiaolu Zhang"
  - "Jun Zhou"
  - "Wei Chen"
date: "2026-08-05"
arxiv_id: "2608.04374"
arxiv_url: "https://arxiv.org/abs/2608.04374"
pdf_url: "https://arxiv.org/pdf/2608.04374v1"
github_url: "https://github.com/MisterBrookT/finreportbench"
categories:
  - "cs.CL"
  - "cs.AI"
tags:
  - "financial report generation"
  - "benchmark"
  - "rubric-based evaluation"
  - "skill distillation"
  - "self-review"
  - "LLM evaluation"
  - "institution-grade reporting"
relevance_score: 7.5
---

# FinReportBench: Measuring and Improving Institution-Grade Financial Report Generation

## 原始摘要

Large language models can produce fluent financial analysis, but fluency alone does not establish whether a report is suitable for institutional delivery. We introduce FinReportBench, an expert-grounded benchmark for measuring and improving institution-grade financial report generation. Expert review reveals recurring gaps in report identity, institutional components, source discipline, and visual delivery. We derive a 35-item rubric through expert partial orders, multimodal evidence, and audits of decision boundaries, covering deliverability, report identity, and institutional completeness. Starting from 10,000 balanced Chinese and English financial-research source records, we curate 244 bilingual tasks across three research objects and two input tiers. Each task separates the public query, reconstructed research trajectory, and hidden source packet. Three independent judge families reproduce the expert partial order at near-ceiling rates, showing that bounded, observable criteria support reliable evaluation. Across nine model families, basic deliverability is nearly saturated, while report identity and institutional completeness remain the primary bottlenecks. The largest cross-model gaps concern generation-trace control, information density, and data discipline rather than basic report framing. We then use benchmark-guided skill distillation to turn recurrent failures into reusable generation and self-review constraints. Across five model families, the evolved skill improves mean G1 by 33.85 points and mean G2 by 13.83 points over paired no-skill runs while preserving G0 for every pair. Code and benchmark artifacts are available at https://github.com/MisterBrookT/finreportbench.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

大型语言模型虽能生成流畅的金融分析文本，但流畅性并不等同于报告达到机构级交付标准。现有金融报告生成基准（如FinSight、Cogito）的评价维度过于宽泛粗粒度，仅关注事实准确性、信息有效性、展示质量等整体指标，无法识别导致报告无法用于机构交付的具体缺陷。例如，一份缺乏发布方、分析师身份和稳定页码系统的网页式报告，仍可能因图表精美而获得高分。初步专家访谈显示，三位资深金融专家对75份模型生成产物全部给出最低满意度1分，核心短板集中在专业报告惯例与视觉呈现，包括首页框架、机构身份、页码系统、合规组件和来源展示。为此，本文提出FinReportBench，首个专门衡量生成报告是否达到机构交付标准的基准。构建该基准面临三大挑战：将专家隐性知识转化为可复现的评分规则、从最终报告反推原始客户需求与研究轨迹、以及提供可指导改进的具体失败证据而非笼统分数。核心问题是建立一套细粒度、可操作、专家对齐的评估体系，以定位并改进模型在机构级金融报告生成中的系统性缺陷。

### Q2: 有哪些相关研究？

相关研究可分为三类。**评测类**：现有金融NLP基准多聚焦于表格、文件和对话上的问答与多模态推理，如FinQA、DocFinQA等，虽能评估事实或分析维度，但无法识别导致专业拒收的具体缺陷。FinReportBench则通过专家推导的细粒度35项规则，对完整渲染报告进行可观测评估，弥补了这一空白。**方法类**：近期工作从资源或执行失败中提取可复用Agent技能，并在保留任务上选择修订方案。本文借鉴此思路，将反复出现的条目级失败转化为紧凑的生产规则，并通过外部验证防止负迁移，应用于机构级报告生成。**应用类**：金融报告系统虽引入广泛的事实、分析和呈现维度，但缺乏对机构身份、来源纪律和视觉交付的系统性检查。本文通过专家访谈揭示的层级审查逻辑（G0可交付性→G1报告身份→G2机构完整性），以及重建研究轨迹的输入设计，与现有系统形成本质区别。此外，与强调网页交互和检索的通用Agent基准不同，本文聚焦于从有组织的证据状态继续生成，而非短查询直接生成。

### Q3: 论文如何解决这个问题？

FinReportBench通过构建一个专家驱动的分层评估基准和技能蒸馏机制来解决机构级金融报告生成的质量问题。整体框架包含三大核心模块：

**数据集构建**：从10,000篇中英文真实研究报告（东方财富和世界银行）出发，通过反向合成恢复合理的用户查询，经LLM审计过滤不自然请求和泄漏问题，最终精选244个双语任务。每个任务将公开查询、重建的研究轨迹和隐藏源文档分离，确保评估的真实性和防泄漏性。

**分层评估体系**：专家通过稀疏偏好排序和对比性证据挖掘，归纳出35项可观察的评估标准，分为三个层级——G0可交付性（4项基础检查）、G1报告身份（4项机构研究报告识别）、G2机构完整性（27项涵盖封面、合规、信息密度、图表规范等）。评估采用层级有效性原则，G0失败则总分为零，G1弱会折减G2得分，避免后期优势补偿前期缺陷。

**基准引导的技能进化**：在外部案例上迭代诊断模型失败模式，由优化器将跨模型复现的失败转化为规划、写作、审查三部分的可复用约束规则。每个候选技能需通过查询不相交的外部验证，且必须改善目标项而不降低其他指标。最终冻结的最优技能在锁定的测试集上与无技能基线配对评估，验证其通用性。

创新点在于：将专家知识转化为可观察、可审计的细粒度标准；通过技能蒸馏将评估反馈转化为轻量级提示约束而非模型微调；采用层级评分机制模拟真实机构审查流程。实验表明该方法在保持G0不降的前提下，平均提升G1达33.85分、G2达13.83分。

### Q4: 论文做了哪些实验？

实验围绕FinReportBench基准展开，包含三部分。首先，对9个模型家族（DeepSeek V4 Flash/Pro、Qwen 3.7 Max、GLM-5.2、Kimi K2.6、MiniMax M2.5/M2.7/M3、Qwen 3.6 27B）在无技能条件下评估，使用GPT-5.6 Luna按35项评分细则打分。结果显示基本可交付性（G0）接近饱和，但报告身份（G1）和机构完整性（G2）是主要瓶颈。MiniMax M2.7总分最高（22.6），G1为40.0，G2为46.6；跨模型最大差异在生成轨迹控制（31.1分）、信息密度（13.4分）和数据纪律（13.2分）。

其次，进行专家校准验证：三位资深专家对18份报告建立共识偏序，生成71个成对约束。三个评估器家族（GPT5.6-Luna、GPT5.6-Terra、Grok-4.5）满足98.6%-100%的约束，Terra重复运行与参考运行在97%的项目决策上一致，评分相关性达0.949-0.981。切片分析显示语言是排名变化最大来源（中文ρ=0.650），而查询类型和对象间排名稳定。

最后，通过基准引导的技能蒸馏，从5个外部发现案例生成技能K*，在5个验证案例上筛选，再对5个模型进行100次配对比较。K*使平均G1提升33.85分（95% CI: 31.17-36.63），G2提升13.83分（12.65-15.02），同时所有配对G0保持不变，各模型G1增益范围26.39-41.86分，G2增益11.22-16.98分。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是基准规模有限（244个双语任务），难以覆盖金融报告的全部场景和语言变体；二是评估依赖专家定义的标准，可能忽略非专家用户或监管机构的差异化需求；三是技能蒸馏方法虽有效，但未深入探索其泛化边界和长期稳定性。

未来可从以下方向拓展：第一，扩大基准覆盖范围，纳入更多资产类别、报告类型和低资源语言，增强评估的生态效度；第二，引入动态专家反馈机制，让评估标准随市场实践和监管要求持续演化；第三，探索将技能蒸馏与在线强化学习结合，使模型在真实反馈中自适应调整生成策略；第四，研究报告生成中的多模态对齐问题，特别是图表与文本的语义一致性；第五，开发可解释的失败诊断工具，帮助用户定位具体缺陷并理解模型决策边界。此外，可尝试将基准用于预训练阶段的目标优化，而非仅作为后训练微调信号，从而更根本地提升模型的专业报告生成能力。

### Q6: 总结一下论文的主要内容

FinReportBench是一个面向机构级金融报告生成的专家基准，旨在解决大语言模型虽能生成流畅分析但缺乏机构交付适用性的问题。论文通过专家评审识别出报告身份、机构组件、来源纪律和视觉呈现四类关键缺陷，并基于专家偏序、多模态证据和决策边界审计构建了35项评估细则。研究从10,000条中英文金融研究记录中精选出244个双语任务，涵盖三类研究对象和两种输入层级，每个任务分离公开查询、重构研究轨迹和隐藏源包。三个独立评判家族以接近上限的比率复现专家偏序，验证了有界可观察标准的可靠性。实验表明，九个模型系列在基本可交付性上已近饱和，但报告身份和机构完整性仍是主要瓶颈，最大跨模型差距集中在生成轨迹控制、信息密度和数据纪律。最后，论文利用基准引导的技能蒸馏，将反复出现的失败转化为可复用的生成与自审约束，在五个模型系列上平均提升G1达33.85分、G2达13.83分，同时保持G0不变。
