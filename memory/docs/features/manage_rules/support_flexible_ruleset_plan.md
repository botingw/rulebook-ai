# Implementation Plan: Composable AI Packs

This document provides the canonical implementation plan for refactoring `rulebook-ai` to a composable "Pack" model. It combines the high-level architectural vision with a detailed, phased roadmap for developers.

Commands not covered here—such as `bug-report` or `rate-ruleset`—retain their legacy behavior documented in [`spec.md`](spec.md).

## 1. First Principles

*   **AI Context is King:** The primary goal is to create a unified, rich, and accessible context for the AI assistant in the target project's `memory/` and `tools/` directories.
*   **Explicitness over Implicitness:** The state of the project (which packs are active and in what order) must be explicitly recorded in a machine-readable file.
*   **User-Centricity:** The developer's workflow should be simple. The CLI should be intuitive, conventional, and provide clear status information.
*   **Separation of Concerns:** The framework's internal state (`.rulebook-ai/`) must be separate from the user's project files (`memory/`, `tools/`).

## 2. Conceptual Changes

*   **"Rule Set" is deprecated.** The new, holistic unit is a **"Pack"**.
*   **`project_rules/` is obsolete.** The `sync` command will no longer read from this directory. All rule composition will be based on the active packs.

## 3. Phase 1: Source Repository Restructuring

The first step is to migrate the existing source repository structure to the new Pack-based model.

**Action:** Create a new top-level `packs/` directory. Migrate the existing `rule_sets/`, `src/rulebook_ai/memory_starters/`, and `src/rulebook_ai/tool_starters/` into this new structure.

**New Structure:**

```
packs/
├── light-spec/
│   ├── rules/              # (from rule_sets/light-spec/)
│   ├── memory_starters/    # (from src/rulebook_ai/memory_starters/)
│   ├── tool_starters/      # (from src/rulebook_ai/tool_starters/)
│   ├── manifest.yaml       # <== NEW
│   └── README.md           # <== NEW
│
└── heavy-spec/
    └── ... (etc.)
```

**`manifest.yaml` Specification:**

Each pack directory **must** contain a `manifest.yaml`:

```yaml
# packs/light-spec/manifest.yaml
name: "Light Spec"
version: "1.0.0"
summary: "A lightweight, general-purpose pack for coding assistance with basic project context."
```

## 4. Phase 2: Target Project Structure

**Action:** The CLI will manage a hidden `.rulebook-ai/` directory in the target project.

**Target Structure:**

```
your-target-project/
│
├── .rulebook-ai/               # Hidden directory for internal state
│   ├── packs/                  # Contains a full copy of each active pack's source
│   │   └── light-spec/
│   └── selection.json          # Source of truth for active packs (order matters)
│
├── memory/                     # User-owned, unified AI context
├── tools/                      # User-owned, unified tools
│
└── .cursor/                    # Generated platform rules (gitignored)
```

**`selection.json` Specification:** Each entry records the pack's name and version.

```json
{
  "packs": [
    { "name": "light-spec", "version": "1.0.0" },
    { "name": "python-data-scientist", "version": "2.3.0" }
  ]
}
```

## 5. Phase 3: CLI Command Evolution

**Action:** Refactor `src/rulebook_ai/cli.py` to implement the new, more intuitive command structure. The old commands will be replaced as follows:

| Old Command | New Command(s) | Purpose |
| :--- | :--- | :--- |
| `list-rules` | `rulebook-ai packs list` | Lists all available packs from the source repository. |
| `install` | `rulebook-ai packs add <name>` | Adds a pack to the target project and triggers an implicit `sync`. |
| (n/a) | `rulebook-ai packs remove <name>` | Removes a pack and triggers an implicit `sync`. |
| (n/a) | `rulebook-ai packs status` | Shows the active packs, their versions, and their order. |
| `sync` | `rulebook-ai sync` | Regenerates all rules and starters from active packs. Supports `--strict` to fail on file conflicts *(optional, low priority)*, `--force` to overwrite on conflict *(optional, low priority)*, and `--rebuild` to purge `memory/` and `tools/` before copying *(optional, low priority)*. |
| `clean-all` | `rulebook-ai clean` | Removes the `.rulebook-ai` dir, `memory/`, `tools/`, and generated rules (destructive). |
| `clean-rules` | `rulebook-ai clean-rules` | Deletes `.rulebook-ai` and generated rules but preserves `memory/` and `tools`. |

