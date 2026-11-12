#!/usr/bin/env python3
"""
Regenerates the paper's figure from the cached runs (no API calls).

    python3 paper/make_figures.py      # from will/project1

Writes paper/fig_aggregator.pdf: AUROC of the composition score on 3- and
4-hop scale300 questions, max over regions (pre-specified) vs. full chain only.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "outputs_openai" / "runs"
MODELS = [("gpt-4.1-mini", "gpt-4.1-mini"), ("gpt-5.5", "gpt-5.5")]


def scores(model: str, hops: int) -> tuple[float, float]:
    d = RUNS / f"scale300__{model}__open_book__n3"
    feats = {r["id"]: r for r in csv.DictReader(open(d / "features.csv"))}
    probes = {json.loads(l)["id"]: json.loads(l) for l in open(d / "probes.jsonl")}
    ids = [i for i, f in feats.items() if int(f["n_hops"]) == hops and f["final_label"] != "abstain"]
    y = [int(feats[i]["wrong"]) for i in ids]
    full = [next(r["delta_comp"] for r in probes[i]["regions"] if r.get("full_chain")) for i in ids]
    mx = [float(feats[i]["delta_comp_max"]) for i in ids]
    return roc_auc_score(y, mx), roc_auc_score(y, full)


def main():
    rows = [(f"{label} · {h}-hop", *scores(m, h)) for m, label in MODELS for h in (3, 4)]
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    for k, (name, mx, full) in enumerate(reversed(rows)):
        ax.plot([mx, full], [k, k], color="0.75", lw=2, zorder=1)
        ax.scatter([mx], [k], color="0.6", s=45, zorder=2, label="max over regions (pre-specified)" if k == 0 else None)
        ax.scatter([full], [k], color="#2a6fdb", s=45, zorder=3, label="full chain only (post hoc)" if k == 0 else None)
        ax.annotate(f"{mx:.2f}", (mx, k), xytext=(0, -13), textcoords="offset points", ha="center", fontsize=8, color="0.4")
        ax.annotate(f"{full:.2f}", (full, k), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=8)
    ax.axvline(0.5, color="0.3", ls="--", lw=1)
    ax.text(0.502, len(rows) - 0.45, "chance", fontsize=8, color="0.3")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in reversed(rows)], fontsize=9)
    ax.set_xlim(0.4, 0.7)
    ax.set_ylim(-0.6, len(rows) - 0.3)
    ax.set_xlabel("AUROC for a wrong final answer", fontsize=9)
    ax.tick_params(axis="x", labelsize=8)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="0.92")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=2, frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "fig_aggregator.pdf")
    for r in rows:
        print(f"{r[0]:<20} max={r[1]:.3f} full={r[2]:.3f}")


if __name__ == "__main__":
    main()
