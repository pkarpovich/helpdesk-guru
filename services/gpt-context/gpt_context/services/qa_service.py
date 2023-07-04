from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from gpt_context.adapters.vector_store_adapter import VectorStoreAdapter
from gpt_context.services.prompts.qa_prompt import qa_prompt

callbacks = [StreamingStdOutCallbackHandler()]


class QAService:
    def __init__(self, model_name: str, store: VectorStoreAdapter):
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        llm = ChatOpenAI(model_name=model_name, callbacks=callbacks, verbose=True, temperature=0.7)

        question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
        combine_docs_chain = load_qa_chain(llm, chain_type="stuff", prompt=qa_prompt)

        self.qa = ConversationalRetrievalChain(
            memory=self.memory,
            retriever=store.retriever,
            question_generator=question_generator,
            combine_docs_chain=combine_docs_chain,
        )

    def ask(self, query: str) -> str:
        res = self.qa({"question": query})

        return res["answer"]

    def clear_history(self) -> None:
        self.memory.clear()