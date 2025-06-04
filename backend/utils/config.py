# backend/utils/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Load local .env only in development
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Load variables from environment (Heroku uses these!)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

SEARCH_NUM_RESULTS = int(os.getenv("SEARCH_NUM_RESULTS", 5))
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

POSTGRES_URL = os.getenv("POSTGRES_URL")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix Heroku-style DATABASE_URL if needed
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Safety check — only warn if missing and not on Heroku
if not os.getenv("DYNO"):  # Set automatically on Heroku
    required_vars = {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "POSTGRES_URL": POSTGRES_URL,
        "AUTH0_DOMAIN": AUTH0_DOMAIN,
        "AUTH0_CLIENT_ID": AUTH0_CLIENT_ID,
        "AUTH0_API_AUDIENCE": AUTH0_API_AUDIENCE,
        "DATABASE_URL": DATABASE_URL,
    }

    for var, val in required_vars.items():
        if not val:
            raise ValueError(f"Missing required environment variable: {var}")
