# run_daily.py
import asyncio
from core.search import generate_search_query, search_articles
from core.fetch import fetch_article_text
from core.summarize import summarize_article
import json, os
from datetime import datetime

async def process_article(title: str, url: str) -> dict | None:
    print(f"Fetching: {title}")
    text = await fetch_article_text(url)
    if not text:
        return None
    summary = await summarize_article(text)
    return {
        "title": title,
        "url": url,
        "summary": summary,
        "raw_text": text
    }

async def run_pipeline_async(user_prompt: str):
    search_query = generate_search_query(user_prompt)
    print(f"[Search Query]: {search_query}")

    results = search_articles(search_query)
    tasks = [
        process_article(r["title"], r["link"])
        for r in results if r.get("link") and r.get("title")
    ]
    articles = await asyncio.gather(*tasks)
    articles_data = [a for a in articles if a is not None]

    save_path = f"data/daily_{datetime.now().strftime('%Y%m%d')}.json"
    os.makedirs("data", exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(articles_data, f, indent=2)
    print(f"Saved {len(articles_data)} articles to {save_path}")

if __name__ == "__main__":
    user_prompt = input("Enter today's topic of interest: ")
    asyncio.run(run_pipeline_async(user_prompt))
