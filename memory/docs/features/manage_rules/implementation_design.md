# Implementation Design: Rulebook-AI CLI

## 1. High-Level Goal & Architecture

The `rulebook-ai` CLI is designed to be maintainable and extensible. The core implementation follows a clean **separation of concerns**, splitting the logic into two distinct parts:

1.  **A declarative configuration (`assistants.py`)**: This file defines the *specification* for each AI assistant—what they expect to find on the filesystem—using a pure, data-only `AssistantSpec` class. It is the single source of truth for all assistant-specific information.
2.  **A generic engine (`core.py`)**: The `RuleManager` class acts as a generic engine that reads the assistant specifications and performs the necessary file operations (copying, cleaning, generating rules). It contains all the logic for *how* to generate rules based on the specifications.

This architecture makes adding a new assistant a simple matter of adding a new entry to the configuration file, without touching the core engine logic.

## 2. Code Structure

-   **`src/rulebook_ai/cli.py`**: Handles command-line argument parsing using Python's `argparse` library. It dynamically generates CLI flags (e.g., `--cursor`, `--cline`) from the `SUPPORTED_ASSISTANTS` list in `assistants.py`. It then calls the appropriate methods in the `RuleManager`.
-   **`src/rulebook_ai/core.py`**: Contains the `RuleManager` class, which implements the main business logic for the `install`, `sync`, `clean-rules`, and `clean-all` commands.
-   **`src/rulebook_ai/assistants.py`**: Contains the `AssistantSpec` dataclass and the `SUPPORTED_ASSISTANTS` list, which provides the specifications for all supported AI assistants.

## 3. Core Implementation Notes

-   **Path Handling:** The implementation must use robust path handling to manage files and directories across different operating systems.
-   **User Feedback:** The CLI should provide clear and concise feedback to the user for all operations.
-   **Hardcoded Constants:** Directory names for the framework components (e.g., `rule_sets` in the source repo, `project_rules`, `memory`, `tools` in the target repo) are hardcoded as constants within the script for simplicity and reliability.
-   **Parent Directory Creation:** Helper functions that write files (e.g., for `copilot-instructions.md` or `GEMINI.md`) must ensure that the parent directories (`.github/`, `.gemini/`) are created if they do not exist.
-   **Extensibility for Assistants:** The `AssistantSpec` is designed to be extensible. For example, the `has_modes` flag was added to support assistants like Kilo Code and Roo Code, which use subdirectories for different modes. The `RuleManager`'s generation logic was extended to interpret this flag.
