from groq import Groq
from src.models.model_adapter import ModelAdapter

class GroqAdapter(ModelAdapter):

    def __init__(self, apiKey=None, modelName=None):
        if apiKey:
            self.client = Groq(api_key=apiKey)
        else:
            self.client = Groq()

        self.modelName = modelName or "openai/gpt-oss-20b"

    def generate(self, messages, tools=None):
        return self.client.chat.completions.create(
            model=self.modelName,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )