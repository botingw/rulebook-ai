# ADR-001: Composable Packs Architecture

*   **Status:** Accepted
*   **Date:** 2025-09-04
*   **Context:** The original `rulebook-ai` framework used a monolithic "Rule Set" model. This made it difficult to combine different AI personas (e.g., a "Project Manager" and a "Frontend Developer") in a single project, as their rules, memory, and tools could not be managed independently. An alternative design proposed keeping each Pack's files completely isolated, but this would make the context invisible to the AI assistants, defeating the project's primary goal.
*   **Decision:** We will adopt a "best of both worlds" hybrid design. We will introduce modular "Packs" that are managed by the CLI. The framework will compose a unified, top-level `memory/` and `tools/` directory via a non-destructive, ordered merge of the active packs' starter files. This makes the context visible to the AI while preventing user data loss. AI rules will be concatenated in order.
*   **Consequences:** This decision leads to the architecture detailed in the summary table below, which combines the essential unified context model with superior metadata (`manifest.yaml`) and state management (`selection.json`).

---

### Critical Analysis: The Core Flaw in the Isolation Model

An alternative design proposed **"Isolation over merging"** for tools and context.

*   **Its Stated Advantage:** It perfectly prevents file-system conflicts. This is 100% true.
*   **Its Unstated but Fatal Flaw:** It fundamentally breaks the principle that **AI Context is King**.

If the context files remain isolated inside separate pack directories, the AI assistant (Cursor, CLINE, etc.) doesn't know to look there. The whole purpose of this framework is to *surface* the combined context into a location the AI can easily see and ingest. Keeping the context files buried in separate, isolated folders makes them invisible to the AI without significant manual work from the user.

**Conclusion:** The principle of strict isolation for `context` and `tools` is a non-starter. The principle of composing a unified, top-level `memory/` and `tools/` directory is correct because it serves the primary goal.

---

### Summary of Final Design Decisions

| Feature | Original Proposal | Alternative (Isolation) | Final Hybrid Design | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Context/Tools** | Unified `memory/` & `tools/` via merging. | Kept isolated in `packs/`. | **Unified `memory/` & `tools/` via non-destructive merging.** | **This is the core decision.** A unified context is essential for the AI to function as intended. User experience is also far better. |
| **State Management** | `active_profiles.json` | `selection.lock.json` | **`.rulebook/selection.json`** | Adopted clearer naming and a dedicated hidden directory for all framework internals, keeping the project root cleaner. |
| **Metadata** | Implicit (directory name). | `manifest.yaml` | **`manifest.yaml` per pack.** | Excellent idea. Makes the framework more robust, descriptive, and future-proof (for versions, dependencies, etc.). |
| **Documentation** | Not explicitly defined. | `README.md` per ruleset. | **`README.md` per pack.** | Perfect for human-readable setup and usage instructions. Keeps the manifest clean. |
| **Tool Execution** | (Not specified) | Optional `runners/`. | **README-driven setup.** | Correctly identified as over-engineering for v1. Simple instructions in a README are more flexible and transparent. |
| **Rule Composition** | Merged and generated. | Merged into `COMBINED.md`. | **Merged into a single file per assistant.** | Both designs agreed on this. Concatenation is the most reliable method for ensuring rule order is respected by all platforms. |
