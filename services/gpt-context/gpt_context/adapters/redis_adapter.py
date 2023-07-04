from langchain.vectorstores.redis import Redis

from gpt_context.adapters.vector_store_adapter import VectorStoreAdapter


class RedisStoreAdapter(VectorStoreAdapter):
    def __init__(
            self,
            url="redis://localhost:6379",
            index_name="link",
            embedding=None,
    ):
        self.url = url
        self.index_name = index_name
        self.embedding = embedding
        self.vector_db = Redis.from_existing_index(redis_url=url, index_name=index_name, embedding=embedding)

    @property
    def db(self):
        return self.vector_db

    @property
    def retriever(self):
        return self.vector_db.as_retriever()

    def from_documents(self, documents, **kwargs):
        return self.vector_db.from_documents(documents, self.embedding, **kwargs)
