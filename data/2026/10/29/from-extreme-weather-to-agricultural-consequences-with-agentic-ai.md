---
title: "From extreme weather to agricultural consequences with agentic AI"
authors:
  - "Minghan Yu"
  - "Mengyu Dai"
  - "Yixin Wen"
  - "Haizhao Yang"
date: "2026-10-29"
arxiv_id: "2610.40641"
arxiv_url: "https://arxiv.org/abs/2610.40641"
pdf_url: "https://arxiv.org/pdf/2610.40641v1"
categories:
  - "physics.ao-ph"
  - "cs.AI"
tags:
  - "Agentic AI"
  - "极端天气"
  - "农业灾害"
  - "因果分析"
  - "可解释指数"
  - "损失预测"
  - "多源数据融合"
  - "证据溯源"
relevance_score: 6.5
---

# From extreme weather to agricultural consequences with agentic AI

## 原始摘要

Extreme weather is forecast days ahead, yet its consequences for agriculture remain hard to predict: a forecast says where a storm will strike, not which crops will suffer or how much is at risk, and the records that could tell span many sources. We present WxCrop, the first agent that judges agricultural hazards from physically interpretable weather indices examined by causal analysis, and the first that combines weather and agricultural information to predict crop loss reliably for past and forecast dates. We demonstrate it in Florida on hurricanes, freezes and dry heat, with a loss model calibrated on insurance records for each, and the same procedure extends to other hazards and areas. Three checks show reliability: the hurricane index detects recorded cyclone days with an AUC of 0.98, recorded losses in held-out years are reproduced to within 2%, and independent production records confirm the county rankings (rank correlation 0.63). Users ask the agent for each crop group's loss as a fraction of expected season value, every number sourced, so that governments, growers and scientists respond to agricultural disasters quickly.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决极端天气预报与农业实际后果之间脱节的问题。研究背景是：极端天气虽可提前数天预报，但预报只能说明风暴将在何处登陆，无法告诉农户、应急管理者和科学家哪些作物会受损、损失有多大。全球农业在1991至2023年间因灾害损失约3.26万亿美元，而提前预警是回报最高的防御手段之一，但现有预警缺乏对农业后果的量化。现有方法的不足体现在三方面：一是官方灾损评估（如UF/IFAS的飓风复合强度指数）在灾后计算，且采用简单加和形式，无法刻画复合灾害的交互作用；二是遥感方法虽快但仍属事后，依赖卫星过境和晴空条件；三是现有语言模型助手多基于文档、影像或数据目录作答，未与带日期的农业地块关联，且用户对其来源可信度、计算可追溯性存疑。核心问题是：如何构建一个智能体，将物理可解释的天气指数与带日期的作物地图、生长日历和保险损失记录结合，通过因果分析检验天气指数对作物损失的影响，从而对任意日期（包括预报日期）给出可追溯、可靠的作物损失比例估计，缩短从灾害发生到资源调配之间的时间。

### Q2: 有哪些相关研究？

本文的相关研究可分为三类。方法类：Chen等将台风风速与降雨合成单一事件指数，复现了中国台风损失；台湾田间记录表明风与暴雨耦合、连续事件及作物生长期决定损失；USDA将卫星洪涝范围与观测风雨叠加到耕地数据层，UF/IFAS助手用Sentinel-2影像回答农户损害问题；还有基于模拟台风风和卫星降雨的田块尺度损害估计。应用类：实证研究量化高温、干旱及复合极端事件对区域至全球产量的影响，近期工作用USDA风险管理署保险损失记录作为天气驱动作物损害的代理，但分辨率粗、时间尺度为季节或年；预报驱动的冲击模型多估计住房损害或按人口暴露排序县。评测/对话助手类：ClimSight将问题路由到气候模式输出，WildfireGPT协调检索代理服务野火适应，DisasTeller串联视觉语言代理做灾后评估并指出早期错误会向下游传播，另有从灾害叙述中抽取洪水记录及集成NASA工具的代理式搜索助手。区别在于：这些系统基于文档、投影、影像或数据目录作答，均未把某日灾害信号与下方作物和田块关联；WxCrop首次以因果分析检验的县级天气指数结合作物记录，对过去与预报日期给出可溯源的价值损失比例，且不依赖影像过境或晴空。

### Q3: 论文如何解决这个问题？

WxCrop 的核心思路是把“天气预报”翻译成“农业损失”，其整体框架分为三步：先把天气与作物放到同一张地图上，再计算可识别灾害事件的物理可解释危险指数，最后估计各作物组的损失比例。

