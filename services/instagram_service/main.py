import os
import asyncio
from dotenv import load_dotenv
from controller import instagram_Contoller
from src import client_grpc
from src import InstagramService


load_dotenv()

if __name__=='main':
  username=os.environ.get('USER_NAME')
  password=os.environ.get('PASSWORD')
  proxy=os.environ.get('PROXY')
  target=os.environ.get('TARGET')
  conversationId=os.environ.get('CONVERSATION_ID')
  contextName=os.environ.get('CONTEXTNAME')
  instagram_service=InstagramService(username,password)
  client=client_grpc(contextName=contextName,conversationId=conversationId,target=target)
  instagram_controller=instagram_Contoller(instagram_service,client)
  asyncio.run(instagram_controller.start())
