# core/fetch.py
from readability import Document
from bs4 import BeautifulSoup
import httpx
from loguru import logger

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0.0.0 Safari/537.36"
    )
}

async def fetch_article_text(url: str, timeout: int = 10) -> dict:
    try:
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
            response = await client.get(url, timeout=timeout)
            response.raise_for_status()
            html = response.text

        doc = Document(html)
        title = doc.title()
        cleaned_html = doc.summary()
        text = BeautifulSoup(cleaned_html, "html.parser").get_text()

        if len(text.strip()) < 200:
            logger.warning(f"⚠️ Skipping {url} — too little text")
            return {"url": url, "title": title, "text": ""}

        logger.info(f"✅ Text length from {url}: {len(text)}")
        return {"url": url, "title": title, "text": text.strip()}
        

    except Exception as e:
        logger.warning(f"❌ Failed to fetch or parse {url}: {e}")
        return {"url": url, "title": "", "text": ""}
