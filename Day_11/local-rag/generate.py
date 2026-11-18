"""Generation: retrieved chunks + question -> answer from the local LLM (OpenAI-compatible API).

The full context sent to the model is returned alongside the answer, so evaluation can see
exactly what the model saw.
"""
import time

from openai import OpenAI

import config


def build_context(chunks: list[dict]) -> str:
    # Each chunk is labelled with its source and page, so the model can point to where it read something.
    parts = [
        f"[Source: {c['source']}, page {c['page']}]\n{c['content']}" for c in chunks
    ]
    return "\n\n".join(parts)


def generate_answer(query: str, chunks: list[dict]) -> dict:
    context = build_context(chunks)
    client = OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY)

    start = time.perf_counter()
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": config.SYSTEM_PROMPT.format(context=context)},
            {"role": "user", "content": query},
        ],
        temperature=config.TEMPERATURE,
        reasoning_effort=config.REASONING_EFFORT,
        **{config.TOKEN_LIMIT_PARAM: config.MAX_TOKENS},
    )
    elapsed_ms = (time.perf_counter() - start) * 1000

    choice = response.choices[0]
    usage = response.usage
    answer = (choice.message.content or "").strip()

    if not answer:
        print(
            f"  WARNING: EMPTY ANSWER for '{query[:60]}' "
            f"(finish_reason={choice.finish_reason}). Thinking may have used the token cap."
        )
    elif "</think>" in answer or "<think>" in answer:
        print(f"  WARNING: reasoning text leaked into the answer for '{query[:60]}'.")
    if choice.finish_reason == "length":
        print(f"  WARNING: answer was cut off at the token cap ({config.MAX_TOKENS}).")

    return {
        "query": query,
        "answer": answer,
        "context_used": context,
        "model": config.LLM_MODEL,
        "thinking": config.REASONING_EFFORT != "none",
        "reasoning_effort": config.REASONING_EFFORT,
        "finish_reason": choice.finish_reason,
        "generation_time_ms": round(elapsed_ms, 1),
        "prompt_tokens": usage.prompt_tokens if usage else None,
        "tokens_generated": usage.completion_tokens if usage else None,
    }
