from google import genai
from google.genai import types
from search_tool import searchTool
from tool_registry import ToolRegistry

client = genai.Client()
registry = ToolRegistry()
registry.register(searchTool)

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

def askAgent(question):
    messages = [question]
    while True:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[geminiTool]
            ),
        )

        if response.function_calls:
            call = response.function_calls[0]
            tool = registry.get(call.name)

            if tool:
                results = tool.execute(call.args["query"])
                messages.append(
                    f"Tool {call.name} returned: {results}"
                )
                continue
            messages.append(
                f"The tool '{call.name}' is not available. "
                "Answer the user's question without using a tool."
            )
            continue
        return response.text

print("HyperCloudAI Agent")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break
    answer = askAgent(question)
    print("AI:", answer)