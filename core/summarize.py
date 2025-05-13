# core/summarize.py
import openai
from utils.config import OPENAI_API_KEY, MODEL_NAME
from asyncio import to_thread

openai.api_key = OPENAI_API_KEY

async def summarize_article(text: str, max_words: int = 300) -> str:
    def _summarize():
        prompt = f"Summarize the following article in under {max_words} words:\n\n{text[:4000]}"
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()

    return await to_thread(_summarize)
