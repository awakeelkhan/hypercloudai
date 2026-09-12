class Tool:
    def __init__(self, name, description, inputSchema, execute):
        self.name = name
        self.description = description
        self.inputSchema = inputSchema
        self.execute = execute