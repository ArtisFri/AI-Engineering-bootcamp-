"""Exercise 1: compare local models on speed and quality.

Run:  uv run python benchmark.py
Writes benchmark_results.json. Rating fields are left empty: fill in
quality_rating (1-5) and rating_note BY HAND after your final run.
Re-running overwrites the file, so rate last (the script refuses to overwrite
rated results unless you pass --force).
"""
import json
import subprocess
import sys
import time

from openai import OpenAI

import config

MODELS = ["qwen3.5:4b-q4_K_M", "qwen3.5:2b-q4_K_M"]
OUTPUT_FILE = "benchmark_results.json"
BENCH_MAX_TOKENS = 1024

ARTICLE = (
    "Remote work expanded rapidly after 2020, and many companies kept hybrid schedules "
    "once offices reopened. Employees report fewer commuting hours and more flexibility, "
    "but managers worry about mentoring junior staff and keeping teams connected. "
    "Several firms now require two or three office days per week, while others have "
    "closed offices entirely and invest in occasional in-person meetups instead."
)

CONTEXT_SNIPPET = (
    "Support tiers: The Standard plan includes email support during business hours. "
    "The Professional plan adds live chat and a 1 hour response time for critical issues."
)

PROMPTS = [
    {
        "category": "factual",
        "prompt": "What causes tides on Earth? Answer in 2-3 sentences.",
    },
    {
        "category": "reasoning",
        "prompt": (
            "If a train travels 120km in 1.5 hours, and then 80km in 1 hour, "
            "what is the average speed for the entire journey? Show the calculation briefly."
        ),
    },
    {
        "category": "summarization",
        "prompt": f"Summarize the following paragraph in exactly one sentence:\n\n{ARTICLE}",
    },
    {
        "category": "structured",
        "prompt": 'List 3 European capitals. Respond ONLY with valid JSON: [{"city": ..., "country": ...}]',
    },
    {
        "category": "code",
        "prompt": (
            "Write a Python function is_palindrome(s) that ignores case and non-alphanumeric "
            "characters. Return only the code in one code block, no explanation."
        ),
    },
    {
        "category": "instruction_following",
        "prompt": (
            "Write exactly 3 bullet points about the benefits of running AI models locally. "
            "Each bullet must start with '- ', be under 12 words, and contain no commas. "
            "Output nothing else."
        ),
    },
    {
        # Mirrors the RAG task: the answer is NOT in the context, so the right behaviour is to say so.
        "category": "grounded_unanswerable",
        "prompt": (
            f"Use ONLY the context below to answer. If the answer is not in the context, say "
            f'"I cannot find this information in the provided documents."\n\n'
            f"Context:\n{CONTEXT_SNIPPET}\n\nQuestion: What is the response time for the Enterprise plan?"
        ),
    },
]


def make_client() -> OpenAI:
    return OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY)


def chat(client: OpenAI, model: str, prompt: str):
    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=config.TEMPERATURE,
        reasoning_effort=config.REASONING_EFFORT,
        **{config.TOKEN_LIMIT_PARAM: BENCH_MAX_TOKENS},
    )


def run_benchmark(client: OpenAI, model: str, prompt_item: dict) -> dict:
    start = time.time()
    response = chat(client, model, prompt_item["prompt"])
    elapsed = time.time() - start
    choice = response.choices[0]
    usage = response.usage
    text = choice.message.content or ""

    if not text.strip():
        print(
            f"  WARNING: empty response from {model} on '{prompt_item['category']}' "
            f"(finish_reason={choice.finish_reason})"
        )

    completion_tokens = usage.completion_tokens if usage else None
    return {
        "model": model,
        "category": prompt_item["category"],
        "prompt": prompt_item["prompt"],
        "response": text,
        "thinking": config.REASONING_EFFORT != "none",
        "reasoning_effort": config.REASONING_EFFORT,
        "temperature": config.TEMPERATURE,
        "finish_reason": choice.finish_reason,
        "time_seconds": round(elapsed, 2),
        "prompt_tokens": usage.prompt_tokens if usage else None,
        "completion_tokens": completion_tokens,
        "tokens_per_second": round(completion_tokens / elapsed, 1) if completion_tokens else None,
        "quality_rating": None,
        "rating_note": "",
    }


def has_ratings(path: str) -> bool:
    try:
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    return any(r.get("quality_rating") is not None for r in rows)


def stop_model(model: str) -> None:
    """Best effort: free memory so only one LLM is loaded at a time."""
    try:
        subprocess.run(["ollama", "stop", model], capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        pass


def main() -> None:
    if has_ratings(OUTPUT_FILE) and "--force" not in sys.argv:
        print(
            f"{OUTPUT_FILE} already contains hand-entered ratings. "
            "Re-running would overwrite them. Pass --force if that is what you want."
        )
        sys.exit(1)

    client = make_client()
    results = []

    for model in MODELS:
        print(f"\n=== {model} (reasoning_effort={config.REASONING_EFFORT}) ===")
        # Warm-up call, not recorded: the first request includes loading the model into memory,
        # which would unfairly inflate the first prompt's time.
        print("  warming up (not recorded)...")
        chat(client, model, "Say OK.")

        for item in PROMPTS:
            print(f"  {item['category']}...")
            results.append(run_benchmark(client, model, item))

        stop_model(model)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {len(results)} rows to {OUTPUT_FILE}")
    print("Next: run `ollama ps` while a model is loaded, then rate each row by hand.")


if __name__ == "__main__":
    main()
