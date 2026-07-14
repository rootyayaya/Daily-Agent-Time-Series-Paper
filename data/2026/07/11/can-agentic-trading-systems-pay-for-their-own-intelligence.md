---
title: "Can Agentic Trading Systems Pay for Their Own Intelligence?"
authors:
  - "Qiqi Duan"
  - "Changlun Li"
  - "Chen Wang"
  - "Fan Zhang"
  - "Mengxiang Wang"
  - "Dayi Miao"
  - "Peixian Ma"
  - "Jiangpeng Yan"
  - "Liyuan Chen"
  - "Shuoling Liu"
  - "Preslav Nakov"
  - "Yuyu Luo"
  - "Nan Tang"
date: "2026-07-11"
arxiv_id: "2607.10286"
arxiv_url: "https://arxiv.org/abs/2607.10286"
pdf_url: "https://arxiv.org/pdf/2607.10286v1"
categories:
  - "cs.AI"
  - "cs.MA"
tags:
  - "LLM Agent"
  - "工具调用"
  - "可追溯诊断"
  - "金融时间序列"
  - "智能体工作流评估"
  - "证据路由"
  - "利润归因"
  - "时序决策系统"
relevance_score: 6.5
---

# Can Agentic Trading Systems Pay for Their Own Intelligence?

## 原始摘要

Large language model (LLM) agents are increasingly used in trading systems, where model reasoning, tool use, and continual decisions incur costs that are expected to produce trading value. Existing evaluations typically report performance metrics, but rarely examine agentic viability: whether dynamic LLM-mediated decisions convert their induced costs into measurable incremental profit. To apply this criterion, we introduce TradeLens, a trace-grounded diagnostic toolkit for evaluating agentic trading systems from their trading records, runtime traces, and deployment configurations. It reconstructs trading trajectories, attributes profit and cost to interpretable evidence, and diagnoses whether and why an agent pays for its own intelligence. We conduct extensive analysis across backbone models, capital scales, trading frequencies, and system architectures, together with deployment discussion. Our results show that viability hinges on intelligence-to-profit conversion: models exhibit different failure patterns, such as poor asset selection in DeepSeek-V3.2 and negative timing in GLM-4.7, while capital scale, trading frequency, and architecture matter only by amplifying or degrading decision-attributed timing value. These findings reframe the evaluation of LLM-based trading agents from capability-centric performance ranking to trace-grounded diagnosis of intelligence-to-profit conversion. Our code is available at https://anonymous.4open.science/r/TradeLens.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

大型语言模型（LLM）智能体正越来越多地被用于交易系统，其模型推理、工具使用和持续决策会产生成本，而这些成本预期应能产生交易价值。现有评估通常报告性能指标，但很少检验“智能体可行性”：即LLM驱动的动态决策能否将其引发的成本转化为可衡量的增量利润。研究背景是，尽管已有系统将LLM用作交易副驾驶或投资组合经理，但评估存在关键盲点：大多数研究仅报告总利润或夏普比率等指标，忽略了利润来源和部署成本对实际利润的影响。现有方法的不足在于，一个盈利的系统可能主要归功于市场走势或初始资产选择，而智能体的动态决策贡献甚微甚至减损价值；同时，高额的推理、工具使用成本若不能产生足够的主动利润，则系统在经济上不可行。因此，本文要解决的核心问题是：如何诊断LLM驱动的交易决策是否将其引发的智能成本（如推理、工具调用）转化为可衡量的增量交易价值，即系统能否“为自己的智能买单”。为此，论文提出了TradeLens，一个基于轨迹的诊断工具包，通过重构交易轨迹、归因利润与成本，来评估智能体交易系统的经济可行性。

### Q2: 有哪些相关研究？

基于论文内容，相关研究主要分为以下几类：

1. **LLM交易智能体方法类**：现有工作将LLM交易智能体从金融分析和信号生成扩展到决策流水线，使用记忆、工具和多智能体协调。本文与这些工作的区别在于，现有评估主要关注能力或总交易表现，而本文引入TradeLens诊断工具包，检查智能体是否能为自身智能付费，即评估决策诱导成本是否转化为可衡量的增量利润。

2. **成本与效率评估类**：近期研究将计算成本纳入模型评估，如成本通过估计获取成功答案的货币成本，高效推理研究思考风格和冗余。这些研究主要将成本视为资源效率变量，而本文强调LLM智能体的成本由决策过程本身（推理、工具使用、记忆访问）诱导，并采用代币经济学视角，将活动与资源使用、交易行动和投资组合结果对齐。

3. **智能体评估与诊断类**：先前工作表明，轨迹证据优于最终任务结果。本文在交易工作流中采用这种轨迹基础视角，诊断决策诱导成本是否转化为交易价值，这是现有评估未充分探索的。

4. **金融绩效归因类**：金融评估长期区分原始收益与可解释收益来源，如夏普比率、制度感知分析、绩效归因（分配、选择、交互效应）。本文采用轻量级归因视图，结合系统成本核算，从决策归因边际而非总利润评估可行性，与仅报告预测准确性或累计收益的金融AI基准和交易智能体研究形成对比。

### Q3: 论文如何解决这个问题？

论文通过提出一个名为TradeLens的溯源诊断工具包，系统性地解决了“智能交易系统能否为其自身智能付费”这一核心问题。核心方法围绕“利润-成本可行性”展开，将评估从性能排名转向可解释的诊断。

