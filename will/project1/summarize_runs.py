#!/usr/bin/env python3
"""
One table across every finished run in outputs_openai/runs/ (and the Groq
pilot in outputs/, once it has budget.json): error rate, single-signal
AUROCs, H1 gain, and the 25%-budget comparison from 06_budget.py.

Usage: python3 summarize_runs.py [--csv path]
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STRATS = ["Random", "Dependency-aware", "Self-consistency", "Composition",
          "Learned baseline", "Learned + composition", "Oracle"]


def fmt_ci(g):
    return f"{g['mean']:+.3f} [{g['ci95'][0]:+.3f}, {g['ci95'][1]:+.3f}]" if isinstance(g, dict) else "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(HERE / "outputs_openai" / "summary.csv"))
    args = ap.parse_args()
    dirs = sorted(p.parent for p in (HERE / "outputs_openai" / "runs").glob("*/budget.json")
                  if not p.parent.name.startswith("smoke"))
    if (HERE / "outputs" / "budget.json").exists():
        dirs.insert(0, HERE / "outputs")
    rows = []
    for d in dirs:
        r = json.loads((d / "results.json").read_text())
        b = json.loads((d / "budget.json").read_text())
        h1 = r["H1"] if isinstance(r["H1"], dict) else {}
        u = r["univariate_auroc"]
        row = {
            "run": "groq_pilot100__gpt-oss-120b" if d.name == "outputs" else d.name,
            "n": r["n_primary"], "err": r["error_rate"],
            "auc_conf": u.get("confidence"), "auc_sc": u.get("ordinary_disagreement"),
            "auc_noise": u.get("same_route_noise"), "auc_comp": u.get("delta_comp_max"),
            "H1_auroc_gain": fmt_ci(h1.get("auroc_gain")),
            "H2_auroc": (r.get("H2") or {}).get("auroc"),
            "claims": b["n_claims"], "false_claims": b["n_false_claims"], "checks": b["headline_checks"],
            **{f"rel_{s}": b["headline"].get(s, {}).get("reliability") for s in STRATS},
            "budget_gain_learned": fmt_ci(b["gain_learned_composition_vs_baseline"]),
            "budget_gain_comp_vs_dep": fmt_ci(b["gain_composition_vs_dependency_aware"]),
            "calls_per_q": round(b["probe_cost"]["llm_calls_per_question"], 1),
        }
        rows.append(row)
    if not rows:
        print("no finished runs yet")
        return
    with open(args.csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    f3 = lambda x: "-" if x is None else f"{x:.3f}"
    print(f"{'run':<44} {'n':>4} {'err':>5} | AUROC {'conf':>5} {'SC':>5} {'noise':>5} {'comp':>5} | H1 gain (AUROC)")
    for r in rows:
        print(f"{r['run']:<44} {r['n']:>4} {f3(r['err']):>5} |       {f3(r['auc_conf']):>5} {f3(r['auc_sc']):>5} "
              f"{f3(r['auc_noise']):>5} {f3(r['auc_comp']):>5} | {r['H1_auroc_gain']}")
    print(f"\n25% budget reliability    {'rand':>5} {'dep':>5} {'SC':>5} {'comp':>5} {'L':>5} {'L+c':>5} {'orac':>5} | L+c - L              | comp - dep")
    for r in rows:
        v = [f3(r[f"rel_{s}"]) for s in STRATS]
        print(f"{r['run'][:25]:<25} " + " ".join(f"{x:>5}" for x in v)
              + f" | {r['budget_gain_learned']:<20} | {r['budget_gain_comp_vs_dep']}")
    print(f"\nwrote {args.csv}")


if __name__ == "__main__":
    main()
