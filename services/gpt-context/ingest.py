import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader, PDFMinerLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from constants import CHROMA_SETTINGS

load_dotenv()


def main():
    persist_directory = os.environ.get('PERSIST_DIRECTORY')

    if os.environ.get("OPENAI_API_KEY") is None:
        print("OpenAI API key not set")
        return None

    loader = None

    for root, dirs, files in os.walk("source_documents"):
        if not files:
            print(f"The directory '{root}' is empty.")
            continue

        for file in files:
            ext = os.path.splitext(file)[-1].lower()

            match ext:
                case ".txt":
                    loader = TextLoader(os.path.join(root, file), encoding="utf8")
                case ".pdf":
                    loader = PDFMinerLoader(os.path.join(root, file))
                case ".csv":
                    loader = CSVLoader(os.path.join(root, file))

    if loader is None:
        print("No loader found")
        return None

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    openai = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, openai, persist_directory=persist_directory, client_settings=CHROMA_SETTINGS)
    db.persist()
    print("All files loaded")


if __name__ == "__main__":
    main()
