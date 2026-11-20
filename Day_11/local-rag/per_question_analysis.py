"""Per-question analysis for the evaluation report. It lays out the evidence; the conclusions are yours.

Run:    uv run python per_question_analysis.py
Reads:  pipeline_outputs_local.json, pipeline_outputs_cloud.json,
        eval_results_local.json, eval_results_cloud.json, test_questions.json
Writes: judge_vs_hand.md             judge verdict vs your own `passed` ratings (local run)
        local_vs_cloud_by_question.md   scores, answers and checks side by side, by question id

Two things to decide yourself and state in the report:
  * what counts as a judge "pass" (see RULES below; both variants are printed),
  * what counts as a notable local/cloud difference (DIFF_THRESHOLD below is arbitrary: compare it with the
    judge-noise estimate that this script prints).
"""
import json
import statistics
import sys
from pathlib import Path

REFUSAL = "cannot find this information"
DIFF_THRESHOLD = 0.2
CONTEXTUAL = ["Contextual Relevancy", "Contextual Recall", "Contextual Precision"]


def load(path):
    p = Path(path)
    if not p.exists():
        sys.exit(f"Missing file: {path}")
    return json.loads(p.read_text(encoding="utf-8"))


def by_id(rows):
    return {r["id"]: r for r in rows}


def short(text, n=300):
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1] + "…"


def score(erow, name):
    m = erow["metrics"].get(name)
    if m is None or m.get("error"):
        return None
    return m.get("score")


def pair(a, b):
    f = lambda x: "n/a" if x is None else f"{x:.2f}"
    return f"{f(a)} / {f(b)}"


def judge_pass(erow, names):
    return all(erow["metrics"].get(n, {}).get("success") is True for n in names)


def judge_vs_hand(out_local, eval_local, metric_names):
    outs, evals = by_id(out_local), by_id(eval_local)
    rules = {
        "Rule A: generation metrics pass (Faithfulness and Answer Relevancy)": ["Faithfulness", "Answer Relevancy"],
        "Rule B: all five metrics pass": metric_names,
    }
    lines = ["# Judge vs your own ratings (local run)", ""]
    unrated = [i for i, r in outs.items() if r.get("passed") is None]
    if unrated:
        lines.append(f"Warning: `passed` is still null for {unrated}; those rows are skipped.\n")
    ids = [i for i in outs if i in evals and outs[i].get("passed") is not None]

    for title, names in rules.items():
        cases = {"both pass": [], "both fail": [], "judge pass, you fail": [], "judge fail, you pass": []}
        for i in ids:
            j = judge_pass(evals[i], names)
            h = outs[i]["passed"] is True
            key = {(True, True): "both pass", (False, False): "both fail",
                   (True, False): "judge pass, you fail", (False, True): "judge fail, you pass"}[(j, h)]
            cases[key].append(i)
        lines += [f"## {title}", "", "| Case | Count | Question ids |", "|---|---|---|"]
        for key, members in cases.items():
            lines.append(f"| {key} | {len(members)} | {', '.join(members) or '-'} |")
        lines.append("")
        for key in ("judge pass, you fail", "judge fail, you pass"):
            for i in cases[key]:
                lines.append(f"### {i}: {key}")
                lines.append(f"- Question: {outs[i]['question']}")
                lines.append(f"- Your note: {outs[i].get('rating_note') or '(none)'}")
                lines.append(f"- Answer: {short(outs[i]['actual_answer'], 250)}")
                for n in names:
                    m = evals[i]["metrics"].get(n, {})
                    if m.get("success") is not True:
                        lines.append(f"- Judge, {n} = {m.get('score')}: {short(m.get('reason'), 350)}")
                lines.append("")
    lines.append(
        "For each disagreement above, decide who was right and say why in the report. "
        "Rows where a correct refusal was marked unfaithful are a judge finding."
    )
    return "\n".join(lines)


