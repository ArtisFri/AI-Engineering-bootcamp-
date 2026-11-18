import os

# --- LLM (swap to cloud with environment variables only) ---
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3.5:4b-q4_K_M")

# --- Embeddings (stay local, even in the Day 12 cloud swap) ---
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "http://localhost:11434/v1")

# --- Documents and vector store ---
DOCUMENTS_DIR = "documents"
CHROMA_PATH = "chroma_db"
# pypdf extraction: "layout" keeps table rows on one line, "plain" is pypdf's default.
EXTRACTION_MODE = os.getenv("EXTRACTION_MODE", "layout")
# nomic-embed-text was trained with task prefixes; use the same ones at ingest and query time.
DOC_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "

# --- Chunking and retrieval ---
# CHUNK_SIZE and CHUNK_OVERLAP are in CHARACTERS (RecursiveCharacterTextSplitter), not tokens.
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 10
COLLECTION_NAME = "bootcamp_docs"
MIN_CHUNK_CHARS = 30
# --- Generation ---
SYSTEM_PROMPT = """You are a helpful assistant answering questions based on provided context.
Use ONLY the context below to answer. If the answer is not in the context, say "I cannot find this information in the provided documents."

Context:
{context}
"""
TEMPERATURE = 0.3
REASONING_EFFORT = os.getenv("REASONING_EFFORT", "none")
MAX_TOKENS = 1024
# Ollama reads only "max_tokens"; the Day 12 cloud model wants "max_completion_tokens".
TOKEN_LIMIT_PARAM = os.getenv("TOKEN_LIMIT_PARAM", "max_tokens")
