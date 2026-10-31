#!/usr/bin/env bash
# Hand a brief to this repository's Pi orchestrator, starting it first if needed.
#
# Usage: hand-off.sh <brief-file>
#
# Run from inside the main checkout, in a Herdr pane. The orchestrator is named
# after the repository and runs in its own tab of the current workspace, so later
# briefs go to the same one. Prints the orchestrator's agent name.
set -euo pipefail

# Orchestrator launch flags.
ORCHESTRATOR_MODEL="claude-bridge/claude-opus-5-5:high"
# Only these extensions, plus Pi's built-ins, load; skills load as usual. Paths match each package's
# pi.extensions entry, so package prompt templates stay out.
PI_MODULES=/opt/pi/node_modules
ORCHESTRATOR_EXTENSIONS=(
  builtin:mcp
  builtin:llama.cpp
  builtin:codemode
  builtin:tool-search
  "$PI_MODULES/pi-subagents/bundle/index.js"
  "$PI_MODULES/pi-web-access/dist/index.js"
  "$PI_MODULES/@narumitw/pi-lsp/dist/index.ts"
  "$PI_MODULES/pi-calm/extensions/calm/index.ts"
  "$PI_MODULES/pi-claude-bridge/src/index.ts"
  "$PI_MODULES/@danielgap/pi-claude-usage/extensions/claude_usage.ts"
  "$PI_MODULES/pi-context-view/src/index.ts"
  "$PI_MODULES/@narumitw/pi-usage/dist/index.ts"
  "$PI_MODULES/@juicesharp/rpiv-todo/index.ts"
  "$PI_MODULES/pi-stretchtext/index.ts"
)
ORCHESTRATOR_PROFILE="$(cd "$(dirname "$0")" && pwd)/orchestrator.md"

brief=$(realpath "$1")
repo=$(basename "$(git rev-parse --show-toplevel)")
# Herdr agent names must match [a-z][a-z0-9_-]{0,31}.
name=$(printf 'orch-%s' "$repo" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9_-' '-' | cut -c1-32)

extension_args=()
for extension in "${ORCHESTRATOR_EXTENSIONS[@]}"; do
  extension_args+=(-e "$extension")
done

# Print a dotted field from the JSON on stdin, e.g. `field result.tab.tab_id`.
field() {
  python3 -c '
import json, sys
value = json.load(sys.stdin)
for key in sys.argv[1].split("."):
    value = value[key]
print(value)' "$1"
}

message="New brief: $brief"
if ! herdr agent get "$name" >/dev/null 2>&1; then
  tab=$(herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" --label "$name" --no-focus)
  herdr agent start "$name" --kind pi --pane "$(field result.root_pane.pane_id <<<"$tab")" -- \
    --model "$ORCHESTRATOR_MODEL" \
    --no-extensions \
    "${extension_args[@]}" \
    --append-system-prompt "$ORCHESTRATOR_PROFILE" >/dev/null
  message="You are $name. $message"
fi

herdr agent prompt "$name" "$message" >/dev/null
echo "$name"
