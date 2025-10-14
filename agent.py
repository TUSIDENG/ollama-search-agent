# agent.py
from llm_clients import OllamaClient, OpenAIClient
from search_engines import PlaceholderSearch

class SearchAgent:
    def __init__(self, llm_client, search_engine):
        self.llm_client = llm_client
        self.search_engine = search_engine

    def run(self, query: str):
        print(f"--- Running agent for query: '{query}' ---")
        
        # 1. Deconstruct query and form a search plan
        plan_prompt = f"Based on the user query '{query}', create a search plan with a few search keywords."
        plan = self.llm_client.generate(plan_prompt)
        print(f"Search Plan: {plan}")

        # 2. Execute search
        print(f"\n--- Executing Search ---")
        search_results = self.search_engine.search(plan)
        
        # Print detailed search results
        print(f"Found {len(search_results)} search results:")
        for i, result in enumerate(search_results, 1):
            print(f"\nResult {i}:")
            if 'title' in result:
                print(f"  Title: {result['title']}")
            if 'link' in result:
                print(f"  Link: {result['link']}")
            if 'snippet' in result:
                # Truncate long snippets for readability
                snippet = result['snippet']
                if len(snippet) > 200:
                    snippet = snippet[:200] + "..."
                print(f"  Snippet: {snippet}")
        
        # 3. Synthesize results and generate a final answer
        print(f"\n--- Synthesizing Results ---")
        synthesis_prompt = f"Query: {query}\n\nSearch Results:\n{search_results}\n\nSynthesize the information and provide a comprehensive answer."
        final_answer = self.llm_client.generate(synthesis_prompt)
        
        return final_answer

def main():
    # Example usage with Ollama and PlaceholderSearch
    ollama_client = OllamaClient()
    search_engine = PlaceholderSearch()
    agent = SearchAgent(llm_client=ollama_client, search_engine=search_engine)
    
    query = "What are the latest advancements in AI?"
    result = agent.run(query)
    
    print("\n--- Final Answer ---")
    print(result)

if __name__ == "__main__":
    main()
