from abc import ABC, abstractmethod


class VectorStoreAdapter(ABC):
    @property
    @abstractmethod
    def db(self):
        pass

    @property
    @abstractmethod
    def retriever(self):
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
