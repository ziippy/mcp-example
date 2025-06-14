import requests

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_google(query: str) -> str:
    url = "https://google.serper.dev/search"
    headers = { "X-API-KEY": SERPER_API_KEY }
    data = { "q": query }
    response = requests.post(url, json=data, headers=headers)
    results = response.json()
    return results["organic"][0]["snippet"] if results.get("organic") else "No results"

# print(search_google("LLMOps란?"))

# print(search_google("서울 현재"))