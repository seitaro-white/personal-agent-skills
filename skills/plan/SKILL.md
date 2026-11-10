---
name: plan
description: "Plan a feature or change with the user by interviewing them, researching the codebase and external options through subagents, and agreeing a brief. Use when asked to plan, design or spec something."
metadata:
  author: seitaro-white
---

Plan the work with the user until you agree a brief. Do not implement anything. Resolve paths below relative to this skill's directory.

1. Read and follow `../grill-me/SKILL.md` to interview the user. Keep going until the frontier is empty.
2. Get facts through subagents instead of reading the codebase yourself. You are authorised to launch these, in parallel where questions are independent:
   - `scout` for codebase questions: where something lives, how it works, what a change would touch. Give it a specific question, not "read the codebase".
   - `researcher` for anything outside the codebase: libraries, APIs, standard approaches, best practice. Before recommending a library, tool or approach, have `researcher` compare the options. Do not rely on memory for these.
   Ask the user only for decisions, never for facts a subagent can find.
3. Write the brief in the `hand-off` skill's brief format and show it to the user in the conversation. Do not save it to the repository.
4. When the user confirms it, offer to hand it off with the `hand-off` skill.
