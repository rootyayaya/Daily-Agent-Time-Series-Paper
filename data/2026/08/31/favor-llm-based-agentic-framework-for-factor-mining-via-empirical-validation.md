---
title: "FaVOR: LLM-Based Agentic Framework for Factor Mining via Empirical Validation"
authors:
  - "Hyeonjin Kim"
  - "Minseok Kim"
  - "Seunghyeon Jung"
  - "Sujin Pyo"
  - "Huisu Jang"
  - "Woojin Lee"
date: "2026-08-31"
arxiv_id: "2608.30192"
arxiv_url: "https://arxiv.org/abs/2608.30192"
pdf_url: "https://arxiv.org/pdf/2608.30192v1"
github_url: "https://github.com/damilab/FaVOR"
categories:
  - "cs.AI"
  - "cs.CE"
tags:
  - "LLM Agent"
  - "多智能体系统"
  - "因子挖掘"
  - "假设验证"
  - "可解释性"
  - "金融时间序列"
  - "验证循环"
  - "经济合理性"
  - "鲁棒性"
relevance_score: 7.5
---

# FaVOR: LLM-Based Agentic Framework for Factor Mining via Empirical Validation

## 原始摘要

Traditional finance relies on experts to hand-craft factors through a principled process grounded in economic rationale. Recent LLM-based multi-agent systems have automated this process, scaling factor mining far beyond manual effort. However, these automated approaches optimize directly for returns and rarely check whether a generated factor still expresses the economic hypothesis that motivated it. We identify this inconsistency between mathematical form and economic meaning as a structural failure mode of return-oriented automation. The resulting factors blur the line between real signals and spurious correlations and break down across regime shifts. We propose FaVOR (Factor Validation through Observable Reasoning), an agentic framework that restructures factor mining around hypothesis-level evidence rather than return outcomes. In place of the standard hypothesis-to-formula leap, FaVOR enforces a three-stage consistency loop tying mathematical form to economic rationale throughout. (1) Decomposition splits a broad economic hypothesis into independent observable conditions. (2) Validation checks whether each factor reflects its intended condition. (3) Integration merges them into a composite whose structure remains interpretable. On the CSI 500 and S&P 500 in 2025, FaVOR outperforms existing baselines while remaining effective across regimes. FaVOR shows that hypothesis-grounded factor discovery produces signals that are interpretable by construction, regime-robust, and economically faithful. The code is available at https://github.com/damilab/FaVOR.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

传统因子挖掘依赖专家手工构建，虽具备经济可解释性但扩展性受限。近年基于LLM的多智能体系统虽能自动化生成海量因子，却存在一个结构性缺陷：这些方法直接以预测收益为优化目标，几乎不验证生成因子是否仍表达其初始经济假设。这导致数学形式与经济含义脱节——过拟合噪声的公式与基于真实经济机制的因子难以区分，在样本内表现优异但市场风格切换时迅速失效。现有LLM管线返回完整公式却不暴露中间推理过程，使得验证“公式-假设”映射关系极为困难。FaVOR的核心贡献在于将因子挖掘重构为假设层面的证据验证而非收益导向的优化：通过分解（将宽泛经济假设拆分为可观测市场条件）、验证（检查因子是否反映预期条件）、整合（合并通过验证的因子为可解释复合因子）三阶段一致性循环，强制数学形式与经济逻辑全程绑定。在CSI 500和S&P 500的2025年样本外测试中，FaVOR在保持跨市场稳健性的同时超越现有基线，证明假设驱动的因子发现能产生结构性可解释、经济忠实且适应不同市场环境的信号。

### Q2: 有哪些相关研究？

传统因子投资研究强调因子应表达明确的经济机制，而非仅优化收益。相关基础工作包括：Fama-French三因子/五因子模型（市场、规模、价值、盈利、投资）、动量因子研究、以及将估值比率与预期收益关联的文献。这些工作依赖专家手工验证，因子可解释但无法规模化。

在自动化因子挖掘方面，近期LLM方法显著推进了该领域：FAMA引入样本选择和经验机制降低冗余；GPT-4被证明能通过金融推理合成有效因子；多智能体框架如Alpha-GPT将研究者想法转化为公式并优化，RD-Agent-Quant联合优化因子与机器学习模型，AlphaAgent通过正则化探索增强假设一致性。这些方法主要基于语义匹配或收益表现评估因子，缺乏对因子是否真实反映其经济假设的实证检验。

FaVOR与上述工作的核心区别在于：它将传统金融的实证验证逻辑引入自动化流程，通过“分解-验证-整合”三阶段循环，强制因子的数学形式与经济假设保持一致。相比现有方法直接优化收益，FaVOR以假设级证据为优化目标，从而避免虚假相关和跨体制失效问题，在保持可解释性的同时提升稳健性。

### Q3: 论文如何解决这个问题？

FaVOR通过一个三阶段一致性循环框架，将因子挖掘从“收益导向”重构为“假设证据导向”，核心创新在于用可观测的市场条件验证替代直接的收益优化。

