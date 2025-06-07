import asyncio
import json
from upstash_redis import Redis
from backend.pipeline import run_news_pipeline  # adjust import as needed
from backend.utils.config import REDIS_URL, REDIS_TOKEN  # adjust import as needed

REDIS_URL = REDIS_URL
REDIS_TOKEN = REDIS_TOKEN

redis = Redis(url="https://refined-lionfish-46203.upstash.io", token="AbR7AAIjcDFjMTljNTlkMzNjZGY0NTljOWEzMTU4MjVmM2QwY2MzYnAxMA")

async def main():
    print("🚀 Worker started. Listening for tasks...")
    while True:
        try:
            _, task_data = await client.blpop("pipeline_queue")
            task = json.loads(task_data)
            print(f"📥 Received task: {task}")
            
            user_id = task.get("user_id")
            prompt = task.get("prompt")

            result = await run_news_pipeline(user_id, prompt)
            print(f"✅ Finished task: {task['task_id']}")
            # optionally: store result in Redis or DB here

        except Exception as e:
            print(f"❌ Error processing task: {e}")

if __name__ == "__main__":
    asyncio.run(main())
