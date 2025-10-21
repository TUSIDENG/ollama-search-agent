# agent.py - LangChain Optimized Version
from typing import List, Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import BaseTool
from langchain.schema import SystemMessage
from langchain_tools import SearchTool
from config import OLLAMA_CONFIG, OPENAI_API_CONFIG
from langchain_core.messages import HumanMessage, SystemMessage


class LangChainSearchAgent:
    """DeepSearch agent with iterative research capabilities."""
    
    def __init__(self, llm_client, tools: List[BaseTool] = None):
        self.llm_client = llm_client
        self.tools = tools or []
        self.search_tool = self._get_search_tool()
        self.max_depth = 3 # Default max iterations for iterative search
        self.initial_query_prompt_template = PromptTemplate.from_template(
            """You are a research assistant. Your task is to break down a user's research query into 3-5 diverse sub-queries or research questions.
            These sub-queries should cover different aspects of the main topic to ensure comprehensive research.
            Return the sub-queries as a comma-separated list.

            User Query: {user_query}

            Sub-queries:"""
        )
        self.summarize_content_prompt_template = PromptTemplate.from_template(
            """You are a helpful assistant. Your task is to summarize the provided search results to answer the following sub-query.
            Focus on extracting key information and providing a concise summary.

            Sub-query: {sub_query}
            Search Results: {search_results}

            Summary:"""
        )
        self.follow_up_query_prompt_template = PromptTemplate.from_template(
            """You are a research assistant. Based on the original research query and the current findings,
            generate 1-2 new, refined follow-up search queries to delve deeper into specific points or explore related angles.
            Return the follow-up queries as a comma-separated list. If no further queries are needed, return an empty string.

            Original Query: {original_query}
            Current Findings: {current_findings}

            Follow-up Queries:"""
        )
    
    def _get_search_tool(self) -> SearchTool:
        """Extracts the SearchTool from the list of tools."""
        for tool in self.tools:
            if isinstance(tool, SearchTool):
                return tool
        raise ValueError("SearchTool not found in the provided tools.")

    def _generate_initial_queries(self, user_query: str) -> List[str]:
        """
        Generates an initial set of diverse sub-queries based on the user's main query.
        """
        print(f"LLM: Generating initial queries for: '{user_query}'")
        prompt = self.initial_query_prompt_template.format(user_query=user_query)
        response = self.llm_client.invoke([HumanMessage(content=prompt)])
        
        # Assuming the LLM returns a comma-separated string of queries
        sub_queries = [q.strip() for q in response.content.split(',') if q.strip()]
        return sub_queries if sub_queries else [user_query] # Fallback to original query if LLM fails

    def _execute_search(self, query: str) -> str:
        """Executes a search using the configured search tool."""
        print(f"Executing search for: '{query}'")
        if self.search_tool:
            return self.search_tool.run(query)
        return "No search tool available."

    def _extract_and_summarize_content(self, search_results: str, sub_query: str) -> str:
        """
        Extracts key information and summarizes content from search results
        relevant to the sub-query.
        """
        print(f"LLM: Summarizing content for sub-query: '{sub_query}'")
        prompt = self.summarize_content_prompt_template.format(
            sub_query=sub_query,
            search_results=search_results
        )
        response = self.llm_client.invoke([HumanMessage(content=prompt)])
        return response.content

    def _generate_follow_up_queries(self, current_findings: List[Dict[str, str]], original_query: str) -> List[str]:
        """
        Generates new, refined follow-up search queries based on current findings.
        """
        print(f"LLM: Generating follow-up queries based on current findings.")
        findings_str = "\n".join([f"- {f['summary']} (Source: {f['source']})" for f in current_findings])
        prompt = self.follow_up_query_prompt_template.format(
            original_query=original_query,
            current_findings=findings_str
        )
        response = self.llm_client.invoke([HumanMessage(content=prompt)])
        follow_up_queries = [q.strip() for q in response.content.split(',') if q.strip()]
        return follow_up_queries

    def _merge_and_refine_findings(self, all_findings: List[Dict[str, str]]) -> str:
        """
        De-duplicates, consolidates, and performs a preliminary synthesis of all findings.
        """
        print(f"LLM: Merging and refining all findings.")
        findings_str = "\n".join([f"- {f['summary']} (Source: {f['source']})" for f in all_findings])
        
        merge_refine_prompt_template = PromptTemplate.from_template(
            """You are a research assistant. Your task is to de-duplicate, consolidate, and synthesize the following research findings from various sources.
            Identify key themes, resolve potential contradictions, and structure the raw findings into a more organized and coherent format.

            Research Findings:
            {findings_str}

            Consolidated and Refined Findings:"""
        )
        prompt = merge_refine_prompt_template.format(findings_str=findings_str)
        response = self.llm_client.invoke([HumanMessage(content=prompt)])
        return response.content

    def _generate_final_report(self, refined_findings: str, original_query: str) -> str:
        """
        Generates a comprehensive final report based on the refined findings.
        """
        print(f"LLM: Generating final report for: '{original_query}'")
        final_report_prompt_template = PromptTemplate.from_template(
            """You are a professional research report writer. Your task is to generate a comprehensive, well-organized, and coherent research report
            based on the following refined findings and the original research query.
            Ensure the report includes clear citations/references to the original source URLs where applicable.

            Original Research Query: {original_query}
            Refined Findings: {refined_findings}

            Comprehensive Research Report:"""
        )
        prompt = final_report_prompt_template.format(
            original_query=original_query,
            refined_findings=refined_findings
        )
        response = self.llm_client.invoke([HumanMessage(content=prompt)])
        return response.content

    def deep_search(self, user_query: str) -> str:
        """
        Orchestrates the DeepSearch workflow.
        """
        print(f"--- Starting DeepSearch for query: '{user_query}' ---")
        
        all_accumulated_findings = []
        
        # 1. Initial Research Planning & Query Generation
        initial_sub_queries = self._generate_initial_queries(user_query)
        
        for sub_query_idx, initial_q in enumerate(initial_sub_queries):
            current_sub_query = initial_q
            current_findings_for_sub_query = []
            
            print(f"\n--- Starting research for initial sub-query {sub_query_idx + 1}: '{initial_q}' ---")

            for iteration in range(self.max_depth):
                print(f"\n--- Iteration {iteration + 1} for current sub-query: '{current_sub_query}' ---")
                
                # 1.2.1. Execute Search
                search_results = self._execute_search(current_sub_query)
                
                # 1.2.2. Retrieve & Filter Results (simplified for placeholder)
                # In a real scenario, this would involve more sophisticated parsing and filtering
                
                # 1.2.3. Content Extraction & Summarization
                summary = self._extract_and_summarize_content(search_results, current_sub_query)
                
                # Assuming search_results might contain URLs, for now, we'll use a placeholder source
                # In a real implementation, you'd parse actual URLs from search_results
                current_findings_for_sub_query.append({"query": current_sub_query, "summary": summary, "source": "web_search_result"})
                
                # 1.2.4. Accumulate Findings
                # We extend all_accumulated_findings with the new findings
                all_accumulated_findings.append({"query": current_sub_query, "summary": summary, "source": "web_search_result"})
                
                # 1.2.5. Generate Follow-up Queries
                follow_up_queries = self._generate_follow_up_queries(current_findings_for_sub_query, user_query)
                
                if follow_up_queries and iteration < self.max_depth - 1:
                    current_sub_query = follow_up_queries[0] # Use the first follow-up query for the next iteration
                    print(f"Generated follow-up query: '{current_sub_query}'")
                else:
                    print("No further follow-up queries generated or max depth reached for this sub-query.")
                    break # Exit iteration loop for this sub-query
        
        # 3. Cross-Source Evidence Merging & Refinement
        refined_findings = self._merge_and_refine_findings(all_accumulated_findings)
        
        # 4. Final Report Generation
        final_report = self._generate_final_report(refined_findings, user_query)
        
        print(f"--- DeepSearch completed for query: '{user_query}' ---")
        return final_report


def create_search_agent(llm_type: str = "ollama", search_engine: str = "auto"):
    """Factory function to create a DeepSearch agent."""
    
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
    """Example usage of the DeepSearch agent."""
    # Create agent with default settings
    agent = create_search_agent(llm_type="ollama", search_engine="auto")
    
    # Test queries
    test_queries = [
        "What are the latest advancements in AI?",
        # "Find information about climate change effects", # Commented out for brevity
        # "What's the current weather in San Francisco?" # Commented out for brevity
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        result = agent.deep_search(query) # Call the new deep_search method
        print(f"\nFinal Answer:")
        print(result)
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
