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



# 3.Agent Translator
def translator_agent(english_text: str) -> str:
    print("Translate the Summary Text into Persian ... ")

    response = client.chat(
        model=ollama_model,
        messages=[
            {
                "role": "system",
                "content": """
you are the helpful translator languages into the persian.
translate the givin text from user into persian.
                """
            },
            {
                "role": "user",
                "content": f"Translate the below text into the persian language.\n\n{english_text}"
            }
        ]
    )

    return response.message.content


# 4.Agent Translator
def save_agent(text: str, file_name: str) -> None:
    print("Saving the all result in file ... ")

    with open(file_name, 'w', encoding="UTF-8") as file:
        file.write(text)

    print("Done!")

# orchestrator
def main():
    input_topic = input("Enter your topic that want to search: ")
    input_num_result = int(input("Enter number of result: ")) 

    response = search_agent(input_topic, input_num_result)
    print("Searching Done!")
    save_agent(response, f"save_files/result of searching about {input_topic}.rtf")


    summary_text = summarize_agent(response)
    print("summarizing Done!")
    save_agent(summary_text, f"save_files/summary of all result about {input_topic}.rtf")


    translate_text = translator_agent(summary_text)
    print("translate Done!")
    save_agent(translate_text, f"save_files/translate of summary about {input_topic}.rtf")

        
if __name__ == "__main__":
    main()


