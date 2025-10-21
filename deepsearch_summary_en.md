# Deep Research Technical Deep Dive Summary

Reference: https://mp.weixin.qq.com/s/ZjV0BQs7RkYHwhG8oJcR9Q

This article deeply analyzes Deep Research (deep research/deep search) technology, an application system built around large language models (LLMs), aiming to automate and enhance research tasks. It drives large-scale online retrieval through multi-step reasoning, merges evidence across sources, and performs structured writing, producing research-grade results with citations.

## 1. Core Definition and Capability Boundaries of Deep Research Agent

### Core Definition
A Deep Research Agent is an AI agent driven by LLMs, integrating dynamic reasoning, adaptive planning, multi-iterative external data retrieval and tool use, and the ability to generate comprehensive analytical reports for information research tasks.

### Core Capabilities
*   **Intelligent Knowledge Discovery**: Autonomous literature review, hypothesis generation, research pattern recognition.
*   **End-to-End Workflow Automation**: AI-driven processes for solution design, data collection/analysis, and report generation.
*   **Collaborative Intelligence Enhancement**: Provides user-friendly interfaces to promote human-machine collaboration, including natural language interaction, visualization, and dynamic knowledge representation.

### Definition Boundaries
*   **Distinction from General Models/Agents**: Possesses automated workflows, specialized research tools, and end-to-end research planning and orchestration capabilities.
*   **Distinction from Single-Function Research Tools**: Can combine the model's reasoning capabilities with a single tool to solve problems through orchestration and planning.
*   **Distinction from Pure LLM Applications**: Has the ability for environmental interaction, tool integration, and workflow automation.

## 2. Deep Research Agent Core Technical Architecture

The architecture and workflow design of Deep Research Agent are divided into two categories: static workflow and dynamic workflow.

### Static Workflow
*   **Characteristics**: Relies on human-defined task pipelines, such as breaking down research tasks into stages like demand processing, information retrieval, content parsing, and summary output, and pre-defining tools and sub-processes for each stage.
*   **Advantages**: Clear structure, easy to implement and fault-tolerant, suitable for scenarios requiring high task delivery stability, moderate difficulty, and long chains.
*   **Disadvantages**: Limited generalization ability, fixed steps are difficult to migrate to different task scenarios.

### Dynamic Workflow
*   **Characteristics**: Supports dynamic task planning, where the agent adjusts execution steps based on feedback and context, completing a closed loop of planning, execution, reflection, and adjustment entirely by the model itself.
*   **Advantages**: Strong flexibility and generalization ability, more capable of handling complex tasks.
*   **Disadvantages**: High demands on LLM capabilities, poor stability, and difficult debugging.
*   **Subdivisions**:
    *   **Single-Agent Architecture**: Completes tasks through a single agent's planning, execution, and reflection loop, relying on the model's powerful reasoning capabilities and long context window.
    *   **Multi-Agent Architecture**: Achieves flexible task allocation through multiple specialized agents, simulating human team collaboration. Typically, a planner agent performs task decomposition and allocation, sub-task agents execute, and finally, a specific agent delivers the results.

### Tool Usage
*   **Web Search**:
    *   **Based on Search API**: Obtains structured data through search engine or scientific database APIs. Disadvantage is being limited by API functions, unable to flexibly operate web pages.
    *   **Based on Browser Simulation**: Simulates human operations in a sandbox environment, extracting web content in real-time. Disadvantage is high resource consumption, high latency, and bottlenecks in parsing dynamic web content.
*   **Code Interpreter (Data Analysis)**: Executes Python code in a sandbox environment, providing data processing, algorithm verification, and model simulation capabilities.
*   **Multimodal Processing and Generation**: Supports image, audio, and video processing, and can achieve multimodal output based on TTS, text-to-image/video, etc.

### Optimization Methods
*   **Prompt Engineering**: Lowest cost, fastest migration speed, but limited robustness, suitable for rapid prototyping.
*   **Supervised Fine-Tuning**: Optimizes agent performance in specific环节 through high-quality specialized data.
*   **Reinforcement Learning**: Optimizes information retrieval, dynamic tool calling, and complex reasoning capabilities through real interaction with the environment and reward signals.
*   **Non-Parametric Continual Learning**: Continuously optimizes external memory banks, workflows, and tool configurations through continuous interaction, such as Case-Based Reasoning (CBR).

## 3. Analysis of Main Closed/Open Source Works

The article analyzes projects such as A.deep research, B.DeerFlow, C.sicra (mini-perplex), D.open_deep_research, E.Open Deep Search, and F.OpenDeepResearcher, summarizing their architectures, workflows, and core features.

