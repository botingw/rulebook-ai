# TDD Plan: Composable Packs

This document tracks the tests for the composable packs feature, with a focus on integration tests for the CLI commands.

## Phase 1: Integration Tests

### `packs list`

- [x] `test_packs_list_success`: The command runs successfully and exits with code 0.
- [x] `test_packs_list_output_contains_pack_names`: The output includes the names of all available packs (e.g., "light-spec", "heavy-spec").
- [x] `test_packs_list_output_contains_manifest_data`: The output displays the `version` and `summary` for each pack, read from its `manifest.yaml`.

### `packs add <name>`

- [x] `test_add_first_pack`: Add a pack to a new project.
    - [x] Verify `.rulebook-ai/` directory is created.
    - [x] Verify `.rulebook-ai/selection.json` is created and contains the pack's name and version.
    - [x] Verify the full pack is copied to `.rulebook-ai/packs/<name>/`.
    - [x] Verify `memory/` and `tools/` directories are created and populated with starter files.
    - [x] Verify an implicit sync runs and generated assistant rules are present.
- [x] `test_add_second_pack`: Add a second pack to the project.
    - [x] Verify `selection.json` is updated with the second pack.
    - [x] Verify the second pack is copied to `.rulebook-ai/packs/<new-pack>/`.
    - [x] Verify `memory/` and `tools/` are updated by merging the new files without overwriting existing ones.
    - [x] Verify implicit sync runs and generated rules are updated based on the combined packs.
- [ ] `test_add_existing_pack_refreshes`: Add a pack that is already active.
    - [ ] Verify the pack's content in `.rulebook-ai/packs/<name>/` is updated to match the source.
    - [ ] Verify `selection.json` remains unchanged.
    - [ ] Verify an implicit sync is triggered.
- [x] `test_add_non_existent_pack`: Attempt to add a pack that does not exist.
    - [x] Verify the command fails with a non-zero exit code.
    - [x] Verify an informative error message is printed.

### `packs remove <name>`

- [x] `test_remove_pack`: Remove an active pack.
    - [x] Verify the pack is removed from `selection.json`.
    - [x] Verify the pack's directory is deleted from `.rulebook-ai/packs/`.
    - [x] Verify starter files associated with the pack are removed from `memory/` and `tools/` (using a file map).
    - [x] Verify an implicit sync runs and generated rules are updated.
- [x] `test_remove_last_pack`: Remove the only active pack.
    - [x] Verify `selection.json` becomes an empty list.
    - [x] Verify `.rulebook-ai/packs/` becomes empty.
    - [x] Verify `memory/` and `tools/` become empty (or are removed).
- [x] `test_remove_non_existent_pack`: Attempt to remove a pack that is not active.
    - [x] Verify the command fails with a non-zero exit code.
    - [x] Verify an informative error message is printed.

### `packs status`

- [x] `test_status_no_packs`: Run `packs status` in a project with no active packs.
    - [x] Verify the output indicates that no packs are active.
- [x] `test_status_one_pack`: Run `packs status` with one active pack.
    - [x] Verify the output correctly displays the pack's name and version.
- [x] `test_status_multiple_packs`: Run `packs status` with multiple active packs.
    - [x] Verify the output lists all packs in the correct order of precedence.

### `sync`

- [x] `test_sync_no_flags`: Run `sync` to regenerate rules for all active packs.
    - [x] Verify generated rules reflect the combined content of all packs.
- [ ] `test_sync_rebuild`: Run `sync --rebuild`.
    - [ ] Verify `memory/` and `tools/` are purged and fully repopulated from active packs.
- [ ] `test_sync_force`: Test conflict resolution with `sync --force`.
    - [ ] Create a conflict where a later pack has a file that also exists from an earlier pack.
    - [ ] Verify the file from the later pack overwrites the earlier one.
- [ ] `test_sync_strict`: Test conflict resolution with `sync --strict`.
    - [ ] Create a file conflict.
    - [ ] Verify the command fails with a non-zero exit code and an error message.

### Target Platform Rules

- [x] `test_sync_generates_platform_rules`: After adding a pack, run `sync` and verify platform-specific artifacts for multi-file, mode-based, and single-file assistants are created.
- [x] `test_clean_rules_removes_platform_artifacts`: After generating platform rules, run `clean-rules` and confirm those artifacts are removed while `memory/` and `tools/` remain.

### `clean`

- [x] `test_clean_confirm_yes`: Run `clean` and provide "yes" to the confirmation prompt.
    - [x] Verify `.rulebook-ai/`, `memory/`, `tools/`, and all generated rule artifacts are removed.
- [x] `test_clean_confirm_no`: Run `clean` and provide "no" to the confirmation prompt.
    - [x] Verify no files or directories are removed.

### `clean-rules`

- [x] `test_clean_rules`: Run the `clean-rules` command.
    - [x] Verify `.rulebook-ai/` and generated rule artifacts are removed.
    - [x] Verify `memory/` and `tools/` are preserved.

## Phase 2: Unit Tests

This section outlines the unit tests for the `RuleManager` class in `core.py`.

### `RuleManager`

- [x] `test_list_packs`: Mocks the filesystem and verifies the method correctly finds and parses pack manifests.
- [ ] `test_add_pack_logic`: Tests the core logic of adding a pack, mocking filesystem interactions.
- [ ] `test_remove_pack_logic`: Tests the core logic of removing a pack.
- [ ] `test_sync_logic`: Tests the file composition and conflict resolution logic in isolation.
- [ ] `test_clean_logic`: Tests the file/directory removal logic.
- [ ] `test_status_logic`: Tests reading and parsing of `selection.json`.
