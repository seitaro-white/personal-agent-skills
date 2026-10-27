---
name: write-code
description: "Guidelines for writing clean and simple code as the user prefers. Use when writing code of any kind, planning software features, implementing tests, refactoring, or generally doing anything that touches the practice of software engineering."
metadata:
  author: seitaro-white
---

The following are some guidelines and principles for writing code in this project. They will help you write clean & simple code - easy to read, understand and maintain, and adhere to the user's preferences for how they like to build software. 

# Why? 
As an AI agent, you already know how to write good code and solve problems - you've certainly been trained on enough of it! However, you can have a tendancy to:
- Over-engineer and hedge around features;
- Be overly-verbose and fail to prioritise what information is actually important; and
- Write code that solves the immediate problem/request, but with poor structure and legibility - this leads overtime to issues with maintainability and understandability for both the human user and AI.

The user wants you to prioritise writing code that is clean, simple and understandable, for the following reasons:
- **The bottleneck is the user's understanding/cognitive load** - The user is involved in engineering process, treating you as a companion. They will review your code at the diff level, and try to maintain a broad understand of what is happening in the codebase as it develops and features are added. The cleaner/simpler the code is, the easier this will be. Simimilarly, documentation that is concise and only surfaces what is truely important will reduce cognitive load.
- **Gall’s Law, i.e. complex systems that work evolve from simple systems that work, while complex systems built from scratch fail** - with AI, software is mallable and easier to fix and extend. This means we should prioritise building miminal, light-weight implementations of core logic and features that work. We can add/extend the code later rather than trying to design for everything at the outset. 
- **Clean and maintainable code helps YOU as well as the user** - AI generated codebases can, without care, tend towards slop and unmaintability over time. Hard-to-understand code-spagetthi makes it harder for AI agents to understand and implement changes just as much as for humans. 

# Principles
The following principles have been around for a while, but have stood the test of time because they work! They are listed here not only to remind you of them, but as an _expression of the user's preference for how software should be written_.

Where principles conflict, you should prefer the design that makes the current behaviour easiest to understand and safely change. Simplicity must preserve correctness, so implement current requirements completely, including necessary validation, error handling, security and tests.

## Core system principles

### SoC (Separation of Concerns)
Software should be divided into distinct, non-overlapping sections, where each section addresses a separate "concern". Each module, class or function should do one thing and do it well, and components should be loosely coupled. 

Crucial for maintainability and understandability - when editing code, you do not want to be making changes to half the modules and files in the system every time because everything is coupled together 

**This is a central priority**. Separation should reduce cognitive load, not just increase the number of modules. Keep closely related logic together, and introduce boundaries where responsibilities genuinely differ.

### KISS (Keep it Simple, Stupid)
Keep things simple, straightfoward logic and standard patterns. Complexity makes it hard to understand the code and introduces more points of potential failure.

Simple means less complexity to understand and maintain, not fewer dependencies. Prefer established, industry-standard tools and libraries where they reduce bespoke code, especially those already used in the project. Do not reimplement standard capabilities, or introduce dependencies without a meaningful benefit.

### YAGNI (You Aren’t Gonna Need It)
Implement only what is immediately necessary for any given feature. Do not guess what might be required in future, or add functionality, features or abstractions that don't match current requirements. 

This is crucial for reducing technical debt, and remember we can always modify add features later if we need - but after we've checked the minimal implementation works.

### Boy Scout Rule (Always leave the codebase cleaner than you found it)
Make small, relevant improvements in the code you change, e.g. clarifying a vague variable name or deleting a stale comment. Keep the diff focused on the task; propose broader or unrelated cleanup separately. **Tolerating messy code invites more messy code**.

### SOLID 
Use SOLID principles where they simplify the actual design, not as a checklist requiring new interfaces, classes or dependency-injection layers. Place *particular* importance on:
- SRP (Single Responsibility Principle) - give components a clear responsibility so they can be understood and changed safely.
- ISP (Interface Segregation Principle) - keep interfaces small, specific and focused on what their consumers need.


## Code style guidelines 

- Use meaningful names - variables with nouns and functions with action verbs that are immediately legiable - prefer longer descriptive names over short/abstract ones even if they look a bit clunky.
- Keep functions focused - aim for a consistent level of abstraction. Around 20-30 lines is a useful prompt to review a function and check if it's getting overly long, although it is not a hard limit. Extract helpers when they clarify intent or isolate a distinct responsibility.
- Keep files cohesive - around 200-300 lines is a useful prompt to review their structure and see if breaking them out into multiple smaller files might improve SoC.
- Keep nesting to a minimal - again break into functions rather than deep nesting, use early returns to flatten.
- In Python, give public modules, classes, functions and methods a short Google-style docstring so IDE hovers explain their purpose. Add `Args:`, `Returns:` or `Raises:` sections only where they say something the name and signature do not; document contracts and important edge cases rather than narrating the implementation, and do not repeat types already expressed in annotations. Private helpers, dunder methods and tests usually need none - their names should explain them.

## Python examples

These examples illustrate complementary styles, not templates to copy mechanically. Read the one relevant to the task; neither its dependencies nor its class structure are requirements for every project.

- [Practical Python](examples/timesheet_report.py): a small reporting script that uses pandas for tabular work and Click for CLI behaviour, keeping our own code focused on the input contract and report.
- [Domain modelling](examples/order_fulfilment.py): a cohesive class that owns stock and reservation rules, with explicit state transitions and no speculative framework. This example needs no external runtime library because the business rules are specific to the application.
- [Tests and usage](examples/README.md): behavioural tests for both examples, plus run, lint and type-check commands.

## How to apply
Before presenting a coherent change to code, plans, documentation or tests, review it against these principles and guidelines. Check that it meets the current requirements and that any abstractions or extra files earn their complexity. Make relevant improvements before handing it back.
