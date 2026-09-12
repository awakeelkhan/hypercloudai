from src.models.model_adapter import ModelAdapter
from src.models.groq_adapter import GroqAdapter

from src.skills.skill_registry import SkillRegistry
from src.skills.filesystem_skill import filesystemSkill

from src.state.thread import Thread
from src.config import Config

import json


config = Config()

model: ModelAdapter = GroqAdapter(
    apiKey=config.groqApiKey,
    modelName=config.modelName
)


skillRegistry = SkillRegistry()

skillRegistry.register(
    filesystemSkill
)


tools = [
    {
        "type": "function",
        "function": {
            "name": "searchProject",
            "description": "Search the HyperCloudAI project files for a keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The keyword to search for."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listDirectory",
            "description": "List the files inside the src directory.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


def findTool(toolName):
    for skill in skillRegistry.getAll():

        tool = skill.getTool(
            toolName
        )

        if tool:
            return tool

    return None


def log(message):
    print(
        f"[LOG] {message}"
    )


def askAgent(thread):

    while True:

        log(
            "Sending request to model"
        )

        response = model.generate(
            messages=thread.getMessages(),
            tools=tools
        )

        message = response.choices[0].message

        if message.tool_calls:

            for call in message.tool_calls:

                toolName = call.function.name

                log(
                    f"Tool requested: {toolName}"
                )

                tool = findTool(
                    toolName
                )

                if not tool:

                    log(
                        f"Tool not found: {toolName}"
                    )

                    continue

                arguments = json.loads(
                    call.function.arguments
                )

                if toolName == "searchProject":

                    results = tool.execute(
                        arguments["query"]
                    )

                else:

                    results = tool.execute()

                log(
                    f"Tool result: {results}"
                )

                toolCall = {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": toolName,
                        "arguments": call.function.arguments
                    }
                }

                thread.addToolCall(
                    toolCall
                )

                thread.addMessage(
                    "assistant",
                    None,
                    tool_calls=[toolCall]
                )

                thread.addToolResult(
                    results
                )

                thread.addMessage(
                    "tool",
                    str(results),
                    tool_call_id=call.id
                )

            continue

        log(
            "Model returned final response"
        )

        thread.addMessage(
            "assistant",
            message.content
        )

        return message.content


print(
    "HyperCloudAI Agent"
)

print(
    "Type 'exit' to quit.\n"
)


thread = Thread()


while True:

    question = input(
        "You: "
    )

    if question.lower() == "exit":

        break

    thread.addMessage(
        "user",
        question
    )

    answer = askAgent(
        thread
    )

    print(
        "AI:",
        answer
    )