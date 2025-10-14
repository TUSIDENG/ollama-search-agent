# search_engines/bing_search.py
from langchain_community.utilities import BingSearchAPIWrapper
from .base_search import BaseSearch
from config import SEARCH_ENGINES

class BingSearch(BaseSearch):
    def __init__(self):
        self.api_key = SEARCH_ENGINES.get("bing", {}).get("api_key")
        if not self.api_key:
            raise ValueError("Bing API key not found in config.")
        
        self.search_wrapper = BingSearchAPIWrapper(
            bing_subscription_key=self.api_key
        )

    def search(self, query: str):
        try:
            results = self.search_wrapper.run(query)
            return [{"snippet": results}]
        except Exception as e:
            print(f"Error calling Bing Search API with LangChain: {e}")
            return []

if __name__ == '__main__':
    # Example usage
    if SEARCH_ENGINES.get("bing", {}).get("api_key"):
        bing_search = BingSearch()
        search_results = bing_search.search("what is langchain")
        print(search_results)
    else:
        print("Please set your BING_API_KEY in a .env file.")
