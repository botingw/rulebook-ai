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
| **1.1** | Create top-level `packs/` directory and migrate existing `rule_sets`, `memory_starters`, and `tool_starters`. | P1 | To Do | 0.3 |
| **1.2** | Add `manifest.yaml` for each pack recording name, version, and summary. | P1 | To Do | 1.1 |
| **1.3** | Provide `README.md` in each pack describing its purpose. | P3 | To Do | 1.2 |

### Phase 2: Target Project Structure

**Description:** Establish hidden state and persistent context directories in user projects.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **2.1** | Initialize `.rulebook-ai/` directory with per-pack copies and machine-readable `selection.json`. | P0 | To Do | 1.1 |
| **2.2** | Ensure `memory/` and `tools/` directories are created and tracked under version control. | P0 | To Do | 2.1 |
| **2.3** | Maintain per-pack `file-map.json` to track starter files for clean removal. | P1 | To Do | 2.1 |

### Phase 3: CLI Command Evolution

**Description:** Replace legacy rule-set commands with a pack-focused interface.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **3.1** | Implement `rulebook-ai packs list` showing pack name, version, and description. | P0 | To Do | 1.2 |
| **3.2** | Implement `packs add <name>` with implicit sync and refresh of existing pack copy. | P0 | To Do | 2.1 |
| **3.3** | Implement `packs remove <name>` with implicit sync and cleanup of starter files. | P0 | To Do | 2.3 |
| **3.4** | Implement `packs status` to display active packs in order. | P1 | To Do | 2.1 |
| **3.5** | Update `sync` command with `--strict`, `--force`, and `--rebuild` options. | P2 | To Do | 3.2 |
| **3.6** | Add `clean` and `clean-rules` commands with safety prompts. | P2 | To Do | 2.1 |

### Phase 4: Core Logic Refactoring

**Description:** Extend `RuleManager` to manage packs and compose outputs.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **4.1** | Add `list_packs`, `add_pack`, `remove_pack`, and `status` methods. | P0 | To Do | 3.1 |
| **4.2** | Refactor `sync()` for explicit and implicit modes, conflict handling, and per-pack precedence. | P0 | To Do | 3.5 |
| **4.3** | Implement `clean()` and `clean_rules()` aligned with new state layout. | P1 | To Do | 4.1 |
| **4.4** | Read `manifest.yaml` and maintain per-pack file maps. | P1 | To Do | 4.1 |

### Phase 5: CLI Refactoring

**Description:** Wire argument parsing and handlers to the new core logic.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **5.1** | Create `packs` subparsers (`list`, `add`, `remove`, `status`). | P0 | To Do | 3.1 |
| **5.2** | Expose `sync` assistant flags and options from `SUPPORTED_ASSISTANTS`. | P1 | To Do | 4.2 |
| **5.3** | Expose top-level `clean` and `clean-rules` commands. | P1 | To Do | 4.3 |
| **5.4** | Provide clear progress messages and commit/ignore hints. | P3 | To Do | 5.1 |

### Phase 6: Testing & Documentation

**Description:** Validate behavior and keep documentation current.

| Task ID | Description | Importance | Status | Dependencies |
|:--------|:------------|:-----------|:-------|:-------------|
| **6.1** | Add integration tests for pack workflows (`add`, `remove`, `sync`). | P0 | To Do | 5.1 |
| **6.2** | Update unit tests for `RuleManager` pack logic. | P0 | To Do | 4.2 |
| **6.3** | Document workflows and examples in README and feature docs. | P1 | To Do | 6.1 |
