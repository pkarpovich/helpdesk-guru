from abc import ABC, abstractmethod


class VectorStoreAdapter(ABC):
    @abstractmethod
    def get_retriever(self, index_name: str):
        pass

    @abstractmethod
    def from_documents(self, documents, index_name, **kwargs):
        pass

    @abstractmethod
    def truncate(self, context_name: str):
        pass

    @abstractmethod
    def context_exists(self, context_name: str) -> bool:
        pass
