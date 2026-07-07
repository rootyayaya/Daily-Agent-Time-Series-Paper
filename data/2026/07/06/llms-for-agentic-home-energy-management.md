---
title: "LLMs for Agentic Home Energy Management"
authors:
  - "Sokipriala Jonah"
date: "2026-07-06"
arxiv_id: "2607.04569"
arxiv_url: "https://arxiv.org/abs/2607.04569"
pdf_url: "https://arxiv.org/pdf/2607.04569v1"
github_url: "https://github.com/sokistar24/ecohome-energy-agent"
categories:
  - "eess.SY"
tags:
  - "Agentic Time Series"
  - "LLM Agent"
  - "tool calling"
  - "ReAct"
  - "RAG"
  - "home energy management"
  - "time series scheduling"
  - "natural language interface"
  - "multi-appliance scheduling"
  - "MILP ground truth"
relevance_score: 7.5
---

# LLMs for Agentic Home Energy Management

## 原始摘要

Home Energy Management Systems (HEMS) can reduce residential electricity costs and support demand response, but adoption is limited by the difficulty of translating household preferences into technical scheduling constraints. This paper evaluates whether large language model (LLM) agents can provide a practical natural-language interface for multi-appliance home energy scheduling. We present a tool-calling ReAct agent that uses live half-hourly Octopus Agile prices, weather forecasts, photovoltaic generation estimates, household usage data, and a retrieval-augmented knowledge base to schedule flexible loads against a mixed-integer linear programming (MILP) ground truth. Three commercial models, GPT-4o-mini, Gemini 2.5 Flash, and Claude Sonnet 4.6, are benchmarked across tariff days, constraint-conflict scenarios, weather-aware solar co-optimization, and week-long deployment. With native function calling, all models achieve 100% scheduling success and near-MILP optimality, while text-parsed action interfaces sharply reduce reliability. Constraint testing shows that cost-optimal and safety-optimal models differ: Claude is strongest under infeasibility and power-cap conflicts, while GPT-4o-mini is most efficient. Over a simulated week, agents capture 96.7-98.0% of oracle savings, projecting approximately GBP 1,270 annual savings over an off-peak timer baseline. Code and a live demonstration are available at https://github.com/sokistar24/ecohome-energy-agent and https://www.ecohomeagent.com/.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

家庭能源管理系统（HEMS）能降低居民电费并支持需求响应，但实际部署不足。现有方法的主要瓶颈在于用户交互负担：传统HEMS要求用户将日常偏好（如何时使用洗衣机）转化为技术调度参数（如运行时间窗口、功率限制），这对非专业用户极不友好，阻碍了大规模采用。虽然已有研究尝试用大语言模型（LLM）作为接口层，但现有工作存在四个关键不足：1）仅测试开源模型，且部分模型协调失败，商业模型潜力未知；2）仅基于日前电价优化，忽略了带屋顶光伏（PV）家庭需考虑天气感知的净成本优化；3）仅用单日数据评估，缺乏对价格波动鲁棒性的统计检验；4）未测试用户约束冲突场景（如功率上限、截止时间冲突），导致安全盲区。本文旨在解决上述问题，提出一个基于工具调用ReAct智能体的HEMS，使用商业模型（GPT-4o-mini、Gemini 2.5 Flash、Claude Sonnet 4.6）实现自然语言接口的多设备调度。核心目标是验证：在结构化工具接口下，更强的商业模型能否实现接近混合整数线性规划（MILP）最优解的调度性能，同时处理约束冲突、天气感知光伏协同优化，并在多日滚动部署中保持鲁棒性。

### Q2: 有哪些相关研究？

相关研究主要围绕LLM在家庭能源管理中的应用，可分为以下几类：

**方法类**：ReAct模式是主流实现方式，通过交替推理与工具调用生成可追溯轨迹。本文采用该模式，并重点对比了原生函数调用与文本解析接口的可靠性差异。El-Makroum等人首次让LLM作为自主编排器直接提交调度决策，但仅测试了开源模型，且优化目标单一（仅电价），未考虑天气、光伏等约束冲突场景。

**应用类**：现有工作涵盖多种角色：作为代码生成器（如EV充电优化）、诊断助手（建筑运维）、控制器（商用楼宇HVAC）、决策评估器（住宅改造建议）等。多数系统将LLM作为传统优化器的接口或预处理层，而非直接决策者。本文则让LLM直接调度多设备，并整合实时电价、天气预报、光伏发电等多元数据。

**评测类**：本文填补了现有评估的空白：El-Makroum等仅用单日电价测试，未考虑约束冲突；多数研究缺乏统计显著性检验。本文在12天、1100+次运行中，对三个商业模型（GPT-4o-mini、Gemini 2.5 Flash、Claude Sonnet 4.6）进行了多电价场景、天气感知光伏协同优化、约束冲突压力测试及一周部署评估，并报告了统计显著性。

### Q3: 论文如何解决这个问题？

