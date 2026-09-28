# Command Flow Diagrams

This document visualizes the high-level flow of major commands introduced in the composable pack system. Diagrams focus on
spec-level behavior rather than implementation details.

## `rulebook-ai packs add <name>`

```mermaid
flowchart TD
    A[User runs `packs add <name>`] --> B{Pack exists in source repo or community index?}
    B -- No --> Z[Report not found and list available packs]
    B -- Yes --> C[Copy pack to `.rulebook-ai/packs/`]
    C --> D[Record name & version in `selection.json`]
    D --> E[Print reminder to run `project sync`]
    E --> F[Command completes]
```

*`packs add` only edits the pack library. It does not touch `memory/`, `tools/`, or generated rules — the user must run `project sync` explicitly.*

## `rulebook-ai packs remove <name>`

```mermaid
flowchart TD
    A[User runs `packs remove <name>`] --> B{Pack installed?}
    B -- No --> Z[Report not installed]
    B -- Yes --> C[Delete pack dir from `.rulebook-ai/packs/`]
    C --> D[Remove entry from `selection.json` and every profile]
    D --> E[Print reminder to run `project sync`]
    E --> F[Command completes]
```

*`packs remove` only edits the pack library. Files previously copied into `memory/` and `tools/` are purged by the next `project sync`, using the pack's entries in `file_manifest.json`.*

## `rulebook-ai project sync`

```mermaid
flowchart TD
    A[User runs `project sync`] --> B{`--assistant/-a` or `--all` provided?}
    B -- Yes --> C[Target the listed / all supported assistants]
    B -- No --> Z[Error: no target assistants selected]
    C --> D[Read active packs and profiles from `selection.json`]
    D --> E[Merge packs into `memory/` & `tools/`]
    E --> F[Update `file_manifest.json` with per-pack file ownership]
    F --> G[Write platform rules for the targeted assistants]
    G --> H[Record results in `sync_status.json`]
    H --> I[Command completes]
```

## `rulebook-ai project clean`

```mermaid
flowchart TD
    A[User runs `project clean`] --> B{User confirms?}
    B -- No --> Z[Print cancelled and abort]
    B -- Yes --> C[Delete generated assistant rule dirs]
    C --> D[Delete `.rulebook-ai/`]
    D --> E[Delete `memory/` & `tools/`]
    E --> F[Command completes]
```

## `rulebook-ai project clean-rules`

```mermaid
flowchart TD
    A[User runs `project clean-rules`] --> B[Delete generated assistant rule dirs]
    B --> C[Delete `.rulebook-ai/`]
    C --> D[Preserve `memory/` & `tools/`]
    D --> E[Command completes]
```

*Unlike `project clean`, `project clean-rules` runs without a confirmation prompt; it never touches user-owned `memory/` and `tools/`.*

## `rulebook-ai project clean-context`

```mermaid
flowchart TD
    A[User runs `project clean-context`] --> B{`--action` provided?}
    B -- No --> C[Report orphaned context files]
    B -- `delete` --> D[Delete orphaned context files]
    B -- `keep` --> E[Leave orphaned context files in place]
    D --> F[Command completes]
    E --> F
```

*`--force` skips the prompt when removing orphaned context files.*
