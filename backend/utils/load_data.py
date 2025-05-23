import json
from pathlib import Path

# Get the path two levels up from utils/load_data.py to reach the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT.parent / "data"  # Go up one more to get to project root

def get_latest_data():
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found at: {DATA_DIR}")

    files = sorted([f for f in DATA_DIR.iterdir() if f.suffix == ".json"], reverse=True)
    if not files:
        return None

    latest_file = files[0]
    with open(latest_file, "r") as f:
        return json.load(f)
