"""
Pilot A: a cellular-sheaf inconsistency score on the parent project's claim DAGs.

Question
--------
Will's delta_comp compares two routes along a *chain*. On a DAG a claim can have
several parents, so there are more "routes" that must agree. Does a sheaf-style
inconsistency score that uses *all* DAG edges localize false claims better than
the same score restricted to the spanning tree (the chain-only view), and does it
help the parent project's budgeted verification (reliability at a fixed budget)?

Model of what an LLM reports (THIS IS AN ASSUMPTION, NOT DATA)
--------------------------------------------------------------
* Claim DAGs, truths, confidences and descendant counts come unchanged from
  dag_codes/dag_model.ClaimDAG (PARC-fitted error/propagation rates).
* Each claim v gets a d-dim "content" vector. The true contents x*_v form a
  global section of a cellular sheaf on the DAG: for each edge e = (u -> v),
  restriction maps F_{u<e} = R_e (orthogonal), F_{v<e} = I, with R_e x*_u = x*_v.
* The model's reported content x_v:
    - true claim:                    x*_v + sigma * noise
    - originating error (parents ok):x*_v + a * (random direction)   ("fabrication")
    - propagated error (a false parent): with prob q_consistent the model reasons
      *consistently from its wrong premise*: x_v = R_e x_p + sigma * noise for a false
      parent p; otherwise it fabricates afresh as above.
  This encodes the "consistently wrong" failure mode the paper worries about.
* Gold-free scores only see x, the graph and the restriction maps.

Scores
------
edge energy        d_e = || R_e x_u - x_v ||^2      (sheaf Dirichlet energy = sum_e d_e = x^T L_F x)
repair score       dE(v) = E_v(x_v) - min_y E_v(y), E_v = energy of edges incident to v
                   (how much the global inconsistency drops if v alone is re-solved; a local
                   harmonic-extension / leave-one-out localisation)
sheaf-tree         same repair score but only on spanning-tree (primary-parent) edges
                   = the "chain-only" analogue of delta_comp
p_sheaf            1 - exp(-dE / (2 * s2 * d)), s2 = robust noise scale from median edge energy
Strategies are evaluated with the parent project's evaluate() (quarantine + reliability).

Usage: ./run.sh will/ct_safety_survey/pilots/sheaf_dag/sheaf_dag_pilot.py [--trials 100] [--quick]
(run from the repo root so dag_codes is importable).
"""
import argparse
import json
import os
import random
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
sys.path.insert(0, os.path.join(ROOT, "dag_codes"))

_cwd = os.getcwd()
os.chdir(ROOT)  # dag_model creates ./results_dag on import; keep that inside the repo's existing folder
import dag_model as dm  # noqa: E402
from constants import BASE_ERROR_RATE, PROPAGATION_RATE  # noqa: E402
os.chdir(_cwd)

from sklearn.metrics import roc_auc_score  # noqa: E402


# ---------------------------------------------------------------- sheaf construction
def random_orthogonal(d, rng):
    q, r = np.linalg.qr(rng.standard_normal((d, d)))
    return q * np.sign(np.diag(r))


def householder_to(a, b):
    """Orthogonal H with H a = b (requires ||a|| = ||b||)."""
    v = a - b
    nv = np.linalg.norm(v)
    if nv < 1e-12:
        return np.eye(len(a))
    v = v / nv
    return np.eye(len(a)) - 2.0 * np.outer(v, v)


def edges_of(dag):
    """List of (u, v, is_tree_edge). The first parent is the BFS-tree parent."""
    out = []
    for v, node in dag.nodes.items():
        for k, u in enumerate(node.parents):
            out.append((u, v, k == 0))
    return out


