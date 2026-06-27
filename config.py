import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

LLM_MODEL="gemini-2.5-flash"

VECTOR_DB_PATH="vector_db/index.faiss"

CHUNK_PATH="vector_db/chunks.pkl"

TOP_K = 5

SIMILARITY_THRESHOLD = 0.50