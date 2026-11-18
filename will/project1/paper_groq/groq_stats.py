#!/usr/bin/env python3
"""
Numbers for paper_groq/paper.tex from cached outputs (no API calls).

    python3 paper_groq/groq_stats.py      # from will/project1

Groq run: outputs/. Comparison runs: outputs_openai/runs/pilot100__<model>__open_book__n3/.
Writes paper_groq/stats.json and paper_groq/fig_compare.pdf.
"""
from __future__ import annotations
import csv, json
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
P = HERE.parent
RUNS = {
    "gpt-oss-120b": P / "outputs",
    "gpt-4.1-mini": P / "outputs_openai/runs/pilot100__gpt-4.1-mini__open_book__n3",
    "gpt-4.1": P / "outputs_openai/runs/pilot100__gpt-4.1__open_book__n3",
    "gpt-5.5": P / "outputs_openai/runs/pilot100__gpt-5.5__open_book__n3",
}
SIGNALS = [("confidence", -1), ("ordinary_disagreement", 1), ("same_route_noise", 1), ("delta_comp_max", 1)]
rng = np.random.default_rng(0)


def load(d):
    f = {r["id"]: r for r in csv.DictReader(open(d / "features.csv"))}
    lab = {json.loads(l)["id"]: json.loads(l) for l in open(d / "labels.jsonl")}
    return f, lab


def boot_diff(y, a, b, n=2000):
    y, a, b = map(np.asarray, (y, a, b)); out = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].min() == y[i].max(): continue
        out.append(roc_auc_score(y[i], a[i]) - roc_auc_score(y[i], b[i]))
    return float(np.mean(out)), [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


S = {}
wrong_sets = {}
for m, d in RUNS.items():
    f, lab = load(d)
    ids = [i for i in f if f[i]["final_label"] != "abstain"]
    y = np.array([int(f[i]["wrong"]) for i in ids])
    col = lambda c, s: np.array([s * float(f[i][c]) for i in ids])
    conf = np.array([float(f[i]["confidence"]) for i in ids])
    dc = col("delta_comp_max", 1)
    s1 = [lab[i]["step_labels"][0]["label"] == "false" for i in ids]
    s2 = [lab[i]["step_labels"][1]["label"] == "false" for i in ids]
    fin = y.astype(bool)
    r = {
        "n": len(ids), "abstain": len(f) - len(ids), "err": float(y.mean()),
        "auroc": {c: float(roc_auc_score(y, col(c, s))) for c, s in SIGNALS},
        "comp_minus_sc": boot_diff(y, dc, col("ordinary_disagreement", 1)),
        "comp_minus_conf": boot_diff(y, dc, -conf),
        "conf_mean_correct": float(conf[~fin].mean()), "conf_mean_wrong": float(conf[fin].mean()),
        "conf_ge90": float((conf >= 90).mean()),
        "dc_zero": float((dc == 0).mean()), "dc_one": float((dc == 1).mean()),
        "wrong_rate_dc0": float(y[dc == 0].mean()), "wrong_rate_dcpos": float(y[dc > 0].mean()),
        "n_dc0": int((dc == 0).sum()),
        "step1_err": float(np.mean(s1)), "step2_err": float(np.mean(s2)),
        "p_final_wrong_given_s1_wrong": float(np.mean([a for a, b in zip(fin, s1) if b])) if any(s1) else None,
        "p_final_wrong_given_s1_ok": float(np.mean([a for a, b in zip(fin, s1) if not b])),
    }
    rj = json.load(open(d / "results.json"))
    r["H1"] = {"base": rj["H1"]["baseline"]["auroc"], "aug": rj["H1"]["augmented"]["auroc"],
               "gain": rj["H1"]["auroc_gain"]}
    r["H2"] = rj.get("H2")
    r["consistently_wrong"] = rj.get("consistently_wrong"); r["inconsistent_but_correct"] = rj.get("inconsistent_but_correct")
    bj = d / "budget.json"
    if bj.exists():
        b = json.load(open(bj)); r["budget"] = {k: v["reliability"] for k, v in b["headline"].items()}
        r["budget_gain_comp_vs_dep"] = b["gain_composition_vs_dependency_aware"]
        r["budget_gain_learned"] = b["gain_learned_composition_vs_baseline"]
        r["false_claims"] = b["n_false_claims"]
    S[m] = r
    wrong_sets[m] = {i for i in ids if f[i]["wrong"] == "1"}

# overlap of wrong questions with gpt-oss
g = wrong_sets["gpt-oss-120b"]
S["overlap"] = {m: {"both": len(g & w), "oss_only": len(g - w), "other_only": len(w - g)} for m, w in wrong_sets.items() if m != "gpt-oss-120b"}
allw = set.intersection(*wrong_sets.values()); S["wrong_all_four"] = len(allw)

# budget sweep for gpt-oss
curve = {}
for r in csv.DictReader(open(RUNS["gpt-oss-120b"] / "budget_curve.csv")):
    curve.setdefault(r["strategy"], []).append((float(r["budget_share"]), float(r["reliability"])))
S["oss_curve"] = curve
json.dump(S, open(HERE / "stats.json", "w"), indent=1)

# figure: reliability vs budget share for gpt-oss
fig, ax = plt.subplots(figsize=(6.4, 3.2))
style = {"Random": ("0.6", "--"), "Dependency-aware": ("#d08c2a", "-"), "Self-consistency": ("#3a9d5d", "-"),
         "Composition": ("#2a6fdb", "-"), "Learned + composition": ("#8a5cc2", ":")}
for k, (c, ls) in style.items():
    xs, ys = zip(*curve[k]); ax.plot([x * 100 for x in xs], ys, color=c, ls=ls, lw=1.8, marker="o", ms=3, label=k)
ax.axvline(25, color="0.85", lw=1)
ax.set_xlabel("Verification budget (% of claims checked)", fontsize=9); ax.set_ylabel("Reliability", fontsize=9)
ax.tick_params(labelsize=8)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.grid(color="0.93"); ax.legend(fontsize=7.5, frameon=False, loc="lower right")
fig.tight_layout(); fig.savefig(HERE / "fig_budget.pdf")

print(json.dumps({m: {k: v for k, v in r.items() if k not in ("H2",)} for m, r in S.items() if isinstance(r, dict) and m != "oss_curve"}, indent=1)); print("wrong_all_four", S["wrong_all_four"])
