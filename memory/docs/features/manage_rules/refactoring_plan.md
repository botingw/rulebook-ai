# Refactoring Plan: `rulebook-ai` Core and CLI

**Objective:** This document outlines the plan for a purely internal refactoring of the `rulebook-ai` codebase. The goal is to improve maintainability and extensibility without changing any user-facing behavior of the CLI.

## High-Level Goal

The current implementation in `core.py` and `cli.py` is functional, but the logic for handling different AI assistants (Cursor, Cline, etc.) is tightly coupled within the `RuleManager` class. Adding a new assistant requires modifying multiple `if/elif` blocks and functions across both files. This makes the code harder to maintain and extend.

This refactoring introduces an "Assistant" abstraction using a more object-oriented approach. Each supported AI assistant will be represented by its own class, encapsulating its specific configuration (like its target directory name) and behavior (how to generate its rule files).

The `RuleManager` will be simplified to operate on a collection of these "Assistant" objects, delegating the specific work to them. This will make adding a new assistant as simple as creating a new `Assistant` class and registering it, adhering to the Open/Closed Principle.

---

## Detailed Refactoring Plan

### Phase 1: Abstract AI Assistants in `src/rulebook_ai/core.py`

1.  **Introduce an `Assistant` Abstraction:**
    *   Create a base class (or a `Protocol`) named `Assistant` that defines a common interface for all assistants.
    *   This interface will include:
        *   `name`: A string identifier (e.g., 'cursor').
        *   `install(source_dir, target_root)`: A method to handle the installation logic for that assistant.
        *   `sync(source_dir, target_root)`: A method to synchronize rules, which can default to cleaning and then installing.
        *   `clean(target_root)`: A method to remove all files and directories related to the assistant.

2.  **Implement Concrete `Assistant` Classes:**
    *   For each currently supported assistant, create a concrete class that implements the `Assistant` interface (e.g., `CursorAssistant`, `WindsurfAssistant`, `ClineAssistant`, `RooCodeAssistant`).
    *   Each class will contain the specific logic and configuration for its assistant. For example, `CursorAssistant` will know its target directory is `.cursor/rules` and that it needs to generate `.mdc` files.
    *   These classes will reuse the existing file operation helpers (like `copy_and_number_files`) from `RuleManager`.

3.  **Create a Central `AssistantRegistry`:**
    *   Implement a registry (e.g., a dictionary or a dedicated class) that holds an instance of each concrete `Assistant` class.
    *   This registry will serve as the single source of truth for all supported assistants, making them discoverable.

4.  **Refactor `RuleManager` to be an Orchestrator:**
    *   Remove the assistant-specific private methods (e.g., `_install_cursor_rules`, `_sync_roo_rules`).
    *   Modify the main `install`, `sync`, and `clean_rules` methods. Instead of containing large `if/elif` blocks, they will now iterate over a list of `Assistant` objects (retrieved from the registry based on user input) and call the appropriate method (`install`, `sync`, `clean`) on each one.

5.  **Treat GitHub Copilot as an Assistant:**
    *   Create a `CopilotAssistant` class that implements the `Assistant` interface. Its `install` logic will use the `concatenate_ordered_files` function.
    *   This removes the special-cased `include_copilot` boolean flag, making the logic more consistent and unified.

### Phase 2: Simplify and Decouple `src/rulebook_ai/cli.py`

1.  **Reduce Argument Parser Duplication:**
    *   Create a single helper function, `add_assistant_arguments(parser)`, which adds all the assistant-related command-line flags (e.g., `--cursor`, `--cline`, `--all-assistants`) to a given parser.
    *   Use this helper function for both the `install` and `sync` command parsers to keep them consistent and DRY (Don't Repeat Yourself).

2.  **Decouple CLI from Core Logic:**
    *   The logic for determining which assistants to act on will be simplified. The CLI will pass the list of selected assistant names (e.g., `['cursor', 'copilot']`) to the `RuleManager`.
    *   The `RuleManager` will then use the `AssistantRegistry` to get the corresponding `Assistant` objects.

3.  **Improve Separation of Concerns for the `doctor` Command:**
    *   Move the environment-checking logic currently inside the `handle_doctor` function into a new, dedicated `run_doctor_check()` method within the `RuleManager` class in `core.py`.
    *   The `handle_doctor` function in `cli.py` will become a simple wrapper that calls this new core method.