from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from backend.models import db, UserPrompt
from backend.utils.auth import requires_auth

pipeline_bp = Blueprint("pipeline", __name__)

@pipeline_bp.route("/api/run_pipeline", methods=["POST"])
@cross_origin()
@requires_auth
def run_pipeline_route(payload):
    data = request.json
    if data is None:
        return jsonify({"error": "Missing JSON in request"}), 400

    user_id = data.get("user_id")
    user_prompt = data.get("user_prompt")

    if not user_id or not user_prompt:
        return jsonify({"error": "Missing user_id or user_prompt"}), 400

    try:
        # Create a new UserPrompt with status = 'pending'
        prompt = UserPrompt(
            user_id=user_id,
            prompt_text=user_prompt,
            status="pending",
            created_at=datetime.utcnow()
        )
        db.session.add(prompt)
        db.session.commit()

        return jsonify({"status": "queued", "prompt_id": prompt.id}), 202

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
