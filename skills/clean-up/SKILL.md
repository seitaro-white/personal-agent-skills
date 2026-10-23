---
name: clean-up
description: "Clean up accumulated duplication and historical residue across a codebase, and flag structural drift for separate refactoring. Use after implementation commits, before merging a feature branch, or when asked for a codebase cleanup."
metadata:
  author: seitaro-white
---

Inspect the codebase and directly apply worthwhile cleanups so it expresses one coherent, current implementation. Prioritize simplicity and understandability, making the code easier to change without speculative abstractions or extension points.

This normally runs on a feature branch after implementation commits and before merging. Check the current branch and working-tree state before editing. Use the agreed merge target and feature diff, where available, to understand recent work, but look beyond changed lines for codebase-level problems. For a pre-merge cleanup, clarify the merge target if it cannot be established. Recommend a separate branch rather than making cleanup edits directly on the merge target; do not switch branches automatically.

Use the user request, agreed constraints, and plan where available to establish intended behaviour. Inspect related code, tests, comments, and documentation together, rather than reviewing each changed file in isolation.

Look for:
- **Duplicated knowledge or responsibility.** Consolidate equivalent logic, repeated explanations, and tests that cover the same behaviour without a meaningful distinction. Prefer one authoritative explanation with references where useful. Preserve tests that protect distinct cases, boundaries, or regressions.
- **Contradictory or stale descriptions.** Reconcile comments, documentation, examples, and tests that disagree about intended behaviour. Do not assume the newest implementation is automatically correct or weaken tests merely to match it. Flag material uncertainty rather than guessing.
- **Historical residue and redundant negative assertions.** Remove commentary that narrates discarded approaches, development conversations, or prohibitions against behaviour nobody would otherwise expect. Ordinary comments and documentation should explain the current system. Keep warnings that communicate real constraints or plausible pitfalls, and preserve useful history in changelogs and intentional design-decision records.
- **Structural drift to flag, not automatically refactor.** Identify modules with unrelated responsibilities or coherent features scattered across the codebase. Report worthwhile restructuring separately, with the problem and suggested direction. Leave substantial boundary changes for a dedicated refactoring task.
- **Orphaned artifacts and obsolete transition machinery.** Remove unused code, fixtures, configuration, dependencies, documentation for removed features, and temporary compatibility paths only when there is evidence they are no longer needed. Check relevant callers, entry points, and compatibility requirements before removal.
- **Inconsistent conventions.** Align equivalent operations that use inconsistent names or representations without a meaningful reason. Preserve differences that reflect genuinely different requirements.

These are prompts for judgment, not a mandate to deduplicate or reorganize everything. Inspect broadly, but keep edits focused and justified. Preserve intended behaviour, meaningful test coverage, necessary safeguards, and unrelated user changes. Small, obvious consolidations are appropriate, but defer changes that require a new design decision to a separate refactoring task. If no worthwhile changes are warranted, leave the code unchanged.

Run relevant tests and checks after editing, including affected consumers when changing shared code. Add or adjust focused tests where needed. Report failures, checks not run, and anything you could not verify.

Leave edits in the working tree for inspection and a follow-up cleanup commit before merge. Do not stage, commit, amend, merge, or rewrite history.

Return:
- **Changes made:** Cleanups applied, with file paths and brief reasoning. Say explicitly if no changes were needed.
- **Verification:** Checks run and their results.
- **Remaining concerns:** Material uncertainties or worthwhile larger cleanups deferred, if any.
