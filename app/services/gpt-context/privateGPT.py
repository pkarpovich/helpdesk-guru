import langchain
import os

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.cache import GPTCache
from constants import CHROMA_SETTINGS
from gptcache.adapter.api import init_similar_cache


load_dotenv()

persist_directory = os.environ.get('PERSIST_DIRECTORY')
model_name = os.environ.get('OPENAI_MODEL')


def main():
    if os.environ.get("OPENAI_API_KEY") is None:
        print("OpenAI API key not set")
        return None

    openai = OpenAIEmbeddings()
    db = Chroma(persist_directory=persist_directory, embedding_function=openai, client_settings=CHROMA_SETTINGS)
    retriever = db.as_retriever()
    callbacks = [StreamingStdOutCallbackHandler()]

    llm = ChatOpenAI(model_name=model_name, callbacks=callbacks)
    langchain.llm_cache = GPTCache(init_func=lambda cache_obj: init_similar_cache(cache_obj=cache_obj))
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
    while True:
        query = input("\nEnter a query: ")
        if query == "exit":
            break
        
        res = qa(query)
        answer, _ = res['result'], res['source_documents']

        print("\n\n> Question:")
        print(query)
        print("\n> Answer:")
        print(answer)


if __name__ == "__main__":
    main()