def build_sheaf_and_observations(dag, d, sigma, a, q_consistent, rng):
    order = dag._topological_order()
    xstar, R = {}, {}
    root = order[0]
    xstar[root] = rng.standard_normal(d)
    xstar[root] *= np.sqrt(d) / np.linalg.norm(xstar[root])
    for v in order[1:]:
        ps = dag.nodes[v].parents
        Q = random_orthogonal(d, rng)
        xstar[v] = Q @ xstar[ps[0]]
        R[(ps[0], v)] = Q
        for u in ps[1:]:
            Q2 = random_orthogonal(d, rng)
            R[(u, v)] = householder_to(Q2 @ xstar[u], xstar[v]) @ Q2

    x, kind = {}, {}
    for v in order:
        node = dag.nodes[v]
        false_parents = [p for p in node.parents if dag.nodes[p].truth == 0]
        if node.truth == 1:
            x[v] = xstar[v] + sigma * rng.standard_normal(d)
            kind[v] = "true"
        elif false_parents and rng.random() < q_consistent:
            p = false_parents[int(rng.integers(len(false_parents)))]
            x[v] = R[(p, v)] @ x[p] + sigma * rng.standard_normal(d)
            kind[v] = "propagated_consistent"
        else:
            z = rng.standard_normal(d)
            # fabricated error with norm a*sqrt(d) (noise has expected norm sigma*sqrt(d))
            x[v] = xstar[v] + a * np.sqrt(d) * z / np.linalg.norm(z)
            kind[v] = "originating" if not false_parents else "propagated_fresh"
    return x, R, kind


# ---------------------------------------------------------------- scores
def repair_scores(dag, x, R, edge_list, d):
    inc = {v: [] for v in dag.nodes}
    energy = {}
    for (u, v, _t) in edge_list:
        r = R[(u, v)] @ x[u] - x[v]
        energy[(u, v)] = float(r @ r)
        inc[u].append(("out", u, v))
        inc[v].append(("in", u, v))
    dE, local = {}, {}
    for v in dag.nodes:
        if not inc[v]:
            dE[v], local[v] = 0.0, 0.0
            continue
        AtA = np.zeros((d, d))
        Atb = np.zeros(d)
        E_now = 0.0
        for (direction, u, w) in inc[v]:
            if direction == "in":           # edge u -> v : || I y - R x_u ||^2
                A, b = np.eye(d), R[(u, w)] @ x[u]
            else:                            # edge v -> w : || R y - x_w ||^2
                A, b = R[(u, w)], x[w]
            AtA += A.T @ A
            Atb += A.T @ b
            E_now += energy[(u, w)]
        y = np.linalg.solve(AtA, Atb)
        E_best = 0.0
        for (direction, u, w) in inc[v]:
            if direction == "in":
                r = y - R[(u, w)] @ x[u]
            else:
                r = R[(u, w)] @ y - x[w]
            E_best += float(r @ r)
        dE[v] = E_now - E_best
        local[v] = E_now
    return dE, local, energy


def to_prob(scores, energy, d):
    s2 = np.median(list(energy.values())) / (2.0 * d) if energy else 1.0  # median edge energy ~ 2*d*sigma^2 under null
    s2 = max(s2, 1e-9)
    return {v: float(1.0 - np.exp(-max(s, 0.0) / (2.0 * s2 * d))) for v, s in scores.items()}


# ---------------------------------------------------------------- strategies
def topk(score, budget):
    return set(sorted(score, key=lambda v: (-score[v], v))[:budget])


def truth_greedy(dag, budget):
    """Truth-conditioned ceiling: greedily pick the false claim that newly quarantines the most."""
    false = set(dag.false_ids)
    chosen, covered = set(), set()
    for _ in range(budget):
        best, gain = None, -1
        for v in false - chosen:
            g = len((dag.descendants_ids(v) & false) - covered)
            if g > gain:
                best, gain = v, g
        if best is None:
            break
        chosen.add(best)
        covered |= dag.descendants_ids(best) & false
    return chosen


