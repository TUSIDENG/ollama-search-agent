# llm_clients/ollama_client.py
import requests
import json
from config import OLLAMA_CONFIG

class OllamaClient:
    def __init__(self):
        self.host = OLLAMA_CONFIG["host"]
        self.model = OLLAMA_CONFIG["model"]

    def generate(self, prompt: str, model: str = None):
        """
        Generate a response from the Ollama model.
        """
        try:
            url = f"{self.host}/api/generate"
            payload = {
                "model": model if model else self.model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            # Process the response line by line if it's streaming-like
            response_data = response.json()
            return response_data.get("response", "").strip()

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            return None

if __name__ == '__main__':
    # Example usage
    client = OllamaClient()
    prompt = "Why is the sky blue?"
    response = client.generate(prompt)
    if response:
        print("Response from Ollama:")
        print(response)
