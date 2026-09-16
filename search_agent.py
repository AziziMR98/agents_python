from ollama import Client
import os
from ddgs import DDGS
from dotenv import load_dotenv
from alive_progress import alive_bar
import threading
import time




load_dotenv()

ollama_model = os.getenv("OLAMA_MODEL", "")
ollama_api_key = os.getenv("OLAMA_API_KEY", "")

client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": f"Bearer {ollama_api_key}"
    }
)


# 1. Searching Agent
def search_agent(topic, num_result=5):

    results = []

    def search():
        nonlocal results
        with DDGS() as ddgs:
            for item in ddgs.text(topic, max_results=num_result):
                results.append(f'title: {item['title']}\nURL: {item['href']}\nSnippet: {item['body']}')

    t = threading.Thread(target=search)

    with alive_bar(None, title="Searching") as bar:
        t.start()

        while t.is_alive():
            bar()
            time.sleep(0.1)

        t.join()

    return "\n\n--------------\n\n".join(results)

# 2. Summay Agent
def summarize_agent(text: str) -> str:
    print("Summarizing Text:")

    response = client.chat(
        model=ollama_model,
        messages=[
            {
                "role": "system",
                'content': """
you are helpful summarizer.
Return the results as a single, countinuous piece of prose;
do not use table.
"""
            },
            {
                "role": "user",
                "content": f"Summarize the following the search result: \n\n{text}"
            }
        ]
    )

    return response.message.content


if __name__ == "__main__":
    input_topic = input("Enter your topic that want to search: ")
    input_num_result = int(input("Enter number of result: ")) 

    response = search_agent(input_topic, input_num_result)

    print(response, end= "\n\n\n----------\n\n\n")

    print(summarize_agent(response))