def local_vs_cloud(out_local, out_cloud, eval_local, eval_cloud, questions, metric_names):
    ol, oc, el, ec = by_id(out_local), by_id(out_cloud), by_id(eval_local), by_id(eval_cloud)
    ids = [i for i in ol if i in oc and i in el and i in ec]
    qinfo = by_id(questions)
    lines = ["# Local vs cloud, by question (cells are local / cloud)", ""]

    # Retrieval is shared, so differences on identical contexts are judge noise.
    same = [i for i in ids if ol[i]["retrieved_context"] == oc[i]["retrieved_context"]]
    lines += [
        f"Questions whose retrieved context is identical in both runs: {len(same)} of {len(ids)}.",
        "",
        "## Judge noise on identical contexts (mean and max |cloud - local|)",
        "",
        "| Metric | Questions | Mean abs diff | Max abs diff |",
        "|---|---|---|---|",
    ]
    for m in CONTEXTUAL:
        diffs = []
        for i in same:
            a, b = score(el[i], m), score(ec[i], m)
            if a is not None and b is not None:
                diffs.append(abs(b - a))
        if diffs:
            lines.append(f"| {m} | {len(diffs)} | {statistics.mean(diffs):.3f} | {max(diffs):.3f} |")
    lines.append("")

    header = "| id | type | " + " | ".join(metric_names) + " | refusal phrase | hand passed | time (s) | finish |"
    lines += ["## Scores and checks", "", header, "|" + "---|" * (header.count("|") - 1)]
    big = []
    for i in ids:
        cells = []
        for m in metric_names:
            a, b = score(el[i], m), score(ec[i], m)
            cells.append(pair(a, b))
            if a is not None and b is not None and abs(b - a) >= DIFF_THRESHOLD:
                big.append((abs(b - a), i, m, a, b))
        ref = lambda r: "yes" if REFUSAL in (r.get("actual_answer") or "").lower() else "no"
        hp = lambda r: {True: "T", False: "F", None: "-"}[r.get("passed")]
        t = lambda r: f"{r['generation_time_ms'] / 1000:.1f}"
        lines.append(
            f"| {i} | {qinfo.get(i, {}).get('type', '')} | " + " | ".join(cells)
            + f" | {ref(ol[i])} / {ref(oc[i])} | {hp(ol[i])} / {hp(oc[i])}"
            + f" | {t(ol[i])} / {t(oc[i])} | {ol[i]['finish_reason']} / {oc[i]['finish_reason']} |"
        )
    lines.append("")

    lines += [f"## Differences of at least {DIFF_THRESHOLD} on one metric (compare with the judge noise above)", ""]
    if big:
        for d, i, m, a, b in sorted(big, reverse=True):
            lines.append(f"- {i}, {m}: local {a:.2f}, cloud {b:.2f} ({b - a:+.2f})")
    else:
        lines.append("- none")
    lines.append("")

    lines += ["## Answers side by side", ""]
    for i in ids:
        lines += [
            f"### {i} ({qinfo.get(i, {}).get('type', '')}): {ol[i]['question']}",
            f"- Expected: {short(ol[i]['expected_answer'], 350)}",
            f"- Local: {short(ol[i]['actual_answer'], 350)}",
            f"- Cloud: {short(oc[i]['actual_answer'], 350)}",
            "",
        ]
    lines.append(
        "Read these pairs and answer, by id, where the cloud model fixed a local failure, where it did not, "
        "and where it was worse. The scores alone cannot tell you that."
    )
    return "\n".join(lines)


def main() -> None:
    out_local = load("pipeline_outputs_local.json")
    out_cloud = load("pipeline_outputs_cloud.json")
    eval_local = load("eval_results_local.json")
    eval_cloud = load("eval_results_cloud.json")
    questions = load("test_questions.json")
    metric_names = list(eval_local[0]["metrics"].keys())

    a = judge_vs_hand(out_local, eval_local, metric_names)
    b = local_vs_cloud(out_local, out_cloud, eval_local, eval_cloud, questions, metric_names)
    Path("judge_vs_hand.md").write_text(a + "\n", encoding="utf-8")
    Path("local_vs_cloud_by_question.md").write_text(b + "\n", encoding="utf-8")
    print(a.split("### ")[0])
    print("Wrote judge_vs_hand.md and local_vs_cloud_by_question.md")


if __name__ == "__main__":
    main()
