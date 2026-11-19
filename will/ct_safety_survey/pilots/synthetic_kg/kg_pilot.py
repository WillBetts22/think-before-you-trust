"""
Pilot B: functoriality, duality and linear-relational composition in a tiny transformer
trained from scratch on a synthetic knowledge graph (CPU, no downloads, no API keys).

Why synthetic: this sandbox cannot reach Hugging Face, so no pretrained LM is available.
A model trained from scratch lets us know the gold answer of every query and compute
*exact* answer distributions (no sampling), which is impossible with API models.

World
-----
N entities, R relations. Each relation r is a random permutation t_r of the entities
(a bijection, so it has an inverse r^-1). Entity "popularity" is Zipf-distributed, and
training facts are sampled in proportion to popularity, so rare entities are learned
worse (a crude stand-in for long-tail hallucination).

Queries are 3 tokens [e, r1, r2]; r2 = NOOP for one-hop queries. The model outputs a
distribution over entities. Training data:
  * all one-hop facts (e, r)            -> t_r(e)
  * inverse facts (t_r(e), r^-1)        -> e      for a random half of the (e, r) pairs
  * two-hop facts (e, r1, r2)           -> t_r2(t_r1(e)) for a random TRAIN_2HOP fraction of triples
Held-out two-hop triples are the test set for composition.

Experiments (all gold-free scores, gold only for labels)
-------------------------------------------------------
E1 functoriality / Kleisli composition:
    P_direct  = model(e, r1, r2)
    P_step    = sum_y model(y | e, r1) * model(. | y, r2)       (exact composite of Markov kernels)
    delta_comp = TV(P_direct, P_step); also the sampled estimator with N=3 per route as in project1.
    H1 analogue: does delta_comp predict a wrong direct answer beyond confidence/entropy/step-confidence?
E2 duality (reversal):
    accuracy of r^-1 queries on pairs never trained in reverse (the "reversal curse");
    round-trip score rho = sum_t P(t | e, r) P(e | t, r^-1) as an error signal for forward facts.
E3 linear-relational functor:
    fit a ridge-regression linear map A_r on output-embedding space (u_e -> u_{model answer}),
    and A_{r1 r2} on the model's direct two-hop answers; is A_{r2} A_{r1} close to A_{r1 r2}
    compared with mismatched relation pairs (null)?

Usage: python kg_pilot.py [--seeds 0 1 2] [--quick]
"""
import argparse
import json
import math
import os
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ world
class World:
    def __init__(self, n_ent, n_rel, train_2hop, seed, zipf=1.0):
        rng = np.random.default_rng(seed)
        self.N, self.R = n_ent, n_rel
        self.perm = np.stack([rng.permutation(n_ent) for _ in range(n_rel)])  # perm[r, e] = t_r(e)
        self.inv = np.argsort(self.perm, axis=1)                                 # inv[r, t] = e
        ranks = rng.permutation(n_ent) + 1
        self.pop = 1.0 / ranks ** zipf                                           # Zipf popularity
        self.pop /= self.pop.sum()
        # token ids
        self.NOOP = n_ent + 2 * n_rel
        self.vocab = n_ent + 2 * n_rel + 1
        rel_tok = lambda r: n_ent + r
        inv_tok = lambda r: n_ent + n_rel + r
        self.rel_tok, self.inv_tok = rel_tok, inv_tok
        # one-hop
        E, Rr = np.meshgrid(np.arange(n_ent), np.arange(n_rel), indexing="ij")
        E, Rr = E.ravel(), Rr.ravel()
        self.one_x = np.stack([E, rel_tok(Rr), np.full_like(E, self.NOOP)], 1)
        self.one_y = self.perm[Rr, E]
        self.one_w = self.pop[E]
        # inverse facts for a random half of (e, r)
        rev_mask = rng.random(len(E)) < 0.5
        self.rev_trained = rev_mask.reshape(n_ent, n_rel)
        T = self.perm[Rr, E]
        self.inv_x_all = np.stack([T, inv_tok(Rr), np.full_like(E, self.NOOP)], 1)
        self.inv_y_all = E
        self.inv_x, self.inv_y = self.inv_x_all[rev_mask], self.inv_y_all[rev_mask]
        self.inv_w = self.pop[E][rev_mask]
        # two-hop
        E3, R1, R2 = np.meshgrid(np.arange(n_ent), np.arange(n_rel), np.arange(n_rel), indexing="ij")
        E3, R1, R2 = E3.ravel(), R1.ravel(), R2.ravel()
        two_x = np.stack([E3, rel_tok(R1), rel_tok(R2)], 1)
        two_y = self.perm[R2, self.perm[R1, E3]]
        tr = rng.random(len(E3)) < train_2hop
        self.two_x_tr, self.two_y_tr, self.two_w_tr = two_x[tr], two_y[tr], self.pop[E3][tr]
        self.two_x_te, self.two_y_te = two_x[~tr], two_y[~tr]
        self.two_meta_te = np.stack([E3[~tr], R1[~tr], R2[~tr]], 1)
        self.two_meta_tr = np.stack([E3[tr], R1[tr], R2[tr]], 1)

    def train_pool(self):
        x = np.concatenate([self.one_x, self.inv_x, self.two_x_tr])
        y = np.concatenate([self.one_y, self.inv_y, self.two_y_tr])
        w = np.concatenate([self.one_w, self.inv_w, self.two_w_tr])
        # mixture: popularity-weighted within each block, blocks weighted by size
        return x, y, w / w.sum()


