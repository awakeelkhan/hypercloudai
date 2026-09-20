from src.core.bundle_config import createAgentBundle

class AgentConfig:
    def __init__(self, agent):
        self.agent = agent

    def load(self):
        return createAgentBundle(self.agent)