# utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

SEARCH_NUM_RESULTS = int(os.getenv("SEARCH_NUM_RESULTS", 5))
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")

# Optional safety check
required_vars = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "SERPAPI_KEY": SERPAPI_KEY
}
for var, val in required_vars.items():
    if not val:
        raise ValueError(f"Missing required environment variable: {var}")
