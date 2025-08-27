# AI Assistant - Workflow: Planning & Solution Proposal (FOCUS = PLANNING) (Simplified)
# Applies when internal mode is Plan Mode (Cline) / Architect Mode (Roo Code), OR when task FOCUS is PLANNING. Assumes General Principles (File 6) processed, including initial context gathering.

**(Rules for Planning, Analysis, and Solution Design)**

**Overall Goal:** Thoroughly understand the task, leverage project context to explore solutions, and produce a detailed, validated implementation plan.

## Process & Best Practices:

1.  **Clarify Requirements & Context:**
    *   Achieve 100% clarity on the specific task requirements via rigorous questioning and referencing initial context findings (relevant PRD scope, task status from `tasks_plan.md`). State assumptions.

2.  **Develop & Justify Solution:**
    *   **Analyze Context:** Deeply consider relevant constraints and patterns from `architecture.md`, `technical.md`, and the codebase.
    *   **Explore Options:** Brainstorm multiple solutions consistent with the project context.
    *   **Evaluate:** Analyze trade-offs (maintainability, performance, security, complexity, alignment with context).
    *   **Select & Justify:** Choose the optimal solution, clearly explaining *why* it's best in the context of the project and task requirements, referencing key architectural/technical alignments.

3.  **Create Detailed Implementation Plan:**
    *   Provide a step-by-step breakdown.
    *   For each step, specify key details ensuring alignment with project context:
        *   Affected components (ref: `architecture.md`).
        *   Key algorithms/data structures (ref: `technical.md`, codebase patterns).
        *   APIs interactions (endpoints, contracts per standards).
        *   Required error handling, security measures, logging (per standards in `technical.md`).
        *   Testing strategy (unit tests, integration points).
        *   Documentation needs (comments, docstrings).
        *   Dependencies (components, libraries, tasks).

4.  **Assess Impact & Request Validation:**
    *   Briefly assess potential impacts on Memory Bank files (e.g., does this change architecture or introduce new patterns needing documentation?). Note these potential updates.
    *   Present the structured plan, including justification and impact assessment. **Request human review and approval**, specifically asking for validation of context alignment.

**(End of Planning Workflow - Simplified)**