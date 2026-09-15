class AgentEvent:
    def __init__(self, eventType, data=None):
        self.eventType = eventType
        self.data = data or {}

    def toDict(self):
        return {
            "type": self.eventType,
            "data": self.data
        }