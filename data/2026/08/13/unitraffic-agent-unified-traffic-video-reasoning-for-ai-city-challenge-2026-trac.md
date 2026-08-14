---
title: "UniTraffic-Agent: Unified Traffic Video Reasoning for AI City Challenge 2026 Track 3 with Two Out-of-Domain Evaluations"
authors:
  - "Peng Li"
  - "Qianqian Xu"
  - "Shilong Bao"
  - "Yangbangyan Jiang"
  - "Qingming Huang"
date: "2026-08-13"
arxiv_id: "2608.13031"
arxiv_url: "https://arxiv.org/abs/2608.13031"
pdf_url: "https://arxiv.org/pdf/2608.13031v1"
github_url: "https://github.com/Roclp/UniTraffic-Agent"
categories:
  - "cs.CV"
  - "cs.AI"
tags:
  - "Agentic workflow"
  - "Video reasoning"
  - "Traffic anomaly reasoning"
  - "Multimodal LLM"
  - "Evidence-based reasoning"
  - "Task-specific action adapters"
  - "AI City Challenge"
relevance_score: 7.5
---

# UniTraffic-Agent: Unified Traffic Video Reasoning for AI City Challenge 2026 Track 3 with Two Out-of-Domain Evaluations

## 原始摘要

Traffic video understanding has become an important problem in intelligent transportation, as road videos provide direct evidence for accidents, violations, and interactions between vehicles and vulnerable road users. A useful system should explain how a traffic event develops, why it happens, and when the relevant interaction occurs, yet this remains difficult for multimodal large language models (MLLMs) because traffic videos contain sparse events and varied viewpoints. We introduce UniTraffic-Agent, the MR-CAS solution for Track~3 of the 10th AI City Challenge, which includes Traffic Anomaly Reasoning (TAR) and two out-of-domain evaluations: FETV for fisheye traffic events and PSI-VQA for pedestrian intention reasoning. UniTraffic-Agent follows an observe--reason--act--verify workflow that samples timestamped visual evidence, reasons over all questions from the same clip in one request, and converts responses through task-specific action adapters. On the official Public leaderboards, MR-CAS ranks 16th on TAR with a score of 0.5780, 2nd on FETV with 0.4884, and 4th on PSI-VQA with 64.4161. The code is available at https://github.com/Roclp/UniTraffic-Agent.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

交通视频理解在智能交通系统中至关重要，因为道路视频能为事故、违规及车辆与弱势道路使用者之间的交互提供直接证据。然而，现有系统（如TrafficVLM、TrafficVILA等）虽能识别相关主体和道路条件，却难以解释事件如何发展、为何发生以及关键交互发生的具体时刻。多模态大语言模型（MLLMs）虽提供灵活接口，但交通视频存在关键证据仅出现在少数帧、视角差异大（如监控、鱼眼、行车记录仪）以及单片段关联多问题等挑战，远超常规图像和短视频问答。此外，独立回答每个问题会导致预测结果不一致。本文要解决的核心问题是：构建一个统一框架，能在稀疏事件和多样视角下，对交通视频进行时间感知的联合推理，同时适应不同任务输出格式，并提升跨域泛化能力。为此，UniTraffic-Agent采用“观察-推理-行动-验证”工作流，结合全局帧覆盖与问题特定时间戳证据，对同一片段的所有问题联合推理，并通过任务适配器转换输出，最终在AI City Challenge 2026 Track 3的TAR、FETV和PSI-VQA任务上取得优异排名。

### Q2: 有哪些相关研究？

近年来，多模态大语言模型（MLLMs）与智能体在视频理解领域发展迅速。相关工作可分为三类：**基础MLLMs与视频模型**，如GPT-4V、Gemini、LLaVA、Video-ChatGPT，以及VideoCLIP、VideoCoCa、TimeChat等，它们探索视频-文本表示与时间定位，但缺乏针对交通场景的专门设计。**交通领域MLLMs与智能体**，如SpatialAgent利用LLM智能体协调感知工具处理AI City空间问答，其他系统通过相位感知输入、高分辨率视图、参考示例或专用提示词适应道路场景，但多聚焦单一任务或视角。**交通异常与时间推理**，涵盖异常检测、弱监督定位、事故理解及因果推理，QVHighlights和TimeChat等查询条件模型将语言查询与视频时间区间关联，但通常针对特定问题类型。

本文UniTraffic-Agent与上述工作的区别在于：它统一处理CCTV、鱼眼和行车记录仪三种视角，覆盖异常推理（TAR）、鱼眼事件（FETV）和行人意图（PSI-VQA）三类任务；采用“观察-推理-行动-验证”智能体工作流，在同一请求中联合推理同一片段的所有问题，并通过任务特定动作适配器输出，实现了跨域、多任务的统一视频推理。

