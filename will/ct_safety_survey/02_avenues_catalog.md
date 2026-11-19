# 02 — Avenues catalog (50 ideas, scored)

[← back to README](README.md)

Each avenue is tied to one categorical concept (see [05_category_theory_primer.md](05_category_theory_primer.md)). Citation keys refer to [01_literature_map.md](01_literature_map.md).

**Scoring (1–5, 5 = best; judgement calls, not measurements).** **F** feasibility for an undergrad with modest compute and no big API budget · **N** novelty (5 = no one seems to have done it, given the search limits in the [notes](CHANGELOG_or_NOTES.md)) · **S** safety relevance · **C** connection to Will's existing pipeline (`will/project1`, `dag_codes`) · **T** time to first result (5 = days, 1 = months). **Total = 1.5·F + N + S + C + T** (max 27.5).

> **Novelty caveat.** Novelty scores reflect only what the literature agents could find through web search (arXiv itself was not reachable). Re-search arXiv for 2026 preprints before claiming novelty for any avenue. The field is moving fast: two 2026 papers ([`bottman2026operadic`](01_literature_map.md), [`liu2026intent`](01_literature_map.md)) already cover the core of Will's current test.

## Ranked table

| Rank | ID | Avenue | Concept | F | N | S | C | T | Total | Pilot |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | [S2](#s2) | Sheaf-Laplacian edge energy for budgeted verification | coboundary, Dirichlet energy | 5 | 4 | 4 | 5 | 5 | 25.5 | yes |
| 2 | [O1](#o1) | Consistency-guided budget allocation over decomposition trees | operad algebras; failures of algebra laws localise errors | 5 | 4 | 5 | 5 | 4 | 25.5 | yes |
| 3 | [A4](#a4) | Lax functor / subadditive defect bound for long chains | Lawvere-metric-enriched (lax) functor; triangle inequality | 5 | 4 | 3 | 5 | 5 | 24.5 |  |
| 4 | [A7](#a7) | Quantifying consistent-but-false | functor into the wrong target (lawful but unfaithful) | 5 | 3 | 5 | 4 | 5 | 24.5 | yes |
| 5 | [P5](#p5) | d-separation-aware expected damage | categorical d-separation | 5 | 4 | 4 | 5 | 4 | 24.5 |  |
| 6 | [D1](#d1) | Dagger defect as a hallucination signal on chains | dagger functor (relational converse) | 5 | 3 | 4 | 5 | 5 | 24.5 | yes |
| 7 | [S1](#s1) | delta_comp as Robinson's consistency radius | sheaf of pseudometric spaces | 5 | 4 | 4 | 5 | 4 | 24.5 |  |
| 8 | [G1](#g1) | Abstract interpretation over claim DAGs | Galois connection α ⊣ γ, sound fixpoints | 5 | 4 | 4 | 5 | 4 | 24.5 |  |
| 9 | [L1](#l1) | Bayesian-lens blame attribution through chains | Bayesian lenses / optics | 5 | 4 | 4 | 5 | 4 | 24.5 |  |
| 10 | [A1](#a1) | Distributional functoriality vs. Operadic Consistency, head to head | functor into Stoch (Kleisli of the distribution monad) | 5 | 2 | 4 | 5 | 5 | 23.5 |  |
| 11 | [A2](#a2) | Kleisli composite instead of the argmax bridge | Kleisli composition of Markov kernels | 5 | 3 | 3 | 5 | 5 | 23.5 | yes |
| 12 | [P1](#p1) | Which divergence? TV vs KL vs Wasserstein vs arbitrage | enrichment choice; Baez–Fritz relative entropy | 5 | 3 | 3 | 5 | 5 | 23.5 |  |
| 13 | [P2](#p2) | Determinism × functoriality 2×2 | deterministic morphisms; entropy in Markov categories | 4 | 4 | 4 | 5 | 4 | 23.0 |  |
| 14 | [N1](#n1) | Paraphrase/translation naturality defect | natural transformation; commuting square | 5 | 2 | 4 | 4 | 5 | 22.5 |  |
| 15 | [D2](#d2) | Round-trip consistency under controlled training | dagger in a synthetic world | 5 | 3 | 3 | 4 | 5 | 22.5 | yes |
| 16 | [S7](#s7) | Join (universal-relation) consistency of top-k answers | relational databases & gluing | 5 | 4 | 3 | 4 | 4 | 22.5 |  |
| 17 | [A3](#a3) | Functoriality in the quotient category of meanings | quotient category / semantic equivalence classes | 4 | 3 | 4 | 5 | 4 | 22.0 |  |
| 18 | [A6](#a6) | Overlapping-region defect attribution (H2) | presheaf on regions; least-squares attribution | 4 | 3 | 4 | 5 | 4 | 22.0 |  |
| 19 | [P3](#p3) | Backward (Bayesian-lens) consistency | Bayesian inversion composes optically | 4 | 4 | 4 | 4 | 4 | 22.0 |  |
| 20 | [N2](#n2) | Battery of categorical laws | functor axioms + involution + dagger + monotonicity | 4 | 3 | 5 | 4 | 4 | 22.0 |  |
| 21 | [S3](#s3) | Signalling vs H^1: two kinds of inconsistency | Hodge decomposition of edge data; contextuality | 4 | 5 | 4 | 4 | 3 | 22.0 |  |
| 22 | [A9](#a9) | Linear-relational functor: does W_g W_f ≈ W_{g∘f}? | functor from the free category on relations to Aff/Vect | 4 | 4 | 3 | 4 | 4 | 21.0 | yes |
| 23 | [D3](#d3) | Is composition dagger-compatible? (g∘f)† = f†∘g† | dagger category axiom | 4 | 4 | 3 | 4 | 4 | 21.0 |  |
| 24 | [S4](#s4) | Harmonic-extension answer repair | nearest global section; Schur complement | 4 | 4 | 4 | 4 | 3 | 21.0 |  |
| 25 | [L5](#l5) | Bayesian-lens test of LLM belief updates | Bayesian inversion composes | 4 | 4 | 4 | 3 | 4 | 21.0 |  |
| 26 | [O4](#o4) | GNN that imitates the budgeted DP oracle | polynomial functors / algorithmic alignment | 4 | 3 | 3 | 5 | 4 | 21.0 |  |
| 27 | [Y1](#y1) | Yoneda probes for fabricated entities | Yoneda lemma (object = its relationships) | 4 | 4 | 4 | 3 | 4 | 21.0 |  |
| 28 | [A8](#a8) | Amortised functoriality probe | linear probe as an approximate natural transformation | 3 | 4 | 4 | 4 | 3 | 19.5 |  |
| 29 | [P4](#p4) | Skipped-hop test via conditional independence | sufficient statistics / CI in Markov categories | 3 | 4 | 4 | 4 | 3 | 19.5 |  |
| 30 | [N7](#n7) | CCS generalised from negation to composition | functor to [0,1]-relations preserving composition and negation | 3 | 4 | 5 | 3 | 3 | 19.5 |  |
| 31 | [Y2](#y2) | Meaning vs saying: continuation profile of the stated bridge | enriched Yoneda (copresheaf of continuations) | 3 | 4 | 4 | 4 | 3 | 19.5 |  |
| 32 | [G2](#g2) | Reward hacking as a Galois-connection failure | Galois connections between policy preorders | 4 | 4 | 5 | 1 | 3 | 19.0 |  |
| 33 | [A5](#a5) | Scale crossover of the composition signal | functoriality defect vs calibration | 3 | 3 | 4 | 4 | 3 | 18.5 | yes |
| 34 | [S6](#s6) | Contextual fraction of multi-hop answers | Abramsky–Brandenburger contextuality | 3 | 5 | 3 | 3 | 3 | 18.5 |  |
| 35 | [S8](#s8) | Discourse-sheaf model of multi-agent debate | opinion dynamics on discourse sheaves | 3 | 4 | 5 | 2 | 3 | 18.5 |  |
| 36 | [X1](#x1) | Magnitude of the decomposition's enriched category | magnitude (Tsallis entropies) | 3 | 5 | 3 | 3 | 3 | 18.5 |  |
| 37 | [G4](#g4) | Refinement loop for a GSAI-style verifier at toy scale | Galois insertion, CEGAR-style refinement | 3 | 3 | 4 | 3 | 3 | 17.5 |  |
| 38 | [X3](#x3) | Fibration over evidence conditions | Grothendieck fibration / reindexing | 3 | 3 | 3 | 4 | 3 | 17.5 |  |
| 39 | [N3](#n3) | Knowledge edits as a naturality stress test | naturality between pre- and post-edit functors | 3 | 2 | 4 | 3 | 3 | 16.5 |  |
| 40 | [N5](#n5) | Stitching maps as natural isomorphisms | naturality: one component commuting with all morphisms | 3 | 4 | 3 | 2 | 3 | 16.5 |  |
| 41 | [S5](#s5) | Learned restriction maps on hidden states | neural sheaf diffusion | 3 | 3 | 4 | 3 | 2 | 16.5 |  |
| 42 | [O2](#o2) | Where safety fails to compose in tool-using agents | graded monoidal categories / resource theories | 3 | 3 | 5 | 1 | 3 | 16.5 |  |
| 43 | [O3](#o3) | Amplification as an operad-algebra homomorphism | operad algebra homomorphisms | 2 | 4 | 4 | 3 | 2 | 16.0 |  |
| 44 | [G3](#g3) | Specs vs tests as a closure operator | Galois connection between specs and behaviours | 3 | 4 | 4 | 1 | 2 | 15.5 |  |
| 45 | [L2](#l2) | RLHF as a lens; reward hacking as backward-pass mismatch | lenses / Para / categorical cybernetics | 3 | 3 | 5 | 1 | 2 | 15.5 |  |
| 46 | [L4](#l4) | Hazard puncturing via pushouts in compositional RL | pushouts in a category of MDPs; optic value iteration | 3 | 3 | 4 | 1 | 3 | 15.5 |  |
| 47 | [N4](#n4) | Interchange interventions as naturality for 2-hop recall | causal abstraction as a natural transformation | 2 | 3 | 4 | 3 | 2 | 15.0 |  |
| 48 | [N6](#n6) | SAE dictionaries as natural transformations across model sizes | natural transformation between model functors | 2 | 4 | 4 | 2 | 2 | 15.0 |  |
| 49 | [L3](#l3) | Debate as an open game | open games, equilibria | 2 | 3 | 5 | 2 | 2 | 15.0 |  |
| 50 | [X2](#x2) | Kan-extension view of compositional generalisation | left Kan extension along generators → free category | 2 | 4 | 3 | 3 | 2 | 15.0 |  |

## Per-avenue entries


### Family A: Functors & composition

<a id="a1"></a>
#### A1. Distributional functoriality vs. Operadic Consistency, head to head
- **Concept:** functor into Stoch (Kleisli of the distribution monad)
- **Idea:** Re-run Will's MuSiQue pipeline next to Bottman et al.'s Operadic Consistency (greedy direct vs decomposed answer, token-F1). Ask whether the distributional TV score adds information beyond OC + self-consistency + semantic entropy.
- **Safety relevance:** hallucination detection
- **Measurable quantity:** ΔAUROC over OC+SC+SE; AUARC (selective prediction); paired bootstrap over questions
- **Closest prior work:** bottman2026operadic, bottman2026operads, chen2024twofailures
- **Novelty risk:** HIGH: the pointwise version is published (NeurIPS 2026). Only the distributional/budget angle is new.
- **Scores:** F5 N2 S4 C5 T5 → **23.5**

<a id="a2"></a>
#### A2. Kleisli composite instead of the argmax bridge
- **Concept:** Kleisli composition of Markov kernels
- **Idea:** Compute the stepwise distribution as Σ_y P(y|x,f)P(z|y,g) (marginalising over sampled bridges), not by plugging in one sampled bridge. Compare it with the plug-in estimator Will uses now.
- **Safety relevance:** hallucination detection
- **Measurable quantity:** AUROC of exact-Kleisli vs plug-in vs N=3 sampled estimator
- **Closest prior work:** press2023compositionality, wang2023selfconsistency
- **Novelty risk:** Low-medium: the estimator choice is rarely discussed.
- **Scores:** F5 N3 S3 C5 T5 → **23.5**  · **Pilot:** Pilot B computes the exact composite.

<a id="a3"></a>
#### A3. Functoriality in the quotient category of meanings
- **Concept:** quotient category / semantic equivalence classes
- **Idea:** Cluster answers by bidirectional entailment (as in semantic entropy) before computing delta_comp. This fixes the exact-match inflation in Will's paper ("May 2, 2008" vs "May 2").
- **Safety relevance:** hallucination detection
- **Measurable quantity:** ΔAUROC of semantic delta_comp vs exact-match delta_comp, vs semantic entropy
- **Closest prior work:** farquhar2024semantic, kuhn2023semantic
- **Novelty risk:** Medium: obvious once stated, but not found as a composition test.
- **Scores:** F4 N3 S4 C5 T4 → **22.0**

<a id="a4"></a>
#### A4. Lax functor / subadditive defect bound for long chains
- **Concept:** Lawvere-metric-enriched (lax) functor; triangle inequality
- **Idea:** Treat the composition defect as a metric. Then δ(h∘g∘f) ≤ δ(region1)+δ(region2)+… must hold for a coherent model. Use the slack or violation as a principled aggregator to replace `max`, which Will found saturates.
- **Safety relevance:** hallucination localisation
- **Measurable quantity:** violation rate of the bound; AUROC of sum/slack aggregators vs max vs full-chain
- **Closest prior work:** rischel2021compositional, baez2011characterization
- **Novelty risk:** Low: abstraction-error bounds exist for causal models, not for LLM QA.
- **Scores:** F5 N4 S3 C5 T5 → **24.5**

<a id="a5"></a>
#### A5. Scale crossover of the composition signal
- **Concept:** functoriality defect vs calibration
- **Idea:** Measure ΔAUROC(delta_comp | confidence, SC) across one model family (Pythia 70m→1.4b, Qwen2.5 0.5b→7b). Test the hypothesis that the signal matters most for weak models, as Will's gpt-4.1-mini vs gpt-5.5 pattern suggests.
- **Safety relevance:** eval design, scalable oversight
- **Measurable quantity:** ΔAUROC as a function of parameter count
- **Closest prior work:** press2023compositionality, kadavath2022know, bottman2026operadic
- **Novelty risk:** Medium: OC reports cross-model correlation, not incremental value by size.
- **Scores:** F3 N3 S4 C4 T3 → **18.5**  · **Pilot:** Pilot B's checkpoints are a toy analogue.

<a id="a6"></a>
#### A6. Overlapping-region defect attribution (H2)
- **Concept:** presheaf on regions; least-squares attribution
- **Idea:** From overlapping 2-step region defects, solve for per-hop 'blame' (a linear inverse problem on the region-incidence matrix) to localise the false hop.
- **Safety relevance:** localisation for verifiers
- **Measurable quantity:** top-1 hop localisation accuracy; covered-error fraction at k
- **Closest prior work:** bottman2026operads
- **Novelty risk:** Medium.
- **Scores:** F4 N3 S4 C5 T4 → **22.0**

<a id="a7"></a>
#### A7. Quantifying consistent-but-false
- **Concept:** functor into the wrong target (lawful but unfaithful)
- **Idea:** Build 2-hop chains from TruthfulQA-style misconceptions, or use the synthetic world with planted false facts, and measure how many errors have delta_comp≈0. This sets the ceiling of any consistency detector.
- **Safety relevance:** deception/consistency, eval design
- **Measurable quantity:** fraction of errors with delta below threshold; detector recall ceiling
- **Closest prior work:** lin2022truthfulqa, fluri2023superhuman, paleka2025forecasters
- **Novelty risk:** Low-medium: noted qualitatively, rarely quantified.
- **Scores:** F5 N3 S5 C4 T5 → **24.5**  · **Pilot:** Pilots A and B both measure it.

<a id="a8"></a>
#### A8. Amortised functoriality probe
- **Concept:** linear probe as an approximate natural transformation
- **Idea:** Train a probe on hidden states of the direct query to predict delta_comp, so a monitor needs no stepwise calls at test time.
- **Safety relevance:** cheap runtime monitoring
- **Measurable quantity:** probe AUROC for error vs full delta_comp vs semantic-entropy probes
- **Closest prior work:** kossen2024sep
- **Novelty risk:** Medium.
- **Scores:** F3 N4 S4 C4 T3 → **19.5**

<a id="a9"></a>
#### A9. Linear-relational functor: does W_g W_f ≈ W_{g∘f}?
- **Concept:** functor from the free category on relations to Aff/Vect
- **Idea:** Fit linear relational embeddings per relation and for composite prompts, and measure the functoriality defect of the linear maps against mismatched-pair nulls.
- **Safety relevance:** interpretability; predicts compositional hallucination without querying
- **Measurable quantity:** relative Frobenius defect; nearest-neighbour accuracy of the composed map vs the direct map
- **Closest prior work:** hernandez2024linearity, christ2025structure
- **Novelty risk:** Low: LRE composition not found tested.
- **Scores:** F4 N4 S3 C4 T4 → **21.0**  · **Pilot:** Pilot B (E3), toy version.


### Family P: Markov categories & information

<a id="p1"></a>
#### P1. Which divergence? TV vs KL vs Wasserstein vs arbitrage
- **Concept:** enrichment choice; Baez–Fritz relative entropy
- **Idea:** Recompute the composition defect from cached samples under several divergences, including Paleka et al.'s arbitrage metric, and compare predictive value.
- **Safety relevance:** eval design
- **Measurable quantity:** AUROC per divergence (free: reuses Will's cache)
- **Closest prior work:** baez2014bayesian, paleka2025forecasters
- **Novelty risk:** Low.
- **Scores:** F5 N3 S3 C5 T5 → **23.5**

<a id="p2"></a>
#### P2. Determinism × functoriality 2×2
- **Concept:** deterministic morphisms; entropy in Markov categories
- **Idea:** Cross Perrone's distance-from-determinism (≈ per-hop entropy) with delta_comp. Confidently-wrong-but-non-functorial and uncertain-but-functorial are distinct failure types.
- **Safety relevance:** hallucination, deception (confident errors)
- **Measurable quantity:** error rate per quadrant; incremental AUROC
- **Closest prior work:** perrone2024markov, farquhar2024semantic
- **Novelty risk:** Low.
- **Scores:** F4 N4 S4 C5 T4 → **23.0**

<a id="p3"></a>
#### P3. Backward (Bayesian-lens) consistency
- **Concept:** Bayesian inversion composes optically
- **Idea:** Ask 'given z, which x?' directly and hop by hop (invert g then f). Exact Bayesian inversion composes, so the gap is a second label-free signal.
- **Safety relevance:** hallucination, reversal-type asymmetry
- **Measurable quantity:** backward delta; correlation with forward delta and with error
- **Closest prior work:** smithe2020bayesian, braithwaite2023compositional
- **Novelty risk:** Low as a probe.
- **Scores:** F4 N4 S4 C4 T4 → **22.0**

<a id="p4"></a>
#### P4. Skipped-hop test via conditional independence
- **Concept:** sufficient statistics / CI in Markov categories
- **Idea:** If the direct answer Z depends on X beyond the bridge Y (I(Z;X|Y)>0), the model skipped or shortcut the hop.
- **Safety relevance:** faithfulness of reasoning
- **Measurable quantity:** estimated CMI; association with error and with 'hopping too late'
- **Closest prior work:** fritz2020synthetic, biran2024hopping, yang2024latent
- **Novelty risk:** Medium.
- **Scores:** F3 N4 S4 C4 T3 → **19.5**

<a id="p5"></a>
#### P5. d-separation-aware expected damage
- **Concept:** categorical d-separation
- **Idea:** In the parent DP, replace the descendant count D̂ with the number of descendants not screened off by already-verified claims, so the DP becomes adaptive.
- **Safety relevance:** scalable oversight (budgeted verification)
- **Measurable quantity:** reliability at fixed budget in dag_codes vs current D̂
- **Closest prior work:** fritz2023dseparation, yin2022markov
- **Novelty risk:** Low for verification budgets.
- **Scores:** F5 N4 S4 C5 T4 → **24.5**


### Family N: Natural transformations

<a id="n1"></a>
#### N1. Paraphrase/translation naturality defect
- **Concept:** natural transformation; commuting square
- **Idea:** Answer-then-paraphrase vs paraphrase-then-answer, and EN vs FR, on the same chains. TV of the two routes.
- **Safety relevance:** robustness, consistency
- **Measurable quantity:** naturality defect AUROC; added value over delta_comp
- **Closest prior work:** elazar2021pararel, yang2025metaqa, li2024drowzee
- **Novelty risk:** HIGH: paraphrase consistency is well studied; only the unified framing is new.
- **Scores:** F5 N2 S4 C4 T5 → **22.5**

<a id="n2"></a>
#### N2. Battery of categorical laws
- **Concept:** functor axioms + involution + dagger + monotonicity
- **Idea:** Run identity (paraphrase), composition, negation-involution, monotonicity and dagger checks on one dataset. Which laws carry non-redundant signal, and at what scale?
- **Safety relevance:** eval design, hallucination
- **Measurable quantity:** incremental AUROC per law; law-violation profile per model
- **Closest prior work:** jang2022becel, fluri2023superhuman, ghosh2025logical, elazar2021pararel
- **Novelty risk:** Medium: the benchmarks exist; a head-to-head as detectors does not.
- **Scores:** F4 N3 S5 C4 T4 → **22.0**

<a id="n3"></a>
#### N3. Knowledge edits as a naturality stress test
- **Concept:** naturality between pre- and post-edit functors
- **Idea:** ROME-edit hop f and check whether the direct 2-hop answer moves to g(new bridge); measure delta_comp before and after.
- **Safety relevance:** robustness of editing/unlearning
- **Measurable quantity:** post-edit composition consistency vs single-hop edit success
- **Closest prior work:** meng2022locating, zhong2023mquake
- **Novelty risk:** HIGH: MQuAKE covers the behaviour; framing only.
- **Scores:** F3 N2 S4 C3 T3 → **16.5**

<a id="n4"></a>
#### N4. Interchange interventions as naturality for 2-hop recall
- **Concept:** causal abstraction as a natural transformation
- **Idea:** Use DAS to find a bridge-entity subspace. Swap it between prompts; does the answer follow g(b')? IIA = degree of commutativity.
- **Safety relevance:** interpretability (right answer via the right mechanism)
- **Measurable quantity:** IIA per layer vs behavioural delta_comp
- **Closest prior work:** geiger2024finding, geiger2025causal, yang2024latent, biran2024hopping
- **Novelty risk:** Medium.
- **Scores:** F2 N3 S4 C3 T2 → **15.0**

<a id="n5"></a>
#### N5. Stitching maps as natural isomorphisms
- **Concept:** naturality: one component commuting with all morphisms
- **Idea:** Learn one affine map T between two models; does T∘LRE_r^A ≈ LRE_r^B∘T hold for all relations r at once?
- **Safety relevance:** transfer of probes/monitors across models
- **Measurable quantity:** naturality residual per relation
- **Closest prior work:** bansal2021revisiting, lenc2015understanding, huh2024platonic
- **Novelty risk:** Low-medium.
- **Scores:** F3 N4 S3 C2 T3 → **16.5**

<a id="n6"></a>
#### N6. SAE dictionaries as natural transformations across model sizes
- **Concept:** natural transformation between model functors
- **Idea:** Match SAE features small↔large, then test whether the matching commutes with relation maps.
- **Safety relevance:** transfer of safety features/monitors
- **Measurable quantity:** commutation error per relation vs size
- **Closest prior work:** lan2024sparse, thasarathan2025universal, templeton2024scaling
- **Novelty risk:** Low-medium.
- **Scores:** F2 N4 S4 C2 T2 → **15.0**

<a id="n7"></a>
#### N7. CCS generalised from negation to composition
- **Concept:** functor to [0,1]-relations preserving composition and negation
- **Idea:** Add a composition constraint (truth of A r1∘r2 C ≈ ∃B: T(A r1 B)∧T(B r2 C)) to a CCS-style unsupervised probe.
- **Safety relevance:** ELK, deception
- **Measurable quantity:** probe accuracy vs CCS on 2-hop statements
- **Closest prior work:** burns2022ccs, christiano2021elk
- **Novelty risk:** Low.
- **Scores:** F3 N4 S5 C3 T3 → **19.5**


### Family D: Duals / dagger

<a id="d1"></a>
#### D1. Dagger defect as a hallucination signal on chains
- **Concept:** dagger functor (relational converse)
- **Idea:** For each hop r(a)=b also ask r⁻¹(b). Does the round-trip probability add to delta_comp in predicting multi-hop errors?
- **Safety relevance:** hallucination, knowledge asymmetry
- **Measurable quantity:** dagger defect; ΔAUROC over delta_comp+conf
- **Closest prior work:** berglund2024reversal, allenzhu2025physics32
- **Novelty risk:** Medium: reversal is measured as a curse, not used as a detector.
- **Scores:** F5 N3 S4 C5 T5 → **24.5**  · **Pilot:** Pilot B (E2) in a toy world.

<a id="d2"></a>
#### D2. Round-trip consistency under controlled training
- **Concept:** dagger in a synthetic world
- **Idea:** In a synthetic KG where you control which reverse facts are trained, measure how round-trip consistency tracks forward errors on reverse-trained vs untrained pairs.
- **Safety relevance:** eval design
- **Measurable quantity:** AUROC of 1-roundtrip for forward error by condition
- **Closest prior work:** berglund2024reversal
- **Novelty risk:** Low.
- **Scores:** F5 N3 S3 C4 T5 → **22.5**  · **Pilot:** Pilot B (E2).

<a id="d3"></a>
#### D3. Is composition dagger-compatible? (g∘f)† = f†∘g†
- **Concept:** dagger category axiom
- **Idea:** Ask reversed two-hop questions directly vs as reversed hops in the opposite order.
- **Safety relevance:** hallucination
- **Measurable quantity:** defect of the reversed composite
- **Closest prior work:** balesni2024twohop, berglund2024reversal
- **Novelty risk:** Low.
- **Scores:** F4 N4 S3 C4 T4 → **21.0**


### Family S: Sheaves & cohomology

<a id="s1"></a>
#### S1. delta_comp as Robinson's consistency radius
- **Concept:** sheaf of pseudometric spaces
- **Idea:** Rewrite delta_comp as the consistency radius of a small sheaf (TV-metric stalks), which extends unchanged to 3–4-hop and branching decompositions.
- **Safety relevance:** hallucination (multi-hop)
- **Measurable quantity:** consistency radius AUROC vs delta_comp_max/full-chain
- **Closest prior work:** robinson2020assignments, huntsman2024sheaves
- **Novelty risk:** Low-medium (Huntsman et al. is a prospects paper).
- **Scores:** F5 N4 S4 C5 T4 → **24.5**

<a id="s2"></a>
#### S2. Sheaf-Laplacian edge energy for budgeted verification
- **Concept:** coboundary, Dirichlet energy
- **Idea:** Rank claims by local sheaf inconsistency and spend the verification budget there. Compare against the parent project's strategies at equal budget.
- **Safety relevance:** scalable oversight
- **Measurable quantity:** reliability at budget k (dag_codes evaluate())
- **Closest prior work:** hansen2019spectral, kim2025holograph, huntsman2024sheaves
- **Novelty risk:** Medium-low.
- **Scores:** F5 N4 S4 C5 T5 → **25.5**  · **Pilot:** Pilot A (synthetic).

<a id="s3"></a>
#### S3. Signalling vs H^1: two kinds of inconsistency
- **Concept:** Hodge decomposition of edge data; contextuality
- **Idea:** Separate local disagreement (marginals differ: what delta_comp measures) from global obstruction (pairwise-agreeing yet no global section). This needs 'diamond' DAGs with two routes to a node.
- **Safety relevance:** hallucination vs incoherent world model
- **Measurable quantity:** fraction of errors with nonzero harmonic/cycle component
- **Closest prior work:** abramsky2011sheaf, abramsky2015contextuality, hansen2019spectral
- **Novelty risk:** Low.
- **Scores:** F4 N5 S4 C4 T3 → **22.0**

<a id="s4"></a>
#### S4. Harmonic-extension answer repair
- **Concept:** nearest global section; Schur complement
- **Idea:** Use the glued (nearest-consistent) assignment as a corrected answer, not just a flag.
- **Safety relevance:** mitigation
- **Measurable quantity:** EM/F1 of the glued answer vs direct/CoT
- **Closest prior work:** gebhart2023knowledge, robinson2017sensor
- **Novelty risk:** Low for LLM outputs.
- **Scores:** F4 N4 S4 C4 T3 → **21.0**

<a id="s5"></a>
#### S5. Learned restriction maps on hidden states
- **Concept:** neural sheaf diffusion
- **Idea:** Fit restriction maps between hidden states of sub-question/answer pairs on correct chains; use energy on held-out chains as a white-box detector.
- **Safety relevance:** white-box hallucination detection
- **Measurable quantity:** AUROC vs linear probes / TDA detectors
- **Closest prior work:** bodnar2022nsd, barbero2022connection, grant2026gluing, bazarova2025toha
- **Novelty risk:** Medium.
- **Scores:** F3 N3 S4 C3 T2 → **16.5**

<a id="s6"></a>
#### S6. Contextual fraction of multi-hop answers
- **Concept:** Abramsky–Brandenburger contextuality
- **Idea:** Treat overlapping sub-question pairs as measurement contexts and compute the (signalling-corrected) contextual fraction per question.
- **Safety relevance:** incoherent world model
- **Measurable quantity:** contextual fraction vs error
- **Closest prior work:** lo2025contextualityllm, abramsky2011sheaf
- **Novelty risk:** Low (but Lo et al. found contextuality very rare in BERT).
- **Scores:** F3 N5 S3 C3 T3 → **18.5**

<a id="s7"></a>
#### S7. Join (universal-relation) consistency of top-k answers
- **Concept:** relational databases & gluing
- **Idea:** Treat each sub-question's top-k answers as a relation; an empty or near-empty join flags a hallucination. Discrete, cheap, interpretable.
- **Safety relevance:** hallucination
- **Measurable quantity:** join emptiness / support ratio vs error
- **Closest prior work:** abramsky2013relational
- **Novelty risk:** Low.
- **Scores:** F5 N4 S3 C4 T4 → **22.5**

<a id="s8"></a>
#### S8. Discourse-sheaf model of multi-agent debate
- **Concept:** opinion dynamics on discourse sheaves
- **Idea:** Model debating agents as a sheaf; track energy decay per round and whether the consensus (a global section) is correct.
- **Safety relevance:** multi-agent, scalable oversight, collective hallucination
- **Measurable quantity:** energy per round; accuracy of the harmonic consensus
- **Closest prior work:** hansen2021opinion, hanks2025distributed, irving2018debate
- **Novelty risk:** Low.
- **Scores:** F3 N4 S5 C2 T3 → **18.5**


### Family G: Galois connections & adjunctions

<a id="g1"></a>
#### G1. Abstract interpretation over claim DAGs
- **Concept:** Galois connection α ⊣ γ, sound fixpoints
- **Idea:** Give each claim an abstract truth value (an interval of P(true), or {⊥,T,F,⊤}) and propagate soundly through the DAG; verify concretely only where the abstraction is too coarse.
- **Safety relevance:** guaranteed-safe-style verification
- **Measurable quantity:** reliability per concrete check; soundness rate
- **Closest prior work:** cousot1977abstract, singh2019deeppoly, dalrymple2024gsai
- **Novelty risk:** Low for LLM claim graphs.
- **Scores:** F5 N4 S4 C5 T4 → **24.5**

<a id="g2"></a>
#### G2. Reward hacking as a Galois-connection failure
- **Concept:** Galois connections between policy preorders
- **Idea:** Restate Skalse et al.'s unhackability order-theoretically and test in tabular gridworlds whether Galois coarsenings bound hackability.
- **Safety relevance:** specification/reward hacking
- **Measurable quantity:** fraction of proxy-improving policy pairs that lower true return
- **Closest prior work:** skalse2022reward, pan2022effects, krakovna2020specgaming
- **Novelty risk:** Unknown (order statements exist; Galois framing not found).
- **Scores:** F4 N4 S5 C1 T3 → **19.0**

<a id="g3"></a>
#### G3. Specs vs tests as a closure operator
- **Concept:** Galois connection between specs and behaviours
- **Idea:** The 'strongest spec implied by an eval suite' is a closure operator; measure the gap between the closed spec and the intended spec on a toy eval suite (eval-design tool).
- **Safety relevance:** eval design, specification gaming
- **Measurable quantity:** spec-gap size; behaviours that pass tests but violate intent
- **Closest prior work:** krakovna2020specgaming, cousot1977abstract
- **Novelty risk:** Unknown; speculative.
- **Scores:** F3 N4 S4 C1 T2 → **15.5**

<a id="g4"></a>
#### G4. Refinement loop for a GSAI-style verifier at toy scale
- **Concept:** Galois insertion, CEGAR-style refinement
- **Idea:** Implement the 'world model + spec + verifier' loop of guaranteed-safe AI on the claim DAG, with refinement as the budget.
- **Safety relevance:** guaranteed-safe AI
- **Measurable quantity:** checks needed to certify a DAG at a given risk
- **Closest prior work:** dalrymple2024gsai, aria2024safeguarded
- **Novelty risk:** Low; mostly an engineering demo.
- **Scores:** F3 N3 S4 C3 T3 → **17.5**


### Family L: Lenses, optics & open games

<a id="l1"></a>
#### L1. Bayesian-lens blame attribution through chains
- **Concept:** Bayesian lenses / optics
- **Idea:** When a verifier says the final answer is wrong, push that signal backwards through the chain by Bayesian inversion to pick which intermediate claim to check next.
- **Safety relevance:** scalable oversight (adaptive verification)
- **Measurable quantity:** top-1 blame accuracy; reliability of adaptive policies in dag_codes
- **Closest prior work:** smithe2020bayesian, capucci2021foundations
- **Novelty risk:** Low.
- **Scores:** F5 N4 S4 C5 T4 → **24.5**

<a id="l2"></a>
#### L2. RLHF as a lens; reward hacking as backward-pass mismatch
- **Concept:** lenses / Para / categorical cybernetics
- **Idea:** Model policy (forward) and reward-model update (backward) as a lens; in a toy bandit with a misspecified reward, measure the gap between the true and the proxy backward pass.
- **Safety relevance:** reward hacking
- **Measurable quantity:** true vs proxy return divergence across optimisation pressure
- **Closest prior work:** cruttwell2022categorical, capucci2021foundations, pan2022effects
- **Novelty risk:** Medium (framing risk: may be relabelling).
- **Scores:** F3 N3 S5 C1 T2 → **15.5**

<a id="l3"></a>
#### L3. Debate as an open game
- **Concept:** open games, equilibria
- **Idea:** Encode debate over a claim DAG as an open game; do winning transcripts satisfy functoriality more often?
- **Safety relevance:** scalable oversight
- **Measurable quantity:** correlation of verdicts with consistency
- **Closest prior work:** ghani2018compositional, irving2018debate, kenton2024scalable
- **Novelty risk:** Low; noisy with small models.
- **Scores:** F2 N3 S5 C2 T2 → **15.0**

<a id="l4"></a>
#### L4. Hazard puncturing via pushouts in compositional RL
- **Concept:** pushouts in a category of MDPs; optic value iteration
- **Idea:** Reproduce Bakirtzis et al.'s safety pushouts on a small gridworld/text game where sub-policies are prompts.
- **Safety relevance:** safe composition of skills
- **Measurable quantity:** violation rate composed vs monolithic
- **Closest prior work:** bakirtzis2022mdp, hedges2022value
- **Novelty risk:** Medium.
- **Scores:** F3 N3 S4 C1 T3 → **15.5**

<a id="l5"></a>
#### L5. Bayesian-lens test of LLM belief updates
- **Concept:** Bayesian inversion composes
- **Idea:** Elicit P(B|A), P(C|B), P(C|A) and posteriors on 2-step evidence chains; measure the deviation from the lens law.
- **Safety relevance:** calibration/coherence
- **Measurable quantity:** KL between direct and composed posteriors
- **Closest prior work:** smithe2020bayesian, christiano2022presumption
- **Novelty risk:** Low.
- **Scores:** F4 N4 S4 C3 T4 → **21.0**


### Family O: Operads & monoidal structure

<a id="o1"></a>
#### O1. Consistency-guided budget allocation over decomposition trees
- **Concept:** operad algebras; failures of algebra laws localise errors
- **Idea:** Use per-node composition failures to allocate verification over real (MuSiQue/2Wiki) claim DAGs. This is the clearest differentiator from Bottman et al., who only detect.
- **Safety relevance:** scalable oversight
- **Measurable quantity:** reliability at fixed total cost (probe calls + checks)
- **Closest prior work:** bottman2026operadic, christiano2018amplification
- **Novelty risk:** Low for allocation.
- **Scores:** F5 N4 S5 C5 T4 → **25.5**  · **Pilot:** Pilot A is the synthetic analogue; Will's 06_budget.py is the real one.

<a id="o2"></a>
#### O2. Where safety fails to compose in tool-using agents
- **Concept:** graded monoidal categories / resource theories
- **Idea:** Formalise Spera's counterexample as a 'safe' subcategory not closed under ⊗; find minimal grading under which it is; test on a toy tool agent.
- **Safety relevance:** multi-agent, tool use
- **Measurable quantity:** reachability of forbidden goals in composed agents
- **Closest prior work:** spera2026noncomp, libkind2025doubleoperadic
- **Novelty risk:** Medium.
- **Scores:** F3 N3 S5 C1 T3 → **16.5**

<a id="o3"></a>
#### O3. Amplification as an operad-algebra homomorphism
- **Concept:** operad algebra homomorphisms
- **Idea:** Distil a small model on decomposed-then-recomposed answers; do its functoriality violations drop?
- **Safety relevance:** IDA assumptions
- **Measurable quantity:** change in OC/delta_comp after LoRA
- **Closest prior work:** christiano2018amplification, bottman2026operads
- **Novelty risk:** Low.
- **Scores:** F2 N4 S4 C3 T2 → **16.0**

<a id="o4"></a>
#### O4. GNN that imitates the budgeted DP oracle
- **Concept:** polynomial functors / algorithmic alignment
- **Idea:** Train a GNN on (DAG, p_false) to imitate the DP oracle and generalise to larger DAGs.
- **Safety relevance:** scalable oversight
- **Measurable quantity:** regret vs DP; size generalisation
- **Closest prior work:** dudzik2022graph
- **Novelty risk:** Low for verification.
- **Scores:** F4 N3 S3 C5 T4 → **21.0**


### Family Y: Yoneda

<a id="y1"></a>
#### Y1. Yoneda probes for fabricated entities
- **Concept:** Yoneda lemma (object = its relationships)
- **Idea:** Query a real and an invented entity through many relations; a fabricated entity's answer profile should be incoherent (fails composition/dagger laws), even when each answer is fluent.
- **Safety relevance:** hallucination about non-existent entities, deception
- **Measurable quantity:** coherence of the relation profile; AUROC real vs fabricated
- **Closest prior work:** bradley2022enriched
- **Novelty risk:** Medium (fabricated-entity detection exists without this lens).
- **Scores:** F4 N4 S4 C3 T4 → **21.0**

<a id="y2"></a>
#### Y2. Meaning vs saying: continuation profile of the stated bridge
- **Concept:** enriched Yoneda (copresheaf of continuations)
- **Idea:** Compare the continuation profile of the model's stated bridge entity with that of the gold or most-likely entity: does the model 'mean' what it says?
- **Safety relevance:** deception/faithfulness
- **Measurable quantity:** profile distance vs error
- **Closest prior work:** bradley2022enriched, bradley2024structure
- **Novelty risk:** Low.
- **Scores:** F3 N4 S4 C4 T3 → **19.5**


### Family X: Speculative (Kan extensions, magnitude, fibrations)

<a id="x1"></a>
#### X1. Magnitude of the decomposition's enriched category
- **Concept:** magnitude (Tsallis entropies)
- **Idea:** Compute the magnitude of the LM-enriched subcategory spanned by a question's decomposition and use it as an uncertainty score.
- **Safety relevance:** uncertainty
- **Measurable quantity:** AUROC vs semantic entropy
- **Closest prior work:** bradley2025magnitude
- **Novelty risk:** Low; highly speculative.
- **Scores:** F3 N5 S3 C3 T3 → **18.5**

<a id="x2"></a>
#### X2. Kan-extension view of compositional generalisation
- **Concept:** left Kan extension along generators → free category
- **Idea:** Predict composite behaviour from single-hop behaviour (the free extension) and treat the gap as a generalisation measure.
- **Safety relevance:** eval design
- **Measurable quantity:** gap between predicted and actual composite behaviour
- **Closest prior work:** (no direct prior found)
- **Novelty risk:** Unknown; speculative.
- **Scores:** F2 N4 S3 C3 T2 → **15.0**

<a id="x3"></a>
#### X3. Fibration over evidence conditions
- **Concept:** Grothendieck fibration / reindexing
- **Idea:** Organise open-book vs closed-book vs partial-evidence conditions as a base category. Will's signal vanished closed-book; does it degrade monotonically along evidence removal?
- **Safety relevance:** hallucination under missing evidence
- **Measurable quantity:** delta_comp AUROC as a function of evidence fraction
- **Closest prior work:** (no direct prior found)
- **Novelty risk:** Unknown; framing mostly.
- **Scores:** F3 N3 S3 C4 T3 → **17.5**

