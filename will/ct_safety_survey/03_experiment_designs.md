# 03 — Top-5 experiment designs

[← back to README](README.md)

These come from the ranked shortlist in the [README](README.md#ranked-top-10-avenues) and the [catalog](02_avenues_catalog.md). Each is chosen to be (a) runnable by one undergrad, (b) defensible against the 2026 prior art (`bottman2026operadic`, `bottman2026operads`, `liu2026intent`), and (c) plugged into what Will already has: `will/project1` (cached MuSiQue runs, `delta_comp`, `06_budget.py`) and `dag_codes/`.

Cost figures use Will's own measurements: a 2-hop open-book question costs about 28 calls and about 66k prompt tokens with N=3, and every call is cached. "Free" means it reuses the cache or runs on local open models.

**Common protocol for all five** (from the project abstract; keep it):
- Detectors never see gold.
- Splits are by question.
- Paired bootstrap CIs are clustered by question.
- Analysis code is frozen before touching MuSiQue dev.
- Dumb baselines are always included: stated confidence, length/hops, self-consistency at matched call count, semantic entropy, and (new, required) **Operadic Consistency**.

---

## Design 1 — Distributional functoriality vs. Operadic Consistency (avenues A1 + A2 + A3 + P1)

**Why first:** Bottman, Liu & Richardson (NeurIPS 2026, `bottman2026operadic`) already publish "direct vs decomposed answer agreement on MuSiQue as a label-free signal." Will's paper cannot go out without a head-to-head, and the head-to-head is also his best shot at a distinct contribution.

- **Hypothesis H1′.** The distributional composition defect, computed (i) with the exact or sampled **Kleisli composite** (marginalising over bridges) and (ii) after **semantic clustering** of answers, adds error-predictive information beyond OC (greedy, token-F1), self-consistency and semantic entropy. *Secondary:* the divergence choice (TV vs JS vs arbitrage) matters less than (i) and (ii).
- **Data.** MuSiQue-Ans train `pilot100` and `scale300` (already cached), plus a **fresh held-out set** from MuSiQue dev (≥300 questions, 2–4 hops) for the confirmatory test. Add 2WikiMultiHopQA (`ho2020twowiki`) as a second dataset if budget allows.
- **Models.** The models already cached (gpt-4.1-mini, gpt-5.5), plus one open model run locally (Qwen2.5-7B-Instruct or Llama-3.1-8B on a free Colab GPU) so that a key-free replication exists.
- **Signals.**
  - `delta_comp` exact-match (current)
  - `delta_comp` semantic: cluster answers with a DeBERTa-MNLI bidirectional-entailment check, as in `farquhar2024semantic`
  - Kleisli `delta_comp`: for each sampled bridge y_i, sample N_z answers to g(y_i), so the stepwise distribution is a mixture over bridges
  - OC: Bottman et al.'s definition from their public code (greedy direct vs greedy decomposed, token-F1 ≥ 0.5)
  - semantic entropy
  - SC at matched calls
  - confidence
- **Metric.** AUROC/AUPRC for wrong final answer. ΔAUROC of a nested logistic model (baseline + OC + SE + SC → + delta variant), 5-fold out-of-fold. AUARC for selective prediction (OC's own metric).
- **Falsification.** If every distributional variant gives ΔAUROC CI overlapping 0 over OC+SE+SC on held-out dev, *for both models*, the distributional framing adds nothing. Then the paper's contribution must shift to Designs 2–3.
- **Cost.** OC adds 3 greedy calls per 2-hop question (1 direct + 2 stepwise). The Kleisli estimator with N_y=3 bridges × N_z=2 adds about 6 calls per hop pair; NLI clustering is local and free. On 300 new dev questions this is about 300 × (28 + 9) ≈ 11k calls per model, roughly 25% more than an existing scale300 run. On the cached sets, OC + NLI-quotient reanalysis costs about 3 calls per question.
- **Risks.** OC's greedy pair may already capture most of the signal. Semantic clustering errors could add noise. And reviewers will see this as incremental unless Designs 2–3 are attached.

## Design 2 — Consistency-guided verification on real claim DAGs (avenues O1 + S2 + S1)

**Why:** Allocation under a budget is the clearest differentiator from all prior art, which only *detects*. Pilot A (synthetic) found that a static sheaf score barely beats descendant count, because consistent-but-wrong cascades are invisible. So the design must test an **adaptive, boundary-aware** policy on **real** data.

- **Hypothesis H3′.** On real multi-hop claim graphs, an adaptive policy can beat `D`-only, dependency-aware and confidence-based rules in reliability at equal *total* cost (diagnostic calls + checks). The policy checks the claim at the upstream end of the highest-energy edge, then re-scores after each check, moving inward when a false claim is found.
- **Data.** MuSiQue 3–4 hop chains, which are already DAG-like through overlapping regions. 2WikiMultiHopQA "compositional / bridge-comparison" questions give genuine branching (two parents → one claim), which is what makes DAG edges informative.
- **Sheaf construction.**
  - Vertices are claims (step answers).
  - Edge data for a pair of claims sharing a region is the region's `delta_comp`, i.e. Robinson's consistency radius on TV-metric stalks (`robinson2020assignments`).
  - For diamonds (two routes to a node), also compute the cycle (H^1-type) component (avenue S3).
- **Policies.**
  - Random
  - uncertainty
  - dependency-aware (repo)
  - `D` only
  - Conf × D
  - static composition × D (Will's current `06_budget.py`)
  - adaptive boundary-walk (new)
  - learned baseline + composition
  - truth oracle
- **Metric.** Reliability at budgets 6%…63% of claims (the existing sweep). Also report the reliability vs *total cost* frontier for check cost c ∈ {10, 30, 100} LLM calls (Step 2 of Will's project1 README).
- **Falsification.** The adaptive policy does not beat `D` only by more than its CI at the headline budget on held-out data.
- **Cost.** Reuses cached probes. Adaptive policies are simulated offline from labels, so the evaluation is free, and new data costs about the same as a scale300 run.
- **Risks.**
  - MuSiQue chains are nearly linear, so DAG structure adds little (exactly what pilot A predicts). Use 2Wiki for branching.
  - The quarantine rule may over-reward structure, as in pilot A.

## Design 3 — Lax-functor aggregation for long chains (avenue A4)

**Why:** Will's exploratory finding is that `max` over sub-regions saturates on 3–4 hop chains while the full-chain score keeps its signal. A metric-enriched (lax) functor gives a principled aggregator and a falsifiable inequality. It costs **zero new calls**.

- **Hypothesis.** For a coherent model, the defect is subadditive, δ(full chain) ≤ Σ δ(adjacent regions), by the triangle inequality for TV through Kleisli composition. Two predictions follow:
  - (a) Questions that *violate* the bound (full-chain defect larger than the sum) are disproportionately wrong.
  - (b) The **slack** Σδ_regions − δ_full, or the full-chain δ alone, beats `max` as an error predictor.
- **Data.** The existing scale300 caches (gpt-4.1-mini, gpt-5.5; 3–4 hops). Then confirm on new dev questions collected in Design 1.
- **Metric.** Bound-violation rate. AUROC of {max, mean, sum, full-chain, slack, violation indicator}. ΔAUROC over the baseline predictor.
- **Baselines.** max (pre-registered), full-chain (exploratory winner), SC, confidence.
- **Falsification.** If the bound is violated at a rate indistinguishable from a shuffled-region null, the metric reading is not supported (likely because nested synthetic composites are not "the same" task). If neither slack nor violation beats full-chain, report that and keep full-chain.
- **Cost.** 0 calls for analysis; 0 GPU. About a day of coding.
- **Risks.**
  - Sub-region composites are synthetic nested questions, which Will found read poorly. They may not be "equivalent tasks", in which case the triangle inequality does not apply.
  - The bound needs a *common* answer space across regions; define it on the final-answer space only.

## Design 4 — A battery of categorical laws, including the dagger (avenues N2 + D1 + D3)

**Why:** Will's paper found that composition fades with scale. Different laws may carry signal at different scales. The reversal curse (`berglund2024reversal`) suggests the **dagger law** is badly violated and could be a cheap complementary detector. Pilot B shows the curse cleanly in a toy model.

- **Hypothesis.** Each law-violation score (composition δ, identity/paraphrase δ, negation involution, dagger round-trip, dagger-compatibility of composition) predicts errors. At least one law other than composition adds ΔAUROC > 0 over confidence + SC on each model.
- **Data.**
  - MuSiQue chains: for each hop r(a)=b, write the converse question r⁻¹(b)=? by template, then audit the templates.
  - ParaRel-style paraphrase templates (`elazar2021pararel`) for the identity law.
  - BECEL-style negation (`jang2022becel`).
- **Models.** Local open models across sizes: Qwen2.5 0.5B/1.5B/3B/7B, or Pythia 160m–1.4b. Open weights give exact next-token distributions for short answers, which removes sampling noise.
- **Metric.** Per-law AUROC; nested ΔAUROC; law-violation profile vs model size (avenue A5); correlation matrix between laws.
- **Falsification.** All non-composition laws have ΔAUROC CIs overlapping 0 at all sizes.
- **Cost.** About 5 extra prompts per hop. Open-model inference on a free T4 is ~1–3 h per model size for 300 questions; zero API cost.
- **Risks.**
  - Templated converses can be unnatural, which inflates dagger defects for reasons unrelated to knowledge. Audit them, and use relations with natural converses (parent/child, capital-of/has-capital).
  - With greedy answers, small models are mostly wrong.

## Design 5 — How much hallucination is consistent-but-false? (avenues A7 + P2)

**Why:** Every consistency detector (delta_comp, OC, semantic entropy, sheaf energy) has a blind spot: a model that is wrong *in a lawful way*. Pilot A shows consistently-propagated errors rank *below* true claims (AUROC 0.28). Will's scale300 data has 13–20 questions that are wrong with both routes agreeing. Measuring the size of this blind spot is directly safety-relevant: it bounds what consistency-based oversight can ever catch.

- **Hypothesis.**
  - A non-trivial fraction of errors (≥20%) is consistent: delta_comp ≈ 0 and low semantic entropy.
  - That fraction grows with model capability (gpt-5.5 > gpt-4.1-mini) and in closed-book settings.
  - In the 2×2 of {deterministic vs uncertain} × {functorial vs non-functorial} (P2), the "deterministic and functorial but wrong" cell holds most closed-book errors.
- **Data.**
  - Existing caches (open- and closed-book).
  - A small adversarial set: TruthfulQA misconceptions (`lin2022truthfulqa`) chained into 2-hop questions, e.g. "What is the capital of the country where [misconception-laden entity] is located?".
  - The synthetic KG with planted false facts (pilot B world, extended).
- **Metric.**
  - Error rate per quadrant.
  - The recall ceiling of consistency detectors (the share of errors with δ below threshold).
  - How the ceiling changes with model and condition.
- **Baselines.** Semantic entropy (`farquhar2024semantic`); verbalised confidence. Neither should rescue the consistent-wrong quadrant, which is part of the hypothesis.
- **Falsification.** If the consistent-wrong share is below 10% everywhere, the blind spot is small. That is good news and still worth reporting.
- **Cost.** About 0 for the reanalysis. The adversarial set of about 100 chains × 28 calls ≈ 3k calls per model, or free on an open model.
- **Risks.** The threshold choice for "consistent" is arbitrary, so report curves rather than a single threshold. The TruthfulQA chains need careful hand-writing.

---

### Where the pilots fit
- **Pilot A** ([pilots/sheaf_dag](pilots/sheaf_dag/README.md)) informs Design 2. A static sheaf score is not enough; structure dominates; adaptivity and branching data are needed.
- **Pilot B** ([pilots/synthetic_kg](pilots/synthetic_kg/README.md)) informs Designs 1, 4 and 5. It gives exact Kleisli composites, the reversal curse, the consistent-but-wrong fraction, and a toy LRE functoriality test.
