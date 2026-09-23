class ToolPermissions:
    def __init__(self, allowedTools=None, deniedTools=None, readOnlyTools=None, actionTools=None):
        self.allowedTools = allowedTools or []
        self.deniedTools = deniedTools or []
        self.readOnlyTools = readOnlyTools or []
        self.actionTools = actionTools or []

    def isAllowed(self, toolName):
        if toolName in self.deniedTools:
            return False

        if self.allowedTools and toolName not in self.allowedTools:
            return False

        return True

    def isReadOnly(self, toolName):
        return toolName in self.readOnlyTools

    def isAction(self, toolName):
        return toolName in self.actionTools

    def needsApproval(self, toolName):
        return self.isAction(toolName) and self.isAllowed(toolName)

    def approve(self, toolName):
        if self.needsApproval(toolName):
            print("Approval required for:", toolName)
            answer = input("Allow this action? (y/n): ")
            return answer.lower() == "y"

        return self.isAllowed(toolName)