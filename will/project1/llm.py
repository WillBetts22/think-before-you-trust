"""
llm.py — one chat-completion call, with on-disk caching and usage logging.

Providers follow the convention of llm_runs_pipeline/generate_runs.py: keys
come from environment variables, never from code.

    groq        GROQ_API_KEY         (OpenAI-compatible)
    openrouter  OPENROUTER_API_KEY   (OpenAI-compatible)
    openai      OPENAI_API_KEY       (OpenAI-compatible)
    anthropic   ANTHROPIC_API_KEY    (Messages API)
    mock        none — returns canned answers so the pipeline can be smoke-tested
                for free. Mock output is meaningless; never analyse it.

Every call is cached under cache/<provider>/<model>/ keyed by
(system, user, temperature, sample_index). Re-running a stage therefore costs
nothing and reproduces the same samples; bump sample_index to get a fresh,
independent sample of the same prompt.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import threading
import time
from dataclasses import dataclass
from datetime import date

import requests

import config

OPENAI_COMPATIBLE = {
    "groq": ("https://api.groq.com/openai/v1/chat/completions", "GROQ_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1/chat/completions", "OPENROUTER_API_KEY"),
    "openai": ("https://api.openai.com/v1/chat/completions", "OPENAI_API_KEY"),
}
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

# OpenAI reasoning models: they take max_completion_tokens (which also covers
# hidden reasoning tokens) and reasoning_effort, and reject any temperature but 1.
OPENAI_REASONING = re.compile(r"^(o\d|gpt-5)", re.I)


class BudgetExhausted(Exception):
    """Today's call budget (ours or the provider's daily quota) is used up.

    Stages let this propagate; daily_job.py catches it and resumes tomorrow,
    when everything already done is served from the cache for free.
    """


def _parse_wait(msg: str) -> float | None:
    """Seconds from 'try again in 1h2m3.4s' / '7m12s' / '850ms' style messages."""
    m = re.search(r"try again in ((?:[\d.]+(?:h|ms|m|s))+)", msg)
    if not m:
        return None
    total = 0.0
    for val, unit in re.findall(r"([\d.]+)(h|ms|m|s)", m.group(1)):
        total += float(val) * {"h": 3600, "m": 60, "s": 1, "ms": 0.001}[unit]
    return total


@dataclass
class Completion:
    text: str
    prompt_tokens: int
    completion_tokens: int
    latency_s: float
    cached: bool


class LLM:
    def __init__(self, provider: str = config.PROVIDER, model: str = config.MODEL,
                 temperature: float = config.TEMPERATURE,
                 max_tokens: int = config.MAX_TOKENS):
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        safe_model = re.sub(r"[^A-Za-z0-9._-]", "_", model)
        self.cache_dir = config.CACHE_DIR / provider / safe_model
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # running totals, for the cost accounting the abstract requires
        self.calls = 0
        self.api_calls = 0
        # Daily cap on *new* API calls, shared across stages and restarts by
        # counting cache files written today. 0 / unset = no cap.
        self.daily_cap = int(os.environ.get("DAILY_MAX_API_CALLS", "0") or 0)
        today = date.today()
        self.calls_today = sum(
            1 for f in self.cache_dir.glob("*.json")
            if date.fromtimestamp(f.stat().st_mtime) == today
        )
        self.prompt_tokens = 0
        self.completion_tokens = 0
        # Stage C can call complete() from several threads (config.WORKERS)
        self._lock = threading.Lock()

        self.openai_reasoning = provider == "openai" and bool(OPENAI_REASONING.match(model))
        # gpt-5.1+ accept any temperature when reasoning_effort is "none"; with reasoning
        # on (and for gpt-5 / o-series always) only the default temperature of 1 works.
        self.send_temperature = not self.openai_reasoning or config.REASONING_EFFORT == "none"
        if not self.send_temperature and temperature != 1:
            raise SystemExit(f"{model} with reasoning only accepts temperature 1; set TBYT_TEMPERATURE=1 "
                             f"(and a larger TBYT_MAX_TOKENS, since reasoning tokens count), "
                             f"or TBYT_REASONING_EFFORT=none on gpt-5.1 and later.")

        if provider in OPENAI_COMPATIBLE:
            self.url, key_env = OPENAI_COMPATIBLE[provider]
        elif provider == "anthropic":
            self.url, key_env = ANTHROPIC_URL, "ANTHROPIC_API_KEY"
        elif provider == "mock":
            self.url, key_env = None, None
        else:
            raise ValueError(f"unknown provider {provider!r}")
        self.api_key = os.environ.get(key_env) if key_env else None
        if key_env and not self.api_key:
            raise SystemExit(f"Set {key_env} in your environment to use provider {provider!r}.")

    # ── public ──────────────────────────────────────────────────────────────
    def complete(self, system: str, user: str, sample_index: int = 0) -> Completion:
        key = hashlib.sha256(json.dumps(
            [system, user, self.temperature, self.max_tokens, sample_index]
        ).encode()).hexdigest()
        path = self.cache_dir / f"{key}.json"
        with self._lock:
            self.calls += 1
        if path.exists():
            d = json.loads(path.read_text())
            c = Completion(d["text"], d["prompt_tokens"], d["completion_tokens"],
                           d["latency_s"], cached=True)
        else:
            with self._lock:
                if self.daily_cap and self.calls_today >= self.daily_cap:
                    raise BudgetExhausted(f"daily cap of {self.daily_cap} API calls reached")
            c = self._call_with_retries(system, user, sample_index)
            # write to a temp file and rename, so a crash never leaves a half-written cache entry
            tmp = path.with_suffix(f".tmp{threading.get_ident()}")
            tmp.write_text(json.dumps({
                "system": system, "user": user, "sample_index": sample_index,
                "temperature": self.temperature, "model": self.model,
                "text": c.text, "prompt_tokens": c.prompt_tokens,
                "completion_tokens": c.completion_tokens, "latency_s": c.latency_s,
            }))
            tmp.replace(path)
            with self._lock:
                self.calls_today += 1
                self.api_calls += 1
        with self._lock:
            self.prompt_tokens += c.prompt_tokens
            self.completion_tokens += c.completion_tokens
        return c

    def usage(self) -> dict:
        return {"calls": self.calls, "api_calls": self.api_calls,
                "prompt_tokens": self.prompt_tokens,
                "completion_tokens": self.completion_tokens}

    # ── internals ───────────────────────────────────────────────────────────
    def _call_with_retries(self, system, user, sample_index, max_retries=10) -> Completion:
        attempt = 0
        throttled = 0          # short per-minute rate-limit waits; these don't use up retries
        while attempt < max_retries:
            attempt += 1
            try:
                return self._call(system, user, sample_index)
            except Exception as e:
                msg = str(e)
                # out of credit or a bad key: retrying won't help
                if re.search(r"insufficient_quota|exceeded your current quota", msg, re.I):
                    raise BudgetExhausted(f"provider quota/billing: {msg[:200]}")
                if msg.startswith(("401:", "403:", "404:")):
                    raise SystemExit(f"API rejected the request: {msg[:300]}")
                wait = _parse_wait(msg)
                # A long wait means a per-day quota, not a per-minute one: stop for today.
                if (wait is not None and wait > 300) or re.search(r"per day|\bTPD\b|\bRPD\b", msg):
                    raise BudgetExhausted(f"provider daily limit: {msg[:200]}")
                if msg.startswith("429:") and wait is not None and wait < 60 and throttled < 500:
                    throttled += 1
                    attempt -= 1
                    time.sleep(wait + random.uniform(0.2, 2.0))   # jitter so workers don't retry in lockstep
                    continue
                wait = wait + 1 if wait is not None else min(60, 2 ** attempt)
                print(f"    API error (attempt {attempt}/{max_retries}): {msg[:200]} — retry in {wait:.0f}s")
                time.sleep(wait)
        raise RuntimeError("API call failed after retries")

    def _call(self, system, user, sample_index) -> Completion:
        t0 = time.time()
        if self.provider == "mock":
            return self._mock(user, sample_index, t0)

        if self.provider == "anthropic":
            headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01",
                       "content-type": "application/json"}
            payload = {"model": self.model, "system": system, "max_tokens": self.max_tokens,
                       "temperature": self.temperature,
                       "messages": [{"role": "user", "content": user}]}
            resp = requests.post(self.url, headers=headers, json=payload, timeout=180)
            if resp.status_code != 200:
                raise RuntimeError(f"{resp.status_code}: {resp.text[:300]}")
            d = resp.json()
            text = "".join(b.get("text", "") for b in d.get("content", []))
            u = d.get("usage", {})
            return Completion(text, u.get("input_tokens", 0), u.get("output_tokens", 0),
                              time.time() - t0, cached=False)

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "temperature": self.temperature,
                   "max_tokens": self.max_tokens,
                   "messages": [{"role": "system", "content": system},
                                {"role": "user", "content": user}]}
        if self.provider == "openai":
            # OpenAI replaced max_tokens with max_completion_tokens (works for every model)
            payload["max_completion_tokens"] = payload.pop("max_tokens")
            if self.openai_reasoning:
                if not self.send_temperature:
                    del payload["temperature"]      # only the default (1) is allowed
                payload["reasoning_effort"] = config.REASONING_EFFORT
        elif "gpt-oss" in self.model.lower():
            if self.provider == "groq":
                payload["reasoning_effort"] = "low"
            else:
                payload["reasoning"] = {"effort": "low"}
        resp = requests.post(self.url, headers=headers, json=payload, timeout=180)
        if resp.status_code != 200:
            try:
                msg = resp.json().get("error", {}).get("message", resp.text[:300])
            except Exception:
                msg = resp.text[:300]
            raise RuntimeError(f"{resp.status_code}: {msg}")
        d = resp.json()
        u = d.get("usage", {})
        return Completion(d["choices"][0]["message"]["content"],
                          u.get("prompt_tokens", 0), u.get("completion_tokens", 0),
                          time.time() - t0, cached=False)

    def _mock(self, user, sample_index, t0) -> Completion:
        """Canned, gold-free answers drawn from a tiny pool, seeded by the prompt."""
        rng = random.Random(f"{user}|{sample_index}")
        pool = ["Alpha", "Beta", "Beta", "Gamma", "unknown"]
        if '"intermediate_answers"' in user:
            n = len(re.findall(r"^\s*\d+\.", user.split("Steps:")[-1], re.M)) or 2
            obj = {"intermediate_answers": [rng.choice(pool) for _ in range(n)],
                   "final_answer": rng.choice(pool), "confidence": rng.randint(20, 100)}
            text = json.dumps(obj)
        else:
            text = json.dumps({"answer": rng.choice(pool)})
        return Completion(text, len(user) // 4, len(text) // 4, time.time() - t0, cached=False)
