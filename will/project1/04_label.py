#!/usr/bin/env python3
"""
Stage D — independently label factual errors.

This is the only stage that reads gold.jsonl. It labels the Stage B outputs
(the original final answer and each intermediate claim) against MuSiQue's
reference answers.

Labels:
    correct                 matches the reference (token F1 >= threshold, aliases allowed
                            for the final answer)
    false                   does not match, and every upstream claim was correct
    false_on_wrong_premise  does not match, but an upstream claim was already wrong; the
                            step may be a valid inference from a false premise (§6.4)
    abstain                 model abstained or output was unusable

Automatic labels are a first pass. The abstract also asks for "unsupported"
and "invalid inference" labels, which need a person reading the evidence, so
labels_manual.csv has a manual_label column: anything filled in there
overrides the automatic label in Stage E.

Writes outputs/labels.jsonl and outputs/labels_manual.csv.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import config
from common import ABSTAIN, INVALID, normalize, read_jsonl, token_f1, write_jsonl


def match(pred: str, golds: list[str]) -> tuple[bool, float]:
    best = max((token_f1(pred, g) for g in golds), default=0.0)
    exact = any(normalize(pred) == normalize(g) for g in golds)
    return exact or best >= config.F1_CORRECT_THRESHOLD, best


def label_claim(pred: str, golds: list[str], upstream_ok: bool) -> tuple[str, float]:
    if normalize(pred) in (ABSTAIN, INVALID):
        return "abstain", 0.0
    ok, f1 = match(pred, golds)
    if ok:
        return "correct", f1
    return ("false" if upstream_ok else "false_on_wrong_premise"), f1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(config.OUTPUT_DIR))
    args = ap.parse_args()
    out = Path(args.out)

    gold = {g["id"]: g for g in read_jsonl(out / "gold.jsonl")}
    rows, sheet = [], []
    for o in read_jsonl(out / "original.jsonl"):
        g = gold[o["id"]]
        step_labels, upstream_ok = [], True
        for k, pred in enumerate(o["intermediate_answers"]):
            lab, f1 = label_claim(pred, [g["step_answers"][k]], upstream_ok)
            step_labels.append({"step": k + 1, "pred": pred, "gold": g["step_answers"][k],
                                "label": lab, "f1": round(f1, 3)})
            upstream_ok = upstream_ok and lab == "correct"
        final_lab, final_f1 = label_claim(o["final_answer"], [g["answer"]] + g["aliases"],
                                          upstream_ok=True)
        rows.append({"id": o["id"], "final_label": final_lab, "final_f1": round(final_f1, 3),
                     "final_pred": o["final_answer"], "final_gold": g["answer"],
                     "step_labels": step_labels,
                     "any_step_error": any(s["label"] != "correct" for s in step_labels)})
        sheet.append({"id": o["id"], "claim": "final", "pred": o["final_answer"],
                      "gold": " / ".join([g["answer"]] + g["aliases"]),
                      "auto_label": final_lab, "manual_label": "", "note": ""})
        for s in step_labels:
            sheet.append({"id": o["id"], "claim": f"step{s['step']}", "pred": s["pred"],
                          "gold": s["gold"], "auto_label": s["label"],
                          "manual_label": "", "note": ""})

    write_jsonl(out / "labels.jsonl", rows)
    manual = out / "labels_manual.csv"
    if manual.exists():
        print(f"  {manual} already exists — left untouched so manual labels are not lost.")
    else:
        with open(manual, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(sheet[0]))
            w.writeheader()
            w.writerows(sheet)
    counts = {}
    for r in rows:
        counts[r["final_label"]] = counts.get(r["final_label"], 0) + 1
    print(f"Labeled {len(rows)} questions. Final-answer labels: {counts}")


if __name__ == "__main__":
    main()
