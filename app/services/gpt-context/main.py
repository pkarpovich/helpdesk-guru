import os
import asyncio
from grpclib.server import Server
from dotenv import load_dotenv
from openai_client import OpenaiClient

from gpt_service import GptService

load_dotenv()

persist_directory = os.environ.get('PERSIST_DIRECTORY')
model_name = os.environ.get('OPENAI_MODEL')


async def main():
    if os.environ.get("OPENAI_API_KEY") is None:
        print("OpenAI API key not set")
        return None

    openai_client = OpenaiClient(persist_directory, model_name)

    server = Server([GptService(openai_client)])
    await server.start("0.0.0.0", 50051)
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
