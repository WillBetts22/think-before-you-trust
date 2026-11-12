#!/usr/bin/env python3
"""
Stage F (first pass) — the composition signal under a fixed verification budget.

This puts the probe results into the framework of the parent project
(dag_codes/dag_model.py, Allison Li): every claim is a node, a verification
reveals one claim's truth, a verified-false claim quarantines everything
downstream of it, and

    reliability = 1 - undetected_false / total_claims

Here the DAG is real: each MuSiQue chain is a path step1 -> step2 -> ... -> final,
labelled by Stage D. A strategy spends a budget of B verifications across all
claims of all questions. Budgets are given as a share of claims; the headline
is 25%, matching the parent project's 20 checks on an 80-node DAG, and the
sweep matches its 5..50 checks / 80.

Strategies (each scores claims; verification goes to the top B):
    Random                 floor (mean of 500 draws)
    Uncertainty-first      1 - stated confidence                     (self-report)
    Dependency-aware       (1 - confidence) * D,  D = 1 + #downstream  (parent project's p_false * D)
    Self-consistency       ordinary disagreement * D
    Composition            delta_comp of the claim's region * D
    Learned baseline       out-of-fold P(wrong) from Stage E's baseline features * D
    Learned + composition  same, with delta_comp added                 <- the H1 comparison in budget terms
    Oracle                 truth-conditioned ceiling (catch upstream-most false claims first)

In this pass every question gets the full composition probe, so the probe's
LLM calls are a separate, fixed cost reported next to the result. Deciding how
much of a shared budget to spend on probes vs. verifications is the follow-up
optimisation (see README, "Budget").

Writes outputs/budget.json and outputs/budget_curve.csv.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import config
from common import read_jsonl

HEADLINE = 0.25                                   # 20 / 80 in dag_main.py
SWEEP = [5 / 80, 10 / 80, 15 / 80, 20 / 80, 25 / 80, 30 / 80, 40 / 80, 50 / 80]
BASELINE = ["confidence", "n_hops", "question_words", "ordinary_disagreement", "same_route_noise"]


def oof(X, y, seed=0):
    folds = min(config.CV_FOLDS, int(y.sum()), int(len(y) - y.sum()))
    if folds < 2:
        return None
    pred = np.zeros(len(y))
    for tr, te in StratifiedKFold(folds, shuffle=True, random_state=seed).split(X, y):
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        m.fit(X[tr], y[tr])
        pred[te] = m.predict_proba(X[te])[:, 1]
    return pred


def build_claims(out: Path):
    """One node per (question, step); the last step is the final answer."""
    feats = {r["id"]: r for r in csv.DictReader(open(out / "features.csv"))}
    labels = {r["id"]: r for r in read_jsonl(out / "labels.jsonl")}
    probes = {r["id"]: r for r in read_jsonl(out / "probes.jsonl")}
    claims = []
    for qid, f in feats.items():
        lab, n = labels[qid], int(f["n_hops"])
        regions = [r for r in probes[qid]["regions"] if "delta_comp" in r]
        for k in range(1, n + 1):
            label = lab["final_label"] if k == n else lab["step_labels"][k - 1]["label"]
            # delta of the most inconsistent region that contains this step
            d = max((r["delta_comp"] for r in regions if r["hops"][0] + 1 <= k <= r["hops"][1] + 1),
                    default=0.0)
            claims.append({"qid": qid, "step": k, "n": n, "false": label in ("false", "false_on_wrong_premise"),
                           "downstream": n - k, "delta": d})
    return feats, claims


def evaluate(claims, chosen: set[int]) -> dict:
    false = {i for i, c in enumerate(claims) if c["false"]}
    caught = chosen & false
    quarantined = set()
    for i in caught:                     # everything after a caught false claim, same question
        c = claims[i]
        quarantined |= {j for j, d in enumerate(claims) if d["qid"] == c["qid"] and d["step"] > c["step"]}
    undetected = false - chosen - quarantined
    return {"reliability": 1 - len(undetected) / len(claims),
            "recall": (len(false) - len(undetected)) / len(false) if false else 1.0,
            "precision": len(caught) / len(chosen) if chosen else 0.0,
            "undetected_false": len(undetected)}


def top_b(scores: list[float], claims, b: int) -> set[int]:
    # ties: upstream first (more downstream claims protected), then stable
    order = sorted(range(len(claims)), key=lambda i: (-scores[i], -claims[i]["downstream"], i))
    return set(order[:b])


def oracle(claims, b: int) -> set[int]:
    # first false claim of each question protects the whole rest of the chain
    firsts = {}
    for i, c in enumerate(claims):
        if c["false"] and (c["qid"] not in firsts or c["step"] < claims[firsts[c["qid"]]]["step"]):
            firsts[c["qid"]] = i
    ranked = sorted(firsts.values(), key=lambda i: -sum(
        d["false"] for d in claims if d["qid"] == claims[i]["qid"] and d["step"] >= claims[i]["step"]))
    others = [i for i, c in enumerate(claims) if c["false"] and i not in firsts.values()]
    rest = [i for i in range(len(claims)) if i not in set(ranked) | set(others)]
    return set((ranked + others + rest)[:b])


def strategy_scores(feats, claims):
    ids = list(feats)
    y = np.array([int(feats[q]["wrong"]) for q in ids])
    Xb = np.array([[float(feats[q][k]) for k in BASELINE] for q in ids])
    Xa = np.column_stack([Xb, [float(feats[q]["delta_comp_max"]) for q in ids]])
    pb, pa = oof(Xb, y), oof(Xa, y)
    p_base = dict(zip(ids, pb)) if pb is not None else None
    p_aug = dict(zip(ids, pa)) if pa is not None else None

    D = [1 + c["downstream"] for c in claims]
    conf = [1 - float(feats[c["qid"]]["confidence"]) / 100 for c in claims]
    s = {
        "Uncertainty-first": conf,
        "Dependency-aware": [p * d for p, d in zip(conf, D)],
        "Self-consistency": [float(feats[c["qid"]]["ordinary_disagreement"]) * d for c, d in zip(claims, D)],
        "Composition": [c["delta"] * d for c, d in zip(claims, D)],
    }
    if p_base:
        s["Learned baseline"] = [p_base[c["qid"]] * d for c, d in zip(claims, D)]
        s["Learned + composition"] = [p_aug[c["qid"]] * d for c, d in zip(claims, D)]
    return s


def run(feats, claims, fractions, n_random=500, seed=0):
    rng = random.Random(seed)
    scores = strategy_scores(feats, claims)
    rows = []
    for frac in fractions:
        b = max(1, round(frac * len(claims)))
        res = {"Random": {k: float(np.mean(v)) for k, v in _random(claims, b, n_random, rng).items()}}
        for name, sc in scores.items():
            res[name] = evaluate(claims, top_b(sc, claims, b))
        res["Oracle"] = evaluate(claims, oracle(claims, b))
        for name, m in res.items():
            rows.append({"budget_share": round(frac, 4), "checks": b, "strategy": name, **m})
    return rows


def _random(claims, b, n, rng):
    out = {"reliability": [], "recall": [], "precision": [], "undetected_false": []}
    for _ in range(n):
        m = evaluate(claims, set(rng.sample(range(len(claims)), b)))
        for k in out:
            out[k].append(m[k])
    return out


def bootstrap_gain(feats, claims, frac, a="Learned baseline", b="Learned + composition", iters=1000, seed=0):
    """Paired bootstrap over questions of reliability(b) - reliability(a) at one budget."""
    rng = np.random.default_rng(seed)
    ids = list(feats)
    by_q = {}
    for c in claims:
        by_q.setdefault(c["qid"], []).append(c)
    diffs = []
    for _ in range(iters):
        pick = rng.choice(ids, len(ids), replace=True)
        f2, c2 = {}, []
        for j, q in enumerate(pick):
            nq = f"{q}#{j}"
            f2[nq] = feats[q]
            c2 += [{**c, "qid": nq} for c in by_q[q]]
        y = [int(f2[q]["wrong"]) for q in f2]
        if not (0 < sum(y) < len(y)) or min(sum(y), len(y) - sum(y)) < 2:
            continue
        sc = strategy_scores(f2, c2)
        if a not in sc:
            continue
        k = max(1, round(frac * len(c2)))
        diffs.append(evaluate(c2, top_b(sc[b], c2, k))["reliability"]
                     - evaluate(c2, top_b(sc[a], c2, k))["reliability"])
    if not diffs:
        return None
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {"mean": float(np.mean(diffs)), "ci95": [float(lo), float(hi)], "n_boot": len(diffs)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(config.OUTPUT_DIR))
    ap.add_argument("--boot", type=int, default=1000)
    args = ap.parse_args()
    out = Path(args.out)

    feats, claims = build_claims(out)
    rows = run(feats, claims, SWEEP + ([HEADLINE] if HEADLINE not in SWEEP else []))
    with open(out / "budget_curve.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    head = {r["strategy"]: {k: r[k] for k in ("reliability", "recall", "precision", "undetected_false")}
            for r in rows if abs(r["budget_share"] - HEADLINE) < 1e-9}
    usage = {s: json.loads((out / f"usage_{s}.json").read_text())
             for s in ("B", "C") if (out / f"usage_{s}.json").exists()}
    res = {
        "n_questions": len(feats), "n_claims": len(claims),
        "n_false_claims": sum(c["false"] for c in claims),
        "headline_budget_share": HEADLINE,
        "headline_checks": max(1, round(HEADLINE * len(claims))),
        "headline": head,
        "gain_learned_composition_vs_baseline": bootstrap_gain(feats, claims, HEADLINE, iters=args.boot),
        "gain_composition_vs_dependency_aware": bootstrap_gain(
            feats, claims, HEADLINE, a="Dependency-aware", b="Composition", iters=args.boot),
        "probe_cost": {
            "llm_calls_per_question": (usage.get("C", {}).get("calls", 0) + usage.get("B", {}).get("calls", 0))
                                      / max(1, len(feats)),
            "prompt_tokens": sum(u.get("prompt_tokens", 0) for u in usage.values()),
            "completion_tokens": sum(u.get("completion_tokens", 0) for u in usage.values()),
        },
    }
    (out / "budget.json").write_text(json.dumps(res, indent=2))
    print(f"{len(claims)} claims ({res['n_false_claims']} false), headline budget "
          f"{res['headline_checks']} checks ({HEADLINE:.0%}):")
    for name, m in head.items():
        print(f"  {name:<22} reliability={m['reliability']:.3f}  recall={m['recall']:.3f}  "
              f"undetected={m['undetected_false']}")
    print(f"  learned+composition vs learned baseline: {res['gain_learned_composition_vs_baseline']}")


if __name__ == "__main__":
    main()
