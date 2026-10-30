#!/usr/bin/env bash
# Start a Pi worker for one branch in a new Herdr worktree workspace.
#
# Usage: start-worker.sh <branch> <task-file>
#
# Run from inside the main checkout, in a Herdr pane. Creates three tabs:
#   agent  Pi worker, launched with the flags below
#   diff   hunk diff --watch against the worktree's starting commit
#   shell  plain shell for servers and ad hoc commands
# Then sends the worker its name, the orchestrator's name and <task-file>, and
# prints the worker's agent name.
set -euo pipefail

# Worker launch flags.
WORKER_MODEL="openai-codex/gpt-6.1-sol:medium"
# Only these extensions, plus Pi's built-ins, load; skills load as usual. Paths match each package's
# pi.extensions entry, so package prompt templates stay out.
PI_MODULES=/opt/pi/node_modules
WORKER_EXTENSIONS=(
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
  "$PI_MODULES/pi-context/src/context.ts"
)
WORKER_PROFILE="$(cd "$(dirname "$0")" && pwd)/worker.md"
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE_ROOT="$REPO_ROOT/../worktrees"

branch=$1
task_file=$2
worktree="$WORKTREE_ROOT/$branch"
# Herdr agent names must match [a-z][a-z0-9_-]{0,31}.
name=$(printf 'w-%s' "$branch" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9_-' '-' | cut -c1-32)
# Same name as hand-off.sh gives the orchestrator, so it survives restarts.
repo=$(basename "$REPO_ROOT")
orchestrator=$(printf 'orch-%s' "$repo" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9_-' '-' | cut -c1-32)

extension_args=()
for extension in "${WORKER_EXTENSIONS[@]}"; do
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

# --cwd, or Herdr uses the repo of the calling workspace instead of this one.
created=$(herdr worktree create --cwd "$REPO_ROOT" --branch "$branch" --path "$worktree" --label "$branch" --no-focus)
workspace=$(field result.workspace.workspace_id <<<"$created")
# Diff against the starting commit, not main, so later merges to main stay out.
base=$(git -C "$worktree" rev-parse HEAD)
herdr tab rename "$(field result.tab.tab_id <<<"$created")" agent >/dev/null
herdr agent start "$name" --kind pi --pane "$(field result.root_pane.pane_id <<<"$created")" -- \
  --model "$WORKER_MODEL" \
  --no-extensions \
  "${extension_args[@]}" \
  --append-system-prompt "$WORKER_PROFILE" >/dev/null

diff_tab=$(herdr tab create --workspace "$workspace" --cwd "$worktree" --label diff --no-focus)
herdr pane run "$(field result.root_pane.pane_id <<<"$diff_tab")" "hunk diff $base --watch" >/dev/null

herdr tab create --workspace "$workspace" --cwd "$worktree" --label shell --no-focus >/dev/null

herdr agent prompt "$name" "You are $name. Your orchestrator is $orchestrator.

$(cat "$task_file")" >/dev/null
echo "$name"
