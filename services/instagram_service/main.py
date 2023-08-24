import os
import asyncio

from dotenv import load_dotenv

from services.instagram_service.src import InstagramService
from services.instagram_service.controller import InstagramContoller
from services.instagram_service.src import ClientGrpc
from services.instagram_service.configs import AppConfig

load_dotenv()

if __name__=='__main__':
  config = AppConfig(os.environ)

  instagram_service=InstagramService(config=config)
  client=ClientGrpc(config=config)
  instagram_controller=InstagramContoller()
  instagram_controller.__int__(instagram_service, client)

  asyncio.run(instagram_controller.start())