### Introduction to Open Source Works

#### A. deep research
*   **Source**: David Zhang Co-founder & CEO @ Aomni (aomni.com), GitHub: [https://github.com/dzhng/deep-research](https://github.com/dzhng/deep-research) (star 17k)
*   **Main Architecture**: Static workflow.
    *   **Basic Configuration**: Search engine uses Firecrawl API, model uses OpenAI API (o3 mini model).
    *   **Workflow**:
        1.  **Query and Parameter Input**: Requires inputting query, depth (number of loops), breadth (number of queries per round), and isReport (report or simple answer).
        2.  **Human-in-the-loop (Report Mode)**: Calls the model to generate questions to ask the user to clarify research questions, combining initial query, follow-up questions, and user answers as input query.
        3.  **Deep Research Recursion**: The model generates SERP search queries and research goals based on the previous query and existing research learnings, ensuring diversity and progression. Concurrent retrieval and parsing use Firecrawl to fetch content, and the model summarizes learnings and follow-up questions. Manages depth and breadth states, generating new input queries. Determines whether to recursively call or return all learning information and URL access history based on depth conditions.
        4.  **Post-processing**: After the search tree is formed, de-duplicates and merges all learnings and URL access history.
        5.  **Result Generation**: Calls the model to generate a report or direct reply, inputting learnings, the combined query from the human-in-the-loop stage, system prompts, and historical URLs.
*   **Core Features**: Iterative search (recursively building search trees), query generation (agent generates targeted search queries), depth/breadth control (exposing search tree parameters), concurrent processing.
*   **Summary**: Uses LLM to summarize and refine learnings to reduce report context pressure, builds search trees to increase search history diversity, and exposes control options to balance cost and time. The code implementation is lightweight and concise.

#### B. DeerFlow
*   **Source**: ByteDance DeerFlow Team, GitHub: [https://github.com/bytedance/deer-flow](https://github.com/bytedance/deer-flow) (star 15.2k)
*   **Main Architecture**: Multi-agent architecture.
    *   **Basic Configuration**: Search engines support Tavily (default), DuckDuckGo, Brave Search, Arxiv; personal knowledge base supports RAGFlow, vikingdb; models support OpenAI-compatible API interface, Qwen and other open-source models, litellm integrable models.
    *   **Workflow**:
        1.  **Coordinator Judgment**: Handles simple greetings, safety/ethical risks, situations requiring more information, or calls handoff_to_planner to generate research_topic and locale.
        2.  **Background_investigator Search**: Uses the research topic passed by the coordinator as a query for searching, then hands off to the planner.
        3.  **Planner Determines Research Plan**: Obtains background information, checks loop boundaries, and generates a plan in JSON format. Checks if the plan is sufficient to meet the answer requirements, otherwise hands off to human feedback.
        4.  **Human Feedback Modifies Plan**: Users can reject the plan and return to the planner for regeneration, or accept the plan and hand off to the research team.
        5.  **Research Team Executes Plan**: According to the research plan, sequentially calls researcher (web search, local database search) and coder (executes Python tools) for data collection or code execution. After completing the plan, returns to the planner's logic to decide whether to continue planning or hand off to the reporter.
        6.  **Reporter Outputs Report**: Obtains plan, observation, and other context information to generate a report (supports multimodal).
*   **Core Features**: Human-in-the-loop (supports plan modification), Report Post-Editing (supports further modification after report generation), Content Generation (supports podcast and PPT output formats).
*   **Summary**: A multi-agent implementation centered on model capabilities, where tools are passed to a ReAct-style agent, providing a large number of standardized prompts for reference. Uses state to record core context information passed between all nodes.

#### C. sicra (mini-perplex)
*   **Source**: Zaid Mukaddam (Independent Developer), GitHub: [https://github.com/zaidmukaddam/scirastar](https://github.com/zaidmukaddam/scirastar) (star 9.9k)
*   **Main Architecture**: Pipeline-based.
    *   **Basic Configuration**: Search supports exa, tavily, x, reddit; tools support Google Maps, OpenWeather, Daytona, TMDB, Aviation Stack; models support xAI, Google, Anthropic, OpenAI, GRoq.
    *   **Workflow (extreme mode)**:
        1.  **Search Mode Grouping**: Frontend explicitly specifies search mode and model usage, performs user information and model permission verification, and allocates available tool groups and instructions according to the search mode.
        2.  **Model Streaming Call**: Passes sys prompt, user query, and tools (e.g., Extreme Search Tool), requiring the model to immediately call the search tool without modifying user information.
        3.  **Extreme Search Tool Internal**: Uses exa for search and content parsing. Requires sequential query execution, searching for the target topic within a certain range of times, enriching research perspectives (broad overview → specific details → recent developments → expert opinions), specifying different categories (news, research papers, company info, financial reports, github), progressively improving search, diversity, and cross-validation.
        4.  **Plan**: Uses the original prompt + built-in model scira-x-fast for breakdown.
        5.  **Research**: Uses the plan results + built-in model scira-x-fast-mini + tools (code and search) for search-driven research.
        6.  **Search Tool**: Receives search query and category for searching, parses content from URLs.
        7.  **Coding Tool**: Receives code and runs it in a sandbox, returning results (visualization, mathematical calculations, data analysis).
*   **Core Features**: Multiple search modes allocate different needs (Web, Memory, Analysis, Chat, X, Reddit, Academic, YouTube, Extreme), providing tool adaptation for various functions.
*   **Summary**: Formulates search modes according to different scenarios, specified by the user, and further matches targeted tools for the scenarios. The framework relies on prompt engineering and simple model streaming calls for task layering, not involving frameworks like ReAct. Selects models for different stages and components based on different principles. Search optimization logic may not solely rely on powerful search engines, but more on Agent capabilities (prompts, reflection).

#### D. open_deep_research (LangChain AI)
*   **Source**: LangChain AI, GitHub: [https://github.com/langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) (star 7.2k)
*   **Main Architecture**: Multi-agent architecture.
    *   **Basic Configuration**: Search supports Tavily, Anthropic and OpenAI native web search, MCP; tools support a large number of MCP tool compatibility; models use Summarization (openai:gpt-4.1-mini), Research/Compression/Final Report Model (openai:gpt-4.1).
    *   **Workflow**:
        1.  **Research Scope -> Confirm Research Intent**: User intent clarification (model asks user for additional context), research summary generation (covering research questions, research requirements, research ideas, report requirements).
        2.  **Execute Research -> Obtain Context**: Research Supervisor receives the research summary, breaks it down into multiple independent sub-topics, and assigns them to sub-agents for parallel information gathering. Research Sub-Agents, based on the sub-topics distributed by the Supervisor, conduct research through a tool-calling loop, and summarize findings back to the Supervisor after completion. Research Supervisor Iteration reflects on the Sub-Agents' findings and the research summary to determine if further information collection is needed.
        3.  **Write Report -> Form Output**: Based on the findings accumulated in the previous process and the initial research summary, directly generates the final report.
*   **Core Features**: Complete research intent clarification (proactively summarizes and reflects), cleaner context delivery (interaction between stages and agents relies on processed content), maintains the dynamic nature of deep research workflow (configurable or automatically expandable, dynamic adjustment).
*   **Summary**: At the sub-agent level, the model is allowed to autonomously perform tool calling, while the supervisor maintains overall planning and reflection, balancing stability and flexibility. Information discontinuity and result coherence issues between multiple agents can be solved by replacing intermediate delivery content. Reasonable context design can reduce demands on model capabilities and improve result quality.

## 4. Summary and Future Outlook

### Key Conclusions
*   **Understand the boundaries of model capabilities and adjust tasks in a timely manner**: Re-evaluate which structures in the workflow should be taken over by the model based on model capability advancements.
*   **Multi-round, progressive search pipeline**: Query generation should adaptively converge or diverge based on "learned learnings/findings" to avoid generating a large number of redundant keywords at once.
*   **Deliver "clean" context**: De-duplicate, reorder, and refine at each stage, consolidating into structured learnings/findings to improve stability and reduce costs.
*   **Improve performance by changing node division of labor**: For example, in a multi-agent architecture, let each agent deliver organized information, and let the final report generation agent write the report, which can solve coherence issues.
*   **Human-in-the-loop is simple yet important**: Design reasonable intent clarification mechanisms, such as asking users questions, generating and allowing users to modify plans.
*   **Agents still need to learn to use tools well**: Optimize query rewriting to collect appropriate information, and consider specialized engines as supplements.

### Future Outlook
*   **Reasonable and comprehensive evaluation benchmarks**: Lack of authoritative, comprehensive open-source evaluation benchmarks; there is a need to design an end-to-end evaluation system that meets the characteristics of Deep Research tasks.
*   **Expand information sources and optimize content parsing**: Obtain more professional database, media, and academic website data through MCP tools; design an agent-native browser, providing explicit API hooks for retrieval, navigation, and information scraping.
