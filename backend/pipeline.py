import json
from datetime import datetime
import asyncio

from core.search import generate_search_queries, search_articles
from core.fetch import fetch_article_text  # includes fetch + summarize
from core.summarize import summarize_article, generate_daily_summary

from backend.models import db, UserResult

async def run_news_pipeline(user_id: str, user_prompt: str) -> str:
    if not user_id or not isinstance(user_id, str):
        raise ValueError("user_id must be a non-empty string")
    if not user_prompt or not user_prompt.strip():
        raise ValueError("user_prompt must be a non-empty string")
        
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
    articles_data = []
    for a in articles:
        if not a:
            continue
        text = a.get("text")
        if text and len(text) > 200:
            articles_data.append(a)

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

    try:
        result_entry = UserResult(
            user_id=user_id, # type: ignore
            result_json=json.dumps(save_data), # type: ignore
        )

        db.session.add(result_entry)
        db.session.commit()
        print(f"✅ DB Write Successful: Saved {len(articles_data)} articles for user {user_id}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ DB Write Failed: {e}")
    
    return daily_summary