class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def get(self, toolName):
        return self.tools.get(toolName)

    def getAll(self):
        return self.tools.values()