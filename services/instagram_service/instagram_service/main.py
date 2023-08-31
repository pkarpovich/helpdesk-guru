import os
import asyncio

from dotenv import load_dotenv
from instagram_service.configs import AppConfig
from instagram_service.controller import InstagramController
from instagram_service.services import InstagramService, GptService

load_dotenv()

config = AppConfig(os.environ)
print(config)
instagram_service=InstagramService(config=config)
client=GptService(config=config)
instagram_controller=InstagramContoller()
instagram_controller.__int__(instagram_service, client)

if __name__=='__main__':
 asyncio.run(instagram_controller.start())