def run_trial(seed, cfg, budget):
    dag = dm.ClaimDAG(max_nodes=cfg["max_nodes"], base_error_rate=BASE_ERROR_RATE,
                      propagation_rate=PROPAGATION_RATE, extra_edge_prob=cfg["extra_edge_prob"], seed=seed,
                      overconfident=cfg.get("overconfident", False))
    rng = np.random.default_rng(10_000 + seed)
    random.seed(seed)
    d = cfg["d"]
    x, R, kind = build_sheaf_and_observations(dag, d, cfg["sigma"], cfg["a"], cfg["q_consistent"], rng)
    all_edges = edges_of(dag)
    tree_edges = [e for e in all_edges if e[2]]
    dE_dag, local_dag, en_dag = repair_scores(dag, x, R, all_edges, d)
    dE_tree, _, en_tree = repair_scores(dag, x, R, tree_edges, d)
    p_dag = to_prob(dE_dag, en_dag, d)
    p_tree = to_prob(dE_tree, en_tree, d)
    D = {v: 1 + dag.nodes[v].num_descendants for v in dag.nodes}
    # "boundary -> upstream" rule: a high-energy edge u->v marks the boundary of an inconsistent
    # region; since a caught false claim quarantines everything downstream, blame the upstream end u.
    p_edge = to_prob({e: en for e, en in en_dag.items()}, en_dag, d)
    upstream = {v: 0.0 for v in dag.nodes}
    for (u, v), pe in p_edge.items():
        upstream[u] = max(upstream[u], pe)
    p_conf = {v: dm.compute_predicted_error(v, dag, set()) for v in dag.nodes}

    strategies = {
        "Random": dm.strategy_random(dag, budget),
        "Uncertainty (repo)": dm.strategy_uncertainty(dag, budget),
        "Dependency-aware (repo)": dm.strategy_dependency_aware(dag, budget),
        "D only (structure)": topk({v: D[v] + 1e-6 * rng.random() for v in dag.nodes}, budget),
        "Conf x D": topk({v: p_conf[v] * D[v] for v in dag.nodes}, budget),
        "Sheaf-tree x D (chain-only)": topk({v: p_tree[v] * D[v] for v in dag.nodes}, budget),
        "Sheaf-DAG (no D)": topk(p_dag, budget),
        "Sheaf-DAG x D": topk({v: p_dag[v] * D[v] for v in dag.nodes}, budget),
        "Sheaf-DAG+Conf x D": topk({v: 0.5 * (p_dag[v] + p_conf[v]) * D[v] for v in dag.nodes}, budget),
        "Sheaf edge->upstream x D": topk({v: upstream[v] * D[v] for v in dag.nodes}, budget),
        "Naive incident energy x D": topk({v: to_prob(local_dag, en_dag, d)[v] * D[v] for v in dag.nodes}, budget),
        "Truth-greedy (ceiling)": truth_greedy(dag, budget),
    }
    if cfg.get("greedy_mc"):
        strategies["Greedy MC (repo)"] = dm.strategy_greedy_mc_lazy(dag, budget, n_simulations=100)
    rel = {name: dm.evaluate(dag, vs)["reliability"] for name, vs in strategies.items()}

    y = np.array([1 - dag.nodes[v].truth for v in dag.nodes])
    kinds = np.array([kind[v] for v in dag.nodes])
    node_scores = {"conf": p_conf, "sheaf_tree": dE_tree, "sheaf_dag": dE_dag, "incident_energy": local_dag, "upstream_edge": upstream}
    auc_rows = {}
    for name, sc in node_scores.items():
        s = np.array([sc[v] for v in dag.nodes])
        auc_rows[name] = {"all": s, "y": y, "kinds": kinds}
    return rel, auc_rows, {"n": len(dag.nodes), "n_false": int(y.sum()),
                           "n_multi_parent": dag.num_extra_edges,
                           "kinds": {k: int((kinds == k).sum()) for k in set(kinds)}}


