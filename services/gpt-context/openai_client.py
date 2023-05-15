import langchain

from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.cache import GPTCache
from constants import CHROMA_SETTINGS
from gptcache.adapter.api import init_similar_cache


class OpenaiClient:
    def __init__(self, persist_directory: str, model_name: str):
        embedding = OpenAIEmbeddings()
        db = Chroma(persist_directory=persist_directory, embedding_function=embedding, client_settings=CHROMA_SETTINGS)
        retriever = db.as_retriever()
        callbacks = [StreamingStdOutCallbackHandler()]

        llm = ChatOpenAI(model_name=model_name, callbacks=callbacks)
        langchain.llm_cache = GPTCache(init_func=lambda cache_obj: init_similar_cache(cache_obj=cache_obj))

        self.qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                              return_source_documents=True)

    def ask(self, query: str) -> str:
        res = self.qa(query)
        return res['result']
