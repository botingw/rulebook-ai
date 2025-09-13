# AI Assistant - Workflow: Debugging & Error Fixing (FOCUS = DEBUGGING) (Enhanced)
# Applies when internal mode is Act Mode (Cline) / Debug Mode (Roo Code) for a debugging task, OR when task FOCUS is DEBUGGING.
# Assumes General Principles (File approx. 6 - Enhanced) processed.

**(Rules for diagnosing and fixing errors follow)**

**Overall Goal:** Systematically diagnose the root cause of a specific failure, leveraging project context, propose/implement a correct fix consistent with standards, verify its effectiveness, and document the findings.

## Process & Best Practices:

1.  **Diagnose & Reproduce (Context-Driven):**
    *   **Gather All Context:** Collect error messages, logs, symptoms, steps to reproduce, the plan step/code change being executed when failure occurred.
    *   **Mandatory Memory Consult:** Gather relevant context from:
        *   `tasks_plan.md` (Original goal of the failing task, related issues).
        *   `active_context.md` (Recent changes, what was being attempted).
        *   `error-documentation.md` (Check for similar past issues/solutions).
    *   Reproduce the failure consistently (if possible). Request steps if needed.

2.  **Analyze & Understand (Context-Aware):**
    *   Perform detailed Error Analysis (stack traces, messages, code sections). Use tools if applicable.
    *   **Mandatory Memory Consult:** Conduct focused Dependency/Flow analysis around the failure point, interpreting findings **in the context of `architecture.md`** (component interactions, boundaries) and relevant code patterns from **`technical.md`** or the codebase.
    *   Understand *exactly* why the failure is occurring at a code level, considering potential violations of architectural or technical constraints.

3.  **Hypothesize & Reason:**
    *   Formulate potential root causes (logic error, incorrect assumption, interaction issue, architectural mismatch, environmental issue, violation of `technical.md` standards).
    *   Rigorously reason through evidence (logs, code, test results, Memory Bank context) to confirm/deny hypotheses.
    *   Look for similar patterns solved previously (`error-documentation.md`, `lessons-learned.md`, codebase, web search per general guidelines).

4.  **Identify Root Cause & Plan Fix (Validation):**
    *   Pinpoint the specific root cause with high confidence.
    *   Briefly outline the minimal necessary change to correct the issue.
    *   **Validate Fix Plan:** Ensure the proposed fix itself is consistent with `architecture.md` and `technical.md`. Consider side effects.
    *   **Flag Doc Issues:** If the root cause suggests a flaw or ambiguity in requirements, `architecture.md`, or `technical.md`, **explicitly note this** as needing attention.

5.  **Implement & Verify Fix:**
    *   Apply the fix. **Follow core implementation principles where applicable** (apply standards from `technical.md`, respect `architecture.md`, simulate mentally).
    *   Rerun the specific test(s) that initially failed.
    *   Run directly related tests to check for regressions.
    *   Add a new test specifically for the bug fixed, if appropriate.

6.  **Handle Persistence / Getting Stuck:**
    *   If debugging fails after reasonable attempts:
        *   Try a different diagnostic approach.
        *   Explicitly state the difficulty, approaches tried, why they failed, referencing analysis against Memory Bank context.
        *   Request human assistance or suggest stepping back. Do not loop indefinitely.

7.  **Report Outcome & Propose Memory Updates:**
    *   Report clearly: Was the issue diagnosed, fixed, and verified?
    *   If debugging failed, report findings, last state, reason for being stuck.
    *   Provide corrected code and new tests (if successful).
    *   **Propose Specific Memory Updates:**
        *   **Mandatory:** `error-documentation.md` (Document the problem, root cause, and solution/fix).
        *   `tasks_plan.md` / `active_context.md` (Update status of the affected task).
        *   `lessons-learned.md` (If the fix revealed a broader pattern or important learning).
        *   Potentially flag need for updates to `architecture.md` or `technical.md` if a root cause was traced back to them.
    *   Indicate completion of Debug Mode.

**(End of Debugging Workflow - Enhanced)**