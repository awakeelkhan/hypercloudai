class AgentBundle:
    def __init__(self, agent, skills, tools, mcpServers, permissions=None):
        self.agent = agent
        self.skills = skills
        self.tools = tools
        self.mcpServers = mcpServers
        self.permissions = permissions

    def getAgent(self):
        return self.agent

    def getSkills(self):
        return self.skills

    def getTools(self):
        return self.tools

    def getMcpServers(self):
        return self.mcpServers

    def getPermissions(self):
        return self.permissions