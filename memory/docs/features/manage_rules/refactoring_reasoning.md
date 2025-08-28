# Core Reasoning for the Refactoring Plan

This document explains the thinking process and the fundamental principles used to develop the refactoring plan for the `rulebook-ai` codebase.

## First Principles Guiding the Plan

The plan was not based on arbitrary preference but on established software engineering principles that promote maintainable, scalable, and robust code. These are:

1.  **Single Responsibility Principle (SRP):** A class or module should have only one primary reason to change. The goal is to have components that do one thing and do it well.

2.  **Open/Closed Principle (OCP):** Software entities (classes, modules, functions) should be open for extension but closed for modification. This means you should be able to add new functionality without changing existing, working code.

3.  **Don't Repeat Yourself (DRY):** Avoid duplication of code and logic. Duplication leads to maintenance nightmares, where a change in one place must be manually replicated in many others.

4.  **Separation of Concerns (SoC):** Different parts of the system should handle distinct concerns. For example, the user interface should be separate from the core business logic.

## My Thinking Process

My process for developing the plan followed these steps:

### Step 1: Analyze the Current State

I started by reading `src/rulebook_ai/core.py` and `src/rulebook_ai/cli.py` to build a mental model of the existing architecture. I observed:
*   `RuleManager` in `core.py` was a large class holding almost all the business logic.
*   It contained many specific methods like `_install_cursor_rules`, `_sync_windsurf_rules`, etc.
*   `cli.py` handled argument parsing but also contained some logic that wasn't strictly UI-related (e.g., the `doctor` command's implementation).

### Step 2: Identify Pain Points Using a Thought Experiment

To test the design's robustness, I asked a key question: **"What would I need to do to add a new assistant called 'FooCode'?"**

The answer revealed the design's weaknesses:
1.  Add a new constant for the target directory in `core.py`.
2.  Add a new `_install_foocode_rules` method to `RuleManager`.
3.  Add a new `_sync_foocode_rules` method to `RuleManager`.
4.  Modify the `_install_assistant_rules` dispatcher in `RuleManager`.
5.  Modify the `_sync_assistant_rules` dispatcher in `RuleManager`.
6.  Add a `--foocode` flag to both the `install` and `sync` commands in `cli.py`.
7.  Update the assistant list creation logic in `handle_install` and `handle_sync` in `cli.py`.

This process violates the **Open/Closed Principle** because adding a feature requires modifying existing code in many places. It also shows that `RuleManager` has too many responsibilities (**SRP** violation) and that the CLI and core are tightly coupled.

### Step 3: Apply First Principles to Formulate a Solution

Based on the pain points, I applied the principles to design a better structure:

*   To solve the **OCP** violation, I proposed the `Assistant` abstraction. Instead of `RuleManager` knowing about every assistant, it would operate on a generic `Assistant` interface. Now, adding a new assistant only requires creating a new class (extension), not modifying `RuleManager` (modification).

*   To address the **SRP** violation, this abstraction naturally breaks up the monolithic `RuleManager`. The `RuleManager`'s responsibility is simplified to *orchestrating* the process, while each `Assistant` class is responsible for its *own specific implementation*.

*   The **DRY** principle was applied to `cli.py`, where the `install` and `sync` commands had nearly identical argument parsing logic. A single helper function solves this.

*   **Separation of Concerns** motivated moving the `doctor` command's implementation out of the UI layer (`cli.py`) and into the core logic layer (`core.py`), making the CLI a thinner, more focused view controller.

### Step 4: Structure the Plan for Execution

Finally, I organized the solution into a phased plan (`task_plan.md`). This makes the refactoring process incremental and easier to manage, starting with the core abstractions first (Phase 1) before moving to the dependent CLI changes (Phase 2) and final verification (Phase 3).
