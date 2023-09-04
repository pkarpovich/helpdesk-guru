from grpclib.client import Channel

from instagram_service.services.lib.gpt import GptServiceStub,AskRequest
from instagram_service.services import AppConfig
class GptService:
    def __init__(self, config:'AppConfig') -> None:
        self.host=config.HOST
        self.port=config.PORT
        self.context_name = config.CONTEXT_NAME
        self.conversation_id = config.CONVERSATION_ID

    async def ask(self, query: str) -> str:
        if not isinstance(query, str):
            query = str(query)

        channel = Channel(host=self.host,port=self.port,ssl=False)
        service = GptServiceStub(channel)
        response = await service.ask(
            AskRequest(
                context_name=self.context_name,
                conversation_id=self.conversation_id,
                query=query
            )
        )

        channel.close()

        return response
