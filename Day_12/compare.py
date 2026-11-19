"""Local vs cloud comparison, from the saved result files.

Run:    uv run python compare.py
Reads:  eval_results_local.json, eval_results_cloud.json,
        pipeline_outputs_local.json, pipeline_outputs_cloud.json
Writes: compare_output.md  (the same markdown that is printed; paste it into the report)

For each metric, only questions that have a score on BOTH sides are used, so the two means are
computed on the same questions. "± band" is 2 x SE, with SE = sample standard deviation / sqrt(n).
The per-question difference is cloud minus local on the same question; if its range
(mean ± 2 x SE) includes zero, the verdict is "no clear difference".
"""
import json
import math
import statistics
import sys
from pathlib import Path

LOCAL = "local"
CLOUD = "cloud"
METRIC_ORDER = [
    "Contextual Relevancy",
    "Contextual Recall",
    "Contextual Precision",
    "Faithfulness",
    "Answer Relevancy",
]


def load(path: str):
    p = Path(path)
    if not p.exists():
        sys.exit(f"Missing file: {path}")
    return json.loads(p.read_text(encoding="utf-8"))


def scores_by_id(eval_rows):
    """{question id: {metric name: score}}, skipping metrics that errored or have no score."""
    scores = {}
    errors = 0
    for row in eval_rows:
        per_metric = {}
        for name, m in row["metrics"].items():
            if m.get("error"):
                errors += 1
                continue
            if m.get("score") is not None:
                per_metric[name] = m["score"]
        scores[row["id"]] = per_metric
    return scores, errors


def mean_band(values):
    """(mean, 2 x SE). The band is None when fewer than two values exist."""
    n = len(values)
    if n == 0:
        return None, None
    mean = sum(values) / n
    if n < 2:
        return mean, None
    return mean, 2 * statistics.stdev(values) / math.sqrt(n)


def fmt(mean, band, signed=False):
    if mean is None:
        return "n/a"
    text = f"{mean:+.3f}" if signed else f"{mean:.3f}"
    return f"{text} ± {band:.3f}" if band is not None else f"{text} (n<2)"


def verdict(mean, band):
    if mean is None or band is None:
        return "n too small"
    if mean - band <= 0 <= mean + band:
        return "no clear difference"
    return "cloud higher" if mean > 0 else "local higher"


def run_stats(rows):
    times = [r["generation_time_ms"] / 1000 for r in rows if r.get("generation_time_ms") is not None]
    tokens = [r["tokens_generated"] for r in rows if r.get("tokens_generated") is not None]
    return {
        "questions": len(rows),
        "median_s": statistics.median(times) if times else None,
        "slowest_s": max(times) if times else None,
        "mean_tokens": sum(tokens) / len(tokens) if tokens else None,
        "empty": sum(1 for r in rows if not (r.get("actual_answer") or "").strip()),
        "not_stop": sum(1 for r in rows if r.get("finish_reason") != "stop"),
    }


def num(value, digits=1):
    return "n/a" if value is None else f"{value:.{digits}f}"


def main() -> None:
    eval_local = load(f"eval_results_{LOCAL}.json")
    eval_cloud = load(f"eval_results_{CLOUD}.json")
    out_local = load(f"pipeline_outputs_{LOCAL}.json")
    out_cloud = load(f"pipeline_outputs_{CLOUD}.json")

    s_local, err_local = scores_by_id(eval_local)
    s_cloud, err_cloud = scores_by_id(eval_cloud)

    only_local = sorted(set(s_local) - set(s_cloud))
    only_cloud = sorted(set(s_cloud) - set(s_local))

    metrics = [m for m in METRIC_ORDER if any(m in v for v in s_local.values())]
    for v in list(s_local.values()) + list(s_cloud.values()):
        for m in v:
            if m not in metrics:
                metrics.append(m)

    lines = []
    lines.append(
        "| Metric | n | Local mean ± 2×SE | Cloud mean ± 2×SE | Cloud − local (mean ± 2×SE) | Verdict |"
    )
    lines.append("|---|---|---|---|---|---|")
    for metric in metrics:
        ids = [i for i in s_local if i in s_cloud and metric in s_local[i] and metric in s_cloud[i]]
        loc = [s_local[i][metric] for i in ids]
        clo = [s_cloud[i][metric] for i in ids]
        diffs = [c - l for c, l in zip(clo, loc)]
        lm, lb = mean_band(loc)
        cm, cb = mean_band(clo)
        dm, db = mean_band(diffs)
        lines.append(
            f"| {metric} | {len(ids)} | {fmt(lm, lb)} | {fmt(cm, cb)} | {fmt(dm, db, signed=True)} | {verdict(dm, db)} |"
        )

    stats_local = run_stats(out_local)
    stats_cloud = run_stats(out_cloud)
    lines.append("")
    lines.append(
        "| Run | Questions | Median generation time (s) | Slowest (s) | Mean tokens generated | Empty answers | finish_reason ≠ stop | Metric errors |"
    )
    lines.append("|---|---|---|---|---|---|---|---|")
    for label, st, err in ((LOCAL, stats_local, err_local), (CLOUD, stats_cloud, err_cloud)):
        lines.append(
            f"| {label} | {st['questions']} | {num(st['median_s'])} | {num(st['slowest_s'])} | "
            f"{num(st['mean_tokens'], 0)} | {st['empty']} | {st['not_stop']} | {err} |"
        )

    lines.append("")
    lines.append(
        "Notes: n = questions with a score on both sides. Mean tokens generated is `tokens_generated` "
        "from the pipeline outputs, i.e. the API's completion token count (reasoning tokens included where "
        "the API counts them). A metric that errored counts as missing for that question."
    )
    if only_local or only_cloud:
        lines.append(
            f"Warning: ids only in local eval: {only_local or 'none'}; only in cloud eval: {only_cloud or 'none'}."
        )

    text = "\n".join(lines)
    print(text)
    Path("compare_output.md").write_text(text + "\n", encoding="utf-8")
    print("\nWrote compare_output.md")


if __name__ == "__main__":
    main()
