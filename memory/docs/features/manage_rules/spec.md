# Specification: Rulebook-AI CLI (Composable Packs)

**1. Overview**

The `rulebook-ai` command-line interface manages modular "Packs" that bundle AI rules, starter memory documents, and starter tools. Users can add and remove packs, compose their contents, and generate platform-specific rules for multiple assistants within a target project. The CLI maintains the user's project context in `memory/` and `tools/` while keeping internal state in a hidden `.rulebook-ai/` directory.

**2. Core Concepts**

1.  **Source Repository (Framework):** Hosts a top-level `packs/` directory. Each pack contains `rules/`, `memory_starters/`, `tool_starters/`, a required `manifest.yaml`, and a `README.md`.
2.  **Target Repo:** Any project repository where packs are added.
3.  **Target Internal State:** A hidden **`.rulebook-ai/`** directory created inside the Target Repo. It contains a copy of each active pack under `.rulebook-ai/packs/` and a machine-readable **`selection.json`** recording the active pack list and order.
4.  **Target Memory Bank Directory:** A folder named **`memory/`** created inside the Target Repo and populated from pack `memory_starters/`. This folder is persistent and should be version controlled.
5.  **Target Tools Directory:** A folder named **`tools/`** created inside the Target Repo and populated from pack `tool_starters/`. This folder is persistent and should be version controlled.
6.  **Target Platform Rules:** Generated assistant-specific rule files and directories created by the `sync` command. For a detailed specification on how rules are generated for different platforms, see [Platform Rules Spec](platform_rules_spec.md). These generated outputs should always be added to the Target Repo's `.gitignore` file.

**3. Features & Advantages**

*   **Composable Packs:** Multiple packs can be combined in a single project. Their order is tracked in `selection.json`, and earlier packs take precedence when files conflict.
*   **Explicit State:** The `.rulebook-ai/selection.json` file provides a clear, machine-readable record of active packs.
*   **Project-Specific Context:** The `memory/` and `tools/` directories hold the unified AI context and are under user control.
*   **Cleanliness:** Generated platform rules are kept out of version control, and internal state is isolated in `.rulebook-ai/`.
*   **Focused Cleaning:** `clean-rules` removes only rule-related artifacts, preserving project memory and tools. `clean` provides a complete removal option.

**4. Sync Logic**

The CLI maintains Target Platform Rules by composing active packs and writing their outputs to each assistant's rule directory. Running `rulebook-ai sync` performs this regeneration explicitly. Commands that modify the active pack list (`packs add` and `packs remove`) automatically invoke the same logic as an **implicit sync** so that Target Platform Rules stay current without an extra step.

**5. CLI Commands**

*   **`rulebook-ai packs list`**
    *   **Action:** Lists all available packs from the Source Repository's `packs/` directory.
    *   **Output:** Prints each pack's name, version, and description, along with a link to the Ratings & Reviews wiki.
    *   **Use Case:** Explore available Packs before selecting one to add to a project.

*   **`rulebook-ai packs add <name>`**
    *   **Action:** Adds a pack to the Target Repo and triggers an implicit sync (see **Sync Logic**).
        1.  Copies the pack into the Target Internal State at `.rulebook-ai/packs/<name>/`. If that directory already exists, it is cleared and overwritten to ensure a fresh copy.
        2.  Appends the pack's `name` and `version` to `.rulebook-ai/selection.json`.
        3.  Merges `memory_starters/` and `tool_starters` into the Target Memory Bank Directory (`memory/`) and Target Tools Directory (`tools/`) without overwriting existing files.
    *   **Output:** Prints progress messages and recommends which files to commit versus which to add to `.gitignore`.
    *   **Use Case:** Introduce a new Pack or refresh an existing one while keeping project-specific memory and tools intact.

*   **`rulebook-ai packs remove <name>`**
    *   **Action:** Removes a pack and triggers an implicit sync.
        1.  Deletes the pack's entry from `.rulebook-ai/selection.json`.
        2.  Removes the pack source from the Target Internal State at `.rulebook-ai/packs/<name>/`.
        3.  Removes any `memory/` and `tools/` files previously provided by the pack from the Target Memory Bank and Tools directories.
    *   **Output:** Prints progress messages.
    *   **Use Case:** Drop a Pack's rules and context when it is no longer needed.

*   **`rulebook-ai packs status`**
    *   **Action:** Displays the active packs, their versions, and their order as recorded in `selection.json`.
    *   **Use Case:** Verify which Packs are active and in what order when debugging rule composition.

*   **`rulebook-ai sync [--cursor] [--cline] [--roo] [--kilocode] [--warp] [--windsurf] [--copilot] [--claude-code] [--codex-cli] [--gemini-cli] [--all] [--strict] [--force] [--rebuild]`**
    *   **Action:** Explicitly regenerates Target Platform Rules from the active packs. If no assistant flags are provided, it regenerates rules for all assistants.
    *   **Behavior:**
        *   Deletes existing generated rule directories before regeneration.
        *   Composes the Target Memory Bank and Tools directories by copying files from each active pack in order. Earlier packs win conflicts; later packs are skipped with a warning unless `--force` is provided. `--strict` aborts on conflict. `--rebuild` purges `memory/` and `tools/` before copying.
    *   **Output:** Prints progress messages.
    *   **Use Case:** Run after manually editing `memory/` or `tools/`, or when pack contents change in the Source Repository and you want to refresh generated rules without changing the pack selection.

*   **`rulebook-ai clean`**
    *   **Action:** Removes the `.rulebook-ai/` directory, the Target Memory Bank (`memory/`), the Target Tools directory (`tools/`), and all generated platform rules.
    *   **Behavior:** Destructive operation that **must prompt for user confirmation**. Parent directories (e.g., `.github/`) are removed if they become empty.
    *   **Output:** Prints a prominent warning, a confirmation prompt, and a summary of what was removed.
    *   **Use Case:** Completely uninstall all Rulebook-AI components from a project.

*   **`rulebook-ai clean-rules`**
    *   **Action:** Deletes `.rulebook-ai/` and all generated platform rules while preserving the Target Memory Bank and Tools directories.
    *   **Behavior:** If a rule file is the only item within a directory, the parent directory is also removed.
    *   **Output:** Prints progress messages.
    *   **Use Case:** Revert to a clean state without generated rules while preserving project memory and tools.

*   **`rulebook-ai bug-report`**
    *   **Action:** Prints the GitHub issue tracker URL and attempts to open it in the user's default browser.

*   **`rulebook-ai rate-ruleset`**
    *   **Action:** Prints the ratings and reviews wiki URL and attempts to open it in the user's default browser.

