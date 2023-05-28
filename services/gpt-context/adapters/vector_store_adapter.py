from abc import ABC, abstractmethod

class VectorStoreAdapter(ABC):
    @property
    @abstractmethod
    def db(self):
        pass

    @abstractmethod
    def from_documents(self, documents, embeddings, **kwargs):
        pass