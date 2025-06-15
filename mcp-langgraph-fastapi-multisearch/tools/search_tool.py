import requests

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# def search_google(query: str) -> str:
#     url = "https://google.serper.dev/search"
#     headers = { "X-API-KEY": SERPER_API_KEY }
#     data = { "q": query }
#     response = requests.post(url, json=data, headers=headers)
#     results = response.json()
#     return results["organic"][0]["snippet"] if results.get("organic") else "No results"

def search_google_all(query: str, max_results: int = 5) -> list[dict]:
    """
    Serper API를 사용해 검색 결과를 다수 반환하는 함수
    :param query: 검색어
    :param api_key: Serper API 키
    :param max_results: 반환할 최대 결과 수
    :return: 검색 결과의 리스트 (title, snippet 포함)
    """
    url = "https://google.serper.dev/search"
    headers = { "X-API-KEY": SERPER_API_KEY }
    data = { "q": query }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # 에러 시 예외 발생
    results = response.json()

    organic_results = results.get("organic", [])
    # 최대 max_results 개까지만 추려서 반환
    return [
        {
            "title": r.get("title", ""),
            "snippet": r.get("snippet", "")
        }
        for r in organic_results[:max_results]
    ]

# print(search_google("LLMOps란?"))

# print(search_google("서울 현재"))