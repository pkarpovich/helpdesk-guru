from weaviate import Client as weaviateClient
from langchain.vectorstores.weaviate import Weaviate

from adapters.vector_store_adapter import VectorStoreAdapter

class WeaviateVectorStoreAdapter(VectorStoreAdapter):
    def __init__(
            self,
            url="http://localhost:8080",
            index_name="Langchain",
            text_key="text",
            embedding=None,
    ):
        self.url = url
        self.index_name = index_name
        self.text_key = text_key

        client = weaviateClient(url)
        self._weaviate = Weaviate(
            client,
            index_name,
            text_key,
            by_text=False,
            embedding=embedding,
            attributes=["source"]
        )

    @property
    def db(self):
        return self._weaviate

    def from_documents(self, documents, embeddings, **kwargs):
        self._weaviate.from_documents(
            documents,
            embeddings,
            weaviate_url=self.url,
            index_name=self.index_name,
            text_key=self.text_key,
        )