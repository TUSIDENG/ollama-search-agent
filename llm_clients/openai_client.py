# llm_clients/openai_client.py
import openai
from config import OPENAI_API_CONFIG

class OpenAIClient:
    def __init__(self):
        self.api_key = OPENAI_API_CONFIG["api_key"]
        self.base_url = OPENAI_API_CONFIG["base_url"]
        self.model = OPENAI_API_CONFIG["model"]
        
        # Initialize OpenAI client with new API
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def generate(self, prompt: str, model: str = None):
        """
        Generate a response from an OpenAI-compatible model.
        """
        try:
            response = self.client.chat.completions.create(
                model=model if model else self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error connecting to OpenAI API: {e}")
            return None

if __name__ == '__main__':
    # Example usage
    # Make sure to set your API key in config.py
    if OPENAI_API_CONFIG["api_key"] != "YOUR_OPENAI_API_KEY":
        client = OpenAIClient()
        prompt = "Explain the theory of relativity in simple terms."
        response = client.generate(prompt)
        if response:
            print("Response from OpenAI-compatible API:")
            print(response)
    else:
        print("Please configure your OpenAI API key in config.py")
