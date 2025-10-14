# Technical Overview: Ollama Search Agent

## 1. Project Goal & Vision

The primary goal of this project is to create a modular and extensible search agent in Python that leverages Large Language Models (LLMs) to provide intelligent search capabilities. The agent is designed to:

- **Understand complex user queries** through LLM-powered analysis
- **Formulate effective search strategies** by generating relevant keywords and sub-queries
- **Synthesize information** from multiple search results into coherent, comprehensive answers
- **Support multiple LLM providers** including local Ollama models and cloud-based OpenAI-compatible APIs
- **Integrate with various search engines** through a unified interface

## 2. Core Architecture & Design Principles

The architecture follows modern software engineering principles with clear separation of concerns:

- **Modularity**: Each component has a single responsibility and well-defined interface
- **Extensibility**: Easy to add new LLM providers and search engines
- **Configuration Management**: Centralized configuration with environment-based secrets
- **Error Handling**: Graceful degradation and informative error messages
- **Modern Python**: Type hints, docstrings, and contemporary library usage

### Architecture Components

- **Entry Point (`main.py`)**: CLI interface with argument parsing and component orchestration
- **Configuration (`config.py`)**: Centralized settings management with environment variables
- **Agent Core (`agent.py`)**: Search workflow orchestration (Plan → Search → Synthesize)
- **LLM Clients (`llm_clients/`)**: Provider-specific implementations with consistent interface
- **Search Engines (`search_engines/`)**: Search API integrations with abstract base class

## 3. Component Deep Dive

### `main.py` - Command Line Interface
- **Purpose**: User-facing entry point with CLI argument parsing
- **Key Features**:
  - `argparse` for command-line arguments (`--llm`, query input)
  - Dynamic component initialization based on user selection
  - Error handling and user feedback
  - Support for both direct query input and interactive mode

### `agent.py` - Search Agent Core
- **Class**: `SearchAgent`
- **Core Workflow**:
  1. **Plan Generation**: Uses LLM to analyze query and create search strategy
  2. **Search Execution**: Delegates to search engine with generated plan
  3. **Information Synthesis**: Combines query and results for final LLM processing
- **Design Patterns**: Strategy pattern for interchangeable LLM/search components

### `config.py` - Configuration Management
- **Technology**: `python-dotenv` for environment variable loading
- **Structure**:
  - `OLLAMA_CONFIG`: Local Ollama instance settings
  - `OPENAI_API_CONFIG`: OpenAI-compatible API settings
  - `SEARCH_ENGINES`: Search engine API configurations
- **Security**: Sensitive data (API keys) stored in `.env` file, excluded from version control

### LLM Clients (`llm_clients/`)

#### `ollama_client.py`
- **Protocol**: REST API communication with local Ollama instance
- **Endpoint**: `/api/generate` for text generation
- **Dependencies**: `requests` library for HTTP operations
- **Features**: Model selection, streaming support (potential)

#### `openai_client.py` (Updated for v1.0.0+)
- **SDK**: OpenAI Python library v1.0.0+
- **Pattern**: Uses `openai.OpenAI()` client instance
- **Method**: `client.chat.completions.create()` for chat-based completion
- **Compatibility**: Works with any OpenAI-compatible API (OpenRouter, etc.)
- **Response Handling**: Accesses `response.choices[0].message.content`

### Search Engines (`search_engines/`)

#### `base_search.py`
- **Pattern**: Abstract Base Class (ABC) defining interface
- **Method**: Abstract `search(query)` method
- **Purpose**: Ensures consistent interface across all search implementations

#### Implemented Search Engines
- **`placeholder_search.py`**: Mock implementation for development/testing
- **`google_search.py`**: Google Custom Search API integration
- **`bing_search.py`**: Bing Search API integration  
- **`brave_search.py`**: Brave Search API integration
- **`custom_google_search.py`**: Alternative Google search implementation

## 4. Data Flow & Execution Pipeline

### Detailed Execution Flow

1. **User Input**: `python main.py "query" [--llm openai]`
2. **CLI Processing**: `main.py` parses arguments and validates inputs
3. **Component Initialization**:
   - LLM client instantiated based on `--llm` argument (default: OllamaClient)
   - Search engine initialized (currently PlaceholderSearch)
   - SearchAgent created with configured components
4. **Search Workflow**:
   - **Phase 1: Planning**
     - Query sent to LLM with planning prompt
     - LLM generates search keywords/sub-questions
     - Search plan returned to agent
   - **Phase 2: Search Execution**
     - Plan sent to search engine
     - Search engine executes API calls
     - Structured results returned
   - **Phase 3: Synthesis**
     - Original query + search results combined in synthesis prompt
     - LLM generates final comprehensive answer
     - Answer returned through agent to main.py
5. **Output**: Final synthesized answer printed to console

### Data Structures

**Search Results Format**:
```python
[
    {
        "title": "Result Title",
        "link": "https://example.com",
        "snippet": "Brief description..."
    },
    # ... more results
]
```

**LLM Response Format**:
- Planning phase: String of search keywords/questions
- Synthesis phase: Comprehensive answer string

## 5. API Compatibility & Modernization

### OpenAI SDK v1.0.0+ Migration

The project has been updated to use the modern OpenAI Python SDK:

**Before (Legacy)**:
```python
response = openai.Completion.create(
    model="gpt-3.5-turbo",
    prompt=prompt,
    max_tokens=150
)
return response.choices[0].text.strip()
```

**After (Modern)**:
```python
response = self.client.chat.completions.create(
    model=model if model else self.model,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=150
)
return response.choices[0].message.content.strip()
```

### Key Changes
- Use `openai.OpenAI()` client instance instead of global configuration
- Switch from `Completion.create()` to `chat.completions.create()`
- Update response access from `.choices[0].text` to `.choices[0].message.content`
- Support for chat-based models and message history

## 6. Extension Guide

### Adding New LLM Providers

1. **Create Client Class** (`llm_clients/new_provider.py`):
   ```python
   class NewProviderClient:
       def __init__(self):
           # Initialize with config from config.py
           pass
           
       def generate(self, prompt: str) -> str:
           # Implement generation logic
           return generated_text
   ```

2. **Update Configuration**:
   - Add provider config to `config.py`
   - Update `.env.example` with required environment variables

3. **Integrate with CLI**:
   - Add provider option to `main.py` argument parser
   - Update client selection logic

### Adding New Search Engines

1. **Create Search Class** (`search_engines/new_search.py`):
   ```python
   class NewSearch(BaseSearch):
       def search(self, query: str) -> List[Dict]:
           # Implement search logic
           return formatted_results
   ```

2. **Update Configuration**:
   - Add search engine config to `config.py`
   - Update `.env.example` with API keys

3. **Integration**:
   - Update search engine selection in `main.py`
   - Ensure results follow standard format

## 7. Development & Testing

### Development Setup
- Use `.env` for local configuration (excluded via `.gitignore`)
- `placeholder_search.py` for testing without API dependencies
- Comprehensive error handling in all components

### Testing Strategy
- Unit tests for individual components (recommended)
- Integration tests for workflow validation
- Mock implementations for external API testing

## 8. Future Enhancements

### Potential Improvements
- **Streaming Support**: Real-time response generation
- **Caching**: Result caching for performance
- **Multi-modal Search**: Image and document search capabilities
- **Advanced Planning**: Multi-step search strategies
- **Result Evaluation**: Quality assessment of search results
- **Plugin System**: Dynamic component loading

### Scalability Considerations
- Async/await for concurrent operations
- Rate limiting and API quota management
- Distributed search across multiple engines
- Result deduplication and ranking
