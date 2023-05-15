import os
from dotenv import load_dotenv
from chromadb.config import Settings


load_dotenv()

PERSIST_DIRECTORY = os.environ.get('PERSIST_DIRECTORY')

CHROMA_SETTINGS = Settings(
        chroma_db_impl='duckdb+parquet',
        persist_directory=PERSIST_DIRECTORY,
        anonymized_telemetry=False
)
