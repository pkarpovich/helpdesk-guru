import langchain

from langchain.cache import RedisSemanticCache
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models.openai import ChatOpenAI

from adapters.redis_adapter import RedisStoreAdapter
from prompt import qa_prompt


class OpenaiClient:
    def __init__(self, model_name: str):
        embedding = OpenAIEmbeddings()

        langchain.llm_cache = RedisSemanticCache(
            redis_url="redis://localhost:6379",
            embedding=embedding,
        )

        callbacks = [StreamingStdOutCallbackHandler()]

        model = ChatOpenAI(model_name=model_name, callbacks=callbacks, temperature=0.7, verbose=True)

        vector_store = RedisStoreAdapter(embedding=embedding)

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        question_generator = LLMChain(llm=model, prompt=CONDENSE_QUESTION_PROMPT)
        combine_docs_chain = load_qa_chain(model, chain_type="stuff", prompt=qa_prompt)

        self.qa = ConversationalRetrievalChain(
            memory=self.memory,
            retriever=vector_store.retriever,
            question_generator=question_generator,
            combine_docs_chain=combine_docs_chain,
        )

    def ask(self, query: str) -> str:
        res = self.qa({"question": query})

        return res["answer"]
