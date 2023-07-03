from openai_client import OpenaiClient

from gpt_context.adapters.vector_store_adapter import VectorStoreAdapter

from lib.gpt import (
    GptServiceBase,
    AskResponse,
    AskRequest,
    ClearHistoryRequest,
    ClearHistoryResponse,
    ClearIndexRequest,
    ClearIndexResponse,
)


class GptService(GptServiceBase):
    def __init__(self, openai: OpenaiClient, store: VectorStoreAdapter):
        self.openai = openai
        self.store = store

    async def ask(self, ask_request: AskRequest) -> AskResponse:
        return AskResponse(answer=self.openai.ask(ask_request.query))

    async def clear_history(self, clear_history_request: ClearHistoryRequest) -> ClearHistoryResponse:
        self.openai.clear_history()
        return ClearHistoryResponse()

    async def clear_index(self, clear_index_request: ClearIndexRequest) -> ClearIndexResponse:
        self.store.truncate()
        return ClearIndexResponse()
