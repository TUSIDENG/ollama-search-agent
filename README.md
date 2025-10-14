# Ollama Search Agent

This project is a Python-based search agent that integrates with local Ollama models and OpenAI-compatible APIs to provide intelligent search capabilities.

## Features

- **Modular Design**: Easily switch between different LLMs (Ollama, OpenAI) and search engines.
- **Extensible**: Designed to be easily extended with new search engines and functionalities.
- **Configurable**: All settings are managed in a central `config.py` file.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ollama-search-agent
    ```

2.  **Install dependencies:**

    You can use either `pip` or `uv`. `uv` is a very fast Python package installer and resolver, written in Rust.

    **Using `pip`:**
    ```bash
    pip install -r requirements.txt
    ```

    **Using `uv`:**
    ```bash
    uv pip install -r requirements.txt
    ```

3.  **Configure the agent:**
    - Create a `.env` file by copying the `.env.example` file:
      ```bash
      cp .env.example .env
      ```
    - Open the `.env` file and add your API keys and other configurations.

## Usage

You can run the agent from the command line.

### Basic Usage

To run with the default settings (Ollama):
```bash
python main.py "your search query"
```

If you don't provide a query, the agent will prompt you for one:
```bash
python main.py
```

### Using a different LLM

To use an OpenAI-compatible model:
```bash
python main.py --llm openai "your search query"
```

## Project Structure

```
.
├── agent.py                  # Core agent logic
├── config.py                 # Configuration for LLMs and search engines
├── llm_clients/              # Modules for interacting with LLMs
│   ├── __init__.py
│   ├── ollama_client.py
│   └── openai_client.py
├── main.py                   # Main entry point
├── README.md                 # This file
├── requirements.txt          # Project dependencies
└── search_engines/           # Modules for search engines
    ├── __init__.py
    ├── base_search.py
    └── placeholder_search.py
