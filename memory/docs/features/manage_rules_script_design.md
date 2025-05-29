**1. Overview**

This document outlines the design for a new Python script, `src/manage_rules.py`. This script provides a command-line interface for installing, synchronizing, and cleaning AI assistant rule sets, project memory banks, and supporting tools within target project repositories. It uses fixed directory names for simplicity: `project_rules/` (for rule sources), `memory/` (for project context), and `tools/` (for utilities) in the target repository.

**2. Core Concepts**

1.  **Source Repository (Framework):** The central repository containing master rule sets (from `rule_sets/`), master memory bank starter documents (from `memory_starters/`), master tool starters (from `tool_starters/`), and the `manage_rules.py` script itself.
2.  **Target Repo:** Any project repository where the framework is installed.
3.  **Target Project Rules Directory:** A folder named **`project_rules/`** *created inside* the Target Repo during installation. It holds project-specific rule files, copied from a chosen set in the Source Repository. **This folder is considered temporary by `clean-rules` but can be version-controlled if desired for manual restoration between `clean-rules` and `install` operations.**
4.  **Target Memory Bank Directory:** A folder named **`memory/`** *created inside* the Target Repo during installation, holding project-specific memory documents, populated from the Source Repository's `memory_starters/`. **This folder should be version controlled within the Target Repo.**
5.  **Target Tools Directory:** A folder named **`tools/`** *created inside* the Target Repo during installation, holding utility scripts or configurations, populated from the Source Repository's `tool_starters/`. **This folder should be version controlled within the Target Repo.**
6.  **Target Platform Rules:** The generated, platform-specific rule directories/files (e.g., `.clinerules/`, `.cursor/rules/`, `.roo/`, `.windsurf/rules/`, `.github/copilot-instructions.md`) created *inside* the Target Repo by the `sync` command using `project_rules/` as input. **These folders/files should be added to the Target Repo's `.gitignore` file.**

**3. Features & Advantages**

*   **Project-Specific Customization:** Enables each target repository to maintain its own tailored project memory bank and utility tools based on common starting templates. Rule sets can be easily swapped or refreshed.
*   **Simplified Maintenance:** Developers manage and customize memory documents and tools directly within their project's context (`memory/`, `tools/`). Rule sets (`project_rules/`) are managed by the script and can be easily cleaned and re-installed.
*   **Clear Project Context:** The `memory/` and `tools/` folders serve as the persistent, version-controlled core for project-specific AI guidance.
*   **Reusability:** The Source Repository acts as a factory for bootstrapping framework components.
*   **Cleanliness:** Keeps generated platform-specific rules (`.clinerules/`, etc.) out of the target repository's version control.
*   **Simplified Workflow:** Provides clear `install`, `sync`, `clean-rules`, and `clean-all` commands.
*   **Focused Cleaning:** `clean-rules` removes rule-related artifacts (generated rules and `project_rules/`), leaving core project memory (`memory/`) and tools untouched. `clean-all` provides a complete removal option.

**4. Specification: `manage_rules.py` Commands**

*   **`install <target_repo_path> [--rule-set <name>]`**
    *   **Action:**
        1.  Copies the specified rule set (default: `light-spec`) from the Source Repository's `rule_sets/<rule-set-name>` directory into `<target_repo_path>/project_rules/`. If `project_rules/` already exists, it will be overwritten or cleared first to ensure a fresh copy of the chosen rule set. *(A warning should be issued if overwriting)*.
        2.  Copies the content of the Source Repository's `memory_starters/` directory into `<target_repo_path>/memory/`. If `memory/` exists, new starter files from the source will be copied if they don't exist in the target; existing files in the target `memory/` will **not** be overwritten.
        3.  Copies the content of the Source Repository's `tool_starters/` directory into `<target_repo_path>/tools/`. If `tools/` exists, new starter files/subdirectories from the source will be copied if they don't exist in the target; existing files/subdirectories in the target `tools/` will **not** be overwritten.
        4.  Copies `env.example` and `requirements.txt` from the Source Repository's root to `<target_repo_path>/env.example` and `<target_repo_path>/requirements.txt`. If `env.example` / `requirements.txt` already exists in the target, it will **not** be overwritten.
        5.  Immediately runs the `sync` logic (using `<target_repo_path>/project_rules/` as the source).
    *   **Output:** Prints progress messages. Suggests adding generated platform rule directories/files (including `.github/copilot-instructions.md`) to `.gitignore`. Recommends committing `memory/`, `tools/`, `env.example`, and `requirements.txt` to version control. Informs the user that `project_rules/` will be managed by the script (and removed by `clean-rules`).

