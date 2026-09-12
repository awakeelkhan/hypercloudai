class Skill:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.tools = {}

    def addTool(self, tool):
        self.tools[tool.name] = tool

    def getTool(self, toolName):
        return self.tools.get(toolName)

    def getTools(self):
        return self.tools.values()