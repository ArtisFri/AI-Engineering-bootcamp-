| Metric | n | Local mean ± 2×SE | Cloud mean ± 2×SE | Cloud − local (mean ± 2×SE) | Verdict |
|---|---|---|---|---|---|
| Contextual Relevancy | 20 | 0.201 ± 0.071 | 0.200 ± 0.072 | -0.001 ± 0.024 | no clear difference |
| Contextual Recall | 20 | 0.833 ± 0.147 | 0.808 ± 0.150 | -0.025 ± 0.081 | no clear difference |
| Contextual Precision | 20 | 0.818 ± 0.114 | 0.819 ± 0.113 | +0.000 ± 0.020 | no clear difference |
| Faithfulness | 20 | 0.689 ± 0.170 | 0.739 ± 0.197 | +0.050 ± 0.118 | no clear difference |
| Answer Relevancy | 20 | 0.972 ± 0.044 | 0.938 ± 0.075 | -0.035 ± 0.088 | no clear difference |

| Run | Questions | Median generation time (s) | Slowest (s) | Mean tokens generated | Empty answers | finish_reason ≠ stop | Metric errors |
|---|---|---|---|---|---|---|---|
| local | 20 | 95.9 | 207.3 | 104 | 0 | 0 | 0 |
| cloud | 20 | 1.3 | 3.5 | 43 | 0 | 0 | 0 |

Notes: n = questions with a score on both sides. Mean tokens generated is `tokens_generated` from the pipeline outputs, i.e. the API's completion token count (reasoning tokens included where the API counts them). A metric that errored counts as missing for that question.