整体框架包含两个主要模块：**核算层**和**诊断层**。核算层负责重建交易轨迹，并应用嵌套反事实基线对利润和成本进行归因。利润归因将总利润分解为市场暴露、资产选择和择时决策三部分，其中择时利润被视为智能体干预最直接的贡献。成本归因则细分为LLM推理成本、交易执行成本、基础设施成本和剩余成本，并进一步区分动态成本（随智能体决策变化）与静态成本。基于此，论文定义了**系统可行性**（总利润覆盖总成本）和**智能体可行性**（择时利润覆盖动态成本）两个层级。

诊断层将核算结果转化为可解释的系统级诊断。它首先提取关键指标，检查可行性状态，识别主导失败模式（如DeepSeek-V3.2的资产选择差、GLM-4.7的择时负价值）。然后，通过约束输出合同生成结构化诊断报告，将溯源支持的失败模式（如决策频率与增量利润不匹配）映射到可操作的修订建议，例如减少冗余模型调用或改进执行逻辑。

关键技术在于：1）**利润归因**：通过两个反事实基线（被动市场基准和初始持仓不变基准）分离择时价值；2）**成本归因**：区分动态与静态成本以精准评估智能体干预的净价值；3）**溯源接口**：定义统一的交易结果、运行时轨迹和系统配置输入，使工具包不依赖特定智能体架构。创新点在于将可行性评估从简单的性能指标比较，转变为基于溯源的“智能到利润转化”诊断，揭示了不同模型、资本规模、交易频率和架构对转化效率的影响模式。

### Q4: 论文做了哪些实验？

论文通过回测实验，从四个维度评估了智能交易系统的经济可行性。实验设置基于AI-Trader系统，交易标的为美国流动性股票，时间窗口为2025年12月1日至2026年1月30日，初始资本10万美元。成本涵盖LLM决策、交易执行、基础设施和随机开销四部分，利润归因则分解为市场效应、资产选择和择时效应。

**RQ1（骨干模型）**：对比了GPT-5.2、DeepSeek-V3.2等10个LLM。结果显示，Mistral-large-3是唯一净利和智能利润均为正的模型（净利362.99美元，智能利润833.52美元），主要得益于正向择时效应。Claude Sonnet 4.5虽净利为正（264.36美元），但智能利润为负（-372.86美元），表明系统可行但智能组件未增值。其余模型大多不可行，如DeepSeek-V3.2主要因资产选择差（-1500.44美元），GLM-4.7因负择时效应（-2152.06美元）。

**RQ2（资本规模）**：初始资本从1万到50万美元，发现资本放大模型行为而非稀释成本。DeepSeek-V3.2在所有规模下均亏损，50万时损失扩大；GPT-5.2系统可行但智能利润非线性，50万时主要依赖市场被动暴露。

**RQ3（交易频率）**：比较日频与小时频。日频表现更优，如DeepSeek-V3.2净利从-1222.24提升至29.84美元，GPT-5.2从-585.46升至-198.28美元。高频交易增加了噪音和择时错误。

**RQ4（系统架构）**：对比CoT、AI-Trader和DeepFund。DeepFund表现最佳，为DeepSeek-V3.2唯一实现正净利（412.98美元）和智能利润（328.01美元）的架构，其优势来自正向择时效应（516.62美元），表明复杂架构的价值在于将推理成本转化为更好的择时决策。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在实验设置和评估范围上。未来可从以下方向探索：1) 改进摩擦成本估计，引入更精细的延迟成交日志和滑点模型，提升诊断精度；2) 扩展至更多资产类别（如期货、外汇）和交易场所，验证框架的通用性；3) 深入研究工具使用、多智能体协作和长上下文推理对“智能-利润”转化边界的影响，例如设计更高效的工具调用策略或协调机制；4) 在更广泛的牛熊市周期中评估，并对比更强的非LLM基线（如传统量化策略），以明确LLM的增量价值；5) 将生存力信号与强化学习结合，动态优化智能体系统的决策策略，使其直接面向经济收益进行调优。此外，可引入自动化成本测量机制，减少对用户配置的依赖，并开展更大规模的受控实验来验证诊断结果对实际交易决策的改进效果。

### Q6: 总结一下论文的主要内容

这篇论文提出了一个评估智能交易系统经济可行性的新框架，核心贡献在于将评估从单纯的能力导向转向经济价值导向。问题定义是：现有的LLM交易系统评估仅关注利润或夏普比率，忽略了LLM推理、工具调用等智能行为产生的成本，无法判断这些成本是否创造了足够的增量利润。为此，作者提出了TradeLens诊断工具包，通过重构交易轨迹、归因利润与成本，来诊断系统是否“为智能买单”。方法上，TradeLens将交易记录、运行时轨迹和部署配置统一到一个核算窗口，区分了“系统可行性”（整体是否盈利）和“智能可行性”（LLM决策是否创造足够价值）。主要结论表明，可行性取决于“智能到利润的转化”，不同模型表现出不同的失败模式（如DeepSeek-V3.2资产选择差、GLM-4.7择时负贡献），而资本规模、交易频率等仅通过放大或削弱决策价值来影响结果。这项工作为LLM交易代理的部署提供了可解释的诊断依据，具有重要的实践意义。
