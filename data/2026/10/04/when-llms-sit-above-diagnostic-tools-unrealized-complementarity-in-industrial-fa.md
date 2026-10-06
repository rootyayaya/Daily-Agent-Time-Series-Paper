---
title: "When LLMs Sit Above Diagnostic Tools: Unrealized Complementarity in Industrial Fault Diagnosis"
authors:
  - "Donghwan Kim"
date: "2026-10-04"
arxiv_id: "2610.05031"
arxiv_url: "https://arxiv.org/abs/2610.05031"
pdf_url: "https://arxiv.org/pdf/2610.05031v1"
categories:
  - "cs.CL"
  - "eess.SY"
tags:
  - "LLM集成"
  - "工业故障诊断"
  - "工具调用"
  - "证据路由"
  - "多源信息融合"
  - "诊断报告生成"
  - "可解释性"
  - "时序异常检测"
  - "预测性维护"
  - "基准评估"
relevance_score: 8.5
---

# When LLMs Sit Above Diagnostic Tools: Unrealized Complementarity in Industrial Fault Diagnosis

## 原始摘要

Large language models are increasingly used as integration layers above specialized tools, but a stronger component does not necessarily produce a stronger combined system. Across five diagnostic datasets (bearing vibration, process monitoring, semiconductor equipment), we study whether an LLM can reliably use external diagnostic information; paired repeat calls separate advice effects from output instability. In all five, conflicting external information overturned initially correct LLM judgments. Among the four datasets with direct integration comparisons, none showed a consistent advantage for implicit LLM integration over the stronger standalone source. On a Tennessee Eastman confirmation set whose protocol was fixed before evaluation, unaided accuracy was 64.67%, implicit LLM-specialist integration 77.43%, and the specialist alone 83.33%. Specialist information improved the LLM by 12.8 points (95% interval 9.7 to 15.9), yet the integrated output stayed 5.9 points below the specialist (95% interval -12.0 to -0.7). A two-source selector oracle reached 92.76%, indicating complementarity that the integrated output did not fully realize. The integrated output missed 140 of 295 specialist corrections (47.5%) but lost 15 of 99 initially correct LLM judgments (15.2%). The deficit remained under prompt and specialist sensitivity analyses. Among CWRU cases solved under both evidence presentations, task-aligned physical evidence yielded lower estimates of susceptibility to incorrect advice in six of seven models (five intervals excluding zero); higher reasoning effort gave no reliable reduction in five models, and a separate four-model TEP analysis gave no clear evidence that it resolves the integration problem. Source quality and integration quality should be evaluated separately: an integration layer should be compared with its stronger standalone component, not only with the unaided LLM.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文关注的是大语言模型在工业故障诊断中作为“集成层”的角色问题。近年来，LLM 常被置于振动分类器、过程监控模型等专用诊断工具之上，负责综合工具输出、传感器摘要、报警和维护记录，从而影响最终决策。然而，现有研究与工程实践往往默认“更强的组件叠加会带来更强的组合系统”，却很少检验 LLM 是否真的能可靠地利用外部诊断信息。论文指出，两个来源即使互补，也需要在个案层面进行仲裁；若集成器忽略纠正或盲从错误建议，强专用模型加一个能干的 LLM 反而可能不如专用模型单独使用。为此，作者在五个诊断数据集上，通过配对重复调用区分“外部建议效应”与“输出不稳定”，核心问题是：LLM 集成器能否把互补但不完美的来源整合为达到或超过更强单独来源的决策，并比较集成质量与来源质量。

### Q2: 有哪些相关研究？

相关研究可分为四类。方法类：Perez等（2022）、Sharma等（2023）发现助手会迎合用户偏好甚至承认未犯错误；Xie等（2024）指出模型易受与知识冲突的外部证据影响；Kumar和Chopra（2026）、Schuster等（2026）、Li等（2025）研究来源身份与权威性对冲突消解的影响。工具评测类：Yang等（2026a）通过污染搜索、委托答案和代码来测量采纳率；Soni（2026）、Xu等（2026）区分跳过工具、忽略结果、编造与过度调用等失败模式；Varlamov等（2026）的MemToC与Xu等（2026b）的TrustMargin研究模型记忆与工具/检索间的仲裁。人机协作类：Schemmer等（2023）、Bansal等（2021）、Vaccaro等（2024）研究人类接受或拒绝AI建议，以及组合系统常劣于更优成员；Madras等（2018）、Mozannar等（2020）等学习延迟决策。工业应用类：Lee等（2025）、Li和Zhao（2025）研究证据呈现方式；Khan等（2025）、Liang和Sin（2026）、Yang等（2026b）、Wei和Fink（2026）等将LLM置于工具之上做诊断、报告或因果链构建。本文区别在于：以拟合诊断专家为第二来源，用配对重复调用控制输出不稳定，并检验集成输出能否匹配或超过更强的单一来源，而非仅测采纳率或流水线质量。

