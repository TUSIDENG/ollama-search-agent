# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Ollama configuration
OLLAMA_CONFIG = {
    "host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    "model": os.getenv("OLLAMA_MODEL", "llama3")
}

# OpenAI-compatible API configuration
OPENAI_API_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "model": os.getenv("OPENAI_MODEL", "gpt-4")
}

# Search engine configurations (placeholders)
SEARCH_ENGINES = {
    "google": {
        "api_key": os.getenv("GOOGLE_API_KEY"),
        "cse_id": os.getenv("GOOGLE_CSE_ID")
    },
    "bing": {
        "api_key": os.getenv("BING_API_KEY")
    },
    "yandex": {
        "api_key": os.getenv("YANDEX_API_KEY")
    },
    "baidu": {
        "api_key": os.getenv("BAIDU_API_KEY")
    },
    "brave": {
        "api_key": os.getenv("BRAVE_API_KEY")
    }
}
