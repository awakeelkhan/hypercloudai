class Thread:
    def __init__(self):
        self.messages = []
        self.toolCalls = []
        self.toolResults = []

    def addMessage(
        self,
        role,
        content,
        tool_calls=None,
        tool_call_id=None
    ):
        message = {
            "role": role,
            "content": content
        }

        if tool_calls is not None:
            message["tool_calls"] = tool_calls

        if tool_call_id is not None:
            message["tool_call_id"] = tool_call_id

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