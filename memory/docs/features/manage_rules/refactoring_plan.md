# Refactoring Plan: `rulebook-ai` Core and CLI

**Objective:** This document outlines the plan for a purely internal refactoring of the `rulebook-ai` codebase. The goal is to improve maintainability and extensibility without changing any user-facing behavior of the CLI.

## High-Level Goal

The current implementation in `core.py` is monolithic. The logic for handling different AI assistants is tightly coupled with the core file-management operations, making the system difficult to extend and maintain.

This refactoring will implement a clean **separation of concerns** by splitting the logic into two distinct parts:
1.  **A declarative configuration (`assistants.py`)**: This new file will define the *specification* for each assistant—what they expect to find on the filesystem—using a pure, data-only `AssistantSpec` class.
2.  **A generic engine (`core.py`)**: The `RuleManager` will be refactored into a generic engine that reads the assistant specifications and performs the necessary file operations. It will contain all the logic for how to generate rules.

This change will make adding a new assistant a simple matter of adding a new entry to the configuration file, without touching the core engine logic.

---

## Detailed Refactoring Plan

### Phase 1: Separate Specification from Logic

1.  **Create `src/rulebook_ai/assistants.py` (New File):**
    *   This file will contain the declarative specifications for all supported assistants and will have no logic.
    *   Define a new `AssistantSpec` `dataclass` based on a first-principles analysis of assistant rule systems. Key attributes will include:
        *   `name`, `display_name`
        *   `is_single_file` (boolean)
        *   `rule_path` (the directory where rules are stored)
        *   `filename` (for single-file assistants)
        *   `file_extension` (for multi-file assistants)
        *   `supports_subdirectories` (boolean)
    *   Create the `SUPPORTED_ASSISTANTS` list in this file, populated with an `AssistantSpec` instance for each AI tool.

2.  **Refactor `src/rulebook_ai/core.py` into a Generic Engine:**
    *   Remove all assistant-specific constants and logic from `core.py`.
    *   Import the `SUPPORTED_ASSISTANTS` configuration from the new `assistants.py`.
    *   Refactor `RuleManager` to be a generic interpreter of the `AssistantSpec`.
    *   The logic for *how* to generate rules (e.g., "flatten and number files" vs. "preserve hierarchy") will now reside entirely within private methods in `RuleManager`. The manager will decide which strategy to use based on the pure attributes from an `AssistantSpec` (e.g., if `supports_subdirectories` is `False`, it must flatten).

### Phase 2: Simplify and Automate `src/rulebook_ai/cli.py`

1.  **Automate CLI Argument Generation:**
    *   The `cli.py` module will import `SUPPORTED_ASSISTANTS` from `assistants.py`.
    *   A helper function will be created that iterates through this list and **dynamically generates** the CLI flags (e.g., `--cursor`, `--cline`, `--copilot`) and their help text for the `install` and `sync` commands.

2.  **Decouple Handlers from Implementation:**
    *   The command-handling functions (`handle_install`, `handle_sync`) will be simplified. They will determine which assistants were selected by the user and pass a simple list of their string names (e.g., `['cursor', 'copilot']`) to the `RuleManager`.
    *   The special-cased `include_copilot` boolean flag will be removed entirely, as Copilot will be handled uniformly with all other assistants via its own `--copilot` flag.
