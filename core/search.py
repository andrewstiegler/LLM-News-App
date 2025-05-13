# core/search.py
import openai
from utils.config import OPENAI_API_KEY
from serpapi import GoogleSearch

openai.api_key = OPENAI_API_KEY

def generate_search_query(user_prompt: str) -> str:
    system_prompt = "Convert this user prompt into a precise Google search query for news or finance articles."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )
    return response['choices'][0]['message']['content'].strip()

def search_articles(query: str, num_results: int = 5) -> list[dict]:
    params = {
        "engine": "google",
        "q": query,
        "num": num_results,
        "api_key": "<your_serpapi_key>"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])
