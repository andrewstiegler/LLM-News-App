from flask import Blueprint, request, jsonify
from backend.utils.load_data import get_latest_data
from backend.services.openai_client import ask_about_articles
from backend.utils.auth import requires_auth

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/api/chat", methods=["POST"])
@requires_auth
def chat(payload):
    user_id = payload.get("sub")
    if not user_id:
        return jsonify({"error": "User ID not found in token"}), 401

    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Question is required"}), 400
    question = data["question"].strip()

    data = get_latest_data(user_id)
    if not data:
        return jsonify({"error": "No article data found"}), 404

    articles = data.get("articles", [])
    reply = ask_about_articles(question, articles)
    return jsonify({"response": reply})