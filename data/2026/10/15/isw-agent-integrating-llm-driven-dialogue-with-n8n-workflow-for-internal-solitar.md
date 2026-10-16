---
title: "ISW-Agent: Integrating LLM-Driven Dialogue with n8n Workflow for Internal Solitary Wave Remote Sensing Image Processing"
authors:
  - "Hao Zhang"
  - "Hengrui Liu"
  - "Lina Sun"
  - "Junmin Meng"
date: "2026-10-15"
arxiv_id: "2610.21502"
arxiv_url: "https://arxiv.org/abs/2610.21502"
pdf_url: "https://arxiv.org/pdf/2610.21502v1"
categories:
  - "cs.AI"
tags:
  - "LLM Agent"
  - "工作流编排"
  - "遥感图像处理"
  - "工具调用"
  - "输出验证"
  - "故障注入"
  - "可追溯处理链"
  - "自然语言指令"
  - "多模型集成"
  - "地理空间变换"
relevance_score: 7.5
---

# ISW-Agent: Integrating LLM-Driven Dialogue with n8n Workflow for Internal Solitary Wave Remote Sensing Image Processing

## 原始摘要

Internal solitary wave (ISW) remote sensing requires task parameters and spatial information to be transferred across image acquisition, detection, stripe extraction, and propagation prediction. Here, we present ISW-Agent, which integrates large language model (LLM) interpretation with n8n workflows and independent scientific models through structured task constraints, geospatial transformations, and stage-specific output validation. In tests of 120 Chinese instructions per backend, GPT-5.6 Sol and DeepSeek both achieved a strict task-match rate of 94.2%, with all intents and execution decisions matching the reference. Sentinel-1 cases demonstrated continuous processing from dialogue requests to wavefront prediction for the specified scene. Of 50 timed scenes, 39 completed detection, extraction, and prediction with a median turnaround time of 48.04 s; 11 stopped after empty extraction. Across 3,408 controlled fault-injection runs, retries recovered 234 transient-failure conditions and output validation rejected 234 structural defects, while 61 provenance or completeness errors indicated the need for content-consistency checks. Overall, ISW-Agent thus connects natural-language requests to traceable spatial processing chains for multimodel ISW analysis.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

内孤立波（ISW）遥感分析通常涉及图像获取、检测、条纹提取和传播预测等多个阶段，需要在这些阶段之间传递任务参数与空间信息。然而，现有研究多针对特定输入和评估目标独立开发方法，从传统小波检测、边缘/SVM提取、KdV求解器，到Faster R-CNN、IWE-Net、U-Net及机器学习预测模型，各环节彼此割裂。这种碎片化带来两个实际瓶颈：一是用户必须在不同程序间手动转移中间产品，并理解各服务所需的字段、坐标和文件格式；二是服务成功响应并不保证输出满足下一阶段要求，例如截断的条纹轮廓虽可写为矢量文件，却会改变构建初始波前的空间范围。现有工作流平台虽已用于地学领域，但对自然语言任务描述和领域特定决策规则支持有限；基于LLM的智能体（如RS-Agent、ThinkGeo）虽提供自然语言接口，却难以保证空间产品在模型间连续传递时图像与波峰线身份的一致性，也缺乏对服务失败的显式处理规则。因此，本文提出ISW-Agent，旨在将自然语言解释与确定性执行分离，通过结构化任务约束、地理空间变换和分阶段输出验证，把自然语言请求连接到可追溯的多模型内孤立波空间处理链，解决跨阶段任务规范、接口兼容与输出验证的核心问题。

### Q2: 有哪些相关研究？

相关研究主要可分为三类。方法类方面，ISW检测由小波方法发展到Faster R-CNN、IWE-Net等深度学习模型；条纹提取从边缘检测、SVM发展到U-Net；传播预测从KdV类解析求解器发展到结合卫星观测与预报的机器学习模型。这些工作为ISW-Agent提供了可调用的独立科学模型，但它们各自面向特定输入与评价目标，中间产品（检测框、条纹掩膜、波峰线坐标）的传递仍需人工准备与参数配置，本文则以结构化任务约束和地理空间变换将这些阶段串联为可追溯的处理链。应用与平台类方面，已有工作流平台被用于地球科学，但通常对自然语言任务描述和领域决策规则支持有限；RS-Agent将任务推理与工具调用结合，ThinkGeo评测遥感操作智能体。与它们相比，ISW-Agent强调自然语言解释与确定性执行的分离，并针对ISW场景增加空间产品一致性保持、阶段输出校验与故障处理规则。评测类方面，本文通过对话契约、空间表示保持、执行时间和受控故障注入下的终止结果进行评估，区别于以往仅关注单一模型精度或工具调用成功率的评测方式。

### Q3: 论文如何解决这个问题？

