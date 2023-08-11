import asyncio
import os

from grpclib.server import Server
from langchain.embeddings import OpenAIEmbeddings

from gpt_context.adapters import WeaviateVectorStoreAdapter
from gpt_context.api import GptGrpcService, HealthCheckGrpcService
from gpt_context.controllers import GptController
from gpt_context.services import ContextService, QAService, AppConfig
from gpt_context.stores.conversation_store import ConversationStore


async def main():
    config = AppConfig(os.environ)

    store = WeaviateVectorStoreAdapter(config, embedding=OpenAIEmbeddings())
    conversation_store = ConversationStore(config)
    context_service = ContextService(config, store)
    qa_service = QAService(config.OPENAI_MODEL, store, conversation_store)

    gpt_controller = GptController(qa_service, context_service)

    gpt_grpc_service = GptGrpcService(gpt_controller)
    health_check_service = HealthCheckGrpcService(context_service)

    server = Server([gpt_grpc_service, health_check_service])
    await server.start("0.0.0.0", config.PORT)
    print(f"Server started on {config.PORT}")
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
