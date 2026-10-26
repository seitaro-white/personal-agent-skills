---
name: write-code
description: "Guidelines for writing clean and simple code as the user prefers. Use when writing code of any kind, planning software features, implementating tests, refactoring, or generally doing anything that touches the practice of software engineering."
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
The following principles have been around for a while, but have stood the test of time because they work! They are listed here not only to remind you of them, but as an _expression of the user's preference for how software should be written_ - these are especially imporant and should be prioritised

## Core system principles

### SoC (Separation of Concerns)
Software should be divided into distinct, non-overlapping sections, where each section addresses a separate "concern". Each module, class or function should do one thing and do it well, and components should be loosely coupled. 

Crucial for maintainability and understandability - when editing code, you do not want to be making changes to half the modules and files in the system every time because everything is coupled together 

**This is the most imporant** thing to prioritise.

### KISS (Keep it Simple, Stupid)
Keep things simple, straightfoward logic and standard patterns. Complexity makes it hard to understand the code and introduces more points of potential failure.

### YAGNI (You Aren’t Gonna Need It)
Implement only what is immediately necessary for any given feature. Do not guess what might be required in future, or add functionality, features or abstractions that don't match current requirements. 

This is crucial for reducing technical debt, and remember we can always modify add features later if we need - but after we've checked the minimal implementation works.

### Boy Scout Rule (Alway leave the codebase cleaner than you found it)
Clean up code as you go, e.g. renaming vague variables, deleting dead code comments, everytime you touch a file. **Tolerating messy code invites more messy code**

### SOLID 
The solid coding principles for object oriented programming are all good, however place *particular* importance on:
- SRP (Single Responsibility Principles) - keep mode highly modular, ideal for safe re-writing and modification later on. 
- ISP (Interface Segregation Principle) - keep interfaces small, specific and focused. 


## Code style guidelines 

- Use meaningful names - variables with nouns and functions with action verbs that are immediately legiable - prefer longer descriptive names over short/abstract ones even if they look a bit clunky.
- Keep functions small - limits functions to a single level of abstractions, and genreally 20-30 lines of code, otherwise break out into more functions.
- Keep files small - files should generally not go over 200-300 lines except in special cases - should be broken up if so.
- Keep nesting to a minimal - again break into functions rather than deep nesting, use early returns to flatten.

## How to apply
When writing code, plans, documentation, tests and so on, everytime you add or modify code, you should review what you have done against these principles and guidelines, and make changes and improvements if anything is lacking.
