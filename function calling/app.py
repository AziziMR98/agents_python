import requests
from ollama import Client
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OLAMA_API_KEY")
Model = os.getenv("OLAMA_MODEL")


def ask_ollama(prompt: str) -> str:
    """Sends a prompt to the Ollama model and detect the indeed tools."""
    client = Client.chat(
        model=Model,
        headers={
            "Authorization": f"Bearer {API_KEY}"
        },
        Messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that detects the indeed tools.
                you must return the results as a single, continuous piece of prose.
                this means you must not return the results as one function's name from a list that i will you.

                our list of functions that you can use is:
                1. get_current_weather(location: str) -> str: Fetches the current weather for a given location.

                example of the output you should return:
                user: "What is the current weather in New York?"
                assistant: 1, New York
                """
        ]


        
    )


def get_current_weather(location: str) -> str:
    """Fetches the current weather for a given location."""
    base_url = "https://wttr.in/{location}?format=j1"
    response = requests.get(base_url.format(location=location))
    return response.json()

def weather_report(json_information: str) -> str:
    """Asks the Ollama model for weather information based on the provided JSON data."""
    response = client.chat(
        model=Model,
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that provides weather information.
                you must return the results as a single, continuous piece of prose.
                that is, you must not return the results as a list or any other format.
                like :
                city: {city}
                today: 
                    temperature: {temperature} C
                    Sunny Day or any rainy day or any other weather condition
                
                tomorrow:
                    temperature: {temperature} C
                    sunny Day or any rainy day or any other weather condition

                the day after tomorrow:
                    temperature: {temperature} C
                    Sunny Day or any rainy day or any other weather condition
                """
            },
            {
                "role": "user",
                "content": f"Here is the weather data in JSON format: {json_information}"
            }
        ]
    )
    return response['choices'][0]['message']['content']


if __name__ == "__main__":
    city = input("Enter a city name to get the current weather: ")
    weather_data = get_current_weather(city)
    print(f"Current weather in {city}:")
    print(weather_data['current_condition'][0]['temp_C'], "°C")