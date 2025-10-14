# search_engines/google_search.py
import os
from langchain_google_community import GoogleSearchAPIWrapper
from search_engines.base_search import BaseSearch
from config import SEARCH_ENGINES

class GoogleSearch(BaseSearch):
    def __init__(self):
        self.api_key = SEARCH_ENGINES.get("google", {}).get("api_key")
        self.cse_id = SEARCH_ENGINES.get("google", {}).get("cse_id")
        if not self.api_key or not self.cse_id:
            raise ValueError("Google API key or CSE ID not found in config.")
        
        # Get proxy settings from environment variables
        http_proxy = os.getenv("HTTP_PROXY")
        https_proxy = os.getenv("HTTPS_PROXY")
        self.proxies = {}
        if http_proxy:
            self.proxies["http"] = http_proxy
        if https_proxy:
            self.proxies["https"] = https_proxy

        self.search_wrapper = GoogleSearchAPIWrapper(
            google_api_key=self.api_key,
            google_cse_id=self.cse_id,
            # The GoogleSearchAPIWrapper in langchain doesn't directly support proxies.
            # We would need to extend it or use a different approach.
            # For now, let's assume a direct connection and document this limitation.
        )

    def search(self, query: str):
        try:
            # The run method returns a string, which we need to parse if we want structured data.
            # For simplicity, we'll return the raw string result.
            results = self.search_wrapper.run(query)
            # Langchain's wrapper returns a string. To maintain consistency, we'll format it.
            return [{"snippet": results}]
        except Exception as e:
            print(f"Error calling Google Search API with LangChain: {e}")
            return []

if __name__ == '__main__':
    # Use absolute import when running as script
    from search_engines.base_search import BaseSearch
    # Example usage
    if SEARCH_ENGINES.get("google", {}).get("api_key"):
        google_search = GoogleSearch()
        search_results = google_search.search("what is langchain")
        print(search_results)
    else:
        print("Please set your GOOGLE_API_KEY and GOOGLE_CSE_ID in a .env file.")
