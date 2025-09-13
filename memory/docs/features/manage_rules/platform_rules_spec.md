# Specification: Target Platform Rules

This document provides a detailed specification for how the `rulebook-ai` CLI generates platform-specific rule files for various AI assistants.

## Generation Logic

Target Platform Rules are the final, assistant-specific rule files generated in a user's project by the `sync` command. Their structure and content are derived from the `rules/` directories of all active packs, composed according to the order defined in the project's `.rulebook-ai/selection.json` file. These source directories must follow the [Pack Structure Spec](pack_structure_spec.md), which enforces numeric prefixes for deterministic ordering.

The generation logic is determined by a declarative specification for each assistant, which defines two main output formats:

### 1. Multi-File Assistants

This format is for assistants that read from a directory of individual rule files (e.g., Cursor, Cline).

*   **Action:** The CLI copies the rule files from each active pack into a single target directory (e.g., `.cursor/rules/`).
*   **Modes:** Some multi-file assistants support "modes," represented by `NN-rules-{mode}` subdirectories in the pack's `rules/` folder as defined in the [Pack Structure Spec](pack_structure_spec.md) (e.g., `02-rules-code`, `03-rules-debug`). During sync the numeric prefix is removed and the mode name becomes the subdirectory in the target directory (e.g., `.kilocode/code/`, `.kilocode/debug/`).
*   **File Extensions:** The assistant's specification may enforce a specific file extension (e.g., `.mdc` for Cursor).

### 2. Single-File Assistants

This format is for assistants that read a single, consolidated rule file (e.g., Warp, GitHub Copilot, Claude).

*   **Action:** The CLI concatenates the content of all rule files from all active packs into a single output file (e.g., `WARP.md`).
*   **Order:** The order of concatenation follows the pack order in `selection.json` and the alphabetical order of files within each pack's `rules/` directory and its subdirectories. The `NN-` prefixes mandated by the [Pack Structure Spec](pack_structure_spec.md) ensure this alphabetical ordering is deterministic.

## Important Considerations

*   **Gitignore:** All generated rule files and directories are considered artifacts that can be regenerated at any time. They should always be added to the Target Repo's `.gitignore` file.
*   **Conflict Resolution:** When multiple active packs provide a rule file at the same path, the file from the pack that appears earliest in the `selection.json` list is used. The versions from later packs are ignored, and a warning is issued to the user.
