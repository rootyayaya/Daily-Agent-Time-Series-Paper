---
title: "SCORE-LM: State-Space Radar Representations with Language Models for Fault Diagnosis"
authors:
  - "Mainak Mallick"
  - "Seung-Kyum Choi"
date: "2026-09-30"
arxiv_id: "2609.38980"
arxiv_url: "https://arxiv.org/abs/2609.38980"
pdf_url: "https://arxiv.org/pdf/2609.38980v1"
categories:
  - "cs.LG"
  - "eess.SP"
tags:
  - "LLM for fault diagnosis"
  - "radar fault diagnosis"
  - "state-space model"
  - "language model adaptation"
  - "maintenance guidance"
  - "soft token projection"
  - "industrial sensor interpretation"
  - "compact diagnosis"
  - "self-supervised learning"
relevance_score: 7.5
---

# SCORE-LM: State-Space Radar Representations with Language Models for Fault Diagnosis

## 原始摘要

Radar hardware faults threaten automated perception, motivating accurate, compact diagnosis and understandable maintenance guidance. We introduce SCORE-LM, which couples a small scatterer-conditioned operator-response encoder (SCORE) to an adapted local language model. SCORE combines self-referenced complex trajectories, physical descriptors, and a selective state-space branch, with source-only self-supervision and directional fault inference. On eight capture-excluded Rad-R fault recordings, it achieves state-of-the-art performance within the evaluated nine-model comparison: 88.39% mean capture recall and 88.20% four-fault macro-F1 at ten frames. Its 39,520 radar inference coefficients are 119.7 times fewer than RadrNet-DS-CI's, while recall is 15.56 percentage points higher than this strongest competitor. In a separate low-label protocol, SCORE reaches 71.58% recall with one labeled source window per class. A nonlinear projector converts four frozen fault similarities into five soft tokens, linking compact diagnosis to class-conditioned maintenance guidance. On 75 development questions covering 24 radar windows, language adaptation raises correct-fault answers from 45 to 62 (60.0% to 82.7%) relative to removing the co-trained adapters, while retaining the same projector. SCORE-LM thus combines a compact radar specialist with a language interface for communicating fault-specific inspection guidance.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

雷达硬件故障会威胁自动驾驶感知系统的可靠性，因此需要准确、紧凑的故障诊断方法以及可理解的维护指导。然而，现有方法面临两个核心困难：其一，雷达观测同时依赖环境和仪器状态，分类器容易将特定场景或记录与故障标签错误关联，而学不到可迁移的故障证据；其二，故障标签需要受控的硬件干预才能获取，导致大规模多样化训练集难以构建。此外，分类之后还存在沟通障碍：操作人员需要的是可理解的故障描述和后续检查建议，而非一个整数标签；但语言模型虽然提供了灵活接口，却可能编造从未测量到的观测，例如声称回波完全缺失或接收机受损，因此分类准确率与答案可靠性必须分开评估。针对上述问题，本文提出SCORE-LM，将紧凑的散射体条件化算子响应编码器与适配的本地语言模型相连接。其雷达部分SCORE结合自参考复轨迹、物理描述符和选择性状态空间分支，采用仅源域自监督和方向性故障推断，在Rad-R数据集上以极少的推理系数实现领先的故障识别性能；语言部分则冻结雷达编码器，通过非线性投影器将四个故障相似度转换为五个软令牌，从而在保持诊断紧凑性的同时，为操作人员生成与故障类别条件相关的维护指导，并区分故障正确性、与专家判断的一致性以及无依据陈述。

### Q2: 有哪些相关研究？

相关研究主要可分为四类。方法类上，RadrNet-DS-CI 用捕获不变预处理结合 IQ 与 RD 自适应门控，是本文最强竞争者，但参数量大且仅用两折评估；本文 SCORE 以 39,520 个系数实现更紧凑编码，召回率高出 15.56 个百分点。域泛化方面，Deep CORAL、MixStyle、DARM、DDDG、BDC、DWCN 等被适配到雷达，本文则采用仅源域自监督与方向性故障推断，并明确目标排除与最终检查点选择。序列建模上，Mamba、Mamba-2、S4 提供选择性状态空间基础，Deep Sets 支持置换不变聚合，VICReg 与掩码自编码器启发自监督目标，本文将其组合为散射体条件算子响应编码器。语言接口方面，BearLLM、FaultGPT、FD-LLM 探索振动或设备故障问答，BLIP-2、前缀微调、LoRA 提供连续条件与冻结语言模型适配思路，但均非雷达场景；本文用非线性投影器把四个冻结故障相似度转为五个软 token，并单独评测故障正确性与无支撑陈述。评测类上，DomainBed 指出模型选择偏差，FActScore、SelfCheckGPT 与幻觉研究启发了本文对断言忠实性的检查。

