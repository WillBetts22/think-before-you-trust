#!/usr/bin/env python3
"""
daily_job.py — chip away at the pilot a little each day until it's finished.

Each run:
    1. builds the pilot set (Stage A) if it doesn't exist yet
    2. runs Stage B, then Stage C, until today's budget runs out — either
       DAILY_MAX_API_CALLS (our cap) or the provider's daily quota
    3. once B and C both complete, runs Stages D and E, writes outputs/DONE,
       and sends a macOS notification; later runs then do nothing

Nothing is lost when a day's budget runs out: every call is cached, so the
next run replays finished work from disk for free and continues where it
stopped. Progress is appended to outputs/daily_log.txt.

Edits to outputs/audit.csv (include=0) take effect from the next run.

Scheduled by launchd (see run_daily.sh and the plist in README.md), or run by hand:
    DAILY_MAX_API_CALLS=500 python3 daily_job.py
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime

import config

OUT = config.OUTPUT_DIR
LOG = OUT / "daily_log.txt"
EXIT_BUDGET = 75


def log(msg: str) -> None:
    line = f"[{datetime.now():%Y-%m-%d %H:%M}] {msg}"
    print(line, flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def stage(script: str) -> int:
    log(f"running {script}")
    proc = subprocess.run([sys.executable, script], cwd=config.PROJECT_DIR,
                          capture_output=True, text=True)
    tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
    for line in tail:
        log(f"  {line}")
    return proc.returncode


def cached_calls() -> int:
    return sum(1 for _ in config.CACHE_DIR.rglob("*.json")) if config.CACHE_DIR.exists() else 0


def notify(msg: str) -> None:
    subprocess.run(["osascript", "-e", f'display notification "{msg}" with title "TBYT pilot"'],
                   capture_output=True)


def main() -> int:
    if (OUT / "DONE").exists():
        log("pilot already finished — nothing to do (remove the launchd job: see README)")
        return 0

    before = cached_calls()
    if not (OUT / "tasks.jsonl").exists():
        if stage("01_build_pilot.py") != 0:
            log("Stage A failed")
            return 1

    for script, product in (("02_generate_original.py", "original.jsonl"),
                            ("03_run_probes.py", "probes.jsonl")):
        if (OUT / product).exists():
            continue
        code = stage(script)
        if code == EXIT_BUDGET:
            log(f"budget used up for today; new API calls this run: {cached_calls() - before}")
            return 0
        if code != 0:
            log(f"{script} failed with exit code {code}; will retry next run")
            notify(f"{script} failed — see outputs/daily_log.txt")
            return 1

    for script in ("04_label.py", "05_analyze.py"):
        if stage(script) != 0:
            log(f"{script} failed")
            return 1
    (OUT / "DONE").write_text(datetime.now().isoformat())
    log(f"pilot finished; results in {OUT / 'results.json'}")
    notify("Pilot finished — results in outputs/results.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
