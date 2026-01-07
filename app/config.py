import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    COHERE_API_KEY = str(os.getenv("COHERE_API_KEY", ""))
    DOCUMENTS_DIR = "data/documents"
    VECTORSTORE_DIR = "data/vectorstore"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

settings = Settings()