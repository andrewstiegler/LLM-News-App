from flask import Blueprint, request, jsonify
from utils.load_data import get_latest_data
from services.openai_client import ask_about_articles

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "Question is required"}), 400
    data = get_latest_data()
    articles = data.get("articles", [])
    reply = ask_about_articles(question, articles)
    return jsonify({"response": reply})
