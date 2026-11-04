---
title: "GlucoAgent: Personalized Glucose Forecasting from Multimodal Personal Context"
authors:
  - "Xingzhi Sun"
  - "Hyo Jin Kim"
  - "Zhiyuan Wang"
  - "Hao Chen"
date: "2026-11-03"
arxiv_id: "2611.04126"
arxiv_url: "https://arxiv.org/abs/2611.04126"
pdf_url: "https://arxiv.org/pdf/2611.04126v1"
categories:
  - "cs.AI"
tags:
  - "LLM Agent"
  - "多模态时序预测"
  - "代码生成与执行"
  - "个性化健康监测"
  - "可解释预测"
  - "证据支持"
  - "时序基础模型对比"
  - "连续血糖监测"
relevance_score: 8.5
---

# GlucoAgent: Personalized Glucose Forecasting from Multimodal Personal Context

## 原始摘要

Continuous glucose monitors, smartwatches, meal logs, and health profiles form a rich multimodal personal context that can significantly enhance glucose forecasting. However, existing methods struggle to effectively utilize these signals to improve glucose prediction because the relevance of different modalities varies drastically across individuals and time. We present GlucoAgent, an LLM-based agentic system that addresses this challenge through dynamic, case-by-case analysis at inference time. For each forecast, GlucoAgent writes and runs code over an individual's multimodal context and returns predictions with a reason and supporting evidence. The generated programs are highly diverse, ranging from retrieving similar past meals to fitting and back-testing physiological and statistical models. On CGMacros, a multimodal glucose dataset, GlucoAgent outperforms time series foundation models on every forecasting horizon, achieving an average RMSE of 22.5 mg/dL compared to 23.5 mg/dL of Chronos-2, the leading multimodal time series foundation model. Furthermore, GlucoAgent is highly effective at leveraging multimodal data. The addition of multimodal data reduces its average RMSE by 1.4 mg/dL (24.0 mg/dL to 22.5 mg/dL), compared to a marginal 0.3 mg/dL (23.8 mg/dL to 23.5 mg/dL) improvement for Chronos-2. This advantage is most pronounced in challenging post-meal windows, where GlucoAgent uses multimodal context to reduce 60-minute forecast RMSE by 4.6 mg/dL (31.0 mg/dL to 26.5 mg/dL), far exceeding the 0.8 mg/dL (31.9 mg/dL to 31.1 mg/dL) reduction achieved by Chronos-2.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注短时程连续血糖监测（CGM）预测问题，即预测未来30至120分钟的血糖值，这对个性化营养管理和自动胰岛素输注等应用至关重要。现有方法包括生理模型、自回归模型、神经网络和通用时间序列基础模型，也有研究通过为每位受试者单独训练模型或按验证误差选择架构来实现个性化。智能手表、饮食记录和健康档案等多模态个人上下文本应显著提升预测效果，但现有方法在加入胰岛素、碳水、可穿戴信号等上下文后改进十分有限，例如MetaboNet-Bench中30分钟RMSE仅降低0.13至0.71 mg/dL。作者认为这反映出多模态上下文被严重低估利用，其核心难点在于不同模态的预测价值因人、因时刻而剧烈变化：临近进餐时历史餐食响应更有用，平静时段则近期血糖动态更重要。而现有方法在开发阶段就固定了模型类别和上下文进入方式，无法在预测时按个案构建分析。因此本文提出基于LLM的智能体系统GlucoAgent，在每次预测时针对个体多模态上下文动态编写并运行代码，构建N-of-1式的个案分析，并随预测返回理由与支持证据，以解决多模态上下文利用不足和预测缺乏可解释性的问题。

### Q2: 有哪些相关研究？

现有研究主要可分为三类。方法类方面，葡萄糖预测工作包括葡萄糖专用预训练模型和通用时间序列基础模型（如TimesFM-2.5在GlucoFM-Bench上零样本误差接近全监督LSTM），以及为每个受试者单独训练、按验证误差选模型或在线更新线性模型的个性化方法；多模态预测器则引入心率、活动、餐食照片或健康记录等信息，MetaboNet-Bench还评估了胰岛素与碳水输入，但提升有限，CGMacros上亦有按人微调的多模态餐后预测器及据此提出饮食建议的LLM智能体。语言模型与智能体用于时间序列方面，包括提示或微调式预测、自然语言描述与检索增强预测，以及ReAct、PAL等工具使用方法，还有在预训练预测器间路由或协调固定角色步骤的预测智能体，以及编写运行Python代码回答时间序列选择题的编码智能体。个人健康智能体方面，已有CGM智能体做片段检索、模式总结与问答，Personal Health Agent、PHIA、PULSE等编写运行代码分析可穿戴数据。区别在于：上述工作均在开发阶段预先确定模型类别及多模态信息进入方式，且多聚焦回顾性分析；GlucoAgent则在每次预测时动态编写并运行代码，按个案分析多模态上下文以预测未来血糖，并给出理由与证据。

### Q3: 论文如何解决这个问题？

