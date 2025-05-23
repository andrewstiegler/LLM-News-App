# core/summarize.py
from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY, MODEL_NAME
from asyncio import to_thread

client = OpenAI(api_key=OPENAI_API_KEY)

async def summarize_article(text: str, max_words: int = 300) -> str:
    def _summarize():
        if not text or not isinstance(text, str):
            return "No article text available for summarization."
        
        prompt = f"Summarize the following article in under {max_words} words:\n\n{text[:4000]}"
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        
        return response.choices[0].message.content.strip()

    return await to_thread(_summarize)

async def generate_daily_summary(articles: list[dict], max_words: int = 300) -> str:
    def _summarize_all():
        if not articles:
            return "No articles found to summarize today."

        # Build a structured input for the LLM
        content_blocks = []
        for article in articles:
            title = article.get("title", "Untitled")
            url = article.get("url", "")
            text = article.get("text", "")[:1000]  # Shorten to keep token count reasonable
            content_blocks.append(f"Title: {title}\nURL: {url}\nExcerpt:\n{text}\n")

        input_text = "\n\n".join(content_blocks)

        # Prompt to generate the summary
        prompt = (
            f"You are an expert business analyst. Your job is to read recent news articles and summarize the most important "
            f"business updates, financial results, and product developments in {max_words} words or less. "
            f"Focus on major takeaways, trends, or corporate moves.\n\n"
            f"Here are today's articles:\n\n{input_text}"
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    return await to_thread(_summarize_all)