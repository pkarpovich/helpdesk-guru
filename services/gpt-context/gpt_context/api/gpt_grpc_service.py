from gpt_context.controllers.gpt_controller import GptController

from lib.gpt import (
    GptServiceBase,
    AskResponse,
    AskRequest,
    ClearHistoryRequest,
    ClearHistoryResponse,
    ClearIndexRequest,
    ClearIndexResponse,
    AddGoogleDocsRequest,
    AddGoogleDocsResponse,
)


class GptGrpcService(GptServiceBase):
    def __init__(self, gpt_controller: GptController):
        self.gpt_controller = gpt_controller

    async def ask(self, ask_request: AskRequest) -> AskResponse:
        answer = self.gpt_controller.ask(ask_request.query, ask_request.conversation_id)
        return AskResponse(answer=answer)

    async def clear_history(self, clear_history_request: ClearHistoryRequest) -> ClearHistoryResponse:
        self.gpt_controller.clear_history(clear_history_request.conversation_id)
        return ClearHistoryResponse()

    async def clear_index(self, clear_index_request: ClearIndexRequest) -> ClearIndexResponse:
        self.gpt_controller.clear_index()
        return ClearIndexResponse()

    async def add_google_docs(self, add_google_docs_request: AddGoogleDocsRequest) -> AddGoogleDocsResponse:
        self.gpt_controller.add_google_docs(add_google_docs_request.folder_id)
        return AddGoogleDocsResponse()
