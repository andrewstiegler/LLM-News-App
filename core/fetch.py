# core/fetch.py
import aiohttp
from newspaper import Article
from asyncio import to_thread

async def fetch_article_text(url: str) -> str:
    try:
        # Use to_thread to run blocking newspaper3k parsing
        def _parse_article():
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        
        return await to_thread(_parse_article)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""
