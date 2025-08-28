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

### Phase 1: Separate Specification from Logic (Completed)

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
    *   The logic for *how* to generate rules (e.g., "flatten and number files" vs. "preserve hierarchy") will reside entirely within private methods in `RuleManager`.
    *   **Refine public method orchestration:** The public methods will be refactored for clarity and compliance with the original design spec.
        *   `install()` will only handle copying files and will conclude by calling `self.sync()` to perform the rule generation.
        *   `sync()` will be the single entry point for all rule generation, always reading from the local `project_rules/` directory.
        *   `clean_rules()` and `clean_all()` will be made data-driven by iterating over `SUPPORTED_ASSISTANTS` and using the `clean_path` from the spec.

### Phase 2: Simplify and Automate `src/rulebook_ai/cli.py`

1.  **Implement Dynamic, Multi-Select CLI Arguments:**
    *   The `cli.py` module will import `SUPPORTED_ASSISTANTS` from `assistants.py`.
    *   The hardcoded, mutually exclusive CLI flags will be replaced. A loop will dynamically generate flags for each assistant (e.g., `--cursor`, `--cline`).
    *   These flags will use `action='append_const'` to allow users to select multiple assistants at once (e.g., `rulebook-ai install --cursor --copilot`).
    *   The `--all` flag will be a simple shortcut that populates the list with all assistants.
    *   The confusing `--no-copilot` flag will be removed entirely.

2.  **Decouple and Simplify Handlers:**
    *   The `handle_install` and `handle_sync` functions will be simplified to single lines.
    *   They will pass the `assistants` list, generated directly by `argparse`, to the corresponding `RuleManager` method.
    *   If no assistant flags are provided by the user, the list will be `None`, and the `RuleManager` will correctly interpret this as a request to install/sync for all assistants (the default behavior).
