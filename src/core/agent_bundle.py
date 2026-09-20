class AgentBundle:
    def __init__(self, agent, skills, tools, mcpServers):
        self.agent = agent
        self.skills = skills
        self.tools = tools
        self.mcpServers = mcpServers

    def getAgent(self):
        return self.agent

    def getSkills(self):
        return self.skills

    def getTools(self):
        return self.tools

    def getMcpServers(self):
        return self.mcpServers