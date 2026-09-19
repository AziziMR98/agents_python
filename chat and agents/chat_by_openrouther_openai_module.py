from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

routher_api_key = os.getenv("OPEN_ROUTER_API_KEY", "")
routher_model = os.getenv("OPEN_ROUTER_MODEL", "")

# print(f"API Key: {routher_api_key}")
# print(f"Model: {routher_model}")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=routher_api_key,
)

def ask_openrouter(prompt: str) -> set:

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
        response = client.chat.completions.create(
            model=routher_model,
            messages = message,
            extra_body={"reasoning": {"enabled": True}}
            )


    except Exception as e:
        return f"Error: {e}"

    return response

if __name__ == "__main__":
    user_prompt = input("User: ")

    response = ask_openrouter(user_prompt)
    print(response.choices[0].message.content)




