# Specification: Community Pack Ecosystem (MVP)

## 1. Overview & Motivation

The primary motivation for this feature is to evolve `rulebook-ai` from a standalone tool into a platform with a thriving, community-driven ecosystem. We want to empower users to easily share, discover, and use `Rule Packs` created by others, fostering a collaborative environment for AI-assisted development best practices.

This document specifies the Minimum Viable Product (MVP) for this feature, designed to be simple, secure, and maintainable, while providing a solid foundation for future growth. It **extends** the core CLI behavior described in [`manage_rules/spec.md`](../manage_rules/spec.md); only community‑specific behavior is documented here.

## 2. Design Principles

The design of this feature is guided by the following core principles, which prioritize maintainer sustainability and user safety:

1.  **Sustainable Maintenance & Delegated Trust**: We acknowledge that the project maintainer cannot personally audit every community pack for security. Therefore, the system is designed to delegate the final trust decision to the end-user. The community index is a discovery tool, not a security endorsement.
2.  **User Empowerment Through Transparency**: The CLI's primary role is to empower users to make informed decisions. It achieves this by performing an automated structural validation on packs and presenting clear, explicit warnings about installing third-party code.
3.  **Contributor Convenience**: To foster a healthy ecosystem, the process for contributing a pack should be as low-friction as possible. This means pointing to a default branch instead of requiring contributors to manage immutable commit hashes.
4.  **Simplicity & Predictability**: The user-facing commands should be simple, and their behavior (especially network access) must be predictable. The user should always be in control.

## 3. Core Concepts

1.  **Community Pack**: A standard Rule Pack, conforming to the `pack_developer_guide.md`, hosted in a public GitHub repository.

2.  **Public Index Repository**: A single, official, public Git repository that serves as a curated list of community packs. Its core is a `packs.json` file.

3.  **Local Index Cache**: A local copy of the `packs.json` file stored on the user's machine. For the MVP the cache lives inside the installed Python package at `rulebook_ai/community/index_cache/packs.json` so that all repositories share one updated index. This cache is **only** updated when the user explicitly runs the `packs update` command.
## 4. Index Data Model

Each entry in `packs.json` describes a single community pack with the following fields:

* `name` (string, required) – globally unique pack identifier.
* `username` (string, required) – GitHub account that hosts the repository.
* `repo` (string, required) – repository name.
* `path` (string, optional) – path within the repository to the pack root; defaults to `/`.
* `description` (string, required) – short human-readable summary.
* `commit` (string, optional) – specific commit or tag to check out.

The trio `username`, `repo`, and optional `path` form a **slug** `username/repo[/path]` that uniquely identifies the source location. The slug is recorded in local metadata so the original source can always be traced.

## 5. Installation Path & Collision Rules

* Every installed community pack is copied to `.rulebook-ai/packs/<name>` within the target repository.
* Pack `name` values must be globally unique and cannot match built‑in pack names.
* If `.rulebook-ai/packs/<name>` already exists from a different source, the CLI aborts and no files are modified.
* Local metadata records the source slug to ensure traceability of each pack.

## 6. CLI Integration

The following notes supplement the `packs` subcommands defined in [`manage_rules/spec.md`](../manage_rules/spec.md) with community-specific behavior.

* **`packs list`** – merges built‑in packs with entries from the Local Index Cache. Community packs appear with a `(community)` label. No network calls are made.
* **`packs add <input>`** – resolves `<input>` either as a direct GitHub slug (`username/repo[/path]`) or as a named pack from the unified list. If no match is found, the CLI aborts with a clear "pack not found" error. After resolving the source, the CLI clones, **warns and requires explicit user confirmation** before installing, reflecting the *User Empowerment Through Transparency* principle in the Design section. The pack is then structurally verified using the same checks described in the **Contribution Workflow** section; any validation failure aborts the install. If the pack's `manifest.yaml` `name` conflicts with an existing local pack, the command fails.
* **`packs update`** – new command that:
    1. Fetches the latest `packs.json` from the Public Index Repository.
    2. Validates the JSON structure and required fields.
    3. Replaces the Local Index Cache on success; otherwise the existing cache is kept and an error is reported.
  This is the only `packs` subcommand that performs network access.

## 7. Contribution Workflow

Before a pack can be added to the public index, it must meet several quality standards. These requirements are checked during the maintainer review.

**Pack Requirements:**
*   **Public GitHub Repository**: The pack must be hosted in a public GitHub repository.
*   **Valid Structure**: It must adhere to the `pack_developer_guide.md`.
*   **High-Quality `README.md`**: The pack's own root `README.md` must clearly explain its purpose, philosophy, and usage.
*   **Stability**: The pack should be reasonably stable. Highly experimental packs may not be accepted.

The process for adding a new pack to the public index is as follows:

1.  **Developer Creates Pack**: A developer creates a high-quality pack in their own public GitHub repository, ensuring it follows the `pack_developer_guide.md`.
2.  **Submit Pull Request**: The developer submits a Pull Request to the `Index Repository`, adding their pack's metadata to the `packs.json` file.
    *   Including a specific `commit` or `tag` is **highly recommended** for security and stability, as it ensures users install a specific, reviewed version of the pack.
    *   If omitted, the pack will be installed from the default branch, which is less secure.
3.  **Automated Validation (CI)**: A `GitHub Action` automatically runs on the Pull Request. This CI job performs a sanity check by cloning the pack's repository and validating its structure. This validation **must** include a check to ensure the `name` in the pack's `manifest.yaml` matches the `name` being submitted to `packs.json`. The CI check must fail if they do not match.
4.  **Maintainer Review**: After CI passes, a maintainer performs a quick review of the submission (e.g., checking for appropriateness, clear documentation) and merges the PR.
5.  **Public Availability**: Once merged, the pack becomes available for discovery to all users after they run `rulebook-ai packs update`.