### Q3: 论文如何解决这个问题？

论文的核心方法是把 LLM 定位为“集成层”而非“替代检测器”，通过严格的配对实验框架来检验其能否可靠地仲裁两个不完美信息源。整体框架包含三类调用：第一次为无辅助调用，仅给出不含标签的案例证据；第二次为独立重复调用，使用完全相同的提示与解码设置，用于捕捉温度 0 下仍存在的提供方非确定性；第三次为“受建议调用”，在上下文中加入一句外部诊断标签，即 prompt 级隐式集成。只有将第三次与第二次配对比较，才能把外部信息的影响与普通测试—重测波动区分开，这是该方法的关键设计。

在数据与模块层面，实验覆盖五个诊断数据集：三个轴承数据集（CWRU、Paderborn、XJTU-SY）、田纳西伊士曼过程与 Lam 9600 半导体设备。轴承集成比较使用六个 400 棵树随机森林，分别对应强、弱预定义特征集，并采用留一记录文件或留一轴承的折外预测；田纳西伊士曼使用仅由训练集拟合的多项逻辑回归专家，其选择规则在确认评估前已固定。外部诊断在受控建议实验中由设计决定正确或错误，在集成实验中则来自固定专家模型。

创新点在于：一是提出“双源选择器 oracle”作为互补性上界，即只要两个存储预测之一正确即算正确，从而量化集成输出未实现的互补空间；二是把源质量与集成质量分开评估，要求集成层与更强的独立组件比较，而非仅与无辅助 LLM 比较；三是通过任务对齐的物理证据表示、仲裁提示、先验标签、替代专家与更高推理努力等敏感性分析，检验集成缺陷的稳健性。

### Q4: 论文做了哪些实验？

论文围绕“LLM作为诊断工具上层集成层是否真正带来增益”开展实验。实验覆盖五个诊断数据集，包括轴承振动（CWRU）、过程监控（田纳西伊士曼TEP）和半导体设备，采用配对重复调用以区分建议效应与输出不稳定性。核心对比为：无辅助LLM、隐式LLM-专家集成、专家单独，以及双源选择器oracle。在TEP确认集上，无辅助准确率64.67%，隐式集成77.43%，专家单独83.33%，选择器oracle达92.76%。专家信息使LLM提升12.8个百分点（95%区间9.7–15.9），但集成输出仍比专家低5.9个百分点（95%区间−12.0–−0.7）。错误解剖显示，集成错过295次专家纠正中的140次（47.5%），仅丢失99次正确LLM判断中的15次（15.2%）。敏感性分析中，显式仲裁指令、提供存储的无辅助诊断、替换随机森林专家均未消除集成赤字；显式仲裁反而使集成降至76.1%，错过纠正升至54.6%。CWRU上22个可比比较中仅1个区间高于零，28个点估计均低于更强单源。任务对齐物理证据在七个模型中的六个降低了错误建议易感性，五个区间排除零。

### Q5: 有什么可以进一步探索的点？

论文的核心局限在于：LLM 作为集成层未能兑现两个独立诊断源之间的互补性，选择器 oracle 达 92.76%，而实际集成仅 77.43%，说明瓶颈不在源质量而在集成机制。未来可从三方面探索：一是设计显式的源可靠性建模与仲裁机制，例如让 LLM 先估计各源在具体工况下的可信度，而非被动接受建议；二是将任务对齐的物理证据（如 CWRU 中有效的证据呈现方式）系统性地引入 TEP 等流程数据场景，验证其能否同样降低错误建议的易感性；三是探索推理努力之外的因素，如结构化证据格式、多轮验证或外部校准模块，因为提高推理预算并未可靠缓解集成缺陷。此外，当前仅用单一专家标签，未来可引入多专家投票或不确定性量化，让集成层在源冲突时主动弃权或请求补充信息，从而逼近 oracle 上界。

### Q6: 总结一下论文的主要内容

论文研究大语言模型作为集成层置于专业诊断工具之上时，能否可靠利用外部诊断信息。作者在五个诊断数据集（轴承振动、过程监控、半导体设备）上采用配对重复调用，将外部建议效应与输出不稳定性分离。结果发现，在所有数据集中，冲突的外部信息都会推翻LLM原本正确的判断；在四个可比较数据集上，隐式LLM集成均未稳定优于更强的独立诊断源。在田纳西伊士曼确认集上，无辅助LLM准确率64.67%，集成后77.43%，而专家单独达83.33%，集成输出仍低于专家5.9个百分点；双源选择器预言机可达92.76%，说明存在未被充分实现的互补性。论文核心贡献在于区分“源质量”与“集成质量”，主张将LLM集成层与其更强的独立组件直接比较，而非仅与无辅助LLM比较。
