# Refactoring Task Plan

## 🎯 Goal

This document breaks down the work required for the internal refactoring of the `rulebook-ai` core and CLI components. The primary objective is to improve code modularity, maintainability, and extensibility by abstracting the logic for each AI assistant.

This plan is derived from the full technical design, which can be found in the [Refactoring Plan](./refactoring_plan.md).

---

### Phase 1: Abstract AI Assistants in `core.py`

**Description:** This phase focuses on creating a new object-oriented abstraction for AI assistants to decouple the core logic from assistant-specific implementations.

| Task ID | Description                                                                              | Importance | Status      | Dependencies      |
|:--------|:-----------------------------------------------------------------------------------------|:-----------|:------------|:------------------|
| **1.1** | Define the `Assistant` abstract base class or `Protocol` in `core.py`.                   | P0         | Not Started | -                 |
| **1.2** | Implement concrete classes for each assistant: `Cursor`, `Windsurf`, `Cline`, `RooCode`.   | P0         | Not Started | 1.1               |
| **1.3** | Create the `AssistantRegistry` to hold and manage all `Assistant` objects.               | P0         | Not Started | 1.2               |
| **1.4** | Refactor `RuleManager` to be an orchestrator that uses the `AssistantRegistry`.            | P0         | Not Started | 1.3               |
| **1.5** | Implement `CopilotAssistant` and integrate it into the registry.                         | P1         | Not Started | 1.4               |

### Phase 2: Simplify and Decouple `cli.py`

**Description:** This phase refactors the command-line interface to reduce code duplication and better separate its concerns from the core business logic.

| Task ID | Description                                                                              | Importance | Status      | Dependencies      |
|:--------|:-----------------------------------------------------------------------------------------|:-----------|:------------|:------------------|
| **2.1** | Create a helper function in `cli.py` to add assistant arguments to the `install`/`sync` commands. | P1         | Not Started | -                 |
| **2.2** | Refactor `cli.py` command handlers to use the new `RuleManager` methods and registry.      | P1         | Not Started | 1.4               |
| **2.3** | Move the `doctor` command's implementation logic from `cli.py` to `core.py`.             | P2         | Not Started | -                 |

### Phase 3: Verification

**Description:** This final phase ensures that the refactoring has not introduced any regressions and that the tool's behavior remains unchanged from a user's perspective.

| Task ID | Description                                                                              | Importance | Status      | Dependencies      |
|:--------|:-----------------------------------------------------------------------------------------|:-----------|:------------|:------------------|
| **3.1** | After refactoring, run all existing unit and integration tests to check for regressions.   | P0         | Not Started | 1.4, 2.2          |
| **3.2** | Manually test the CLI commands (`install`, `sync`, `clean-rules`, etc.) to verify behavior. | P0         | Not Started | 1.4, 2.2          |