### Q3: 论文如何解决这个问题？

SCORE-LM 采用“雷达专家 + 语言接口”的两阶段解耦架构。第一阶段是 SCORE 雷达表征编码器：对每个雷达帧先做距离 FFT 与多普勒 FFT，通过局部极大值检测选出至多 16 个峰值；对每个峰值提取 64×8 的自参考复数轨迹和 54 维物理描述子，分别经时间分支和描述子分支编码后融合，再对峰值做置换不变的掩码均值池化，得到 128 维帧嵌入。时间分支的核心是一个选择性状态空间模型（SSM）块，采用输入依赖的 Δ、B、C 和 16 维隐状态递归，配合因果深度卷积与 SiLU 门控，实现线性复杂度的长序列建模。训练仅用源域自监督：掩码重建、双视图不变性、方差与协方差正则，故障标签不进入表征目标。诊断阶段冻结编码器，用源域十帧窗口估计四类故障相对健康中心的单位方向向量，查询窗口的嵌入减去健康中心并归一化后，与四个方向做余弦相似度，取最大者为预测故障，具有径向不变性和分数间隔鲁棒性。第二阶段是分数到语言对齐：将四个原始相似度经 4→256→1024→12800 的三层非线性投影器映射为五个软 token，作为 Qwen 语言模型的唯一雷达输入，同时用 rank-8 LoRA 适配语言解码器，仅训练投影器和 LoRA，冻结 SCORE 与语言基座，以答案 token 交叉熵为目标。创新点在于：用自参考复数轨迹与物理描述子结合 SSM 实现极紧凑的雷达专家（仅 39,520 个推理系数）；用方向性故障推断替代分类头；以及通过分数瓶颈将紧凑诊断与类别级维护指导语言生成连接起来。

### Q4: 论文做了哪些实验？

论文围绕雷达硬件故障诊断开展了多组实验。主实验在八个排除捕获的Rad-R故障记录上进行，采用五种子、十帧窗口协议，对比九种方法（RD-CNN ERM、CORAL、MixStyle、DARM、DDDG、BDC、DWCN、RadrNet-DS-CI及SCORE）。SCORE取得88.39%平均捕获召回率和88.20%四故障宏F1，较最强竞争者RadrNet-DS-CI（72.83%召回、77.37%F1）高15.56个百分点，且推理系数仅39,520个，比RadrNet少119.7倍。类别上，SCORE对振动召回100%、失准92.5%、堵塞78.4%、退化82.0%，但退化召回低于RadrNet的96.5%。低标签实验中，每类仅1个标注源窗口时SCORE召回71.58%，比最强竞争者DARM高19.19个百分点。消融实验显示，移除IQ/SSM分支后十帧召回从88.39%降至87.47%，仅用时间分支则降至44.58%。语言接口方面，在75个维护问题、24个雷达窗口上，加入rank-8 LoRA后正确故障回答从45/75（60.0%）提升至62/75（82.7%），解码器一致率从62.7%升至89.3%。

### Q5: 有什么可以进一步探索的点？

论文的局限主要体现在三方面：其一，阻塞与退化两类故障混淆严重，SCORE 对退化召回（82.0%）甚至低于 RadrNet（96.5%），说明幅度或响应质量变化无法唯一归因于物理机制；其二，语言评估仅 75 题、24 个窗口，且所有回答均为四类模板，缺乏真实维护语料的泛化验证；其三，时序分支贡献仅 0.92 个百分点，而时序单独输入时性能骤降至 44.58%，说明物理描述子仍占主导，状态空间建模的潜力未被充分释放。

未来可探索：引入故障机理先验或频域相位特征以解耦阻塞与退化；扩展到多故障并发与未知故障的开集诊断；用真实维护日志替代模板，评估语言接口的忠实性与幻觉风险；此外，可尝试将方向性读出与不确定性校准结合，在低标签场景下给出可拒识的维护建议。

### Q6: 总结一下论文的主要内容

论文针对雷达硬件故障诊断中环境依赖强、故障标签稀缺以及分类结果难以转化为可理解维护建议的问题，提出SCORE-LM框架。其核心是SCORE编码器：将雷达帧表示为散射体条件响应，融合复数轨迹的选择性状态空间分支与物理描述符分支，并通过仅源域自监督预训练和方向性故障推断实现诊断。在Rad-R数据集上，SCORE在十帧设置下达到88.39%平均捕获召回率和88.20%四类宏F1，推理系数仅39,520个，比RadrNet-DS-CI少119.7倍，召回率高15.56个百分点；单标签窗口下召回率达71.58%。语言侧将四个冻结故障相似度经非线性投影器映射为五个软令牌，连接本地语言模型生成故障条件维护指导。在75个问题上，语言适配将正确故障回答从45提升至62，表明紧凑雷达专家可与语言接口结合，输出可理解的检查建议。
