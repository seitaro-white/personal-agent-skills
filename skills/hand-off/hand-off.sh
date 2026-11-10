#!/usr/bin/env bash
# Hand a brief to this repository's Pi orchestrator, starting it first if needed.
#
# Usage: hand-off.sh <brief-file>
#
# Run from inside the main checkout, in a Herdr pane. Sends the brief's contents,
# so the file can be temporary. The orchestrator is named
# after the repository and runs in its own tab of the current workspace, so later
# briefs go to the same one. Prints the orchestrator's agent name.
set -euo pipefail

launch_args=()
if [[ -n ${PI_AGENT_PROFILES:-} && -f $PI_AGENT_PROFILES/orchestrator.args ]]; then
  mapfile -t launch_args < "$PI_AGENT_PROFILES/orchestrator.args"
fi
ORCHESTRATOR_ROLE_PROMPT="$(cd "$(dirname "$0")" && pwd)/orchestrator.md"

brief_file=$1
repo=$(basename "$(git rev-parse --show-toplevel)")
# Herdr agent names must match [a-z][a-z0-9_-]{0,31}.
name=$(printf 'orch-%s' "$repo" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9_-' '-' | cut -c1-32)

# Print a dotted field from the JSON on stdin, e.g. `field result.tab.tab_id`.
field() {
  python3 -c '
import json, sys
value = json.load(sys.stdin)
for key in sys.argv[1].split("."):
    value = value[key]
print(value)' "$1"
}

message="New brief:

$(cat "$brief_file")"
if ! herdr agent get "$name" >/dev/null 2>&1; then
  tab=$(herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" --label "$name" --no-focus)
  herdr agent start "$name" --kind pi --pane "$(field result.root_pane.pane_id <<<"$tab")" -- \
    "${launch_args[@]}" \
    --append-system-prompt "$ORCHESTRATOR_ROLE_PROMPT" >/dev/null
  message="You are $name. $message"
fi

# Starting Pi is not enough: wait for input readiness, then confirm brief pickup.
herdr agent wait "$name" --until idle --until done --timeout 30000 >/dev/null
herdr agent prompt "$name" "$message" --wait --until working --timeout 30000 >&2
echo "$name"
