"""
config.py — every knob of the Project 1 protocol in one place.

The abstract requires the estimator and sampling procedure to be "selected
during development and frozen before testing". Each stage copies this config
into its output folder (config_snapshot.json), so a run can always be traced
back to the exact settings that produced it. Change values here, not inside
the stage scripts.
"""

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parent.parent
MUSIQUE_DIR = REPO_ROOT / "multihop_data" / "data"

# ── data selection (Stage A) ─────────────────────────────────────────────────
# Pilot is drawn from MuSiQue *train* so dev/test stay untouched for the
# later development and held-out evaluation sets.
SOURCE_FILE = "musique_ans_v1.0_train.jsonl"
PILOT_SIZE = 100
# Hop counts to include. The paper starts with clean two-step chains; add 3/4
# once the basic test works. Only linear chains are ever selected (branching
# decompositions such as 3hop2 / 4hop2 / 4hop3 are filtered out structurally).
HOPS = (2,)
SELECTION_SEED = 0

# ── model (Stages B and C) ───────────────────────────────────────────────────
# provider: "groq" | "openrouter" | "openai" | "anthropic" | "mock"
# TBYT_PROVIDER / TBYT_MODEL override these (used by the daily job's env file).
PROVIDER = os.environ.get("TBYT_PROVIDER", "groq")
MODEL = os.environ.get("TBYT_MODEL", "openai/gpt-oss-120b")
# TBYT_TEMPERATURE / TBYT_MAX_TOKENS / TBYT_CONDITION / TBYT_SAMPLES_PER_ROUTE /
# TBYT_WORKERS override the values below; the defaults are what the Groq pilot
# runs with. Each stage's config snapshot records the values actually used.
TEMPERATURE = float(os.environ.get("TBYT_TEMPERATURE", "0.7"))  # > 0 so repeated samples form a distribution
# For OpenAI reasoning models (gpt-5*, o*) this cap also covers hidden reasoning
# tokens, so give them more room (e.g. TBYT_MAX_TOKENS=4000).
MAX_TOKENS = int(os.environ.get("TBYT_MAX_TOKENS", "512"))
# OpenAI reasoning models only: "none" (gpt-5.1+, allows any temperature) | "minimal" | "low" | "medium" | "high".
REASONING_EFFORT = os.environ.get("TBYT_REASONING_EFFORT", "low")
# "open_book": every call gets the same 20 MuSiQue paragraphs (evidence +
#              distractors, supporting flags hidden) — the paper's primary condition.
# "closed_book": no paragraphs; answers come from model knowledge.
CONDITION = os.environ.get("TBYT_CONDITION", "open_book")

# ── composition probes (Stage C) ─────────────────────────────────────────────
SAMPLES_PER_ROUTE = int(os.environ.get("TBYT_SAMPLES_PER_ROUTE", "3"))  # the paper's 3 direct + 3x(f then g) = 9 calls per test
# Same-route control: draw a second independent batch per route so we can
# measure ordinary sampling disagreement (direct-vs-direct, step-vs-step).
# Doubles probe cost; required for H1's "beyond ordinary disagreement" claim.
SAME_ROUTE_CONTROL = True
# Questions probed in parallel in Stage C. 1 = one at a time (the Groq daily
# job, which must stay under a per-day quota). Results don't depend on it.
WORKERS = int(os.environ.get("TBYT_WORKERS", "1"))

# ── labeling (Stage D) ───────────────────────────────────────────────────────
F1_CORRECT_THRESHOLD = 0.8   # token-F1 against gold+aliases to auto-label "correct"

# ── analysis (Stage E) ───────────────────────────────────────────────────────
CV_FOLDS = 5
BOOTSTRAP_ITERS = 2000

OUTPUT_DIR = Path(os.environ.get("TBYT_OUTPUT_DIR", PROJECT_DIR / "outputs"))
CACHE_DIR = PROJECT_DIR / "cache"


def snapshot() -> dict:
    """All upper-case settings as a JSON-serialisable dict."""
    out = {}
    for k, v in globals().items():
        if k.isupper():
            out[k] = str(v) if isinstance(v, Path) else v
    return out
