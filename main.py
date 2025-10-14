# main.py
import argparse
from agent import SearchAgent
from llm_clients import OllamaClient, OpenAIClient
from search_engines import (
    create_search_engine, 
    get_default_search_engine, 
    list_available_engines,
    check_engine_availability
)
from config import OPENAI_API_CONFIG

def main():
    parser = argparse.ArgumentParser(description="Ollama Search Agent")
    parser.add_argument("--llm", type=str, default="ollama", help="LLM to use (ollama or openai)")
    parser.add_argument("--search-engine", type=str, default="auto", help="Search engine to use (auto, placeholder, brave, google, bing, custom_google). Use 'auto' for automatic selection.")
    parser.add_argument("--list-engines", action="store_true", help="List all available search engines and their status")
    parser.add_argument("query", type=str, nargs="?", default="", help="Search query")
    args = parser.parse_args()

    # List available engines if requested
    if args.list_engines:
        print("Available Search Engines:")
        engines = list_available_engines()
        for engine in engines:
            status = check_engine_availability(engine)
            is_available = all(status.values())
            print(f"  - {engine}: {'✓ Available' if is_available else '✗ Not configured'}")
            if status:
                for key, value in status.items():
                    print(f"    {key}: {'✓' if value else '✗'}")
        return

    # Select LLM client
    if args.llm == "openai":
        if not OPENAI_API_CONFIG["api_key"]:
            print("Please configure your OPENAI_API_KEY in the .env file.")
            return
        llm_client = OpenAIClient()
    else:
        llm_client = OllamaClient()

    # Select search engine using factory
    try:
        if args.search_engine == "auto":
            search_engine = get_default_search_engine()
            print(f"Using default search engine: {type(search_engine).__name__}")
        else:
            search_engine = create_search_engine(args.search_engine)
            print(f"Using search engine: {args.search_engine}")
    except Exception as e:
        print(f"Error creating search engine: {e}")
        print("Available engines:", ", ".join(list_available_engines()))
        return

    agent = SearchAgent(llm_client=llm_client, search_engine=search_engine)

    query = args.query
    if not query:
        query = input("Please enter your search query: ")

    result = agent.run(query)
    
    print("\n--- Final Answer ---")
    print(result)

if __name__ == "__main__":
    main()
