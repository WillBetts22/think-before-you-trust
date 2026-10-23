#!/usr/bin/env bash
# Runs the Project 1 pilot end to end.
#
#   ./run_pilot.sh build                   Stage A only; then audit outputs/audit.csv
#   ./run_pilot.sh run [provider] [model]  Stages B-E on the audited tasks
#   ./run_pilot.sh smoke                   whole pipeline on 5 questions with the free
#                                          mock provider, into outputs_smoke/ (tests code only)
#
# Provider/model default to config.py. API keys come from the environment
# (GROQ_API_KEY, OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

cmd="${1:-}"
case "$cmd" in
  build)
    python3 01_build_pilot.py
    ;;
  run)
    model_args=()
    [[ -n "${2:-}" ]] && model_args+=(--provider "$2")
    [[ -n "${3:-}" ]] && model_args+=(--model "$3")
    python3 02_generate_original.py ${model_args[@]+"${model_args[@]}"}
    python3 03_run_probes.py ${model_args[@]+"${model_args[@]}"}
    python3 04_label.py
    python3 05_analyze.py
    ;;
  smoke)
    out=outputs_smoke
    rm -rf "$out"
    python3 01_build_pilot.py --n 5 --out "$out"
    python3 02_generate_original.py --provider mock --model mock --out "$out"
    python3 03_run_probes.py --provider mock --model mock --out "$out"
    python3 04_label.py --out "$out"
    python3 05_analyze.py --out "$out"
    ;;
  *)
    sed -n '2,10p' "$0"; exit 1
    ;;
esac
