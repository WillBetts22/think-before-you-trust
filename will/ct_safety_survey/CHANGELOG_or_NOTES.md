# Notes: what was done, what could not be verified, dead ends

[← back to README](README.md)

This folder was produced in one unattended session (19 Nov 2026) by Claude Code working in a cloud sandbox. Nobody reviewed it before the PR. Treat it as a well-organised first draft.

## What was done

1. **Read the repo**: `README.md`, `will/README.md`, `will/project1/README.md`, the pilot paper `will/project1/paper/paper.tex`, `Abstract.pdf`, and skimmed `dag_codes/` and `tree_codes/`. The survey builds on Will's actual findings: composition predicts errors on 2-hop chains and in weaker models but not beyond confidence and self-consistency at scale; the `max` aggregator saturates; the signal vanishes closed-book; exact-match answer identity inflates disagreement.
2. **Literature**: six parallel search agents, one per cluster (categorical DL/probability; compositional semantics and CT×LLM; sheaves; causal abstraction/interpretability; open games and formal safety; empirical compositionality and consistency). They returned 161 entries, deduplicated to **152 distinct works** ([01](01_literature_map.md), [references.bib](references.bib)). Two citations were then re-checked by hand: Bottman et al. and Press et al.
3. **Ideation**: about 60 raw ideas from the agents plus my own, merged and deduplicated into **50 scored avenues** ([02](02_avenues_catalog.md); the source of truth is `tools/avenues.py`), **5 experiment designs** ([03](03_experiment_designs.md)) and **18 small questions** ([04](04_small_questions.md)).
4. **Two pilots, four experiments**, all CPU and no API keys ([pilots/](pilots/)):
   - **Pilot A**: sheaf-Laplacian inconsistency on the parent project's claim DAGs.
   - **Pilot B**: a tiny transformer trained from scratch on a synthetic knowledge graph. It covers functoriality (exact Kleisli composite), duality/reversal, and linear-relational functoriality.

## Verification caveats (important)

- **Network.** The sandbox allowed package registries and web *search*, but **blocked direct fetches** of arxiv.org, Semantic Scholar, OpenReview, ACL Anthology, Hugging Face, nature.com, alignmentforum.org, lesswrong.com, aria.org.uk and most publisher sites. The original plan, verifying every citation by fetching its page and reading intros/methods for the top ~20, **could not be carried out**.
- **What was done instead.** Every listed work was confirmed through web-search result listings that showed the canonical page (arXiv, proceedings or journal) with the matching title and authors, usually from two or more results. Summaries come from abstracts as shown in search results. Numbers quoted from papers are flagged in the entries and **must be re-checked against the PDFs** before citing. One exception: the Operadic Consistency code repository on GitHub *was* readable, so its implementation details (greedy answers, token-F1, depth 2) come from the code.
- **Contradiction resolved.** The empirical-cluster agent's single search "found no paper using direct-vs-decomposed disagreement on MuSiQue as a hallucination detector". The CT×LLM agent found one, `bottman2026operadic`, and I re-confirmed it by search (arXiv 2606.13649, 11 June 2026; MuSiQue is one of its four datasets). **The CT×LLM agent's finding stands.** It shows how fragile single-search novelty claims are.
- **Hugging Face blocked** means no pretrained models. Hence pilot B trains a model from scratch. The suggested pilots on Pythia/GPT-2/Qwen2.5-0.5B (LRE composition, reversal on real facts) were **not run**.
- MuSiQue was not downloaded. `multihop_data/download_musique.sh` fetches it from Google Drive with `gdown`. I did not try that host, because the pilots that ran do not need MuSiQue and the network policy was restrictive.

## Could not verify

These items appeared in searches but could not be confirmed, so they are **not** in the literature map. Each is worth a look once arXiv is reachable.