该论文提出了一种基于大语言模型（LLM）代理的家居能源管理系统，通过自然语言接口解决用户偏好难以转化为技术调度约束的问题。核心方法采用**工具调用型ReAct代理**架构，基于LangGraph框架实现“推理-行动”循环：代理接收自然语言请求后，自主选择工具、观察结果并迭代，直至生成调度方案。

**整体框架**包含三大模块：
1. **LLM核心**：评估了GPT-4o-mini、Gemini 2.5 Flash和Claude Sonnet 4.6三种商业模型，通过原生函数调用接口实现结构化工具调用，温度参数固定为0以保证可重复性。
2. **工具层**：提供6个专用工具——电价检索（Octopus Agile实时半小时间隔电价）、天气预报（Open-Meteo）、光伏发电预测（基于辐照度和温度）、最优时段计算、设备调度提交、不可行性报告。实验1仅使用电价相关工具，其他实验使用完整工具集。
3. **知识增强**：集成检索增强生成（RAG）向量库存储节能文档，同时连接家庭SQLite数据库存储用电和光伏数据。

**关键技术**包括：
- **时间锚定机制**：显式声明评估日期时间，所有工具基于该固定时间解析相对日期（如“明天”），确保跨模型可重复性。
- **双接口对比**：比较原生函数调用（结构化输出）与文本解析ReAct动作（自由文本提取）两种交互方式，发现前者实现100%调度成功率。
- **约束处理策略**：当请求不可满足时，代理调用不可行性报告工具而非强行调度，区分成本最优与安全最优模型行为。

**创新点**在于：1）单一代理而非分层架构实现多设备协调；2）将实时电价、天气预报、光伏预测等异构数据源统一为工具接口；3）通过约束冲突测试揭示不同模型在成本优化与安全约束间的权衡特性。实验表明，代理在模拟周内捕获96.7-98.0%的oracle节省，年省约1270英镑。

### Q4: 论文做了哪些实验？

论文围绕LLM智能体在家庭能源管理中的应用，设计了一系列实验。实验设置包括：使用工具调用的ReAct智能体，基于Octopus Agile实时电价、天气预报、光伏发电估计、家庭用电数据和检索增强知识库，以混合整数线性规划（MILP）为基准。数据集为2026年4月20日至6月20日的Agile电价存档，按波动性分层。对比方法包括静态非高峰定时器、即时启动策略和贪婪最便宜单槽启发式算法，以及MILP oracle。主要结果：在实验1中，所有模型通过原生函数调用实现100%调度成功率和接近MILP的最优性，而文本解析动作界面可靠性显著下降。实验2显示，约束冲突下模型表现不同：Claude在不可行性和功率上限冲突中最强，GPT-4o-mini效率最高。实验3中，与光伏预测协同优化降低了净成本并提高了自消耗率，且对预测误差具有鲁棒性。实验4a的周级部署中，智能体捕获了96.7-98.0%的oracle节省，预计年节省约1270英镑。实验4b的周级联合规划测试中，冠军模型实现了接近最优的调度。关键数据指标包括调度成功率、最优性率、约束违反率、成本节省比例等。

### Q5: 有什么可以进一步探索的点？

论文的局限性在于：实验仅基于英国Octopus Agile动态电价和典型家庭场景，未验证模型在更复杂电价结构、多区域协调或极端天气下的鲁棒性；MILP作为ground truth虽提供最优解，但忽略了用户行为随机性和设备退化等现实因素；LLM agent的调度决策完全依赖工具调用，缺乏对用户长期偏好的主动学习能力。未来可探索：1）引入强化学习使agent能在线适应家庭用电模式变化；2）设计多agent协作框架处理社区级需求响应，平衡个体与群体利益；3）结合因果推理增强agent在罕见约束冲突下的可解释性，例如解释为何选择成本最优而非安全方案；4）开发轻量化本地模型以解决隐私和延迟问题，同时保持调度性能。

### Q6: 总结一下论文的主要内容

这篇论文提出并评估了一种基于大语言模型（LLM）的智能体家庭能源管理系统（HEMS），旨在解决传统HEMS因用户需将日常偏好转化为技术参数而导致的采用率低的问题。核心贡献在于：1）提供了一个多模型基准测试，对比了GPT-4o-mini、Gemini 2.5 Flash和Claude Sonnet 4.6在多种电价波动场景下的调度性能；2）引入了约束冲突压力测试套件，评估模型在成本最优与用户安全约束冲突时的行为；3）将调度目标从纯电价优化扩展至考虑光伏自消纳的净成本优化。方法上，该系统采用工具调用型ReAct智能体，结合实时电价、天气预报、光伏发电估计及检索增强知识库，以混合整数线性规划（MILP）为基准。主要结论是：所有商业模型在原生函数调用下均实现100%调度成功率且接近MILP最优，但文本解析接口会显著降低可靠性；Claude在不可行约束和功率上限冲突下表现最强，而GPT-4o-mini效率最高。模拟一周内，智能体捕获了96.7-98.0%的基准节省，预计年节省约1270英镑。该研究证明了LLM智能体作为实用自然语言接口的可行性，推动了家庭能源管理的智能化与用户友好化。
