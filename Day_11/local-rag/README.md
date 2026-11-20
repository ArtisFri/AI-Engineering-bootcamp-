# Local Document Q&A (RAG) with Ollama

A document question-answering pipeline that runs entirely on local infrastructure. Documents are
parsed, chunked, embedded with a local model, stored in ChromaDB, and answered by a local LLM through
Ollama's OpenAI-compatible API. No document text leaves the machine.

Built for the Day 11 capstone. The reasoning behind every choice is in `decision_log.md`.

## AI assistant used

Claude (model: Claude Sonnet 5.5), in the Claude chat app, helped write the code. The model inside the
pipeline is a local Ollama model (`qwen3.5:4b-q4_K_M`, no cloud tag).

## Requirements

- Windows (the commands below are PowerShell), macOS or Linux
- [Ollama](https://ollama.com/download), installed natively (not inside WSL on Windows)
- Python 3.11 or newer and [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- About 16 GB of RAM for the main model plus the embedding model

## Setup

1. **Models**

   ```powershell
   ollama pull qwen3.5:4b-q4_K_M
   ollama pull qwen3.5:2b-q4_K_M
   ollama pull nomic-embed-text
   ```

2. **Context window of 8192.** Add a user environment variable `OLLAMA_CONTEXT_LENGTH` = `8192`, quit
   Ollama from the tray and start it again. Then check that `ollama ps` shows `CONTEXT 8192` while a
   model is loaded.

3. **Python environment**

   ```powershell
   uv sync
   ```

4. **Documents.** Put the five PDFs in `documents/`.

5. **Check that Ollama answers**

   ```powershell
   uv run python test_api.py
   ```

   It should print one sentence and `stop`.

## Rebuild the vector database

`chroma_db/` is not committed. This one command rebuilds it from `documents/`:

```powershell
uv run python ingest.py
```

It deletes and recreates the collection each time (no duplicate chunks) and writes `ingest_report.json`.
Add `--dump-text` to also write the extracted text of each PDF to `extracted_text/`, so you can check
how tables came out.

## Run the pipeline

One question:

```powershell
uv run python pipeline.py "What uptime SLA does the Enterprise tier guarantee?"
```

It prints the retrieved sources, the answer, `finish_reason`, `prompt_tokens` and timings.

All test questions (reads `test_questions.json`, writes `pipeline_outputs.json`):

```powershell
uv run python pipeline.py
```

This takes a while on a CPU-only laptop. The file is saved after every question. The script refuses
to overwrite a file that already contains hand-entered ratings unless you pass `--force`.

## Other scripts

| Command | What it does | Writes |
|---|---|---|
| `uv run python benchmark.py` | Compares two local models on 7 prompts (speed, quality) | `benchmark_results.json` |
| `uv run python compare_retrieval.py` | Checks, for several values of top-K, whether the expected pages are retrieved (retrieval only, no LLM) | `retrieval_by_k.json` |
| `uv run python summarize_results.py` | Computes the figures for the decision log from the saved result files | `results_summary.json` |
| `uv run python retrieve.py "question"` | Shows the retrieved chunks for one query | nothing |

## Configuration

Everything is set in `config.py`. Chunk size and overlap are in **characters**. The LLM provider, model
and a few parameters can be changed with environment variables, with no code change:

| Variable | Meaning | Default |
|---|---|---|
| `LLM_BASE_URL` | OpenAI-compatible endpoint | `http://localhost:11434/v1` |
| `LLM_API_KEY` | API key | `ollama` |
| `LLM_MODEL` | Chat model | `qwen3.5:4b-q4_K_M` |
| `REASONING_EFFORT` | Thinking setting passed on every chat call | `none` |
| `TOKEN_LIMIT_PARAM` | Name of the token-cap parameter (`max_tokens` for Ollama, `max_completion_tokens` for the Day 12 cloud model) | `max_tokens` |
| `EMBEDDING_MODEL`, `EMBEDDING_BASE_URL` | Embeddings stay local | `nomic-embed-text`, local Ollama |
| `EXTRACTION_MODE` | pypdf extraction mode, `layout` or `plain` | `layout` |

Swapping to a cloud model (Day 12) changes only these variables, for example:

```powershell
$env:LLM_BASE_URL = "https://<resource>.openai.azure.com/openai/v1/"
$env:LLM_API_KEY = $env:AZURE_OPENAI_API_KEY
$env:LLM_MODEL = "gpt-5.6-luna"
$env:TOKEN_LIMIT_PARAM = "max_completion_tokens"
```

Set variables in the same PowerShell window that runs the script. They do not carry over to a new
window. If you change chunking or the embedding model, re-run `ingest.py` first.

## Project layout

```
config.py              all configuration
ingest.py              PDF loading, chunking, embedding, storage in ChromaDB
retrieve.py            embeds the query, searches ChromaDB, returns chunks with metadata
generate.py            builds the prompt from chunks, calls the LLM, returns the answer and its context
pipeline.py            question -> retrieve -> generate; runs the test set
benchmark.py           model comparison (Exercise 1)
compare_retrieval.py   top-K comparison, retrieval only
summarize_results.py   figures for the decision log, computed from the result files
test_questions.json    test questions with expected answers and source pages
benchmark_results.json model comparison results, quality ratings entered by hand
pipeline_outputs.json  pipeline run over all test questions, `passed` entered by hand
decision_log.md        written by hand
AGENTS.md              rules for AI assistants working in this repository
documents/             the PDFs
chroma_db/             vector store (not committed, rebuilt by ingest.py)
```

## Rules this project follows

- Local models only. No cloud-tagged Ollama models.
- Every number in the decision log comes from a file written by code
  (`benchmark_results.json`, `pipeline_outputs.json`, `ingest_report.json`, `retrieval_by_k.json` or
  `results_summary.json`). Ratings (`quality_rating`, `passed`, `rating_note`) are entered by hand after
  the final run.
