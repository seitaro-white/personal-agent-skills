---
name: grill-me
description: "A relentless interview to sharpen a plan, decision, or idea. Use when explicitly asked to be grilled or to stress-test thinking."
disable-model-invocation: true
license: MIT
metadata:
  author: Matt Pocock
  source: https://github.com/mattpocock/skills
  upstream-entry: skills/productivity/grill-me/SKILL.md
  upstream-instructions: skills/productivity/grilling/SKILL.md
  adaptation: "Combined the entry point and grilling instructions into a standalone Pi skill; factual exploration uses available tools or authorized delegation."
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), use available tools to find it; delegate exploration only when authorized. Don't ask the user for anything you could look up yourself. If exploration is running asynchronously, treat it as an unsettled prerequisite: only the questions downstream of it wait for the result; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
