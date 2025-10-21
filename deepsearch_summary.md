# Deep Research 技术深度解析总结

参考于：https://mp.weixin.qq.com/s/ZjV0BQs7RkYHwhG8oJcR9Q

本文深度解析了Deep Research（深度研究/深度搜索）技术，这是一种以大型语言模型（LLM）为核心构建的应用系统，旨在自动化和增强研究任务。它通过多步推理驱动大规模联网检索、跨源证据归并与结构化写作，并产出带引用的研究级结果。

## 1. Deep Research Agent 的核心定义与能力边界

### 核心定义
Deep Research Agent 是一种由LLM驱动的AI智能体，它集成了动态推理、自适应规划、多迭代外部数据检索和工具使用，以及为信息研究任务生成全面分析报告的能力。

### 核心能力
*   **智能知识发现（Intelligent Knowledge Discovery）**：自主进行文献调研、假设生成、研究模式识别。
*   **端到端工作流自动化（End-to-End Workflow Automation）**：AI驱动的流程，完成方案设计、数据收集/分析及结果报告产出。
*   **协作智能增强（Collaborative Intelligence Enhancement）**：提供友好接口促进人机协作，包括自然语言交互、可视化和动态知识表征。

### 定义边界
*   **与通用模型/Agents的区别**：具备自动化的工作流、专用的研究工具、端到端的研究规划与编排能力。
*   **与单功能科研工具的区别**：能将模型的推理能力与单一工具结合，通过编排和规划解决问题。
*   **与单纯的LLM应用相比**：具备环境交互、工具集成和工作流自动化的能力。

## 2. Deep Research Agent 核心技术架构

Deep Research Agent 的架构和工作流设计分为静态工作流和动态工作流两类。

### 静态工作流（Static Workflow）
*   **特点**：依赖人为定义的任务管道（pipeline），如将调研任务分解为需求处理、信息检索、内容解析、总结输出等阶段，并预定义每个阶段的工具和子流程。
*   **优势**：结构清晰，易于实现和容错，适用于任务交付稳定性要求高、难度不大、链路较长的场景。
*   **劣势**：泛化能力有限，固定步骤难以迁移到不同任务场景。

### 动态工作流（Dynamic Workflow）
*   **特点**：支持动态任务规划，智能体根据反馈和上下文调整执行步骤，完全由模型自主完成规划、执行、反思、调整的闭环。
*   **优势**：灵活性和泛化能力强，处理复杂任务能力更强。
*   **劣势**：对LLM能力要求高，稳定性差，排错难度大。
*   **细分**：
    *   **单智能体架构（Single-Agent Architecture）**：通过单一智能体的规划、执行、反思循环完成任务，依赖模型强大的推理能力和长上下文窗口。
    *   **多智能体架构（Multi-Agent Architecture）**：通过多个专用智能体实现任务灵活分配，模拟人类团队协作，通常由一个规划者智能体进行任务拆分与分配，子任务智能体执行，最后由特定智能体交付结果。

### 工具使用
*   **网络搜索**：
    *   **基于搜索API**：通过搜索引擎或科学数据库API获取结构化数据，缺点是受限于API功能，无法灵活操作网页。
    *   **基于浏览器模拟**：在沙箱环境中模拟人类操作，实时提取网页内容，缺点是资源消耗大、延迟高，解析动态网页内容易遇瓶颈。
*   **代码解释器（数据分析）**：在沙箱环境中执行Python代码，提供数据处理、算法验证和模型仿真能力。
*   **多模态处理与生成**：支持图像、音频、视频处理，并能基于TTS、文生图/视频等方式实现多模态输出。

### 优化方法
*   **提示词工程（Prompt Engineering）**：成本最低、迁移速度最快，但鲁棒性有限，适合快速原型。
*   **监督微调（Supervised Fine-Tuning）**：通过高质量专用数据，优化智能体在特定环节的表现。
*   **强化学习（Reinforcement Learning）**：通过与环境的真实交互和奖励信号，优化信息检索、动态工具调用和复杂推理能力。
*   **非参数持续学习（Non-Parametric Continual Learning）**：通过持续交互优化外部记忆库、工作流和工具配置，如案例推理（CBR）。

## 3. 主流闭/开源工作分析

文章分析了A.deep research、B.DeerFlow、C.sicra(mini-perplex)、D.open_deep_research、E.Open Deep Search、F.OpenDeepResearcher等项目，总结了它们的架构、工作流程和核心特性。