# ------------------------------------------------------------------ model
class TinyEncoder(nn.Module):
    def __init__(self, vocab, n_ent, d=128, layers=2, heads=4):
        super().__init__()
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Parameter(torch.randn(3, d) * 0.02)
        layer = nn.TransformerEncoderLayer(d, heads, 4 * d, dropout=0.0, batch_first=True, norm_first=True)
        self.enc = nn.TransformerEncoder(layer, layers, enable_nested_tensor=False)
        self.ln = nn.LayerNorm(d)
        self.out = nn.Linear(d, n_ent)

    def hidden(self, x):
        h = self.enc(self.tok(x) + self.pos)
        return self.ln(h[:, -1])

    def forward(self, x):
        return self.out(self.hidden(x))


@torch.no_grad()
def probs(model, x, bs=8192):
    out = []
    for i in range(0, len(x), bs):
        out.append(F.softmax(model(torch.as_tensor(x[i:i + bs])), -1).numpy())
    return np.concatenate(out)


def train(world, steps, seed, checkpoints, d=128, layers=2, lr=1e-3, bs=512, wd=0.01):
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed + 1)
    model = TinyEncoder(world.vocab, world.N, d=d, layers=layers)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    x, y, w = world.train_pool()
    xt, yt = torch.as_tensor(x), torch.as_tensor(y)
    snaps = {}
    for step in range(1, steps + 1):
        idx = torch.as_tensor(rng.choice(len(x), size=bs, p=w))
        loss = F.cross_entropy(model(xt[idx]), yt[idx])
        opt.zero_grad(); loss.backward(); opt.step()
        if step in checkpoints:
            snaps[step] = {k: v.clone() for k, v in model.state_dict().items()}
    return model, snaps


# ------------------------------------------------------------------ helpers
def tv(p, q):
    return 0.5 * np.abs(p - q).sum(-1)


def entropy(p):
    return -(p * np.log(p + 1e-12)).sum(-1)


def safe_auc(y, s):
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(roc_auc_score(y, s))


