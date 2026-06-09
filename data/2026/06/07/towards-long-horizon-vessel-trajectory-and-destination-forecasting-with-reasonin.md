---
title: "Towards Long-Horizon Vessel Trajectory and Destination Forecasting with Reasoning Large Language Models"
authors:
  - "Hongwei Wang"
  - "Miao Zhou"
  - "Fengde Wang"
  - "Yuting Wang"
  - "Jiewen Yu"
  - "Jun-Yan He"
  - "Bohao Qu"
  - "Wanbing Zhang"
  - "Xiuju Fu"
  - "Qing Guo"
  - "Zipei Fan"
  - "Yingying Xing"
  - "Yi Yuan"
date: "2026-06-07"
arxiv_id: "2606.08633"
arxiv_url: "https://arxiv.org/abs/2606.08633"
pdf_url: "https://arxiv.org/pdf/2606.08633v1"
categories:
  - "cs.AI"
  - "cs.LG"
tags:
  - "LLM/Agent for Time Series"
  - "Time Series Report"
  - "Semantic Description"
  - "Verifiable Reward"
  - "Trajectory Forecasting"
  - "Maritime Decision Support"
  - "Reinforcement Learning"
  - "Reasoning LLM"
relevance_score: 7.5
---

# Towards Long-Horizon Vessel Trajectory and Destination Forecasting with Reasoning Large Language Models

## 原始摘要

Long-horizon maritime trajectory prediction is important for shipping management, logistics planning, and maritime risk analysis, yet month-level forecasting remains insufficiently studied. Existing deep learning methods mainly focus on short- and mid-term coordinate extrapolation and often struggle to preserve route feasibility and destination correctness over extended horizons. This paper investigates joint long-horizon vessel trajectory and destination forecasting with reasoning-capable large language models, and develops a Maritime LLM post-training framework based on Reinforcement Learning with Verifiable Reward (RLVR). An AIS-based benchmark is constructed with 60-day historical trajectories and 30-day forecasting horizons, where trajectories are converted into semantic textual representations for RL prompt construction. RLVR aligns LLMs with maritime forecasting objectives by enforcing physical validity, providing early-weighted trajectory supervision, and evaluating destination correctness through hierarchical matching and curriculum learning. Experimental results show that RLVR-trained LLMs substantially improve over zero-shot LLMs and representative deep learning baselines, especially on destination-related metrics. Among the evaluated RLVR-trained variants, 4B LLMs achieve the best overall performance, suggesting that reward-compatible optimization and task-specific capacity matching are more important than simply using larger 8B or 14B LLMs. The results also show that LSTM remains a strong deep learning baseline under limited fine-tuning data, while Transformer-style spatio-temporal models typically require larger datasets and richer structured inputs. Overall, this work advances semantic, verifier-aligned maritime forecasting for operational decision support.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决长期（月级）船舶轨迹与目的地联合预测这一尚未充分研究的难题。研究背景在于，现有深度学习模型多聚焦于短期或中期的坐标外推，在数周至数月的预测跨度上，由于船舶运动不仅受局部动力学影响，更受目的地规划、航线可行性、运营约束等高层语义因素制约，导致基于逐点回归损失的模型难以保持航线合理性与目的地正确性。现有方法的不足主要体现在：缺乏对月级预测任务的专门研究；传统深度模型在长时域上容易产生不可行的轨迹；而零样本大语言模型虽具推理潜力，但未针对海事预测目标进行对齐优化。本文的核心问题是：如何利用具备推理能力的大语言模型，通过强化学习与可验证奖励机制，使其在60天历史轨迹输入下，准确预测未来30天的完整轨迹与最终目的地，同时保证预测结果的物理有效性与目的地匹配精度。为此，论文构建了基于AIS数据的语义化轨迹表示与RLVR训练框架，通过引入物理约束、早期加权监督及分层目的地匹配等奖励设计，实现模型与海事预测目标的深度对齐。

### Q2: 有哪些相关研究？

本文的相关研究主要分为三类：

1. **深度学习方法**：包括LSTM、GRU等循环模型，以及Informer、Autoformer、PatchTST等Transformer架构。这些方法在短期和中期的船舶轨迹预测上表现良好，但本文指出其点式回归范式难以处理月度级预测中的航线可行性和目的地意图，因此本文采用语义化轨迹表示和强化学习来弥补这一不足。

2. **大语言模型（LLM）用于时空预测**：如ST-LLM、Time-LLM、UrbanGPT通过标记化或嵌入方案适配结构化输入；Time-R1则利用强化学习微调提升推理能力。本文与这些工作的区别在于，本文专门针对月度级海事预测，提出了基于可验证奖励的RLVR框架，显式结合物理有效性、轨迹过程监督和分层目的地优化。

3. **海事领域的LLM应用**：如AIS-LLM探索了联合预测与异常检测，但主要聚焦短期场景。本文则面向长期预测，强调对航行意图和航线可行性的推理，并构建了60天历史+30天预测的基准数据集，这是现有海事LLM工作未覆盖的。

