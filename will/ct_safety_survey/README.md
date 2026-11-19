# Category theory × AI safety: a research-avenue survey with pilot experiments

**Summary.** This folder maps where a category-theory lens could do real work in AI-safety research, starting from Will's current project (composition inconsistency `delta_comp` as a hallucination signal, plus the parent project's budgeted claim-DAG verification) and building outward.

It contains:
- a literature map of **152 works** in six clusters
- a catalog of **50 scored research avenues**, each tied to one categorical concept
- **5 concrete experiment designs**
- **18 small, sharp questions**
- a CT primer restricted to the concepts used here
- **two CPU-only pilots with four experiments**

**Most important finding (do this first):** two 2026 papers already publish the core of Will's test. Bottman, Liu & Richardson's *Operadic consistency* (arXiv 2606.13649) compares direct vs decomposed answers on MuSiQue and three other datasets as a label-free signal, with an operad-theoretic companion paper. Liu et al. 2026 states "chain-of-search" functoriality for research agents. Will's defensible ground is now:
1. the *distributional* (Kleisli, semantic-quotient) version of the test, measured head to head against Operadic Consistency;
2. principled aggregation over long chains;
3. using consistency to **allocate a verification budget**, which no prior work found does.

The pilots are preliminary and run on simulators or tiny from-scratch models. They mostly **temper** the optimistic stories: structure dominates the budget metric, and consistently-wrong claims are invisible to every consistency score.

> ⚠️ **Read [CHANGELOG_or_NOTES.md](CHANGELOG_or_NOTES.md) before citing anything.** The sandbox could not open arXiv or publisher pages. Citations were confirmed through web-search listings (title, authors and canonical URL), not by reading the papers. Numbers quoted from papers must be re-checked against the PDFs.

## Contents

