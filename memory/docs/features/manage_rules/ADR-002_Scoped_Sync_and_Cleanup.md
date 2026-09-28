# ADR-002: Scoped Sync and Pack Cleanup

## Status
Accepted

## Context
`rulebook-ai` is moving from a single ruleset model to composable packs. The original CLI coupled pack operations with a global `sync` that updated every assistant and left stale `memory/` and `tools/` files when packs were removed. This produced surprises for users and inconsistent project state.

## Decision
- `packs add` and `packs remove` only mutate the active pack list recorded in `selection.json`. They never regenerate `memory/`, `tools/`, or platform rules, and never invoke a sync implicitly; both commands print a reminder to run `project sync`.
- Rule generation happens only through the explicit `rulebook-ai project sync` command.
- `project sync` targets assistants with the `--assistant/-a` flag (repeatable, or `--all` for every supported assistant). It does not use per-assistant flags such as `--cursor` or `--claude`.
- During sync, the system records which `memory/` and `tools/` files originate from each pack in `file_manifest.json`, so removing a pack can purge its files on the next sync.
- `file_manifest.json` at the top level of `.rulebook-ai/` is the canonical record of per-pack file ownership.
- Two cleanup commands remain: `project clean` (removes `.rulebook-ai/`, `memory/`, `tools/`, and generated rules, and asks for confirmation) and `project clean-rules` (removes `.rulebook-ai/` and generated rules while preserving `memory/` and `tools/`, without a confirmation prompt). A third command, `project clean-context`, removes orphaned context files.

## Consequences
- Users avoid accidental propagation of rules to new assistants: nothing is regenerated until `project sync` is run.
- Pack add/remove stay cheap and predictable, since they only edit `selection.json`.
- A user who removes a pack and does not sync keeps the previous generated rules and their `memory/`/`tools/` files until the next `project sync`; tracking per-pack file maps makes that cleanup possible.
- Tracking per-pack file maps introduces a small bookkeeping cost.

## Alternatives Considered
- Running a full sync on every `add/remove` regardless of existing assistants – rejected due to surprise updates.
- Per-assistant flags (`--cursor`, `--claude`, …) on `sync` – rejected in favour of a single repeatable `--assistant/-a` flag, which keeps the parser small and matches the implemented CLI.


