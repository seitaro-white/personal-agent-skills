---
name: start-worker
description: "Start an independent Pi worker for one branch in its own Herdr worktree workspace. Use when an orchestrator needs to start a worker. Requires HERDR_ENV=1."
metadata:
  author: seitaro-white
---

Start one worker per branch. Resolve paths below relative to this skill's directory.

1. Check `test "${HERDR_ENV:-}" = 1`. If it fails, say you are not running inside Herdr and stop.
2. Write the task in the format below to a temporary file from `mktemp`, not into the repository.
3. From the main checkout, run `<this skill directory>/start-worker.sh <branch> <task-file>`. It creates the worktree with agent, diff and shell tabs, waits for Pi to be idle, sends the task, and confirms the worker is working before printing its agent name. Readiness and task pickup each have a 30-second timeout. If it fails, inspect `herdr agent get <name>` and `herdr agent read <name>` before retrying; the task may already have been delivered.
4. The worker messages you when it finishes or needs you. Reply with `herdr agent prompt <name> "<reply>"`.

Launch arguments come from `$PI_AGENT_PROFILES/worker.args`, one Pi CLI argument per line (no quoting or comments). If the variable is unset or the file is missing, Pi uses the user's normal settings, plus the worker role prompt.

## Task format

### Goal

<what the worker should achieve>

### Scope

- In: <what to change>
- Out: <what to leave alone>

### Context

<relevant files, decisions already made, constraints>

### Done when

- <checkable completion criteria>

### Escalate if

- <decisions the worker must not make alone>
