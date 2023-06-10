from langchain.vectorstores.redis import Redis

from adapters.vector_store_adapter import VectorStoreAdapter


class RedisStoreAdapter(VectorStoreAdapter):
    def __init__(
            self,
            url="redis://localhost:6379",
            index_name="link",
            embedding=None,
    ):
        self.url = url
        self.index_name = index_name
        self._db = Redis(redis_url=url, index_name=index_name, embedding_function=embedding.embed_query)

    @property
    def db(self):
        return self._db

    @property
    def retriever(self):
        return self._db.as_retriever()

    def from_documents(self, documents, embeddings, **kwargs):
        return self._db.from_documents(documents, embeddings, **kwargs)
