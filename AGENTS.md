# Agents Documentation

This document provides comprehensive documentation of all agents and components in the Ollama Search Agent system.

## Overview

The Ollama Search Agent system implements a modular agent architecture where different components work together to provide intelligent search capabilities. The system follows a clear separation of concerns with distinct agent types handling different aspects of the search workflow.

## Core Agent Types

### 1. SearchAgent (Primary Orchestrator)

**Location**: `agent.py`

**Purpose**: The main orchestrator agent that coordinates the entire search workflow from query analysis to final answer synthesis.

**Key Responsibilities**:
- Query analysis and search plan generation
- Search execution coordination
- Information synthesis from search results
- Response generation and delivery

**Workflow**:
1. **Planning Phase**: Uses LLM to analyze user query and generate search strategy
2. **Search Phase**: Delegates to search engine with generated plan
3. **Synthesis Phase**: Combines query and results for final LLM processing

**Interface**:
```python
class SearchAgent:
    def __init__(self, llm_client, search_engine):
        self.llm_client = llm_client
        self.search_engine = search_engine

    def run(self, query: str) -> str:
        # Orchestrates the complete search workflow
```

### 2. LLM Agents (Language Model Clients)

These agents handle communication with different language model providers.

#### OllamaClient

**Location**: `llm_clients/ollama_client.py`

**Purpose**: Communicates with local Ollama instances for language model inference.

**Key Features**:
- REST API communication with local Ollama instance
- Support for various Ollama models
- Simple prompt-response interface

**Configuration**:
- `OLLAMA_HOST`: HTTP endpoint (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model name (default: llama3)

**Interface**:
```python
class OllamaClient:
    def generate(self, prompt: str, model: str = None) -> str:
        # Generates response from Ollama model
```

#### OpenAIClient

**Location**: `llm_clients/openai_client.py`

**Purpose**: Communicates with OpenAI-compatible APIs for language model inference.

**Key Features**:
- Modern OpenAI SDK v1.0.0+ compatibility
- Support for any OpenAI-compatible API (OpenRouter, etc.)
- Chat-based completion interface

**Configuration**:
- `OPENAI_API_KEY`: API key for authentication
- `OPENAI_BASE_URL`: API endpoint URL
- `OPENAI_MODEL`: Model identifier

**Interface**:
```python
class OpenAIClient:
    def generate(self, prompt: str, model: str = None) -> str:
        # Generates response from OpenAI-compatible API
```

### 3. Search Engine Agents

These agents handle different search engine integrations, all implementing the `BaseSearch` interface.

#### BaseSearch (Abstract Base Class)

**Location**: `search_engines/base_search.py`

**Purpose**: Defines the common interface for all search engine agents.

**Interface**:
```python
class BaseSearch(ABC):
    @abstractmethod
    def search(self, query: str) -> List[Dict]:
        # Must return structured search results
```

#### PlaceholderSearch

**Location**: `search_engines/placeholder_search.py`

**Purpose**: Mock search engine for development and testing without external dependencies.

**Key Features**:
- Returns predefined mock results
- No API dependencies
- Useful for testing agent workflows

#### GoogleSearch

**Location**: `search_engines/google_search.py`

**Purpose**: Integration with Google Custom Search API.

**Configuration**:
- `GOOGLE_API_KEY`: Google API key
- `GOOGLE_CSE_ID`: Custom Search Engine ID

#### BingSearch

**Location**: `search_engines/bing_search.py`

**Purpose**: Integration with Bing Search API.

**Configuration**:
- `BING_API_KEY`: Bing API key

#### BraveSearch

**Location**: `search_engines/brave_search.py`

**Purpose**: Integration with Brave Search API.

**Configuration**:
- `BRAVE_API_KEY`: Brave API key

#### CustomGoogleSearch

**Location**: `search_engines/custom_google_search.py`

**Purpose**: Alternative Google search implementation with different configuration options.

## Agent Factory System

### SearchEngineFactory

**Location**: `search_engines/factory.py`

**Purpose**: Dynamic agent factory for creating and managing search engine instances.

**Key Features**:
- **Dynamic Discovery**: Automatically discovers all search engines inheriting from `BaseSearch`
- **Dynamic Registration**: Register new engines without modifying existing code
- **Configuration Validation**: Checks engine configuration status
- **Smart Default Selection**: Automatically selects best available search engine
- **Error Handling**: Comprehensive error handling with clear messages

**Factory Methods**:
- `create(engine_name)`: Create specific search engine instance
- `get_default_engine()`: Get best available search engine automatically
- `list_available_engines()`: List all discovered engines
- `is_engine_available(name)`: Check if engine is configured and ready
- `register_engine(name, module, class)`: Register external search engine

**Usage Examples**:
```python
from search_engines import create_search_engine, get_default_search_engine

# Create specific engine
engine = create_search_engine("google")

# Get best available engine automatically
engine = get_default_search_engine()

# List all available engines
engines = list_available_engines()
```

## Agent Configuration

### Configuration Management

**Location**: `config.py`

**Purpose**: Centralized configuration management for all agents.

**Configuration Sections**:
- `OLLAMA_CONFIG`: Local Ollama instance settings
- `OPENAI_API_CONFIG`: OpenAI-compatible API settings
- `SEARCH_ENGINES`: Search engine API configurations

**Environment Variables**:
- API keys and endpoints stored in `.env` file
- Secure management of sensitive data
- Environment-based configuration loading

## Agent Workflow

### Complete Execution Flow

1. **User Input**: CLI command with query and optional parameters
2. **Agent Initialization**:
   - LLM client selected based on `--llm` argument
   - Search engine selected via factory pattern
   - SearchAgent instantiated with configured components
3. **Planning Phase**:
   - Query sent to LLM with planning prompt
   - LLM generates search keywords and sub-questions
   - Search plan returned to agent
4. **Search Phase**:
   - Plan sent to search engine agent
   - Search engine executes API calls
   - Structured results returned
5. **Synthesis Phase**:
   - Original query + search results combined in synthesis prompt
   - LLM generates final comprehensive answer
   - Answer returned through agent chain

### Data Flow

```
User Query → SearchAgent → LLM Agent (Planning) → Search Engine Agent → LLM Agent (Synthesis) → Final Answer
```

## Agent Extensibility

### Adding New LLM Agents

1. **Create Client Class** in `llm_clients/` directory:
   ```python
   class NewProviderClient:
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

### Adding New Search Engine Agents

1. **Create Search Class** in `search_engines/` directory:
   ```python
   class NewSearch(BaseSearch):
       def search(self, query: str) -> List[Dict]:
           # Implement search logic
           return formatted_results
   ```

2. **Update Configuration**:
   - Add search engine config to `config.py`
   - Update `.env.example` with API keys

3. **Automatic Integration**:
   - Factory will automatically discover the new engine
   - No code changes required for integration
   - New engine automatically available via CLI

## Agent Interaction Patterns

### 1. Orchestration Pattern
- `SearchAgent` orchestrates the complete workflow
- Delegates specific tasks to specialized agents
- Maintains workflow state and data flow

### 2. Factory Pattern
- `SearchEngineFactory` creates search engine instances
- Enables dynamic agent discovery and creation
- Supports runtime agent registration

### 3. Strategy Pattern
- Interchangeable LLM clients and search engines
- Consistent interfaces across agent types
- Easy swapping of agent implementations

## Agent Performance & Reliability

### Error Handling
- Graceful degradation when agents fail
- Comprehensive error messages for debugging
- Fallback mechanisms (e.g., placeholder search)

### Configuration Validation
- Automatic validation of agent configuration
- Clear status reporting for agent availability
- Configuration-driven agent selection

### Extensibility
- Plugin-like architecture for new agents
- No hard-coded dependencies between agents
- Runtime agent discovery and registration

## Future Agent Enhancements

### Planned Agent Types
- **Multi-Engine Search Agent**: Coordinate searches across multiple engines simultaneously
- **Result Evaluation Agent**: Assess quality and relevance of search results
- **Caching Agent**: Implement result caching for performance
- **Streaming Agent**: Real-time response generation
- **Multi-modal Agent**: Support for image and document search

### Advanced Agent Capabilities
- **Agent Communication**: Inter-agent messaging and coordination
- **Agent Monitoring**: Performance and health monitoring
- **Agent Scaling**: Distributed agent deployment
- **Agent Learning**: Adaptive behavior based on usage patterns

## Usage Examples

### Basic Agent Usage
```bash
# Default configuration (Ollama + auto-selected search engine)
python main.py "What are the latest AI advancements?"

# Specific LLM agent
python main.py --llm openai "Explain quantum computing"

# Specific search engine agent
python main.py --search-engine google "Python best practices"
```

### Agent Configuration Verification
```bash
# List all available search engine agents
python main.py --list-engines

# Check agent configuration status
python main.py --check-config
```

## Troubleshooting

### Common Agent Issues

**LLM Agent Connection Issues**:
- Verify Ollama is running: `ollama serve`
- Check API keys for OpenAI-compatible services
- Validate configuration in `.env` file

**Search Engine Agent Issues**:
- Verify API keys are configured
- Check internet connectivity
- Validate search engine configuration

**Agent Factory Issues**:
- Ensure new agents inherit from correct base classes
- Verify module imports and naming conventions
- Check factory discovery logs for errors

### Agent Debugging
- Enable verbose logging for agent interactions
- Use placeholder search for testing without external dependencies
- Check agent configuration status via factory methods

---

This documentation provides a comprehensive overview of the agent architecture in the Ollama Search Agent system. The modular design enables easy extension and customization while maintaining a clean separation of concerns between different agent types.
