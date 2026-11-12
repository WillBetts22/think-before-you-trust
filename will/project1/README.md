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
./run_pilot.sh run anthropic claude-sonnet-5-5   # any provider/model pair

# 4. Optional: fill manual_label in outputs/labels_manual.csv
#    (unsupported / invalid_inference / correct ...), then re-run:
python3 05_analyze.py
```

Every model call is cached in `cache/`, so re-running a stage after a crash or
a rate-limit hit only pays for calls that haven't been made yet.

## Daily job (free-tier friendly)

`daily_job.py` runs Stages B and C until the day's budget runs out. The budget
is either `DAILY_MAX_API_CALLS` or the provider's own daily quota. The next day
it replays finished work from the cache and continues where it stopped. Once
everything is done, it runs Stages D and E, writes `outputs/DONE`, and sends a
macOS notification. Progress is logged to `outputs/daily_log.txt`.

- **Settings and key:** `~/.config/tbyt/env`, which is outside the repo so the key is never committed.
- **Schedule:** the launchd agent `~/Library/LaunchAgents/com.wbetts.tbyt-pilot.plist` runs `run_daily.sh` every day at 09:00. If the Mac is asleep then, it runs on wake.

```bash
launchctl kickstart gui/$(id -u)/com.wbetts.tbyt-pilot     # run now
tail -f outputs/daily_log.txt                              # watch progress
launchctl bootout gui/$(id -u)/com.wbetts.tbyt-pilot       # stop / uninstall
```

## OpenAI pipeline (separate from the Groq run)

`run_openai.sh` runs the same Stages B–E against the OpenAI API with no daily
limit and questions probed in parallel. It shares the code but none of the
data: it writes to `outputs_openai/`, caches under `cache/openai/<model>/`,
reads its key from `~/.config/tbyt/openai.env`, and never touches `outputs/`,
`daily_job.py` or `STATUS.md`.

```bash
./run_openai.sh check                  # key works; lists the chat models it can use
./run_openai.sh replicate              # task set "pilot100" = the Groq pilot's 100 audited questions
./run_openai.sh smoke                  # 3 questions end to end, to check settings
./run_openai.sh run pilot100           # Stages B-E with TBYT_MODEL
./run_openai.sh build scale300 300 2,3,4   # a new, larger task set (audit it, then `run`)

# any setting can be varied per run; each combination gets its own run folder
TBYT_MODEL=gpt-4.1-mini TBYT_SAMPLES_PER_ROUTE=5 TBYT_CONDITION=closed_book ./run_openai.sh run pilot100
```

Runs land in `outputs_openai/runs/<set>__<model>__<condition>__n<N>/`. Task
sets are model-independent, so every model is scored on identical questions.
OpenAI reasoning models (`gpt-5*`, `o*`) only accept temperature 1 and count
hidden reasoning against the token cap: set `TBYT_TEMPERATURE=1` and
`TBYT_MAX_TOKENS=4000`. Mixing temperatures between models is a confound, so
compare them with that in mind.

## Budget: tying the probe to the parent project's verification budget

The parent project (`dag_codes/`, Allison Li) asks which claims to verify
under a fixed number of checks. A check reveals one claim's truth, a caught
false claim quarantines everything downstream of it, and the score is
`reliability = 1 - undetected_false / total_claims`. Its headline budget is
20 checks on an 80-claim DAG (25%), swept over 5 to 50 checks.

`06_budget.py` (Stage F) runs that exact evaluation on real chains. Each
MuSiQue question is a path step1 → … → final, labelled by Stage D.
Strategies spend 25% of all claims as checks, and the budget is swept over the
same 5/80 to 50/80 shares. Random is the floor and Oracle the ceiling, as in
`dag_model.py`. The strategies are her
uncertainty-first and dependency-aware (`p_false · D`) rules, self-consistency,
composition (`delta_comp · D`), and the H1 comparison in budget terms: a learned
`p_false` from the baseline features vs. the same plus `delta_comp`.

**Step 1 (now):** fixed budgets. Every question gets the full probe, so the
probe's LLM calls are a separate, fixed cost (reported in `budget.json`). The
question is whether, at the same number of checks, composition-informed
selection leaves fewer false claims undetected.

**Step 2 (only if step 1 is positive): an allocation problem.** Put probes and
checks in one budget `B = c · checks + calls`, where `c` is the cost of one check
in LLM-call units (a human or retrieval check costs far more than a call). The
choices are which questions to probe, how many samples per route (`N`), and how
many checks remain. Because every sample is cached, the reliability-vs-cost
frontier can be computed offline for any `c` from the N=3/5/10 runs: subsample
`N`, probe only the questions whose confidence is ambiguous, and compare with
spending the same budget on extra checks.

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
