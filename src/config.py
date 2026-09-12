import os

class Config:
    def __init__(self):
        self.groqApiKey = os.getenv("GROQ_API_KEY")
        self.modelName = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )