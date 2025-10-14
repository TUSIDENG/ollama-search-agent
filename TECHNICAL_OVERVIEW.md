# Technical Overview: Ollama Search Agent

## 1. Project Goal

The primary goal of this project is to create a modular and extensible search agent in Python. It leverages Large Language Models (LLMs) to understand user queries, formulate search plans, and synthesize information from search results into a coherent answer. The agent is designed to support both local LLMs via Ollama and cloud-based models through any OpenAI-compatible API.

## 2. Core Architecture

The architecture is designed to be modular, separating concerns into distinct components:

-   **Entry Point (`main.py`)**: Handles command-line argument parsing, initializes the necessary components, and orchestrates the overall execution.
-   **Configuration (`config.py`)**: Centralizes all external configurations, such as API keys, model names, and service endpoints. It uses `.env` files for secure management of secrets.
-   **Agent (`agent.py`)**: The core logic unit that coordinates the workflow. It takes a user query and uses the LLM and search engine to produce a final answer.
-   **LLM Clients (`llm_clients/`)**: A collection of clients for interacting with different LLM providers. Each client implements a consistent interface (`generate` method).
-   **Search Engines (`search_engines/`)**: A collection of clients for different search APIs. They share a common interface (`search` method).

## 3. Component Breakdown

### `main.py`
-   **Purpose**: User-facing entry point.
-   **Functionality**:
    -   Uses `argparse` to handle command-line arguments (`--llm` for model selection, `query` for the search term).
    -   Instantiates the appropriate LLM client (`OllamaClient` or `OpenAIClient`) based on user input.
    -   Instantiates the search engine (currently `PlaceholderSearch`).
    -   Initializes the `SearchAgent` with the selected clients.
    -   Calls the agent's `run` method and prints the final result.

### `agent.py`
-   **Purpose**: Contains the main orchestration logic for the search process.
-   **Class**: `SearchAgent`
-   **Execution Flow**:
    1.  **Plan**: The `run` method first sends the user query to the LLM to generate a "search plan" (a set of relevant keywords or sub-questions). This step helps focus the search.
    2.  **Search**: The generated plan is passed to the search engine client, which executes the search and returns a list of results.
    3.  **Synthesize**: The original query and the search results are combined into a new prompt. This prompt is sent to the LLM to generate a comprehensive, synthesized answer based on the retrieved information.

### `config.py`
-   **Purpose**: Manage all configurations.
-   **Functionality**:
    -   Uses `python-dotenv` to load environment variables from a `.env` file.
    -   Defines dictionary-based configurations (`OLLAMA_CONFIG`, `OPENAI_API_CONFIG`, `SEARCH_ENGINES`).
    -   Provides default values for non-sensitive settings (e.g., Ollama host) while retrieving sensitive data (API keys) from the environment.

### `llm_clients/`
-   **`ollama_client.py`**:
    -   Communicates with a local Ollama instance via its REST API.
    -   Uses the `requests` library to POST to the `/api/generate` endpoint.
-   **`openai_client.py`**:
    -   Interacts with any OpenAI-compatible API.
    -   Uses the `openai` Python library.
    -   Configures the `api_key` and `api_base` from `config.py`.

### `search_engines/`
-   **`base_search.py`**: Defines the abstract base class `BaseSearch` with an abstract `search` method, ensuring a consistent interface for all search engine clients.
-   **`placeholder_search.py`**: A dummy implementation for development and testing. It returns a fixed set of mock search results.

## 4. Data Flow & Execution

1.  User runs `python main.py "some query"`.
2.  `main.py` parses the arguments and initializes `OllamaClient` (default) and `PlaceholderSearch`.
3.  `main.py` creates a `SearchAgent` instance with these clients.
4.  `agent.run()` is called.
5.  `SearchAgent` sends a prompt to `OllamaClient` to create a search plan.
6.  `OllamaClient` makes an HTTP request to the Ollama server and returns the plan.
7.  `SearchAgent` calls `PlaceholderSearch.search()` with the plan.
8.  `PlaceholderSearch` returns mock results.
9.  `SearchAgent` sends a final prompt (query + results) to `OllamaClient` for synthesis.
10. `OllamaClient` gets the final answer from the Ollama server.
11. The final answer is returned to `main.py` and printed to the console.

## 5. How to Extend

-   **To add a new LLM**:
    1.  Create a new client class in `llm_clients/` (e.g., `anthropic_client.py`).
    2.  Implement the `generate(self, prompt: str)` method.
    3.  Add the configuration to `config.py` and `.env.example`.
    4.  Update `main.py` to allow selecting the new client via a command-line argument.
-   **To add a new Search Engine**:
    1.  Create a new class in `search_engines/` (e.g., `google_search.py`) that inherits from `BaseSearch`.
    2.  Implement the `search(self, query: str)` method, which should call the actual search engine API and return a list of dictionaries (with keys like `title`, `link`, `snippet`).
    3.  Add API key configurations to `config.py` and `.env.example`.
    4.  Update `main.py` to allow selecting the new search engine.
