---
title: "Tool-Making and Self-Evolving LLM Agents in Low-Latency Systems"
authors:
  - "Kalle Kujanpää"
  - "Ning Liu"
  - "Shahnawaz Alam"
  - "Yeshwanth Reddy Sura"
  - "Tianyu Yang"
  - "Kristina Klinkner"
  - "Shervin Malmasi"
date: "2026-07-09"
arxiv_id: "2607.08010"
arxiv_url: "https://arxiv.org/abs/2607.08010"
pdf_url: "https://arxiv.org/pdf/2607.08010v1"
categories:
  - "cs.CL"
  - "cs.LG"
  - "cs.SE"
tags:
  - "Agentic Time Series"
  - "工业故障诊断"
  - "LLM Agent"
  - "工具调用"
  - "自进化"
  - "低延迟系统"
  - "报警分类"
  - "SOP编译"
  - "可追溯诊断链"
  - "工具制作"
relevance_score: 8.5
---

# Tool-Making and Self-Evolving LLM Agents in Low-Latency Systems

## 原始摘要

Production LLM agents often waste latency and reliability by regenerating code for the same procedural steps on every request. We replace this inference-time coding loop with an agentic tool-making pipeline that compiles repeated SOP steps into validated, versioned tools before deployment. The tool-maker grounds synthesis in the live environment as it collects execution traces, observes backend schemas and values, generates candidate tools, and repairs them against labeled cases. At runtime, the production agent calls these tools directly and falls back to code generation only when needed. We deploy the approach in a Fulfillment Center alarm-triage system, where an agent diagnoses alarms against a 44-node SOP over heterogeneous metric backends. In production, tool calls reduce p50 latency by 42%. On 1,500 historical alarms, they reduce end-to-end error rate by up to 53% by suppressing run-to-run variance in repeated steps. Because tools return compact structured verdicts, they also enable a simpler direct-call architecture, reducing p50 latency by a further 62% in a controlled ablation. Versioned tools also improve auditability and expose specification gaps and upstream data drift. Our results show that self-evolving agents can make industrial LLM systems faster, more reliable, and easier to operate.

## Q&A 论文解读

### Q1: 这篇论文试图解决什么问题？

这篇论文试图解决生产环境中LLM代理在重复执行标准操作流程（SOP）时，因每次请求都重新生成代码而导致的延迟高、可靠性差和运行结果不一致的问题。研究背景是，在工业故障诊断等场景中，代理需要根据SOP文档查询异构指标后端并执行诊断，但现有的CodeAct式方法在每次推理时都重新解释指令、发现模式并生成代码，导致大量重复劳动。现有方法的不足在于：1）延迟和成本高，因为重复步骤不断消耗LLM推理资源；2）运行间方差大，每次生成的代码可能不同，导致结果不稳定；3）错误率高，尤其在将模糊的SOP文本转换为具体查询时容易出错。本文的核心问题是：如何将重复的推理时代码生成过程，转化为离线构建可复用、已验证的工具，从而在保持灵活性的同时，显著降低生产系统的延迟、提升可靠性，并实现更好的可审计性。

### Q2: 有哪些相关研究？

在相关研究中，本文主要涉及工具使用与制造、迭代优化与数据接地两类工作。

**工具使用与制造类**：早期LLM工具使用聚焦于固定API调用，后续工作赋予智能体可执行代码的动作空间。近期研究让智能体自行构建工具，包括单次合成方法和基于测试或执行的迭代构建验证。例如，操作文档可被转化为工具，但现有工作如SOP-to-code仅在基准上评估。本文贡献在于将标准操作程序（SOP）编译为工具，并针对生产标注案例进行验证，部署于真实工业告警分类系统，实现了端到端错误率降低53%和延迟降低42%。

**迭代优化与数据接地类**：本文与执行反馈优化家族密切相关。先前研究指出自我修复的成功依赖于反馈质量，且文本到SQL领域发现仅依赖模式会达到性能上限，需要数据库值接地。本文发现工具生成管道缺乏环境接地时会停滞，与这些结论一致。此外，工具生成中规范质量的重要性与代码和SQL生成文献中的发现相呼应。本文通过在生产环境中收集执行轨迹、观察后端模式和值，实现了工具的自进化，提升了可靠性和可审计性。

### Q3: 论文如何解决这个问题？

该论文提出了一种**工具制造与自进化**的流水线方法，将推理时反复的代码生成循环替换为部署前编译好的、经过验证的版本化工具。核心方法包括三个主要组件：

