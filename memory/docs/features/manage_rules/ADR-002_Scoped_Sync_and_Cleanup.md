# ADR-002: Scoped Sync and Pack Cleanup

## Status
Accepted

## Context
`rulebook-ai` is moving from a single ruleset model to composable packs. The original CLI coupled pack operations with a global `sync` that updated every assistant and left stale `memory/` and `tools/` files when packs were removed. This produced surprises for users and inconsistent project state.

## Decision
- `add_pack` and `remove_pack` only mutate the active pack list and then invoke `sync` in *implicit* mode.
- `sync` supports two modes:
  - **Explicit** – users run `rulebook-ai sync --cursor --claude` to target specific assistants.
  - **Implicit** – internal calls without assistant flags rebuild rules only for assistants already present in the repository.
- During sync, the system records which `memory/` and `tools/` files originate from each pack. Removing a pack purges these files before rebuilding from remaining packs.
- Implicit sync never creates rule directories for new assistants; it updates only those previously configured.
- Two cleanup commands remain: `clean` (remove all packs, memory, tools, and rules) and `clean-rules` (delete only `.rulebook-ai/` and generated rules).

## Consequences
- Users avoid accidental propagation of rules to new assistants.
- Projects stay consistent after pack removal because stale files are tracked and deleted.
- Tracking per-pack file maps introduces a small bookkeeping cost.

## Alternatives Considered
- Running a full sync on every `add/remove` regardless of existing assistants – rejected due to surprise updates.
- Requiring users to run `sync` manually after every pack change – rejected because it leaves the repo in an inconsistent state by default.

