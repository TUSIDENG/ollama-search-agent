# Ollama Search Agent

A modular Python-based search agent that leverages Large Language Models (LLMs) to provide intelligent search capabilities. The agent can use both local Ollama models and OpenAI-compatible APIs to understand queries, formulate search plans, and synthesize information from search results.

## 🚀 Features

- **Multi-LLM Support**: Seamlessly switch between Ollama (local) and OpenAI-compatible APIs
- **Modular Architecture**: Clean separation between LLM clients, search engines, and core logic
- **Extensible Design**: Easy to add new LLM providers and search engines
- **Environment-based Configuration**: Secure management of API keys and settings
- **Modern Python**: Uses OpenAI SDK v1.0.0+ and best practices

## 🔮 Planned Features

### Search Engine Abstraction Factory
- **Abstract Factory Pattern**: Implement a factory pattern to encapsulate search engine creation
- **Unified Interface**: Standardized creation and configuration of search engines
- **Dynamic Engine Selection**: Runtime selection and instantiation of search engines

### Advanced Search Customization
- **Multi-Engine Search**: Support simultaneous searches across multiple search engines
- **Customizable Results**: Configurable minimum result count per search engine
- **Result Aggregation**: Intelligent merging and deduplication of results from multiple sources
- **Performance Optimization**: Parallel search execution with configurable timeouts

## 📋 Prerequisites

- Python 3.8+
- Ollama (optional, for local models)
- API keys for desired services (OpenAI, Google, Bing, etc.)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ollama-search-agent
```

### 2. Install Dependencies

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using uv (recommended for speed):**
```bash
uv pip install -r requirements.txt
```

### 3. Configure Environment

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` file with your API keys and settings:
```env
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4

# Search Engine API Keys
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
BING_API_KEY=your_bing_api_key
BRAVE_API_KEY=your_brave_api_key
```

## 🎯 Usage

### Basic Usage with Ollama (Default)
```bash
python main.py "your search query"
```

### Using OpenAI Models
```bash
python main.py --llm openai "your search query"
```

### Interactive Mode
```bash
python main.py
# Then enter your query when prompted
```

## 🏗️ Project Architecture

```
ollama-search-agent/
├── agent.py                  # Core agent orchestration logic
├── config.py                 # Centralized configuration management
├── main.py                   # CLI entry point and argument parsing
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
├── TECHNICAL_OVERVIEW.md    # Detailed technical documentation
├── llm_clients/             # LLM provider implementations
│   ├── __init__.py
│   ├── ollama_client.py     # Ollama local model client
│   └── openai_client.py     # OpenAI-compatible API client
└── search_engines/          # Search engine implementations
    ├── __init__.py
    ├── base_search.py       # Abstract base class for search engines
    ├── placeholder_search.py # Mock search for development
    ├── google_search.py     # Google Custom Search API
    ├── bing_search.py       # Bing Search API
    ├── brave_search.py      # Brave Search API
    └── custom_google_search.py # Alternative Google search
```

## 🔧 Core Components

### SearchAgent (`agent.py`)
- Orchestrates the search workflow: Plan → Search → Synthesize
- Uses LLM to generate search plans from user queries
- Combines search results with original query for final synthesis

### LLM Clients (`llm_clients/`)
- **OllamaClient**: Communicates with local Ollama instance via REST API
- **OpenAIClient**: Uses OpenAI SDK v1.0.0+ for OpenAI-compatible APIs
- Both implement consistent `generate(prompt)` interface

### Search Engines (`search_engines/`)
- **BaseSearch**: Abstract class defining search engine interface
- **PlaceholderSearch**: Mock implementation for testing
- **GoogleSearch**: Google Custom Search API integration
- **BingSearch**: Bing Search API integration
- **BraveSearch**: Brave Search API integration

## 🔄 Workflow

1. **Query Analysis**: LLM analyzes user query and generates search plan
2. **Search Execution**: Search engine executes plan and retrieves results
3. **Information Synthesis**: LLM synthesizes search results into coherent answer
4. **Response Delivery**: Final answer returned to user

## 🚀 Extending the Project

### Adding a New LLM Provider
1. Create new client in `llm_clients/` (e.g., `anthropic_client.py`)
2. Implement `generate(prompt)` method
3. Add configuration to `config.py` and `.env.example`
4. Update CLI arguments in `main.py`

### Adding a New Search Engine
1. Create new class in `search_engines/` inheriting from `BaseSearch`
2. Implement `search(query)` method returning structured results
3. Add API configuration to `config.py` and `.env.example`
4. Update CLI arguments in `main.py`

## 🐛 Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'openai'**
```bash
pip install -r requirements.txt
```

**OpenAI API Compatibility Issues**
- The project uses OpenAI SDK v1.0.0+ with modern API patterns
- Legacy `openai.Completion` calls have been updated to `client.chat.completions.create()`

**Ollama Connection Issues**
- Ensure Ollama is running: `ollama serve`
- Verify OLLAMA_HOST in `.env` matches your Ollama instance

## 📚 Documentation

- **[TECHNICAL_OVERVIEW.md](TECHNICAL_OVERVIEW.md)**: Detailed technical architecture and component breakdown
- Code is well-documented with docstrings and type hints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license here]
