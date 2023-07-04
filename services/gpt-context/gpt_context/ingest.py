import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings

from gpt_context.adapters import WeaviateVectorStoreAdapter
from gpt_context.services.context_service import ContextService

load_dotenv()


def main():
    if os.environ.get("OPENAI_API_KEY") is None:
        print("OpenAI API key not set")
        return None

    weaviate_url = os.environ.get("WEAVIATE_URL") or "http://localhost:8080"

    store = WeaviateVectorStoreAdapter(
        url=weaviate_url,
        embedding=OpenAIEmbeddings()
    )
    context_service = ContextService(store)
    context_service.init()

    print("All files loaded")


if __name__ == "__main__":
    main()
