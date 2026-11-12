#!/usr/bin/env bash
# OpenAI data-collection pipeline, kept separate from the Groq daily job.
#
#   ./run_openai.sh check                       key works? list chat models, make one test call
#   ./run_openai.sh replicate                   copy the Groq pilot's 100 audited tasks into
#                                               task set "pilot100" (same questions, new model)
#   ./run_openai.sh build <set> <n> <hops>      new task set, e.g.  build scale300 300 2,3,4
#                                               then audit outputs_openai/sets/<set>/audit.csv
#   ./run_openai.sh run <set>                   Stages B-E for TBYT_MODEL on that task set
#   ./run_openai.sh smoke                       3 questions from pilot100, real API, to test settings
#   ./run_openai.sh analyze <run dir>           rerun Stages E-F only (no API calls)
#
# Settings and key: ~/.config/tbyt/openai.env (outside the repo, never committed).
# Any TBYT_* variable there (or on the command line) overrides config.py, e.g.
#   TBYT_MODEL=gpt-4.1-mini TBYT_SAMPLES_PER_ROUTE=5 ./run_openai.sh run pilot100
#
# Layout (gitignored):
#   outputs_openai/sets/<set>/            tasks.jsonl, gold.jsonl, audit.csv  (model-independent)
#   outputs_openai/runs/<set>__<model>__<condition>__n<N>/   everything Stages B-E write
#   cache/openai/<model>/                 every API response, so reruns are free
# The Groq pilot (outputs/, cache/groq/, daily_job.py, STATUS.md) is never touched.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

ENV_FILE="$HOME/.config/tbyt/openai.env"
if [[ -f "$ENV_FILE" ]]; then
  # command-line TBYT_* values win over the file
  saved=$(env | grep -E '^TBYT_' || true)
  set -a; source "$ENV_FILE"; set +a
  while IFS= read -r kv; do [[ -n "$kv" ]] && export "$kv"; done <<< "$saved"
fi
export TBYT_PROVIDER=openai
export TBYT_MODEL="${TBYT_MODEL:-gpt-4.1}"
export TBYT_WORKERS="${TBYT_WORKERS:-8}"
unset DAILY_MAX_API_CALLS GROQ_API_KEY
: "${OPENAI_API_KEY:?Set OPENAI_API_KEY in $ENV_FILE}"

SETS=outputs_openai/sets
safe_model=$(echo "$TBYT_MODEL" | sed 's/[^A-Za-z0-9._-]/_/g')

run_dir() {   # one folder per (task set, model, condition, samples per route)
  echo "outputs_openai/runs/$1__${safe_model}__${TBYT_CONDITION:-open_book}__n${TBYT_SAMPLES_PER_ROUTE:-3}"
}

stages() {    # $1 = run dir that already holds the task files
  python3 02_generate_original.py --out "$1"
  python3 03_run_probes.py --out "$1"
  python3 04_label.py --out "$1"
  python3 05_analyze.py --out "$1"
  python3 06_budget.py --out "$1"
  echo "Done: $1/results.json, $1/budget.json"
}

seed_run() {  # copy a task set's files into a fresh run dir
  local set=$1 dir; dir=$(run_dir "$set")
  [[ -f "$SETS/$set/tasks.jsonl" ]] || { echo "no task set '$set' (build or replicate first)"; exit 1; }
  mkdir -p "$dir"
  for f in tasks.jsonl gold.jsonl audit.csv config_snapshot_A.json; do
    [[ -f "$dir/$f" ]] || cp "$SETS/$set/$f" "$dir/"
  done
  echo "$dir"
}

cmd="${1:-}"
case "$cmd" in
  check)
    python3 - <<'PY'
import os, re, requests
h = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}
r = requests.get("https://api.openai.com/v1/models", headers=h, timeout=30)
r.raise_for_status()
ids = sorted(m["id"] for m in r.json()["data"])
chat = [i for i in ids if re.match(r"(gpt-|o\d)", i) and not re.search(r"audio|realtime|transcribe|tts|image|search", i)]
print("Chat models on this key:\n  " + "\n  ".join(chat))
import llm
m = os.environ["TBYT_MODEL"]
c = llm.LLM("openai", m)._call("Respond with JSON only.", 'Capital of France? {"answer": "..."}', 0)
print(f"\nTest call to {m}: {c.text!r}  ({c.prompt_tokens} in / {c.completion_tokens} out, {c.latency_s:.1f}s)")
PY
    ;;
  replicate)
    mkdir -p "$SETS/pilot100"
    for f in tasks.jsonl gold.jsonl audit.csv config_snapshot_A.json; do
      cp -n "outputs/$f" "$SETS/pilot100/" 2>/dev/null || true
    done
    echo "Task set pilot100 = the Groq pilot's 100 audited questions."
    echo "Next: ./run_openai.sh run pilot100"
    ;;
  build)
    set_name="${2:?set name}"; n="${3:?number of questions}"; hops="${4:-2}"
    python3 01_build_pilot.py --n "$n" --hops "$hops" --out "$SETS/$set_name"
    echo "Audit $SETS/$set_name/audit.csv (include=0 to drop), then: ./run_openai.sh run $set_name"
    ;;
  run)
    dir=$(seed_run "${2:?task set name}" | tail -1)
    stages "$dir"
    ;;
  analyze)
    python3 05_analyze.py --out "${2:?run dir}" > /dev/null
    python3 06_budget.py --out "$2"
    ;;
  smoke)
    [[ -f "$SETS/pilot100/tasks.jsonl" ]] || "$0" replicate
    dir="outputs_openai/runs/smoke__${safe_model}"
    rm -rf "$dir"; mkdir -p "$dir"
    head -3 "$SETS/pilot100/tasks.jsonl" > "$dir/tasks.jsonl"
    cp "$SETS/pilot100/gold.jsonl" "$dir/"
    stages "$dir"
    ;;
  *)
    sed -n '2,24p' "$0"; exit 1
    ;;
esac
