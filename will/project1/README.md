# Project 1: Compositional Inconsistency as a Hallucination Signal (Pilot)

Pilot for the first research goal in [`Abstract.pdf`](../../Abstract.pdf): on
roughly 100 clean MuSiQue chain questions, test whether **disagreement between
answering a multi-hop question directly and answering it step by step**
predicts factual errors *beyond* confidence, path length, and ordinary
answer disagreement (hypothesis H1). It also gives a first look at
localization (H2) and measures feasibility: error rate and probe cost.

## The test in one line

For a chain `x --f--> y --g--> z`, category theory says a structure-preserving
implementation satisfies `F(g∘f)(x) = F(g)(F(f)(x))`. We sample both sides from
the model and score their disagreement with total variation distance:

```
delta_comp = d_TV( P_direct(answer | x), P_stepwise(answer | x) )
```

`0` means both routes give the same answer distribution and `1` means the two
distributions never overlap. The detector never sees gold answers.

## Pipeline

| Script | Stage (abstract §6) | Reads gold? | Output |
|---|---|---|---|
| `01_build_pilot.py` | A: select linear chains, render hops | writes it, separately | `tasks.jsonl`, `gold.jsonl`, `audit.csv` |
| *(you)* | A: manual audit | yes | edit `audit.csv` |
| `02_generate_original.py` | B: original answer, per-step answers, confidence | no | `original.jsonl` |
| `03_run_probes.py` | C: direct vs stepwise probes, noise controls | no | `probes.jsonl` |
| `04_label.py` | D: label errors against MuSiQue references | **yes** (only stage) | `labels.jsonl`, `labels_manual.csv` |
| `05_analyze.py` | E: H1 predictive value, H2 localization, cost | via labels | `features.csv`, `results.json` |

All settings live in `config.py`, and each stage saves a snapshot of the config
next to its output so the protocol can be frozen and traced.

## Running it

```bash
cd will/project1
pip install -r requirements.txt

# 0. MuSiQue must be downloaded first (once)
../../multihop_data/download_musique.sh

# 1. Check the code works, for free (mock model, 5 questions, outputs_smoke/)
./run_pilot.sh smoke

# 2. Build the pilot set, then audit it
./run_pilot.sh build
#    open outputs/audit.csv: set include=0 + exclusion_reason for ambiguous
#    relations, time-sensitive facts, or badly rendered hops

# 3. Run the experiment (pick a provider; key from the environment)
export GROQ_API_KEY=...            # or OPENROUTER_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY
./run_pilot.sh run                 # uses PROVIDER/MODEL from config.py
./run_pilot.sh run anthropic claude-sonnet-5-5

# 4. Optional: fill manual_label in outputs/labels_manual.csv
#    (unsupported / invalid_inference / correct ...), then re-run:
python3 05_analyze.py
```

Every model call is cached in `cache/`, so re-running a stage after a crash or
a rate-limit hit only pays for calls that haven't been made yet.

## What gets measured per question

- **Original output (Stage B):** the final answer, an answer per step, and a
  stated confidence. This is a single call.
- **Composition test (Stage C):** `N=3` direct samples, plus `N=3` stepwise
  chains in which the model's own step-1 answer is fed into step 2.
  `delta_comp` is computed from these.
- **Same-route control:** a second independent batch of both routes, giving
  `delta_direct_self` and `delta_step_self`. This separates composition failure
  from ordinary sampling noise.
- **Ordinary disagreement:** `3N` samples of the original question scored as
  `1 - mode share`. This is plain self-consistency at the same call cost as
  one composition test, and it's the main competitor the paper has to beat.
- **Longer chains (`HOPS = (2, 3, 4)`):** these get overlapping two-step
  regions plus a full-chain test. Regions after the first start from the
  model's own upstream answer. MuSiQue has no written composite question for a
  sub-region, so `prompts.compose` builds one by nesting. Audit these.

## Cost (open-book, 2-hop)

| Item | Calls per question |
|---|---|
| Original output (Stage B) | 1 |
| Direct route, 2 batches | 6 |
| Stepwise route, 2 batches | 12 |
| Ordinary disagreement | 9 |
| **Total** | **~28** |

Each call carries all 20 paragraphs (about 2.7k prompt tokens), so the 100-question
pilot comes to **roughly 7–8M input tokens**. That exceeds most free tiers in a
single day. The cache makes it safe to run in chunks. Setting
`CONDITION = "closed_book"` drops the paragraphs and cuts the cost by about 20×.

## Decisions to revisit before freezing the protocol

- **Answer identity:** `common.normalize` is exact match after SQuAD-style
  normalization, so `"USSR"` and `"Soviet Union"` count as different answers.
  That inflates `delta_comp`. Options are fuzzy merging or an LLM-based
  equivalence judge; either one must stay gold-free.
- **Hop rendering:** `Subject >> relation` hops become "What is the relation of
  Subject?". Some read awkwardly, and `audit.csv` flags them.
- **Labels:** automatic labels use token-F1 ≥ 0.8. "Unsupported" and "invalid
  inference" need a person, so use `labels_manual.csv` for them.
- **Missing baseline feature:** relation type isn't a feature yet.
- **Data splits:** the pilot draws from MuSiQue **train**, so dev and test stay
  clean for the later development and held-out sets.

## Not in this project (later milestones)

- Stage F verification policies under equal budgets. These plug into
  `dag_codes/` as a new `Composition` strategy.
- A second model.
- 2WikiMultiHopQA and HotpotQA.
