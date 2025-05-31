# AI Assistant - Workflow: Implementation & Coding (FOCUS = IMPLEMENTATION) (Simplified)
# Applies when internal mode is Act Mode (Cline) / Code Mode (Roo Code) for an implementation task, OR when task FOCUS is IMPLEMENTATION. Assumes General Principles (File 6) processed and an approved Plan exists.

**(Rules for writing/modifying code based on a plan)**

**Overall Goal:** Faithfully execute the approved plan, ensuring code aligns with project context and standards, producing high-quality code and tests.

## Process & Best Practices:

1.  **Acknowledge Plan & Context:** Confirm understanding of the plan for the specific task and its key context/constraints.

2.  **Execute Plan Steps Incrementally:**
    *   For each major step in the plan:
        *   **Prepare & Validate Step:** Before coding, briefly re-verify the planned action against relevant context (`architecture.md` boundaries, `technical.md` standards/patterns, `active_context.md`). Perform quick dependency/flow analysis for immediate impacts. **Halt and report** if significant conflicts with the approved plan or context are found.
        *   **Implement & Verify:** Write/modify code precisely as planned, strictly applying project standards (`technical.md`, style guides) and respecting architecture (`architecture.md`). Perform mental/dry runs. Check for obvious side effects. If issues arise, attempt self-correction or initiate **Debug Mode**.

3.  **Develop Tests:** Implement unit tests as per the plan's strategy, covering specified scenarios and interactions. Run tests; if failures occur, initiate **Debug Mode**.

4.  **Document Code:** Add comments and documentation as planned and per standards.

5.  **Report Completion & Propose Updates:**
    *   If halted due to issues, report status after Debug attempt.
    *   If successful: Report completion. Propose concise updates to key Memory Files: `tasks_plan.md` (status), `active_context.md` (state), `error-documentation.md` / `lessons-learned.md` (if applicable based on experience).

**(End of Implementation Workflow - Simplified)**