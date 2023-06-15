from lib.gpt import GptServiceBase, AskResponse, AskRequest, ClearHistoryRequest, ClearHistoryResponse
from openai_client import OpenaiClient


class GptService(GptServiceBase):
    def __init__(self, openai: OpenaiClient):
        self.openai = openai

    async def ask(self, ask_request: AskRequest) -> AskResponse:
        return AskResponse(answer=self.openai.ask(ask_request.query))

    async def clear_history(self, clear_history_request: ClearHistoryRequest) -> ClearHistoryResponse:
        self.openai.clear_history()
        return ClearHistoryResponse()