架构上包含三个主要模块。第一是地图与数据层：用户选择灾害类型后，系统按因果分析选出的驱动天气层（如飓风的风速与七日降雨）按需加载公共档案数据，同时叠加县/地块级作物清单、作物日历与生长阶段，并给出每个地块的“脆弱度百分比”（已投入价值与季节预期收入中已暴露的比例）。第二是危险指数模块：以物理机制设计复合指数，例如飓风指数 H 将随风速平方增长的“风载荷”乘以随降雨增长的“放大因子”，冻结指数用最低温低于设计温度的深度乘以晴空辐射冷却放大，干热指数用降水—蒸散亏缺乘以高温累积；指数阈值由暴露记录的分位数确定，并映射为基线、升高、可能、严重四个等级。第三是损失模型模块：将作物组敏感性 θ_g、当日产量脆弱度 φ_g 与危险指数结合，输出“若成灾的损失比例 S_g”和“获得赔付的概率 P_g”，以二者乘积 L_g=P_gS_g 作为期望损失，并按保险记录分作物组、分灾害校准。

关键创新点在于：用因果分析预先固定候选因子与接受规则来筛选指数形式；指数与损失模型均以保险理赔记录校准并做样本外验证；所有数字通过定义好的工具检索并附带数据版本、单位与来源，由系统计算而非语言模型生成，从而保证可追溯与可靠性；低等级灾害时回答止于等级，避免对非事件给出虚假精度。

### Q4: 论文做了哪些实验？

论文围绕WxCrop智能体开展了三类验证实验。实验设置上，以佛罗里达州为研究区，覆盖飓风、冰冻和干热三种灾害，损失模型分别用各灾害的保险记录进行校准。数据集包括NHC HURDAT2最佳路径风场、HRRR阵风分析、FSAID农业用地清单（超17万个地块、2018年分类）以及2004—2024年县级保险理赔记录。对比与验证方法包括：将飓风指数与有记录的飓风日比对，将模型复现的损失与留出年份的保险损失比对，并将县级排名与独立生产记录比对。主要结果：飓风指数识别有记录飓风日的AUC达0.98；留出年份的损失复现误差在2%以内；县级排名与独立生产记录的秩相关为0.63。案例分析中，2022年9月28日飓风Ian登陆日，DeSoto县飓风指数H=27.9属严重等级，Jackson县H=0.20属基线等级；按H分层的县级月统计显示，最低等级有保险作物损失的比例约16%，最高等级达81%，其中66%损失超过10万美元，表明H能有效排序损失。

### Q5: 有什么可以进一步探索的点？

论文的局限主要在标签粒度与覆盖范围：保险记录仅到县-月-作物组，独立损失记录更稀缺，因此验证只能到方向和县级总量；绝对美元损失因缺乏公开标签而误差较大（仅到数量级）；且仅示范了佛罗里达的飓风、冰冻、干热三类，占全州天气致损赔付64%，而 excess moisture（30%）尚未纳入。未来可探索：一是获取农场级保险记录、理算员报告或实地核验损失，在数据协议下把校准细化到田块尺度；二是将框架扩展到 excess moisture/flood、冰雹与非气旋风，并在持有更细记录的其他州复现；三是把 DiD 检验推广到更多区域以验证跨州泛化；四是量化该智能体在应急调度、种植者情景比较和保险赔付预估中的实际决策价值。我的补充思路是：引入不确定性量化与置信区间输出，让百分比附带可信度；并让 LLM 代理主动追问缺失信息、迭代调用因果分析层，形成可审计的“假设—验证”闭环，从而把当前的单向问答升级为可交互的诊断工作流。

### Q6: 总结一下论文的主要内容

论文针对极端天气预报与农业实际损失之间的脱节问题，提出WxCrop——首个将物理可解释天气指数与因果分析相结合、并融合天气与农业记录来预测作物损失的智能体系统。问题定义上，现有工具多为灾后回溯，且天气指数无法刻画复合灾害的交互效应，气象预报只说天气而不说作物损失。方法上，WxCrop以县为单元、以日为粒度，先用因果分析从风速、降雨、低温、云量、水分亏缺与高温等物理因子中筛选并构建可分解的复合灾害指数（如飓风指数为风压与降雨放大器的乘积），再结合带日期的作物地图、生长日历与作物脆弱度，通过基于保险记录校准的损失模型输出各作物组预期季节价值损失比例及其发生概率，所有数字均可溯源至公开记录。主要结论：飓风指数识别历史气旋日的AUC达0.98，留出年份损失复现误差在2%以内，县排名与独立产量记录秩相关0.63；系统覆盖佛罗里达飓风、冰冻与干热三类灾害，占该州天气致损保险赔付的64%，并可扩展至其他灾害与地区，为政府、种植者和科学家提供快速可追溯的农业灾害早期预警。
