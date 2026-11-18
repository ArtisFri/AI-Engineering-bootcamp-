"""Retrieval: embed the query locally, search ChromaDB, return chunks plus metadata.

Try it:  uv run python retrieve.py "What is the maximum number of remote work days per week?"
"""
import sys
import time

import chromadb

import config
from ingest import embed_texts

_collection = None


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=config.CHROMA_PATH)
        _collection = client.get_collection(config.COLLECTION_NAME)
    return _collection


def retrieve_chunks(query: str, top_k: int = config.TOP_K) -> dict:
    # retrieval_time_ms covers embedding the query AND the vector search.
    start = time.perf_counter()
    query_vector = embed_texts([query], prefix=config.QUERY_PREFIX)[0]
    results = get_collection().query(
        query_embeddings=[query_vector],  # always explicit: Chroma must not embed on its own
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    elapsed_ms = (time.perf_counter() - start) * 1000

    chunks = []
    for content, meta, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        chunks.append(
            {
                "content": content,
                "source": meta["source"],
                "page": meta["page"],
                # Collection uses cosine distance, so 1 - distance is a cosine similarity.
                "relevance_score": round(1 - distance, 4),
            }
        )

    return {
        "query": query,
        "retrieved_chunks": chunks,
        "retrieval_time_ms": round(elapsed_ms, 1),
        "embedding_model": config.EMBEDDING_MODEL,
    }


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "What is the maximum number of remote work days per week?"
    result = retrieve_chunks(question)
    print(f"Query: {result['query']}")
    print(f"{len(result['retrieved_chunks'])} chunks in {result['retrieval_time_ms']} ms\n")
    for rank, chunk in enumerate(result["retrieved_chunks"], start=1):
        print(f"[{rank}] {chunk['source']} p.{chunk['page']}  score={chunk['relevance_score']}")
        print(chunk["content"])
        print("-" * 60)
