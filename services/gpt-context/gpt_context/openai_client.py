from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models.openai import ChatOpenAI

from gpt_context.adapters.vector_store_adapter import VectorStoreAdapter
from prompt import qa_prompt


class OpenaiClient:
    def __init__(self, model_name: str, store: VectorStoreAdapter):
        callbacks = [StreamingStdOutCallbackHandler()]

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        model = ChatOpenAI(model_name=model_name, callbacks=callbacks, verbose=True, temperature=0.7)

        question_generator = LLMChain(llm=model, prompt=CONDENSE_QUESTION_PROMPT)
        combine_docs_chain = load_qa_chain(model, chain_type="stuff", prompt=qa_prompt)

        self.qa = ConversationalRetrievalChain(
            memory=self.memory,
            retriever=store.retriever,
            question_generator=question_generator,
            combine_docs_chain=combine_docs_chain,
        )

    def ask(self, query: str) -> str:
        res = self.qa({"question": query})

        return res["answer"]

    def clear_history(self):
        self.memory.clear()
