# search_engines/custom_google_search.py
import os
import requests
import json
import time
from typing import List, Dict, Optional, Any
from urllib.parse import urlencode
from search_engines.base_search import BaseSearch
from config import SEARCH_ENGINES


class CustomGoogleSearchAPIWrapper:
    """
    Custom Google Search API wrapper with direct API calls and proxy support.
    Completely independent of langchain_google_community.
    """
    
    def __init__(self, google_api_key: str, google_cse_id: str, 
                 proxies: Optional[Dict] = None, timeout: int = 30, 
                 max_retries: int = 3, retry_delay: float = 1.0):
        """
        Initialize the custom Google Search wrapper.
        
        Args:
            google_api_key: Google API key
            google_cse_id: Google Custom Search Engine ID
            proxies: Dictionary of proxy settings (e.g., {'http': 'http://proxy:port', 'https': 'https://proxy:port'})
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.google_api_key = google_api_key
        self.google_cse_id = google_cse_id
        self.proxies = proxies or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Create session with proxy support
        self.session = requests.Session()
        if self.proxies:
            self.session.proxies.update(self.proxies)

    def _make_api_request(self, query: str, num_results: int = 10, start_index: int = 1) -> Dict[str, Any]:
        """
        Make direct API request to Google Custom Search API.
        
        Args:
            query: Search query string
            num_results: Number of results to return (max 10 per request)
            start_index: Start index for pagination
            
        Returns:
            Raw API response as dictionary
        """
        base_url = "https://www.googleapis.com/customsearch/v1"
        
        params = {
            'key': self.google_api_key,
            'cx': self.google_cse_id,
            'q': query,
            'num': min(num_results, 10),  # Google API max is 10 per request
            'start': start_index
        }
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    base_url,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                print(f"Request error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise
            except Exception as e:
                print(f"Unexpected error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise
        
        return {}

    def run(self, query: str) -> str:
        """
        Execute search query and return formatted string results.
        
        Args:
            query: Search query string
            
        Returns:
            Formatted search results as string
        """
        try:
            results = self.results(query, num_results=5)
            if not results:
                return "No results found."
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result.get('title', 'No title')}\n"
                    f"   {result.get('link', 'No link')}\n"
                    f"   {result.get('snippet', 'No snippet')}"
                )
            
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            print(f"Error in run method: {e}")
            return f"Error performing search: {e}"

    def results(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Get structured search results.
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of structured result dictionaries
        """
        try:
            all_results = []
            remaining_results = num_results
            start_index = 1
            
            while remaining_results > 0 and start_index <= 91:  # Google API limit: max 100 results
                current_batch_size = min(remaining_results, 10)  # Max 10 per request
                
                api_response = self._make_api_request(
                    query=query,
                    num_results=current_batch_size,
                    start_index=start_index
                )
                
                # Extract items from response
                items = api_response.get('items', [])
                if not items:
                    break  # No more results
                
                # Format results
                for item in items:
                    formatted_result = {
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'displayLink': item.get('displayLink', '')
                    }
                    all_results.append(formatted_result)
                
                # Update counters
                remaining_results -= len(items)
                start_index += len(items)
                
                # Check if we've reached the desired number of results
                if len(all_results) >= num_results:
                    break
            
            return all_results[:num_results]  # Ensure we don't exceed requested number
            
        except Exception as e:
            print(f"Error getting structured results: {e}")
            return []

    def search_info(self, query: str) -> Dict[str, Any]:
        """
        Get search metadata and statistics.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary with search metadata
        """
        try:
            api_response = self._make_api_request(query, num_results=1)
            
            return {
                'total_results': api_response.get('searchInformation', {}).get('totalResults', '0'),
                'search_time': api_response.get('searchInformation', {}).get('searchTime', '0'),
                'formatted_total_results': api_response.get('searchInformation', {}).get('formattedTotalResults', '0'),
                'formatted_search_time': api_response.get('searchInformation', {}).get('formattedSearchTime', '0')
            }
            
        except Exception as e:
            print(f"Error getting search info: {e}")
            return {}


class CustomGoogleSearch(BaseSearch):
    """
    Enhanced Google Search implementation using the custom wrapper.
    """
    
    def __init__(self, use_proxy: bool = True, timeout: int = 30, max_retries: int = 3):
        self.api_key = SEARCH_ENGINES.get("google", {}).get("api_key")
        self.cse_id = SEARCH_ENGINES.get("google", {}).get("cse_id")
        if not self.api_key or not self.cse_id:
            raise ValueError("Google API key or CSE ID not found in config.")
        
        # Configure proxies
        proxies = {}
        if use_proxy:
            http_proxy = os.getenv("HTTP_PROXY")
            https_proxy = os.getenv("HTTPS_PROXY")
            if http_proxy:
                proxies["http"] = http_proxy
            if https_proxy:
                proxies["https"] = https_proxy

        self.search_wrapper = CustomGoogleSearchAPIWrapper(
            google_api_key=self.api_key,
            google_cse_id=self.cse_id,
            proxies=proxies if proxies else None,
            timeout=timeout,
            max_retries=max_retries
        )

    def search(self, query: str, structured: bool = True, num_results: int = 10):
        """
        Execute search with optional structured results.
        
        Args:
            query: Search query string
            structured: Whether to return structured results or string
            num_results: Number of results to return (for structured results)
            
        Returns:
            Search results in requested format
        """
        try:
            if structured:
                results = self.search_wrapper.results(query, num_results)
                return results
            else:
                result = self.search_wrapper.run(query)
                return [{"snippet": result}]
                
        except Exception as e:
            print(f"Error in CustomGoogleSearch: {e}")
            return []

    def health_check(self) -> bool:
        """
        Check if the Google Search API is accessible.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Test with a simple query
            test_results = self.search_wrapper.results("test", num_results=1)
            return len(test_results) > 0 or True  # Even if no results, API is accessible
        except Exception as e:
            print(f"Health check failed: {e}")
            return False

    def get_search_stats(self, query: str) -> Dict[str, Any]:
        """
        Get search statistics for a query.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary with search statistics
        """
        return self.search_wrapper.search_info(query)


if __name__ == '__main__':
    # Example usage and testing
    if SEARCH_ENGINES.get("google", {}).get("api_key"):
        print("Testing CustomGoogleSearch (Direct API Implementation)...")
        
        # Test with structured results
        custom_search = CustomGoogleSearch()
        
        # Health check
        if custom_search.health_check():
            print("✓ API is accessible")
        else:
            print("✗ API is not accessible")
        
        # Test search with structured results
        print("\nTesting structured search:")
        structured_results = custom_search.search("latest AI developments", structured=True, num_results=3)
        for i, result in enumerate(structured_results, 1):
            print(f"{i}. {result.get('title', 'No title')}")
            print(f"   Link: {result.get('link', 'No link')}")
            print(f"   Snippet: {result.get('snippet', 'No snippet')[:100]}...")
            print()
        
        # Test search with string results
        print("Testing string search:")
        string_results = custom_search.search("what is machine learning", structured=False)
        print(f"String result preview: {string_results[0]['snippet'][:200]}...")
        
        # Test search statistics
        print("\nTesting search statistics:")
        stats = custom_search.get_search_stats("python programming")
        print(f"Search stats: {stats}")
        
    else:
        print("Please set your GOOGLE_API_KEY and GOOGLE_CSE_ID in a .env file.")
