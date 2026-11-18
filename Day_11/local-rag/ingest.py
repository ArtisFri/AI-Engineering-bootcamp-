"""Ingestion: PDFs -> text -> chunks -> local embeddings -> ChromaDB.

Run:   uv run python ingest.py
Debug: uv run python ingest.py --dump-text   (also writes the extracted text per PDF to extracted_text/)

Rebuilds the collection from scratch every run (so no duplicate chunks) and writes
ingest_report.json, the file to cite for chunk counts and sizes in the decision log.
"""
import json
import re
import sys
from pathlib import Path

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from pypdf import PdfReader

import config

try:
    from chromadb.errors import NotFoundError
except ImportError:  # older chromadb
    NotFoundError = Exception

EMBED_BATCH_SIZE = 32


def embed_texts(texts: list[str], prefix: str = "") -> list[list[float]]:
    """Embed texts with the local embedding model. Shared with retrieve.py."""
    client = OpenAI(base_url=config.EMBEDDING_BASE_URL, api_key=config.LLM_API_KEY)
    vectors = []
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = [prefix + t for t in texts[i : i + EMBED_BATCH_SIZE]]
        response = client.embeddings.create(model=config.EMBEDDING_MODEL, input=batch)
        vectors.extend(item.embedding for item in response.data)
    return vectors


def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]{2,}", "  ", text)  # layout mode pads with long runs of spaces
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_pages(pdf_path: Path) -> list[dict]:
    reader = PdfReader(str(pdf_path))
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        if config.EXTRACTION_MODE == "layout":
            raw = page.extract_text(extraction_mode="layout")
        else:
            raw = page.extract_text()
        text = clean_text(raw or "")
        if not text:
            print(f"  WARNING: no text on {pdf_path.name} page {number} (scanned image?)")
        pages.append({"source": pdf_path.name, "page": number, "text": text})
    return pages


def chunk_pages(pages: list[dict]) -> list[dict]:
    # Sizes are in CHARACTERS (RecursiveCharacterTextSplitter default length function).
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = []
    for page in pages:
        if not page["text"]:
            continue
        for index, piece in enumerate(splitter.split_text(page["text"])):
            chunks.append(
                {
                    # Stable ID: re-ingesting can never create duplicates.
                    "id": f"{page['source']}-p{page['page']}-c{index}",
                    "text": piece,
                    "source": page["source"],
                    "page": page["page"],
                    "chunk_index": index,
                }
            )
    return chunks


def main() -> None:
    dump_text = "--dump-text" in sys.argv
    pdf_paths = sorted(Path(config.DOCUMENTS_DIR).glob("*.pdf"))
    if not pdf_paths:
        print(f"No PDFs found in {config.DOCUMENTS_DIR}/. Put the five documents there.")
        sys.exit(1)

    all_chunks = []
    per_document = []
    for pdf_path in pdf_paths:
        print(f"Reading {pdf_path.name}")
        pages = load_pages(pdf_path)
        if dump_text:
            out_dir = Path("extracted_text")
            out_dir.mkdir(exist_ok=True)
            body = "\n\n".join(f"===== page {p['page']} =====\n{p['text']}" for p in pages)
            (out_dir / f"{pdf_path.stem}.txt").write_text(body, encoding="utf-8")
        chunks = chunk_pages(pages)
        per_document.append({"source": pdf_path.name, "pages": len(pages), "chunks": len(chunks)})
        all_chunks.extend(chunks)

    print(f"Embedding {len(all_chunks)} chunks with {config.EMBEDDING_MODEL}...")
    vectors = embed_texts([c["text"] for c in all_chunks], prefix=config.DOC_PREFIX)

    client = chromadb.PersistentClient(path=config.CHROMA_PATH)
    try:
        client.delete_collection(config.COLLECTION_NAME)
    except NotFoundError:
        pass
    collection = client.create_collection(
        name=config.COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )
    # Always pass embeddings explicitly so Chroma never embeds behind our back.
    for i in range(0, len(all_chunks), 100):
        batch = all_chunks[i : i + 100]
        collection.add(
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            embeddings=vectors[i : i + 100],
            metadatas=[
                {"source": c["source"], "page": c["page"], "chunk_index": c["chunk_index"]}
                for c in batch
            ],
        )

    lengths = [len(c["text"]) for c in all_chunks]
    report = {
        "embedding_model": config.EMBEDDING_MODEL,
        "embedding_dimensions": len(vectors[0]) if vectors else None,
        "extraction_mode": config.EXTRACTION_MODE,
        "chunk_size_characters": config.CHUNK_SIZE,
        "chunk_overlap_characters": config.CHUNK_OVERLAP,
        "documents": per_document,
        "total_pages": sum(d["pages"] for d in per_document),
        "total_chunks": len(all_chunks),
        "collection_count": collection.count(),
        "chunk_length_characters": {
            "min": min(lengths),
            "mean": round(sum(lengths) / len(lengths), 1),
            "max": max(lengths),
        }
        if lengths
        else None,
    }
    with open("ingest_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Stored {collection.count()} chunks in {config.CHROMA_PATH}/ (collection '{config.COLLECTION_NAME}')")
    print("Wrote ingest_report.json")


if __name__ == "__main__":
    main()
