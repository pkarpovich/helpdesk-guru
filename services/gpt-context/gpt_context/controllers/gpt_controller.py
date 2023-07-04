from gpt_context.services.context_service import ContextService
from gpt_context.services.qa_service import QAService


class GptController:
    def __init__(self, qa_service: QAService, context_service: ContextService):
        self.qa_service = qa_service
        self.context_service = context_service

    def ask(self, query: str) -> str:
        return self.qa_service.ask(query)

    def clear_history(self) -> None:
        return self.qa_service.clear_history()

    def clear_index(self) -> None:
        return self.context_service.clear_index()
