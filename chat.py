import os 
import requests
from ollama import Client
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_ROUTER_API_KEY", "")
# print(f"API: {API_KEY}")
MODEL = os.getenv("OPEN_ROUTER_MODEL", "")
# print(f"OPEN_ROUTER MODEL: {MODEL}")


client = Client(
    host="https://ollama.com", 
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

def ask_ollama(prompt: str) -> set:
    message = [
        {
            "role": "system",
            "content": """
            You are an intelligent assistant to provide more accurate answer .
            provided the summarized answer but it be a simple answer!
            """
        },
        {
            "role": "user",
            "content": prompt
        }

    ]

    try:
        result = client.chat(
            model= MODEL,
            messages= message
        )

    except Exception as e:
        return f"Error: {e}"

    return result

if __name__ == "__main__":
    user_prompt = input("User: ")

    response = ask_ollama(user_prompt)
    print(response)
    # print(f"Model that Response:\n {response['model']}", end="\n\n")
    # print(f"Response:\n {response['message']['content']}", end="\n\n")
