from groq import Groq

from skill_registry import SkillRegistry
from filesystem_skill import filesystemSkill
from thread import Thread

import json


client = Groq()

skillRegistry = SkillRegistry()
skillRegistry.register(filesystemSkill)


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
        tool = skill.getTool(toolName)

        if tool:
            return tool

    return None


def log(message):
    print(f"[LOG] {message}")


def askAgent(thread):
    while True:
        log("Sending request to model")

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=thread.getMessages(),
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:

            for call in message.tool_calls:

                toolName = call.function.name

                log(f"Tool requested: {toolName}")

                tool = findTool(toolName)

                if not tool:
                    log(f"Tool not found: {toolName}")
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

                log(f"Tool result: {results}")

                toolCall = {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": toolName,
                        "arguments": call.function.arguments
                    }
                }

                thread.addToolCall(toolCall)

                thread.addMessage(
                    "assistant",
                    None,
                    tool_calls=[toolCall]
                )

                thread.addToolResult(results)

                thread.addMessage(
                    "tool",
                    str(results),
                    tool_call_id=call.id
                )

            continue

        log("Model returned final response")

        thread.addMessage(
            "assistant",
            message.content
        )

        return message.content


print("HyperCloudAI Agent")
print("Type 'exit' to quit.\n")

thread = Thread()

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    thread.addMessage(
        "user",
        question
    )

    answer = askAgent(thread)

    print("AI:", answer)