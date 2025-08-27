# Rule Enhancements for Memory Bank Interaction

This document outlines suggestions for improving the AI assistant's rules to foster better, more proactive interaction with the project's memory bank files. The goal is to reduce errors caused by missed context and improve overall alignment with project requirements, architecture, and status.

## Overall Approaches

1.  **Shift from Passive Reference to Active Integration:** Embed specific checks and consultations of memory files *into* the steps of each operational workflow (Plan, Code, Debug), rather than just having them passively available.
2.  **Mandate Cross-Referencing and Validation:** Explicitly require the AI to validate its understanding, plans, and code *against* relevant memory files *before* proceeding or presenting results.
3.  **Contextual Prompts:** Add rules that prompt the AI to ask itself internal questions related to the memory bank based on the current task (e.g., "Does this align with the PRD?").
4.  **Structured Memory Updates:** Refine the process for updating memory files, making it a more integral part of completing tasks or learning.

## Specific Refinements to Rules

### 1. Refine `00-meta-rules.md`
    *   **Memory File Prioritization:** Briefly reiterate that *consulting relevant memory files* is a prerequisite for applying *any* workflow focus.

### 2. Enhance `06-rules_v1.md` (General Principles)
    *   **Strengthen "Prioritize Internal Context":**
        *   Mandate active search and synthesis from key memory files (`product_requirement_docs.md`, `architecture.md`, `technical.md`, `tasks_plan.md`) *before* generating plans, code, or hypotheses. Require stating key findings/constraints derived.
        *   Require explicit statement on how proposed changes relate to existing patterns (`technical.md`, codebase).
    *   **Add "Memory Consistency Check" Principle:** Require proposals, code, and analysis to be consistent with documented state/standards (`tasks_plan.md`, `active_context.md`, `architecture.md`, `technical.md`, `product_requirement_docs.md`). Highlight and justify necessary deviations.

### 3. Integrate Memory Deeply into `01-plan_v1.md` (FOCUS = PLANNING)
    *   **Step 1 (Deep Dive):** Mandate consulting `product_requirement_docs.md` and `tasks_plan.md`. Reference findings.
    *   **Step 2 (Decompose & Explore):** Mandate consulting `architecture.md` and `technical.md` *before* brainstorming. Solutions MUST consider these constraints.
    *   **Step 3 (Evaluate & Select):** Evaluation criteria MUST include alignment with `architecture.md`, `technical.md`, `product_requirement_docs.md`. Justify selection referencing these documents.
    *   **Step 4 (Detailed Plan):** Require mapping plan steps to `architecture.md` components. Ensure consistency with `technical.md`. Verify plan satisfies `product_requirement_docs.md`.
    *   **Add Step: "Memory Impact Assessment":** Before presenting the plan, assess and note potential updates needed for memory files.

### 4. Integrate Memory Deeply into `01-code_v1.md` (FOCUS = IMPLEMENTATION)
    *   **Step 2a (Pre-Change Analysis):** Mandate cross-referencing planned change against `architecture.md`, `technical.md`, and `active_context.md` *before* coding. Confirm adherence or note discrepancies.
    *   **Step 2b (Implement):** Add reference to applying standards from `technical.md` and matching `architecture.md` components.
    *   **Add Step: "Post-Implementation Memory Check":** Briefly re-verify adherence to constraints checked in Step 2a after implementation.
    *   **Step 5 (Handle Plan Deviations/Completion):** Upon success, *propose specific updates* to `tasks_plan.md`, `active_context.md`, and potentially `lessons-learned.md` or `error-documentation.md`.

### 5. Integrate Memory Deeply into `01-debug_v1.md` (FOCUS = DEBUGGING)
    *   **Step 1 (Diagnose & Reproduce):** Mandate gathering context from `tasks_plan.md`, `active_context.md`, logs, and check `error-documentation.md`.
    *   **Step 2 (Analyze & Understand):** Mandate analysis within the context of `architecture.md` and `technical.md`/codebase patterns.
    *   **Step 4 (Identify Root Cause & Plan Fix):** Ensure fix consistency with `architecture.md` and `technical.md`. Note if docs need updates.
    *   **Step 7 (Report Outcome):** Propose updates for `error-documentation.md`, `tasks_plan.md`, `active_context.md` upon success or failure.

### 6. Enhance Memory File Specific Rules (e.g., `04-architecture-understanding.md`)
    *   Make parsing/understanding more actionable by specifying *how* to use the information during planning and implementation (e.g., check boundaries, ripple effects). Add similar usage rules for `technical.md`.

### 7. Refine Memory Update Workflow (`01-memory.md`)
    *   Clarify *when* to update vs. *propose* updates (proposing changes to core docs like `architecture.md` is often safer).
    *   Integrate update proposals into the end of relevant workflows (Plan, Code, Debug).