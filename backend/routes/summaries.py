from flask import Blueprint, jsonify
from utils.load_data import get_latest_data

summaries_bp = Blueprint("summaries", __name__)

@summaries_bp.route("/api/summaries", methods=["GET"])
def get_summaries():
    data = get_latest_data()
    if not data:
        return jsonify({"error": "No article data found"}), 404
    return jsonify({
        "daily_summary": data.get("daily_summary", ""),
        "articles": data.get("articles", [])
    })
