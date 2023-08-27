from grpclib.client import Channel

from lib.gpt import GptServiceStub, AskRequest


class GptService:
    def __init__(self, context_name: str, conversation_id: str, host: str, port: int) -> None:
        self.conversation_id = conversation_id
        self.context_name = context_name
        self.host = host
        self.port = port

    async def ask(self, query: str) -> str:
        if not isinstance(query, str):
            query = str(query)

        channel = Channel(host=self.host, port=self.port, ssl=False)
        service = GptServiceStub(channel)

        response = await service.ask(
            AskRequest(
                context_name=self.context_name,
                conversation_id=self.conversation_id,
                query=query
            )
        )

        channel.close()

        return response.answer
