from weaviate import Client as weaviateClient
from langchain.vectorstores.weaviate import Weaviate

from gpt_context.adapters.vector_store_adapter import VectorStoreAdapter
from gpt_context.exceptions.business_logic_exception import BusinessLogicException
from gpt_context.exceptions.errors import ErrorCode, ErrorMessage


class WeaviateVectorStoreAdapter(VectorStoreAdapter):
    def __init__(
            self,
            url="http://localhost:8080",
            index_name="Langchain",
            text_key="text",
            embedding=None,
            attributes=["source"]
    ):
        self.url = url
        self.index_name = index_name
        self.text_key = text_key
        self.embedding = embedding

        self._client = weaviateClient(url)
        self._weaviate = Weaviate(
            self._client,
            index_name,
            text_key,
            by_text=False,
            embedding=embedding,
            attributes=attributes
        )

    @property
    def db(self):
        return self._weaviate

    @property
    def retriever(self):
        return self._weaviate.as_retriever()

    def from_documents(self, documents, index_name, **kwargs):
        self._weaviate.from_documents(
            documents,
            self.embedding,
            weaviate_url=self.url,
            index_name=index_name,
            text_key=self.text_key,
        )

    def truncate(self, context_name: str):
        if not self.context_exists(context_name):
            raise BusinessLogicException(
                ErrorCode.NOT_FOUND,
                ErrorMessage.CONTEXT_NOT_FOUND.format(context_name=context_name)
            )

        query_result = self._client.query.get(context_name).with_additional(["id"]).do()
        ids = list(map(lambda x: x["_additional"]["id"], query_result["data"]["Get"][context_name]))

        for uuid in ids:
            self._client.data_object.delete(uuid, context_name)

    def context_exists(self, context_name: str) -> bool:
        return self._client.schema.exists(context_name)
