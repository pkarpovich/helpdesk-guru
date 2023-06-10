import langchain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models.openai import ChatOpenAI
from langchain.cache import RedisSemanticCache

from adapters.redis_adapter import RedisStoreAdapter


class OpenaiClient:
    def __init__(self, model_name: str):
        embedding = OpenAIEmbeddings()

        # langchain.llm_cache = RedisSemanticCache(
        #     redis_url="redis://localhost:6379",
        #     embedding=embedding,
        # )

        callbacks = [StreamingStdOutCallbackHandler()]

        llm = ChatOpenAI(model_name=model_name, callbacks=callbacks, temperature=0.7)

        vector_store = RedisStoreAdapter(embedding=embedding)

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.qa = ConversationalRetrievalChain.from_llm(llm, vector_store.retriever, memory=self.memory)

    def ask(self, query: str) -> str:
        res = self.qa({"question": query})

        return res["answer"]
