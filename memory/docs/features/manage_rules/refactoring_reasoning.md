# Core Reasoning for the Refactoring Plan

This document explains the thinking process and the fundamental principles used to develop the refactoring plan for the `rulebook-ai` codebase.

## First Principles Guiding the Plan

The plan was not based on arbitrary preference but on established software engineering principles that promote maintainable, scalable, and robust code. These are:

1.  **Separation of Concerns (SoC):** Different parts of the system should handle distinct concerns. The *data* that defines an assistant's rule system (`assistants.py`) should be strictly separate from the *logic* that generates those rules (`core.py`).

2.  **Open/Closed Principle (OCP):** Software entities should be open for extension but closed for modification. We should be able to add support for a new AI assistant by adding data to `assistants.py`, without modifying the existing engine code in `core.py`.

3.  **Single Source of Truth (SSoT):** There should be one authoritative place to find the specification for all supported assistants. The `SUPPORTED_ASSISTANTS` list in `assistants.py` becomes this source.

4.  **Don't Repeat Yourself (DRY):** Avoid duplication of information. By having the CLI dynamically generate its arguments from the SSoT, we ensure that an assistant is defined in exactly one place.

## My Thinking Process

My process for developing the plan followed these steps:

### Step 1: Analyze the Current State

I started by reading `src/rulebook_ai/core.py` and `src/rulebook_ai/cli.py`. I observed that the logic was monolithic: assistant-specific details (like target paths) and the file operation logic were tightly coupled inside the `RuleManager` class. The CLI layer also contained hardcoded, duplicated argument definitions.

### Step 2: Identify Pain Points Using a Thought Experiment

To test the design's robustness, I asked a key question: **"What would I need to do to add a new assistant called 'FooCode'?"**

The answer revealed that this would require changing code in at least four different places across two files, a clear violation of core software principles.

### Step 3: Apply First Principles to Formulate a Data-Driven Solution

Based on the pain points, I applied the principles to design a much better, data-driven structure. The key insight was to stop thinking about assistants as a set of actions and instead define them by their fundamental, observable properties.

*   **First-Principles Decomposition:** I analyzed the documentation for all assistants to find the elemental attributes of their rule systems. I distilled these down to core concepts:
    *   **Identity:** `name`, `display_name`
    *   **Location & Cardinality:** `is_single_file`, `rule_path`, `filename`
    *   **File Schema:** `file_extension`, `supports_subdirectories`

*   **Achieve True Separation of Concerns:** By capturing these elemental attributes in a declarative `AssistantSpec` dataclass, I could separate the **data** from the **logic**. The new `assistants.py` file holds only this pure data. The `core.py` file becomes a generic engine that *interprets* this data.

*   **Adhere to the Open/Closed Principle:** To add a new assistant, a developer simply adds a new, correctly configured `AssistantSpec` object to the central list in `assistants.py`. **No other code changes are needed**. The system is extended without modification.

*   **Enforce DRY and SSoT:** The `SUPPORTED_ASSISTANTS` list in `assistants.py` becomes the Single Source of Truth. The CLI layer (`cli.py`) will now read this list and *dynamically generate* its command-line arguments. The `RuleManager` in `core.py` will read the same list to drive its logic. Information is defined once and reused everywhere.

### Step 4: Structure the Plan for Execution

Finally, I organized the solution into a phased plan (`refactoring_plan.md`). This makes the refactoring process incremental and easier to manage, starting with the creation of the new `assistants.py` and the refactoring of the `core.py` engine, before moving to the dependent CLI changes.