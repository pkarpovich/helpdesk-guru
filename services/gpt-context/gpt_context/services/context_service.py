import os

from langchain.document_loaders import TextLoader, PDFMinerLoader, CSVLoader
from langchain.document_loaders.base import BaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from gpt_context.adapters.vector_store_adapter import VectorStoreAdapter


class ContextService:
    def __init__(self, store: VectorStoreAdapter):
        self.store = store

    def init(self) -> None:
        for root, _, files in os.walk("source_documents"):
            if not files:
                print(f"The directory '{root}' is empty.")
                return

            for file in files:
                loader = self._get_loader_for_file(root, file)

                if loader is None:
                    print("No loader found")
                    return

                documents = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                texts = text_splitter.split_documents(documents)

                self.store.from_documents(texts)

    def clear_index(self) -> None:
        self.store.truncate()

    @staticmethod
    def _get_loader_for_file(root: str, file: str) -> BaseLoader:
        ext = os.path.splitext(file)[-1].lower()
        loader = None

        match ext:
            case ".txt":
                loader = TextLoader(os.path.join(root, file), encoding="utf8")
            case ".pdf":
                loader = PDFMinerLoader(os.path.join(root, file))
            case ".csv":
                loader = CSVLoader(os.path.join(root, file))

        return loader
