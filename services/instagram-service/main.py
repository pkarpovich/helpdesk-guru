import os
import asyncio
from dotenv import load_dotenv

from services.instagram_service.src import InstagramService
from services.instagram_service.controller import InstagramContoller
from services.instagram_service.src import ClientGrpc

load_dotenv()

if __name__=='__main__':

  username=os.environ.get('USER_NAME')
  password=os.environ.get('PASSWORD')
  proxy=os.environ.get('PROXY')
  target=os.environ.get('TARGET')
  conversationId=os.environ.get('CONVERSATION_ID')
  contextName=os.environ.get('CONTEXT_NAME')

  instagram_service=InstagramService(username,password)
  client=ClientGrpc(contextName=contextName,conversationId=conversationId,target=target)
  instagram_controller=InstagramContoller()
  instagram_controller.__int__(instagram_service, client)

  asyncio.run(instagram_controller.start())
