# Implementation Plan: Community Pack Ecosystem

### Guiding Principle

The most fundamental action is **installing a single, known pack from a direct source**. Everything else—discovery, listing, updating an index—is a layer of abstraction on top of that core capability.

---

### Phase 1: The Core Engine - Installing a Pack by Direct URL

**Objective:** To create a robust, secure mechanism for adding a single pack from a specified Git repository. This phase completely ignores the community index.

1.  **Task: Implement the "Add by Slug" Logic**
    *   Modify the `packs add` command to recognize a GitHub slug (e.g., `username/repository` or `username/repository/path`).
    *   Parse the slug to determine the repository URL.

2.  **Task: Develop the Secure Fetch-and-Validate Workflow**
    *   Create a function that, given a repository URL:
        a. Clones the repository's default branch into a secure, temporary directory.
        b. **Validates** the contents of the temporary directory against the `pack_developer_guide.md` (e.g., `manifest.yaml` and `rules/` exist).
        c. **Verifies Identity:** Parses the `manifest.yaml` and confirms its `name` is valid, not reserved by built-in packs, and not already installed from a different source.
        d. **Returns** the validated pack's temporary path or throws an error.

3.  **Task: Implement User Confirmation and Installation**
    *   If validation succeeds, present a clear warning to the user that they are installing un‑audited code from a direct URL.
    *   Require explicit user confirmation (`y/n`).
    *   Before moving files, check whether `.rulebook-ai/packs/<name>` already exists; abort if it comes from a different source.
    *   Upon confirmation, move the pack from the temporary directory into `.rulebook-ai/packs/<name>`.
    *   Ensure the temporary directory is always cleaned up, especially on error.

**Outcome of Phase 1:** A user can reliably and securely install any compatible pack if they know its GitHub URL slug (e.g., `rulebook-ai packs add my-org/my-cool-pack`).

---

### Phase 2: The Discovery Layer - The Community Index

**Objective:** To introduce the concept of a community index that users can refresh, enabling installation by name instead of by URL.

1.  **Task: Implement the Local Cache**
    *   Store the local index cache inside the Python package at `rulebook_ai/community/index_cache/packs.json` so all repositories share one updated index.
    *   Create functions to read from and write to this cache file.

2.  **Task: Implement the `packs update` Command**
    *   This is the only command that will access the network for the index.
    *   Fetch the `packs.json` from the hardcoded official Index Repository URL.
    *   Validate the JSON structure and required fields.
    *   Replace the local cache only on success; otherwise retain the previous file and report an error.

3.  **Task: Enhance `packs add` to Use the Index**
    *   Update the command's logic:
        a. First, check if the given `<input>` is a slug. If so, use the Phase 1 workflow.
        b. If not a slug, search for a pack with a matching `name` in the local index cache.
        c. If found, use the `repo`, `commit`, or `tag` from the index entry to fuel the secure fetch-and-validate workflow from Phase 1.
        d. Abort if the resolved `name` already exists locally from a different source.
        e. Adjust warning messages based on whether the pack is pinned to a commit or tag.

**Outcome of Phase 2:** A user can run `packs update` to discover new packs and then install them by their simple name (e.g., `rulebook-ai packs add python-pro-pack`).

---

### Phase 3: The UI Layer - Listing and Visibility

**Objective:** To provide users with a clear, unified view of all packs available to them.

1.  **Task: Implement Built-in Pack Discovery**
    *   Create a mechanism for the CLI to be aware of its own bundled, built-in packs.

2.  **Task: Implement the `packs list` Command**
    *   This command will **not** access the network.
    *   It will read the list of built-in packs.
    *   It will read the list of community packs from the local cache (from Phase 2).
    *   It will present a single, merged list to the user, clearly distinguishing between `(built-in)` and `(community)` packs and showing metadata like the summary.

**Outcome of Phase 3:** A user can run `packs list` to see all installable packs from all sources at a glance.

---

### Phase 4: The Ecosystem - Contributor Tooling

**Objective:** To set up the external infrastructure needed for the community to thrive.

1.  **Task: Create the Public Index GitHub Repository**
    *   Initialize a new, public repository on GitHub.
    *   Add the initial `packs.json` file.
    *   Add a `README.md` explaining its purpose.
    *   Add a `CONTRIBUTING.md` that explains the submission process (this can be adapted from the main `spec.md`).

2.  **Task: Implement the CI Validation Workflow**
    *   Create a GitHub Actions workflow within the new Index Repository.
    *   This workflow will trigger on Pull Requests.
    *   It will run a script that performs the critical validation checks defined in the spec (e.g., cloning the submitted pack, checking its structure, and verifying the manifest name matches the index name).

**Outcome of Phase 4:** The community has a place to submit packs and a clear, automated process for validating their submissions, completing the ecosystem loop.
