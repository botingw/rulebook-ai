# Implementation Update Plan: Improved User Experience

This plan outlines the phases required to migrate from the initial composable pack design to the refined model described in `improve_user_experience_plan.md`.

## Phase 1: Decouple Configuration from Application
- Remove implicit sync behavior from `packs add`/`remove`.
- Ensure these commands only modify `.rulebook-ai/selection.json` and local pack sources.
- Update documentation and help text to remind users to run `project sync`.

## Phase 2: Introduce Profiles
- Extend `selection.json` schema to store a `profiles` map.
- Implement CLI commands under `rulebook-ai profiles` for create/delete/add/remove/list.
- Validate profile names and ensure packs referenced in profiles exist in the library.

## Phase 3: Project Sync Revamp
- Replace the old `sync` command with `project sync`.
- Add `--pack` (repeatable) and `--profile` flags; enforce mutual exclusivity.
- Compose context from selected packs, update `file_manifest.json`, generate rules, and write `sync_status.json` with timestamp and source of context.
- Ensure context files are only added when missing; no overwrites.

## Phase 4: Project Status Command
- Implement `rulebook-ai project status` to read `sync_status.json` and report the last sync per assistant.
- Highlight stale or missing contexts.

## Phase 5: Cleaning Commands
- Rename existing cleaning commands to `project clean` and `project clean-rules`.
- `project clean` must prompt for confirmation before removing `.rulebook-ai/`, `memory/`, `tools/`, or generated rules.
- `project clean-rules` executes without a prompt and preserves user context.
- Reserve future work for an interactive `project clean-context` command.

## Phase 6: Testing and Migration
- Update existing tests to account for the decoupled workflow.
- Add new integration tests for profiles and project commands.
- Remove tests covering deprecated implicit sync behavior.

## Phase 7: Future Enhancements (Low Priority)
- Interactive conflict resolution during `project sync`.
- Interactive `project clean-context` for orphaned context files.
- Non-interactive flags (`--force`, `--conflict-strategy`) for automation.
