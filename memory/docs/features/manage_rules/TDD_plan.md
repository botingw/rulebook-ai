# TDD Plan: Improved UX for Composable Packs

This document outlines the updated test strategy for the refined CLI design that separates configuration from application.

## Phase 1: Packs Command Group

### `packs list`
- [ ] `test_packs_list_shows_manifest_info`: Output lists pack names, versions, and descriptions.

### `packs add <name>`
- [ ] `test_add_pack_updates_selection`: Pack added to `selection.json` and copied to `.rulebook-ai/packs/` without touching `memory/` or `tools/`.
- [ ] `test_add_multiple_packs`: Multiple packs can be added in one command.
- [ ] `test_add_nonexistent_pack_fails`: Adding unknown pack exits with error.

### `packs remove <name>`
- [ ] `test_remove_pack_updates_selection`: Pack removed from `selection.json` and `.rulebook-ai/packs/`.
- [ ] `test_remove_pack_does_not_touch_context`: `memory/` and `tools/` remain unchanged.
- [ ] `test_remove_nonexistent_pack_fails`: Removing unknown pack exits with error.

### `packs status`
- [ ] `test_packs_status_lists_library_and_profiles`: Displays all packs and profiles defined in `selection.json`.

## Phase 2: Profiles Command Group
- [ ] `test_profiles_create_and_list`: Creating a profile registers it in `selection.json` and `profiles list` shows it.
- [ ] `test_profiles_add_and_remove_packs`: Packs can be added to and removed from a profile.
- [ ] `test_profiles_delete`: Deleting a profile removes it from `selection.json`.

## Phase 3: Project Sync
- [ ] `test_project_sync_all_packs`: Generates rules using all packs and records entries in `sync_status.json`.
- [ ] `test_project_sync_with_profile`: Only packs from the specified profile are used.
- [ ] `test_project_sync_with_pack_flags`: Only explicitly flagged packs are used.
- [ ] `test_project_sync_updates_file_manifest`: `file_manifest.json` reflects newly created context files.

## Phase 4: Project Status
- [ ] `test_project_status_reports_last_sync`: Shows timestamp, mode (all/profile/pack), and pack count for each assistant.

## Phase 5: Cleaning
- [ ] `test_project_clean_requires_confirmation`: Destructive action prompts the user and removes `.rulebook-ai/`, `memory/`, `tools/`, and generated rules upon confirmation.
- [ ] `test_project_clean_aborts_on_decline`: Declining the prompt leaves existing files untouched.
- [ ] `test_project_clean_rules_preserves_context`: `.rulebook-ai/` and rules are removed while `memory/` and `tools/` remain.

## Phase 6: Unit Tests
- [ ] `test_selection_json_profiles_schema`: Unit test for reading/writing profiles in `selection.json`.
- [ ] `test_sync_status_recording`: Unit test ensuring `project sync` writes correct data to `sync_status.json`.
- [ ] `test_rule_generation_idempotence`: Running `project sync` twice without changes produces identical results.

## Phase 7: Deferred Interactive Features (P3)
- [ ] Tests for `project clean-context` once implemented.
- [ ] Tests for interactive conflict resolution during `project sync`.
