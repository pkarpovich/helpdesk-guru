from gpt_context.controllers import GptController
from gpt_context.exceptions import BusinessLogicException

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
    ErrorInfo
)


class GptGrpcService(GptServiceBase):
    def __init__(self, gpt_controller: GptController):
        self.gpt_controller = gpt_controller

    async def ask(self, ask_request: AskRequest) -> AskResponse:
        try:
            answer = self.gpt_controller.ask(
                ask_request.query,
                ask_request.conversation_id,
                ask_request.context_name
            )
            return AskResponse(answer=answer)
        except BusinessLogicException as e:
            return AskResponse(error=ErrorInfo(code=e.code, message=e.message))

    async def clear_history(self, clear_history_request: ClearHistoryRequest) -> ClearHistoryResponse:
        self.gpt_controller.clear_history(clear_history_request.conversation_id)
        return ClearHistoryResponse()

    async def clear_index(self, clear_index_request: ClearIndexRequest) -> ClearIndexResponse:
        try:
            self.gpt_controller.clear_index(clear_index_request.context_name)
            return ClearIndexResponse()
        except BusinessLogicException as e:
            return ClearIndexResponse(error=ErrorInfo(code=e.code, message=e.message))

    async def add_google_docs(self, add_google_docs_request: AddGoogleDocsRequest) -> AddGoogleDocsResponse:
        self.gpt_controller.add_google_docs(add_google_docs_request.folder_id, add_google_docs_request.context_name)
        return AddGoogleDocsResponse()
