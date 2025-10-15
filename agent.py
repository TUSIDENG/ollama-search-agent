# agent.py - LangChain Optimized Version
from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool
from langchain.schema import SystemMessage
from langchain_tools import SearchTool
from config import OLLAMA_CONFIG, OPENAI_API_CONFIG


class LangChainSearchAgent:
    """LangChain-based search agent with tool usage capabilities."""
    
    def __init__(self, llm_client, tools: List[BaseTool] = None):
        self.llm_client = llm_client
        self.tools = tools or []
        self.agent_executor = None
        self._setup_agent()
    
    def _setup_agent(self):
        """Setup the LangChain agent with tools and prompt."""
        try:
            from langchain.agents import create_react_agent, AgentExecutor
            from langchain_core.prompts import PromptTemplate
            
            # Create the ReAct prompt template with required variables
            react_prompt = PromptTemplate.from_template("""You are a helpful AI assistant that can search the web for information.
Your goal is to help users find accurate and relevant information by using the search tools available to you.

When you need to find current information, facts, or verify something, use the web_search tool.
Always provide comprehensive and well-structured answers based on the search results.

Guidelines:
1. Use the search tool when you need up-to-date information or facts
2. Be thorough in your analysis of search results
3. Cite sources when possible
4. If search results are insufficient, acknowledge limitations
5. Provide clear, well-structured answers

TOOLS:
------

You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Question: {input}

{agent_scratchpad}""")
            
            # Create ReAct agent
            agent = create_react_agent(
                llm=self.llm_client,
                tools=self.tools,
                prompt=react_prompt
            )
            
            # Create agent executor
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True
            )
        except Exception as e:
            print(f"Warning: Failed to initialize LangChain agent: {e}")
            print("Falling back to simple tool execution...")
            self.agent_executor = None
    
    def run(self, query: str) -> str:
        """Run the agent with the given query."""
        print(f"--- Running LangChain agent for query: '{query}' ---")
        
        try:
            # Execute the agent
            result = self.agent_executor.invoke({"input": query})
            return result.get("output", "No response generated")
            
        except Exception as e:
            error_msg = f"Agent execution failed: {str(e)}"
            print(f"Error: {error_msg}")
            return error_msg


def create_search_agent(llm_type: str = "ollama", search_engine: str = "auto"):
    """Factory function to create a LangChain search agent."""
    
    # Create proper LangChain LLM
    if llm_type == "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            api_key=OPENAI_API_CONFIG["api_key"],
            base_url=OPENAI_API_CONFIG["base_url"],
            model=OPENAI_API_CONFIG["model"]
        )
    else:
        from langchain_community.llms import Ollama
        llm = Ollama(
            base_url=OLLAMA_CONFIG["host"],
            model=OLLAMA_CONFIG["model"]
        )
    
    # Create search tool with specified engine
    from langchain_tools import create_search_tool
    search_tool = create_search_tool(engine=search_engine)
    
    # Create agent with tools
    agent = LangChainSearchAgent(
        llm_client=llm,
        tools=[search_tool]
    )
    
    return agent


def main():
    """Example usage of the LangChain optimized agent."""
    # Create agent with default settings
    agent = create_search_agent(llm_type="ollama", search_engine="auto")
    
    # Test queries
    test_queries = [
        "What are the latest advancements in AI?",
        "Find information about climate change effects",
        "What's the current weather in San Francisco?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        result = agent.run(query)
        print(f"\nFinal Answer:")
        print(result)
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
