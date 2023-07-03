from weaviate import Client as weaviateClient
from langchain.vectorstores.weaviate import Weaviate

from gpt_context.adapters.vector_store_adapter import VectorStoreAdapter


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

        self._client = weaviateClient(url)
        self._weaviate = Weaviate(
            self._client,
            index_name,
            text_key,
            by_text=False,
            embedding=embedding,
            attributes=["source"]
        )

    @property
    def db(self):
        return self._weaviate

    @property
    def retriever(self):
        return self._weaviate.as_retriever()

    def from_documents(self, documents, embeddings, **kwargs):
        self._weaviate.from_documents(
            documents,
            embeddings,
            weaviate_url=self.url,
            index_name=self.index_name,
            text_key=self.text_key,
        )

    def truncate(self):
        query_result = self._client.query.get(self.index_name).with_additional(["id"]).do()
        ids = list(map(lambda x: x["_additional"]["id"], query_result["data"]["Get"]["Langchain"]))

        for uuid in ids:
            self._client.data_object.delete(uuid, self.index_name)
