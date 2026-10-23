#!/usr/bin/env python3
"""
Stage C — composition tests, run without correctness labels.

For each question this compares two routes that category theory says should
agree, F(g∘f)(x) vs F(g)(F(f)(x)):

    direct    ask the composite question in one call
    stepwise  ask f, feed the model's *own* answer into g, ask g

Regions:
    - every overlapping two-step region (hop i, hop i+1) of the chain. For
      i > 0 the common input is the model's own upstream answer from Stage B
      (never a gold answer). The direct question for a sub-region is built by
      nesting (prompts.compose), since MuSiQue only writes the full composite.
    - for chains longer than two hops, also the full chain: the original
      question vs. executing every step in sequence.
    For 2-hop questions these coincide, so there is exactly one region.

Scores per region (total variation distance over normalised answers):
    delta_comp         d_TV(direct batch A, stepwise batch A)   — the signal
    delta_direct_self  d_TV(direct A, direct B)                  — noise control
    delta_step_self    d_TV(stepwise A, stepwise B)              — noise control
Per question:
    ordinary_disagreement  1 - (mode share) over 3N samples of the original
                           question, i.e. plain self-consistency at the same
                           cost as one composition test

Writes outputs/probes.jsonl and outputs/usage_C.json.

Usage:
    python 03_run_probes.py [--provider ... --model ...]
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import config
from common import (ABSTAIN, INVALID, distribution, extract_json_object,
                    load_included_tasks, normalize, read_jsonl,
                    save_config_snapshot, save_usage, tv_distance, write_jsonl)
from llm import LLM
from prompts import SYSTEM, answer_prompt, compose, fill

N = config.SAMPLES_PER_ROUTE


def ask(llm: LLM, question: str, paragraphs: list[dict], sample_index: int) -> str:
    c = llm.complete(SYSTEM, answer_prompt(question, paragraphs), sample_index)
    obj = extract_json_object(c.text)
    if obj is None or "answer" not in obj:
        return INVALID
    return str(obj["answer"])


def stepwise_sample(llm, steps, start, first_input, paragraphs, sample_index) -> tuple[list[str], str]:
    """Run steps[start:] in sequence with model-generated answers. Returns (trace, endpoint)."""
    answers = {start: first_input} if first_input is not None else {}
    trace = []
    for k in range(start, len(steps)):
        q = fill(steps[k], answers)
        a = ask(llm, q, paragraphs, sample_index)
        trace.append(a)
        if normalize(a) in (ABSTAIN, INVALID):
            return trace, a            # chain broken; endpoint is the explicit outcome
        answers[k + 1] = a             # step k (0-indexed) is referenced as #(k+1)
    return trace, trace[-1]


def run_region(llm, task, start, end, upstream, direct_q, batches):
    """Region covers hops start..end (inclusive, 0-indexed)."""
    steps = task["steps"][: end + 1]
    paras = task["paragraphs"]
    result = {"hops": [start, end], "direct_question": direct_q, "upstream_input": upstream,
              "direct": [], "stepwise": [], "stepwise_traces": []}
    for b in range(batches):
        idx = range(b * N, (b + 1) * N)
        result["direct"].append([ask(llm, direct_q, paras, s) for s in idx])
        traces = [stepwise_sample(llm, steps, start, upstream, paras, s) for s in idx]
        result["stepwise_traces"].append([t for t, _ in traces])
        result["stepwise"].append([e for _, e in traces])

    dA, sA = distribution(result["direct"][0]), distribution(result["stepwise"][0])
    result["delta_comp"] = tv_distance(dA, sA)
    if batches > 1:
        dB, sB = distribution(result["direct"][1]), distribution(result["stepwise"][1])
        result["delta_comp_B"] = tv_distance(dB, sB)
        result["delta_direct_self"] = tv_distance(dA, dB)
        result["delta_step_self"] = tv_distance(sA, sB)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default=config.PROVIDER)
    ap.add_argument("--model", default=config.MODEL)
    ap.add_argument("--out", default=str(config.OUTPUT_DIR))
    args = ap.parse_args()
    out = Path(args.out)

    llm = LLM(args.provider, args.model)
    tasks = load_included_tasks(out)
    original = {r["id"]: r for r in read_jsonl(out / "original.jsonl")}
    batches = 2 if config.SAME_ROUTE_CONTROL else 1

    rows = []
    for i, t in enumerate(tasks, 1):
        if t["id"] not in original:
            continue
        calls_before = llm.calls
        n, steps, orig = t["n_hops"], t["steps"], original[t["id"]]
        regions = []
        for s in range(n - 1):
            if s == 0:
                upstream = None
                inner = steps[0]
            else:
                upstream = orig["intermediate_answers"][s - 1]
                if normalize(upstream) in (ABSTAIN, INVALID):
                    regions.append({"hops": [s, s + 1], "skipped": "upstream answer missing"})
                    continue
                inner = fill(steps[s], {s: upstream})
            direct_q = t["question"] if n == 2 else compose(steps[s + 1], inner, s + 1)
            regions.append(run_region(llm, t, s, s + 1, upstream, direct_q, batches))
        if n > 2:
            regions.append({**run_region(llm, t, 0, n - 1, None, t["question"], batches),
                            "full_chain": True})

        # plain self-consistency on the original question, matched to one test's
        # cost; sample indices offset so these never reuse the direct-route samples
        ordinary = [ask(llm, t["question"], t["paragraphs"], 1000 + s) for s in range(3 * N)]
        ids = [normalize(a) for a in ordinary]
        ordinary_disagreement = 1 - Counter(ids).most_common(1)[0][1] / len(ids)

        rows.append({"id": t["id"], "n_hops": n, "regions": regions,
                     "ordinary_samples": ordinary,
                     "ordinary_disagreement": ordinary_disagreement,
                     "calls_incl_cached": llm.calls - calls_before})
        scored = [r["delta_comp"] for r in regions if "delta_comp" in r]
        print(f"  [{i}/{len(tasks)}] {t['id']}: delta_comp={['%.2f' % d for d in scored]} "
              f"ordinary={ordinary_disagreement:.2f} calls={rows[-1]['calls_incl_cached']}")

    write_jsonl(out / "probes.jsonl", rows)
    save_usage(out, "C", {"provider": args.provider, "model": args.model, **llm.usage()})
    save_config_snapshot(out, "C")
    print(f"Wrote probes for {len(rows)} questions. Usage: {llm.usage()}")


if __name__ == "__main__":
    main()
