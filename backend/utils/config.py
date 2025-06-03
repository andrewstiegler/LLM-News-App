# utils/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

SEARCH_NUM_RESULTS = int(os.getenv("SEARCH_NUM_RESULTS", 5))
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

POSTGRES_URL = os.getenv("POSTGRES_URL")

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")

# Optional safety check
required_vars = {
     "OPENAI_API_KEY": OPENAI_API_KEY,
     "POSTGRES_URL": POSTGRES_URL,
     "AUTH0_DOMAIN": AUTH0_DOMAIN,
     "AUTH0_CLIENT_ID": AUTH0_CLIENT_ID,
     "AUTH0_API_AUDIENCE": AUTH0_API_AUDIENCE
 }
for var, val in required_vars.items():
    if not val:
        raise ValueError(f"Missing required environment variable: {var}")
