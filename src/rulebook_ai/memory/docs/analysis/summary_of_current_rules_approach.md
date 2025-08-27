# Summary of Original Rules' Approach to Project Complexity

This document summarizes the core approach defined in the initial set of rules (v1) for enabling AI assistants to handle complex software projects, focusing on project management, task tracking, and context awareness via the memory bank.

The approach is built on the following pillars:

1.  **Mode-Based Operation & Separation of Concerns:**
    *   Defines distinct operational modes (Planning, Implementation, Debugging) based on user command or inferred intent (`00-meta-rules.md`).
    *   Assigns specific workflows and rule files (`01-plan_v1.md`, `01-code_v1.md`, `01-debug_v1.md`) to each mode, focusing the AI's cognitive effort.

2.  **Centralized & Structured Project Memory:**
    *   Establishes a "Memory Bank" using specific, defined files (`01-memory.md`) to store critical project context:
        *   `product_requirement_docs.md`: Project purpose and goals.
        *   `architecture.md`: System structure and component relationships.
        *   `technical.md`: Tech stack, patterns, constraints.
        *   `tasks_plan.md`: Backlog, status, known issues.
        *   `active_context.md`: Current work focus, recent changes.
        *   `error-documentation.md`, `lessons-learned.md`: Capturing historical issues/fixes and evolving project intelligence.
    *   Aims to provide a persistent, shared understanding.

3.  **Prioritization of Internal Context:**
    *   General rules (`06-rules_v1.md`) mandate consulting internal project resources (Task Tracker, Memory Files, Codebase) *before* external searches, grounding the AI in project specifics.

4.  **Structured Workflows for Interaction:**
    *   Defines procedural workflows (PLAN/ACT in `01-memory.md`, plus mode-specific ones).
    *   The **PLANNING** mode emphasizes rigorous requirement analysis, solution exploration, and detailed plan creation *before* coding.
    *   The **IMPLEMENTATION** mode focuses on faithfully *executing* an approved plan.
    *   The **DEBUGGING** mode follows a systematic diagnostic process.

5.  **Emphasis on Software Engineering Best Practices:**
    *   General rules (`06-rules_v1.md`) enforce foundational principles (Readability, Consistency, Robustness, Security, DRY, etc.) essential for managing complexity.

**In essence, the original rules aim to manage complexity by:**

*   Structuring the AI's thought process into distinct phases.
*   Providing a persistent, organized knowledge base (Memory Files).
*   Forcing the AI to consult and prioritize this internal knowledge.
*   Mandating planning before implementation.
*   Applying standard software engineering discipline.