def auc_summary(rows_list):
    out = {}
    for name in rows_list[0]:
        s = np.concatenate([r[name]["all"] for r in rows_list])
        y = np.concatenate([r[name]["y"] for r in rows_list])
        k = np.concatenate([r[name]["kinds"] for r in rows_list])
        res = {"all_false": float(roc_auc_score(y, s))}
        for sub in ["originating", "propagated_consistent", "propagated_fresh"]:
            m = (k == "true") | (k == sub)
            if (k == sub).sum() > 5:
                res[sub] = float(roc_auc_score((k[m] == sub).astype(int), s[m]))
        out[name] = res
    return out


def run_config(cfg, n_trials, budget):
    rels, aucs, meta = [], [], []
    for t in range(n_trials):
        r, a, m = run_trial(t, cfg, budget)
        rels.append(r); aucs.append(a); meta.append(m)
    names = list(rels[0])
    mat = np.array([[r[n] for n in names] for r in rels])
    mean = mat.mean(0)
    # paired bootstrap CI for Sheaf-DAG x D minus each other strategy
    rng = np.random.default_rng(0)
    i_ref = names.index("Sheaf-DAG x D")
    boots = rng.integers(0, n_trials, size=(2000, n_trials))
    diffs = {}
    for j, n in enumerate(names):
        if j == i_ref:
            continue
        dd = mat[:, i_ref] - mat[:, j]
        bm = dd[boots].mean(1)
        diffs[n] = {"mean": float(dd.mean()), "ci95": [float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))]}
    return {
        "config": cfg, "n_trials": n_trials, "budget": budget,
        "reliability_mean": {n: float(m) for n, m in zip(names, mean)},
        "reliability_sd": {n: float(s) for n, s in zip(names, mat.std(0))},
        "sheafDAGxD_minus_other": diffs,
        "node_auroc": auc_summary(aucs),
        "dag_stats": {"mean_nodes": float(np.mean([m["n"] for m in meta])),
                      "mean_false": float(np.mean([m["n_false"] for m in meta])),
                      "mean_multi_parent_nodes": float(np.mean([m["n_multi_parent"] for m in meta]))},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=100)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    n = 10 if args.quick else args.trials

    budget = 20  # the parent project's headline: 20 checks on an 80-claim DAG
    grid = []
    for oc in [False, True]:  # repo's default confidence model vs its 'overconfident' (unreliable self-report) mode
        base = dict(max_nodes=80, extra_edge_prob=0.15, d=8, sigma=1.0, a=2.0, q_consistent=0.9, overconfident=oc)
        for a in [0.5, 1.0, 2.0, 4.0]:          # fabrication size relative to noise (signal strength)
            grid.append(dict(base, a=a))
        for q in [0.5, 0.99]:                   # how often propagated errors are "consistently wrong"
            grid.append(dict(base, q_consistent=q))
        for p in [0.0, 0.4]:                    # tree (no cross edges) vs denser DAG
            grid.append(dict(base, extra_edge_prob=p))
    results = []
    t0 = time.time()
    for cfg in grid:
        res = run_config(cfg, n, budget)
        results.append(res)
        rm = res["reliability_mean"]
        print(f"oc={cfg['overconfident']} a={cfg['a']} q={cfg['q_consistent']} p_edge={cfg['extra_edge_prob']}  "
              + "  ".join(f"{k}={v:.3f}" for k, v in rm.items()), flush=True)
    # budget sweep at the base config
    sweep = {}
    for oc in [False, True]:
        base = dict(max_nodes=80, extra_edge_prob=0.15, d=8, sigma=1.0, a=2.0, q_consistent=0.9, overconfident=oc)
        sweep["overconfident" if oc else "default_conf"] = {
            b: run_config(base, n, b)["reliability_mean"] for b in [5, 10, 20, 30, 40]}
    with open(os.path.join(args.out, "sheaf_dag_results.json"), "w") as f:
        json.dump({"grid": results, "budget_sweep_base": sweep, "seconds": time.time() - t0}, f, indent=1)
    print("done in", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
