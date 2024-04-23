import openai
import os

OPENAI_KEY = os.environ["OPENAI_KEY"]

openai.api_key = OPENAI_KEY
openai.base_url = "https://api.totalgpt.ai/v1"
class Conversation:
    model: str = "WizardLM-2-8x22B"

    def __init__(self) -> None:
        self.messages: list[dict] = []

    async def send(self, message: str) -> list[str]:
        self.messages.append({"role": "user", "content": message})
        r = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=self.messages,
        )
        return [choice["message"]["content"] for choice in r["choices"]]

    def pick_response(self, choice: str) -> None:
        self.messages.append({"role": "assistant", "content": choice})

    def clear(self) -> None:
        self.messages = []