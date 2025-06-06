from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_about_articles(question, articles):
    context = "\n\n".join(
        f"{a.get('title', 'Untitled')}:\n{a.get('summary', '')}" for a in articles
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers questions based only on the provided news summaries."
                "\n\nHere are today's news summaries:\n" + context)
        },
        {
            "role": "assistant",
            "content": f"Today's news context:\n\n{context}"
        },
        {
            "role": "user",
            "content": question
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
