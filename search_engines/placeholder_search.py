# search_engines/placeholder_search.py
from .base_search import BaseSearch

class PlaceholderSearch(BaseSearch):
    def search(self, query: str):
        print(f"--- Searching with Placeholder for query: '{query}' ---")
        return [
            {
                "title": "Placeholder Result 1",
                "link": "http://example.com/1",
                "snippet": f"This is a placeholder snippet for the query '{query}'."
            },
            {
                "title": "Placeholder Result 2",
                "link": "http://example.com/2",
                "snippet": f"Another placeholder snippet for '{query}'."
            }
        ]
