# 04 — Small, sharp questions (1–2 week projects / workshop papers)

[← back to README](README.md)

Each question has a yes/no or a single number as its answer, needs at most a few thousand API calls or a free GPU, and maps to a catalog avenue. Questions marked ★ can be answered with **no new LLM calls** by re-analysing Will's cached `will/project1` runs.

| # | Question | Avenue | What you'd compute | Cost |
|---:|---|---|---|---|
| 1 ★ | Does **Operadic Consistency** (greedy direct vs decomposed, token-F1) already capture what `delta_comp` captures on Will's MuSiQue runs? | A1 | OC from the first sample of each route (an approximation of greedy); ΔAUROC of delta_comp over OC | cache only (exact OC needs ~3 greedy calls/q) |
| 2 ★ | How much of `delta_comp` is answer-string mismatch? Recompute it after NLI or alias clustering of answers. | A3 | AUROC(exact) vs AUROC(semantic); share of "disagreements" that vanish | local DeBERTa-MNLI |
| 3 ★ | Is the composition defect subadditive along 3–4 hop chains (δ_full ≤ Σ δ_regions)? Does violating it predict error? | A4 | violation rate; AUROC of slack / violation | cache only |
| 4 ★ | Which divergence predicts errors best: TV, Jensen–Shannon, Hellinger, or Paleka-style arbitrage? | P1 | AUROC per divergence on identical samples | cache only |
| 5 ★ | What fraction of errors is **consistent-but-wrong** (both routes agree), by model and open vs closed book? | A7 | share of errors with δ < τ for a sweep of τ | cache only |
| 6 ★ | Does `delta_comp` add more for **low-confidence** or for **high-confidence** errors? (Confidently-wrong is the safety-critical case.) | P2 | ΔAUROC within confidence terciles | cache only |
| 7 | Does the stepwise distribution computed as a proper **Kleisli mixture** over several sampled bridges beat plugging in one sampled bridge? | A2 | AUROC for both estimators at equal call count | ~6 calls/q |
| 8 | Is the **dagger law** violated more on questions the model gets wrong? (Ask r⁻¹(b) for each hop.) | D1 | ΔAUROC of round-trip score over delta_comp | ~2 calls/hop, or free on open models |
| 9 | For relations with natural converses, is (g∘f)† answered as f†∘g†? (Reverse two-hop.) | D3 | reversed-composite defect | ~6 calls/q |
| 10 ★ | Does **descendant count alone** match the parent project's dependency-aware rule on Will's *real* chains, as it did in the simulator (pilot A)? | S2/O1 | reliability of `D`-only in `06_budget.py` | cache only |
| 11 | In `dag_codes`, does replacing D̂ with **d-separation-aware** damage (descendants not screened off by verified claims) improve adaptive reliability? | P5 | reliability vs current adaptive policy | CPU minutes |
| 12 | In `dag_codes`, can a **sound three-valued abstract interpretation** (true / false / unknown, propagated with the max rule) decide some claims for free and save checks? | G1 | checks saved at equal reliability | CPU minutes |
| 13 ★ | Given a verifier's "final answer wrong", does **Bayesian-lens blame** (inverting the chain) pick the false hop better than "check the lowest-confidence hop"? | L1 | top-1 localisation accuracy on MuSiQue labels | cache only |
| 14 | Do **fabricated entities** (invented names) produce a less coherent relation profile (composition plus dagger checks) than real but rare entities? | Y1 | AUROC real vs fabricated from profile coherence | free on open models |
| 15 | In a tiny transformer trained on a synthetic KG, does `delta_comp` predict errors **better early in training** (weak model) than late? This tests Will's "signal fades with capability" pattern under controlled conditions. | A5 | ΔAUROC per checkpoint (pilot B has a first answer) | CPU |
| 16 | Do **linear relational maps** compose (W_g W_f ≈ W_{g∘f}) in a small open LM such as GPT-2 or Qwen2.5-0.5B, using the Hernandez et al. LRE recipe? | A9 | composed-map faithfulness vs direct LRE vs mismatched null | free GPU, ~1 day |
| 17 | Does the **H^1 / cycle component** (two routes into one claim disagreeing in a way no single repair fixes) ever appear in real 2Wiki "comparison" questions, or is all inconsistency plain local disagreement? | S3 | fraction of questions with nonzero harmonic component | ~20 calls/q |
| 18 ★ | Does **join emptiness** of the top-3 answers across sub-questions (a discrete gluing test) detect errors as well as TV-based delta_comp? | S7 | AUROC of join-based score | cache only (top-k from samples) |

### Suggested order
1. Questions 1, 2, 3, 5 and 10 use only the cache, should take about a week in total, and directly strengthen Will's paper against the prior art.
2. Then 7 and 8, which add new calls but are cheap.
3. Then 11, 12 and 13, which extend the parent project's simulator.
4. The rest are side quests.