*   **`sync <target_repo_path>`**
    *   **Action:** Reads rules from `<target_repo_path>/project_rules/`. Deletes any existing Target Platform Rules directories/files (including `.github/copilot-instructions.md`). Regenerates the Target Platform Rules for all supported platforms.
    *   **Use Case:** Run after manually modifying files within `<target_repo_path>/project_rules/` (if advanced customization is done there, knowing `clean-rules` will remove them) or after `install` to ensure rules are up-to-date.
    *   **Output:** Prints progress messages.

*   **`clean-rules <target_repo_path>`**
    *   **Action:**
        1.  Removes the generated Target Platform Rules directories/files (e.g., `.clinerules/`, `.cursor/rules/`, `.roo/`, `.windsurf/rules/`, `.github/copilot-instructions.md`) from `<target_repo_path>`. If `.github/copilot-instructions.md` is the only file in `.github/`, the `.github/` directory may also be removed.
        2.  Removes the **`project_rules/`** directory itself from `<target_repo_path>`.
        3.  The `memory/` and `tools/` directories are **NOT** removed.
    *   **Use Case:** Remove all rule-related files (both generated and their sources) to allow for a fresh `install` of a different rule set or to revert to a clean state without rules, while preserving the project memory bank and tools.
    *   **Output:** Prints progress messages, clearly indicating which rule-related items were removed.

*   **`clean-all <target_repo_path>`**
    *   **Action:** Removes all framework components from `<target_repo_path>`:
        1.  The generated Target Platform Rules directories/files (including the `.github/` directory if it was created/managed by this script for `copilot-instructions.md`).
        2.  The `project_rules/` directory.
        3.  The `memory/` directory.
        4.  The `tools/` directory. The `env.example` and `requirements.txt` file (environment for tools).
    *   **Important:** This command **MUST prompt for user confirmation** before proceeding, clearly stating that `memory/`, `tools/`, `env.example`, and `requirements.txt` (which may contain user customizations) will be deleted.
    *   **Use Case:** Completely uninstall all components of the framework from the target repository.
    *   **Output:** Prints progress messages. Includes a prominent warning and confirmation prompt before deletion, and a summary of what was removed.

*   **`list-rules`**
    *   **Action:** Scans the Source Repository's `rule_sets/` directory. It lists all subdirectories found within `rule_sets/`, as each subdirectory represents an available rule set.
    *   **Use Case:** Allows users to quickly see which rule sets are available for installation without needing to manually inspect the `rule_sets/` directory in the source framework.
    *   **Output:** Prints a header like "Available rule sets:" followed by the name of each discovered rule set, one per line. If no rule sets are found, it prints an appropriate message.

**5. Implementation Notes**

*   Use Python's `argparse` library.
*   Adapt file processing logic from `copy_rules.py`.
*   Implement robust path handling and error checking.
*   Provide clear user feedback.
*   `install`: Ensure non-destructive copying for `memory/`, `tools/`, `env.example`, and `requirements.txt`. Ensure `project_rules/` is freshly populated from the chosen rule set (e.g., clear and copy, or overwrite with warning).
*   `clean-all`: **Must** include a user confirmation step.
*   Directory names for framework components (e.g., `rule_sets` in source, `project_rules`, `memory`, `tools` in target, `memory_starters`, `tool_starters` in source) will be hardcoded as constants within the script.
*   The `concatenate_ordered_files` helper function should ensure parent directories for the destination file are created (e.g., `.github/` for `copilot-instructions.md`).
*   Cleanup logic for `clean-rules` and `clean-all` should attempt to remove the `.github/` directory if `copilot-instructions.md` was the only file managed by this script within it and the directory becomes empty.

**6. Initial Documentation Approach (Task 6.a)**

1.  Document usage of `manage_rules.py` (commands, the `--rule-set` option for `install`).
2.  Explain the fixed directory structure:
    *   **Source Repository:** `rule_sets/` (contains selectable rule configurations), `memory_starters/` (initial content for memory bank), `tool_starters/` (initial content for tools).
    *   **Target Repository:** `project_rules/` (active rule sources, managed by the script), `memory/` (persistent project context), and `tools/` (persistent utilities).
3.  State that customization of project context is done by editing files in `memory/` and `tools/` in the target repository.
4.  Explain that `project_rules/` is populated by `install` (from a chosen rule set) and removed by `clean-rules`. Advanced users *could* modify it before running `sync` but should be aware it's not preserved by `clean-rules`.
5.  Document behaviors of `clean-rules` (removes generated rules and `project_rules/`) and `clean-all` (removes everything, with confirmation).
6.  Explain how `install` handles pre-existing `memory/` and `tools/` directories (non-overwriting, only adds new starter files).
7.  Document support for GitHub Copilot via `.github/copilot-instructions.md` generation.
8.  Defer detailed guides on writing custom rules (beyond choosing a rule set via `install`) for later.
9.  **Note:** This script now assumes compatibility with Windsurf versions that use the `.windsurf/rules/` structure for loading workspace rules. Users on older versions may need to update Windsurf.
