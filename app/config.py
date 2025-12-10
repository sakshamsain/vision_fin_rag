from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

QDRANT_URL = "http://localhost"
QDRANT_PORT = 6333
QDRANT_COLLECTION = "financial_pages"

COLPALI_MODEL_NAME = "vidore/colpali-v1.2"  # adjust if needed

# Dummy LLM endpoint (replace with real later)
LLM_API_URL = "http://localhost:11434"  # e.g., ollama
LLM_MODEL_NAME = "llama3.2"
