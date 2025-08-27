# AI Assistant - Workflow: Debugging & Error Fixing (FOCUS = DEBUGGING) (Simplified)
# Applies when internal mode is Act Mode (Cline) / Debug Mode (Roo Code) for a debugging task, OR when task FOCUS is DEBUGGING. Assumes General Principles (File 6) processed.

**(Rules for diagnosing and fixing errors)**

**Overall Goal:** Systematically diagnose, fix, and verify errors, leveraging project context and documenting findings.

## Process & Best Practices:

1.  **Gather Context & Reproduce:**
    *   Collect all available information (error messages, logs, steps, failing task context).
    *   Check relevant Memory Files (`tasks_plan.md`, `active_context.md`, `error-documentation.md` for similar issues).
    *   Reproduce the failure if possible.

2.  **Analyze in Context:**
    *   Perform detailed error analysis (stack traces, code).
    *   Interpret findings **within the context of `architecture.md` and `technical.md`/codebase patterns.** Identify potential violations or unexpected interactions.

3.  **Hypothesize & Reason:** Formulate potential root causes, reasoning through evidence and context. Check `error-documentation.md`/`lessons-learned.md`.

4.  **Identify Cause & Plan/Validate Fix:** Pinpoint the root cause. Outline the minimal fix. **Verify the fix aligns with `architecture.md` and `technical.md`.** Note if analysis suggests flaws in documentation.

5.  **Implement & Verify Fix:** Apply the fix adhering to standards. Rerun failed tests and related tests. Add a new test for the bug if appropriate.

6.  **Handle Persistence:** If stuck after reasonable attempts, state difficulty, approaches tried (including context analysis), and request human help.

7.  **Report Outcome & Propose Updates:** Report success/failure. Provide corrected code/tests if successful. Propose updates to key Memory Files: **`error-documentation.md` (Mandatory)**, `tasks_plan.md`, `active_context.md`, potentially `lessons-learned.md` or flags for core docs.

**(End of Debugging Workflow - Simplified)**