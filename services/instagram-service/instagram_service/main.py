import asyncio
import os

from dotenv import load_dotenv

from instagram_service.controller import InstagramController
from instagram_service.services import InstagramService, GptService

load_dotenv()

if __name__ == '__main__':
    username = os.environ.get('USER_NAME')
    password = os.environ.get('PASSWORD')
    proxy = os.environ.get('PROXY')
    gpt_service_host = os.environ.get('GPT_SERVICE_HOST')
    gpt_service_port = os.environ.get('GPT_SERVICE_PORT')
    conversation_id = os.environ.get('CONVERSATION_ID')
    context_name = os.environ.get('CONTEXT_NAME')

    instagram_service = InstagramService(username, password)
    gpt_service = GptService(
        context_name=context_name,
        conversation_id=conversation_id,
        host=gpt_service_host,
        port=int(gpt_service_port)
    )

    instagram_controller = InstagramController(instagram_service, gpt_service)

    asyncio.run(instagram_controller.start())
