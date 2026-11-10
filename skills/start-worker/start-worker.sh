#!/usr/bin/env bash
# Start a Pi worker for one branch in a new Herdr worktree workspace.
#
# Usage: start-worker.sh <branch> <task-file>
#
# Run from inside the main checkout, in a Herdr pane. Creates three tabs:
#   agent  Pi worker, launched with flags from PI_AGENT_PROFILES
#   diff   hunk diff main...HEAD --watch for committed branch changes
#   shell  plain shell for servers and ad hoc commands
# Then sends the worker its name, the orchestrator's name and <task-file>, and
# prints the worker's agent name.
set -euo pipefail

launch_args=()
if [[ -n ${PI_AGENT_PROFILES:-} && -f $PI_AGENT_PROFILES/worker.args ]]; then
  mapfile -t launch_args < "$PI_AGENT_PROFILES/worker.args"
fi
WORKER_ROLE_PROMPT="$(cd "$(dirname "$0")" && pwd)/worker.md"
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
herdr tab rename "$(field result.tab.tab_id <<<"$created")" agent >/dev/null
herdr agent start "$name" --kind pi --pane "$(field result.root_pane.pane_id <<<"$created")" -- \
  "${launch_args[@]}" \
  --append-system-prompt "$WORKER_ROLE_PROMPT" >/dev/null

diff_tab=$(herdr tab create --workspace "$workspace" --cwd "$worktree" --label diff --no-focus)
herdr pane run "$(field result.root_pane.pane_id <<<"$diff_tab")" "hunk diff main...HEAD --watch" >/dev/null

herdr tab create --workspace "$workspace" --cwd "$worktree" --label shell --no-focus >/dev/null

# Starting Pi is not enough: wait for input readiness, then confirm task pickup.
herdr agent wait "$name" --until idle --timeout 30000 >/dev/null
herdr agent prompt "$name" "You are $name. Your orchestrator is $orchestrator.

$(cat "$task_file")" --wait --until working --timeout 30000 >&2
echo "$name"
