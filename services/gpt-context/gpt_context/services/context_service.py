import os

from langchain.document_loaders import TextLoader, PDFMinerLoader, CSVLoader, GoogleDriveLoader
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document
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
                loader = self._get_file_loader(root, file)

                if loader is None:
                    print("No loader found")
                    return

                documents = loader.load()
                self._add_documents_to_store(documents)

    def clear_index(self) -> None:
        self.store.truncate()

    def add_google_docs(self, folder_id: str) -> None:
        credentials_path = os.path.join(os.getcwd(), "..", ".credentials/credentials.json")
        token_path = os.path.join(os.getcwd(), "..", ".credentials/token.json")

        loader = GoogleDriveLoader(
            credentials_path=credentials_path,
            token_path=token_path,
            folder_id=folder_id,
            recursive=False,
        )
        docs = loader.load()
        self._add_documents_to_store(docs)

    @staticmethod
    def _get_file_loader(root: str, file: str) -> BaseLoader:
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

    def _add_documents_to_store(self, documents: list[Document]) -> None:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        self.store.from_documents(texts)

