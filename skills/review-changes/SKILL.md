---
name: review-changes
description: "Review and refactor code changes after implementation, or when asked to review a diff or commit, for simplicity, interpretability and maintainability."
metadata:
  author: seitaro-white
---

Review the specified changes and directly apply worthwhile corrections and simplifications and refactoring. If no target is specified, review uncommitted changes, including staged, unstaged, and relevant untracked files. Establish the review scope before editing.

Your primary goal is to ensure that the changes, as far as possible, following the principles of *simplicity* and *understandability*, and *maintainability*. Simplicity and understandability substantially overlap (simple code is easy to understand and vice-versa) while maintainability is an outcome of the first two, i.e. code that is simple and easy to understand is easier to modify (rather than lots of speculative abstractions/designing for hypothetical extensions).


Review the implementation as a whole. Check whether the changes:
- Satisfy the user request and agreed constraints.
- Introduce bugs or break existing required behaviour.
- Include unnecessary features, speculative safeguards, or abstractions.
- Add dependencies or complexity that a simpler approach could avoid.
- Have appropriate verification for the behaviour being changed.


Within that implementation, look for these sources of unnecessary complexity or difficulity understanding the code and look for opportunities to improve:
- **Vague or misleading names.** Name variables for what they represent and functions for what they actually do. Prefer concrete, descriptive names over abbreviations or generic terms such as `data`, `manager`, or `process`. Longer names are welcome when they add useful meaning.
- **Functions that mix distinct responsibilities.** Break work into coherent, meaningfully named functions where this makes the implementation easier to follow. Avoid both sprawling functions and excessive fragmentation into trivial helpers.
- **Hidden dependencies and side effects.** Make important inputs, state changes, and interactions visible. Avoid surprising mutation, reliance on distant mutable state, or functions whose names conceal additional behaviour.
- **Unnecessary indirection.** Remove wrappers, pass-through functions, and abstractions that make readers jump between locations without providing a useful conceptual boundary.
- **Implicit meanings.** Replace unexplained constants, cryptic conditions, and ambiguous boolean arguments with names or structures that communicate their purpose.
- **Poor information locality.** Keep closely related logic together. Avoid making readers assemble a simple operation from scattered definitions or hold excessive context in memory.
- **Unhelpful documentation.** Use function-level docstrings or comments where they clarify purpose, contracts, assumptions, or non-obvious behaviour. Avoid comments that merely narrate the code; inline comments should primarily explain reasoning, constraints, or surprising choices.

These are prompts for judgment, not mechanical rules. Do not introduce helpers, documentation, or abstractions unless they make the implementation easier to understand
and change.

Apply concrete fixes and useful simplifications, preserving intended behaviour. Keep edits focused on the reviewed implementation; avoid unrelated refactoring, stylistic churn, and overwriting unrelated user changes. Do not invent changes to justify the review. If the implementation is already appropriately simple and correct, leave it unchanged. Flag material uncertainties rather than guessing at intended behaviour.

Run relevant existing tests or checks after editing, and add or adjust focused tests where needed. Report failures and anything you could not verify; do not claim the implementation is verified when checks did not run or pass.

Leave edits in the working tree for the user to inspect. Do not stage, commit, amend, or rewrite history, even when reviewing a commit.

Return:
- **Assessment:** A brief summary of the implementation after review.
- **Changes made:** The corrections and simplifications applied, with file paths and brief reasoning. Say explicitly if no changes were needed.
- **Verification:** Checks run, their results, and any remaining concerns or decisions requiring user input.
