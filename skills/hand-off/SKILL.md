---
name: hand-off
description: "Hand an agreed brief to this repository's Pi orchestrator in its Herdr tab, starting it if needed. The orchestrator runs workers in separate worktrees. Use when asked to hand off a plan or issue for implementation. Requires HERDR_ENV=1."
metadata:
  author: seitaro-white
---

Hand off one brief at a time; later briefs go to the same orchestrator. Resolve paths below relative to this skill's directory.

1. Check `test "${HERDR_ENV:-}" = 1`. If it fails, say you are not running inside Herdr and stop.
2. Write the brief to `plans/<name>/plan.md` in the project root in the format below, or reuse an existing plan there. Use a short filename-safe `<name>`. Confirm the brief with the user before handing it off.
3. From the main checkout, run `<this skill directory>/hand-off.sh plans/<name>/plan.md`. It starts the orchestrator in its own tab if none is running, waits until it is idle or done, sends it the brief's path, and confirms it is working before printing its agent name. Readiness and brief pickup each have a 30-second timeout. If it fails, inspect `herdr agent get <name>` and `herdr agent read <name>` before retrying; the brief may already have been delivered.
4. Tell the user the agent name. Do not follow up with the orchestrator; the user talks to it in its tab.

Launch arguments come from `$PI_AGENT_PROFILES/orchestrator.args`, one Pi CLI argument per line (no quoting or comments). If the variable is unset or the file is missing, Pi uses the user's normal settings, plus the orchestrator role prompt.

## Brief format

### Goal

<what this issue should achieve>

### User priorities

- <what matters most to the user>

### Branches

<branches to run in parallel, and any that must wait for another to merge>

### Decisions

- <what was agreed, and what must be escalated>
