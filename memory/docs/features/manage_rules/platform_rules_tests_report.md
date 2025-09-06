# Platform Rules Test Review

## Summary
This report evaluates existing integration tests related to Target Platform Rules and their alignment with the current composable packs architecture. It also identifies new test coverage needed for the `sync` and cleaning commands.

## Findings
### `tests/integration/test_cli_commands.py`
- Exercises legacy `install` and `sync` commands.
- Examples:
  - `test_install_default_rule_set` checks `.cursor/rules/`, `.roo/rules-architect/01-plan_v1.md`, `WARP.md`, and `.github/copilot-instructions.md` are created.
  - `test_sync_with_specific_assistant_flags` modifies a rule then verifies the synced `.windsurf` artifact contains the change.
  - `test_sync_detects_existing_assistants` auto-detects assistant directories and syncs new outputs.
- Confirms that `clean-rules` removes these artifacts.
- **Action:** Break up and port scenarios into pack-based tests; once migrated, remove this file.

### `tests/integration/test_package_installation.py`
- Checks package importability and basic structure.
- Not tied to pack management; can remain as a generic sanity check.

### `tests/integration/test_rule_manager_integration.py`
- Uses deprecated rule-set `install` workflow.
- Overlaps with new `packs add` tests that already verify `.rulebook-ai/`, `selection.json`, and `file-map.json`.
- **Action:** Remove after confirming new `packs add` and `sync` tests cover needed behavior.

### `tests/integration/test_tools_integration.py`
- Invokes obsolete CLI commands (`install`, `list-packs`, `doctor`).
- Contains programmatic `RuleManager` checks now covered elsewhere.
- **Action:** Remove; any remaining entry-point smoke tests can be folded into new integration suites.

## TDD & Task Plan Updates
- Add TDD items for platform rule generation and cleanup.
- Track an integration-test task for platform rules in the task plan (P1).

