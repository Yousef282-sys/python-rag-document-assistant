from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

CHROMA_PATH = PROJECT_ROOT / "backend" / "data" / "vector_store" / "chroma_db_v2"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "python_tutorial_v2"

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen3:4b"

TOP_K = 3