### Q3: 论文如何解决这个问题？

UniTraffic-Agent通过一个统一的“观察-推理-行动-验证”工作流来解决交通视频推理中的多任务异质性问题。其核心设计是将视频片段而非单个问题作为基本推理单元，从而在共享事件上下文中生成一致的预测。

在观察阶段，系统采用分层采样策略构建紧凑帧集：先均匀选取G帧覆盖全局，再叠加时长自适应网格，若问题带有时间戳锚点，则额外采样锚点前后各1秒的局部邻域。当候选帧超过预算M时，优先保留端点、时间戳附近帧，其余从规则网格填充，并去除重复帧后按时间排序。每帧附带时间戳，提示词明确相邻输入可能间隔数秒，且时间戳附近帧以更高视觉细节发送。解码后的JPEG被缓存，确保重试时使用相同视觉证据。

在推理阶段，模型被要求先检查道路布局、识别相关参与者、追踪事件从初始状态到最终结果的演变，然后基于这一共享上下文在一次请求中回答该片段的所有问题或字段。这种视频级推理减少了同一事件在不同输出中关于参与者身份、因果解释和时间边界的矛盾。

行动阶段通过三个任务特定适配器将共享推理结果映射为官方提交格式：TAR适配器联合处理所有问题类型，约束BCQ/MCQ答案并支持自由文本；FETV适配器生成包含违规者、轨迹、道路上下文等13个字段的结构化记录，并区分3×3网格位置与车道索引；PSI-VQA适配器跟踪红框标记的行人，区分观察到的运动与推断的过街意图。验证阶段恢复官方标识符、规范化类别值、校验时间区间并检查输出完整性，同时保留原始响应和验证结果用于错误分析。

### Q4: 论文做了哪些实验？

论文在AI City Challenge 2026 Track 3的三个任务上评估了UniTraffic-Agent：TAR（交通异常推理）、FETV（鱼眼交通事件）和PSI-VQA（行人意图推理）。实验设置上，TAR测试集含960个问题（80个CCTV片段），FETV含200个鱼眼片段，PSI-VQA含328个问题（40个行车记录仪片段）。所有视频单次请求处理，最多采样32帧，使用gpt-5.5为主模型，温度设为0。

对比方法为各任务Public leaderboard的领先条目。主要结果：TAR上MR-CAS排名16，得分0.5780（领先者0.6788），其中BCQ准确率0.9187、MCQ准确率0.9500，但场景描述（0.2667）和时间描述（0.3248）等长文本任务差距较大。FETV上排名第2，得分0.4884，仅比领先者低0.0007，在描述、违规者类型和位置字段上表现优异，但交叉口类型推理较弱（0.5749 vs 1.0000）。PSI-VQA上排名第4，得分64.4161，Open-QA Cue-F1超过领先者（0.6389 vs 0.5833），但时间定位差距明显（0.5751 vs 0.7427）。整体表明模型在约束性问题上表现强，长格式生成和几何推理仍需改进。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在四个方面：参考对齐的长序列生成、鱼眼镜头下的道路几何畸变、行人意图预测以及时间边界估计。这些误差根源指向了当前方法对动态场景中细粒度时空关系建模的不足。未来可探索的方向包括：引入显式的多目标跟踪模块，将车辆和行人的轨迹作为先验知识注入推理过程，从而增强对交互事件的因果理解；设计几何感知的时间推理机制，利用鱼眼相机的标定参数或逆透视映射来校正空间畸变，提升对非标准视角的适应性；针对行人意图预测，可结合短时运动趋势与场景语义（如人行道、红绿灯状态）构建多模态预测头，而非仅依赖视觉特征；此外，可借鉴视频分割或事件定位技术，对时间边界进行更精细的回归，减少长序列中的累积误差。最终，将这些能力整合进Agent的反思与验证环节，形成闭环优化，有望显著提升跨域泛化性能。

### Q6: 总结一下论文的主要内容

UniTraffic-Agent针对AI City Challenge 2026 Track 3中的交通视频推理任务，提出了一种统一的智能体框架。该任务包含交通异常推理（TAR）及两个域外评估：鱼眼交通事件（FETV）和行人意图推理（PSI-VQA）。方法上，UniTraffic-Agent采用“观察-推理-行动-验证”的工作流，先采样带时间戳的视觉证据，再在同一请求中基于片段级上下文推理所有问题，最后通过任务特定的动作适配器输出答案。在官方公开排行榜上，该方法在TAR上排名第16（得分0.5780），在FETV上排名第2（0.4884），在PSI-VQA上排名第4（64.4161），展现了强大的域外泛化能力。主要错误源于长时生成的对齐、鱼眼几何、行人意图预测及时间边界估计，未来工作可聚焦于显式目标跟踪和几何感知的时间推理。
