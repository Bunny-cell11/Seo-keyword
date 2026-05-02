from serpapi import GoogleSearch
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

def get_keyword_difficulty(keyword: str, num_results=10):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "num": num_results
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        difficulty = len(organic_results) / max(num_results, 1)
        return difficulty, organic_results
    except:
        return 0, []

