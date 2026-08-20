class Thread:
    def __init__(self):
        self.messages = []
        self.toolCalls = []
        self.toolResults = []

    def addMessage(self, message):
        self.messages.append(message)

    def addToolCall(self, toolCall):
        self.toolCalls.append(toolCall)

    def addToolResult(self, toolResult):
        self.toolResults.append(toolResult)

    def getMessages(self):
        return self.messages

    def getToolCalls(self):
        return self.toolCalls

    def getToolResults(self):
        return self.toolResults