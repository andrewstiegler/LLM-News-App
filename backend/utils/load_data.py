import logging
import json
from backend.models import db, UserResult

def get_latest_data(user_id: str):
    try:
        result = (
            UserResult.query
            .filter_by(user_id=user_id)
            .order_by(UserResult.created_at.desc())
            .first()
        )
        if not result:
            logging.warning(f"No UserResult found for user_id: {user_id}")
            return None

        if not result.result_json:
            logging.warning(f"UserResult found but result_json is empty for user_id: {user_id}")
            return None

        if isinstance(result.result_json, str):
            try:
                 return json.loads(result.result_json)
            except json.JSONDecodeError as e:
                logging.error(f"Failed to decode JSON from DB for user_id {user_id}: {e}")
                return None
        
        # If it's already a dict (JSONB), return as-is
        return result.result_json

    except Exception as e:
        logging.error(f"Exception querying UserResult for user_id {user_id}: {e}", exc_info=True)
        return None
