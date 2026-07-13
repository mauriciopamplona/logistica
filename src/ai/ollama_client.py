import os
import requests


class OllamaClient:

    def __init__(self):
        self.url = os.getenv(
            "OLLAMA_URL",
            "http://localhost:11434/api/generate"
        )

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "llama3.2:3b"
        )

    def generate(self, prompt: str):

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        return response.json()["response"]