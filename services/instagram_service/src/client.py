import grpc

from services.instagram_service.src import gpt_pb2 as gpt
from services.instagram_service.src import gpt_pb2_grpc as gpt_grpc
from services.instagram_service.configs import AppConfig


class ClientGrpc:
    def __init__(self, config: 'AppConfig') -> None:
        self.target = config.TARGET
        self.contextName = config.CONTEXT_NAME
        self.conversationId = config.CONVERSATION_ID

    def run(self, query: str) -> str:
        if not isinstance(query, str):
            query = str(query)

        channel = grpc.insecure_channel(target=self.target)
        stub = gpt_grpc.GptServiceStub(channel)
        request = gpt.AskRequest(contextName=self.contextName, conversationId=self.conversationId, query=query)
        answer = stub.ask(request)
        response = answer.answer
        channel.close()
        return response
