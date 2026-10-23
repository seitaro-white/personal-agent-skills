---
name: review-changes
description: "Review and refactor code changes after implementation, or when asked to review a diff or commit, for simplicity, interpretability and maintainability."
metadata:
  author: seitaro-white
---

Review the specified changes and directly apply worthwhile corrections and simplifications and refactoring. If no target is specified, review uncommitted changes, including staged, unstaged, and relevant untracked files. Establish the review scope before editing.

Prioritize simplicity and understandability so the code is easy to modify. Maintainability should come from clear, straightforward code—not speculative abstractions or hypothetical extension points.

Review the implementation as a whole. Check whether the changes:
- Satisfy the user request and agreed constraints.
- Introduce bugs or break existing required behaviour.
- Include unnecessary features, speculative safeguards, dependencies, abstractions, or other avoidable complexity.
- Have appropriate verification for the behaviour being changed.

Look for these sources of unnecessary complexity or difficulty understanding the code:
- **Vague or misleading names.** Name variables for what they represent and functions for what they actually do. Prefer concrete, descriptive names over abbreviations or generic terms such as `data`, `manager`, or `process`. Longer names are welcome when they add useful meaning.
- **Functions that mix distinct responsibilities.** Break work into coherent, meaningfully named functions where this makes the implementation easier to follow. Avoid both sprawling functions and excessive fragmentation into trivial helpers.
- **Hidden dependencies and side effects.** Make important inputs, state changes, and interactions visible. Avoid surprising mutation, reliance on distant mutable state, or functions whose names conceal additional behaviour.
- **Unnecessary indirection.** Remove wrappers, pass-through functions, and abstractions that make readers jump between locations without providing a useful conceptual boundary.
- **Implicit meanings.** Replace unexplained constants, cryptic conditions, and ambiguous boolean arguments with names or structures that communicate their purpose.
- **Poor information locality.** Keep closely related logic together. Avoid making readers assemble a simple operation from scattered definitions or hold excessive context in memory.
- **Unhelpful documentation.** Use function-level docstrings or comments where they clarify purpose, contracts, assumptions, or non-obvious behaviour. Avoid comments that merely narrate the code; inline comments should primarily explain reasoning, constraints, or surprising choices.

These are prompts for judgment, not mechanical rules. Do not introduce helpers, documentation, or abstractions unless they make the implementation easier to understand and change.

Apply focused corrections and simplifications, preserving intended behaviour and unrelated user changes. Avoid unrelated refactoring and stylistic churn. If no worthwhile changes are warranted, leave the code unchanged. Flag material uncertainties rather than guessing.

Run relevant existing tests or checks after editing, and add or adjust focused tests where needed. Report failures and anything you could not verify; do not claim the implementation is verified when checks did not run or pass.

Leave edits in the working tree for the user to inspect. Do not stage, commit, amend, or rewrite history, even when reviewing a commit.

Return:
- **Changes made:** The corrections and simplifications applied, with file paths and brief reasoning. Say explicitly if no changes were needed.
- **Verification:** Checks run, their results, and any remaining concerns or decisions requiring user input.