| File | What it is |
|---|---|
| [01_literature_map.md](01_literature_map.md) | 152 works in 6 clusters, each with citation, URL, summary, "why it matters for us", and a [READ-FIRST]/[RECOMMENDED]/[REFERENCE] tag |
| [02_avenues_catalog.md](02_avenues_catalog.md) | 50 avenues, each tied to one CT concept, scored on feasibility, novelty, safety relevance, connection to Will's pipeline and time-to-result |
| [03_experiment_designs.md](03_experiment_designs.md) | 1-page designs for the top 5 (hypothesis, data, models, metrics, baselines, falsification, cost, risks) |
| [04_small_questions.md](04_small_questions.md) | 18 one-to-two-week questions; 9 need **no new LLM calls** (they re-analyse Will's cache) |
| [05_category_theory_primer.md](05_category_theory_primer.md) | The CT concepts used here, each with an ML/safety example and where to learn it |
| [references.bib](references.bib) | BibTeX for all 152 works |
| [pilots/sheaf_dag/](pilots/sheaf_dag/README.md) | Pilot A: sheaf-Laplacian inconsistency for budgeted verification on `dag_codes` DAGs |
| [pilots/synthetic_kg/](pilots/synthetic_kg/README.md) | Pilot B: functoriality (exact Kleisli), duality (reversal) and linear-relational functoriality in a tiny transformer trained on a synthetic KG |
| [CHANGELOG_or_NOTES.md](CHANGELOG_or_NOTES.md) | What was done, what could not be verified, dead ends |
| [tools/avenues.py](tools/avenues.py) | Source of truth for the catalog: edit scores there and regenerate |

## START HERE: 10 papers, in this order

| # | Paper | Why read it (and why at this point) |
|---:|---|---|
| 1 | Bottman, Liu, Richardson 2026, *Operadic consistency: a label-free signal for compositional reasoning failures in LLMs* — [arXiv:2606.13649](https://arxiv.org/abs/2606.13649) | **The closest prior art.** Direct vs decomposed agreement on MuSiQue, HotpotQA, StrategyQA and DROP as a label-free signal, across 12 models. You must position against it before anything else. Its public code uses greedy answers, token-F1 and depth 2. |
| 2 | Bottman & Richardson 2026, *Operads for compositional reasoning in LLMs* — [arXiv:2606.13634](https://arxiv.org/abs/2606.13634) | The theory companion: QA systems as algebras over a "questions operad". Read before writing your formal section, so you choose a framing that is different (functor into Stoch, metric enrichment) rather than a re-derivation. |
| 3 | Chen et al. 2024, *Two Failures of Self-Consistency in the Multi-Step Reasoning of LLMs* (TMLR) — [arXiv:2305.14279](https://arxiv.org/abs/2305.14279) | The empirical origin of "compositional consistency". You already cite it. Re-read it for what exactly it measured. |
| 4 | Press et al. 2023, *Measuring and Narrowing the Compositionality Gap in Language Models* (Findings of EMNLP) — [arXiv:2210.03350](https://arxiv.org/abs/2210.03350) | The gold-label version of your quantity, and the evidence that the gap does not shrink with scale. |
| 5 | Farquhar et al. 2024, *Detecting hallucinations in large language models using semantic entropy* (Nature) — [doi:10.1038/s41586-024-07421-0](https://doi.org/10.1038/s41586-024-07421-0) | The baseline reviewers will demand, and the semantic-clustering trick that fixes your exact-match answer identity. |
| 6 | Fritz 2020, *A synthetic approach to Markov kernels, conditional independence and theorems on sufficient statistics* — [arXiv:1908.07021](https://arxiv.org/abs/1908.07021) | §1–4 only. The right category for stochastic LLM "hops". The stepwise route should be the **Kleisli composite** Σ_y P(z\|y)P(y\|x), and `delta_comp` is a composition defect in Stoch. |
| 7 | Rischel & Weichwald 2021, *Compositional Abstraction Error and a Category of Causal Models* (UAI) — [PMLR v161](https://proceedings.mlr.press/v161/rischel21a.html) | A worked example of a metric-valued "failure to commute" that **composes with a bound**. This is the template for a principled aggregator over chain regions (Design 3). |
| 8 | Hansen & Ghrist 2019, *Toward a Spectral Theory of Cellular Sheaves* — [arXiv:1808.01513](https://arxiv.org/abs/1808.01513) | Sheaf Laplacians and Dirichlet energy: the tool for going from chains to DAGs (pilot A, Design 2). |
| 9 | Robinson 2020, *Assignments to sheaves of pseudometric spaces* (Compositionality) — [journal page](https://compositionality.episciences.org/13508) | The consistency radius: the metric (non-linear) sheaf inconsistency that `delta_comp` is a special case of. |
| 10 | Fluri, Paleka & Tramèr 2023, *Evaluating Superhuman Models with Consistency Checks* — [arXiv:2306.09983](https://arxiv.org/abs/2306.09983) | The safety framing: consistency checks are how you evaluate models you cannot grade. It is also explicit that consistency is necessary, not sufficient (your consistent-but-wrong problem). |

Next tier: Berglund et al. 2024, *The Reversal Curse* (the dagger law fails), Hernandez et al. 2024, *Linearity of Relation Decoding* (relations as linear maps), Huntsman, Robinson & Huntsman 2024 (sheaves + LLM consistency, a prospects paper), Gavranović et al. 2024 (categorical deep learning), and Dalrymple et al. 2024, *Towards Guaranteed Safe AI*. All are in [01](01_literature_map.md).

## Ranked top-10 avenues

Scores are judgement calls (see [02](02_avenues_catalog.md) for the scheme). This list merges near-duplicates and is re-ordered using the pilot results and the prior-art finding.

| # | Avenue (catalog IDs) | CT concept | One line | Pilot evidence |
|---:|---|---|---|---|
| 1 | Distributional functoriality vs Operadic Consistency, head to head ([A1](02_avenues_catalog.md#a1), [A2](02_avenues_catalog.md#a2), [A3](02_avenues_catalog.md#a3)) | functor into Stoch (Kleisli) | Exact/Kleisli + semantic-quotient `delta_comp` vs OC + SC + semantic entropy on MuSiQue | Pilot B E1 |
| 2 | Consistency-guided **verification budget** on real claim DAGs ([O1](02_avenues_catalog.md#o1), [S2](02_avenues_catalog.md#s2)) | sheaf energy; operad algebra laws | Allocation is the differentiator from all detection-only prior work; must be adaptive and boundary-aware | Pilot A (sobering) |
| 3 | Lax-functor aggregator for long chains ([A4](02_avenues_catalog.md#a4)) | metric-enriched functor, triangle inequality | Replace saturated `max` with a subadditivity slack/violation score; **zero new calls** | none |
| 4 | Size of the consistent-but-wrong blind spot ([A7](02_avenues_catalog.md#a7), [P2](02_avenues_catalog.md#p2)) | lawful-but-unfaithful functor; determinism | Bound what any consistency-based oversight can catch | Pilots A & B |
| 5 | Dagger (reversal) defect as a complementary detector ([D1](02_avenues_catalog.md#d1), [D3](02_avenues_catalog.md#d3)) | dagger functor | Ask the converse of each hop; round-trip probability as a signal | Pilot B E2 |
| 6 | d-separation-aware expected damage ([P5](02_avenues_catalog.md#p5)) | categorical d-separation | Better `D̂` for the parent DP; CPU-only in `dag_codes` | none |
| 7 | Abstract interpretation over claim DAGs ([G1](02_avenues_catalog.md#g1)) | Galois connection | Sound 3-valued propagation decides some claims for free; GSAI-flavoured | none |
| 8 | Bayesian-lens blame attribution ([L1](02_avenues_catalog.md#l1)) | Bayesian lenses / optics | Push "final answer wrong" back through the chain to pick the next check | none |
| 9 | `delta_comp` as Robinson consistency radius ([S1](02_avenues_catalog.md#s1)) | sheaf of pseudometric spaces | One definition that covers chains, overlapping regions and DAGs | Pilot A (vector version) |
| 10 | Battery of categorical laws ([N2](02_avenues_catalog.md#n2)) | functor axioms, involution, dagger | Which law carries non-redundant signal at which scale? | Pilot B (two laws) |

Designs for #1–#5 are in [03_experiment_designs.md](03_experiment_designs.md).

## Pilot results (preliminary; simulators and tiny from-scratch models only)

PILOT_RESULTS_PLACEHOLDER

## Recommended next steps for Will

1. **This week, no API cost.** Answer small questions [1, 2, 3, 5, 10](04_small_questions.md) on the existing `will/project1` caches:
   - approximate OC from the first sample of each route;
   - NLI-cluster the answers;
   - test the subadditivity bound;
   - measure the consistent-but-wrong share;
   - run `D`-only in `06_budget.py`.

   These decide whether the paper's contribution should be "distributional functoriality" (Design 1), "aggregation" (Design 3) or "allocation" (Design 2).
2. **Read papers 1–2 above, then email the authors.** Their code is public. A head-to-head on identical MuSiQue questions is the most valuable single experiment you can run (Design 1), and the authors may welcome it.
3. **Re-frame the paper's claim.** "Functoriality as a hallucination signal" is no longer novel by itself. "Distributional composition defects, aggregated with a metric bound, used to allocate a verification budget" may still be.
4. **Extend the parent simulator cheaply.** P5 (d-separation-aware damage), G1 (abstract interpretation) and L1 (Bayesian-lens blame) are each a few hundred lines in `dag_codes/`. Pilot A suggests also adding an **adaptive** boundary-walk policy, since a static consistency score loses to descendant count.
5. **Get a key-free replication path.** Run one open model (Qwen2.5-7B or Llama-3.1-8B on a free GPU) through `will/project1`, so results do not depend on paid APIs and you get exact log-probabilities for Kleisli composites.
6. **Before claiming novelty for anything**, re-search arXiv directly for 2026 preprints. This survey's search could not open arXiv, and the field is moving month to month.
