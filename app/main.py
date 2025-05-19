# app/main.py
# ---- add project root so sibling packages resolve --------------------------
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
# -----------------------------------------------------------------------------

from utils.config import OPENAI_API_KEY, MODEL_NAME
from utils.logger import logger
import streamlit as st
import json
import os
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="Daily News Agent", layout="wide")
st.title("🧠 Daily News Agent")

# Load latest article file
def get_latest_data():
    data_dir = "data"
    files = sorted([f for f in os.listdir(data_dir) if f.endswith(".json")], reverse=True)
    if not files:
        return []
    latest_file = os.path.join(data_dir, files[0])
    with open(latest_file, "r") as f:
        return json.load(f)

articles = get_latest_data()

if not articles:
    st.warning("No article data found. Run `run_daily.py` first.")
    st.stop()

# Build a markdown-friendly summary of the articles
def build_article_context(articles):
    summaries = []
    for a in articles:
        title = a.get("title", "Untitled")
        summary = a.get("summary", "No summary available.")
        url = a.get("url") or a.get("link", "")
        summaries.append(f"**[{title}]({url})**\n{summary}")
    return "\n\n".join(summaries)

# Streamlit app title
st.title("🗞️ LLM News Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions based on a collection of recent summarized news articles. Always refer to the article context when responding."
        }
    ]

# Add article summaries as assistant context once
if "context_injected" not in st.session_state:
    context = build_article_context(articles)
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Here are the recent articles I've summarized:\n\n{context}"
    })
    st.session_state.context_injected = True

# Render chat messages
for msg in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Ask me something about the news..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Optional reset
if st.button("🔄 Reset"):
    del st.session_state.messages
    del st.session_state.context_injected
    st.experimental_rerun()