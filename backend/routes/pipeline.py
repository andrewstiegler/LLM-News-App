from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import asyncio

from upstash_redis import Redis
from backend.pipeline import run_news_pipeline
from backend.models import db, User
from backend.utils.auth import requires_auth

redis = Redis(url="https://refined-lionfish-46203.upstash.io", token="AbR7AAIjcDFjMTljNTlkMzNjZGY0NTljOWEzMTU4MjVmM2QwY2MzYnAxMA")

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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        summary = loop.run_until_complete(run_news_pipeline(user_id, user_prompt))
        return jsonify({"status": "success", "summary": summary})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
