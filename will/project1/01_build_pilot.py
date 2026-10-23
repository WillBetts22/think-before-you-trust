#!/usr/bin/env python3
"""
Stage A — construct and audit task representations.

Selects linear-chain MuSiQue questions, renders each hop as an askable
question, and writes three files to outputs/:

    tasks.jsonl   what the detector may see: question, question-only steps
                  (with #k placeholders), paragraphs with supporting flags removed
    gold.jsonl    what only the labeler (Stage D) may see: final answer, aliases,
                  per-step answers, supporting paragraph ids
    audit.csv     one row per question for a manual audit; set include=0 and
                  write a reason to drop a question before Stage B

Usage:
    python 01_build_pilot.py [--n 100] [--hops 2,3]
"""

from __future__ import annotations

import argparse
import csv
import random
import re
from collections import defaultdict
from pathlib import Path

import config
from common import read_jsonl, save_config_snapshot, write_jsonl
from prompts import refs, render_step

# Pre-registered exclusion flags (abstract §6.1: rules fixed before looking at
# detector performance). These only *flag*; the auditor makes the call.
TIME_SENSITIVE = re.compile(r"\b(current|currently|now|latest|present|today|recent|this year)\b", re.I)


def is_linear_chain(decomp: list[dict]) -> bool:
    """Step 1 has no #refs, and step k (k >= 2) refers to exactly #(k-1)."""
    for k, step in enumerate(decomp):
        r = refs(step["question"])
        if (k == 0 and r) or (k > 0 and r != {k}):
            return False
    return True


def audit_flags(row: dict, steps: list[str]) -> list[str]:
    flags = []
    if TIME_SENSITIVE.search(row["question"]) or any(TIME_SENSITIVE.search(s) for s in steps):
        flags.append("time_sensitive_wording")
    if any(">>" in s["question"] for s in row["question_decomposition"]):
        flags.append("kb_style_hop_rendered")
    if len(row["answer"].split()) > 6:
        flags.append("long_answer")
    return flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=config.PILOT_SIZE)
    ap.add_argument("--hops", default=",".join(map(str, config.HOPS)))
    ap.add_argument("--out", default=str(config.OUTPUT_DIR))
    args = ap.parse_args()
    hops = tuple(int(h) for h in args.hops.split(","))
    out = Path(args.out)

    src = config.MUSIQUE_DIR / config.SOURCE_FILE
    if not src.exists():
        raise SystemExit(f"{src} not found — run multihop_data/download_musique.sh first.")
    rows = read_jsonl(src)

    by_hops = defaultdict(list)
    for r in rows:
        d = r["question_decomposition"]
        if r.get("answerable", True) and len(d) in hops and is_linear_chain(d):
            by_hops[len(d)].append(r)
    for h in hops:
        print(f"  {h}-hop linear chains available: {len(by_hops[h])}")

    rng = random.Random(config.SELECTION_SEED)
    per = args.n // len(hops)
    chosen = []
    for i, h in enumerate(hops):
        k = per + (1 if i < args.n % len(hops) else 0)
        chosen += rng.sample(by_hops[h], min(k, len(by_hops[h])))

    tasks, gold, audit = [], [], []
    for r in chosen:
        steps = [render_step(s["question"]) for s in r["question_decomposition"]]
        tasks.append({
            "id": r["id"],
            "n_hops": len(steps),
            "question": r["question"],
            "steps": steps,
            "paragraphs": [{"title": p["title"], "text": p["paragraph_text"]}
                           for p in r["paragraphs"]],
        })
        gold.append({
            "id": r["id"],
            "answer": r["answer"],
            "aliases": r.get("answer_aliases", []),
            "step_answers": [s["answer"] for s in r["question_decomposition"]],
            "step_support_idx": [s["paragraph_support_idx"] for s in r["question_decomposition"]],
        })
        audit.append({
            "id": r["id"],
            "include": 1,
            "exclusion_reason": "",
            "flags": ";".join(audit_flags(r, steps)),
            "question": r["question"],
            "rendered_steps": " | ".join(steps),
            "gold_step_answers": " | ".join(s["answer"] for s in r["question_decomposition"]),
            "gold_answer": r["answer"],
        })

    write_jsonl(out / "tasks.jsonl", tasks)
    write_jsonl(out / "gold.jsonl", gold)
    with open(out / "audit.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(audit[0]))
        w.writeheader()
        w.writerows(audit)
    save_config_snapshot(out, "A")
    flagged = sum(1 for a in audit if a["flags"])
    print(f"Wrote {len(tasks)} tasks to {out}  ({flagged} flagged for audit)")
    print(f"Next: review {out / 'audit.csv'} (set include=0 to drop), then run 02_generate_original.py")


if __name__ == "__main__":
    main()
