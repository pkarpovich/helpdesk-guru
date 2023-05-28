from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings

from adapters.weaviate_adapter import WeaviateVectorStoreAdapter


class OpenaiClient:
    def __init__(self, model_name: str):
        callbacks = [StreamingStdOutCallbackHandler()]

        llm = ChatOpenAI(model_name=model_name, callbacks=callbacks, temperature=0.2)
        embedding = OpenAIEmbeddings()

        vector_store = WeaviateVectorStoreAdapter(embedding=embedding)
        db = vector_store.db

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.qa = ConversationalRetrievalChain.from_llm(llm, db.as_retriever(), memory=self.memory)

    def ask(self, query: str) -> str:
        res = self.qa({"question": query})

        return res["answer"]
