# AI Assistant - Workflow: Debugging & Error Fixing (FOCUS = DEBUGGING)
# Applies when internal mode is Act Mode (Cline) / Debug Mode (Roo Code) for a debugging task, OR when task FOCUS is DEBUGGING.
# Assumes General Principles (File approx. 6) processed.

**(Rules for diagnosing and fixing errors follow)**

**Overall Goal:** Systematically diagnose the root cause of a specific failure identified during implementation (or reported as a bug) and propose/implement a correct fix, verifying its effectiveness.

## Process & Best Practices:

1.  **Diagnose & Reproduce:**
    *   Gather all context provided about the failure: Specific error messages, logs, symptoms, the plan step/code change being executed when failure occurred.
    *   Reproduce the failure consistently (if possible). Request steps if needed.

2.  **Analyze & Understand:**
    *   Perform detailed Error Analysis: Examine stack traces, error messages, relevant code sections. Use logging/debugging tools if applicable.
    *   Conduct focused Dependency/Flow analysis around the failure point, using internal KB and codebase knowledge.
    *   Understand *exactly* why the failure is occurring at a code level.

3.  **Hypothesize & Reason:**
    *   Formulate potential root causes (e.g., logic error in new code, incorrect assumption, unexpected interaction with existing code, architectural mismatch, environmental issue).
    *   Rigorously reason through evidence (logs, code behavior, test results) to confirm or deny hypotheses.
    *   Look for similar patterns previously solved (internal error documentation, codebase, web search following general guidelines).

4.  **Identify Root Cause & Plan Fix:**
    *   Pinpoint the specific root cause with high confidence.
    *   Briefly outline the minimal necessary change to correct the issue. Consider potential side effects of the fix itself.

5.  **Implement & Verify Fix:**
    *   Apply the fix. **Follow the core implementation principles from Code Mode where applicable** (e.g., apply standards, consider dependencies, simulate the fix mentally).
    *   Rerun the specific test(s) that initially failed.
    *   Run any directly related tests to check for regressions caused by the fix.
    *   Add a new test specifically for the bug fixed, if appropriate and feasible.

6.  **Handle Persistence / Getting Stuck:**
    *   If debugging fails after reasonable attempts (multiple cycles of analysis/fix attempts):
        *   Try a different diagnostic approach (e.g., different logging, simplifying the code temporarily).
        *   Explicitly state the difficulty, the approaches tried, and why they failed.
        *   Request human assistance or suggest stepping back for a higher-level review. Do not loop indefinitely.

7.  **Report Outcome:**
    *   Report clearly whether the issue was successfully diagnosed, fixed, and verified (with passing tests).
    *   If debugging failed, report the findings, the last state attempted, and the reason for being stuck.
    *   Provide the corrected code (if successful) and any new tests added.
    *   Indicate completion of Debug Mode so the calling process (e.g., Code Mode or user) knows the status.