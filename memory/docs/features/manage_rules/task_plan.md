# Task Plan: Manage Rules Feature (Composable Packs)

## 🎯 Goal

Track the implementation work required to migrate the CLI to the composable Pack architecture.

---

### Phase 0: Documentation Baseline

**Description:** Establish clear specification and design references.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **0.1** | Consolidate pack-based CLI spec in `spec.md`. | P0 | Completed | - |
| **0.2** | Document implementation design and workflows in `implementation_design.md`. | P0 | Completed | 0.1 |
| **0.3** | Finalize phased implementation roadmap in `support_flexible_ruleset_plan.md`. | P0 | Completed | 0.2 |

### Phase 1: Source Repository Restructuring

**Description:** Move legacy assets into a `packs/` directory with per-pack metadata.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **1.1** | Create top-level `packs/` directory and migrate existing `rule_sets`, `memory_starters`, and `tool_starters`. | P1 | Completed | 0.3 |
| **1.2** | Add `manifest.yaml` for each pack recording name, version, and summary. | P1 | Completed | 1.1 |
| **1.3** | Provide `README.md` in each pack describing its purpose. | P3 | To Do | 1.2 |

### Phase 2: Target Project Structure

**Description:** Establish hidden state and persistent context directories in user projects.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **2.1** | Initialize `.rulebook-ai/` directory with per-pack copies and machine-readable `selection.json`. | P0 | Completed | 1.1 |
| **2.2** | Ensure `memory/` and `tools/` directories are created and tracked under version control. | P0 | Completed | 2.1 |
| **2.3** | Maintain per-pack `file-map.json` to track starter files for clean removal. | P1 | Completed | 2.1 |

### Phase 3: CLI Command Evolution

**Description:** Replace legacy rule-set commands with a pack-focused interface.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **3.1** | Implement `rulebook-ai packs list` showing pack name, version, and description. | P0 | Completed | 1.2 |
| **3.2** | Implement `packs add <name>` with implicit sync and refresh of existing pack copy. | P0 | Completed | 2.1 |
| **3.3** | Implement `packs remove <name>` with implicit sync and cleanup of starter files. | P0 | Completed | 2.3 |
| **3.4** | Implement `packs status` to display active packs in order. | P1 | Completed | 2.1 |
| **3.5** | Implement basic `sync` command (advanced options deferred). | P1 | Completed | 3.2 |
| **3.6** | Add `clean` and `clean-rules` commands with safety prompts. | P1 | Completed | 2.1 |
| **3.7** | Establish `packs add` template with integration test. | P0 | Completed | 3.2 |

### Phase 4: Core Logic Refactoring

**Description:** Extend `RuleManager` to manage packs and compose outputs.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **4.1a** | Implement `list_packs` and `add_pack` methods. | P0 | Completed | 3.1 |
| **4.1b** | Implement `remove_pack` and `status` methods. | P0 | Completed | 3.1 |
| **4.2** | Refactor `sync()` for explicit and implicit modes, conflict handling, and per-pack precedence. | P0 | Completed | 3.5 |
| **4.3** | Implement `clean()` and `clean_rules()` aligned with new state layout. | P1 | Completed | 4.1 |
| **4.4** | Read `manifest.yaml` and maintain per-pack file maps. | P1 | Completed | 4.1 |

### Phase 5: CLI Refactoring

**Description:** Wire argument parsing and handlers to the new core logic.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **5.1a** | Create `packs` subparsers with `list` and `add`. | P0 | Completed | 3.1 |
| **5.1b** | Add `remove` and `status` subcommands. | P0 | Completed | 3.1 |
| **5.2** | Expose `sync` assistant flags and options from `SUPPORTED_ASSISTANTS`. | P1 | Completed | 4.2 |
| **5.3** | Expose top-level `clean` and `clean-rules` commands. | P1 | Completed | 4.3 |
| **5.4** | Provide clear progress messages and commit/ignore hints. | P3 | To Do | 5.1 |

### Phase 6: Testing & Documentation

**Description:** Validate behavior and keep documentation current.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **6.1a** | Add integration test for `packs add` workflow. | P0 | Completed | 5.1a |
| **6.1b** | Add integration tests for `remove` and `status` workflows. | P0 | Completed | 5.1b |
| **6.1c** | Add integration test for `packs list` workflow. | P0 | Completed | 5.1a |
| **6.1d** | Expand integration tests for pack edge cases (multi-pack add, error handling). | P1 | Completed | 6.1a |
| **6.1e** | Add integration tests for platform rule generation and cleanup. | P1 | Completed | 5.2, 5.3 |
| **6.1f** | Audit legacy integration tests (`test_cli_commands.py`, `test_rule_manager_integration.py`, `test_tools_integration.py`) and retire or refactor as needed. | P1 | Completed | 6.1e |
| **6.1g** | Restore package smoke test (`test_package_installation.py`) to verify importability and basic structure. | P2 | Completed | 6.1f |
| **6.2** | Update unit tests for `RuleManager` pack logic. | P0 | Completed | 4.2 |
| **6.2b** | Add unit tests for add/remove/sync/clean/status logic. | P2 | To Do | 6.2 |
| **6.3** | Document workflows and examples in README and feature docs. | P1 | To Do | 6.1 |

### Phase 7: UX Refactor (Decouple Configuration from Application)

**Description:** Update the CLI to match the improved user-experience design with explicit project syncing and profiles.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **7.1** | Update `packs add` and `packs remove` to configuration-only commands (remove implicit sync). Requires revisiting tasks **3.2** and **3.3**. | P0 | Completed | 4.2 |
| **7.2** | Introduce Profiles command group and extend `selection.json` schema. | P0 | Completed | 7.1 |
| **7.3** | Implement `project sync` with `--pack` and `--profile` flags, updating `file_manifest.json` and writing `sync_status.json`. Supersedes task **3.5**. | P0 | Completed | 7.2 |
| **7.4** | Implement `project status` command to read `sync_status.json`. | P1 | Completed | 7.3 |
| **7.5** | Replace top-level `clean` and `clean-rules` with `project clean` and `project clean-rules`, preserving confirmation prompt for `project clean`. Update references from task **3.6**. | P1 | Completed | 7.3 |
| **7.6** | Review existing tests and remove or update ones tied to implicit sync or deprecated commands. | P1 | Completed | 7.3 |
| **7.7** | Add integration tests for `profiles` and `project` command group workflows. | P0 | Completed | 7.3 |
| **7.8** | Implement `project clean-context` command with non-interactive flags; plan further interactive prompts. | P3 | Completed | 7.3 |
| **7.9** | Refactor `packs add` to use a prefix-based system (`local:`, `github:`) for specifying pack sources, removing ambiguous resolution. | P0 | Completed | 7.1 |
