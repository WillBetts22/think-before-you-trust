"""
common.py — shared helpers: jsonl I/O, answer normalisation, distances.
"""

from __future__ import annotations

import json
import re
import string
from collections import Counter
from pathlib import Path

import config

# Explicit outcomes kept in the answer space (abstract §4: "including explicit
# outcomes for abstention and invalid responses").
ABSTAIN = "<ABSTAIN>"
INVALID = "<INVALID>"

_ABSTAIN_PATTERNS = re.compile(
    r"^(unknown|i don'?t know|not (stated|mentioned|given|provided|available)|"
    r"cannot (be )?determined?|insufficient information|n/?a|none)\b",
    re.I,
)


# ── I/O ──────────────────────────────────────────────────────────────────────
def read_jsonl(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def save_config_snapshot(out_dir: Path, stage: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / f"config_snapshot_{stage}.json", "w") as f:
        json.dump(config.snapshot(), f, indent=2)


# ── normalisation (SQuAD-style) ──────────────────────────────────────────────
def normalize(text: str | None) -> str:
    """Map a raw model answer to an answer identity.

    Lower-case, strip punctuation / articles / whitespace. Abstentions and
    empty or unparseable answers become explicit outcomes rather than being
    dropped. Uses no gold information, so it is safe for the detector.
    """
    if text is None:
        return INVALID
    t = str(text).strip()
    if not t:
        return INVALID
    if _ABSTAIN_PATTERNS.match(t):
        return ABSTAIN
    t = t.lower()
    t = "".join(ch for ch in t if ch not in set(string.punctuation))
    t = re.sub(r"\b(a|an|the)\b", " ", t)
    t = " ".join(t.split())
    return t or INVALID


def token_f1(pred: str, gold: str) -> float:
    p, g = normalize(pred).split(), normalize(gold).split()
    if not p or not g:
        return float(p == g)
    common = Counter(p) & Counter(g)
    same = sum(common.values())
    if same == 0:
        return 0.0
    prec, rec = same / len(p), same / len(g)
    return 2 * prec * rec / (prec + rec)


# ── distances between answer distributions ───────────────────────────────────
def distribution(answers: list[str]) -> dict[str, float]:
    ids = [normalize(a) for a in answers]
    n = len(ids)
    return {k: v / n for k, v in Counter(ids).items()} if n else {}


def tv_distance(p: dict[str, float], q: dict[str, float]) -> float:
    """d_TV(P, Q) = 1/2 * sum_a |P(a) - Q(a)| over the union of answer ids."""
    support = set(p) | set(q)
    return 0.5 * sum(abs(p.get(a, 0.0) - q.get(a, 0.0)) for a in support)


def mode_answer(answers: list[str]) -> str | None:
    ids = [normalize(a) for a in answers]
    return Counter(ids).most_common(1)[0][0] if ids else None


# ── JSON extraction from model output ────────────────────────────────────────
def extract_json_object(text: str) -> dict | None:
    """Pull the first {...} object out of a response that may contain fences or prose."""
    if not text:
        return None
    cleaned = re.sub(r"```(?:json)?", "", text).strip()
    try:
        obj = json.loads(cleaned)
        return obj if isinstance(obj, dict) else None
    except Exception:
        pass
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start != -1 and end > start:
        try:
            obj = json.loads(cleaned[start:end + 1])
            return obj if isinstance(obj, dict) else None
        except Exception:
            return None
    return None


def load_included_tasks(out_dir: Path) -> list[dict]:
    """tasks.jsonl minus anything the auditor marked include=0 in audit.csv."""
    import csv
    tasks = read_jsonl(out_dir / "tasks.jsonl")
    audit_path = out_dir / "audit.csv"
    if not audit_path.exists():
        return tasks
    with open(audit_path) as f:
        keep = {r["id"] for r in csv.DictReader(f) if str(r["include"]).strip() not in ("0", "")}
    return [t for t in tasks if t["id"] in keep]


def save_usage(out_dir: Path, stage: str, usage: dict) -> None:
    with open(out_dir / f"usage_{stage}.json", "w") as f:
        json.dump(usage, f, indent=2)
