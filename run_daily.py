import asyncio
import sys

from pipeline import run_news_pipeline

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        user_prompt = input("Enter today's topic of interest: ").strip()

    if not user_prompt:
        print("❌ No prompt provided. Exiting.")
        sys.exit(1)

    asyncio.run(run_news_pipeline(user_prompt))
