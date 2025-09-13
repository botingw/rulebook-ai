# TDD Plan: Improved UX for Composable Packs

This document outlines the updated test strategy for the refined CLI design that separates configuration from application.

## Phase 0: Full Test Suite Audit and Migration

**Description:** Before implementing new tests, audit the entire existing test suite for compatibility with the new, decoupled workflow. This is critical to prevent test debt and ensure a stable foundation.

- [x] **Task 0.1: Audit all existing integration tests**
    - **Description:** Review every test file in `tests/integration/` to assess its compatibility with the new architecture.
    - **Checklist for each test:**
        - [x] Does it use a test setup helper/fixture that needs updating?
        - [x] Does it call a command that has been renamed or moved (e.g., `clean` -> `project clean`)?
        - [x] Does it assert specific CLI output text that may have changed?
        - [x] Does it rely on the side-effects of `packs add/remove` (implicit sync)?
        - [x] Does it test a command (like `bug-report`) that internally depends on now-changed core logic?

- [x] **Task 0.2: Categorize and Migrate Tests**
    - **Description:** Based on the audit, categorize each legacy test and take action.
    - **Actions:**
        - **Obsolete:** For tests of deprecated workflows (e.g., `test_cli_commands.py`). **Action: Delete.**
        - **Evaluate:** Legacy integration tests such as `test_rule_manager_integration.py` and `test_tools_integration.py` may contain scenarios worth porting. Review and either refactor or remove them.
        - **Safe:** Tests independent of CLI changes (e.g., `test_package_installation.py`). **Action: Keep.**

- [x] **Task 0.3: Establish a Clean Test Baseline**
    - **Description:** After migrating and deleting tests, ensure the entire test suite passes before proceeding.
    - **Action:** Run `pytest tests/` and resolve any remaining failures.

---

## Phase 1: Packs Command Group

### `packs list`
 - [x] `test_packs_list_shows_manifest_info`: Output lists pack names, versions, and descriptions.

### `packs add <input>`
 - [x] `test_add_pack_updates_selection`: Pack added to `selection.json` and copied to `.rulebook-ai/packs/` without touching `memory/` or `tools/`.
 - [x] `test_add_multiple_packs`: Multiple packs can be added in one command.
 - [x] `test_add_nonexistent_pack_fails`: Adding unknown pack exits with error.
 - [x] `test_add_pack_by_local_path`: `packs add local:<path>` copies pack and updates selection.

### `packs remove <name>`
 - [x] `test_remove_pack_updates_selection`: Pack removed from `selection.json` and `.rulebook-ai/packs/`.
 - [x] `test_remove_pack_does_not_touch_context`: `memory/` and `tools/` remain unchanged.
 - [x] `test_remove_nonexistent_pack_fails`: Removing unknown pack exits with error.

### `packs status`
 - [x] `test_packs_status_lists_library_and_profiles`: Displays all packs and profiles defined in `selection.json`.

## Phase 2: Profiles Command Group
 - [x] `test_profiles_create_and_list`: Creating a profile registers it in `selection.json` and `profiles list` shows it.
 - [x] `test_profiles_add_and_remove_packs`: Packs can be added to and removed from a profile.
 - [x] `test_profiles_delete`: Deleting a profile removes it from `selection.json`.

## Phase 3: Project Sync
 - [x] `test_project_sync_all_packs`: Generates rules using all packs and records entries in `sync_status.json`.
 - [x] `test_project_sync_with_profile`: Only packs from the specified profile are used.
 - [x] `test_project_sync_with_pack_flags`: Only explicitly flagged packs are used.
 - [x] `test_project_sync_updates_file_manifest`: `file_manifest.json` reflects newly created context files.

## Phase 4: Project Status
 - [x] `test_project_status_reports_last_sync`: Shows timestamp, mode (all/profile/pack), and pack count for each assistant.

## Phase 5: Cleaning
 - [x] `test_project_clean_requires_confirmation`: Destructive action prompts the user and removes `.rulebook-ai/`, `memory/`, `tools/`, and generated rules upon confirmation.
 - [x] `test_project_clean_aborts_on_decline`: Declining the prompt leaves existing files untouched.
 - [x] `test_project_clean_rules_preserves_context`: `.rulebook-ai/` and rules are removed while `memory/` and `tools/` remain.
 - [x] `test_project_clean_context_removes_orphans`: `project clean-context --action delete --force` removes files from removed packs and updates the manifest.

## Phase 6: Unit Tests
 - [x] `test_selection_json_profiles_schema`: Unit test for reading/writing profiles in `selection.json`.
 - [x] `test_sync_status_recording`: Unit test ensuring `project sync` writes correct data to `sync_status.json`.
 - [x] `test_rule_generation_idempotence`: Running `project sync` twice without changes produces identical results.

## Phase 7: Deferred Interactive Features (P3)
- [ ] Tests for interactive conflict resolution during `project sync`.