**整体框架**包含三个核心模块：  
1. **分解阶段**：假设智能体\(\mathcal{A}_H\)将人类市场洞察转化为自然语言经济假设\(h\)，观察智能体\(\mathcal{A}_O\)将其分解为\(m\)个独立可观测的市场条件\(\{o_i\}\)，因子智能体\(\mathcal{A}_F\)为每个条件生成多个候选因子公式，且算子限定在预定义集合内以保证可解释性。

2. **验证阶段**：这是框架的关键创新。验证智能体\(\mathcal{A}_V\)不检查因子对未来收益的预测能力，而是检验因子值是否真实反映其对应的市场条件。具体做法是：在训练集上按因子值将股票分入五分位桶，计算每个桶内四类OHLCV变量（日内收益、价格区间、收盘位置、成交量）的统计分布特征，然后通过四条确定性规则（中心趋势系统性偏移、尾部离散度变化、互补统计量一致性、语义匹配）进行一致性判定。LLM仅负责将文本条件映射到相关变量及预期方向，最终通过/失败判定是确定性的，避免了LLM的随机性。

3. **整合阶段**：对每个条件保留的验证通过因子做笛卡尔积形成组合，通过“方向选择性”检验——逐步收紧入场阈值\(\sigma\)，观察组合信号的平均收益和胜率是否随选择性提高而改善。只有通过该结构性筛选的组合才被保留，随后在验证集上用Optuna优化各因子独立阈值（目标为Calmar比率），最终在测试集上回测。

**创新点**在于：将因子验证从收益预测转向假设一致性检验，通过量化分布证据确保因子在数学形式上忠实表达经济含义；三阶段循环使最终因子组合天然具备可解释性和跨市场状态的稳健性；外循环仅记录假设ID和平均信息比等摘要信息，防止过拟合。

### Q4: 论文做了哪些实验？

论文在CSI 500（中国A股）和S&P 500（美国股市）两个市场进行了回测实验，数据来自Baostock和Yahoo Finance，时间跨度为2022-2025年，其中2022-2023年为训练集，2024年为验证集，2025年专门用于样本外测试。回测仅使用每日OHLCV数据，并计入交易成本（CSI 500买入0.0005、卖出0.0015；S&P 500仅卖出0.0005）。

对比方法涵盖三类：ML/DL方法（Linear、XGBoost、LightGBM、MLP、Transformer）、强化学习方法（AlphaForge、AlphaQCM）以及基于LLM的方法（RD-Agent、AlphaAgent）。评估指标包括年化收益（AR）、信息比率（IR）、最大回撤（MDD）和累计收益（CR）。

主要结果显示FaVOR在两个市场均取得最优表现：CSI 500上AR为0.2067、IR为1.5295、MDD为-0.0853、CR为0.2225；S&P 500上AR为0.1062、IR为1.1315、MDD为-0.0443、CR为0.1123。消融实验表明，移除因子验证阶段（Stage 2）会使MDD翻倍以上，移除因子整合阶段（Stage 3）则导致收益大幅恶化。此外，论文还测试了不同LLM骨干模型（GPT-4o、GPT-5.4-mini、Gemini-2.5-Flash、Claude-Sonnet-4.6、Llama-3.3-70B、Qwen3-235B）的鲁棒性，FaVOR在所有骨干模型下均保持正收益。

### Q5: 有什么可以进一步探索的点？

FaVOR在因子挖掘中引入了假设级验证，但仍存在几个可深挖的方向。首先，其方向一致性选择标准天然排斥反转类信号（如极端分位处的逆向模式），这类因子在阈值收紧时方向翻转，但可能蕴含独立的经济逻辑。未来可设计更灵活的验证框架，区分“方向翻转”与“逻辑失效”，或引入分段一致性检验。其次，当前回测基于日频数据，假设市场冲击可忽略，但若拓展至高频交易，需构建高保真执行模拟器，纳入滑点、订单簿动态和容量约束，以评估因子在真实摩擦下的稳健性。此外，FaVOR的验证环节依赖可观测条件的设计，这本身可能引入主观偏差，可探索用因果推断或反事实生成来自动化条件构建，减少人工干预。最后，跨市场（如A股与美股）的迁移性虽已验证，但跨资产类别（如商品、加密货币）和跨周期（如牛熊切换）的适应性尚未充分测试，可引入在线学习机制，让代理根据市场状态动态调整验证阈值和集成权重，进一步提升鲁棒性。

### Q6: 总结一下论文的主要内容

FaVOR提出了一种基于LLM智能体的因子挖掘框架，旨在解决传统自动化因子挖掘中数学形式与经济假设脱节的结构性缺陷。传统方法直接优化收益，易产生伪相关信号且缺乏跨市场状态稳健性。FaVOR将因子挖掘重构为围绕假设级证据的三阶段一致性循环：首先将宽泛经济假设分解为独立可观测条件，其次验证每个因子是否真实反映其目标条件，最后将有效因子整合为结构可解释的复合因子。在2025年CSI 500和S&P 500上的实验表明，FaVOR优于现有基线，且在不同市场状态下保持有效。消融实验证实了验证与整合阶段的关键作用。该框架的核心贡献在于使因子发现过程天然具备可解释性、跨状态稳健性和经济忠实性，为可解释时间序列分析提供了新范式。