论文提出的GlucoAgent是一个基于LLM的智能体系统，核心思路是不预设任何固定的预测模型或特征工程，而是让LLM在推理时针对每个预测案例动态地编写并执行代码，从个体多模态上下文中自主构建预测流程。整体框架上，每次预测时系统将因果边界内可用的多模态数据——包括血糖、心率、能量消耗等时序信号，含时间戳与宏量营养素的饮食日志，以及人口学、体测和化验等静态健康档案——连同目标预测时间戳编译成单一JSON案例文件，不注入任何手工特征，完全交由智能体判断哪些上下文相关以及如何处理。智能体配备两个工具：沙箱中的Python解释器（提供NumPy、SciPy、pandas、scikit-learn、statsmodels等通用库，只读访问数据、无网络、限时限内存）和预测提交工具，遵循ReAct与程序辅助推理范式，循环执行“写程序—观察输出—决定下一步”，每个预测回合最多允许固定轮数的LLM调用，最后两轮禁用Python以保证提交与纠错。关键技术在于智能体生成的程序高度多样，可从检索相似历史餐食到拟合并回测生理与统计模型；提交时须给出每个目标时刻的血糖值、预测理由及引用当前案例、程序与输出的证据，使分析过程可追溯、可解释。创新点包括：以推理时按案例动态分析替代统一模型，天然适配不同个体与时间上模态相关性的剧烈差异；无预训练预测器、无模态专用流水线，仅靠通用计算自主构建预测程序；以及带证据引用的可解释输出，便于重建和审视个体预测。

### Q4: 论文做了哪些实验？

论文在CGMacros多模态血糖数据集上开展主实验：45名参与者中留出9名（正常、糖尿病前期、糖尿病各3名）作为测试集，共1903个预测起点，每个起点预测未来30、60、90、120分钟的血糖，输入含血糖、心率、活动、饮食记录和健康档案，并设置三种输入条件（12小时血糖、全部血糖历史、多模态个人上下文）。对比方法包括Chronos-2、TimesFM-2.5、Moirai-2.0、Timer及持久化基线。主要结果：多模态设置下GlucoAgent四 horizon 平均RMSE为22.5 mg/dL，优于Chronos-2的23.5 mg/dL，且各horizon均领先，60分钟处为22.1对23.7 mg/dL；多模态数据使其RMSE降低1.4 mg/dL（24.0→22.5），而Chronos-2仅降0.3 mg/dL；餐后场景优势最明显，60分钟预测RMSE降低4.6 mg/dL（31.0→26.5），Chronos-2仅降0.8 mg/dL。论文还按餐食/运动情境分层分析、抽样576个起点统计程序行为（如餐后90%读取饮食日志），并比较不同LLM与推理强度（Claude Opus 5高强度最优，替代配置平均RMSE增加1.1–5.2 mg/dL）。此外在GlucoFM-Bench协议下用9个公开CGM数据集（8646个起点）验证仅血糖输入的竞争力，GlucoAgent在5个数据集上RMSE最低、2个第二；在OhioT1DM的CGM-LSM协议下与最佳基础模型差距在0.35 mg/dL以内。

### Q5: 有什么可以进一步探索的点？

论文的局限主要在于评估数据集单一：受限于开源多模态血糖数据稀缺，仅在CGMacros上验证，人群规模与多样性不足，难以判断代理策略在真实临床场景中的泛化性。此外，推理时逐点写码执行带来较高延迟与算力开销，且代码生成与模型拟合的可靠性缺乏系统性的安全与可解释性评估。未来可探索的方向包括：在更大规模、多人群、多设备队列上验证并做跨数据集迁移；引入缓存与程序复用机制，降低推理成本并提升实时性；将代理生成的程序沉淀为可复用的策略库，结合强化学习或元学习实现跨个体经验共享；加入不确定性量化与安全约束，避免错误代码或过拟合模型导致风险预测；还可扩展到胰岛素剂量建议、饮食干预等闭环决策场景，并引入临床专家反馈进行人机协同评估。

### Q6: 总结一下论文的主要内容

论文研究短期血糖预测问题，即基于连续血糖监测数据预测未来30至120分钟的血糖值。现有方法难以有效利用心率、活动量、饮食记录和健康档案等多模态个人上下文，因为不同模态在不同个体和时刻的预测价值差异很大。为此，作者提出GlucoAgent，一个基于大语言模型的智能体系统：在每次预测时，智能体针对该个体的多模态上下文动态编写并执行Python代码，读取输出并迭代分析，最终提交带推理理由和支持证据的预测。在CGMacros多模态数据集上，GlucoAgent在所有预测时域上均优于时间序列基础模型Chronos-2，平均RMSE为22.5 mg/dL对23.5 mg/dL；加入多模态上下文使其RMSE降低1.4 mg/dL，而Chronos-2仅降低0.3 mg/dL，在餐后60分钟预测中优势尤为显著（降低4.6 mg/dL）。在纯血糖基准上，GlucoAgent也保持竞争力。该工作表明，推理时按个案构建分析能更充分地利用多模态个人上下文，并提升预测的可解释性。
