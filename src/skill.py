class Skill:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.tools = []

    def addTool(self, tool):
        self.tools.append(tool)

    def getTool(self, name):
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None

    def getTools(self):
        return self.tools