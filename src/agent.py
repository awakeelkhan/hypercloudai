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
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[geminiTool]
        ),
    )

    if response.function_calls:
        call = response.function_calls[0]

        print("FUNCTION CALL:", call.name)

        tool = registry.get(call.name)

        print("TOOL FOUND:", tool)

        if tool:
            results = tool.execute(call.args["query"])

            print("SEARCH RESULTS:", results)

            finalResponse = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=f"""
Question: {question}

Search results:
{results}

Answer the question using these search results.
Do not call any tools. Just give the user the answer.
"""
            )

            print("FINAL RESPONSE:", finalResponse.text)

            return finalResponse.text

    return response.text

print("HyperCloudAI Agent")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break
    answer = askAgent(question)
    print("AI:", answer)