#!/usr/bin/env python3
"""
Stage E — test predictive value (H1) and localization (H2) on the pilot.

H1: does composition inconsistency predict a wrong final answer *beyond*
    confidence, path length, question length and ordinary disagreement?
    Compares two logistic-regression predictors using out-of-fold predictions:
        baseline  = confidence, n_hops, question length, ordinary disagreement,
                    same-route noise
        augmented = baseline + delta_comp
    and reports AUROC / AUPRC with a paired bootstrap CI on the difference.
    One row per original question, so the CV and bootstrap are already
    clustered by question.

H2: across regions, does delta_comp rank regions that contain an erroneous
    claim above regions that do not? Reports AUROC, precision among the top
    ranked regions, and the share of erroneous claims those regions cover.

Also reports pilot feasibility: error prevalence, consistently-wrong and
inconsistent-but-correct counts, and calls/tokens per stage.

This is the *pilot* analysis: it is for checking feasibility and choosing the
protocol, not for claiming a result. Freeze the protocol, then rerun on
held-out questions for the detection study.

Writes outputs/features.csv and outputs/results.json.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import config
from common import read_jsonl

BASELINE = ["confidence", "n_hops", "question_words", "ordinary_disagreement", "same_route_noise"]
COMPOSITION = ["delta_comp_max"]


def load_manual_overrides(out: Path) -> dict[tuple[str, str], str]:
    path = out / "labels_manual.csv"
    if not path.exists():
        return {}
    with open(path) as f:
        return {(r["id"], r["claim"]): r["manual_label"].strip()
                for r in csv.DictReader(f) if r["manual_label"].strip()}


def safe_auc(y, s, fn):
    y = np.asarray(y)
    return float(fn(y, s)) if 0 < y.sum() < len(y) else None


def oof_predictions(X, y, seed=0):
    folds = min(config.CV_FOLDS, int(y.sum()), int(len(y) - y.sum()))
    if folds < 2:
        return None
    pred = np.zeros(len(y))
    for tr, te in StratifiedKFold(folds, shuffle=True, random_state=seed).split(X, y):
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        m.fit(X[tr], y[tr])
        pred[te] = m.predict_proba(X[te])[:, 1]
    return pred


def paired_bootstrap(y, a, b, fn, iters, seed=0):
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(iters):
        i = rng.integers(0, len(y), len(y))
        if 0 < y[i].sum() < len(i):
            diffs.append(fn(y[i], b[i]) - fn(y[i], a[i]))
    if not diffs:
        return None
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {"mean": float(np.mean(diffs)), "ci95": [float(lo), float(hi)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(config.OUTPUT_DIR))
    args = ap.parse_args()
    out = Path(args.out)

    tasks = {t["id"]: t for t in read_jsonl(out / "tasks.jsonl")}
    original = {r["id"]: r for r in read_jsonl(out / "original.jsonl")}
    labels = {r["id"]: r for r in read_jsonl(out / "labels.jsonl")}
    probes = read_jsonl(out / "probes.jsonl")
    overrides = load_manual_overrides(out)

    feats, region_rows = [], []
    for p in probes:
        qid = p["id"]
        lab = labels[qid]
        final_label = overrides.get((qid, "final"), lab["final_label"])
        step_label = {s["step"]: overrides.get((qid, f"step{s['step']}"), s["label"])
                      for s in lab["step_labels"]}
        scored = [r for r in p["regions"] if "delta_comp" in r]
        noise = [np.mean([r["delta_direct_self"], r["delta_step_self"]])
                 for r in scored if "delta_direct_self" in r]
        conf = original[qid]["confidence"]
        feats.append({
            "id": qid,
            "final_label": final_label,
            "wrong": int(final_label != "correct"),
            "confidence": conf,
            "n_hops": p["n_hops"],
            "question_words": len(tasks[qid]["question"].split()),
            "ordinary_disagreement": p["ordinary_disagreement"],
            "same_route_noise": float(np.mean(noise)) if noise else 0.0,
            "delta_comp_max": max((r["delta_comp"] for r in scored), default=0.0),
        })
        for r in scored:
            if r.get("full_chain"):
                continue
            hops = range(r["hops"][0] + 1, r["hops"][1] + 2)   # 1-indexed steps in region
            bad = [h for h in hops if step_label.get(h, "correct") != "correct"]
            region_rows.append({"id": qid, "hops": r["hops"], "delta_comp": r["delta_comp"],
                                "has_error": int(bool(bad)), "n_bad": len(bad)})

    # fill missing confidence with the median (logged as a count)
    confs = [f["confidence"] for f in feats if f["confidence"] is not None]
    med = float(np.median(confs)) if confs else 50.0
    missing_conf = sum(f["confidence"] is None for f in feats)
    for f in feats:
        if f["confidence"] is None:
            f["confidence"] = med

    with open(out / "features.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(feats[0]))
        w.writeheader()
        w.writerows(feats)

    # primary analysis excludes abstentions (kept separate, §6.4)
    primary = [f for f in feats if f["final_label"] != "abstain"]
    y = np.array([f["wrong"] for f in primary])
    res = {
        "n_questions": len(feats),
        "n_primary": len(primary),
        "n_abstain": len(feats) - len(primary),
        "n_wrong": int(y.sum()),
        "error_rate": float(y.mean()) if len(y) else None,
        "missing_confidence": missing_conf,
        "consistently_wrong": sum(1 for f in primary if f["wrong"] and f["delta_comp_max"] == 0),
        "inconsistent_but_correct": sum(1 for f in primary if not f["wrong"] and f["delta_comp_max"] > 0),
    }

    res["univariate_auroc"] = {}
    for k in BASELINE + COMPOSITION:
        s = np.array([f[k] for f in primary], dtype=float)
        if k == "confidence":
            s = -s                                   # low confidence => predicts error
        res["univariate_auroc"][k] = safe_auc(y, s, roc_auc_score)

    Xb = np.array([[f[k] for k in BASELINE] for f in primary], dtype=float)
    Xa = np.array([[f[k] for k in BASELINE + COMPOSITION] for f in primary], dtype=float)
    pb, pa = oof_predictions(Xb, y), oof_predictions(Xa, y)
    if pb is None:
        res["H1"] = "not enough errors and non-errors for cross-validation"
    else:
        res["H1"] = {
            "baseline": {"auroc": safe_auc(y, pb, roc_auc_score),
                         "auprc": safe_auc(y, pb, average_precision_score)},
            "augmented": {"auroc": safe_auc(y, pa, roc_auc_score),
                          "auprc": safe_auc(y, pa, average_precision_score)},
            "auroc_gain": paired_bootstrap(y, pb, pa, roc_auc_score, config.BOOTSTRAP_ITERS),
            "auprc_gain": paired_bootstrap(y, pb, pa, average_precision_score, config.BOOTSTRAP_ITERS),
            "prevalence": float(y.mean()),
        }

    if region_rows:
        ry = np.array([r["has_error"] for r in region_rows])
        rs = np.array([r["delta_comp"] for r in region_rows])
        order = np.argsort(-rs, kind="stable")
        k = max(1, len(order) // 10)
        top = order[:k]
        total_bad = sum(r["n_bad"] for r in region_rows)
        res["H2"] = {
            "n_regions": len(region_rows),
            "auroc": safe_auc(ry, rs, roc_auc_score),
            f"precision_top_{k}": float(ry[top].mean()),
            f"error_coverage_top_{k}": (sum(region_rows[i]["n_bad"] for i in top) / total_bad
                                        if total_bad else None),
        }

    cost = {}
    for stage in ("B", "C"):
        p = out / f"usage_{stage}.json"
        if p.exists():
            cost[stage] = json.loads(p.read_text())
    res["cost"] = cost
    res["nominal_calls_per_composition_test"] = 3 * config.SAMPLES_PER_ROUTE * (
        2 if config.SAME_ROUTE_CONTROL else 1)

    with open(out / "results.json", "w") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
