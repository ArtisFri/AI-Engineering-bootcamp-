# Decision Log: Local RAG Pipeline

<!-- Skeleton only. Write every section yourself, from what you saw.
     Every number must name its file (benchmark_results.json, pipeline_outputs.json,
     ingest_report.json or results_summary.json) and, where it helps, the question id or model.
     Delete these comments when you are done. -->

## Machine
- **Hardware:** [intel core i5-10310U CPU 1.70GHz, 16 gbs ram, native Ollama ]<!-- CPU, RAM, GPU if any; native Ollama or WSL -->
- **`ollama ps` with my main model loaded:**
 NAME                       ID              SIZE      PROCESSOR    CONTEXT    RUNNER      UNTIL
qwen3.5:4b-q4_K_M          d8b0f5e9760c    3.4 GB    100% CPU     8192       llamacpp    4 minutes from now
nomic-embed-text:latest    0a109f422b47    389 MB    100% CPU     2048       llamacpp    3 minutes from now <!-- paste the output: name, size, processor, context -->

## Model Selection
- **Chosen LLM:** qwen3.5:4b-q4_K_M    <!-- exact model tag -->
- **Thinking:**  thinking off, the result was not different enough for addition computing power
- **Why:** qwen3.5:4b-q4_K_M was compared to qwen3.5:2b-q4_K_M and the answers ware of the same quality, but chose qwen3.5:4b-q4_K_M out of precousion.
- **What I considered but rejected:** only qwen3.5:2b-q4_K_M<!-- other models and why -->

## Embedding Model
- **Chosen:** nomic-embed-text:latest ,768 <!-- model name, vector dimensions (ingest_report.json) -->
- **Why:** there ware no other embedding models, so no comparison. <!-- did you compare? what was the tradeoff? -->

## Parsing
- **Extractor:** i used EXTRACTION_MODE = os.getenv("EXTRACTION_MODE", "layout") and from extracted_text\product_guide.txt page 14.
<!-- which, and what one page with a table looked like after extraction (extracted_text/) -->
If NovaTech fails to meet the uptime commitment, customers are eligible for
service credits:

  Uptime Achieved  Starter Credit  Professional Credit  Enterprise Credit

  99.0% - 99.49%  5%  —  —

  98.0% - 99.89%  —  10%  —

  99.9% - 99.94%  —  —  10%

  95.0% - 98.99%  —  15%  —

  99.0% - 99.89%  —  —  20%

  Below 95.0%  10%  25%  30%

  Below 99.0%  —  —  30%

and 

7.3 Support Response Times

  Severity  Starter  Professional  Enterprise

  Critical (service down)  4 hours  1 hour  15 minutes

  High (major feature broken)  8 hours  2 hours  30 minutes

  Medium (minor feature issue)  24 hours  8 hours  2 hours

  Low (question / enhancement)  72 hours  24 hours  8 hours

## Chunking Strategy
- **Chunk size:** CHUNK_SIZE = 800 characters
<!-- value and unit: characters or tokens -->
- **Overlap:** CHUNK_OVERLAP = 150
<!-- value and unit -->
- **Why:** started with 512 characters with 50 overlap. ingest_report.json showed a minimum chunk length of 1, which led to the MIN_CHUNK_CHARS filter. The 512-character chunks split section 7.3 (the response-times table and the hours paragraph) from its heading and its first rows. The Critical row never appeared in the top 5. Tried 1000 with 150 overlap on the same query. The hours paragraph dropped from rank 1 to rank 3, and the irrelevant tables still outranked the rest, so it wasn’t an improvement.
Chose 800 with 150. In later run, both the p.14 chunk and the p.28 channels table were retrieved for that query.
<!-- did you experiment? what happened with other values? -->

## Retrieval Configuration
- **Top-K:**TOP_K = 10
 <!-- value -->
- **Context window:** 8192 <!-- value from ollama ps; prompt_tokens observed at this K (results_summary.json) -->
- **Why:** I tried 5 and then 10. At 512 characters, K=5 (the first run) Rank 1 was the p.14 paragraph about 24/7 support and the extended hours (score 0.7622). Ranks 2 to 5 were irrelevant tables. At 1000 characters, K=5, then K=10 (the clean K comparison). With K=5, the top 5 were weaker than before: the hours paragraph dropped to rank 3 and two quarterly-report chunks entered. With K=10, ranks 1 to 5 were identical, because a larger K just adds ranks 6 to 10. The extra five included the p.28 chunk with the “13.3 Support Channels” table at rank 10 (score 0.6769).At 800 characters, K=10 in its context_sources, p.14 is at rank 1 and the p.28 channels table is at rank 9. So at K=5 the channels table would not have been included.
<!-- did you try other values? what was the impact? -->

## Observations
- **What worked well:**q02, q04, q05, q11, q17, q19 and q20 passed and mathematical problems were a highlight, becouse of the chain of reasoning why it did thing that it did, also when information was not in the documents it said so clearly. <!-- specific examples, with question ids from pipeline_outputs.json -->
- **What failed:** When there ware conflict between documents , those often ware not addresed. And answer given based on data from a different table <!-- which questions went wrong and why? retrieval miss or generation error? -->
- **Traps I hit:** a 1-character chunk in the first ingest report,first query that was much slower than the rest.<!-- what you saw, what you did -->
- **Local vs cloud expectations:** I would expect cloud would be better and more powerful in resolving conflicts between documents.<!-- how do you think a cloud model would compare on this task? -->

## If I Had More Time / Better Hardware
- <!-- what would you change? -->
I probably would choose a more powerful model, implement /test different chunking methods.
