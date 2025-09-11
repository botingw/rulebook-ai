# TDD Plan: Community Pack Ecosystem

This document outlines the test strategy for introducing community-maintained rule packs.

## Test Strategy & Environment

- **Test Type**: The tests for this feature are primarily **`integration tests`**. They verify the integration of the `rulebook-ai` CLI with external systems like the local filesystem and the `Git` version control system.
- **Test Dependencies**:
    - To test the `packs add <slug>` functionality, tests will rely on local mock `Git` repositories created under the `tests/fixtures/` directory. This approach ensures tests are fast, reliable, and independent of network connectivity.
    - To test the `packs update` functionality, tests will use a local mock `packs.json` index file, rather than fetching from a live production URL.

---

## Phase 1: Core Engine (Add by Slug)
- [x] `test_add_pack_by_slug_installs_to_folder`: installing `username/repo` places files under `.rulebook-ai/packs/<name>`.
- [x] `test_add_pack_conflicting_name_fails`: adding a pack whose `manifest.yaml` `name` already exists aborts.
- [x] `test_add_pack_invalid_structure_fails`: missing required files triggers validation error.
- [x] `test_add_pack_user_decline_aborts`: user choosing "no" cancels installation.

## Phase 2: Community Index
- [x] `test_packs_update_refreshes_cache`: `packs update` replaces `rulebook_ai/community/index_cache/packs.json` when fetch succeeds.
- [x] `test_packs_update_invalid_json_retains_old_cache`: malformed index leaves previous cache untouched.
- [x] `test_add_pack_by_name_uses_cache`: installing by `name` pulls metadata from the cache and clones the correct repository.
- [x] `test_add_unknown_pack_name_fails`: unknown `name` emits "pack not found" error.
- [x] `test_installed_pack_records_slug_metadata`: installed pack stores slug metadata and shows `(community)` in `packs list`.
- [x] `test_add_pack_name_mismatch_fails`: manifest `name` differing from index entry aborts install.

## Phase 3: Listing and Visibility
- [x] `test_packs_list_shows_builtin_and_community`: output merges built-in packs with entries from the cache and labels community packs.
- [x] `test_packs_list_does_not_hit_network`: running `packs list` uses only local data.

## Phase 4: Ecosystem Infrastructure
Tests in this phase run inside the separate public index repository's CI.

- [ ] `test_index_ci_validation_checks_name_alignment`: CI workflow rejects pull requests when `manifest.yaml` `name` differs from index entry.
- [ ] `test_index_ci_validation_detects_missing_files`: CI workflow fails when repository lacks required structure.
