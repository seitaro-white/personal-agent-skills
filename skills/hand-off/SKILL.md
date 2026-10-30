---
name: hand-off
description: "Hand an agreed brief to this repository's Pi orchestrator in its Herdr tab, starting it if needed. The orchestrator runs workers in separate worktrees. Use when asked to hand off a plan or issue for implementation. Requires HERDR_ENV=1."
metadata:
  author: seitaro-white
---

Hand off one brief at a time; later briefs go to the same orchestrator. Resolve paths below relative to this skill's directory.

1. Check `test "${HERDR_ENV:-}" = 1`. If it fails, say you are not running inside Herdr and stop.
2. Write the brief to `plans/<name>/plan.md` in the project root in the format below, or reuse an existing plan there. Use a short filename-safe `<name>`. Confirm the brief with the user before handing it off.
3. From the main checkout, run `<this skill directory>/hand-off.sh plans/<name>/plan.md`. It starts the orchestrator in its own tab if none is running, sends it the brief's path, and prints its agent name.
4. Tell the user the agent name. Do not follow up with the orchestrator; the user talks to it in its tab.

## Brief format

### Goal

<what this issue should achieve>

### User priorities

- <what matters most to the user>

### Branches

<branches to run in parallel, and any that must wait for another to merge>

### Decisions

- <what was agreed, and what must be escalated>
