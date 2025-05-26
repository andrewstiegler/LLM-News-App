import os
import json
from datetime import datetime
import asyncio

from core.search import generate_search_queries, search_articles
from core.fetch import fetch_article_text  # includes fetch + summarize
from core.summarize import summarize_article, generate_daily_summary

async def run_news_pipeline(user_prompt: str) -> str:
    print(f"🔍 Generating search queries for: '{user_prompt}'")
    search_queries = generate_search_queries(user_prompt)
    print(f"[Search Queries]: {search_queries}")

    # 🔁 Search all queries
    all_results = []
    for query in search_queries:
        print(f"🔎 Searching: {query}")
        results = search_articles([query])
        all_results.extend(results)

    # 🧼 Deduplicate by URL
    seen = set()
    unique_results = []
    for r in all_results:
        url = r.get("link")
        if url and url not in seen:
            seen.add(url)
            unique_results.append(r)

    print(f"📰 Found {len(unique_results)} unique articles")

    # ⚙️ Process articles (scrape + summarize)
    tasks = [fetch_article_text(r["link"]) for r in unique_results if r.get("link")]
    articles = await asyncio.gather(*tasks)
    articles_data = [
        a for a in articles if a and a.get("text") and len(a.get("text")) > 200
    ]

    print(f"✍️ Processed {len(articles_data)} articles")

    # 📄 Generate daily summary
    daily_summary = await generate_daily_summary(articles_data)

    # 💾 Save to file
    save_data = {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "user_prompt": user_prompt,
        "daily_summary": daily_summary,
        "articles": articles_data,
    }

    os.makedirs("data", exist_ok=True)
    save_path = f"data/daily_{datetime.now().strftime('%Y%m%d')}.json"
    with open(save_path, "w") as f:
        json.dump(save_data, f, indent=2)

    print(f"✅ Saved {len(articles_data)} articles and summary to {save_path}")

    return daily_summary
