from flask import Blueprint, jsonify
from backend.utils.load_data import get_latest_data
from backend.utils.auth import requires_auth

summaries_bp = Blueprint("summaries", __name__)

@summaries_bp.route("/api/summaries", methods=["GET"])
@requires_auth
def get_summaries(payload):
    try:
        user_id = payload.get("sub")
        if not user_id:
            return jsonify({"error": "User ID not found in token"}), 401

        data = get_latest_data(user_id)
        if not data:
            return jsonify({"error": "No article data found"}), 404

        return jsonify({
            "daily_summary": data.get("daily_summary", ""),
            "articles": data.get("articles", [])
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500