# langchain_tools/search_tools.py
from typing import Type, Dict, Any, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from search_engines import create_search_engine, get_default_search_engine, list_available_engines


class SearchInput(BaseModel):
    """Input schema for the search tool."""
    query: str = Field(description="The search query to execute")
    engine: str = Field(
        default="auto",
        description="Search engine to use. Use 'auto' for automatic selection, or specify engine name like 'google', 'bing', 'brave'"
    )


class SearchTool(BaseTool):
    """LangChain tool for web search using various search engines."""
    
    name: str = "web_search"
    description: str = (
        "Search the web for information using various search engines. "
        "Use this tool to find current information, facts, news, or any web-based content. "
        "The tool supports multiple search engines including Google, Bing, Brave, and more."
    )
    args_schema: Type[BaseModel] = SearchInput
    default_engine: str = "auto"  # Define as a proper Pydantic field
    
    def __init__(self, default_engine: str = "auto", **kwargs):
        super().__init__(default_engine=default_engine, **kwargs)
        # Store available engines as a class attribute, not instance attribute
        if not hasattr(SearchTool, '_available_engines'):
            SearchTool._available_engines = list_available_engines()
    
    def _run(self, query: str, engine: str = "auto") -> str:
        """Execute a web search and return formatted results."""
        try:
            # If engine is "auto", use the default_engine from instance
            if engine == "auto":
                engine = self.default_engine
            
            # Select search engine
            if engine == "auto":
                search_engine = get_default_search_engine()
                engine_name = "auto-selected"
            else:
                search_engine = create_search_engine(engine)
                engine_name = engine
            
            print(f"--- Searching with {engine_name} engine for: '{query}' ---")
            
            # Execute search
            results = search_engine.search(query)
            
            # Format results for LLM consumption
            formatted_results = self._format_search_results(results, query)
            
            return formatted_results
            
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            print(f"Error: {error_msg}")
            return error_msg
    
    def _format_search_results(self, results: List[Dict[str, Any]], query: str) -> str:
        """Format search results into a readable string for the LLM."""
        if not results:
            return f"No search results found for query: '{query}'"
        
        formatted = f"Found {len(results)} search results for '{query}':\n\n"
        
        for i, result in enumerate(results, 1):
            formatted += f"Result {i}:\n"
            
            if 'title' in result and result['title']:
                formatted += f"  Title: {result['title']}\n"
            
            if 'link' in result and result['link']:
                formatted += f"  URL: {result['link']}\n"
            
            if 'snippet' in result and result['snippet']:
                # Truncate long snippets for readability
                snippet = result['snippet']
                if len(snippet) > 300:
                    snippet = snippet[:300] + "..."
                formatted += f"  Snippet: {snippet}\n"
            
            formatted += "\n"
        
        return formatted
    
    def get_available_engines(self) -> List[str]:
        """Get list of available search engines."""
        return SearchTool._available_engines


# Convenience function to create search tools
def create_search_tool(engine: str = "auto") -> SearchTool:
    """Create a search tool with specified engine."""
    return SearchTool(default_engine=engine)


def get_available_search_tools() -> List[str]:
    """Get list of available search engines for tool creation."""
    return list_available_engines()
