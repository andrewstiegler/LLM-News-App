# core/search.py
from googlesearch import search
from openai import OpenAI
import os
from backend.utils.config import OPENAI_API_KEY, SERPAPI_KEY
from backend.utils.logger import logger
from datetime import datetime
import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urlparse

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_search_queries(user_prompt: str) -> list[str]:
    today = datetime.now().strftime("%B %d, %Y")  # e.g., "May 19, 2025"

    system_prompt = f"""
You are a skilled news researcher specialized in corporate and industry news. Your task is to rewrite user requests into a set of 1 to 4 **distinct, time-sensitive Google search queries** that surface the most relevant and recent news articles. These queries should focus on company-specific or industry-specific events like quarterly earnings, acquisitions, product launches, partnerships, or regulatory decisions.

**Today's date is: {today}.** Use this as your reference for current year and quarter.

Follow these instructions carefully:

1. **Use Current Year and Quarter Context:**
   - Assume today's year is the default unless the user explicitly specifies another year.
   - If the user mentions a quarter, convert it to the most recent applicable quarter of {today[-4:]}.
   - If the user is vague (e.g. "recent earnings"), infer the most recent completed quarter.
   - Never generate queries about past years (e.g., 2023) unless the user specifies it.

2. **Produce Multiple Distinct Queries:**
   - Generate between 1 and 4 different Google search queries that together fully cover the user’s topic.
   - Each query should target a slightly different angle — e.g., different companies, products, subtopics, or news types (earnings, testing, launches, partnerships, etc.).

3. **Query Format Rules:**
   - DO NOT wrap the entire query in quotation marks.
   - Use **keywords and short phrases**, not full-sentence queries.
   - You MAY use individual quoted terms (e.g., "Abbott" "Q1 2025") for better targeting, but avoid long quoted phrases.
   - DO NOT invent dates. Infer only from today's date or what the user explicitly states.

4. **Examples:**
   - Input: "Abbott infectious disease testing Q1"
     → Output:
       - Abbott Q1 2025 earnings report
       - Abbott infectious disease test sales Q1 2025
       - Abbott diagnostics revenue Q1 2025
       - Abbott COVID flu RSV test update May 2025

   - Input: "Cepheid product news"
     → Output:
       - Cepheid product launch 2025
       - Cepheid respiratory panel update 2025
       - Cepheid diagnostic pipeline May 2025

Return your output as a plain list of search-ready strings.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
    )

    raw_output = response.choices[0].message.content

    # Parse into list — try to be resilient to either newline or numbered formats
    queries = [line.strip("•-0123456789. ") for line in raw_output.splitlines() if line.strip()]
    return [q for q in queries if q]  # remove any empty strings

def is_relevant_article(url: str, min_word_count: int = 300) -> bool:
    try:
        
        # Blocklist check
        blocked_domains = ["wikipedia.org", "facebook.com", "twitter.com", "instagram.com"]
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        if any(blocked in domain for blocked in blocked_domains):
            print(f"Skipping {url}: Domain is blocklisted")
            return False
        
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            print(f"Skipping {url}: HTTP {resp.status_code}")
            return False
        soup = BeautifulSoup(resp.text, "html.parser")

        # Quick URL keyword filter
        product_keywords = ["product", "shop", "buy", "cart", "pricing", "order"]
        if any(k in url.lower() for k in product_keywords):
            print(f"Skipping {url}: URL contains product keywords")
            return False

        # Check title and meta description for ad/product phrases
        title = soup.title.string if soup.title else ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_tag["content"] if meta_tag and meta_tag.get("content") else ""

        combined_text = f"{title} {meta_desc}".lower()
        ad_keywords = ["buy", "shop", "order now", "add to cart", "free shipping"]
        if any(k in combined_text for k in ad_keywords):
            print(f"Skipping {url}: Meta/title contains ad keywords")
            return False

        # Extract paragraphs and count words
        paragraphs = soup.find_all("p")
        text_content = " ".join(p.get_text() for p in paragraphs)
        word_count = len(text_content.split())
        if word_count < min_word_count:
            print(f"Skipping {url}: Content too short ({word_count} words)")
            return False

        # Passed all checks, consider relevant
        return True

    except Exception as e:
        print(f"Error checking relevance for {url}: {e}")
        return False

def search_articles(queries: list[str], num_results_per_query: int = 10) -> list[dict]:
    all_results = []
    seen_links = set()

    one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    for query in queries:
        query_with_time = f"{query} after:{one_week_ago}"
        print(f"🔎 Searching Google for query: {query_with_time}")

        try:
            results = search(query_with_time, num_results=num_results_per_query)
            for url in results:
                if url not in seen_links:
                    if is_relevant_article(url):
                        seen_links.add(url)
                        all_results.append({"title": "", "link": url})
        except Exception as e:
            print(f"Error searching for '{query}': {e}")

    return all_results

if __name__ == "__main__":
    from core.search import generate_search_queries  # or update the import if needed
    result = generate_search_queries("Abbott Q1 earnings")
    search_results = search_articles(result)
    print("[DEBUG]: Search Queries Returned:")
    print(result)
    print("[DEBUG]: Type of Result:", type(result))
    print("[DEBUG]: Search Results Returned:")
    print(search_results)