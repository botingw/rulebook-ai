# Specification: Rulebook-AI CLI

**1. Overview**

This document outlines the specification for the `rulebook-ai` command-line interface. This script provides commands for installing, synchronizing, and cleaning AI assistant rule sets, project memory banks, and supporting tools within target project repositories. It uses fixed directory names for simplicity: `project_rules/` (for rule sources), `memory/` (for project context), and `tools/` (for utilities) in the target repository.

**2. Core Concepts**

1.  **Source Repository (Framework):** The central repository containing master rule sets (from `rule_sets/`), master memory bank starter documents (from `memory_starters/`), and master tool starters (from `tool_starters/`).
2.  **Target Repo:** Any project repository where the framework is installed.
3.  **Target Project Rules Directory:** A folder named **`project_rules/`** *created inside* the Target Repo during installation. It holds project-specific rule files, copied from a chosen set in the Source Repository. **This folder is considered temporary and is removed by `clean-rules`.**
4.  **Target Memory Bank Directory:** A folder named **`memory/`** *created inside* the Target Repo during installation, holding project-specific memory documents. **This folder should be version controlled within the Target Repo.**
5.  **Target Tools Directory:** A folder named **`tools/`** *created inside* the Target Repo during installation, holding utility scripts or configurations. **This folder should be version controlled within the Target Repo.**
6.  **Target Platform Rules:** The generated, platform-specific rule directories/files (e.g., `.clinerules/`, `.cursor/rules/`, `WARP.md`, etc.) created *inside* the Target Repo by the `sync` command. **These folders/files should be added to the Target Repo's `.gitignore` file.**

**3. Features & Advantages**

*   **Project-Specific Customization:** Enables each target repository to maintain its own tailored project memory bank and utility tools.
*   **Simplified Maintenance:** Rule sets (`project_rules/`) are managed by the script and can be easily cleaned and re-installed.
*   **Clear Project Context:** The `memory/` and `tools/` folders serve as the persistent, version-controlled core for project-specific AI guidance.
*   **Cleanliness:** Keeps generated platform-specific rules out of the target repository's version control.
*   **Focused Cleaning:** `clean-rules` removes rule-related artifacts, leaving core project memory (`memory/`) and tools untouched. `clean-all` provides a complete removal option.

**4. CLI Commands**

*   **`install <target_repo_path> [--rule-set <name>] [--cursor] [--cline] [--roo] [--kilocode] [--warp] [--windsurf] [--copilot] [--claude-code] [--codex-cli] [--gemini-cli] [--all]`**
    *   **Action:** Installs and configures the framework components in a target repository.
        1.  Copies the specified rule set (default: `light-spec`) into `<target_repo_path>/project_rules/`.
        2.  Copies starter files from the framework's `memory_starters/` into `<target_repo_path>/memory/`.
        3.  Copies starter tools from the framework's `tool_starters/` into `<target_repo_path>/tools/`.
        4.  Copies `env.example` and `requirements.txt` to the target repository.
        5.  Immediately runs the `sync` logic for the selected assistants. If no assistant flags are provided, it defaults to ALL supported assistants.
    *   **Behavior:**
        *   The `project_rules/` directory is treated as ephemeral. If it already exists, it will be cleared and overwritten to ensure a fresh copy of the chosen rule set.
        *   The `memory/`, `tools/`, `env.example`, and `requirements.txt` are treated as persistent. The install operation is **non-destructive**; it will only add new starter files and will **not** overwrite any existing files in these locations.
    *   **Output:** Prints progress messages and recommends which files to commit versus which to add to `.gitignore`.

*   **`sync <target_repo_path> [--cursor] [--cline] [--roo] [--kilocode] [--warp] [--windsurf] [--copilot] [--claude-code] [--codex-cli] [--gemini-cli] [--all]`**
    *   **Action:** Reads rules from `<target_repo_path>/project_rules/` and regenerates the platform-specific rules for the selected assistants. If no assistants are specified, it syncs for ALL.
    *   **Use Case:** Run after manually modifying files within `<target_repo_path>/project_rules/` to apply the changes.
    *   **Output:** Prints progress messages.

*   **`clean-rules <target_repo_path>`**
    *   **Action:**
        1.  Removes all generated Target Platform Rules (e.g., `.clinerules/`, `.cursor/rules/`, etc.).
        2.  Removes the `project_rules/` directory.
    *   **Behavior:**
        *   The `memory/` and `tools/` directories are **NOT** removed.
        *   If a rule file is the only item within a directory (e.g., `.github/copilot-instructions.md`), the parent directory (`.github/`) will also be removed.
    *   **Use Case:** Revert to a clean state without rules, while preserving the project memory bank and tools.
    *   **Output:** Prints progress messages.

*   **`clean-all <target_repo_path>`**
    *   **Action:** Removes **all** framework components from the target repository, including generated rules, `project_rules/`, `memory/`, `tools/`, `env.example`, and `requirements.txt`.
    *   **Behavior:**
        *   This is a destructive operation. The command **MUST prompt for user confirmation** before proceeding.
        *   Like `clean-rules`, it will remove parent directories (e.g., `.github/`) if they become empty after the rule files within them are removed.
    *   **Use Case:** Completely uninstall all components of the framework from the target repository.
    *   **Output:** Prints a prominent warning, a confirmation prompt, and a summary of what was removed.

*   **`list-rules`**
    *   **Action:** Lists all available rule sets from the Source Repository's `rule_sets/` directory.
    *   **Output:** Prints a list of available rule sets and a link to the Ratings & Reviews wiki.

*   **`bug-report`**
    *   **Action:** Prints the GitHub issue tracker URL and attempts to open it in the user's default browser.

*   **`rate-ruleset`**
    *   **Action:** Prints the ratings and reviews wiki URL and attempts to open it in the user's default browser.
