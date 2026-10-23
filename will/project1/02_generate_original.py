#!/usr/bin/env python3
"""
Stage B — generate original answers and intermediate claims.

One call per question: the model answers the multi-hop question, records its
answer to each (question-only) step, and states a confidence. These original
outputs are collected before any diagnostic probe runs, and every later
policy uses these same outputs.

Writes outputs/original.jsonl and outputs/usage_B.json.

Usage:
    python 02_generate_original.py [--provider groq --model llama-3.3-70b-versatile]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import config
from common import (INVALID, extract_json_object, load_included_tasks,
                    save_config_snapshot, save_usage, write_jsonl)
from llm import LLM
from prompts import SYSTEM, original_prompt


def parse_original(text: str, n_hops: int) -> dict:
    obj = extract_json_object(text) or {}
    inter = obj.get("intermediate_answers")
    inter = [str(a) for a in inter] if isinstance(inter, list) else []
    inter = (inter + [INVALID] * n_hops)[:n_hops]
    conf = obj.get("confidence")
    try:
        conf = max(0.0, min(100.0, float(conf)))
    except (TypeError, ValueError):
        conf = None
    final = obj.get("final_answer")
    return {
        "parse_ok": bool(obj) and final is not None,
        "intermediate_answers": inter,
        "final_answer": str(final) if final is not None else INVALID,
        "confidence": conf,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default=config.PROVIDER)
    ap.add_argument("--model", default=config.MODEL)
    ap.add_argument("--out", default=str(config.OUTPUT_DIR))
    args = ap.parse_args()
    out = Path(args.out)

    llm = LLM(args.provider, args.model)
    tasks = load_included_tasks(out)
    rows = []
    for i, t in enumerate(tasks, 1):
        c = llm.complete(SYSTEM, original_prompt(t["question"], t["steps"], t["paragraphs"]))
        parsed = parse_original(c.text, t["n_hops"])
        rows.append({"id": t["id"], "n_hops": t["n_hops"], "raw": c.text,
                     "prompt_tokens": c.prompt_tokens, "completion_tokens": c.completion_tokens,
                     "latency_s": c.latency_s, **parsed})
        tag = "ok " if parsed["parse_ok"] else "BAD"
        print(f"  [{i}/{len(tasks)}] {tag} {t['id']}: {parsed['final_answer'][:60]}")

    write_jsonl(out / "original.jsonl", rows)
    save_usage(out, "B", {"provider": args.provider, "model": args.model, **llm.usage()})
    save_config_snapshot(out, "B")
    bad = sum(not r["parse_ok"] for r in rows)
    print(f"Wrote {len(rows)} original outputs ({bad} unparseable). Usage: {llm.usage()}")


if __name__ == "__main__":
    main()
