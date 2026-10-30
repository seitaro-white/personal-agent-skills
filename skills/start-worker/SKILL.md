---
name: start-worker
description: "Start an independent Pi worker for one branch in its own Herdr worktree workspace. Use when an orchestrator needs to start a worker. Requires HERDR_ENV=1."
metadata:
  author: seitaro-white
---

Start one worker per branch. Resolve paths below relative to this skill's directory.

1. Check `test "${HERDR_ENV:-}" = 1`. If it fails, say you are not running inside Herdr and stop.
2. Write the task to `plans/<name>/tasks/<branch>.md` in the format below, next to the brief.
3. From the main checkout, run `<this skill directory>/start-worker.sh <branch> <task-file>`. It creates the worktree with agent, diff and shell tabs, sends the task, and prints the worker's agent name.
4. The worker messages you when it finishes or needs you. Reply with `herdr agent prompt <name> "<reply>"`.

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
