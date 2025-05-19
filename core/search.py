# core/search.py
from serpapi import GoogleSearch
from openai import OpenAI
import os
from utils.config import OPENAI_API_KEY, SERPAPI_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_search_query(user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You help reword user goals into search queries."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

def search_articles(query: str, num_results: int = 10) -> list[dict]:
    params = {
        "engine": "google",
        "q": query,
        "num": num_results,
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    
    # Make sure each result has 'title' and 'link'
    cleaned = []
    for result in organic_results:
        title = result.get("title")
        link = result.get("link")
        if title and link:
            cleaned.append({"title": title, "link": link})
    
    return cleaned

