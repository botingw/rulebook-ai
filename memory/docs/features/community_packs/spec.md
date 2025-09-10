# Specification: Community Pack Ecosystem (MVP)

## 1. Overview & Motivation

The primary motivation for this feature is to evolve `rulebook-ai` from a standalone tool into a platform with a thriving, community-driven ecosystem. We want to empower users to easily share, discover, and use `Rule Packs` created by others, fostering a collaborative environment for AI-assisted development best practices.

This document specifies the Minimum Viable Product (MVP) for this feature, designed to be simple, secure, and maintainable, while providing a solid foundation for future growth.

## 2. Design Principles

The design of this feature is guided by the following core principles, which prioritize maintainer sustainability and user safety:

1.  **Sustainable Maintenance & Delegated Trust**: We acknowledge that the project maintainer cannot personally audit every community pack for security. Therefore, the system is designed to delegate the final trust decision to the end-user. The community index is a discovery tool, not a security endorsement.
2.  **User Empowerment Through Transparency**: The CLI's primary role is to empower users to make informed decisions. It achieves this by performing an automated structural validation on packs and presenting clear, explicit warnings about installing third-party code.
3.  **Contributor Convenience**: To foster a healthy ecosystem, the process for contributing a pack should be as low-friction as possible. This means pointing to a default branch instead of requiring contributors to manage immutable commit hashes.
4.  **Simplicity & Predictability**: The user-facing commands should be simple, and their behavior (especially network access) must be predictable. The user should always be in control.

## 3. Core Concepts

1.  **Community Pack**: A standard Rule Pack, conforming to the `pack_developer_guide.md`, hosted in a public GitHub repository.

2.  **Public Index Repository**: A single, official, public Git repository that serves as a curated list of community packs. Its core is a `packs.json` file.

3.  **Local Index Cache**: A local copy of the `packs.json` file stored on the user's machine. This cache is **only** updated when the user explicitly runs the `packs update` command.

## 4. Finalized CLI Behavior (MVP)

*   **`rulebook-ai packs list`**
    *   Displays a single, merged list of all packs available: built-in packs plus packs from the Local Index Cache.
    *   Community packs are marked, e.g., `python-pro-pack (community)`.
    *   This command **does not** access the network.

*   **`rulebook-ai packs update`**
    *   The **only** command that accesses the network to fetch the community index.
    *   Pulls the latest `packs.json` from the official `Index Repository` and updates the Local Index Cache.

*   **`rulebook-ai packs add <input>`**
    *   This command uses a two-step resolution logic to find the pack's source:
        1.  **Direct Git Location (Slug)**: First, it checks if the `<input>` string matches the GitHub slug format: `username/repository` or `username/repository/path/to/pack`. This is the designated method for installing unlisted packs.
        2.  **Named Pack (from Index)**: If the input is not a slug, the CLI searches for a pack with a matching `name` in the unified list (built-in and cached community packs).

    *   Once the pack's source repository is determined, the installation follows a strict, user-centric validation workflow:
        1.  **Clone**: The CLI checks the pack's index entry for an optional `commit` or `tag`.
            *   If a `commit` or `tag` is specified, the CLI clones that exact version. This is the most secure method.
            *   If not, the CLI clones the repository's default branch.
        2.  **Validate**: The CLI performs an automated validation on the cloned files.
            *   This includes ensuring they conform to the `pack_developer_guide.md` (e.g., a valid `manifest.yaml` and a `rules/` directory exist).
            *   As a critical integrity check, the validation **must** confirm that the `name` inside the pack's `manifest.yaml` exactly matches the name requested for installation. If they do not match, the installation must be aborted with an error.
        3.  **Warn & Confirm**:
            *   If validation fails, the installation is aborted with a clear error message.
            *   If validation succeeds, a clear warning is displayed.
                *   For packs with a specified `commit` or `tag`, the user is informed they are installing third-party code that has been pinned to a specific version.
                *   For packs without a `commit` or `tag`, a **stronger warning** is shown, explaining that the code is from the latest version of the default branch and could change at any time.
            *   In all cases, the user **must** explicitly confirm to proceed.
        4.  **Install**: Only after user confirmation does the CLI move the pack from the temporary directory to its final location in `.rulebook-ai/packs/`.

## 5. Contribution Workflow

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
