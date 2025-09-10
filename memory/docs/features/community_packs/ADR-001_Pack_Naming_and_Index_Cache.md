# ADR-001: Community Pack Naming and Index Cache Strategy

## Status

Accepted

## Context

Community packs allow third-party `Rule Packs` to be installed via the `rulebook-ai` CLI. Because packs are copied into `.rulebook-ai/packs/<name>`, two challenges arise:

1. **Name collisions**: Different repositories may publish packs with the same `manifest.yaml` `name`.
2. **Shared discovery data**: The CLI needs an index of available community packs, and this index should be available across all user projects.

## Decision

* **Global name enforcement (alias deferred)**
  * The `manifest.yaml` `name` is treated as a globally unique identifier.
  * If an unlisted pack's `name` conflicts with an existing local pack, the CLI aborts and no alias is offered in the MVP.
  * Installed packs use this `name` as the directory under `.rulebook-ai/packs/`. The source slug, decomposed as `username/repo[/path]`, is recorded in metadata for traceability.

* **Shared Local Index Cache**
  * The community index `packs.json` is cached inside the installed Python package under `rulebook_ai/community/index_cache/packs.json`.
  * The `rulebook-ai packs update` command refreshes this cache. Because it lives in the package directory, all repositories on the same machine share a single copy.

## Consequences

* Users can keep working with short, memorable pack names while avoiding accidental overwrites.
* Conflicting names result in an error until upstream naming is resolved, keeping behavior predictable.
* A single Local Index Cache avoids repeated downloads and keeps different projects in sync.
* Future features (e.g., alias support, per-repo caches, or namespace support) can build on this foundation without breaking the MVP design.

## Alternatives Considered

* **Installing packs by slug** – This avoids collisions but forces users to remember long identifiers. Rejected for poorer user experience.
* **Per-repository index cache** – Would duplicate data and require each project to update separately. Rejected to keep MVP simple and predictable.

