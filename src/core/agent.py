from src.models.model_adapter import ModelAdapter
from src.models.groq_adapter import GroqAdapter
from src.skills.skill_registry import SkillRegistry
from src.skills.filesystem_skill import filesystemSkill
from src.state.thread import Thread
from src.core.events import AgentEvent
from src.core.event_stream import EventStream
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


def emitEvent(eventStream, eventType, data=None):
    if eventStream:
        eventStream.emit(
            AgentEvent(
                eventType,
                data
            )
        )
def askAgent(thread, eventStream=None):
    emitEvent(
        eventStream,
        "run_started"
    )

    while True:

        log(
            "Sending request to model"
        )

        response = model.stream(
            messages=thread.getMessages(),
            tools=tools
        )

        content = ""
        toolCalls = {}

        for chunk in response:
            delta = chunk.choices[0].delta

            if delta.content:
                content += delta.content

                emitEvent(
                    eventStream,
                    "token",
                    {"content": delta.content}
                )

            if delta.tool_calls:
                for toolCall in delta.tool_calls:
                    index = toolCall.index

                    if index not in toolCalls:
                        toolCalls[index] = {
                            "id": "",
                            "type": "function",
                            "function": {
                                "name": "",
                                "arguments": ""
                            }
                        }

                    currentCall = toolCalls[index]

                    if toolCall.id:
                        currentCall["id"] = toolCall.id

                    if toolCall.function:

                        if toolCall.function.name:
                            currentCall["function"]["name"] += toolCall.function.name

                        if toolCall.function.arguments:
                            currentCall["function"]["arguments"] += toolCall.function.arguments

        if toolCalls:

            for call in toolCalls.values():

                toolName = call["function"]["name"]

                emitEvent(
                    eventStream,
                    "tool_called",
                    {
                        "name": toolName,
                        "arguments": call["function"]["arguments"]
                    }
                )

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

                    emitEvent(
                        eventStream,
                        "tool_result",
                        {
                            "name": toolName,
                            "result": "Tool not found"
                        }
                    )

                    continue

                arguments = json.loads(
                    call["function"]["arguments"]
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

                emitEvent(
                    eventStream,
                    "tool_result",
                    {
                        "name": toolName,
                        "result": results
                    }
                )

                thread.addToolCall(
                    call
                )

                thread.addMessage(
                    "assistant",
                    None,
                    tool_calls=[call]
                )

                thread.addToolResult(
                    results
                )

                thread.addMessage(
                    "tool",
                    str(results),
                    tool_call_id=call["id"]
                )

            continue

        log(
            "Model returned final response"
        )

        thread.addMessage(
            "assistant",
            content
        )

        emitEvent(
            eventStream,
            "run_completed",
            {"content": content}
        )

        return content


def runCli():
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
        eventStream = EventStream()
        answer = askAgent(
            thread,
            eventStream
        )
        print(
            "AI:",
            answer
        )
if __name__ == "__main__":
    runCli()