1. **数据收集器**：在部署前，针对每个SOP节点，使用基线CodeAct子代理在真实生产环境上运行三个平衡样本，收集执行轨迹（包括查询代码、MCP响应、观测到的后端模式与字段值），从而补全SOP文本中缺失的执行细节。

2. **工具制造器**：基于SOP节点文本、决策树位置以及数据收集器的轨迹，生成候选工具函数。该工具具有统一签名（仓库、时间戳、上下文→判定结果），返回结构化判定（真/假/无数据）及支持细节。

3. **测试-修复循环**：将候选工具在完整标注训练集上测试，由反射器LLM分析失败案例并撰写诊断，工具制造器根据诊断和失败三元组（输入、期望、预测）重写工具。循环最多三轮，选择训练集通过率最高的候选工具部署。

创新点在于：工具是模型无关且可独立于智能体微调重新生成；通过版本化工具提升可审计性，暴露规范缺口和数据漂移；在推理时支持两种架构（子代理调用或主代理直接调用），直接调用架构进一步降低62%的p50延迟。此外，通过知识蒸馏（教师模型生成轨迹，LoRA微调学生模型）并引入随机工具禁用策略，确保学生模型在工具缺失时仍能稳健回退到代码生成。

### Q4: 论文做了哪些实验？

论文在工具构建和智能体部署两个阶段进行了实验。**实验设置**：工具构建阶段评估了四种模型（GLM-4.7、GLM-5、Qwen3 235B、GLM-4.7 Flash）作为工具制造者，在44个决策节点上，每个节点有100-200个训练样本和独立评估集，总计约16,033个案例。智能体部署阶段使用Qwen3 32B和GLM-4.5-Air模型，在1,500个历史告警场景上评估端到端正确性，并在生产环境中测量延迟。**对比方法**：工具构建阶段对比了仅使用SOP文本、添加数据收集轨迹(+D)、添加测试修复循环(+R)及其组合。智能体部署阶段对比了无工具（子智能体写代码）、子智能体调用工具、主智能体直接调用工具三种配置。**主要结果**：工具构建方面，GLM-4.7在完整配置(SOP+D+R)下达到94.5%的pass@1（每个节点所有案例正确），GLM-5为93.6%，而Qwen3 235B仅81.1%。修复循环和轨迹分别贡献9.6pp和5.2pp的提升。智能体部署方面，工具调用使生产环境p50延迟降低42%（从100降至58），直接调用架构进一步降低62%（至26）。端到端错误率方面，工具使Qwen3 32B错误率从2.8%降至1.8%（降低36%），GLM-4.5-Air从1.7%降至0.8%（降低53%）。

### Q5: 有什么可以进一步探索的点？

论文的局限性主要体现在三个方面：一是仅在一个应用场景（出库 dock 报警分类）上验证，泛化性尚未确认；二是改进循环仍依赖人工审查，无法保证全自动捕获所有故障；三是创建新工具仍需标注案例，无标注配置的性能与有标注上限仍有差距。

未来可从以下方向探索：首先，将工具制造循环推广到自由格式的 runbook 等更通用的 agentic 工作流，验证其跨领域迁移能力。其次，研究如何实现完全自动化的故障检测与修复，例如利用 LLM 自身进行异常模式识别并自动触发重生成-测试-修复循环，减少人工介入。再次，探索完全无标注的工具生成方法，通过主动学习或自监督方式从执行轨迹中自动提取标注案例。最后，可进一步优化参数化工具的泛化能力，使其能自动适应不同站点的阈值差异，甚至通过元学习自动发现环境漂移并触发工具版本更新。

### Q6: 总结一下论文的主要内容

这篇论文提出了一种面向低延迟生产环境的LLM Agent工具制造与自进化方法。核心问题是：传统LLM Agent在每次请求时都重复生成代码，导致高延迟和不可靠性。为此，论文设计了一个离线工具制造管线，将重复的标准操作程序（SOP）步骤编译为经过环境验证和版本化的工具。方法上，工具制造者通过收集执行轨迹、观察后端模式与值、生成候选工具并基于标注案例进行修复，将工具在真实环境中落地。运行时，生产Agent直接调用这些工具，仅在必要时回退到代码生成。在部署于配送中心告警分类系统的实验中，Agent需基于44节点SOP诊断异构指标后端的告警。主要结论显示：工具调用使p50延迟降低42%，在1500个历史告警上端到端错误率降低53%，通过抑制重复步骤的逐次方差提升了可靠性。版本化工具还增强了可审计性，暴露了规范缺口和数据漂移。该工作的核心贡献是提出了一种工业Agent自进化模式，使LLM能在离线测试中构建和修复自身行动空间，从而在操作工作流中实现更快、更一致、更可靠的低延迟系统。