## 6. Phase 4: Core Logic Refactoring (`src/rulebook_ai/core.py`)

**Action:** Refactor the `RuleManager` class to implement the new pack logic.

1.  **Remove `install()` method:** This is replaced by `add_pack()`.
2.  **Create `add_pack(pack_name)`:**
    *   Validates that the pack exists in the source `packs/` dir.
    *   Copies the pack source into the target's `.rulebook-ai/packs/`.
    *   Appends the pack's `name` and `version` to `.rulebook-ai/selection.json`.
    *   Calls `self.sync()` in implicit mode to update existing assistant rules and merge `memory/` and `tools`.
3.  **Create `remove_pack(pack_name)`:**
    *   Removes the pack from `selection.json`.
    *   Deletes the pack's source from `.rulebook-ai/packs/`.
    *   Uses the per-pack file map to purge `memory/` and `tools` files owned by the pack.
    *   Calls `self.sync()` in implicit mode.
4.  **Heavily Refactor `sync()`:**
    *   Sync operates in two modes:
        *   **Explicit** – user passes assistant flags (e.g., `--cursor`); only those assistants are regenerated.
        *   **Implicit** – no flags; used by `add`/`remove` to rebuild rules only for assistants that already have rule directories.
    *   **Delete all existing generated platform rules** (using `assistants.py` spec).
    *   Read the ordered list of pack entries (name and version) from `.rulebook-ai/selection.json`.
    *   **Compose `memory/` and `tools/`:**
        *   Iterate through the active packs *in order*.
        *   For each file in a pack's `memory_starters/` and `tool_starters/`, perform a **non-destructive copy** to the top-level `memory/` and `tools/`. Record each copied path in `.rulebook-ai/packs/<pack>/file-map.json`.
        *   The first pack to provide a file "wins." If a later pack contains a file that already exists, skip it and log a warning so users know which pack was ignored.
        *   Support a `--strict` mode that aborts the sync when any such conflict is detected *(optional, low priority)*.
        *   Support a `--force` flag that overwrites conflicting files from later packs *(optional, low priority)*.
        *   Support a `--rebuild` flag that purges previously copied `memory/` and `tools` files before performing the copy *(optional, low priority)*.
    *   **Compose AI Rules:**
        *   Gather all rule files from the `rules/` directory of *every* active pack.
        *   Concatenate them into a single stream, respecting the order from `selection.json`.
5.  **Refactor `clean_all()` to `clean()` and add `clean_rules()`:**
    *   `clean()` removes the entire `.rulebook-ai/` directory, `memory/`, `tools/`, and all generated platform rules. It must retain its safety confirmation prompt.
    *   `clean_rules()` deletes only `.rulebook-ai/` and generated platform rules, preserving the top-level `memory/` and `tools/` directories.

## 7. Phase 5: CLI Refactoring (`src/rulebook_ai/cli.py`)

**Action:** Update the `argparse` configuration and handler functions to match the new command structure defined in Phase 3.

*   Create sub-parsers for the `packs` command group (`list`, `add`, `remove`, `status`).
*   The `packs add` and `packs remove` commands will take a `pack_name` argument.
*   The main handler will route subcommands to the new methods in `RuleManager` (`add_pack`, `remove_pack`, etc.).
*   Expose both `clean` and `clean-rules` top-level commands, each prompting for confirmation before deleting files.
*   Add a `--strict` option to `sync` that aborts on file conflicts *(optional, low priority)*; without it, sync emits warnings when later packs are skipped.
*   Add a `--force` option to `sync` that overwrites conflicting files *(optional, low priority)*.
*   Add a `--rebuild` option to `sync` that purges `memory/` and `tools/` before copying from active packs *(optional, low priority)*.
*   The `--cursor`, `--cline`, etc. flags are no longer needed for `add`/`remove`, but should be kept for the `sync` command to allow targeted syncs for specific assistants.
