---
name: create-plan
description: "Write, and then review and revise, a plan, design or spec. Use when asked to make a plan, design or spec for a product or feature."
metadata:
  author: seitaro-white
---

Create a plan by following the draft and review skills in sequence. Resolve the skill paths below relative to this skill's directory.

Save files under `plans/<name>/` in the project root, creating the directory if needed. Use a short filename-safe name based on the issue, branch, PR, or topic for `<name>`.

1. Read and follow `../draft-plan/SKILL.md`. Save the draft to `plans/<name>/draft.md`.
2. Read and follow `../review-plan/SKILL.md` on that draft, retaining the original conversation context and the draft's user goal and agreed constraints.
3. Save the complete revised plan to `plans/<name>/plan.md`. Return both file paths, the review assessment, and the changelog to the user.

Stop after planning; do not implement the plan.
