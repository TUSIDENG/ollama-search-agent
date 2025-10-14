# main.py
import argparse
from agent import SearchAgent
from llm_clients import OllamaClient, OpenAIClient
from search_engines import PlaceholderSearch, BraveSearch, GoogleSearch, BingSearch,CustomGoogleSearch
from config import OPENAI_API_CONFIG, SEARCH_ENGINES

def main():
    parser = argparse.ArgumentParser(description="Ollama Search Agent")
    parser.add_argument("--llm", type=str, default="ollama", help="LLM to use (ollama or openai)")
    parser.add_argument("--search-engine", type=str, default="google", help="Search engine to use (placeholder, brave, google, or bing)")
    parser.add_argument("query", type=str, nargs="?", default="", help="Search query")
    args = parser.parse_args()

    # Select LLM client
    if args.llm == "openai":
        if not OPENAI_API_CONFIG["api_key"]:
            print("Please configure your OPENAI_API_KEY in the .env file.")
            return
        llm_client = OpenAIClient()
    else:
        llm_client = OllamaClient()

    # Select search engine
    if args.search_engine == "brave":
        if not SEARCH_ENGINES.get("brave", {}).get("api_key"):
            print("Please configure your BRAVE_API_KEY in the .env file.")
            return
        search_engine = BraveSearch()
    elif args.search_engine == "google":
        if not SEARCH_ENGINES.get("google", {}).get("api_key") or not SEARCH_ENGINES.get("google", {}).get("cse_id"):
            print("Please configure your GOOGLE_API_KEY and GOOGLE_CSE_ID in the .env file.")
            return
        search_engine = CustomGoogleSearch()
    elif args.search_engine == "bing":
        if not SEARCH_ENGINES.get("bing", {}).get("api_key"):
            print("Please configure your BING_API_KEY in the .env file.")
            return
        search_engine = BingSearch()
    else:
        search_engine = PlaceholderSearch()

    agent = SearchAgent(llm_client=llm_client, search_engine=search_engine)

    query = args.query
    if not query:
        query = input("Please enter your search query: ")

    result = agent.run(query)
    
    print("\n--- Final Answer ---")
    print(result)

if __name__ == "__main__":
    main()
