from google import genai
client = genai.Client()

def ask_model(prompt):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    print("HyperCloudAI Chat")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            print("Goodbye!")
            break
        answer = ask_model(question)
        print(f"AI: {answer}\n")