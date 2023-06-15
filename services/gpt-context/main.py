import os
import asyncio
from grpclib.server import Server
from dotenv import load_dotenv
from openai_client import OpenaiClient

from gpt_service import GptService

load_dotenv()

model_name = os.environ.get('OPENAI_MODEL')


async def main():
    if os.environ.get("OPENAI_API_KEY") is None:
        print("OpenAI API key not set")
        return None

    redis_url = os.environ.get("REDIS_URL") or "redis://localhost:6379"
    weaviate_url = os.environ.get("WEAVIATE_URL") or "http://localhost:8080"

    openai_client = OpenaiClient(model_name, redis_url, weaviate_url)

    server = Server([GptService(openai_client)])
    await server.start("0.0.0.0", 50051)
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
