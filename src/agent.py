from google import genai
from google.genai import types

from skill_registry import SkillRegistry
from filesystem_skill import filesystemSkill
from thread import Thread


client = genai.Client()

skillRegistry = SkillRegistry()
skillRegistry.register(filesystemSkill)


geminiTool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="searchProject",
            description="Search the HyperCloudAI project files for a keyword.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "query": types.Schema(
                        type="STRING",
                        description="The keyword to search for."
                    )
                },
                required=["query"],
            ),
        )
    ]
)


def findTool(toolName):
    for skill in skillRegistry.getAll():
        tool = skill.getTool(toolName)

        if tool:
            return tool

    return None


def askAgent(thread):
    while True:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=thread.getMessages(),
            config=types.GenerateContentConfig(
                tools=[geminiTool]
            ),
        )

        if response.function_calls:
            call = response.function_calls[0]

            print("Tool requested:", call.name)

            tool = findTool(call.name)

            if tool:
                results = tool.execute(
                    call.args["query"]
                )

                print("Tool result:", results)

                thread.addMessage(
                    "user",
                    f"Tool {call.name} returned: {results}"
                )

                continue

        thread.addMessage(
            "model",
            response.text
        )

        return response.text


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