**Possible novelty risks (check these first):**
- arXiv:2608.05675, "Consistency Has a Computable Blind Spot: A Commutation Theory of Label-Free Reliability for Vision-Language Figure Reading". Title only; authors not seen. It sounds directly related to the consistent-but-false analysis (Design 5).
- arXiv:2508.10018, "A Rose by Any Other Name Would Smell as Sweet: Categorical Homotopy Theory for Large Language Models". The author was possibly Mahadevan but is unconfirmed.
- "Detecting Hallucination in LLM with Cohomology" (mathinspector.com blog, "StreamAlign"). An informal post, not a paper, with an H^1-for-hallucination idea.
- ConFactCheck (arXiv:2511.12236). Title only.

**Theory items to look up:**
- An aggregator-only listing of a paper recasting calibration as coherence of Bayesian inversion in a Markov category ("Calib" 2-category; multicalibration as global sections). No title or ID was found.
- arXiv:2609.22929, "Statistical models as natural transformations…". Title only.
- Fritz, Gonda, Perrone, Fjeldgren, "Representable Markov categories…" (arXiv:2010.07416); Smithe arXiv:2306.17009; Lê arXiv:2502.15408. Each was seen once.
- Abramsky, Mansfield, Barbosa, "The cohomology of non-locality and contextuality" (QPL 2011), and Abramsky, Barbosa, Mansfield, "Contextual fraction as a measure of contextuality" (PRL 2017). Both are well known but were not searched in this session. They are needed for avenue S6.
- "The Topos of Transformer Networks" (arXiv:2403.18415); Mahadevan, "Rethinking AI: From Functions to Functors" (AAAI 2026). Titles only.
- Myers, *Categorical Systems Theory* (book project; no stable version found).

**Other gaps:**
- Recent cellular-sheaf preprints for agents: arXiv:2610.07004 and arXiv:2605.31005 (titles only); Cobb & Gebhart arXiv:2309.03773.
- ACT 2025 proceedings, Topos Institute and Hedges/Capucci blog posts on alignment, and operad-based multi-agent LLM papers were **not searched**: the shared search budget ran out.

**Metadata still uncertain** (inside the map, flagged in the entries):
- Kadavath et al. 2022 full author list.
- Paleka et al. 2025 co-authors.
- Kenton et al. 2024 authors.
- Sheaf Attention Networks author list.
- Venue of Hansen & Ghrist "Opinion dynamics".
- Grant & Wang 2026 venue.
- The date of davidad's OAA post.
- Which of the two Bottman et al. papers is the NeurIPS 2026 one.
- Several "from memory" method details (exact LRE layers and β; the exact Rischel–Weichwald bound; sheaf-Laplacian block forms marked [K] in the agent notes).

## Dead ends and surprises in the pilots

- **Pilot B, first design:** I evaluated composition on *held-out* two-hop triples. The model memorised all one-hop facts and all trained two-hop facts (100%), yet answered held-out compositions directly with about 99.7% error at every checkpoint up to 16k steps (probe run, seed 0, 300 entities; numbers in the session log, not committed). The stepwise route was perfect. This matches the literature: tiny transformers do not compose out of distribution without much longer "grokking" training. It makes detection degenerate, because every held-out query is wrong and inconsistent. The final design keeps held-out triples as a reported side result and runs the detection test on *seen-but-imperfectly-memorised* two-hop facts (Zipf-popular entities, early checkpoints). That is closer to the real regime: an LLM answering about facts it saw in pretraining.
- **Pilot B, performance:** my first sampling routine materialised a 6000×30×1000 comparison tensor and stalled. It was rewritten as per-row inverse-CDF sampling.
- **Pilot A:** I expected DAG cross edges to help (the "sheaf generalises delta_comp from chains to DAGs" story). They did not move budget reliability (all differences within ±0.003). An "edge → upstream endpoint" rule, meant to exploit the quarantine rule, was also worse. Both are reported as nulls.
- The container restarted once mid-run; background jobs were relaunched. All committed numbers come from complete runs.

## Reproducibility

- Python 3.13, `torch` 2.15 (CPU), `numpy`, `scipy`, `scikit-learn`, `networkx`, `matplotlib`. See each pilot's README.
- All seeds are fixed. Every number in the README files is produced by a committed script into a committed `results/summary.md`.