ISW-Agent 采用三层架构来解决内孤立波遥感处理中跨阶段信息传递的问题。第一层是对话理解层，兼容 OpenAI 接口的多种 LLM 后端（ChatGPT、DeepSeek、Kimi、Doubao），将自然语言请求转化为显式任务契约 τ=(I,S,D,P,O)，其中 I 为有序意图、S 为时空槽位、D 为传感器与数据规格、P 为模型参数、O 为输出与溯源要求。LLM 仅负责提出字段值，而控制器从资产注册表和服务配置中补充 D、P、O，从而用确定性规则约束 LLM 输出。

第二层是基于 n8n 的领域感知编排层，通过 Webhook 入口接收请求，用 HTTP 请求节点调用共享控制器，集中处理参数校验、重试和输出检查。五个意图（图像下载、预处理、ISW 检测、条带提取、传播预测）按数据依赖串联，每阶段仅在输入可用且前序输出通过校验后才执行。任务被分类为可执行、需澄清或拒绝，缺失图像、条带标识或预报区间时保留已知信息并请求澄清。

第三层是科学模型服务层。检测与条带提取共用单类 YOLO11n-seg 网络，融合三个尺度特征，推理尺寸 1024 像素，置信度与 NMS IoU 阈值分别为 0.07 和 0.30。条带掩膜经地理配准、多边形化、骨架化提取中心线，重采样为 200 个波峰点。每个波前点用经纬度、水深和上下层密度描述符共五维特征表示，由两层 64 通道 ConvLSTM 建模相邻点关系，解码出传播速度与方位角，再经球面位移公式递推预测，最后用加权样条拟合得到预测波前。

创新点在于：以结构化任务契约约束 LLM 输出，用确定性规则实现多模型间的数据依赖编排，结合有界重试与输出校验区分瞬时故障与结构性缺陷，并将自然语言请求连接到可溯源的空间处理链。

### Q4: 论文做了哪些实验？

论文围绕ISW-Agent开展了四类实验。对话理解实验使用120条中文指令，覆盖12类任务，GPT-5.6 Sol与DeepSeek均实现120条有效响应、严格任务匹配率94.2%、槽位F1为0.978，意图与执行决策全部正确；Kimi与Doubao因限流、超时等仅返回27和95条有效响应。案例实验基于50景Maluku海Sentinel-1 IW/VV影像，并补充Andaman海与Celebes海场景，完成检测、条纹提取与传播预测，如ISW 5初始波峰线约65.7 km，4 h平均速度1.71 m/s。矢量化一致性实验中，21个掩膜全像素矢量化后IoU均为1，而原导出中位IoU仅0.682。阈值敏感性实验在12景、108次推理下比较3种置信度与3种NMS阈值，候选数从21降至5。工作流计时实验中，50景有39景完成全流程，中位耗时48.04 s，检测、提取、预测中位耗时分别为20.10、14.16、13.41 s；11景因空提取提前终止。故障注入实验构造15类故障、852个条件、3408次运行，重试恢复234个瞬时故障，输出验证拒绝234个结构缺陷，错误接受从61升至295。

### Q5: 有什么可以进一步探索的点？

当前工作的局限主要体现在三方面：一是对话理解仅覆盖12类中文指令，缺乏多语言、多轮复杂意图与模糊指代的鲁棒性验证；二是流程依赖固定阈值与预设模型，检测阈值变化会显著改变候选目标集，且11个场景因空提取而提前终止，缺乏自适应回退机制；三是故障测试止于提取服务响应，61例溯源与完整性错误表明内容一致性校验仍不足。未来可探索：引入视觉语言模型对SAR图像进行联合推理，实现检测—提取—预测的端到端可微分优化；构建自适应阈值与不确定性感知的候选筛选策略，减少空提取与漏检；将溯源图与物理约束（如KdV方程）嵌入验证环节，提升预测可信度；并扩展到多源卫星、多语言指令与真实业务流中的长时程在线学习。

### Q6: 总结一下论文的主要内容

ISW-Agent面向内孤立波遥感图像处理中跨阶段任务参数与空间信息传递的需求，提出将大语言模型对话理解、n8n工作流编排与独立科学模型相结合的一体化代理框架。其核心方法是通过结构化任务约束、地理空间变换和阶段化输出校验，把自然语言请求转化为可追踪的空间处理链，依次完成图像获取、内孤立波检测、条纹提取与传播预测。实验表明，在每后端120条中文指令测试中，GPT-5.6 Sol与DeepSeek均达到94.2%的严格任务匹配率；Sentinel-1案例实现了从对话请求到波前预测的连续处理，50个计时场景中39个完整完成，中位耗时48.04秒。故障注入实验进一步区分了服务恢复与科学输出验证，重试恢复234次瞬态故障，结构校验拒绝234个缺陷产品，并揭示61个内容一致性错误。该工作为多模型内孤立波分析提供了可追踪、可验证的工作流基础。