### Q3: 论文如何解决这个问题？

该论文提出了一种基于强化学习与可验证奖励（RLVR）的船舶轨迹与目的地联合预测框架，核心方法是将长时域预测转化为结构化语义推理问题。整体框架分为两阶段：首先，将原始AIS轨迹通过预处理、段级特征提取和语义编码转化为结构化文本提示，利用72B大模型将位置一致的轨迹段编码为保留路线语义和时间上下文的文本表示；其次，采用4B-14B的轻量级LLM作为策略模型，直接通过验证器引导的强化学习（GRPO）进行优化，跳过了传统的监督微调阶段。

关键技术包括：1）硬约束门控机制，通过检查输出结构、坐标有效性、日位移上限（约1333.2 km/day）和地理可行性（如陆地穿越）等条件，对无效输出施加固定惩罚（R_hard=-0.5），抑制物理不可行预测；2）过程奖励模型（PRM），对第1-29天轨迹逐日计算地理精度（r_t^acc）和路线走廊可行性（r_t^corr），并通过指数衰减权重（δ=0.92）强化早期预测监督；3）分层目的地匹配奖励，通过精确/模糊位置匹配、港口区域、海域、地理区域、国家等层级分配部分信用，并设置第27-30天匹配窗口处理到达时间不确定性；4）课程学习融合策略，从初始侧重轨迹可行性（α=0.2）逐渐过渡到最终侧重目的地正确性（α=0.85），使训练过程稳定收敛。

创新点在于：将长时域预测重构为受地理连通性和航行意图约束的结构化推理问题，而非简单坐标外推；通过RLVR直接对齐LLM输出与物理有效性、轨迹质量和目的地正确性等多维目标；实验表明4B模型在目的地指标上表现最佳，证明奖励兼容优化和任务特定容量匹配比单纯扩大模型规模更重要。

### Q4: 论文做了哪些实验？

论文基于2022年全球油轮AIS数据构建了包含60天历史轨迹和30天预测窗口的基准测试集，共7,654条轨迹片段（2,168艘船舶），按MMSI划分训练集（6,875条）和测试集（779条）。实验对比了零样本LLM、RLVR训练的LLM（4B/8B/14B参数）及代表性深度学习基线（LSTM、Transformer时空模型）。主要评估指标包括：目的地奖励（R_dest，基于分层地理匹配，允许Day27-30到达窗口）、轨迹奖励（R_traj，采用指数衰减权重δ=0.92加权每日位置精度和路径可行性）及综合得分（α=0.85加权R_dest和R_traj，含Day30端点奖励）。RLVR训练采用GRPO算法（4次rollout/提示，学习率1e-6，批次112，KL系数0.001），课程学习α从0.2递增至0.85。结果显示：RLVR训练的4B LLM在综合得分上最优，显著超越零样本LLM和深度学习基线，尤其在目的地相关指标上提升明显；LSTM在有限微调数据下仍具竞争力，而Transformer模型需更大数据集。关键发现是奖励兼容优化和任务容量匹配比单纯增大模型规模（8B/14B）更重要。

### Q5: 有什么可以进一步探索的点？

当前研究存在若干局限性。首先，基准数据集仅包含一年内的油轮数据，限制了模型的泛化能力，未来需扩展至多船型、多年份数据。其次，可验证奖励仍依赖规则化组件，对复杂海事场景的适应性不足，可探索基于物理仿真或领域知识图谱的自适应奖励函数。此外，当前方法将轨迹转化为语义文本，可能丢失细粒度时空连续性，未来可引入多模态融合（如结合AIS原始坐标与气象数据）的混合架构。在模型层面，4B参数LLM表现最优暗示任务特定容量匹配的重要性，但更大模型（8B/14B）的优化瓶颈值得深入分析，例如通过动态奖励加权或分层强化学习缓解过拟合。最后，当前仅聚焦于单步预测，可扩展至多步交互式决策支持，例如结合实时环境反馈的在线微调框架。

### Q6: 总结一下论文的主要内容

这篇论文研究了利用推理型大语言模型（LLM）进行长期船舶轨迹与目的地联合预测的问题。现有深度学习方法主要聚焦短期坐标外推，难以保证长周期航迹的可行性和目的地准确性。为此，论文提出了一种基于可验证奖励强化学习（RLVR）的海事LLM后训练框架：将AIS轨迹转换为语义文本表示构建RL提示，通过强制物理有效性、提供过程级轨迹监督以及基于课程学习的目的地正确性奖励，使LLM对齐海事预测目标。在构建的60天历史轨迹、30天预测基准上，实验表明RLVR训练的LLM显著优于零样本LLM和典型深度学习基线，尤其在目的地指标上表现突出。值得注意的是，4B参数模型取得了最佳综合性能，说明任务特定的容量匹配比单纯增大模型规模更重要。此外，LSTM在有限微调数据下仍是强基线，而Transformer类时空模型需要更大数据集。该工作推进了语义化、可验证对齐的海事预测，为运营决策支持提供了新范式。
