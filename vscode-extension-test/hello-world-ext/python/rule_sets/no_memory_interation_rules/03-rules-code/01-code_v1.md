# AI Assistant - Workflow: Implementation & Coding (FOCUS = IMPLEMENTATION)
# Applies when internal mode is Act Mode (Cline) / Code Mode (Roo Code) for an implementation task, OR when task FOCUS is IMPLEMENTATION.
# Assumes General Principles (File approx. 6) processed AND an approved Implementation Plan exists.

**(Rules for writing/modifying code based on a plan follow)**

**Overall Goal:** Faithfully and accurately execute the steps outlined in the approved implementation plan, applying rigorous checks and adhering to all standards, producing high-quality code and tests. This mode focuses purely on *implementation*, not re-evaluation or significant deviation from the plan, and invokes Debug Mode when necessary.

## Process & Best Practices:

1.  **Acknowledge Plan:**
    *   Confirm receipt of the **approved** implementation plan. Briefly acknowledge the main objective based on the plan.

2.  **Execute Plan Steps Incrementally & Safely:**
    *   For each major step/feature outlined in the approved plan:
        *   **a. Pre-Change Analysis (Safety Check):**
            *   Identify the specific files/components targeted by *this step* of the plan.
            *   Perform focused Dependency Analysis: What *immediate* dependencies exist for the code being changed? How might this specific change cascade locally?
            *   Perform focused Flow Analysis: Briefly trace the execution flow relevant *only* to the change being made in this step.
            *   *If this analysis reveals a significant conflict with the plan or unforeseen major impact, **HALT execution** and report the issue. Recommend initiating **Debug Mode** or requesting a plan revision.*
        *   **b. Implement Planned Change:**
            *   Write or modify the code precisely as specified in the plan for this step.
            *   Apply *all* General and Project-Specific Standards (coding style, security, readability, etc.).
            *   Prioritize reuse (`reuse`), preserve working components (`code_preservation`), ensure seamless integration (`architecture_preservation`), and maintain modularity (`modularity`, `file_management`).
        *   **c. Pre-Commit Simulation (Safety Check):**
            *   Mentally trace execution or perform dry runs for the *specific change* just made.
            *   Analyze impacts on expected behavior and potential edge cases related to *this change*.
            *   *If simulation reveals unexpected side effects or breaks existing logic related to the change, **HALT execution**, revert the problematic part of the change, and initiate **Debug Mode** for this specific issue.*
        *   **d. Iterate:** Continue implementing sub-parts of the current plan step, repeating a-c as needed for logically distinct changes within the step.

3.  **Develop Comprehensive Tests (Post-Implementation per Step/Feature):**
    *   Based on the plan's testing strategy and the implemented code for the completed step/feature:
        *   **Test Plan Adherence:** Implement tests covering scenarios outlined in the plan (edge cases, validations).
        *   **Dependency-Based Tests:** Write unit tests for new functions/classes. Ensure tests cover interactions with immediate dependencies.
        *   **Separate Test Files:** Place test logic in separate files from implementation code.
        *   **No Breakage Goal:** Run relevant existing tests (if possible/specified) plus new tests. *If any test fails, **HALT execution** and initiate **Debug Mode**.*

4.  **Document Code as Planned:**
    *   Add code comments and documentation (docstrings, etc.) for the implemented code as specified in the plan and per General standards. Focus on the 'why' for complex parts.

5.  **Handle Plan Deviations/Completion:**
    *   If *all* steps are completed and tests pass, report completion.
    *   If execution was halted due to plan infeasibility, failed simulation, or failed tests (and Debug Mode was invoked), report the final status *after* the Debug Mode attempt concludes (whether successful or not).

6.  **(Optional) Final Optimization:** If specified by the plan or as a general rule, perform safe code optimizations *after* all functionality is implemented and verified.