### 开源工作介绍

#### A. deep research
*   **工作来源**：David Zhang Co-founder & CEO @ Aomni (aomni.com)，GitHub: [https://github.com/dzhng/deep-research](https://github.com/dzhng/deep-research) (star 17k)
*   **主要架构**：静态工作流。
    *   **基础配置**：搜索引擎使用Firecrawl API，模型使用OpenAI API (o3 mini model)。
    *   **工作流程**：
        1.  **Query与参数输入**：要求输入query、depth（循环次数）、breadth（单轮搜索query数目）以及isReport（报告还是简单回答）。
        2.  **Human-in-the-loop (报告模式)**：调用模型生成问题询问用户以澄清研究问题，组合初始query、follow-up question和用户回答作为输入query。
        3.  **Deep Research 递归**：模型根据前述query和已有研究learning生成SERP搜索query和研究目标，确保多样性和递进性。并发检索与解析使用Firecrawl抓取内容，模型总结learning和follow up questions。管理depth与breadth状态，生成新的输入query。根据depth条件判断是否递归调用或返回所有learning信息和URL访问历史。
        4.  **后处理**：搜索树形成后，去重合并所有learning和URL访问历史。
        5.  **结果生成**：调用模型生成报告或直接回复，输入learning、human-in-the-loop环节得到的组合query、系统提示词、历史URLs。
*   **核心特性**：迭代搜索（递归构建搜索树）、query生成（智能体生成有针对性的搜索query）、深度/广度控制（暴露搜索树参数）、并发处理。
*   **小结**：使用LLM总结提炼learning以减少报告上下文压力，构建搜索树以增加搜索历史多样性，暴露控制选项以平衡成本和时间。代码实现轻量简洁。

#### B. DeerFlow
*   **工作来源**：字节DeerFlow团队，GitHub: [https://github.com/bytedance/deer-flow](https://github.com/bytedance/deer-flow) (star 15.2k)
*   **主要架构**：多智能体架构。
    *   **基础配置**：搜索引擎支持Tavily (default)、DuckDuckGo、Brave Search、Arxiv；个人知识库支持RAGFlow、vikingdb；模型支持OpenAI-compatible API interface、Qwen等开源模型、litellm可集成模型。
    *   **工作流程**：
        1.  **Coordinater判断**：处理简单问候、安全/道德风险、需要更多信息等情况，或调用handoff_to_planner生成research_topic和locale。
        2.  **Background_investigator搜索**：使用coordinater传递的research topic作为query进行搜索，完成后handoff给planner。
        3.  **Planner确定研究计划**：获取背景信息，检查循环边界，生成JSON形式的计划。检查计划是否足够满足回答要求，否则handoff给human feedback。
        4.  **Human feedback修改计划**：用户可拒绝计划返回planner重新生成，或接收计划并handoff给research team。
        5.  **Research Team执行计划**：根据研究计划依次调用researcher（网络搜索、本地数据库搜索）和coder（执行Python工具）进行资料收集或代码执行。完成计划后回到planner运行逻辑，决定是否继续规划或handoff给reporter。
        6.  **Reporter输出报告**：获取plan、observation等上下文信息，生成报告（支持多模态）。
*   **核心特性**：human-in-the-loop（支持计划修改）、Report Post-Editing（支持报告生成后继续修改）、内容生成（支持播客与PPT多种形式的结果输出）。
*   **小结**：以模型能力为核心的多智能体实现，工具以tool形式传递给ReAct风格的agent，提供大量规范的prompt可参考。使用state记录核心上下文信息在所有node间传递。

#### C. sicra (mini-perplex)
*   **工作来源**：Zaid Mukaddam（独立开发者），GitHub: [https://github.com/zaidmukaddam/scirastar](https://github.com/zaidmukaddam/scirastar) (star 9.9k)
*   **主要架构**：管道式（pipeline-based）。
    *   **基础配置**：搜索支持exa、tavily、x、reddit；工具支持Google Maps、OpenWeather、Daytona、TMDB、Aviation Stack；模型支持xAI、Google、Anthropic、OpenAI、GRoq。
    *   **工作流程 (extreme mode)**：
        1.  **搜索模式分组**：前端显式指定搜索模式和使用模型，进行用户信息和模型权限校验，按照搜索模式分配可用工具组和instruction。
        2.  **模型流式调用**：传入sys prompt、user query和工具（如Extreme Search Tool），要求模型立刻调用搜索工具且不修改用户信息。
        3.  **Extreme Search Tool内部**：使用exa进行搜索和内容解析。要求顺序运行query，为目标topic进行一定次数范围的搜索，丰富调研视角（broad overview → specific details → recent developments → expert opinions），指定不同分类（news, research papers, company info, financial reports, github），渐进式完善搜索，多样性和交叉验证。
        4.  **Plan**：使用原始prompt+内置模型scira-x-fast进行breakdown。
        5.  **Research**：使用plan结果+内置模型scira-x-fast-mini+tools（code和search）进行search-driven research。
        6.  **Search tool**：接收search query和category进行搜索，对URL进行内容解析。
        7.  **Coding tool**：接收code使用沙盒运行代码返回结果（可视化、数学计算、数据分析）。
*   **核心特性**：多种搜索模式分配不同需求（Web、Memory、Analysis、Chat、X、Reddit、Academic、YouTube、Extreme），为多种功能提供工具适配。
*   **小结**：按照不同场景制定搜索模式，交由用户指定，进一步为场景匹配针对性工具。框架依赖prompt engineering和简单的模型流式调用进行任务分层，不涉及ReAct等框架。对不同环节和组件按照不同原则选择模型。搜索优化逻辑可能无法单纯依赖于强大搜索引擎，更多依赖Agent能力（提示词、reflection）。

#### D. open_deep_research (LangChain AI)
*   **工作来源**：LangChain AI，GitHub: [https://github.com/langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) (star 7.2k)
*   **主要架构**：多智能体架构。
    *   **基础配置**：搜索支持Tavily、Anthropic和OpenAI原生网络搜索、MCP；工具支持大量MCP工具兼容；模型使用Summarization(openai:gpt-4.1-mini)、Research/Compression/Final Report Model(openai:gpt-4.1)。
    *   **工作流程**：
        1.  **研究范围->确认研究意图**：用户意图澄清（模型询问用户获取额外上下文），研究概要生成（涵盖研究问题、调研要求、调研思路、报告要求）。
        2.  **执行研究->获取上下文**：Research Supervisor接收研究概要，拆分为多个独立的子主题，分配给sub-agent进行并行信息收集。Research Sub-Agents基于Supervisor分发的子主题，通过tool-calling循环进行调研，完成调研后总结findings返回Supervisor。Research Supervisor Iteration基于Sub-Agents的findings和研究概要进行反思，确定是否需要进一步信息收集。
        3.  **撰写报告->形成产出**：基于前述过程积累的findings和最初的研究概要，直接生成最终报告。
*   **核心特性**：完整的研究意图澄清（主动做总结和reflection）、更干净的上下文交付（各环节和agent之间靠处理后的内容交互）、保持deep research工作流的动态特性（可配置或自动扩展、动态调整）。
*   **小结**：在sub-agent层级放开模型自主进行tool calling，全局仍保持supervisor做规划、反思，兼顾稳定与灵活。多agent之间信息不通、结果连贯性问题可通过替换中间交付内容解决。合理设计上下文可降低对模型能力要求、提高结果质量。

## 4. 总结与未来展望

### 关键结论
*   **理解模型能力边界并及时调整任务**：根据模型能力进展，重新思考工作流中哪些结构应由模型接管。
*   **多轮、可递进的搜索管道**：查询生成应依据“已学到的 learnings / findings”自适应收敛或发散，避免一次性生成大量冗余关键词。
*   **交付“干净”的上下文**：在每个环节进行去重、重排、提炼，汇成结构化的 learnings/findings，提高稳定性并降低成本。
*   **通过更换节点分工改善性能**：例如在多智能体架构中，让每个agent交付整理后的信息，由最终报告生成agent来撰写，可解决连贯性问题。
*   **Human-in-the-loop环节简单而重要**：设计合理的意图澄清机制，如询问用户问题、生成并允许用户修改计划。
*   **智能体仍需学会用好工具**：优化查询改写以搜集合适信息，并考虑专用引擎作为补充。

### 未来展望
*   **合理且全面的评测基准**：缺乏权威、全面的开源评测基准，需要设计符合Deep Research任务特点的端到端测评体系。
*   **扩展信息来源与优化内容解析**：通过MCP工具获取更多专业数据库、媒体、学术网站数据；设计智能体原生的浏览器，提供显式API hook，便于检索、导航与信息抓取。
