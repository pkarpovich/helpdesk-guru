from lib.gpt import GptServiceBase, AskResponse, AskRequest
from openai_client import OpenaiClient


class GptService(GptServiceBase):
    def __init__(self, openai: OpenaiClient):
        self.openai = openai

    async def ask(self, ask_request: AskRequest) -> AskResponse:
        return AskResponse(answer=self.openai.ask(ask_request.query))
