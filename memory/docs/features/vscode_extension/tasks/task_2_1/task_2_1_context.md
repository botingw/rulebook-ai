# Context for Task 2.1: Identify Key `manage_rules.py` Functionality

This document outlines the core commands of the `manage_rules.py` script that the VS Code extension will interact with. Identifying these key functionalities is the first step in designing the extension's user interface and implementing the command handlers.

Based on the `manage_rules_script_design.md`, the core commands are:

*   **`install <target_repo_path> [--rule-set <name>]`**: Installs the AI rule management framework into a target repository. This includes copying a chosen rule set, memory bank starters, tool starters, `env.example`, and `requirements.txt`. It also performs an initial synchronization.
*   **`sync <target_repo_path>`**: Synchronizes the platform-specific rule files based on the source rules in the `project_rules/` directory within the target repository.
*   **`clean-rules <target_repo_path>`**: Removes generated platform-specific rule files and the `project_rules/` source directory from the target repository.
*   **`clean-all <target_repo_path>`**: Removes all AI rule management framework components (`project_rules/`, `memory/`, `tools/`, generated rules, `env.example`, `requirements.txt`) from the target repository after prompting for user confirmation.
*   **`list-rules`**: Lists the names of available rule sets in the source framework repository.

These five commands represent the primary interactions users will have with the AI Rule Management Framework through the VS Code extension's GUI and command palette. The extension will provide a user-friendly way to trigger these commands and view their output.