def h1_gain(X_base, x_extra, y, seed=0, n_boot=1000):
    """5-fold out-of-fold AUROC of logistic regression: baseline vs baseline + extra feature."""
    if len(np.unique(y)) < 2 or min(np.bincount(y)) < 10:
        return None
    skf = StratifiedKFold(5, shuffle=True, random_state=seed)
    Xa = np.column_stack([X_base, x_extra])
    pb, pa = np.zeros(len(y)), np.zeros(len(y))
    for tr, te in skf.split(X_base, y):
        for X, p in [(X_base, pb), (Xa, pa)]:
            mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
            clf = LogisticRegression(max_iter=2000).fit((X[tr] - mu) / sd, y[tr])
            p[te] = clf.predict_proba((X[te] - mu) / sd)[:, 1]
    a_b, a_a = roc_auc_score(y, pb), roc_auc_score(y, pa)
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        if len(np.unique(y[i])) < 2:
            continue
        diffs.append(roc_auc_score(y[i], pa[i]) - roc_auc_score(y[i], pb[i]))
    return {"auc_base": float(a_b), "auc_aug": float(a_a), "gain": float(a_a - a_b),
            "ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))]}


def sample_counts(p, n, rng):
    """Empirical distribution of n samples from each row of p."""
    c = np.cumsum(p, 1)
    u = rng.random((p.shape[0], n))
    idx = np.minimum((u[:, :, None] > c[:, None, :]).sum(-1), p.shape[1] - 1)
    emp = np.zeros_like(p)
    for j in range(n):
        emp[np.arange(len(p)), idx[:, j]] += 1.0 / n
    return emp, idx


# ------------------------------------------------------------------ experiments
def exp_composition(model, world, rng, split="heldout", max_test=6000):
    if split == "heldout":
        X, Y, M = world.two_x_te, world.two_y_te, world.two_meta_te
    else:  # two-hop facts that WERE in the training pool (seen, possibly imperfectly memorised)
        X, Y, M = world.two_x_tr, world.two_y_tr, world.two_meta_tr
    te = np.arange(len(X))
    if len(te) > max_test:
        te = rng.choice(te, max_test, replace=False)
    x, y, meta = X[te], Y[te], M[te]
    P_dir = probs(model, x)
    # one-hop kernels for every (entity, relation): K[r] is an N x N row-stochastic matrix
    K = probs(model, world.one_x).reshape(world.N, world.R, world.N).transpose(1, 0, 2)
    e, r1, r2 = meta[:, 0], meta[:, 1], meta[:, 2]
    P1 = K[r1, e]                                          # P(y | e, r1)
    P_step = np.zeros_like(P_dir)                          # exact Kleisli composite sum_y P1(y) K[r2](y, z)
    for rr in range(world.R):
        m = r2 == rr
        P_step[m] = P1[m] @ K[rr]
    y_hat_dir = P_dir.argmax(1)
    err = (y_hat_dir != y).astype(int)
    step_err = (P_step.argmax(1) != y).astype(int)
    bridge = P1.argmax(1)
    hop1_wrong = (bridge != world.perm[r1, e]).astype(int)
    hop2_wrong = (K[r2, bridge].argmax(1) != world.perm[r2, bridge]).astype(int)
    d_exact = tv(P_dir, P_step)
    # sampled estimator as in project1 (N=3 per route; stepwise samples y then z)
    out_sampled = {}
    for n in [3, 10]:
        emp_d, _ = sample_counts(P_dir, n, rng)
        emp_s = np.zeros_like(P_dir)
        for _ in range(n):
            _, yi = sample_counts(P1, 1, rng)
            _, zi = sample_counts(K[r2, yi[:, 0]], 1, rng)
            emp_s[np.arange(len(x)), zi[:, 0]] += 1.0 / n
        emp_sc, _ = sample_counts(P_dir, 3 * n, rng)
        out_sampled[n] = {"delta": tv(emp_d, emp_s), "sc": 1 - emp_sc.max(1)}
    conf = P_dir.max(1)
    ent = entropy(P_dir)
    c1 = P1.max(1)
    c2 = K[r2, bridge].max(1)
    feats = {
        "neg_conf_direct": -conf, "entropy_direct": ent, "neg_conf_hop1": -c1, "neg_conf_hop2": -c2,
        "delta_comp_exact": d_exact, "delta_comp_N3": out_sampled[3]["delta"], "delta_comp_N10": out_sampled[10]["delta"],
        "selfcons_3N_N3": out_sampled[3]["sc"],
    }
    res = {
        "n_test": int(len(x)), "direct_error_rate": float(err.mean()), "stepwise_error_rate": float(step_err.mean()),
        "hop1_error_rate": float(hop1_wrong.mean()), "hop2_error_rate_given_bridge": float(hop2_wrong.mean()),
        "compositionality_gap": float(err[(hop1_wrong == 0) & (hop2_wrong == 0)].mean()) if ((hop1_wrong == 0) & (hop2_wrong == 0)).any() else float("nan"),
        "mean_delta_exact": float(d_exact.mean()),
        "single_auroc": {k: safe_auc(err, v) for k, v in feats.items()},
    }
    base = np.column_stack([-conf, ent, -c1, -c2])
    res["h1_exact"] = h1_gain(base, d_exact, err)
    res["h1_N3_vs_selfcons"] = h1_gain(np.column_stack([-conf, ent, -c1, -c2, out_sampled[3]["sc"]]), out_sampled[3]["delta"], err)
    # consistent-but-wrong: routes agree (delta<0.1) yet wrong
    agree = d_exact < 0.1
    res["frac_wrong_among_agreeing"] = float(err[agree].mean()) if agree.any() else float("nan")
    res["frac_agreeing"] = float(agree.mean())
    return res


def exp_duality(model, world):
    P_inv_all = probs(model, world.inv_x_all)
    acc_inv = (P_inv_all.argmax(1) == world.inv_y_all)
    rev = world.rev_trained.ravel()
    P_fwd = probs(model, world.one_x)
    fwd_err = (P_fwd.argmax(1) != world.one_y).astype(int)
    # round trip: sum_t P(t | e, r) P(e | t, r^-1); need P(. | t, r^-1) for every t, r
    N, R = world.N, world.R
    T, Rr = np.meshgrid(np.arange(N), np.arange(R), indexing="ij")
    xq = np.stack([T.ravel(), world.inv_tok(Rr.ravel()), np.full(N * R, world.NOOP)], 1)
    Pi = probs(model, xq).reshape(N, R, N)                          # Pi[t, r, e]
    E = world.one_x[:, 0]
    Rel = world.one_x[:, 1] - world.N
    rho = np.einsum("bt,bt->b", P_fwd, Pi[:, Rel, E].T)             # sum_t P(t|e,r) P(e|t,r^-1)
    out = {
        "fwd_acc": float(1 - fwd_err.mean()),
        "inv_acc_trained_pairs": float(acc_inv[rev].mean()),
        "inv_acc_untrained_pairs (reversal curse)": float(acc_inv[~rev].mean()),
        "chance": 1.0 / N,
        "mean_roundtrip_trained": float(rho[rev].mean()),
        "mean_roundtrip_untrained": float(rho[~rev].mean()),
    }
    for name, m in [("trained", rev), ("untrained", ~rev)]:
        y = fwd_err[m]
        out[f"auroc_fwd_error_neg_conf_{name}"] = safe_auc(y, -P_fwd.max(1)[m])
        out[f"auroc_fwd_error_one_minus_roundtrip_{name}"] = safe_auc(y, 1 - rho[m])
        g = h1_gain(np.column_stack([-P_fwd.max(1)[m], entropy(P_fwd)[m]]), 1 - rho[m], y)
        out[f"h1_roundtrip_{name}"] = g
    return out


def ridge(X, Y, lam=1e-2):
    Xa = np.column_stack([X, np.ones(len(X))])
    W = np.linalg.solve(Xa.T @ Xa + lam * np.eye(Xa.shape[1]), Xa.T @ Y)
    return W  # (d+1) x d


def apply_aff(W, X):
    return np.column_stack([X, np.ones(len(X))]) @ W


def nn_acc(pred, U, target_idx):
    Un = U / np.linalg.norm(U, axis=1, keepdims=True)
    pn = pred / (np.linalg.norm(pred, axis=1, keepdims=True) + 1e-12)
    return float(((pn @ Un.T).argmax(1) == target_idx).mean())


def exp_linear_functor(model, world, rng):
    """Relations as linear maps on two entity spaces: output embeddings (unembedding rows) and input embeddings."""
    out = {}
    P1 = probs(model, world.one_x).reshape(world.N, world.R, world.N)
    ans1 = P1.argmax(-1)                                          # model's one-hop answers  [e, r]
    for space_name, U in [("unembedding", model.out.weight.detach().numpy()),
                          ("input_embedding", model.tok.weight.detach().numpy()[: world.N])]:
        ents = np.arange(world.N)
        half = rng.permutation(world.N)
        fit_idx, ev_idx = half[: world.N // 2], half[world.N // 2:]
        A = {}
        faith = []
        for r in range(world.R):
            A[r] = ridge(U[fit_idx], U[ans1[fit_idx, r]])
            faith.append(nn_acc(apply_aff(A[r], U[ev_idx]), U, ans1[ev_idx, r]))
        # two-hop maps from the model's own direct answers on all (e, r1, r2) (train + test triples)
        pairs = [(a, b) for a in range(world.R) for b in range(world.R)]
        rels = rng.choice(len(pairs), min(16, len(pairs)), replace=False)
        defect, null_defect, comp_acc, direct_acc, null_acc = [], [], [], [], []
        for k in rels:
            r1, r2 = pairs[k]
            xq = np.stack([ents, np.full(world.N, world.rel_tok(r1)), np.full(world.N, world.rel_tok(r2))], 1)
            ans2 = probs(model, xq).argmax(1)
            A12 = ridge(U[fit_idx], U[ans2[fit_idx]])
            comp = lambda X: apply_aff(A[r2], apply_aff(A[r1], X))
            # null: a mismatched pair (r1', r2') != (r1, r2)
            r1n, r2n = (r1 + 1 + rng.integers(world.R - 1)) % world.R, (r2 + 1 + rng.integers(world.R - 1)) % world.R
            compn = lambda X: apply_aff(A[r2n], apply_aff(A[r1n], X))
            Xe = U[ev_idx]
            tgt = apply_aff(A12, Xe)
            defect.append(float(np.linalg.norm(comp(Xe) - tgt) / np.linalg.norm(tgt)))
            null_defect.append(float(np.linalg.norm(compn(Xe) - tgt) / np.linalg.norm(tgt)))
            comp_acc.append(nn_acc(comp(Xe), U, ans2[ev_idx]))
            direct_acc.append(nn_acc(tgt, U, ans2[ev_idx]))
            null_acc.append(nn_acc(compn(Xe), U, ans2[ev_idx]))
        out[space_name] = {
            "one_hop_faithfulness_mean": float(np.mean(faith)),
            "functoriality_defect_mean": float(np.mean(defect)),
            "null_defect_mean": float(np.mean(null_defect)),
            "composed_map_nn_acc_vs_model_2hop": float(np.mean(comp_acc)),
            "direct_2hop_map_nn_acc": float(np.mean(direct_acc)),
            "null_composed_nn_acc": float(np.mean(null_acc)),
            "chance": 1.0 / world.N,
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--n_ent", type=int, default=1000)
    ap.add_argument("--n_rel", type=int, default=6)
    ap.add_argument("--train_2hop", type=float, default=0.3)
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--zipf", type=float, default=1.0)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    args = ap.parse_args()
    torch.set_num_threads(args.threads)
    if args.quick:
        args.seeds, args.steps = [0], 800
    os.makedirs(args.out, exist_ok=True)
    ckpts = sorted({args.steps // 8, args.steps // 4, args.steps // 2, args.steps})
    all_res = {"args": vars(args), "checkpoints": ckpts, "runs": []}
    t0 = time.time()
    for seed in args.seeds:
        world = World(args.n_ent, args.n_rel, args.train_2hop, seed, zipf=args.zipf)
        model, snaps = train(world, args.steps, seed, set(ckpts))
        for step in ckpts:
            model.load_state_dict(snaps[step])
            model.eval()
            rng = np.random.default_rng(100 + seed)
            r = {"seed": seed, "step": step,
                 "composition": exp_composition(model, world, rng, split="seen"),
                 "composition_heldout": exp_composition(model, world, rng, split="heldout", max_test=3000),
                 "duality": exp_duality(model, world),
                 "linear_functor": exp_linear_functor(model, world, rng)}
            all_res["runs"].append(r)
            c = r["composition"]
            print(f"seed={seed} step={step} t={time.time()-t0:.0f}s fwd_acc={r['duality']['fwd_acc']:.3f} "
                  f"direct_err={c['direct_error_rate']:.3f} step_err={c['stepwise_error_rate']:.3f} "
                  f"AUROC conf={c['single_auroc']['neg_conf_direct']:.3f} dcomp={c['single_auroc']['delta_comp_exact']:.3f} "
                  f"h1={None if c['h1_exact'] is None else round(c['h1_exact']['gain'],3)} "
                  f"rev_untrained={r['duality']['inv_acc_untrained_pairs (reversal curse)']:.3f}", flush=True)
            with open(os.path.join(args.out, "kg_results_seeds_" + "_".join(map(str, args.seeds)) + ".json"), "w") as f:
                json.dump(all_res, f, indent=1)
    print("done in", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
