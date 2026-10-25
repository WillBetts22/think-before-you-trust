#!/usr/bin/env bash
# launchd entry point for the daily pilot job. Loads the API key and limits
# from ~/.config/tbyt/env (kept outside the repo so the key is never committed),
# then runs daily_job.py.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
ENV_FILE="$HOME/.config/tbyt/env"
if [[ -f "$ENV_FILE" ]]; then
  set -a; source "$ENV_FILE"; set +a
fi
exec /usr/bin/python3 daily_job.py
