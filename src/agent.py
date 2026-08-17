from google import genai
from google.genai import types
from search_tool import search_project

client = genai.Client()

search_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_project",
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


def ask_agent(question):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[search_tool]
        ),
    )

    if response.function_calls:
        call = response.function_calls[0]

        if call.name == "search_project":
            results = search_project(call.args["query"])

            final_response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=f"""
Question: {question}

The project search tool found these results:
{results}

Answer the user's question using these results.
""",
            )

            return final_response.text

    return response.text


print("HyperCloudAI Agent")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    answer = ask_agent(question)
    print("AI:", answer)