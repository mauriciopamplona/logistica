from ai.ollama_client import OllamaClient
from ai.prompts import ROUTER_PROMPT


class FleetAgent:

    def __init__(self):
        self.client = OllamaClient()

    def route(self, question: str) -> str:

        prompt = ROUTER_PROMPT.format(
            question=question
        )

        response = self.client.generate(prompt)

        return response.strip().splitlines()[0].lower()