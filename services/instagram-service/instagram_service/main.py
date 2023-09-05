import asyncio
import os

from dotenv import load_dotenv

from instagram_service.controller import InstagramContoller
from instagram_service.services import AppConfig
from instagram_service.services import InstagramService, GptService

load_dotenv()


async def main():
    config = AppConfig(os.environ)
    instagram_service = InstagramService(config=config)
    client = GptService(config=config)
    instagram_controller = InstagramContoller()
    instagram_controller.__int__(instagram_service, client)
    await instagram_controller.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
