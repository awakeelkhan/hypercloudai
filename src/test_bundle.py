from src.core.agent import askAgent
from src.core.agent_config import AgentConfig


config = AgentConfig(askAgent)
bundle = config.load()

print("Agent Bundle Loaded")
print("Skills:", len(bundle.getSkills()))
print("Tools:", len(bundle.getTools()))
print("MCP Servers:", bundle.getMcpServers())