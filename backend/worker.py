import asyncio
import time
from backend.pipeline import run_news_pipeline
from backend.models import db, UserPrompt
from flask import Flask
from backend.utils.config import DATABASE_URL

# Minimal Flask app context to use SQLAlchemy outside the main app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

async def process_prompt(prompt_obj):
    try:
        print(f"📥 Processing prompt ID {prompt_obj.id} for user {prompt_obj.user_id}")
        await run_news_pipeline(prompt_obj.user_id, prompt_obj.prompt_text)

        # Mark as completed
        prompt_obj.status = 'completed'
        db.session.commit()
        print(f"✅ Completed prompt ID {prompt_obj.id}")

    except Exception as e:
        print(f"❌ Error processing prompt ID {prompt_obj.id}: {e}")
        prompt_obj.status = 'error'
        db.session.commit()

async def main():
    print("🚀 Worker started. Polling for pending prompts...")
    while True:
        try:
            with app.app_context():
                pending_prompt = (
                    db.session.query(UserPrompt)
                    .filter_by(status='pending')
                    .order_by(UserPrompt.created_at.asc())
                    .first()
                )

                if pending_prompt:
                    await process_prompt(pending_prompt)
                else:
                    print("🕐 No pending prompts. Sleeping...")

        except Exception as e:
            print(f"❌ Worker loop error: {e}")

        time.sleep(5)  # Poll every 5 seconds

if __name__ == "__main__":
    asyncio.run(main())