# Implementation Design: Rulebook-AI CLI

## 1. High-Level Goal & Architecture

The refactored CLI lets users compose multiple modular **Packs** inside one project while still keeping the codebase easy to maintain. It preserves a **separation of concerns**:

1. **Declarative configuration (`assistants.py`)** – describes how each supported assistant expects its rules to be laid out on disk. Adding a new assistant remains a matter of adding a new spec.
2. **Generic engine (`core.py`)** – interprets those specs and carries out filesystem operations such as copying, syncing, and cleaning. The engine now manages multiple packs rather than a single rule set.

### Key Directories in a Target Project

| Path | Purpose |
|------|---------|
| `.rulebook-ai/` | Hidden internal state. Holds per-pack copies under `.rulebook-ai/packs/<pack>/` and a machine-readable `selection.json` recording the active pack list and order. |
| `memory/` | User-owned unified memory bank. Populated from pack `memory_starters/` and intended for version control. |
| `tools/` | User-owned unified tools directory. Populated from pack `tool_starters/` and intended for version control. |
| *Assistant rule dirs* | Generated platform rules (e.g., `.cursor/`, `.clinerules/`, `WARP.md`). Should be gitignored. |

Earlier packs in `selection.json` take precedence when files conflict; later packs are skipped unless the user opts into `--force` or `--strict` behaviors.

## 2. Code Structure

### `src/rulebook_ai/assistants.py`
Declarative definitions of supported assistants using an `AssistantSpec` dataclass. Each spec describes how rule files are laid out on disk.

### `src/rulebook_ai/core.py`
Home of the `RuleManager` class. Key responsibilities:

- `list_packs()` – enumerate available packs from the source repo.
- `add_pack(name)` – copy a pack into `.rulebook-ai/packs/`, refresh if it already exists, append to `selection.json`, merge starter `memory/` and `tools` without overwriting existing files, then trigger an implicit sync.
- `remove_pack(name)` – drop a pack from `selection.json`, delete its copy under `.rulebook-ai/packs/`, remove starter files it introduced, then trigger an implicit sync.
- `sync(assistants=None, strict=False, force=False, rebuild=False)` – regenerate assistant rules and compose `memory/`/`tools` from active packs. Supports explicit invocation (user runs `sync`) and implicit invocation (called from `add_pack`/`remove_pack`).
- `clean()` – remove `.rulebook-ai/`, `memory/`, `tools/`, and all generated rule directories after confirmation.
- `clean_rules()` – remove `.rulebook-ai/` and generated rule directories while preserving `memory/` and `tools`.
- `status()` – read `selection.json` and report the active pack list and order.

The class reads each pack's `manifest.yaml` and maintains a `file-map.json` per pack to track which starter files were copied.

### `src/rulebook_ai/cli.py`
Argument parsing and user interaction via `argparse`:

- Provides a `packs` command group with `list`, `add <name>`, `remove <name>`, and `status` subcommands.
- Exposes top-level `sync`, `clean`, and `clean-rules` commands.
- Dynamically generates assistant flags (`--cursor`, `--cline`, etc.) from `SUPPORTED_ASSISTANTS` for the `sync` command.
- Prints progress messages and helpful commit/ignore hints after operations.

## 3. Core Implementation Notes

- **Explicit state:** `selection.json` is the source of truth for which packs are active and in what order. All operations read and update this file.
- **Pack refresh:** `add_pack` always clears and overwrites any existing copy of the pack in `.rulebook-ai/packs/<pack>/` to ensure freshness.
- **Conflict handling:** When composing `memory/` and `tools`, earlier packs win. Later packs encountering existing files are skipped with a warning. `--strict` aborts on conflict; `--force` overwrites.
- **Implicit vs. explicit sync:** `sync` regenerates assistant rules and merges starter files. Explicit sync is invoked directly by the user and may target specific assistants. Implicit sync is automatically run after `add_pack` or `remove_pack`.
- **Path handling:** The implementation must use robust path handling to manage files and directories across different operating systems.
- **User feedback:** The CLI should provide clear and concise feedback to the user for all operations.
- **Hardcoded constants:** Directory names for framework components (e.g., `rule_sets` in the source repo, `memory`, `tools` in the target repo) are hardcoded as constants within the script for simplicity and reliability.
- **Parent directory creation:** Helper functions that write files (e.g., for `copilot-instructions.md` or `GEMINI.md`) must ensure that the parent directories (`.github/`, `.gemini/`) are created if they do not exist.
- **Extensibility for assistants:** The `AssistantSpec` is designed to be extensible. For example, the `has_modes` flag supports assistants like Kilo Code and Roo Code, which use subdirectories for different modes.

## 4. Typical Workflows

1. **Start a project**
   - `rulebook-ai packs add light-spec`
   - Commit `memory/`, `tools/`, and relevant `.gitignore` updates.

2. **Compose personas**
   - `rulebook-ai packs add python-data-scientist`
   - `rulebook-ai packs status`

3. **Regenerate rules after manual edits**
   - Modify files in `memory/` or `tools/`.
   - `rulebook-ai sync --cursor`

4. **Remove a pack**
   - `rulebook-ai packs remove python-data-scientist`
   - Commit resulting changes to `memory/`, `tools`, and generated rules.

5. **Reset generated rules only**
   - `rulebook-ai clean-rules`

6. **Full uninstall**
   - `rulebook-ai clean`

These workflows mirror the CLI behaviors documented in `spec.md` while highlighting how the underlying components cooperate.
