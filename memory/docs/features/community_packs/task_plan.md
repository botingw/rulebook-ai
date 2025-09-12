# Task Plan: Community Pack Ecosystem

## 🌟 Goal

Track the implementation work required to support third-party rule packs.

---

### Phase 1: Core Engine (Add by Source)

**Description:** Allow installation from explicit sources like a GitHub repository or a local path.

| Task ID | Description | Importance | Status | Dependencies |
|:-------|:------------|:----------|:------|:-------------|
| **1.0** | Set up mock Git repos & test index for integration tests. | P0 | Done | - |
| **1.1** | Update `packs add` to resolve repository slugs via the `github:` prefix. | P0 | Done | 1.0 |
| **1.2** | Implement `packs add` with the `local:` prefix to install from a local filesystem path. | P0 | Done | - |
| **1.3** | Fetch repository to temp dir and validate per `pack_developer_guide.md`. | P0 | Done | 1.1 |
| **1.4** | Prompt user, ensure `.rulebook-ai/packs/<name>` is free, then install. | P0 | Done | 1.2, 1.3 |
| **1.5** | Persist source metadata to pack and selection files; verify against built-in names. | P0 | Done | 1.4 |

### Phase 2: Community Index

**Description:** Introduce discoverability via shared index cache.

| Task ID | Description | Importance | Status | Dependencies |
|:-------|:------------|:----------|:------|:-------------|
| **2.1** | Maintain local index cache at `rulebook_ai/community/index_cache/packs.json`. | P0 | Done | 1.4 |
| **2.2** | Implement `packs update` to fetch and validate `packs.json`. | P0 | Done | 2.1 |
| **2.3** | Extend `packs add` to resolve by `name` using the cache with collision checks. | P0 | Done | 2.2 |

### Phase 3: Listing and Visibility

**Description:** Provide unified view of available packs.

| Task ID | Description | Importance | Status | Dependencies |
|:-------|:------------|:----------|:------|:-------------|
| **3.1** | Enumerate built-in packs for the CLI. | P1 | Done | 2.3 |
| **3.2** | Implement `packs list` merging built-in and community entries. | P1 | Done | 3.1 |

### Phase 4: Ecosystem Infrastructure

**Description:** Enable community contributions via public index.

| Task ID | Description | Importance | Status | Dependencies |
|:-------|:------------|:----------|:------|:-------------|
| **4.1** | Create public Index Repository with `packs.json` and docs. | P2 | In Progress | 3.2 |
| **4.2** | Add CI workflow to validate submitted packs. | P2 | In Progress | 4.1 |
