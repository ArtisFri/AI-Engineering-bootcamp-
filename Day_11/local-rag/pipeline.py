"""End-to-end pipeline: question -> retrieve -> generate -> answer.

One question:   uv run python pipeline.py "What is the maximum number of remote work days per week?"
All questions:  uv run python pipeline.py
                (reads test_questions.json, writes pipeline_outputs.json)

Fill in `passed` and `rating_note` BY HAND after your final run. Re-running overwrites the file,
so rate last (the script refuses to overwrite rated rows unless you pass --force).
"""
import json
import sys
import time

import config
from generate import generate_answer
from retrieve import retrieve_chunks

QUESTIONS_FILE = "test_questions.json"
OUTPUT_FILE = "pipeline_outputs.json"


def answer_question(query: str) -> dict:
    retrieval_result = retrieve_chunks(query)
    generation_result = generate_answer(
        query=query, chunks=retrieval_result["retrieved_chunks"]
    )
    return {
        **generation_result,
        "retrieval": retrieval_result,
    }


def build_row(item: dict, result: dict) -> dict:
    chunks = result["retrieval"]["retrieved_chunks"]
    return {
        "id": item["id"],
        "question": item["question"],
        "expected_answer": item["expected_answer"],
        "actual_answer": result["answer"],
        "retrieved_context": [c["content"] for c in chunks],
        "context_sources": [
            {"source": c["source"], "page": c["page"], "score": c["relevance_score"]}
            for c in chunks
        ],
        "model": result["model"],
        "thinking": result["thinking"],
        "finish_reason": result["finish_reason"],
        "embedding_model": result["retrieval"]["embedding_model"],
        "top_k": config.TOP_K,
        "prompt_tokens": result["prompt_tokens"],
        "tokens_generated": result["tokens_generated"],
        "retrieval_time_ms": result["retrieval"]["retrieval_time_ms"],
        "generation_time_ms": result["generation_time_ms"],
        "passed": None,
        "rating_note": "",
    }


def has_ratings(path: str) -> bool:
    try:
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    return any(r.get("passed") is not None or r.get("rating_note") for r in rows)


def save(rows: list[dict]) -> None:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)


def run_all() -> None:
    if has_ratings(OUTPUT_FILE) and "--force" not in sys.argv:
        print(
            f"{OUTPUT_FILE} already contains hand-entered ratings. "
            "Re-running would overwrite them. Pass --force if that is what you want."
        )
        sys.exit(1)

    with open(QUESTIONS_FILE, encoding="utf-8") as f:
        questions = json.load(f)

    rows = []
    started = time.time()
    for i, item in enumerate(questions, start=1):
        print(f"[{i}/{len(questions)}] {item['id']}: {item['question']}")
        result = answer_question(item["question"])
        rows.append(build_row(item, result))
        save(rows)  # saved after every question, so a crash or Ctrl+C loses nothing
        print(f"  finish_reason={result['finish_reason']}, prompt_tokens={result['prompt_tokens']}")

    print(f"\nWrote {len(rows)} rows to {OUTPUT_FILE} in {round(time.time() - started)} s")
    print("Next: read each actual_answer against expected_answer, then set passed and rating_note by hand.")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        result = answer_question(" ".join(args))
        print("\n--- Retrieved ---")
        for c in result["retrieval"]["retrieved_chunks"]:
            print(f"{c['source']} p.{c['page']}  score={c['relevance_score']}")
        print("\n--- Answer ---")
        print(result["answer"])
        print(
            f"\n(finish_reason={result['finish_reason']}, prompt_tokens={result['prompt_tokens']}, "
            f"generated={result['tokens_generated']}, generation={result['generation_time_ms']} ms)"
        )
    else:
        run_all()


if __name__ == "__main__":
    main()
