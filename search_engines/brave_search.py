# search_engines/brave_search.py
import requests
from .base_search import BaseSearch
from config import SEARCH_ENGINES

class BraveSearch(BaseSearch):
    def __init__(self):
        self.api_key = SEARCH_ENGINES.get("brave", {}).get("api_key")
        if not self.api_key:
            raise ValueError("Brave API key not found in config. Please set BRAVE_API_KEY in your .env file.")
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

    def search(self, query: str):
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,
        }
        params = {"q": query}
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            results = response.json()
            
            # Format results to a consistent format
            formatted_results = []
            for item in results.get("web", {}).get("results", []):
                formatted_results.append({
                    "title": item.get("title"),
                    "link": item.get("url"),
                    "snippet": item.get("description"),
                })
            return formatted_results

        except requests.exceptions.RequestException as e:
            print(f"Error calling Brave Search API: {e}")
            return []

if __name__ == '__main__':
    # Example usage
    # Make sure to set your BRAVE_API_KEY in a .env file
    if SEARCH_ENGINES.get("brave", {}).get("api_key"):
        brave_search = BraveSearch()
        search_results = brave_search.search("latest AI advancements")
        for result in search_results:
            print(f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n")
    else:
        print("Please set your BRAVE_API_KEY in a .env file to run this example.")
