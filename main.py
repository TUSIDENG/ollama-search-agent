# main.py - LangChain Optimized Version
import argparse
from agent import create_search_agent
from search_engines import (
    list_available_engines,
    check_engine_availability
)
from config import OPENAI_API_CONFIG

def main():
    parser = argparse.ArgumentParser(description="Ollama Search Agent - LangChain Optimized")
    parser.add_argument("--llm", type=str, default="openai", help="LLM to use (ollama or openai)")
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

    # Validate OpenAI configuration if selected
    if args.llm == "openai" and not OPENAI_API_CONFIG["api_key"]:
        print("Please configure your OPENAI_API_KEY in the .env file.")
        return

    # Create LangChain search agent
    try:
        agent = create_search_agent(llm_type=args.llm, search_engine=args.search_engine)
        print(f"Created LangChain agent with {args.llm} LLM and {args.search_engine} search engine")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error creating agent: {e}")
        print("Available engines:", ", ".join(list_available_engines()))
        return

    # Get query from user
    query = args.query
    if not query:
        query = input("Please enter your search query: ")

    # Execute agent
    result = agent.deep_search(query)
    
    print("\n--- Final Answer ---")
    print(result)

if __name__ == "__main__":
    main()
